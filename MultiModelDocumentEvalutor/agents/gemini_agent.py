import google.generativeai as genai
from prompts import EXTRACTION_PROMPT


def run_gemini(context, question, model_name="gemini-3-pro-preview"):
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


def get_supported_gemini_models():
    genai.configure()

    models = []
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            # Remove "models/" prefix
            print(m.name)
            models.append(m.name.replace("models/", ""))
    return models    
