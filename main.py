import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MODEL_NAME, system_prompt
from functions.get_files_info import schema_get_files_info

def main():
    
    user_prompt = sys.argv[1]
    verbose = len(sys.argv) == 3 and sys.argv[2] == '--verbose'

    # API Initalization
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )

    if verbose:
        print(f'User prompt: {user_prompt}\n')
        print(response.text)
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    
    if not response.function_calls:
        return response.text
    
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

        if function_call_part.name == 'get_files_info':
            from functions.get_files_info import get_files_info

            directory = function_call_part.args.get('directory', '.')

            working_directory = '.'

            result = get_files_info(working_directory, directory)

            print(result)


if __name__ =='__main__':
    main()