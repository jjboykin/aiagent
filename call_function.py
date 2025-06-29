from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

func_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part:types.FunctionCall, verbose:bool=False) -> types.Content:
    if verbose:
        print(f'Calling function: {function_call_part.name}({function_call_part.args})')
    else:
        print(f'Calling function: {function_call_part.name}')

    func = func_map[function_call_part.name]
    if not func:
        return types.Content(
            role='tool',
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={'error': f'Unknown function: {function_call_part.name}'},
                )
            ],
        )
    
    function_call_part.args['working_directory'] = './calculator'
    result = func(**function_call_part.args)

    return types.Content(
    role='tool',
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={'result': result},
        )
    ],
)