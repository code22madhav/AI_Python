from typing_extensions import TypedDict
from typing import Optional, Literal
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    user_querry: str
    llm_output:Optional[str]
    isGood:Optional[str]

client=OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)
def chatbot(state:State):
    response=client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[
            {
                "role":"user",
                "content":state.get("user_querry")
            }
        ]
    )
    return {"llm_output": response.choices[0].message.content}

def evaluate_response(state: State) -> Literal["human_node", "endnode"]:
    if state.get("isGood") == "no":
        return "human_node"
    return "endnode"

def human_node(state:State):
    state["llm_output"]="This is a better response"
    return state

def endnode(state:State):
    return state


graph_builder=StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("human_node",human_node)
graph_builder.add_node("endnode",endnode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("human_node","endnode")
graph_builder.add_edge("endnode",END)

graph=graph_builder.compile()

updated_state_output=graph.invoke({
    "user_querry": "Hey my name is madhav",
    "isGood": "no"   # change to anything other than "no" to test endnode path
})
print(updated_state_output)