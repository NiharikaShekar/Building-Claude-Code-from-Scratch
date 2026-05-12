import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function
import sys

def generate_content(client,messages):
    response =  client.models.generate_content(model = "gemini-2.5-flash", contents = messages,
                                               config = types.GenerateContentConfig(system_instruction=system_prompt, 
                                                                                    tools = [available_functions])
                                               )
    return response

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Gemini api key was not found, please check again")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt",type=str,help="user prompt")
    parser.add_argument("--verbose", action ="store_true", help="Adding verbose detailed output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = generate_content(client,messages)
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if response.function_calls:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call,args.verbose)
                if not function_call_result.parts:
                    raise Exception("Error, parts property is empty")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Error, function response is None")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Error, no response in function response")
                function_results.append(function_call_result.parts[0])
            messages.append(types.Content(role="tool",parts=function_results))
        else:
            print(f"Response:\n{response.text}")
            return
    
    print("Maximum number of iterations reached, couldn't produce the output")
    sys.exit(1)
    




    if not response.usage_metadata:
        raise RuntimeError("Sorry, the response failed, try again!")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    # if response.function_calls:
    #     for function_call in response.function_calls:
    #         function_call_result = call_function(function_call,args.verbose)
    #         if not function_call_result.parts:
    #             raise Exception("Error, parts property is empty")
    #         if not function_call_result.parts[0].function_response:
    #             raise Exception("Error, function response is None")
    #         if not function_call_result.parts[0].function_response.response:
    #             raise Exception("Error, no response in function response")
    #         function_results = []
    #         function_results.append(function_call_result.parts[0])
    #         if args.verbose:
    #             print(f"-> {function_call_result.parts[0].function_response.response}")
    # else:
    #     print(f"Response:\n{response.text}")
    # #print("""Response:
    # # {response.text}""")

if __name__ == "__main__":
    main()