
from tools.WebSearch import WebSearch
from tools.ProductRecommendation import ProductRecommendation
from tools.ProductComparison import ProductComparison
from tools.ShoppingPlan import ShoppingPlan
from tools.ReviewSummarizer import ReviewSummarizer
from tools.Retrieve_internal_documents import Retrieve_internal_documents
from tools.Submit_final_answer import Submit_final_answer
from tools.Remember_user_preference import Remember_user_preference
from tools.Recall_user_preference import Recall_user_preference
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from database import (
    save_user_preference,
    recall_user_preference as db_recall_user_preference
)


tools = [
    ProductRecommendation,
    ProductComparison,
    ShoppingPlan,
    ReviewSummarizer,
    Retrieve_internal_documents,
    WebSearch ,
    Remember_user_preference,
    Recall_user_preference
]