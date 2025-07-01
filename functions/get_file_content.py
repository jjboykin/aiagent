import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not os.path.commonpath([working_directory, target_file_path]) == working_directory:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'  

    try:
        with open(target_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(target_file_path) > MAX_CHARS:
                file_content_string += f'\n\n[...File "{file_path}" truncated at 10000 characters]'
        
        return file_content_string
    
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)