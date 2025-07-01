import os
from google.genai import types

def get_files_info(working_directory: str, directory: str=None) -> str:
    if directory is None:
        directory = working_directory

    working_directory = os.path.abspath(working_directory)
    target_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not os.path.commonpath([working_directory, target_directory]) == working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'    

    try:
        files = os.listdir(target_directory)
        output = ''
        for file in files:
            output += f'- {file}: file_size={os.path.getsize(os.path.join(target_directory, file))} bytes, is_dir={os.path.isdir(os.path.join(target_directory, file))}\n'
        
        return output
    
    except Exception as e:
        return f'Error: Unable to access directory: {e}'
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)