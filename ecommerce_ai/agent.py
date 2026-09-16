# ===============================================================================#
# ================================= Agent =======================================#
# ===============================================================================#

from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from memory.summary_memory import (
    get_compact_memory,
    update_compact_memory
)

from pydantic import ValidationError
from schemas import UserRequest

from models import agent_llm
from tools import tools
from prompt import prompt

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


# ===============================================================================#
# ================================ LLM ==========================================#
# ===============================================================================#

# Bind tools to the agent LLM
llm_with_tools = agent_llm.bind_tools(tools)


# ===============================================================================#
# ================================= State =======================================#
# ===============================================================================#

class AgentState(TypedDict):
    session_id: str
    query: str
    memory_context: str
    messages: Annotated[list, add_messages]
    final_answer: str


# ===============================================================================#
# =========================== Memory Routing ====================================#
# ===============================================================================#

def check_memory_need(state: AgentState):

    query = state["query"].lower().strip()

    memory_keywords = [

        # -----------------------------------------------------------------------#
        # Previous conversation
        # -----------------------------------------------------------------------#

        "previous",
        "earlier",
        "before",
        "last time",
        "you remember",
        "remember when",
        "what did i tell you",
        "what did i say",
        "as i said",
        "as before",

        # -----------------------------------------------------------------------#
        # User-specific preferences
        # -----------------------------------------------------------------------#

        "for me",
        "my preference",
        "my preferences",
        "my budget",
        "my requirements",
        "my needs",
        "my choice",
        "my favorite",
        "i prefer",
        "i preferred",

        # -----------------------------------------------------------------------#
        # Conversation continuation
        # -----------------------------------------------------------------------#

        "again",
        "another one",
        "something else",
        "what about",
        "which one for me",

        # -----------------------------------------------------------------------#
        # Personalized recommendations
        # -----------------------------------------------------------------------#

        "recommend me",
        "recommend for me",
        "what should i buy",
        "what do you recommend"
    ]

    needs_memory = any(
        keyword in query
        for keyword in memory_keywords
    )

    if needs_memory:

        print("🧠 Memory needed → loading memory")

        return "load_memory"

    print("⚡ Memory not needed → skipping memory")

    return "call_model"


# ===============================================================================#
# ================================ Load Memory ==================================#
# ===============================================================================#

async def load_memory(state: AgentState):

    memory = await get_compact_memory(
        state["session_id"]
    )

    print("\n========== MEMORY ==========")
    print(memory)
    print("============================\n")

    return {
        "memory_context": f"""
Summary:
{memory["summary"]}

Important keywords:
{", ".join(memory["keywords"])}
"""
    }


# ===============================================================================#
# ================================== Model ======================================#
# ===============================================================================#

async def call_model(state: AgentState):

    messages = [
        {
            "role": "system",
            "content": prompt.format(
                memory_context=state["memory_context"]
            )
        }
    ]

    # Add memory only if it was loaded
    if state["memory_context"]:
        messages.append(
            {
                "role": "system",
                "content": state["memory_context"]
            }
        )

    # ============================================================
    # Keep only the most recent conversation messages
    # ============================================================

    conversation_messages = state["messages"]

    MAX_MESSAGES = 10

    if len(conversation_messages) > MAX_MESSAGES:
        conversation_messages = conversation_messages[-MAX_MESSAGES:]

        print(
            f"✂️ Conversation history trimmed "
            f"to last {MAX_MESSAGES} messages."
        )

    messages.extend(conversation_messages)

    response = await llm_with_tools.ainvoke(
        messages
    )

    return {
        "messages": [response]
    }



    # ---------------------------------------------------------------------------#
    # Add memory only if it was loaded
    # ---------------------------------------------------------------------------#

    if state["memory_context"]:

        messages.append(
            {
                "role": "system",
                "content": state["memory_context"]
            }
        )

    # ---------------------------------------------------------------------------#
    # Add user / conversation messages
    # ---------------------------------------------------------------------------#

    messages.extend(
        state["messages"]
    )

    # ---------------------------------------------------------------------------#
    # Call LLM
    # ---------------------------------------------------------------------------#

    response = await llm_with_tools.ainvoke(
        messages
    )

    return {
        "messages": [response]
    }


# ===============================================================================#
# =============================== Tool Routing ==================================#
# ===============================================================================#

def should_use_tool(state: AgentState):

    last_message = state["messages"][-1]

    if getattr(
        last_message,
        "tool_calls",
        None
    ):

        return "run_tools"

    return "finalize"


# ===============================================================================#
# ================================= Tools =======================================#
# ===============================================================================#

async def run_tools(state: AgentState):

    tool_node = ToolNode(tools)

    result = await tool_node.ainvoke(
        {
            "messages": state["messages"]
        }
    )

    return result


