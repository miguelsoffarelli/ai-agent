import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('prompt')
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

# Set system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Functions schema and listing of available functions for the AI Agent to use
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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_contents",
    description="Reads and returns the content of the file on file_path, limited to 10000 characters. Also constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read the contents from, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file on file_path and returns it's stdout, stderr, and in case of the executed program exiting with a code different to 0, returns the returncode. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to run, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the contents of the content argument into the file on the file_path argument. If file_path doesn't exists, it creates it. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write the content on, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into the file.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

# Load api key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Save messages
messages = [
    types.Content(role="user", parts=[types.Part(text=args.prompt)]),
]

# Get response
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
)

if response.text is not None:
    res_text = response.text
else:
    res_text = ""

# Check for function calls
if len(response.function_calls) > 0:
    for call in response.function_calls:
        function_call_result = call_function(call, args.verbose)
        try:
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        except Exception as e:
            raise Exception(f"Fatal Error: {str(e)}")

# Check for --verbose
if args.verbose:
    print(f"{res_text}\nUser prompt: {args.prompt}\n Prompt tokens: {response.usage_metadata.prompt_token_count}\n Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    print(res_text)

