from langchain_cohere import CohereEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

#vector embeddings
embedding_model = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

#getting the db
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="https://c1c9578b-ad6d-46a5-b68c-677a8a0f41fc.sa-east-1-0.aws.cloud.qdrant.io",
    api_key=os.getenv("Qdrant_api"),
    collection_name="learning_rag",
)

#taking user querry
querry=input("👉: ")

#Relevant chunks from the vector db
search_result=vector_store.similarity_search(query=querry)

context="\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_result])

SYSTEM_PROMPT="""
You are a helpfull AI Assistant who answers user querry based on the available
context retrieved from a PDF along with page_contents and page number.

You should only answer the user based on the following context and navigate the user
to open the right page to know more.

Context:{context}
"""

client = OpenAI(
    api_key=os.getenv("gemini_api_key"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {   "role": "system", "content": SYSTEM_PROMPT},
        { "role": "user", "content": querry}
    ]
)

print(f"🤖 {response.choices[0].message.content}")