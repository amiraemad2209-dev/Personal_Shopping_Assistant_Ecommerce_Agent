

# ===============================================================================#
# =============================== WebSearch TOOL ================================#
# ===============================================================================#


from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from models import WebSearch_llm
from schemas import WebSearchResponse


search = TavilySearch(
    max_results=3
)


@tool
def WebSearch(query: str) -> WebSearchResponse :
    """
    Search the web for current product information such as
    prices, specifications, reviews, availability, and offers.

    If the user doesn't enter a specific year, retrieve the data for the latest year.
    """

    # ==========================================
    # 1. Search the web using Tavily
    # ==========================================

    results = search.invoke(query)

    # ==========================================
    # 2. Convert raw results into structured output
    # ==========================================

    response = WebSearch_llm.invoke(
        f"""
        Extract the relevant product information from these
        web search results.

        Return the information using the required structured format.

        Search results:
                        {results}
        """
    )

    return response
