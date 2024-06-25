import sys

from dotenv.main import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from research.research_assistant.llm_tools.query import refine_query
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
async def refine(search: str):
    queries = refine_query(search)
    return queries
