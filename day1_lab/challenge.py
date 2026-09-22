from agent import run_agent

question = "I can pay Rs. 30,000. Which two courses can I take together within this budget?"

print("Q:", question)

# Course fees
courses = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}

budget = 30000

for course1 in courses:
    for course2 in courses:
        if course1 < course2:
            total = courses[course1] + courses[course2]

            if total <= budget:
                print(
                    f"A: {course1} + {course2} = Rs. {total:,} "
                    f"(within Rs. {budget:,})"
                )