# ===============================================================================#
# ================================= Finalize ====================================#
# ===============================================================================#

def finalize(state: AgentState):

    last_message = state["messages"][-1]

    return {
        "final_answer": last_message.content
    }


# ===============================================================================#
# ================================= Workflow ====================================#
# ===============================================================================#

workflow = StateGraph(AgentState)


# ================================ Nodes ========================================#

workflow.add_node(
    "load_memory",
    load_memory
)

workflow.add_node(
    "call_model",
    call_model
)

workflow.add_node(
    "run_tools",
    run_tools
)

workflow.add_node(
    "finalize",
    finalize
)


# ============================== Memory Routing =================================#

# START → check_memory_need
#
# If memory is needed:
# START → load_memory → call_model
#
# If memory is not needed:
# START → call_model

workflow.add_conditional_edges(
    START,
    check_memory_need,
    {
        "load_memory": "load_memory",
        "call_model": "call_model"
    }
)


# -------------------------------------------------------------------------------#
# Memory → Model
# -------------------------------------------------------------------------------#

workflow.add_edge(
    "load_memory",
    "call_model"
)


# ============================== Tool Routing ===================================#

workflow.add_conditional_edges(
    "call_model",
    should_use_tool,
    {
        "run_tools": "run_tools",
        "finalize": "finalize"
    }
)


# -------------------------------------------------------------------------------#
# Tools → Model
# -------------------------------------------------------------------------------#

workflow.add_edge(
    "run_tools",
    "call_model"
)


# ================================ END ==========================================#

workflow.add_edge(
    "finalize",
    END
)


# ===============================================================================#
# ================================= Checkpoint ==================================#
# ===============================================================================#

CHECKPOINT_DB_PATH = "checkpoints.sqlite"







async def get_thread_messages(thread_id: str):
    async with AsyncSqliteSaver.from_conn_string(
        CHECKPOINT_DB_PATH
    ) as checkpointer:

        graph = workflow.compile(
            checkpointer=checkpointer
        )

        state = await graph.aget_state(
            {
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        if not state or not state.values:
            return []

        messages = state.values.get("messages", [])

        result = []

        for message in messages:
            role = "user" if message.type == "human" else "assistant"

            if message.content:
                result.append({
                    "role": role,
                    "content": message.content
                })

        return result



        
# ===============================================================================#
# ================================= Run Agent ===================================#
# ===============================================================================#

async def run_agent(
    user_input: str,
    user_id: str,
    thread_id: str
):

    print("1️⃣ ENTERED run_agent")

    # ---------------------------------------------------------------------------#
    # Validate User Request
    # ---------------------------------------------------------------------------#

    try:

        request = UserRequest(
            query=user_input,
            user_id=user_id,
            thread_id=thread_id
        )

        print("2️⃣ REQUEST CREATED")

        print(
            "Query:",
            request.query
        )

        print(
            "user:",
            request.user_id
        )

        print(
            "thread:",
            request.thread_id
        )

    except ValidationError as e:

        print("❌ VALIDATION ERROR")
        print(e)

        return {
            "error": "Invalid input format.",
            "details": e.errors()
        }


    print("3️⃣ BEFORE GRAPH")


    # ---------------------------------------------------------------------------#
    # Checkpoint
    # ---------------------------------------------------------------------------#

    async with AsyncSqliteSaver.from_conn_string(
        CHECKPOINT_DB_PATH
    ) as checkpointer:

        graph = workflow.compile(
            checkpointer=checkpointer
        )


        # -----------------------------------------------------------------------#
        # Run Graph
        # -----------------------------------------------------------------------#

        result = await graph.ainvoke(

            {
                "session_id": request.user_id,

                "query": request.query,

                # Memory starts empty.
                # It will only be filled if check_memory_need
                # decides that memory is required.

                "memory_context": "",

                "messages": [
                    {
                        "role": "user",
                        "content": request.query
                    }
                ],

                "final_answer": ""
            },

            config={
                "configurable": {
                    "thread_id": request.thread_id,
                    "user_id": request.user_id
                }
            }
        )


    print("4️⃣ AFTER GRAPH")


    # ---------------------------------------------------------------------------#
    # Update Memory
    # ---------------------------------------------------------------------------#

    await update_compact_memory(
        user_id=request.user_id,
        user_message=request.query,
        assistant_response=result["final_answer"],
    )


    # ---------------------------------------------------------------------------#
    # Return Final Answer
    # ---------------------------------------------------------------------------#

    print("5️⃣ BEFORE RETURN")

    print(
        "Final answer:",
        result["final_answer"]
    )

    return result["final_answer"]