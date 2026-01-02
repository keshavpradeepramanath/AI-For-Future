import google.generativeai as genai
import json
import re
from typing import List

def agent_decide(api_key: str, keyword: str, emails: list):
    """
    Hybrid agent:
    - Deterministic keyword match first
    - Agent reasoning optional later
    """

    keyword_lower = keyword.lower()
    selected = []

    for e in emails:
        if (
            keyword_lower in (e["subject"] or "").lower()
            or keyword_lower in (e["from"] or "").lower()
        ):
            selected.append(e["id"])

    return selected
