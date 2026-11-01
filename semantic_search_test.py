from openai import OpenAI
import os
import numpy
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def get_embedding(text):
    response=client.embeddings.create(
        model="nomic-embed-text",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(A,B):
    dot_prod=numpy.dot(A,B)
    norm_a=numpy.linalg.norm(A)
    norm_b=numpy.linalg.norm(B)
    return dot_prod/(norm_a*norm_b)

text1="python is good programming language"
text2="python is best for coding"
text3="python is best  language"

embedding1=get_embedding(text1)
embedding2=get_embedding(text2)
embedding3=get_embedding(text3)

similarity12=cosine_similarity(embedding1,embedding2)
similarity13=cosine_similarity(embedding1,embedding3)
similarity23=cosine_similarity(embedding2,embedding3)


print("similarity btw text1 & text2 : ", similarity12)
print("similarity btw text1 & text3 : ", similarity13)
print("similarity btw text2 & text3 : ", similarity23)