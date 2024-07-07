import json

from research.technical_content_analysis.interfaces.openai import completion
from research.research_assistant.prompts.highlights import GENERATE_HIGHLIGHTS_SYSTEM_MESSAGE


def create_highlights(text: str, verbose: bool = True, **kwargs):
    return completion(
        prompt=text,
        verbose=verbose,
        system_instruction=GENERATE_HIGHLIGHTS_SYSTEM_MESSAGE,
        model="gpt-4o",
        **kwargs,
    )["response_text"]
