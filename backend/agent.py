import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# NEW: Import the memory module
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

try:
    from backend.tools import get_claim_info, update_claim_status
except ImportError:
    from tools import get_claim_info, update_claim_status

@tool
def lookup_claim(claim_id: int) -> str:
    """
    Looks up the details of an insurance claim by its unique ID.
    Returns a summary text string containing the claim status, the user's name, and the claim amount.
    If the claim doesn't exist, it explains that the claim was not found in the database.
    Use this tool whenever a user asks about the status of a specific claim number.
    
    Args:
        claim_id (int): The unique integer ID of the insurance claim to look up.
    """
    return get_claim_info(claim_id)

@tool
def change_claim_status(claim_id: int, new_status: str) -> str:
    """
    Updates or changes the status of an insurance claim.
    Use this tool whenever a user asks to modify or change a claim's status (e.g., to 'Approved' or 'Denied').
    
    Args:
        claim_id (int): The unique integer ID of the insurance claim to update.
        new_status (str): The new status string to apply to the claim.
    """
    return update_claim_status(claim_id, new_status)


# --- GLOBAL SCOPE ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
tools = [lookup_claim, change_claim_status]

# NEW: Create the memory notepad
memory = MemorySaver()

decision_rules = """You are the Claimpilot Decision Agent. Your job is to evaluate insurance claims based on extracted document data.
Strict Company Policy:

If a claim amount is LESS than 20,000rs, you must AUTOMATICALLY APPROVE it. You must immediately use your change_claim_status tool to update the database to 'Approved'. After the tool runs, inform the user that the claim was auto-approved and the database was updated.

If a claim amount is 20,000rs or MORE, you must NOT use your write tool. You must halt and output exactly: 'I recommend HUMAN REVIEW', followed by your mathematical reasoning."""

# NEW: Attach the memory to the agent!
agent_executor = create_react_agent(llm, tools, checkpointer=memory, prompt=decision_rules)
# --------------------


def main():
    # Test the agent locally with memory
    config = {"configurable": {"thread_id": "demo_terminal_session"}}
    
    query1 = "What is the status of claim #1?"
    print(f"\nAsking Agent: '{query1}'")
    inputs1 = {"messages": [("user", query1)]}
    for s in agent_executor.stream(inputs1, config=config, stream_mode="values"):
        s["messages"][-1].pretty_print()

    query2 = "Wait, who does that claim belong to again?"
    print(f"\nAsking Agent: '{query2}'")
    inputs2 = {"messages": [("user", query2)]}
    for s in agent_executor.stream(inputs2, config=config, stream_mode="values"):
        s["messages"][-1].pretty_print()

if __name__ == '__main__':
    main()