import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    target_file_directory = os.path.dirname(target_file)
    

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to  "{file_path}" as it is outside the permitted working directory\n'

    if not os.path.exists(target_file_directory):
        os.makedirs(target_file_directory)

    with open(target_file, 'w') as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Finds the listed file and writes the content into it, if the file doesnt exist, creates one with the given name.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file given to write contents to, creates new file if doesnt exist."
            ),
            'content': types.Schema(
                type=types.Type.STRING,
                description='The content that will be written to a file.'
            )
        },
    ),
)