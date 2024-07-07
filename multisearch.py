from concurrent.futures import ThreadPoolExecutor

from models.SearchInput import SearchInput
from research.research_assistant.paper_retrieval.search_engine import MultiEngineSearch

from research.research_assistant.paper_retrieval.papers import Paper
from research.research_assistant.paper_retrieval.search_engine import MultiEngineSearch, SearchEngineType
from research.research_assistant.paper_retrieval.search_engine import PaperSourceType

SEARCH_MAP = {SearchEngineType.papers: [PaperSourceType.google_scholar]}


def threaded_search(query, top_k_per_source):
    multisearch = MultiEngineSearch(SEARCH_MAP)
    return multisearch.search([query], top_k_per_source=top_k_per_source)


def search_all(search_input: SearchInput):
    with ThreadPoolExecutor() as executor:
        tasks = {executor.submit(threaded_search, query, search_input.top_k_per_source) for query in
                 search_input.queries}
        papers = [task.result() for task in tasks]
    return papers
