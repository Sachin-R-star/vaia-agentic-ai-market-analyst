# VAIA Agentic AI Market Analyst

## Overview

VAIA (Versatile AI for Analysis) is a sophisticated market research and analysis system powered by Claude AI. It leverages agentic AI with extended thinking capabilities to provide deep market insights, competitive analysis, and strategic recommendations.

## Features

- **Intelligent Market Analysis**: Analyze market trends and provide strategic insights
- **Competitor Analysis**: Deep dive into competitor positioning and strategies
- **Market Trend Identification**: Identify emerging trends and market opportunities
- **Strategic Recommendations**: Get actionable recommendations for business decisions
- **Extended Thinking**: Claude's thinking capability for deeper analysis
- **FastAPI Web Interface**: RESTful API for easy integration
- **Docker Support**: Containerized deployment for scalability

## Architecture

### Components

```
┌─────────────────────────────────────────┐
│         FastAPI Web Server              │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  API Endpoints                     │ │
│  │  - /analyze                        │ │
│  │  - /competitor-analysis            │ │
│  │  - /market-trend                   │ │
│  │  - /strategic-recommendation       │ │
│  │  - /health                         │ │
│  └───────────────────────────────────┘ │
│                 │                       │
│                 ▼                       │
│  ┌───────────────────────────────────┐ │
│  │  Agent Processor                   │ │
│  │  (Claude with Extended Thinking)  │ │
│  └───────────────────────────────────┘ │
│                 │                       │
│                 ▼                       │
│  ┌───────────────────────────────────┐ │
│  │  Anthropic API                     │ │
│  │  (Claude 3.5 Sonnet)               │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Tech Stack

- **Framework**: FastAPI
- **AI Model**: Claude 3.5 Sonnet with Extended Thinking
- **Server**: Uvicorn
- **Language**: Python 3.11
- **Containerization**: Docker
- **API Documentation**: Automatic Swagger UI

## Setup Instructions

### Prerequisites

- Python 3.11+
- pip or conda
- Anthropic API Key
- Docker (optional)

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sachin-R-star/vaia-agentic-ai-market-analyst.git
   cd vaia-agentic-ai-market-analyst
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

5. **Run the application**:
   ```bash
   python src/main.py
   ```

6. **Access the API**:
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Docker Setup

1. **Build Docker image**:
   ```bash
   docker build -t vaia-market-analyst .
   ```

2. **Run container**:
   ```bash
   docker run -e ANTHROPIC_API_KEY="your-api-key-here" \
              -p 8000:8000 \
              vaia-market-analyst
   ```

## API Endpoints

### 1. Root Endpoint

**GET** `/`

Returns API information and available endpoints.

```bash
curl http://localhost:8000/
```

### 2. Health Check

**GET** `/health`

Check API availability.

```bash
curl http://localhost:8000/health
```

### 3. Market Analysis

**POST** `/analyze`

Perform comprehensive market analysis.

**Request Body**:
```json
{
  "query": "Analyze the current state of the AI market in 2024",
  "market": "Artificial Intelligence",
  "context": "Focus on emerging startups and their innovations"
}
```

**Response**:
```json
{
  "query": "Analyze the current state of the AI market in 2024",
  "analysis": "Detailed market analysis...",
  "market": "Artificial Intelligence",
  "timestamp": "2024-10-30T10:30:00",
  "thinking_process": "Extended thinking analysis..."
}
```

### 4. Competitor Analysis

**GET** `/competitor-analysis`

Analyze a specific competitor.

**Query Parameters**:
- `competitor` (required): Competitor name
- `market` (optional): Market focus

```bash
curl "http://localhost:8000/competitor-analysis?competitor=OpenAI&market=Generative%20AI"
```

### 5. Market Trend Analysis

**GET** `/market-trend`

Analyze market trends.

**Query Parameters**:
- `market` (required): Market to analyze
- `timeframe` (optional): Timeframe for analysis

```bash
curl "http://localhost:8000/market-trend?market=Cloud%20Computing&timeframe=2024"
```

### 6. Strategic Recommendations

**POST** `/strategic-recommendation`

Get strategic recommendations based on market analysis.

**Request Body**:
```json
{
  "query": "Market entry strategy for European AI market",
  "market": "Artificial Intelligence",
  "context": "Our company specializes in enterprise AI solutions"
}
```

## Demo Examples

### Example 1: Analyze AI Market

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the emerging opportunities in the AI market?",
    "market": "Artificial Intelligence"
  }'
```

### Example 2: Competitor Analysis

```bash
curl http://localhost:8000/competitor-analysis?competitor=Google&market=Cloud%20AI
```

### Example 3: Market Trend

```bash
curl http://localhost:8000/market-trend?market=Generative%20AI&timeframe=2024
```

## Technologies Used

### Core Technologies

- **Anthropic Claude 3.5 Sonnet**: Advanced language model with extended thinking
- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server implementation

### Additional Libraries

- `python-dotenv`: Environment variable management
- `requests`: HTTP client library
- `python-multipart`: Multipart form data support

### Development Tools

- `pytest`: Testing framework
- `pytest-asyncio`: Async testing support
- `black`: Code formatter
- `flake8`: Linting
- `mypy`: Type checking

## Project Structure

```
vaia-agentic-ai-market-analyst/
├── src/
│   └── main.py              # FastAPI application and agent logic
├── data/
│   └── market_research.txt  # Market research data
├── tests/
│   └── test_main.py         # Test suite
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitkeep                # Git placeholder files
```

## Future Enhancements

1. **Database Integration**: Add persistent storage for analysis history
2. **Real-time Data**: Integrate with financial data APIs
3. **Advanced Visualization**: Add charts and graphs for insights
4. **Multi-language Support**: Support for multiple languages
5. **Custom Training**: Fine-tuning on domain-specific data
6. **Batch Processing**: Support for batch analysis requests
7. **Caching**: Implement caching for frequently requested analyses
8. **Authentication**: Add user authentication and API keys

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Author

Sachin-R-star

## Support

For support, please open an issue on GitHub or contact the maintainer.

---

**Last Updated**: October 30, 2024
