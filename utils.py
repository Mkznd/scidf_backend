import requests


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


def generate_filename_from_url(url):
    return f"{url.split('/')[-1].replace('.pdf', '')}.pdf"


def download_pdf(url, output_path):
    response = requests.get(url)
    with open(output_path, 'wb') as file:
        file.write(response.content)
