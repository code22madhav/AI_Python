#Zero shot prompting: Model is given a direct instruction or task without an example
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GEMINI_KEY'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#SYSTEM_PROMPT="You are a maths expert, You will only answer maths question."
#If you write these kind of prompt the accuracy can be less it will still try to generate answer therefore
#write pompt like below
SYSTEM_PROMPT="You are a maths expert, You will only answer maths question. else reply sorry."

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)

print(response.choices[0].message.content)