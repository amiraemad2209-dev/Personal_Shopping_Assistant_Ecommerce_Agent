

# ===============================================================================#
# ================================= Agent =======================================#
# ===============================================================================#

#----composition


# RunnableWithMessageHistory adds chat_history to the prompt
# we won't raw history to be send to the model 
# in the same time we want raw history to be stored in the DB
# we will separete it 
# insteade of make RunnableWithMessageHistory manage both  history , agent
# SQLChatMessageHistory manage the conversation history 
# compact_memory manage what we need the agent to remember (the retrieve , summary and keywords )

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_classic.agents import  AgentExecutor, create_tool_calling_agent
from memory.summary_memory import  get_compact_memory , update_compact_memory
from memory.history import get_session_history
from models import llm
from tools import tools
from prompt import prompt
from pydantic import ValidationError
from schemas import UserRequest
from rag.utils.Rate_Limite import RPMGroqRateLimiter
from rag.utils.Retry_Mechanism import invoke_with_retry



# =========================== Create Tool Calling Agent ===========================#
# Connects the LLM with the available tools and prompt.
# The agent decides when to use a tool and how to respond to the user.

agent = create_tool_calling_agent(
    llm,
    tools,
    prompt
)


# ============================ Agent Executor ======================================#
# Executes the agent's decisions and manages the interaction
# between the LLM and the tools.
# verbose=True  ----->   shows the agent's steps in the terminal.
# max_iterations -----> limits the number of tool-calling steps.

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=2
)

rate_limiter = RPMGroqRateLimiter(
    rpm=30,
    window_s=60.0
)


async def run_agent(user_input: str, session_id: str = "default_guest"):

    print("USER INPUT:", repr(user_input))

    try:
        request = UserRequest(
            query=user_input,
            session_id=session_id
        )

        print("VALIDATION PASSED")

    except ValidationError as e:
        print("VALIDATION FAILED")
        return {
            "error": "Invalid input format.",
            "details": e.errors()
        }

    # ==========================================
    # 1. Get compact memory
    # ==========================================

    memory = get_compact_memory(request.session_id)

    memory_context = f"""
Summary:
{memory["summary"]}

Important keywords:
{", ".join(memory["keywords"])}
"""

    # ==========================================
    # 2. Run Agent
    # ==========================================
    
    response = await invoke_with_retry(
    chain=agent_executor,
    payload={
        "input": request.query,
        "memory_context": memory_context,
    },
    rate_limiter=rate_limiter,
)

    # ==========================================
    # 3. Save raw conversation
    # ==========================================

    history = get_session_history(request.session_id)

    history.add_user_message(request.query)
    history.add_ai_message(response["output"])

    # ==========================================
    # 4. Update compact memory
    # ==========================================

    update_compact_memory(
        session_id=request.session_id,
        user_message=request.query,
        assistant_response=response["output"],
    )

    return response["output"]




"""

DATABASE have both
│
├── Full History
│   ├── message 1
│   ├── message 2
│   ├── message 3
│   └── ...
│
└── Compact Memory -----> retrieved to the model + Current Question
    ├── Summary
    └── Keywords

"""