from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
messages=[]
while True:
        user_input=input("User: ")
        if user_input.lower() in ["exit","quit"]:
            print("Exiting the Ai Assistant. GoodBye!")
            break
        response=client.chat.completions.create(
            model="qwen3:0.6b",
            messages=messages
        )
        #User's Input
        messages.append(
            {
            "role":"user",
            "content":user_input
                }
            )
        LLM_response=response.choices[0].message.content
        #LLM's Response 
        messages.append({
            "role":"assistant",
            "content":LLM_response
        })
        
        print("LLM Response:")
        print("Assistant: " + LLM_response)
        print(response)