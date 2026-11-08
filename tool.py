from datetime import datetime
from rag import search
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def search_knowledge_base(query):
    results=search(query,top_k=3)
    
    #debugging purpose
    print(f"search_knowledge_base: query={query}")
    for r in results:
        print(f"Score: {r['score']:.2f}, Source: {r['source']}, # {r['chunk_id']} chunkid")
        
    blocks=[]
    for r in results:
        sourcefilename=r["source"]
        chunkid=r["chunk_id"]
        chunktext=r["text"]
        
        header=f"{sourcefilename} #{chunkid}"
        block=f"{header} \n {chunktext}"
        blocks.append(block)
        
    return blocks

Tools=[
    {
        "type":"function",
        "name":"get_current_time",
        "description":"Get the current date and time in the format YYYY-MM-DD HH:MM:SS",
        "parameters":{
            "type":"object",
            "properties":{},
            
        },
        #write down all parameters that are required for this function to work.
        "required":[]
    },
    {
        "type":"function",
            "name":"search_knowledge_base",
            "description":"Searches the Zorvex Technologies company knowledge base"
                          "including leave, medical, HR, hiring, technology, incident reports, and travel expense policies."
                          "Use it to answer questions about company policies or documents. Returns the most relevant passages along with their sources.",
            "parameters":{
                "type":"object",
                "properties":{
                    "query":{
                        "type":"string",
                        "description":"The query to search in the knowledge base"
                    },
                },
                "required":["query"]
            }
        
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP={
    "get_current_time":get_current_time,
    "search_knowledge_base":search_knowledge_base
}
