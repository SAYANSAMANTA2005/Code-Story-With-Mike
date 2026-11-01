from openai import OpenAI
import os
#from tool_calling.py file import Tools, FUNCTION_NAME_TO_FUNCTION_MAP
from tool_calling import Tools,FUNCTION_NAME_TO_FUNCTION_MAP

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

        LLM_response=response.choices[0].message.content
        #LLM's Response 
        messages.append({
            "role":"assistant",
            "content":LLM_response
        })
        
        print("LLM Response:")
        print("Assistant: " + LLM_response)