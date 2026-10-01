from langchain_core.prompts import ChatPromptTemplate

from backend.chains.llm import llm
from backend.rag.retriever import get_retriever


def create_tutor_chain():

    retriever = get_retriever()


    prompt = ChatPromptTemplate.from_template(
        """
You are SmartLearn AI Tutor.

You are helping a student learn based on their
personalized learning requirements.

Student Information:

Name: {name}
Branch: {branch}
Academic Year: {year}
Target Skill: {skill}
Learning Goal: {goal}

Relevant Learning Material:

{context}

Student Question:

{question}


Instructions:

1. Answer the student's question clearly.
2. Use the provided learning material whenever relevant.
3. Explain concepts according to the student's level.
4. Give simple examples when useful.
5. For programming questions, provide code examples.
6. Do not invent information that conflicts with the learning material.
7. If the retrieved material does not contain the answer,
   clearly say that and then provide a general explanation.
8. Keep the answer focused on the student's question.


Answer:
"""
    )


    def tutor(question, student):

        documents = retriever.invoke(
            question
        )


        context = "\n\n".join(
            document.page_content
            for document in documents
        )


        messages = prompt.invoke(
            {
                "name": student.get(
                    "name",
                    "Student"
                ),

                "branch": student.get(
                    "branch",
                    "CSE"
                ),

                "year": student.get(
                    "year",
                    "Final Year"
                ),

                "skill": student.get(
                    "target_skill",
                    "Java"
                ),

                "goal": student.get(
                    "learning_goal",
                    "Skill Development"
                ),

                "context": context,

                "question": question
            }
        )


        response = llm.invoke(
            messages
        )


        return response.content


    return tutor
