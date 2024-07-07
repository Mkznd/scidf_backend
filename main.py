from fastapi.encoders import jsonable_encoder

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
from text_extractor import extract_text_from_pdf, extract_text_from_pdf_url
from research.research_assistant.llm_tools.summarize import summarize
from utils import flatten_list

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
    res = highlights.create_highlights(extract_text_from_pdf_url(summary_input.url))
    res = json.loads(res.encode("utf-8"))
    return SummaryResponse(summary=res["summary"], highlights=res["highlights"])


@app.post("/paper_highlight")
def get_highlighted_paper(paper_highlight_input: PaperHighlightInput):
    response = requests.get(paper_highlight_input.url)
    filename_base = f"{round(time.time())}.pdf"
    filename = f"./tmp/{filename_base}"
    with open(filename, 'wb') as f:
        f.write(response.content)

    doc = pymupdf.open(filename)
    missed_highlights = []

    for point in [i.excerpt.strip() for i in paper_highlight_input.highlights]:
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

    highlighted_filename = f"{filename_base}_highlighted.pdf"
    doc.save(highlighted_filename, deflate=True)
    content = doc.tobytes()
    doc.close()
    os.remove(filename)
    os.remove(highlighted_filename)
    return Response(content, media_type="application/pdf")
