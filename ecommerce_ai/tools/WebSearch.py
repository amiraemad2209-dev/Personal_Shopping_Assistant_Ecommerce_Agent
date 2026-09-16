

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
async def WebSearch(query: str) -> WebSearchResponse:
    """
    Search the web for current product information such as
    prices, specifications, reviews, availability, and offers.

    If the user doesn't enter a specific year, retrieve the data for the latest year.
    """

    results = await search.ainvoke(query)

    response = await  WebSearch_llm.ainvoke(
        f"""
        Extract product information from the following web search results.

        Only use information that appears in the search results.
        Do not invent or assume missing information.

        Search results:
        {results}
        """
    )

    return response