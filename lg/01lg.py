from typing import Annotated , TypedDict
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph , START , END
from langchain.chat_models import init_chat_model

llm = init_chat_model(model="gpt-4.1-mini", model_provider="openai")

class State(TypedDict):
    messages : Annotated[list,add_messages]

# class State(TypedDict):
#     messages : list


graph_builder = StateGraph(State)

def chatbot(state : State):
    response = llm.invoke(state.get("messages"))
    return {"messages" : [response]}


def samplenode(state :State):
    print("inside samplenode")
    return {"messages" : ["hi , msg from sample"]}

graph_builder.add_node("chatbot" , chatbot)
graph_builder.add_node("samplenode" , samplenode)


graph_builder.add_edge(START , "chatbot")
graph_builder.add_edge("chatbot" , "samplenode")
graph_builder.add_edge("samplenode", END)

#  start -> chatbot -> samplenode -> end


graph = graph_builder.compile()
updated_state = graph.invoke(State({"messages" : ["jay here"]}))
print(updated_state)