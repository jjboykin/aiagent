import os

def get_files_info(working_directory, directory=None):
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