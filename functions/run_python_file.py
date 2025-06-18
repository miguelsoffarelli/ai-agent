import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_working_dir.endswith(os.sep):
            abs_working_dir += os.sep

        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        output = subprocess.run(["python3", file_path], timeout=30, cwd=abs_working_dir, capture_output=True)
        stdout, stderr = output.stdout.decode("utf-8"), output.stderr.decode("utf-8")
        formatted_output = f"STDOUT: {str(stdout)}\nSTDERR: {str(stderr)}\n"

        if not stdout and not stderr:
            return "No output produced"
        
        if not output.returncode == 0:
            formatted_output += f"Process exited with code {output.returncode}"

        formatted_output += f"\n{("=" * 50)}\n"        

        return formatted_output
    
    except Exception as e:
        return f"Error: executing python file: {e}"
