from typing import TypedDict, List, Dict


class LearningState(TypedDict, total=False):

    student: Dict

    user_query: str

    intent: str

    skill: str

    context: str

    answer: str

    questions: List[Dict]

    score: int

    competency_gaps: List[str]

    learning_plan: List[Dict]

    recommendations: List[str]