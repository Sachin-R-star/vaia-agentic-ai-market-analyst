"""VAIA Agentic AI Market Analyst

Full-featured market research and analysis agent using Claude AI
with FastAPI web interface.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Any

import anthropic
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="VAIA Agentic AI Market Analyst",
    description="Market research and analysis powered by Claude AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Constants
MARKET_RESEARCH_FILE = "data/market_research.txt"
MODEL = "claude-3-5-sonnet-20241022"

# Pydantic models
class AnalysisRequest(BaseModel):
    """Request model for market analysis"""
    query: str
    market: Optional[str] = None
    context: Optional[str] = None

class AnalysisResponse(BaseModel):
    """Response model for market analysis"""
    query: str
    analysis: str
    market: Optional[str] = None
    timestamp: str
    thinking_process: Optional[str] = None

class CompetitorAnalysis(BaseModel):
    """Competitor analysis response"""
    competitor_name: str
    strengths: list[str]
    weaknesses: list[str]
    market_share: Optional[str] = None
    recommendations: list[str]

# Helper functions
def load_market_research() -> str:
    """Load market research data from file"""
    try:
        with open(MARKET_RESEARCH_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No market research data available."

def extract_json_from_response(response_text: str) -> dict[str, Any]:
    """Extract JSON from response text"""
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            return {}
    return {}

def format_market_context(market: Optional[str]) -> str:
    """Format market context for the agent"""
    market_research = load_market_research()
    context = f"Current market research data:\\n{market_research}\\n\\n"
    
    if market:
        context += f"Focus on {market} market.\\n"
    
    return context

# Agent tools
def process_with_agent(
    query: str,
    market: Optional[str] = None,
    context: Optional[str] = None
) -> dict[str, Any]:
    """Process query using Claude as an agent with extended thinking"""
    
    # Prepare system message
    system_message = """You are VAIA, an expert market research and analysis agent. 
You have deep knowledge of various markets, competitive landscapes, and industry trends.

Your responsibilities:
1. Analyze market trends and competitive landscapes
2. Provide strategic insights and recommendations
3. Identify market opportunities and threats
4. Assess competitor positioning and strategies
5. Generate actionable insights for business decisions

Always structure your analysis clearly with sections for:
- Executive Summary
- Market Overview
- Key Findings
- Competitive Analysis
- Recommendations
- Risk Assessment
"""
    
    # Build the user message
    user_message = format_market_context(market) + "\\n\\n" + query
    if context:
        user_message += f"\\n\\nAdditional context:\\n{context}"
    
    # Use extended thinking for deeper analysis
    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        thinking={
            "type": "enabled",
            "budget_tokens": 10000
        },
        temperature=1,
        system=system_message,
        messages=[{
            "role": "user",
            "content": user_message
        }]
    )
    
    # Extract thinking and analysis
    thinking_process = None
    analysis_text = ""
    
    for block in response.content:
        if block.type == "thinking":
            thinking_process = block.thinking
        elif block.type == "text":
            analysis_text = block.text
    
    return {
        "analysis": analysis_text,
        "thinking_process": thinking_process,
        "stop_reason": response.stop_reason
    }

# API Endpoints
@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API information"""
    return {
        "message": "Welcome to VAIA Agentic AI Market Analyst",
        "version": "1.0.0",
        "description": "Market research and analysis powered by Claude AI",
        "endpoints": {
            "analyze": "/analyze",
            "competitor-analysis": "/competitor-analysis",
            "market-trend": "/market-trend",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    request: AnalysisRequest
) -> AnalysisResponse:
    """Perform market analysis on a given query"""
    try:
        result = process_with_agent(
            query=request.query,
            market=request.market,
            context=request.context
        )
        
        return AnalysisResponse(
            query=request.query,
            analysis=result["analysis"],
            market=request.market,
            timestamp=datetime.now().isoformat(),
            thinking_process=result.get("thinking_process")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/competitor-analysis")
async def competitor_analysis(
    competitor: str = Query(..., description="Competitor name"),
    market: Optional[str] = Query(None, description="Market focus")
) -> dict[str, Any]:
    """Analyze a specific competitor"""
    try:
        query = f"Provide a detailed competitive analysis of {competitor}"
        if market:
            query += f" in the {market} market"
        
        result = process_with_agent(
            query=query,
            market=market
        )
        
        return {
            "competitor": competitor,
            "analysis": result["analysis"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-trend")
async def market_trend(
    market: str = Query(..., description="Market to analyze"),
    timeframe: Optional[str] = Query(None, description="Timeframe for analysis")
) -> dict[str, Any]:
    """Analyze market trends"""
    try:
        query = f"Analyze current trends in the {market} market"
        if timeframe:
            query += f" over the {timeframe}"
        
        result = process_with_agent(
            query=query,
            market=market
        )
        
        return {
            "market": market,
            "timeframe": timeframe,
            "trend_analysis": result["analysis"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/strategic-recommendation")
async def strategic_recommendation(
    request: AnalysisRequest
) -> dict[str, Any]:
    """Get strategic recommendations based on market analysis"""
    try:
        enhanced_query = f"""Based on your analysis, provide strategic recommendations for: {request.query}
        
Structure your response as:
1. Short-term actions (0-3 months)
2. Medium-term strategy (3-12 months)
3. Long-term positioning (1+ years)
4. Key success factors
5. Risks to monitor
        """
        
        result = process_with_agent(
            query=enhanced_query,
            market=request.market,
            context=request.context
        )
        
        return {
            "query": request.query,
            "recommendations": result["analysis"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
