import os
import sys
from call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MODEL_NAME, system_prompt
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file

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
            schema_run_python_file,
            schema_get_file_content,
            schema_write_file
        ]
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )

    if verbose and not response.function_calls:
        print(f'User prompt: {user_prompt}\n')
        print(response.text)
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    
    if not response.function_calls:
        return response.text
    
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception('Fatal Exception')
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")


if __name__ =='__main__':
    main()