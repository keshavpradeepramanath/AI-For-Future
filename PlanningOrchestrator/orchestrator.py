from agents import researcher_agent, planner_agent, writer_agent

def orchestrate(query):
    """
    Simple sequential orchestrator
    """
    research = researcher_agent(query)
    plan = planner_agent(research)
    final_output = writer_agent(plan)

    return {
        "research": research,
        "plan": plan,
        "final": final_output
    }
