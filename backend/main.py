from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import asyncio
import re
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from langchain_core.documents import Document
import json

app = FastAPI(title="Student Loan AI Assistant", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    response: str
    tools_used: List[str] = []

class LoanCalculatorRequest(BaseModel):
    name: str
    income: float
    family_size: int
    loan_balance: float
    loan_type: str = "federal"
    current_plan: str = "standard"

class LoanCalculatorResponse(BaseModel):
    timeline: str
    monthly_payment: float
    total_paid: float
    years_to_payoff: float

def clean_markdown(text: str) -> str:
    """Remove markdown formatting from text"""
    # Remove bold formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove italic formatting
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove code formatting
    text = re.sub(r'`(.*?)`', r'\1', text)
    # Convert markdown links to plain text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove markdown headers (###, ##, #)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Remove table formatting
    # Remove table headers with | separators
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)
    # Remove table separator rows (| --- | --- |)
    text = re.sub(r'^\|[\s\-:|]+\|$', '', text, flags=re.MULTILINE)
    # Remove remaining table cell separators
    text = re.sub(r'\s*\|\s*', ' ', text)
    # Remove leading/trailing | characters
    text = re.sub(r'^\|\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*\|$', '', text, flags=re.MULTILINE)
    
    # Remove horizontal rules
    text = re.sub(r'^[\-\*_]{3,}$', '', text, flags=re.MULTILINE)
    
    # Remove extra newlines and spaces
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

# Initialize tools
@tool
def tool_comparison_tool(question: str) -> str:
    """
    Expert tool that compares existing loan repayment plans (SAVE, PAYE, IBR) to the new RAP plan.
    Use this when users ask about existing plans to translate them to the new RAP plan.
    """
    response = f"Comparing existing plans to RAP: {question}. The new RAP plan offers improved terms compared to traditional SAVE, PAYE, and IBR plans."
    return clean_markdown(response)

@tool
def timeline_tool(user_info: str) -> str:
    """
    Simulates loan balance over time under the new megabill RAP plan.
    Use this to show users how their loans will be paid off over time.
    """
    # Parse user information
    try:
        info = json.loads(user_info)
        name = info.get('name', 'User')
        income = info.get('income', 50000)
        family_size = info.get('family_size', 1)
        loan_balance = info.get('loan_balance', 30000)
        
        # Calculate RAP plan details
        # RAP plan: 5% of discretionary income for undergraduate loans
        # Discretionary income = AGI - 225% of federal poverty line
        poverty_line = 14580 + (family_size - 1) * 5140  # 2024 federal poverty line
        discretionary_income = max(0, income - (2.25 * poverty_line))
        monthly_payment = min(discretionary_income * 0.05 / 12, loan_balance * 0.01)  # Cap at 1% of balance
        
        # Calculate timeline
        if monthly_payment > 0:
            years_to_payoff = loan_balance / (monthly_payment * 12)
            total_paid = monthly_payment * 12 * years_to_payoff
        else:
            years_to_payoff = 25  # Maximum repayment period
            total_paid = loan_balance
        
        timeline_response = f"""
Personalized RAP Plan Timeline for {name}:

Current Loan Balance: ${loan_balance:,.2f}
Annual Income: ${income:,.2f}
Family Size: {family_size}

Monthly Payment: ${monthly_payment:.2f}
Years to Payoff: {years_to_payoff:.1f} years
Total Amount Paid: ${total_paid:,.2f}

Timeline Breakdown:
- Year 1: Balance reduces to ${max(0, loan_balance - monthly_payment * 12):,.2f}
- Year 5: Balance reduces to ${max(0, loan_balance - monthly_payment * 60):,.2f}
- Year 10: Balance reduces to ${max(0, loan_balance - monthly_payment * 120):,.2f}

The RAP plan offers more favorable terms than traditional plans, with payments based on your income and family size.
        """
        
        return clean_markdown(timeline_response)
        
    except Exception as e:
        return clean_markdown(f"Error processing timeline: {str(e)}. Please provide valid financial information.")

