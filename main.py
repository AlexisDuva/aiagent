import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions,call_function

def main() -> None:

    max_nb_calls = 5

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it to your environment or a .env file."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose :
            print(f"User prompt: {args.user_prompt}")

    for i in range(max_nb_calls):

        if args.verbose :
            print(f"*********************** Call number : {i} ***********************")
            print(f"----------------- Messages to send to the model: -----------------")
            print(f"{messages}")
            print(f"------------------------------------------------------------------")


        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )

        if response.usage is None:
            raise RuntimeError(
                "The API response is missing usage data, which likely indicates a failed request."
            )

        # if args.verbose :
        #     print(f"Prompt tokens: {response.usage.prompt_tokens}")
        #     print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)
        tool_calls = message.tool_calls
        print(f"----------------- Response from the model {i} -----------------")
        print(f"----------------- Message -----------------")
        print(f"{message}")
        print(f"----------------- Tool list -----------------")
        if tool_calls :
            for tool_call in tool_calls:
                print(f"{tool_call.function.name}")
        if tool_calls :
            print(f"----------------- Tool calls  -----------------")
            for tool_call in tool_calls:
                print(f"Call : {tool_call.function.name}")
                call_result = call_function(tool_call, args.verbose)
                messages.append(call_result)
                print(f"Results :")
                print(f"{call_result['content']}")
        else:
            print("No tools called. Final response:")
            print(response.choices[0].message.content)
            return 0
    print(f"Max number of calls reached : {max_nb_calls}")
    return 1


if __name__ == "__main__":
    main()