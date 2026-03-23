import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import sys


load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]



def main():
    for _ in range(20):
        response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        if response.usage_metadata is None:
            raise RuntimeError("Usage Metadata is empty. Please check")
        
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            function_results = []
            function_call_result = None
            for func in response.function_calls:
                function_call_result = call_function(func)
                if function_call_result.parts is None:
                    raise Exception("function call list is empty")
                elif function_call_result.parts[0].function_response is None:
                    raise Exception("Function response is empty")
                elif function_call_result.parts[0].function_response.response is None:
                    raise Exception("There is no response in function response")
                else:
                    function_results.append(function_call_result.parts[0])
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            break    
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"-> {function_call_result.parts[0].function_response.response}")

        else:
            print(response.text)
     
    else:
        print(f'Model returned no responses after the end of the loop')
        sys.exit(1)


if __name__ == "__main__":
    main()
