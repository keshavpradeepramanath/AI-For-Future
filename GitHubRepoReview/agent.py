from openai import OpenAI
from prompts import REVIEW_PROMPT
from tools import read_github_file

def review_file(owner, repo, file_path):
    client = OpenAI()  # created AFTER key is set

    code = read_github_file(owner, repo, file_path)

    prompt = REVIEW_PROMPT.format(
        file_path=file_path,
        code=code
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text
