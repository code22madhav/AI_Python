from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
from langchain_cohere import CohereEmbeddings
import time

load_dotenv()

pdf_path=Path(__file__).parent / "The Bhagavad Gita.pdf"

#Load this file in python program

loader =PyPDFLoader(file_path=pdf_path)
docs = loader.load()

#split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks =text_splitter.split_documents(documents=docs)


#vector embeddings
embedding_model = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

#dividing the vector into chunks so that it should not throw rate limits on free tier.
def batch_list(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]

vector_store = None

for i, batch in enumerate(batch_list(chunks, 20)):  # 20 chunks at a time
    print(f"Processing batch {i+1}...")
    #storing in vector db
    if vector_store is None:
        # first batch — create the collection
        vector_store = QdrantVectorStore.from_documents(
            documents=batch,
            embedding=embedding_model,
            url="https://c1c9578b-ad6d-46a5-b68c-677a8a0f41fc.sa-east-1-0.aws.cloud.qdrant.io",
            api_key=os.getenv("Qdrant_api"),
            collection_name="learning_rag",
            force_recreate=True  # only on first batch
        )
    else:
        # subsequent batches — just add to existing collection
        vector_store.add_documents(batch)
    
    time.sleep(10)  # wait 10 seconds between batches

print("✅ All chunks stored successfully!")