from backend.chains.tutor_chain import create_tutor_chain
from backend.chains.llm import llm


tutor = create_tutor_chain(llm)


def detect_intent(state):

    query = state.get("user_query", "").lower()

    if "quiz" in query or "test" in query:
        intent = "quiz"

    elif "learn" in query or "study" in query:
        intent = "learning"

    elif "explain" in query or "what is" in query:
        intent = "tutor"

    else:
        intent = "tutor"

    return {
        "intent": intent
    }


def tutor_node(state):

    student = state.get("student", {})

    question = state.get("user_query", "")

    answer = tutor(
        question,
        student
    )

    return {
        "answer": answer
    }


def quiz_node(state):

    return {
        "questions": []
    }


def learning_node(state):

    return {
        "learning_plan": []
    }