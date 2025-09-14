from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.graph import run_analyst

app = FastAPI(
    title="Market Insights Analyst API",
    description="An API for getting market insights using a multi-agent system."
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    report: str

@app.post("/analyze", response_model=QueryResponse)
async def analyze_market(request: QueryRequest):
    """
    Receives a financial query, runs it through the agent system,
    and returns a synthesized report.
    """
    print(f"Received query: {request.query}")
    try:
        report = run_analyst(request.query)
        return QueryResponse(report=report)
    except Exception as e:
        # Handle potential errors during the agent run
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Market Insights Analyst API"}