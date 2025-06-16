import os

def get_file_contents(working_directory, file_path):
    try:
        # See get_files_info
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_working_dir.endswith(os.sep):
            abs_working_dir += os.sep

        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Because Gemini's free plan tokens are limited, limit the file's number of characters to read
        CHAR_LIMIT = 10000

        with open(abs_file_path, "r") as f:
            file_content = f.read(CHAR_LIMIT)
            # Check for remainder. If there's any, it means the file is +10000 characters and was truncated
            remainder = f.read(1)
            if remainder:
                # If there is a remainder, notify the user
                return file_content + f'[...File "{file_path}" truncated at 10000 characters]'
        
        return file_content
    
    except Exception as e:
        return f"Error: {str(e)}"