from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)
"""This config is not mandatory if you don't provide config then mem0 will take it's default
embedder, vector db, llm. Infact you can custmoise in you way by providing only required custom
config for ex: just provide db and llm then it will take it's default embedder
Suggestion:
use the default config only because in the you can end up in facing lot of config issues
like compatibilty of these 3rd party things with mem0 or maybe at some time some pacakage
is updated and mem0 can still be on same old version so you can end up in lot's of config 
and communication conflicts.
"""

#step 1 create a config or use the dafault config
config = {
    "version": "v1.1",

    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "models/gemini-embedding-001",
            "api_key": os.getenv("GEMINI_API_KEY")
        }
    },
    
    "llm": {
        "provider": "groq",
        "config": {
            "model": "llama-3.3-70b-versatile",
            "api_key": os.getenv("GROQ_API_KEY")
        }
    },
    
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": "https://f98112a2-9a57-4336-b9bf-4753793b91fc.eu-central-1-0.aws.cloud.qdrant.io",
            "api_key": os.getenv("Qdrant_api"),
            "collection_name": "mem0_test_memory",
            "embedding_model_dims": 768
        }
    }
}

# step 2 create memory from config
mem_client = Memory.from_config(config)

"""This user id is used to store different users data seperately.
mem0 manages everything interanally like converting the data in vector embeddings
then classifing the data in short term memory long term memory further more in 
facatual memory, semantic memory, episodic memory.
And when you search anything in memory it again converty the query in vector embedding
and do semantic search and provide the relevant data only.
Just we have to follow the pattern which is followed in below chat function"""
userId="madhav"

def chat(user_query:str):
    # Step 1 — search relevant memories for this input
    search_memory=mem_client.search(query=user_query,filters={"user_id": userId})

    # Step 2 — format memories as context string
    memory_context = "\n".join(
        [m["memory"] for m in search_memory["results"]]
    )
    print(f"memor_context: {memory_context}")

    # Step 3 — build sys prompt with memory context
    SYSTEM_PROMPT=f"""
        You are a helpful assistant with memory.
        Here is what you remember about this user:
        {memory_context}
        Use this to personalize your responses.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {   "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )
    assistant_reply = response.choices[0].message.content

    # Step 5 — save this conversation turn to mem0
    mem_client.add(
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": assistant_reply}
        ],
        user_id=userId
    )

    return assistant_reply

def main():
    print("Chat started. Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "quit":
            break
        
        response = chat(user_input)
        print(f"AI: {response}\n")

main()
