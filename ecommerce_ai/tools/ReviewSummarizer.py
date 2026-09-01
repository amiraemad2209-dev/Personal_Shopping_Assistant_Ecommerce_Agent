

# ===============================================================================#
# ============================ ReviewSummarizer TOOL ============================#
# ===============================================================================#

from langchain_core.tools import tool

from models import ReviewSummarizer_llm
from schemas import ReviewSummarizerResponse


@tool
def ReviewSummarizer(X: str) -> ReviewSummarizerResponse:
    """
    Summarize customer reviews for a product to help the customer
    make a better purchasing decision.
    """

    return ReviewSummarizer_llm.invoke(X)