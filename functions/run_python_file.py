import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not os.path.commonpath([working_directory, target_file_path]) == working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file_path):
        return f'Error: File "{file_path}" not found.'

    _, extension = os.path.splitext(file_path)
    if not extension == '.py':
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            ['python3', file_path],
            cwd=working_directory,
            timeout=30,
            capture_output=True
        )

        output = f'STDOUT: {completed_process.stdout}\n'
        output += f'STDERR: {completed_process.stderr}\n'
        if completed_process.returncode != 0:
            output += f'Process exited with code {completed_process.returncode}\n'
        
        if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
            return 'No output produced.'
        
        return output
    
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path within the working directory to the Python file to execute.",
            ),
        },
    ),
)