from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

PROMPT = PromptTemplate(
    input_variables=["keyword", "emails"],
    template="""
You are an assistant helping clean Gmail inbox.

User intent keyword: "{keyword}"

Below are emails (subject + sender).
Return ONLY a Python list of email IDs that clearly match the intent.

Emails:
{emails}
"""
)

def agent_decide(api_key: str, keyword: str, emails: list):
    """
    LLM agent that recommends which emails to delete.
    """
    llm = ChatOpenAI(
        api_key=api_key,
        temperature=0
    )

    formatted = "\n".join(
        f"ID:{e['id']} | {e['subject']} | {e['from']}"
        for e in emails
    )

    response = llm.invoke(
        PROMPT.format(keyword=keyword, emails=formatted)
    )

    try:
        return eval(response.content)
    except Exception:
        return []
