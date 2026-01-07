from openai import OpenAI
import os


def researcher_agent(query):
    client = OpenAI()
    prompt = f"""
    You are a research agent.
    Provide key facts and background information for:
    {query}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def planner_agent(research):
    client = OpenAI()
    prompt = f"""
    You are a planning agent.
    Create a structured plan using this research:
    {research}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def writer_agent(plan):
    client = OpenAI()
    prompt = f"""
    You are a writing agent.
    Generate a clear, user-friendly response based on this plan:
    {plan}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
