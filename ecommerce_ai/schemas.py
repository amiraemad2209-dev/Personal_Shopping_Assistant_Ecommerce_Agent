

# ===============================================================================#
# ===============================  Output Schema ================================#
# ===============================================================================#


from typing import List
from pydantic import BaseModel, Field



class ProductComparison(BaseModel):
    product_name: str
    advantages: List[str]
    disadvantages: List[str]
    best_for: str
    value_for_money: str


class ProductComparisonResponse(BaseModel):
    comparisons: List[ProductComparison]
    best_choice: str
    reason: str
    summary: str

#-------------------------------------------------------------------------------------------#
class ProductRecommendation(BaseModel):
    product_name: str
    reason: str
    price: str
    availability: str
    specifications: str
    source: str

class ProductRecommendationResponse(BaseModel):

    recommendations: List[ProductRecommendation] = Field(description="List of recommended products")

    summary: str = Field(description="Short summary of the recommendations")

#-------------------------------------------------------------------------------------------#

class SearchResult(BaseModel):
    
    product_name: str
    price: str
    availability: str
    specifications: str
    source: str


class WebSearchResponse(BaseModel):
    results: List[SearchResult]

#-------------------------------------------------------------------------------------------#

class ShoppingItem(BaseModel):

    item_name: str = Field(description="Name of the item the customer should buy")

    reason: str = Field(description="Why this item is needed for the customer's situation")

    priority: str = Field(description="Priority of the item: essential, recommended, or optional")

    estimated_price: str = Field(description="Estimated price or price range of the item")


class ShoppingPlanResponse(BaseModel):

    items: List[ShoppingItem] = Field(description="List of items the customer should consider buying")

    estimated_budget: str = Field(description="Estimated total budget for the shopping plan")

    summary: str = Field(description="Short summary of the shopping plan")


#-------------------------------------------------------------------------------------------#

class ReviewSummary(BaseModel):

    overall_sentiment: str = Field(description="Overall sentiment of the product reviews")

    positive_points: List[str] = Field(description="Most common positive points mentioned by customers")

    negative_points: List[str] = Field(description="Most common negative points mentioned by customers")

    common_complaints: List[str] = Field(description="Most common complaints or recurring issues mentioned in reviews")

    best_for: str = Field(description="Type of customer or use case the product is best suited for")


class ReviewSummarizerResponse(BaseModel):

    product_name: str = Field(description="Name of the product being reviewed")

    review_summary: ReviewSummary = Field(description="Summarized analysis of customer reviews")

    recommendation: str = Field(description="Short recommendation to help the customer decide whether to buy the product")

    summary: str = Field(description="Short overall summary of the customer reviews")
    

#-------------------------------------------------------------------------------------------#


#ده Schema لشكل الناتج من الـRAG:

class Source(BaseModel):

    source: str = Field(description="The source document name or path.")

    content: str = Field(description="The relevant content retrieved from the source.")


class RAGResponse(BaseModel):

    answer: str = Field(
        description=(
            "Answer the user's question based only on the retrieved documents. "
            "Be concise and provide only the information necessary to answer the question. "
            "Adjust the level of detail to the complexity of the question."
        )
    )

    sources: list[Source] = Field( default_factory=list ,description="Relevant sources used to answer the question." )

    found: bool = Field(description="True if relevant information was found in the documents.")


#-------------------------------------------------------------------------------------------#

class UserRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=2,
        description="User's question."
    )

    session_id: str = Field(
        default="default_guest",
        description="Session ID for memory tracking."
    )

#-------------------------------------------------------------------------------------------#

class SubmitFinalAnswerInput(BaseModel):
    answer: str
    sources: list[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)

#-------------------------------------------------------------------------------------------#

class RetrieveInternalDocsInput(BaseModel):
    query: str = Field(
        ...,
        min_length=2,
        description="The query to search for in the internal documents."
    )