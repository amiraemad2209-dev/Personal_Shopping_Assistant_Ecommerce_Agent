

# ===============================================================================#
# ========================== LLM & Structured Output ============================#
# ===============================================================================#


from langchain_openai import ChatOpenAI
from config import LITELLM_BASE_URL, TEMPERATURE


from schemas import (
    ProductComparisonResponse,
    ProductRecommendationResponse,
    WebSearchResponse,
    ShoppingPlanResponse,
    ReviewSummarizerResponse,
    RAGResponse
)


# General Agent LLM 

agent_llm = ChatOpenAI(
    model="agent-pool",
    base_url=LITELLM_BASE_URL,
    api_key="anything",
    temperature=TEMPERATURE,
)

# Structured Output LLM 

structured_llm = ChatOpenAI(
    model="response-pool",
    base_url=LITELLM_BASE_URL,
    api_key="anything",
    temperature=TEMPERATURE,
)


# Summary Output LLM 

summary_llm = ChatOpenAI(
    model="summary-pool",
    base_url=LITELLM_BASE_URL,
    api_key="anything",
    temperature=TEMPERATURE,
)




#==== Structured Output ( User--> LLM--> use a tool --> Structured response ---> return it) ====#

ProductComparison_llm = structured_llm.with_structured_output(
    ProductComparisonResponse )

ProductRecommendation_llm = structured_llm.with_structured_output(
    ProductRecommendationResponse , 
    method="json_schema" )

WebSearch_llm=structured_llm.with_structured_output(
    WebSearchResponse ,
    method="json_schema")

ShoppingPlan_llm = structured_llm.with_structured_output(
    ShoppingPlanResponse )

ReviewSummarizer_llm = structured_llm.with_structured_output(
    ReviewSummarizerResponse )


#DocumentSearch_llm= structured_llm.with_structured_output(RAGResponse)