import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Check for user prompt. Exit the program if there isn't any
if len(sys.argv) < 2:
    sys.exit(1)

# Check for --verbose flag
if len(sys.argv) > 2:
    verbose = True

input = sys.argv[1]

# Load api key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Save messages
messages = [
    types.Content(role="user", parts=[types.Part(text=input)]),
]

# Get response
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages,
)


print(f"{response.text}\n Prompt tokens: {response.usage_metadata.prompt_token_count}\n Response tokens: {response.usage_metadata.candidates_token_count}")
