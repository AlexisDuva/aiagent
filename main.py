import os
import argparse
from pprint import pformat

from dotenv import load_dotenv
from openai import OpenAI

import console
from prompts import system_prompt
from functions.call_function import available_functions, call_function

MAX_CALLS = 5
MODEL = "openrouter/free"


def main() -> int:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it to your environment or a .env file."
        )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    console.set_verbose(args.verbose)

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    console.detail(f"User prompt: {args.user_prompt}")

    for i in range(MAX_CALLS):
        console.detail(f"\n=== Call {i + 1}/{MAX_CALLS} ===")
        console.detail("Messages sent to the model:")
        console.detail(pformat(messages))

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0,
            tools=available_functions,
        )

        if response.usage is None:
            raise RuntimeError(
                "The API response is missing usage data, which likely indicates a failed request."
            )

        console.detail(
            f"Tokens: {response.usage.prompt_tokens} prompt, "
            f"{response.usage.completion_tokens} response"
        )

        message = response.choices[0].message
        messages.append(message)

        console.detail("Model message:")
        console.detail(pformat(message))

        tool_calls = message.tool_calls
        if not tool_calls:
            console.info(message.content or "")
            return 0

        for tool_call in tool_calls:
            result = call_function(tool_call)
            messages.append(result)
            console.detail(f"   -> {result['content']}")

    console.info(f"Reached the maximum of {MAX_CALLS} calls without a final answer.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
