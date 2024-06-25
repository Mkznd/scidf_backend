import sys

from dotenv.main import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from research.research_assistant.llm_tools.query import refine_query, create_subqueries
import os

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
async def refine(query: str):
    print(query)
    queries = refine_query(query)
    return queries


@app.post("/subqueries")
async def subqueries(query: str):
    print(query)
    queries = create_subqueries(query)
    return queries
