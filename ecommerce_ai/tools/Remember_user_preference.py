
# ===============================================================================#
# ======================== Remember user preference TOOL ========================#
# ===============================================================================#

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def Remember_user_preference(
    key: str,
    value: str,
    config: RunnableConfig  ) -> str:
    """
    Save an important permanent user preference
    in long-term memory.

    Use this when the user gives information that
    may be useful in future conversations.
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
            "Failed to save preference: "
            "user_id was not provided."
        )

    save_user_preference(
        user_id=user_id,
        key=key,
        value=value
    )

    return (
        f"Preference saved successfully: "
        f"{key} -> {value}"
    )