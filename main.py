from fastapi.encoders import jsonable_encoder

from db.database import Base, engine
from setup import setup

setup()
from research.app.components.search import sort_papers
import json
import time
from typing import Annotated, List, Any
from fastapi import Response
import os
import requests
from dotenv.main import load_dotenv
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pymupdf import pymupdf

import highlights
from models.RefineInput import RefineInput
from models.SearchInput import SearchInput
from models.SubqueryInput import SubqueryInput
from models.SummaryInput import SummaryInput
from models.SummaryResponse import SummaryResponse
from models.PaperHighlightInput import PaperHighlightInput

from multisearch import search_and_score_papers
from research.app.components.highlights import find_highlights
from research.research_assistant.llm_tools.query import refine_query, create_subqueries
from text_extractor import extract_text_from_pdf, extract_text_from_pdf_url, download_pdf
from research.research_assistant.llm_tools.summarize import summarize
from utils import flatten_list, generate_filename_from_url

load_dotenv()

app = FastAPI()
Base.metadata.create_all(engine)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    print(search_input)
    papers = sort_papers(search_and_score_papers(search_input))
    return [jsonable_encoder(i) for i in papers]


@app.post("/summary")
async def summary(summary_input: SummaryInput) -> SummaryResponse:
    print(summary_input.url)
    text, pdf_path = extract_text_from_pdf_url(summary_input.url)
    result_json = None
    while not result_json:
        try:
            start = time.time()
            res = highlights.create_highlights(text).encode("utf-8")
            result_json = json.loads(res)
            print(f"Time taken to generate highlights: {time.time() - start:.2f} seconds")
        except Exception as e:
            print(e)
    return SummaryResponse(summary=result_json["summary"], highlights=result_json["highlights"])


@app.post("/paper_highlight")
def get_highlighted_paper(paper_highlight_input: PaperHighlightInput):
    filename_base = f"{generate_filename_from_url(paper_highlight_input.url)}.pdf"
    filepath = f"./pdf/{filename_base}"
    highlighted_filepath = f"./pdf_highlighted/{filename_base}.pdf"

    if os.path.exists(highlighted_filepath):
        with open(highlighted_filepath, "rb") as f:
            content = f.read()
            return Response(content, media_type="application/pdf")
    if not os.path.exists(filepath):
        download_pdf(paper_highlight_input.url, filepath)

    with open(filepath, "rb") as f:
        start = time.time()
        doc = highlight_pdf(filepath, paper_highlight_input.highlights)
        doc.save(highlighted_filepath, deflate=True)
        content = doc.tobytes()
        doc.close()
        print(f"Time taken to highlight paper: {time.time() - start:.2f} seconds")
        return Response(content, media_type="application/pdf")


def highlight_pdf(filename: str, highlights: List[str]):
    doc = pymupdf.open(filename)
    missed_highlights = []
    for point in [i.strip() for i in highlights]:
        point_found = False
        for page in doc:
            found = page.search_for(
                point.replace("...", ""), flags=pymupdf.TEXT_DEHYPHENATE | pymupdf.TEXT_PRESERVE_WHITESPACE)
            if found:
                point_found = True
                for i in found:
                    annot = page.add_highlight_annot(i)
                    annot.set_colors(stroke=(0, 1, 0))
                    annot.update()
        if not point_found:
            missed_highlights.append(point)
    if missed_highlights:
        print(f"Could not find the following excerpts: {missed_highlights}")
    return doc
