from openai import OpenAI
import os
import numpy
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
EMBED_MODEL=os.getenv("EMBED_MODEL")
KB_FOLDER=os.getenv("KB_FOLDER")

## 1.currently we are using cosine similarity to find the most relevant documents based on the user query.
## 2. we are deriving the document by each files in knowledge base folder 
# and then we are adding the embedding of each document in the documents list.

#problems -->
## 1.currently we are converting each file into a single document 
# and then we are adding the embedding of each document in the documents list.
## 2. However for Larger documents we can split the document into smaller chunks 
# and then we can add the embedding of each chunk in the documents list.
# 3.however we did not implement the chunking of the document in this code.
# 4.load_documents( ) function loads evertime u run this programme ,which can be painful for large documents



#get the embedding of a text
def get_embedding(text):
    response=client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(A,B):
    dot_prod=numpy.dot(A,B)
    norm_a=numpy.linalg.norm(A)
    norm_b=numpy.linalg.norm(B)
    return dot_prod/(norm_a*norm_b)


#LOAD documents from kb_folder

def load_documents(folder=KB_FOLDER):
    documents=[]
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path=os.path.join(folder,filename)
            with open(path,"r",encoding="utf-8") as f:
                documents.append(
                    {
                        "source":filename,
                        "text":f.read(),
                    }
                )
                
    return documents





#add embeddings in documents

def add_embeddings(documents):
    for document in documents:
        document["vector"]=get_embedding(document["text"])
    return documents


#search function to find the most relevant documents based on cosine similarity
def search(query,documents,top_k=3):
    query_vector=get_embedding(query)
    
    results=[]
    for document in documents:
            score= cosine_similarity(query_vector,document["vector"])
            results.append({
                "score":score,
                "source":document["source"],
                "text":document["text"],
                "size":len(document["text"])
            })
     
    results.sort(key=lambda rec:rec["score"],reverse=True)#descending order
    return results[:top_k] # returns [0, top_k) results
 
 
 #testing methode
 
def test(user_query,documents,top_k=3):
     
    print(f"User query: {user_query}")
    
    results=search(user_query,documents,top_k)
    print(f"Top {top_k} results: {len(results)}")
    
    for r in results:
        print(f"Score: {r['score']:.4f}, Source: {r['source']}, Size: {r['size']} characters")


#lets start testing the code

documents=load_documents()
documents=add_embeddings(documents)

print(f"Loaded {len(documents)} documents from {KB_FOLDER} folder")

user_query="python is good for Ai engineering"
test(user_query,documents,3)

