from langgraph.graph import StateGraph, START, END

from backend.graph.state import LearningState
from backend.graph.nodes import (
    detect_intent,
    tutor_node,
    quiz_node,
    learning_node
)


def build_workflow():

    graph = StateGraph(LearningState)

    graph.add_node("detect_intent", detect_intent)
    graph.add_node("tutor", tutor_node)
    graph.add_node("quiz", quiz_node)
    graph.add_node("learning", learning_node)

    graph.add_edge(START, "detect_intent")

    graph.add_conditional_edges(
        "detect_intent",
        lambda state: state["intent"],
        {
            "tutor": "tutor",
            "quiz": "quiz",
            "learning": "learning"
        }
    )

    graph.add_edge("tutor", END)
    graph.add_edge("quiz", END)
    graph.add_edge("learning", END)

    return graph.compile()