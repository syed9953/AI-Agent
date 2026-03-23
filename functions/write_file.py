import os
from google.genai import types


def write_file(working_directory, file_path, content):
    absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(absolute_path, file_path))
    parent_directory = os.path.dirname(target_path)
    os.makedirs(parent_directory, exist_ok = True)
    valid_target_file = os.path.commonpath([absolute_path, target_path]) == absolute_path
    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    try:
        
        with open(target_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the permitted working directory. Creates parent directories if they do not exist and overwrites the file if it already exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)