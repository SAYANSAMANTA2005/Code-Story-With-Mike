from openai import OpenAI
import os
import json

#from tool.py file import Tools, FUNCTION_NAME_TO_FUNCTION_MAP
from tool import Tools,FUNCTION_NAME_TO_FUNCTION_MAP

from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
messages=[]
#System Prompt
messages.append({
    "role":"system",
    "content":"Give Shorts and Concise answers to the user. If you don't know the answer, say 'I don't know'."
})
while True:
        user_input=input("User: ")
        if user_input.lower() in ["exit","quit"]:
            print("Exiting the Ai Assistant. GoodBye!")
            break
        #User's Input
        messages.append(
            {
            "role":"user",
            "content":user_input
                }
            )
        response=client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=Tools
        )
        
        msg=response.choices[0].message
        if msg.tool_calls:
            messages.append(msg)
            
            for tool_call in msg.tool_calls:
                func_name=tool_call.function.name #function.name
                
                #stringfied Json of the arguments
                func_args=tool_call.function.arguments
                
                #convert the stringfied Json to a Python dictionary
                func_args=json.loads(func_args or "{}")
                
                fn=FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result=fn(**func_args)
                
                messages.append({
                    "role":"tool",
                    "tool_id":tool_call.id,
                    "content":str(result)
                })
            
            #2nd call to LLM api 
            response=client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages
            )
            msg=response.choices[0].message
        messages.append({
            "role":"assistant",
            "content":msg.content
        })
        
        print("Assistant: " + msg.content)
                
