import yaml
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from nodes import SupervisorNode, AgentNode, SummarizerNode
from state import State
import os


def build_graph(query):
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Load API key from environment variable
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    agents = {
        f"agent{i}": ChatGroq(temperature=config['temperature'],
                              model=config['models'][f'agent{i}'],
                              api_key=api_key)
        for i in range(1, 4)
    }
    summarizer = ChatGroq(temperature=config['temperature'],
                          model=config['models']['summarizer'],
                          api_key=api_key)

    builder = StateGraph(State)

    nodes = {
        "supervisor": SupervisorNode(),
        "agent1": AgentNode("Agent1 (llama-3.1)", agents['agent1']),
        "agent2": AgentNode("Agent2 (mixtral)", agents['agent2']),
        "agent3": AgentNode("Agent3 (llama-3.2-11b)", agents['agent3']),
        "summarizer": SummarizerNode(summarizer)
    }

    for name, node in nodes.items():
        builder.add_node(name, node)

    builder.add_edge(START, "supervisor")
    for agent in ["agent1", "agent2", "agent3"]:
        builder.add_edge("supervisor", agent)
        builder.add_edge(agent, "summarizer")
    builder.add_edge("summarizer", END)

    graph = builder.compile()

    return graph, {"messages": [query], "iteration": 0}