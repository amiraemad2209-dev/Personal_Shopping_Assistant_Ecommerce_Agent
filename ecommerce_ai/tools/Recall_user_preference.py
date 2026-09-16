
# ===============================================================================#
# ====================== Recall user preference TOOL ============================#
# ===============================================================================#

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

@tool
def Recall_user_preference(
    query_key: str,
    config: RunnableConfig  ) -> str:
    """
    Retrieve an important user preference
    from long-term memory.

    Use this when the user asks about
    something they mentioned previously.
    """

    configurable = config.get(
        "configurable",
        {}
    )

    user_id = configurable.get(
        "user_id"
    )

    if not user_id:

        return (
            "Failed to recall preference: "
            "user_id was not provided."
        )

    result = db_recall_user_preference(
        user_id=user_id,
        query_key=query_key
    )

    if result:

        return (
            f"Long-term memory found: {result}"
        )

    return (
        f"No saved preference found "
        f"for: {query_key}"
    )