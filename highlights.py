import json

from research.technical_content_analysis.interfaces.openai import completion
from research.research_assistant.prompts.highlights import GENERATE_HIGHLIGHTS_SIMPLIFIED_SYSTEM_MESSAGE
from research.research_assistant.utils.utils import measure_time


@measure_time
def create_highlights(text: str, verbose: bool = True, **kwargs):
    return completion(
        prompt=text,
        verbose=verbose,
        system_instruction=GENERATE_HIGHLIGHTS_SIMPLIFIED_SYSTEM_MESSAGE,
        model="gpt-4o",
        **kwargs,
    )["response_text"]
