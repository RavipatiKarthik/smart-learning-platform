from backend.assessment.generator import generate_assessment


questions = generate_assessment(
    skill="Java",
    level="Beginner",
    goal="Placement Preparation",
    difficulty="Easy",
    question_count=5
)


for i, question in enumerate(questions, start=1):

    print(f"\nQuestion {i}")
    print(question["question"])

    for option in question["options"]:
        print("-", option)

    print("Answer:", question["answer"])
    print("Topic:", question["topic"])