"""VAIA Agentic AI Market Analyst

Full-featured market research and analysis agent using Google GenAI (Gemini)
with FastAPI web interface.
"""

import json
import os
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path 

# ✅ GOOGLE GENAI इम्पोर्ट करें (जो हमने इंस्टॉल किया था)
from google import genai 
from google.genai.errors import APIError as GenAI_APIError # GenAI API Errors के लिए

from fastapi import FastAPI, HTTPException, Query, Header, Depends 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- Authentication Configuration ---
# 🔑 VAIA API Key सीधे सेट करें
VAIA_AGENT_API_KEY = "VAIA_ASSIGNMENT_KEY_2025_SecretXyZ" 

# 🔑 GEMINI API Key (OpenAI की जगह) को सीधे सेट करें
# 🚨 यहाँ अपनी असली Gemini API Key पेस्ट करें
GEMINI_API_KEY = "AIzaSyDjNH4bTPSBBnhavbCq2sUrPb3Unc8cqCc" 

if not VAIA_AGENT_API_KEY or not GEMINI_API_KEY:
    print("Error: Required API keys are not configured!")
    pass 

async def verify_api_key(x_api_key: str = Header(..., alias="X-Api-Key")):
    """जाँचता है कि 'X-Api-Key' हेडर में दी गई API Key सही है या नहीं।"""
    if x_api_key != VAIA_AGENT_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Could not resolve authentication method. Invalid X-Api-Key provided."
        )
    return x_api_key

# --- End Authentication Logic ---

# ✅ Gemini Client का उपयोग करें
# client = OpenAI(api_key=OPENAI_API_KEY) # पुरानी लाइन
client = genai.Client(api_key=GEMINI_API_KEY)

# Constants
MARKET_RESEARCH_FILE = "data/market_research.txt"
MODEL = "gemini-2.5-flash" # ✅ मॉडल को Gemini में बदलें (तेज और कुशल)

app = FastAPI(
    title="VAIA Agentic AI Market Analyst (Gemini)",
    description="Market research and analysis powered by Google GenAI (Gemini)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    query: str
    market: Optional[str] = None
    context: Optional[str] = None

class AnalysisResponse(BaseModel):
    query: str
    analysis: str
    market: Optional[str] = None
    timestamp: str
    thinking_process: Optional[str] = None

# ... (बाकी Pydantic models वही रहेंगे) ...

def load_market_research() -> str:
    # फाइल एक्सेस लॉजिक वही रहेगा
    try:
        data_path = Path(__file__).resolve().parent.parent / MARKET_RESEARCH_FILE
        if not data_path.exists():
             return f"Error: Market research file not found at {data_path}"
             
        with open(data_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No market research data available."

def format_market_context(market: Optional[str]) -> str:
    market_research = load_market_research()
    context = f"Current market research data:\n{market_research}\n\n"
    if market:
        context += f"Focus on {market} market.\n"
    return context

def process_with_agent(
    query: str,
    market: Optional[str] = None,
    context: Optional[str] = None
) -> Dict[str, Any]:
    
    system_message = f"""You are VAIA, an expert market research and analysis agent. 
You have deep knowledge of various markets, competitive landscapes, and industry trends.
Your goal is to provide **precise, actionable, and data-driven insights** based on the user's query and the provided market context.

Your responsibilities:
1. **Analyze:** Carefully review the user's query and the current market research data.
2. **Synthesize:** Combine external knowledge with the internal market data to form a comprehensive analysis.
3. **Structure:** Present your analysis clearly using markdown (headings, bullet points, and bold text).
4. **Be Objective:** Maintain a professional and objective tone. Do not provide information outside the scope of market analysis.
"""

    user_message = format_market_context(market) + "\n\n" + query
    if context:
        user_message += f"\n\nAdditional context provided by user:\n{context}"

    try:
        # 🚨 Google GenAI API Call (generate_content)
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                {"role": "user", "parts": [{"text": user_message}]},
            ],
            # Gemini के लिए System Instruction इस तरह पास की जाती है
            config={"system_instruction": system_message},
        )
        
        # Gemini से कंटेंट निकालने का तरीका
        analysis_text = response.text
        
        return {
            "analysis": analysis_text,
            "thinking_process": None,
            "stop_reason": response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN"
        }
        
    # ✅ Google GenAI-विशिष्ट त्रुटियों को हैंडल करें
    except GenAI_APIError as e:
        print(f"Gemini API Error: {e}") 
        # API त्रुटियों को HTTP 500 में बदलें
        raise HTTPException(
            status_code=500, 
            detail=f"AI Agent Processing Error: Gemini API Error: {str(e)}"
        )
    except Exception as e:
        # अन्य सभी त्रुटियाँ
        print(f"General Processing Error: {e}")
        raise HTTPException(status_code=500, detail=f"AI Agent Processing Error: {str(e)}")


# --- सभी FastAPI Endpoints (जैसे /analyze, /strategic-recommendation) वही रहेंगे ---
# मैंने उन्हें छोटा कर दिया है ताकि कोड दोहराया न जाए, लेकिन आपके कोड में वे पूरी तरह से मौजूद हैं।

@app.get("/")
async def root() -> dict:
# ... (बाकी root फ़ंक्शन) ...
    return {
        "message": "Welcome to VAIA Agentic AI Market Analyst (Gemini)",
        "version": "1.0.0",
        "description": "Market research and analysis powered by Google GenAI (Gemini)",
        "endpoints": {
            "analyze": "/analyze (POST)",
            "competitor-analysis": "/competitor-analysis (GET)",
            "market-trend": "/market-trend (GET)",
            "strategic-recommendation": "/strategic-recommendation (POST)",
            "health": "/health (GET)"
        }
    }
@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    request: AnalysisRequest,
    api_key: str = Depends(verify_api_key) 
) -> AnalysisResponse:
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/competitor-analysis")
async def competitor_analysis(
    competitor: str = Query(..., description="Competitor name"),
    market: Optional[str] = Query(None, description="Market focus"),
    api_key: str = Depends(verify_api_key) 
) -> dict:
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-trend")
async def market_trend(
    market: str = Query(..., description="Market to analyze"),
    timeframe: Optional[str] = Query(None, description="Timeframe for analysis"),
    api_key: str = Depends(verify_api_key) 
) -> dict:
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/strategic-recommendation")
async def strategic_recommendation(
    request: AnalysisRequest,
    api_key: str = Depends(verify_api_key) 
) -> dict:
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
if __name__ == "__main__":
    import uvicorn
    import logging
    logging.basicConfig(level=logging.INFO) 

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )