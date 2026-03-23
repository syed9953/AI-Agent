import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_target_file = os.path.commonpath([absolute_path, target_path]) == absolute_path
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    try:
        command = ["python", target_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        elif result.stdout is None or result.stderr is None:
            output += "No output produced"
        else:
            output += f"STDOUT: {result.stdout} STDERR: {result.stderr}"
        
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located within the permitted working directory. Optionally accepts a list of command-line arguments. Returns the captured standard output and standard error, or an error message if execution fails.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python script",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single command-line argument",
                ),
            ),
        },
        required=["file_path"],
    ),
)
