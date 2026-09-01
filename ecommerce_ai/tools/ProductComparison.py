

# ===============================================================================#
# ====================== ShoppingComparison TOOL ================================#
# ===============================================================================#


from langchain_core.tools import tool

from models import ProductComparison_llm
from schemas import ProductComparisonResponse


@tool
def ProductComparison(X: str) -> ProductComparisonResponse:
    """
    Compare products and help the customer choose the best option.

    Use this tool when the customer wants to compare products,
    understand their pros and cons, evaluate value for money,
    or decide which product best matches their needs.
    """

    return ProductComparison_llm.invoke(X)