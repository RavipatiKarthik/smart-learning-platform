from backend.graph.workflow import build_workflow


workflow = build_workflow()


student = {
    "name": "Karthik",
    "branch": "CSE",
    "year": "Final Year",
    "target_skill": "Java",
    "learning_goal": "Placement Preparation"
}


result = workflow.invoke({
    "student": student,
    "user_query": "Explain inheritance in Java"
})


print("\nIntent:", result["intent"])

print("\nSmartLearn AI:\n")

print(result["answer"])