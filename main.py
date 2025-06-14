import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('prompt')
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

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
    model='gemini-2.0-flash-001', contents=messages,
)

# Check for --verbose
if args.verbose:
    print(f"{response.text}\nUser prompt: {args.prompt}\n Prompt tokens: {response.usage_metadata.prompt_token_count}\n Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    print(response.text)

