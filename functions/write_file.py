import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    target_file_directory = os.path.dirname(target_file)
    

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'

    if not os.path.exists(target_file_directory):
        os.makedirs(target_file_directory)

    with open(target_file, 'w') as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'