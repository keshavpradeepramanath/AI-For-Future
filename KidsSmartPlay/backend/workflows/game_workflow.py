from langgraph.graph import StateGraph

from agents.psychologist import psychologist_agent
from agents.game_designer import game_designer_agent
from agents.generator import game_generator_agent
from agents.qa_agent import qa_agent


graph = StateGraph(dict)

graph.add_node("psychologist", psychologist_agent)
graph.add_node("designer", game_designer_agent)
graph.add_node("generator", game_generator_agent)
graph.add_node("qa", qa_agent)

graph.set_entry_point("psychologist")

graph.add_edge("psychologist", "designer")
graph.add_edge("designer", "generator")
graph.add_edge("generator", "qa")

workflow = graph.compile()
