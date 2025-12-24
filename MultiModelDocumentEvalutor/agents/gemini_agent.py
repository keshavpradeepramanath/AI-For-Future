import google.generativeai as genai
from prompts import EXTRACTION_PROMPT


def run_gemini(context, question, model_name="gemini-1.5-pro"):
    """
    Runs document extraction / QnA using Google Gemini.
    """
    genai.configure()  # uses GOOGLE_API_KEY env var

    prompt = EXTRACTION_PROMPT.format(
        context=context,
        question=question
    )

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    return response.text.strip()
