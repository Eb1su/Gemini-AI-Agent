import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    print(f'Finding {file_path} in {working_directory}...\n')

    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"\n'
    
    with open(target_file, 'r') as f:
        file_content_string = f.read(MAX_CHARS)
    
    if len(file_content_string) == MAX_CHARS:
        return f'{file_content_string} \n[...File "{file_path}" truncated at 10000 characters]\n'
    
    return f'{file_content_string} \n'

