from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import RetryPolicy
from langgraph.graph import StateGraph, START, END
from state import EmailAgentState
from nodes import (
    read_email,
    classify_intent,
    search_documentation,
    bug_tracking,
    draft_response,
    human_review,
    send_reply,
)

# create the graph
workflow = StateGraph(EmailAgentState)

# Add nodes with appropriate error handling
workflow.add_node("read_email", read_email)
workflow.add_node("classify_intent", classify_intent)
# Add retry policy to the nodes that might have transient failures
workflow.add_node(
    "search_documentation",
    search_documentation,
    retry_policy=RetryPolicy(max_attempts=3),
)
workflow.add_node("bug_tracking", bug_tracking)
workflow.add_node("draft_response", draft_response)
workflow.add_node("human_review", human_review)
workflow.add_node("send_reply", send_reply)

# Add only the essential edges
workflow.add_edge(START, "read_email")
workflow.add_edge("read_email", "classify_intent")
workflow.add_edge("send_reply", END)

# Compile with checkpointer for persistence, in case run graph with local server ---> please compile without checkpointer
memory = MemorySaver()

app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "customer_123"}}
results = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "I was charged twice for my subscription! This is urgent for me!",
            }
        ]
    },
    config=config
)

for msg in results["messages"]:
    msg.pretty_print()
