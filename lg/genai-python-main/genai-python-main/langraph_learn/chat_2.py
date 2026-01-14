from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()

client = OpenAI()

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("ChatBot Node", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            { "role": "user", "content": state.get("user_query") }
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state

def evalaute_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    # print("evalaute_response Node", state)
    # if False:
    #     return "endnode"

    # return "chatbot_gemini"
#updated
    if not state.get("llm_output") or len(state["llm_output"].strip()) == 0:
        state["is_good"] = False
        return "endnode"  # If response is bad, go to endnode
    
    
    # If the response is acceptable, we consider it good
    state["is_good"] = True
    return "chatbot_gemini"
    

def chatbot_gemini(state: State):
    print("chatbot_gemini Node", state)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            { "role": "user", "content": state.get("user_query") }
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state

def endnode(state: State):
    print("endnode Node", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evalaute_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

# while user_query != "exit" :
#     updated_state = graph.invoke(State({"user_query": input("enter query : ")}))
#     print(updated_state)

while True:
    user_query = input("Enter query (type 'exit' to stop): ")
    if user_query.lower() == "exit":
        print("Exiting the chatbot...")
        break

    updated_state = graph.invoke(State({"user_query": user_query}))
    print(updated_state)