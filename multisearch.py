import time
from concurrent.futures import ThreadPoolExecutor

from models.SearchInput import SearchInput
from paper_retrieval.papers.paper_search_engine import PaperSourceType
from research.app.components.search import search_and_retrieve_papers, score_papers
from research.research_assistant.llm_tools.query import refine_query, create_subqueries
from research.research_assistant.paper_retrieval.papers.paper import PaperWithScore
from research.research_assistant.paper_retrieval.search_engine import MultiEngineSearch

from research.research_assistant.paper_retrieval.papers import Paper
from research.research_assistant.paper_retrieval.search_engine import MultiEngineSearch, SearchEngineType
from research.research_assistant.utils.utils import measure_time

SEARCH_MAP = {SearchEngineType.papers: [PaperSourceType.google_scholar]}
EMBEDDING_WEIGHT = 0.6
RECENCY_WEIGHT = 0.1
CITATION_WEIGHT = 0.1
ORDER_WEIGHT = 0.3
AUTHOR_WEIGHT = 0


@measure_time
def search_and_score_papers(research_topic):
    start = time.time()
    research_topic = refine_query(research_topic)
    print(f"Time taken by refine_query: {time.time() - start}, research_topic: {research_topic}")
    queries = [research_topic]

    start = time.time()
    sub_queries = create_subqueries(research_topic)
    queries += sub_queries
    print(f"Time taken by subqueries: {time.time() - start}, subqueries: {sub_queries}")

    # measure time
    papers_without_scores = []
    while not papers_without_scores:
        start = time.time()
        with ThreadPoolExecutor() as executor:
            tasks = {executor.submit(search_and_retrieve_papers, query, 5) for query in queries}
            papers_without_scores = [task.result() for task in tasks]
        papers_without_scores = [item for sublist in papers_without_scores for item in sublist]
        print(f"Time taken by search: {time.time() - start}")
        print(papers_without_scores)
    print(papers_without_scores)
    papers_with_scores = score_papers(
        research_topic,
        papers_without_scores,
        EMBEDDING_WEIGHT,
        RECENCY_WEIGHT,
        CITATION_WEIGHT,
        ORDER_WEIGHT,
        AUTHOR_WEIGHT,
    )
    papers_with_scores = PaperWithScore.remove_duplicates(papers_with_scores)
    return papers_with_scores
