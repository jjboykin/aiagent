import os

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