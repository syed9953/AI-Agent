import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(absolute_path, directory))
    valid_target_dir = os.path.commonpath([absolute_path, target_path]) == absolute_path
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'
    results = []
    for file in os.listdir(target_path):
        try:
            full_file_path = os.path.join(target_path, file)
            results.append(f"{file}: file_size={os.path.getsize(full_file_path)} bytes, is_dir={os.path.isdir(full_file_path)}")
        except Exception as e:
            return f"Error. {e}"
        
    return '\n'.join(results)

    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)