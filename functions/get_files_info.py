import os

def get_files_info(working_directory, directory='.'):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    path_contents = os.listdir(target_dir)

    lines = [f"Result for '{directory}' directory:"]
    for content in path_contents:
        content_path = os.path.join(target_dir, content)
        get_content_size = os.path.getsize(content_path)
        is_directory = os.path.isdir(content_path)
        lines.append(f'- {content}: file_size={get_content_size} bytes, is_dir={is_directory}')
    return '\n'.join(lines)