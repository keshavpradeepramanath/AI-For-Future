from agents import (
    profile_agent,
    it_access_agent,
    buddy_agent,
    knowledge_agent
)

def orchestrate_onboarding(profile):
    trace = []

    trace.append("profile_agent")
    profile_data = profile_agent(profile)

    trace.append("it_access_agent")
    it_data = it_access_agent(profile)

    trace.append("buddy_agent")
    buddy = buddy_agent()

    trace.append("knowledge_agent")
    knowledge = knowledge_agent()

    return {
        "trace": trace,
        "profile": profile_data,
        "it_access": it_data,
        "buddy": buddy,
        "knowledge": knowledge
    }
