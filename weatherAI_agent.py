from openai import OpenAI
import json
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

Client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)

def get_weather(city:str):
    respose=requests.get(f"https://wttr.in/{city.lower()}?format=%C+%t")

    if respose.status_code==200:
        return f"The weather in {city} is {respose.text}"

def run_command(cmd: str):
    result=os.system(cmd)
    return result

available_tool={
    "get_weather": get_weather,
    "run_command": run_command
}
SYSTEM_PROMPT = """
You are an AI assistant that solves problems step by step.

Rules:
1. Always respond ONLY in JSON
2. Format:
   Format: {"step": "start" | "thinking" | "output" | "Tool", "content": "string", "tool":"string", "input":"string"}

3. First response must be "start"
4. Then move to "thinking"
5. Finally give "output"

5. Do NOT repeat steps unnecessarily
6. You can also call a tool from available list of tools.
7. For every tool call wait for the observe step which is output from the called tool.
8. NEVER skip steps. NEVER return multiple JSONs.

AvailableTools:
- get_weather(city:str): Takes city name as an input and returns the weather info about the city.
- run_command(cmd:str): Takes a system linux command as string and returns output from that command.

Example 1:
User: 2+2

Assistant:
{"step": "start", "content": "User asked a math question"}

Assistant:
{"step": "thinking", "content": "2+2 = 4"}

Assistant:
{"step": "output", "content": "4"}


Example 2:
{"step":"start": "content":"Hey What is the weather of delhi?"}
{"step":"thinking": "content":"Seems like user is intrested in weather of delhi."}
{"step":"thinking": "content":"Great we have get_weather tool available for this querry."}
{"step":"thinking: "content":"I need to call get_weather tool for delhi as input for city."}
{"step":"Tool": "tool":"get_weather", "input":"delhi"}
{"step":"Observe": "tool":"get_weather", "output":"The weather in delhi is cloudy with 20°C"} 
{"step":"thinking": "content":"Great I got the weather info about delhi"}
{"step":"output": "content":"The current weather in delhi is 20°C with some cloudy sky"}
"""

Model_response=[
    {   "role": "system",
        "content": SYSTEM_PROMPT
    }
]
while True:
    user_querry=input("👉")
    if user_querry=="break":
        break
    Model_response.append({   
        "role": "user",
        "content": user_querry
    })
    while True:
        response=Client.chat.completions.create(
            model="llama-3.1-8b-instant",
            response_format={"type":"json_object"},
            messages=Model_response
        )
        raw_result=response.choices[0].message.content
        Model_response.append({"role":"assistant", "content":raw_result})
        parsed_res=json.loads(raw_result)

        if isinstance(parsed_res,list):
            parsed_res=parsed_res[0]
        
        if parsed_res["step"] == "start":
            print("🚀",parsed_res["content"])
            Model_response.append({
                "role": "user",
                "content": "Proceed to thinking step"
            })
            time.sleep(2)
            continue

        if parsed_res["step"] == "thinking":
            print("🧠",parsed_res["content"])
            Model_response.append({
                "role": "user",
                "content": "Proceed to next step"
            })
            time.sleep(2)
            continue

        if parsed_res["step"] == "Tool":
            tool_to_call=parsed_res.get("tool")
            tool_input=parsed_res.get("input")
            tool_response=available_tool[tool_to_call](tool_input)
            print(f"⛏️: {tool_to_call}({tool_input}):{tool_response}")
            Model_response.append({
                "role": "developer",
                "content": json.dumps(
                    {"step":"Observe", "tool":tool_to_call, "input":tool_input, "output":tool_response}
                )
            })
            time.sleep(2)
            continue

        if parsed_res["step"] == "output":
            print("🤖",parsed_res["content"])
            break