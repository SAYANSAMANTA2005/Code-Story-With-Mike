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
    "content":"Give short, concise answers. Use get_current_time for questions about the current date or time. Use search_knowledge_base for questions about company policies or documents. If you don't know the answer, say 'I don't know'."
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
        while True:
            response=client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages,
                tools=Tools
            )
            msg=response.choices[0].message
            if not msg.tool_calls:
                answer=msg.content or ""
                messages.append({"role":"assistant","content":answer})
                print("Assistant: " + answer)
                break

            messages.append(msg.model_dump(exclude_none=True))
            for tool_call in msg.tool_calls:
                func_name=tool_call.function.name
                func_args=json.loads(tool_call.function.arguments or "{}")
                fn=FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result=fn(**func_args)
                messages.append({
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":json.dumps(result, ensure_ascii=False)
                })
                
