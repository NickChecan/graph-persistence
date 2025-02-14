from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# MemorySaver is a checkpoint which stores the state after each node execution
# It is ephemeral, which means it will be gone after the execution ends
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    input: str
    user_feedback: str

def step_1(state: State) -> None:
    print("---Step 1---")

def human_feedback(state: State) -> None:
    print("---human_feedback---")

def step_3(state: State) -> None:
    print("---Step 3---")

builder = StateGraph(State)

builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)

builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)

memory = MemorySaver()

# The following arguments (checkpointer and interrupt_before) will stop the graph
# before the "human_feedback" node is executed, checkpoint the state of the graph
# and get the input of the user before resume its execution
graph = builder.compile(checkpointer=memory, interrupt_before=["human_feedback"])

print(graph.get_graph().draw_mermaid())
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    # Thread ID represents a session/conversation and will enable us to
    # differentiate between different runs of the same graph
    thread = {"configurable": {"thread_id": "1"}}

    initial_input = {"input": "hello world"}

    for event in graph.stream(initial_input, thread, stream_mode="values"):
        print(event)

    print(graph.get_state(thread).next)

    user_input = input("Tell me how you want to update the state: ")

    graph.update_state(thread, {"user_feedback": user_input}, as_node="human_feedback")

    print("--State after update--")
    print(graph.get_state(thread))

    for event in graph.stream(None, thread, stream_mode="values"):
        print(event)