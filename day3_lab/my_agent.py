"""Day 3: ReAct agent - Failure Mode 3: Context Overflow."""

import json

from config import client, MODEL, banner
from my_tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a college assistant. "
    "Use read_webpage to read any page or file the user mentions, "
    "and use calculator for every arithmetic step. "
    "Never guess a number that should come from a page. "
    "If a tool returns an error, keep trying."
)


def agent(question, max_steps=20, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        # 1. REASON
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # 2. STOP
        if not message.tool_calls:
            return message.content.strip()

        # 3. RECORD
        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    }
                    for call in message.tool_calls
                ]
            }
        )

        # 4. ACT
        # 5. OBSERVE

        for call in message.tool_calls:

            name = call.function.name
            arguments = {}

            try:

                arguments = json.loads(
                    call.function.arguments or "{}"
                )

                function = TOOL_FUNCTIONS.get(name)

                if function is None:

                    result = (
                        f"Unknown tool: {name}. "
                        f"Available: {list(TOOL_FUNCTIONS)}"
                    )

                else:

                    result = function(**arguments)

            except json.JSONDecodeError as error:

                result = (
                    f"Argument error: {error}. "
                    "Send valid JSON."
                )

            except TypeError as error:

                result = f"Argument error: {error}"

            # -------------------------------------------------
            # INTENTIONAL FAILURE:
            # Add a huge amount of text to every tool result.
            # This makes the conversation context grow rapidly.
            # -------------------------------------------------

            huge_result = str(result) + ("\n" + "X" * 10000)

            if verbose:

                print(
                    f"   step {step}: "
                    f"{name}({arguments}) -> "
                    f"result length = {len(huge_result)}"
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": huge_result
                }
            )

    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


if __name__ == "__main__":

    banner("MY AGENT (context overflow test)")

    question = (
        "Read notice.html and tell me the fee for CS101."
    )

    print("Q:", question)

    print("A:", agent(question))