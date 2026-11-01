from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)          
response=client.embeddings.create(
    model="nomic-embed-text",
    input=["i am a good boy","python is a programming language","i love to play football"]
)

for i in range(len(response.data)):
    print(response.data[i].embedding[:5])
    print(len(response.data[i].embedding))