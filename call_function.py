from google.genai import types
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.get_file_content import get_file_content
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    function_call_part.args['working_directory'] = './calculator'

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    functionDict = {
        'get_files_info': get_files_info,
        'run_python_file': run_python_file,
        'get_file_content': get_file_content,
        'write_file': write_file
    }

    if function_call_part.name in functionDict:
        result = functionDict[function_call_part.name](**function_call_part.args)
        return types.Content(
                role="tool",
                parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                    )
                ],
            )

    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )