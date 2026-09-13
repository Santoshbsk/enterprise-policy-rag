from scope import check_scope


questions = [
    "How many annual leave days are employees entitled to?",
    "What is the work from home policy?",
    "What is the annual health insurance coverage?",
    "How many leaves did I take last month?",
    "What is my current leave balance?",
    "What is my salary?",
]


for question in questions:

    result = check_scope(question)

    print()
    print(f"Question: {question}")
    print(f"In scope: {result}")