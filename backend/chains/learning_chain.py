from langchain_core.prompts import ChatPromptTemplate
from backend.chains.llm import llm
from backend.rag.retriever import get_retriever
import json


def generate_learning_plan(student, gaps, moderate_topics):

    skill = student["target_skill"]
    goal = student["learning_goal"]

    topics = gaps + moderate_topics

    if not topics:
        topics = [skill]

    retriever = get_retriever()

    query = f"{skill} {' '.join(topics)} {goal}"

    documents = retriever.invoke(query)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an AI learning-plan generator.

Create a personalized learning plan for a student.

Student:
Name: {name}
Branch: {branch}
Academic Year: {year}
Target Skill: {skill}
Learning Goal: {goal}

Topics that need improvement:
{topics}

Use the following learning material:

{context}

Create a practical learning plan.

Return ONLY valid JSON.

Format:

[
  {{
    "topic": "Topic name",
    "priority": "High",
    "duration": "2 days",
    "concepts": [
      "Concept 1",
      "Concept 2",
      "Concept 3"
    ],
    "activity": "Practice activity"
  }}
]

Rules:

- Focus mainly on weak topics.
- Include moderate topics after weak topics.
- High priority for weak topics.
- Medium priority for moderate topics.
- Keep the plan suitable for the student's level.
- Make the plan useful for the student's learning goal.
- Do not invent topics unrelated to the target skill.
- Return valid JSON only.
"""
    )

    messages = prompt.invoke({
        "name": student["name"],
        "branch": student["branch"],
        "year": student["year"],
        "skill": skill,
        "goal": goal,
        "topics": ", ".join(topics),
        "context": context
    })

    response = llm.invoke(messages)

    content = response.content

    if isinstance(content, list):

        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    content = content.strip()

    if content.startswith("```"):

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    return json.loads(content)