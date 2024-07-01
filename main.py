import sys
from typing import Annotated

from dotenv.main import load_dotenv
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from models.RefineInput import RefineInput
from models.SearchInput import SearchInput
from models.SubqueryInput import SubqueryInput
from research.research_assistant.llm_tools.query import refine_query, create_subqueries
import os

from research.research_assistant.paper_retrieval.papers import Paper
from research.research_assistant.paper_retrieval.search_engine import MultiEngineSearch, SearchEngineType
from research.research_assistant.paper_retrieval.types import PaperSourceType

load_dotenv()

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World!"}


@app.post("/refine")
async def refine(refine_input: RefineInput):
    queries = refine_query(refine_input.query)
    return queries


@app.post("/subqueries")
async def subqueries(subquery_input: SubqueryInput):
    queries = create_subqueries(subquery_input.query)
    return queries


@app.post("/search")
async def search(search_input: SearchInput) -> list[dict]:
    multisearch = MultiEngineSearch(
        {
            SearchEngineType.papers: [PaperSourceType.arxiv],
        }
    )
    print(search_input.queries)
    return [i.__dict__ for i in multisearch.search(search_input.queries, search_input.article_no)]


@app.post("/summary")
async def summary(summary_input: SearchInput) -> list[dict]:
    queries = create_subqueries(subquery_input.query)
    return queries
