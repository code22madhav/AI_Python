from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)

class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state:State):
    response=client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[
            {   "role": "user",
                "content": state["messages"][-1].content
            }
        ]
    )
    return {"messages": [response.choices[0].message.content]}

def sampleNode(state:State):
    return {"messages": ["Sample message Appended"]}

graph_builder=StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", sampleNode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

graph=graph_builder.compile()

updated_state_output=graph.invoke({"messages": ["Hey my name is madhav"]})
print(updated_state_output)