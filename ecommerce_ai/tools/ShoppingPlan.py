

# ===============================================================================#
# ============================ ShoppingPlan TOOL ================================#
# ===============================================================================#



from langchain_core.tools import tool

from models import ShoppingPlan_llm
from schemas import ShoppingPlanResponse


@tool
def ShoppingPlan(X: str) -> ShoppingPlanResponse:
    """
    Create a personalized shopping plan based on the customer's
    needs, occasion, destination, duration, budget, and preferences.
    """

    return ShoppingPlan_llm.invoke(X)