



#================================================================================
#----------------- a simple example for add,subtract,multiply numbers
#================================================================================

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent


load_dotenv()


# LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# Tools
@tool
def add_numbers(x: float, y: float) -> float:
    """Add "X" and "Y" """
    return x + y


@tool
def subtract_numbers(x: float, y: float) -> float:
    """Subtract "X" from  "y" """
    return y - x


@tool
def multiply_numbers(x: float, y: float) -> float:
    """Multiply "X" and "Y" ."""
    return x * y




tools = [
    add_numbers,
    subtract_numbers,
    multiply_numbers
]


# Prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful math assistant. "
        "Use the available tools to perform calculations."
    ),
    (
        "human",
        "{input}"
    ),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])



# Create Tool Calling Agent
agent = create_tool_calling_agent(
    llm,
    tools,
    prompt
)


# Agent Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

# Call the Agent
response = agent_executor.invoke({
    "input": "What is (10 * 5)+20-10 ?"
})



print(response["output"])