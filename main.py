from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

load_dotenv()

llm = init_chat_model("gpt-5-mini", model_provider="openai", temperature=0.7)

class MessageClassifier(BaseModel):
    message_type: Literal["emotional", "logical"] = Field(
        ..., 
        description="Classify if the message requires an emotional or logical response"
        )    


class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_types: str | None



def classify_message(state: State):
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)

    result = classifier_llm.invoke(
            [
                {"role": "system", 
                 "content": """Classify the user's message into one of two categories: "emotional" or "logical".
                 - "emotional" messages express feelings, emotions, or personal experiences and may require empathy, support, or understanding in the response.
                 - "logical" messages are focused on facts, reasoning, or problem-solving and may require a more analytical or informative response."""},
                {"role": "user", "content": last_message.content}
            ]
        )
    return {"message_types": result.message_type}


def router(state: State):  
    message_type = state.get("message_types", "logical")
    if message_type == "emotional":
        return {"next": "therapist"}
    
    return {"next": "logical"}


def therapist_agent(state: State):
    last_message = state["messages"][-1]
    messages = [{"role": "system", "content": "You are a compassionate therapist. Respond empathetically and emotionally to  the user's message."}
                , {"role": "user", "content": last_message.content}]
    
    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}

def logical_agent(state: State):
    last_message = state["messages"][-1]
    messages = [{"role": "system", "content": "You are a logical assistant. Respond analytically and informatively to the user's message."}
                , {"role": "user", "content": last_message.content}]

    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}

graph_builder = StateGraph(State)

# def chatbot(state: State):
#     return {"messages": [llm.invoke(state["messages"])]}


# graph_builder.add_node("chatbot", chatbot)

# graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("chatbot", END)

graph_builder.add_node("classify", classify_message)
graph_builder.add_node("router", router)
graph_builder.add_node("therapist", therapist_agent)
graph_builder.add_node("logical", logical_agent)

graph_builder.add_edge(START, "classify")
graph_builder.add_edge("classify", "router")
graph_builder.add_conditional_edges("router", lambda state: state.get("next"),
                                    {"therapist": "therapist", "logical": "logical"})

graph_builder.add_edge("therapist", END)
graph_builder.add_edge("logical", END)
    

graph = graph_builder.compile()



def run_chatbot():
    state = {"messages": [], "message_type": None}
    
    while True:
        user_input = input("Message: ")
        if user_input.lower() == "exit":
            print("Exiting chatbot. Goodbye!")
            break

        state["messages"] = state.get("messages", []) + [{"role": "user", "content": user_input}]

        state = graph.invoke(state)

        if state.get("messages") and len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            print(f"Assistant: {last_message.content}")



if __name__ == "__main__":
    run_chatbot()          
# user_input = input("Enter your message: ")
# state = graph.invoke({"messages": [{"role": "user", "content": user_input}]})


# print(state["messages"][-1].content)

