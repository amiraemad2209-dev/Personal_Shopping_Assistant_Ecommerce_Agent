

# ===============================================================================#
# ========================== LLM & Structured Output ============================#
# ===============================================================================#



from langchain_groq import ChatGroq
from config import GROQ_MODEL, TEMPERATURE

from schemas import (
    ProductComparisonResponse,
    ProductRecommendationResponse,
    WebSearchResponse,
    ShoppingPlanResponse,
    ReviewSummarizerResponse,
    RAGResponse
)


# General Agent LLM 
llm = ChatGroq( model=GROQ_MODEL, temperature=0 ) 

# Structured Output LLM 
structured_llm = ChatGroq( model=GROQ_MODEL, temperature=0 )




#==== Structured Output ( User--> LLM--> use a tool --> Structured response ---> return it) ====#

ProductComparison_llm = structured_llm.with_structured_output(
    ProductComparisonResponse )

ProductRecommendation_llm = structured_llm.with_structured_output(
    ProductRecommendationResponse )

WebSearch_llm=structured_llm.with_structured_output(
    WebSearchResponse ,
    method="json_schema")

ShoppingPlan_llm = structured_llm.with_structured_output(
    ShoppingPlanResponse )

ReviewSummarizer_llm = structured_llm.with_structured_output(
    ReviewSummarizerResponse )


#DocumentSearch_llm= structured_llm.with_structured_output(RAGResponse)