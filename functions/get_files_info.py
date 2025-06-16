import os

def get_files_info(working_directory, directory=None):
    # if no directory is provided, default directory to the current working directory
    if directory is None:
        directory = working_directory

    try:    
        # set working directory to absolute and check if it ends with separator to avoid false positives 
        # (for example: working_directory = workingdirectory, directory = workingdirectory123, directory would be true at .startswith(working_directory) even though it isn't)
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_working_dir.endswith(os.sep):
            abs_working_dir += os.sep
    
        # set directory to absolute and check if it is inside the working directory
        # (now that the working directory ends with the separator, the case mentioned before would return false and print the error)
        abs_dir = os.path.abspath(os.path.join(abs_working_dir, directory))
        if not abs_dir.endswith(os.sep):
            abs_dir += os.sep
            
        if not abs_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        # check if directory is an actual directory
        if not os.path.isdir(abs_dir):
            return f'Error: "{directory}" is not a directory'

        # get list of files and directories
        dir_list = os.listdir(abs_dir)
        # create output
        dir_contents = ""
        for dir_name in dir_list:
            dir_path = os.path.join(abs_dir, dir_name)
            dir_size = os.path.getsize(dir_path)
            dir_isdir = os.path.isdir(dir_path)
            dir_contents += f"- {dir_name}: file_size={dir_size} bytes, is_dir={dir_isdir}\n"

        return dir_contents

    except Exception as e:
        return f"Error: {str(e)}"

