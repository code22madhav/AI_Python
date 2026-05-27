from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
import os
from openai import OpenAI
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain_core.messages import AIMessage, HumanMessage
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)

class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    """ ✅ convert all messages in state to dict format for Groq
    Final list
    [
        {"role": "human",     "content": "My name is Madhav"},
        {"role": "assistant", "content": "Nice to meet you Madhav!"},
        {"role": "human",     "content": "What is my name?"}
    ]
    """
    history = [
        {
            "role": "user" if msg.type == "human" else "assistant" if msg.type == "ai" else "system",
            "content": msg.content
        } for msg in state["messages"]
    ]
    """Above is an example of list comprehension and terniary operator:
            msg.type == "human"?  
            YES → "user"
            NO  → check next condition
                    msg.type == "ai"?
                        YES → "assistant"
                        NO  → "system"
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=history        # ✅ full history, not just last message
    )

    # ✅ wrap response in AIMessage
    return {"messages": [AIMessage(content=response.choices[0].message.content)]}
    """It's neccassy to add AIMessage object and prepare the state like this
    other wise llm will not understand which is user message and which is ai response
    also which making the full history list it wil fail to make that format"""

def get_checkpointer():
    # connect to mongodb
    client = MongoClient(os.getenv("MONGODB_URI"))
    
    # MongoDBSaver automatically saves graph state
    # after every node runs
    checkpointer = MongoDBSaver(client)
    
    return checkpointer


graph_builder=StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

checkpointer=get_checkpointer()
graph=graph_builder.compile(checkpointer=checkpointer)

"""Each thread have it's memory like madhav will have it's state memory which stores all msg"""
config={
    "configurable":{
        "thread_id":"madhav"
    }
}
"""
for chunk in graph.stream(
    State({"messages": [HumanMessage(content="what is my name")]}), 
    config=config,
    stream_mode="values"
):
    chunk['messages'][-1].pretty_print()
"""

updated_state_output=graph.invoke(State({
    "messages": [
        HumanMessage(content="what is my name")
    ]
}), config=config)
print(updated_state_output)
""" To print it beautifully
for chunk in graph.stream(
    State({"messages": [HumanMessage(content="what is my name")]}), 
    config=config,
    stream_mode="values"
):
    chunk['messages'][-1].pretty_print()
"""

"""2 things:
First it's again mandatory to wrap in HumanMessage object other wise it will be confusion
second thing if you don't wrap it then add_message reducer which is passed on Anotted list
will internally converts plain strings into HumanMessage objects:
{
    "messages": [
        HumanMessage(content="my name is madhav")
    ]
}
so even if you pass state like this while invoking graph.invoke({"messages": ["Hey my name is madhav"]})
then it will automatically convert in that manner. that is also why in the previous program where checkpointing
is not implemented doing this: tate["messages"][-1].content in
 messages=[
            {   "role": "user",
                "content": state["messages"][-1].content
            }
        ]
    works otherwise if state will be simple list of string then .content will fail
"""



"""
🔥 Actual architecture
MongoDBSaver
    ↓
Restores old state

add_messages
    ↓
Merges messages into state

Your node
    ↓
Decides what to send to LLM
"""