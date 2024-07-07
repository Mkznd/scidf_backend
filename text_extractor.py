import os

import requests
from pymupdf import pymupdf


def download_pdf(url, output_path):
    response = requests.get(url)
    with open(output_path, 'wb') as file:
        file.write(response.content)


def extract_text_from_pdf(pdf_path):
    with pymupdf.open(pdf_path) as doc:  # open document
        text = "\n".join([page.get_text() for page in doc])
    return text


def extract_text_from_pdf_url(url):
    pdf_path = "downloaded_file.pdf"
    download_pdf(url, pdf_path)
    text = extract_text_from_pdf(pdf_path)
    os.remove(pdf_path)
    return text
