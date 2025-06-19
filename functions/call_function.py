from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    # Create dictionary with string function name keys and function object values
    functions_dict = {
        "get_files_info": get_files_info,
        "get_file_contents": get_file_contents,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    function_name = function_call_part.name

    # Check if function name is valid
    if function_name in functions_dict:
        function_to_call = functions_dict.get(function_call_part.name)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Get args and add working_directory to them
    args_dict = function_call_part.args
    args_dict["working_directory"] = "./calculator"
    # Call the function and store the result
    result = function_to_call(**args_dict)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )

