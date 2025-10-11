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
            Use this tool to get the most recent system statistics.
            It provides the total number of requests, total cost, and average latency
            for all LLM calls made in the last hour.
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
    llm = ChatOllama(model="llama3", temperature=0)
    
    # Get the tools
    tools = get_tools(db)
    
    # Create the agent using the compatible ReAct creator
    agent = create_react_agent(llm, tools, prompt)
    
    # Create the Agent Executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor