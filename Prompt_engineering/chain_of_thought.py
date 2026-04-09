from openai import OpenAI
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

Client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
You are an AI assistant that solves problems step by step.
Each time return ONLY ONE JSON object.
Format: {"step": "start" | "thinking" | "output", "content": "string"}
- First call → step must be "start"
- When told to think → step must be "thinking"
- When told to output → step must be "output"
NEVER skip steps. NEVER return multiple JSONs.
"""

def call_api(messages):
    for attempt in range(3):
        try:
            response = Client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                response_format={"type": "json_object"},
                messages=messages
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            if "429" in str(e):
                wait = 60 * (attempt + 1)  # 60s, 120s, 180s
                print(f"⏳ Rate limit hit. Waiting {wait}s... (attempt {attempt+1}/3)")
                time.sleep(wait)
            else:
                raise e
    raise Exception("❌ Max retries exceeded. Daily quota may be exhausted.")

def run_cot(user_query):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": user_query})

    # Step 1 — start
    res = call_api(messages)
    print(f"🚀 {res['content']}")
    messages.append({"role": "assistant", "content": json.dumps(res)})
    messages.append({"role": "user", "content": 'Now respond with {"step": "thinking", "content": "your reasoning"}'})
    time.sleep(3)

    # Step 2 — thinking
    res = call_api(messages)
    print(f"🧠 {res['content']}")
    messages.append({"role": "assistant", "content": json.dumps(res)})
    messages.append({"role": "user", "content": 'Now respond with {"step": "output", "content": "your final answer"}'})
    time.sleep(3)

    # Step 3 — output
    res = call_api(messages)
    print(f"🤖 {res['content']}")

while True:
    user_query = input("\n👉 ")
    if user_query.lower() in ["exit", "quit"]:
        break
    run_cot(user_query)