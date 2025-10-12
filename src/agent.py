from sqlalchemy.orm import Session
from langchain_ollama import ChatOllama
# REVERT: Go back to using the ReAct agent
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain.prompts import PromptTemplate

# Import our analysis function
from . import analysis

# 1. Define the Tools (No changes here)
def get_tools(db: Session):
    tools = [
        Tool(
            name="get_system_statistics",
            func=lambda _: analysis.get_stats_for_last_hour(db),
            description="""
            Use this tool to get the most recent overall system statistics.
            It provides the total number of requests, total cost, and average latency
            for all LLM calls made in the last hour.
            """
        ),
        # --- ADD THE NEW TOOL HERE ---
        Tool(
            name="find_highest_cost_users",
            func=lambda top_n_str: analysis.find_top_cost_users(db, int(top_n_str.strip("'\" "))),
            description="""
            Use this tool to find the users who have incurred the most cost.
            The input to this tool should be a single integer representing the
            number of top users to find. For example, '5' would find the top 5 users.
            """
        ),
    ]
    return tools

# 2. Use our custom, improved prompt template
AGENT_PROMPT_TEMPLATE = """
You are a helpful AI monitoring assistant. Your goal is to answer the user's question about system performance.
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: You should always think about what to do to answer the Question.
Action: The action to take, should be one of [{tool_names}]
Action Input: The input to the action
Observation: The result of the action
Thought: I have now received the result from the tool. I have enough information to answer the user's original question.
Final Answer: A human-readable summary of the observation that directly answers the user's Question.

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

# 3. Set up the ReAct Agent (which we know is compatible)
def create_monitoring_agent(db: Session):
    # Create the prompt from our good template
    prompt = PromptTemplate.from_template(AGENT_PROMPT_TEMPLATE)
    
    # Initialize the LLM
    llm = ChatOllama(model="qwen3:8b", temperature=0)
    
    # Get the tools
    tools = get_tools(db)
    
    # Create the agent using the compatible ReAct creator
    agent = create_react_agent(llm, tools, prompt)
    
    # Create the Agent Executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def generate_alert_message(reason: str):
    """
    Uses the LLM to generate a human-readable alert message.
    """
    # Initialize a new LLM instance for this task
    llm = ChatOllama(model="qwen3:8b", temperature=0)
    
    prompt = f"""
    You are an AI monitoring system. An anomaly has been detected in the system for the following reason:
    
    REASON: "{reason}"
    
    Write a brief, clear, and professional alert message (2-3 sentences) to be sent to the engineering team.
    """
    
    # Invoke the LLM directly with the prompt
    response = llm.invoke(prompt)
    
    # The response object has a 'content' attribute with the text
    return response.content