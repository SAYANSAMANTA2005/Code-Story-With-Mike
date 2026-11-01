from openai import OpenAI
import os
import numpy
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
EMBED_MODEL=os.getenv("EMBED_MODEL")
KB_FOLDER=os.getenv("KB_FOLDER")

#problems -->
#1. The saved vector_store.json file can be stale/outdated 
# if the knowledge base folder is updated with new document
# or existing documents are modified.

#2. if embedding model is changed in the .env file, 
# then the saved vector_store.json file will be stale/outdated.


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





#add embeddings in the chunks

def add_embeddings(chunks):
    for chunk in chunks:
        chunk["vector"]=get_embedding(chunk["text"])
    return chunks


#search function to find the most relevant top_k chunks based on cosine similarity
def search(query,chunks,top_k=3):
    query_vector=get_embedding(query)
    
    results=[]
    for chunk in chunks:
            score= cosine_similarity(query_vector,chunk["vector"])
            results.append({
                "score":score,
                "source":chunk["source"],
                "chunk_id":chunk["chunk_id"],
                "text":chunk["text"],
                "size":len(chunk["text"])
            })
     
    results.sort(key=lambda rec:rec["score"],reverse=True)#descending order
    return results[:top_k] # returns [0, top_k) results
 
 
#it takes one file & creates multiple chunks from it 
def chunk_document(document):
    chunks=[]
    chunk_id=0
    for part in document["text"].split("\n\n"):
            #what does this part.split() do? -- it splits the part into words based on whitespace
            part=part.strip()
            
            if part:
                chunks.append({
                    "source":document["source"],
                    "chunk_id":chunk_id,
                    "text":part,
                    "size":len(part)
                })
            chunk_id=chunk_id+1
    
    return chunks


#save chunks in vector_store.json file
def save_vector_store(chunks):
    with open(os.getenv("VECTOR_STORE_FILE"),"w",encoding="utf-8") as f:#f --> file er pointer
        json.dump(chunks,f,indent=4)#indent=4 --> pretty print the json file with 4 spaces indentation

#load chunks from vector_store.json file

def load_vector_store():
    with open(os.getenv("VECTOR_STORE_FILE"),"r",encoding="utf-8") as f:
      return json.load(f)


 #create chunks from a document -- 
 # each chunk should have these keys -- source,chunk_id,text,size,vector
def create_chunks():
    documents=load_documents()
    chunks=[]
    for document in documents:
        chunks.extend(chunk_document(document))
        #extend -- methode via which many chunk can be added in chunks list at once
    return chunks




 #testing methode
 
def test(user_query,chunks,top_k=3):
     
    print(f"User query: {user_query}")
    
    results=search(user_query,chunks,top_k)
    print(f"Top {top_k} results: {len(results)}")
    
    for r in results:
        print(f"Score: {r['score']:.4f}, Source: {r['source']}, Chunk_id:{r['chunk_id']}, Size: {r['size']} characters ,Text: {r['text'][:100]}...")


#lets start testing the code

chunks=[]
if os.path.exists(os.getenv("VECTOR_STORE_FILE")):
    chunks=load_vector_store()
else:
    
    chunks=create_chunks()
    chunks=add_embeddings(chunks)
    save_vector_store(chunks)
    
    
print(f"Loaded {len(chunks)} chunks from {KB_FOLDER} folder")

user_query="Benefits of Maternity Leave and How Can One be Good At Python Programming ?"
test(user_query,chunks,3)

