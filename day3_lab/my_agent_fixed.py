"""Day 3: ReAct agent with guards and failure handling."""

import json

from config import client, MODEL, banner
from my_tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a college assistant. "
    "Use read_webpage to read any page or file the user mentions, "
    "and use calculator for every arithmetic step. "
    "Never guess a number that should come from a page. "
    "If no tool is needed, answer directly."
)


# Maximum number of ReAct steps
MAX_STEPS = 6

# Maximum number of characters allowed in one tool observation
MAX_OBSERVATION_CHARS = 4000


def agent(question, max_steps=MAX_STEPS, verbose=True):

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

    # Remember failed tool calls
    failed_calls = set()

    for step in range(1, max_steps + 1):

        # -------------------------------------------------
        # 1. REASON
        # -------------------------------------------------

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # -------------------------------------------------
        # 2. STOP
        # -------------------------------------------------

        if not message.tool_calls:
            return message.content.strip()

        # -------------------------------------------------
        # 3. RECORD
        # -------------------------------------------------

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

        # -------------------------------------------------
        # 4. ACT
        # 5. OBSERVE
        # -------------------------------------------------

        for call in message.tool_calls:

            name = call.function.name
            raw_arguments = call.function.arguments or "{}"

            # ---------------------------------------------
            # GUARD 1: Validate tool name
            # ---------------------------------------------

            if name not in TOOL_FUNCTIONS:

                result = (
                    f"Unknown tool: {name}. "
                    f"Available tools: {list(TOOL_FUNCTIONS)}"
                )

                if verbose:
                    print(
                        f"   step {step}: "
                        f"{name} -> {result}"
                    )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result
                    }
                )

                continue

            # ---------------------------------------------
            # Parse arguments
            # ---------------------------------------------

            try:

                arguments = json.loads(raw_arguments)

            except json.JSONDecodeError as error:

                result = (
                    f"Argument error: {error}. "
                    "Please send valid JSON."
                )

                if verbose:
                    print(
                        f"   step {step}: "
                        f"{name}({raw_arguments}) -> "
                        f"{result}"
                    )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result
                    }
                )

                continue

            # ---------------------------------------------
            # GUARD 2: Detect repeated failed calls
            # ---------------------------------------------

            call_signature = (
                name,
                json.dumps(arguments, sort_keys=True)
            )

            if call_signature in failed_calls:

                result = (
                    "This exact tool call has already failed. "
                    "Do not repeat it."
                )

                if verbose:
                    print(
                        f"   step {step}: "
                        f"{name}({arguments}) -> "
                        f"{result}"
                    )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result
                    }
                )

                continue

            # ---------------------------------------------
            # Execute the tool
            # ---------------------------------------------

            try:

                function = TOOL_FUNCTIONS[name]

                result = function(**arguments)

            except TypeError as error:

                result = f"Argument error: {error}"

            except Exception as error:

                result = f"Tool error: {error}"

            # Convert result to string
            result = str(result)

            # ---------------------------------------------
            # GUARD 3: Limit observation size
            # ---------------------------------------------

            if len(result) > MAX_OBSERVATION_CHARS:

                result = (
                    result[:MAX_OBSERVATION_CHARS]
                    + "\n[Observation truncated]"
                )

            # ---------------------------------------------
            # Detect failed result
            # ---------------------------------------------

            if (
                result.startswith("Read error:")
                or result.startswith("Calculator error:")
                or result.startswith("Argument error:")
                or result.startswith("Tool error:")
            ):

                failed_calls.add(call_signature)

            # ---------------------------------------------
            # Print trace
            # ---------------------------------------------

            if verbose:

                print(
                    f"   step {step}: "
                    f"{name}({arguments}) -> "
                    f"{result[:120]}"
                )

            # ---------------------------------------------
            # Send observation back to model
            # ---------------------------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                }
            )

    # -----------------------------------------------------
    # SAFETY EXIT
    # -----------------------------------------------------

    return (
        "Stopped safely: maximum number of steps reached "
        "without a final answer."
    )


if __name__ == "__main__":

    banner("MY AGENT (fixed with guards)")

    question = (
        "Read notice.html and tell me the total fee for CS101 "
        "and AI202 after the merit scholarship."
    )

    print("Q:", question)

    print("A:", agent(question))