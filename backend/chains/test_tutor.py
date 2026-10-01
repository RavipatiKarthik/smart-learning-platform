from backend.chains.llm import llm
from backend.chains.tutor_chain import create_tutor_chain


tutor = create_tutor_chain(llm)


student = {
    "name": "Karthik",
    "branch": "CSE",
    "year": "Final Year",
    "target_skill": "Java",
    "learning_goal": "Placement Preparation"
}


while True:

    question = input("\nYou: ")

    if question.lower() in ["exit", "quit"]:
        print("\nSmartLearn AI: Happy learning!")
        break

    answer = tutor(question, student)

    print("\nSmartLearn AI:\n")
    print(answer)