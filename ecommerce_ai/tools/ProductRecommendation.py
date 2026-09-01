

# ===============================================================================#
# ======================== ProductRecommendation TOOL ============================#
# ===============================================================================#



from langchain_core.tools import tool

from models import ProductRecommendation_llm
from schemas import ProductRecommendationResponse


@tool
def ProductRecommendation(X: str) -> ProductRecommendationResponse:
    """
    Generate product recommendations based on customer needs,
    preferences, budget, usage, or requirements.

    Current prices, availability, specifications, and recent
    reviews should be obtained using web_search.
    """

    return ProductRecommendation_llm.invoke(X)