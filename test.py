from mem0 import Memory
from openai import OpenAI
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)

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

mem_client = Memory.from_config(config)

result = mem_client.add(
    messages=[
        {
            "role": "user",
            "content": "My name is Madhav"
        }
    ],
    user_id="madhav"
)
print(result)

result1 = mem_client.search(
    query="What is my name?",
    filters={"user_id": "madhav"}
)

print(result1)

print("Collection:", mem_client.vector_store.collection_name)
print("Qdrant URL:", "https://f98112a2-9a57-4336-b9bf-4753793b91fc.eu-central-1-0.aws.cloud.qdrant.io")

clientqdrant = QdrantClient(
    url="https://f98112a2-9a57-4336-b9bf-4753793b91fc.eu-central-1-0.aws.cloud.qdrant.io",
    api_key=os.getenv("Qdrant_api")
)

print(clientqdrant.get_collections())