@tool
def complete_form_tool(user_info: str) -> str:
    """
    Processes user form information and generates personalized loan repayment analysis.
    Use this when users provide their financial information.
    """
    try:
        info = json.loads(user_info)
        response = f"""
Thank you for providing your information! I've processed your details:

Name: {info.get('name', 'N/A')}
Income: ${info.get('income', 0):,.2f}
Family Size: {info.get('family_size', 1)}
Loan Balance: ${info.get('loan_balance', 0):,.2f}
Loan Type: {info.get('loan_type', 'federal')}
Current Plan: {info.get('current_plan', 'standard')}

Now generating your personalized RAP plan timeline...
        """
        return clean_markdown(response)
        
    except Exception as e:
        return clean_markdown(f"Error processing form: {str(e)}. Please provide valid information.")

# Initialize external tools
tavily_tool = TavilySearchResults(max_results=5)

# Tool belt
tool_belt = [
    tavily_tool,
    tool_comparison_tool,
    timeline_tool,
    complete_form_tool,
]

# Initialize model
model = ChatOpenAI(model="gpt-4.1", temperature=0)
model = model.bind_tools(tool_belt)

# Agent state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    context: List[Document]

# Model call function
def call_model(state):
    messages = state["messages"]
    response = model.invoke(messages)
    return {
        "messages": [response],
        "context": state.get("context", [])
    }

# Tool node
tool_node = ToolNode(tool_belt)

# Build graph
uncompiled_graph = StateGraph(AgentState)
uncompiled_graph.add_node("agent", call_model)
uncompiled_graph.add_node("action", tool_node)
uncompiled_graph.set_entry_point("agent")

def should_continue(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "action"
    return END

uncompiled_graph.add_conditional_edges("agent", should_continue)
uncompiled_graph.add_edge("action", "agent")
compiled_graph = uncompiled_graph.compile()

@app.get("/")
async def root():
    return {"message": "Student Loan AI Assistant API"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Convert history to LangChain messages
        messages = []
        for msg in request.history:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))
        
        # Add current message
        messages.append(HumanMessage(content=request.message))
        
        # Initialize state
        inputs = {"messages": messages}
        
        # Track tools used
        tools_used = []
        
        # Process through graph
        async for chunk in compiled_graph.astream(inputs, stream_mode="updates"):
            for node, values in chunk.items():
                if node == "action" and values["messages"]:
                    tool_name = values["messages"][0].name
                    if tool_name:
                        tools_used.append(tool_name)
        
        # Get final response
        final_state = await compiled_graph.ainvoke(inputs)
        final_message = final_state["messages"][-1]
        
        # Clean markdown from response
        cleaned_response = clean_markdown(final_message.content)
        
        return ChatResponse(
            response=cleaned_response,
            tools_used=tools_used
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/loan-calculator", response_model=LoanCalculatorResponse)
async def loan_calculator(request: LoanCalculatorRequest):
    try:
        # Create user info string for tools
        user_info = json.dumps({
            "name": request.name,
            "income": request.income,
            "family_size": request.family_size,
            "loan_balance": request.loan_balance,
            "loan_type": request.loan_type,
            "current_plan": request.current_plan
        })
        
        # First process the form
        form_response = complete_form_tool(user_info)
        
        # Then generate timeline
        timeline_response = timeline_tool(user_info)
        
        # Calculate payment details
        poverty_line = 14580 + (request.family_size - 1) * 5140
        discretionary_income = max(0, request.income - (2.25 * poverty_line))
        monthly_payment = min(discretionary_income * 0.05 / 12, request.loan_balance * 0.01)
        
        if monthly_payment > 0:
            years_to_payoff = request.loan_balance / (monthly_payment * 12)
            total_paid = monthly_payment * 12 * years_to_payoff
        else:
            years_to_payoff = 25
            total_paid = request.loan_balance
        
        return LoanCalculatorResponse(
            timeline=timeline_response,
            monthly_payment=monthly_payment,
            total_paid=total_paid,
            years_to_payoff=years_to_payoff
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 