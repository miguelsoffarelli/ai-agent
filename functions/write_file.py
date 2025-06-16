import os

def write_file(working_directory, file_path, content):
    try:
        # See get_files_info
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_working_dir.endswith(os.sep):
            abs_working_dir += os.sep

        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # split file path to get necessary directories
        split_file_path = os.path.split(abs_file_path)
        # if directory doesn't exist, create it (if it already exists nothing will happen because of exist_ok=True)
        os.makedirs(split_file_path[0], exist_ok=True)

        # write content on the file
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"
        