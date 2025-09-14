import os
import operator
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from tools.financial_tools import search_financial_news, get_stock_performance

load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file")


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

class MarketAnalystAgent:
    """
    This class defines the primary research agent.
    It is responsible for using tools to answer a user's query.
    """
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)
        
        self.tools = [search_financial_news, get_stock_performance]
        
        self.model_with_tools = self.model.bind_tools(self.tools)

    def research_node(self, state: AgentState):
        """
        This is the primary node for the research agent. It takes the current
        state (conversation history) and decides the next action.
        """
        print("---AGENT: Researching---")
        response = self.model_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue_node(self, state: AgentState) -> str:
        """
        This node determines the next step in the graph.
        - If the agent called a tool, we continue to the 'execute_tools' node.
        - If the agent did not call a tool, it means it's finished, so we end.
        """
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            print("---DECISION: Agent wants to use a tool---")
            return "continue"
        else:
            print("---DECISION: Agent is finished with research---")
            return "end"

    def execute_tools_node(self, state: AgentState):
        """
        This node executes the tools called by the agent and returns the results.
        """
        print("---ACTION: Executing Tools---")
        last_message = state["messages"][-1]
        tool_call = last_message.tool_calls[0]
        tool_map = {tool.name: tool for tool in self.tools}
        tool_to_call = tool_map[tool_call["name"]]
        observation = tool_to_call.invoke(tool_call["args"])
        return {"messages": [ToolMessage(content=str(observation), tool_call_id=tool_call['id'])]}

def build_agent_graph():
    """
    This function builds the LangGraph workflow.
    """
    agent = MarketAnalystAgent()

    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", agent.research_node)
    workflow.add_node("tools", agent.execute_tools_node)
    workflow.set_entry_point("researcher")

    workflow.add_conditional_edges(
        "researcher",
        agent.should_continue_node,
        {"continue": "tools", "end": END},
    )
    
    workflow.add_edge("tools", "researcher")

    return workflow.compile()

def get_writer_agent():
    """
    Creates a separate agent responsible for synthesizing the final report.
    This agent does not have tools.
    """
    writer_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert financial analyst. Your task is to synthesize the provided "
                "information into a clear, concise, and well-structured report. The information "
                "includes a user query and the results of tool calls (news articles, stock data). "
                "Do not add any information that is not present in the context. "
                "Base your entire response on the provided data. Structure your report with a "
                "clear title, a summary, and then detailed sections based on the findings."
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)
    writer_chain = writer_prompt | llm
    return writer_chain


graph = build_agent_graph()
writer = get_writer_agent()

def run_analyst(query: str):
    """
    The main entry point for running the multi-agent system.
    """
    print(f"\n--- Running Analyst for query: '{query}' ---")
    
    research_result = graph.invoke({"messages": [HumanMessage(content=query)]})

    final_report = writer.invoke({"messages": research_result['messages']})
    
    print("--- Analyst run complete. ---")
    return final_report.content