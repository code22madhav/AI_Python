"""Few-shot prompting is a prompt engineering technique where you provide an AI model with
 a few input-output examples (shots) within the prompt to demonstrate a desired pattern, 
 format, or task before asking it to generate a final response.
 with the help of few shot prompting we can structure our output as well, adjust the tone etc.
 """
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GEMINI_KEY'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="""You will only answer coding related questions, do not answer anything else coding. If the
user ask any thing apart from it you can reply sorry.

Example:
Q. Can you explain a + b square?
A. Sorry, I can only help with coding related issues.

Q. Can you help me write a function to return sum of a + b?
A. Yes, Here is the function for sum of two numbers.
    def sum(a,b):
        return a + b
"""

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {   "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "help to write a function which return sum of 3 numbers"
        }
    ]
)

print(response.choices[0].message.content)