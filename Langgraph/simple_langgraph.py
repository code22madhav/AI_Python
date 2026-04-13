"""
What is Langgraph?
-LangGraph is a framework to build stateful, multi-step LLM workflows using a graph structure

Core purpose:
-To control how an AI system thinks step-by-step, instead of just calling an LLM once

Normal LLM usage:
-User → LLM → Response

Real-world AI systems need:
-Think → Decide → Call tool → Re-think → Respond

What LangGraph gives you:
-Stateful workflows
-Keeps track of:
-conversation + intermediate steps
-Multi-step reasoning & Control over execution
-LLM → think → act → observe → repeat

Without LangGraph -> Hard-coded logic

With LangGraph -> Structured flow: Node1 → Node2 → Node3 → Node4
"""


from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

#Step 1: create a typedDict State
class State(TypedDict):
    messages: Annotated[list, add_messages]

"""
What does add_message annotation do?
Our State is typeDict which have message as key and value is list
eg: {messages:["Hey how are you"]}
so add_message basically appends new list ["I'm fine"] in the old list
so after update it becomes:
["How are you", "I'm fine"]
If you don't use this annotation in tpyedDict and make it a simple list like this -> message: list
then evey time a node will run old list will be update with new list and old list ["How are you"] this data will be lost and
new list will be message:["I'm fine"]
"""

#Step 3: Create Nodes (Node is nothing but a function that takes state performs some operation and then returns a modified state)
def chatbot(state:State):
    return {"messages": ["Hi, This is a message from ChatBot Node"]}

def sampleNode(state:State):
    return {"messages": ["Sample message Appended"]}


#Step 2: Pass that state to StateGraph to create a graph
graph_builder=StateGraph(State)

#step 4: Register Node
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", sampleNode)


#step 5: Create edges First of all import START and END edge and follow this pattern
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)
#These are simple egdes

#step 6: compile the graph
graph=graph_builder.compile()

#step 7: Running the Graph
updated_state_output=graph.invoke(State({"messages":["Hey my name is madhav"]}))
print(updated_state_output)
