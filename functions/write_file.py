import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not os.path.commonpath([working_directory, target_file_path]) == working_directory:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        dirname, _ = os.path.split(target_file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Overwrite the contents of the file with the content argument.
        with open(target_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a specified file with provided content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The path within the working directory to the file to write.",
            ),
        },
    ),
)