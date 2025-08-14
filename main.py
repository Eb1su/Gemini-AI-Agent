import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function
from config import MODEL_NAME, system_prompt
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file


def main():
    try:
        final_answer = None
        user_prompt = sys.argv[1]
        verbose = len(sys.argv) == 3 and sys.argv[2] == '--verbose'

        # API Initialization
        load_dotenv()
        api_key = os.environ.get('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)

        messages = [
            types.Content(role='user', parts=[types.Part(text=user_prompt)]),
        ]

        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_run_python_file,
                schema_get_file_content,
                schema_write_file
            ]
        )

        for i in range(20):
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                )
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            if verbose and not response.function_calls:
                print(f'User prompt: {user_prompt}\n')
                print(response.text)
                print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
                print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
            
            if response.text and not response.function_calls:
                final_answer = response.text
                break
                
            if response.function_calls:
                tool_responses = []
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose)
                    tool_responses.append(function_call_result.parts[0])
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception('Fatal Exception')
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(types.Content(role='tool', parts=tool_responses))

        if final_answer and not verbose:
            print(final_answer)

    except Exception as e:
        print(f'An error occured: {e}')
        raise


if __name__ == '__main__':
    main()