import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()

    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    verbose: bool = "--verbose" in sys.argv

    if not args:
            print('AI Code Assistant')
            print('\nUsage: python main.py "your prompt here" [--verbose]')
            print('Example: python main.py "How do I build a calculator app?"')
            sys.exit(1)

    api_key: str = os.environ.get("GEMINI_API_KEY")
    client: genai.Client = genai.Client(api_key=api_key)
    
    user_prompt: str = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages: list[types.Content] = [
        types.Content(
            role="user", 
            parts=[types.Part(text=user_prompt)]
        ),
    ]  

    max_feedback_loop_iteration: int = 20
    iterations: int = 0

    while True:
        iterations += 1
        if iterations > max_feedback_loop_iteration:
            print(f"Maximum iterations ({max_feedback_loop_iteration}) reached.")
            sys.exit(1)

        try:
            final_response: types.GenerateContentResponse = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response.text)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}") 

def generate_content(client: genai.Client, messages: list[types.Content], verbose: bool) -> types.GenerateContentResponse:
    response: types.GenerateContentResponse = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response
    
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result: types.Content = call_function(function_call_part, verbose)
        if not function_call_result.parts[0].function_response.response:
            raise Exception('Error: no result part')
        if verbose:
            print(f'-> {function_call_result.parts[0].function_response.response}')
        function_responses.append(function_call_result.parts[0])
    
    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    messages.append(types.Content(role="tool", parts=function_responses))

if __name__ == "__main__":
    main()