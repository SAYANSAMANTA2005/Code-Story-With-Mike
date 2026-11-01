from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
while True:
        user_input=input("User:")
        if user_input.lower() in ["exit","quit"]:
            print("Exiting the Ai Assistant. GoodBye!")
            break
        stream= client.responses.create(
            model=os.getenv("MODEL"),
            input=[
                {
                "role":"user",
                "content":user_input,
                },
                ],
            stream=True,
        )

        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
        print("\n")