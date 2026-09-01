

# ===============================================================================#
# ========================== Submit_final_answer TOOL ===========================#
# ===============================================================================#

import json
from langchain_core.tools import tool

from schemas import SubmitFinalAnswerInput


@tool(args_schema=SubmitFinalAnswerInput, return_direct=True)
def Submit_final_answer(
    answer: str,
    sources: list[str],
    confidence_score: float
) -> str:

    """
    Submit the final answer to the user.

    This tool MUST be called only after the agent has finished
    reasoning and using any necessary tools.
    """

    result = {
        "answer": answer,
        "sources": sources,
        "confidence_score": confidence_score,
    }

    return json.dumps(result, ensure_ascii=False)