COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}


def workflow(question):
    if "fee for AI202" in question:
        return "AI202 fee is Rs. 18,000."

    if "CS101 and AI202" in question and "10%" in question:
        total = (COURSE_FEES["CS101"] + COURSE_FEES["AI202"]) * 0.9
        return f"Total after 10% scholarship is Rs. {total:.0f}."

    return "I don't have a rule for this question."


questions = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students."
]

for q in questions:
    print("\nQ:", q)
    print("A:", workflow(q))