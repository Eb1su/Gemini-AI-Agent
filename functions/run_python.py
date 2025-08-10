import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    print(f'Executing {file_path}...')
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory\n'
    
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.\n'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    returned_result = subprocess.run(
        ['python', target_file, *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30
        )

    return f'STDOUT: {returned_result.stdout},\nSTDERR: {returned_result.stderr}'