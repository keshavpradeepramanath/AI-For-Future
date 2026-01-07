from openai import OpenAI
import os
import google.generativeai as genai

def researcher_agent(query,model_name="gemini-3-pro-preview"):
    genai.configure()  # uses GOOGLE_API_KEY env var
    client = genai.GenerativeModel(model_name)
    prompt = f"""
    You are a research agent.
    Provide key facts and background information for:
    {query}
    """
    response = client.generate_content(prompt)
    return response.text
    


def planner_agent(research,model_name="gemini-3-pro-preview"):
    genai.configure()  # uses GOOGLE_API_KEY env var
    client = genai.GenerativeModel(model_name)
    prompt = f"""
    You are a planning agent.
    Create a structured plan using this research:
    {research}
    """
    response = client.generate_content(prompt)
    return response.text


def writer_agent(plan,model_name="gemini-3-pro-preview"):
    genai.configure()  # uses GOOGLE_API_KEY env var
    client = genai.GenerativeModel(model_name)
    prompt = f"""
    You are a writing agent.
    Generate a clear, user-friendly response based on this plan:
    {plan}
    """
    response = client.generate_content(prompt)
    return response.text