"""Day 2: Trace the ReAct agent."""

from agent import run_agent


QUESTION = (
    "Which is cheaper: CS101 and AI202 with a 10% scholarship, "
    "or all three courses with a 25% scholarship? By how much?"
)


print("QUESTION:", QUESTION)
print("\n--- THE AGENT'S ACTIONS AND OBSERVATIONS ---")

answer = run_agent(QUESTION)

print("\nFINAL ANSWER:", answer)