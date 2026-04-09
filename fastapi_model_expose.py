from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv 
import os

load_dotenv()
app = FastAPI()

client = OpenAI(
    api_key=os.getenv('GEMINI_KEY'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response=client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "user",
            "content": req.message
        }
    ])
    return {
        "response": response.choices[0].message.content
    }