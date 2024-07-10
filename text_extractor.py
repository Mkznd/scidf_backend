import os
import time

import requests
from pymupdf import pymupdf

from utils import download_pdf


def extract_text_from_pdf(pdf_path):
    with pymupdf.open(pdf_path) as doc:  # open document
        text = "\n".join([page.get_text() for page in doc])
    return text


def extract_text_from_pdf_url(url: str):
    start = time.time()
    pdf_path = f"./pdf/{url.replace('/', '_')}.pdf"
    download_pdf(url, pdf_path)
    print(f"Downloaded PDF in {time.time() - start:.2f} seconds")
    start = time.time()
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted text in {time.time() - start:.2f} seconds")
    return text, pdf_path
