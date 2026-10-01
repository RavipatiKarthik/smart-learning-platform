from langchain_core.prompts import ChatPromptTemplate
from backend.rag.retriever import get_retriever
from backend.chains.llm import llm
import json


def generate_assessment(
    skill,
    level,
    goal,
    difficulty,
    question_count
):

    retriever = get_retriever()

    documents = retriever.invoke(
        f"{skill} {level} {goal} {difficulty}"
    )

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an AI assessment generator.

Create a personalized assessment for a student.

Skill: {skill}
Current Level: {level}
Learning Goal: {goal}
Difficulty: {difficulty}
Number of Questions: {question_count}

Use the following learning material:

{context}

Generate exactly {question_count} multiple-choice questions.

Return ONLY valid JSON.

Format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A",
    "topic": "Topic"
  }}
]

Rules:

- Questions must match the selected skill.
- Questions must match the student's level.
- Questions must match the selected goal.
- Questions must match the requested difficulty.
- Use the learning material when relevant.
- Do not include explanations.
- Return valid JSON only.
"""
    )

    messages = prompt.invoke({
        "skill": skill,
        "level": level,
        "goal": goal,
        "difficulty": difficulty,
        "question_count": question_count,
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