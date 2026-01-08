# 🚀 AI Content Crew

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-orange.svg)](https://crewai.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Transform any topic into comprehensive research reports and SEO-optimized blog posts in minutes using AI-powered multi-agent collaboration.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Output Examples](#output-examples)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**AI Content Crew** is a production-grade content generation system that uses multi-agent AI collaboration to create high-quality, research-backed content. Built with CrewAI and powered by GPT-4, it automates the entire workflow from research to publication-ready output.

### What It Does

✅ Researches your topic using real-time web search  
✅ Generates comprehensive 2000-word strategic reports  
✅ Creates engaging 500-word SEO-optimized blog posts  
✅ Ensures quality through automated fact-checking and editing  
✅ Completes in **1-2 minutes**

### Who It's For

- 📝 Content Creators
- 🏢 Marketing Teams
- 📊 Research Analysts
- 🚀 Startups & Agencies

---

## Features

### 🤖 Multi-Agent Intelligence
- **4 Specialized AI Agents** working in orchestrated collaboration
- Research Analyst → Report Writer → Blog Creator → Quality Editor

### 📊 Comprehensive Research
- Real-time web search integration
- Fact-checking and source verification
- Trend analysis and predictions
- Credible source citations

### 📝 Professional Output
- **2000-word strategic reports** with executive summaries
- **500-word blog posts** optimized for SEO
- Keywords, meta descriptions, and URL slugs included
- Publication-ready formatting

### ⚡ Fast & Efficient
- Complete workflow in **1-2 minutes**
- Caching to avoid redundant work
- Resource-optimized execution

### 🔌 API-First Design
- RESTful API for programmatic access
- Async job processing with status tracking
- Easy integration with existing systems

---

## Quick Start

### Prerequisites

- Python 3.12+ (3.10+ supported)
- OpenAI API Key ([Get it here](https://platform.openai.com/api-keys))
- Serper API Key ([Get free key](https://serper.dev) - 2,500 searches/month free)

### Installation
```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Clone the repository
git clone https://github.com/tanishra/ai-content-crew.git
cd ai-content-crew

# 3. Create virtual environment with uv
uv venv

# 4. Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 5. Install dependencies with uv (much faster!)
uv pip install -r requirements.txt

# 6. Set up environment variables
cp .env.example .env
# Edit .env with your API keys (use nano, vim, or any text editor)

# 7. Create required directories
mkdir -p output logs

# 8. Run your first generation
crewai run
```

### Environment Setup

Create a `.env` file with your API keys:
```env
# Required API Keys
OPENAI_API_KEY=sk-your-openai-key-here
SERPER_API_KEY=your-serper-key-here

# Optional Configuration
OPENAI_MODEL=gpt-4-turbo-preview
MAX_CONCURRENT_JOBS=5
DEBUG=false
```

### Verify Installation
```bash
# Test the installation
crewai run

# Or run with Python directly
python src/research_and_blog_crew/main.py run
```

---

## Usage

### CLI Usage
```bash
# Run with default topic
crewai run

# Run with custom topic (modify in main.py)
python main.py run --topic "Quantum Computing in 2026"

# Interactive mode
python main.py interactive

# Batch process multiple topics
python main.py batch --file topics.txt
```

### API Usage

#### 1. Start the API Server
```bash
# Development
uvicorn api.server:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn api.server:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 2. Generate Content
```bash
# Create a generation job
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"topic": "Future of Remote Work"}'

# Response
{
  "job_id": "a7b2c3d4-e5f6-4321-9876-543210fedcba",
  "status": "processing",
  "message": "Job started"
}
```

#### 3. Check Status
```bash
curl -X GET "http://localhost:8000/status/{job_id}" \
  -H "X-API-Key: your_api_key"

# Response
{
  "job_id": "a7b2c3d4-e5f6-4321-9876-543210fedcba",
  "status": "completed",
  "topic": "Future of Remote Work",
  "result": {
    "report": "output/strategic_report.md",
    "blog": "output/blog_post_with_seo.md"
  }
}
```

#### 4. Health Check
```bash
curl http://localhost:8000/health
```

### Interactive Mode
```bash
python main.py interactive
```
```
Welcome to AI Content Crew Interactive Mode!

Enter topic (or 'quit' to exit): Sustainable Energy
🚀 Generating content for: Sustainable Energy
⏱️  Processing... (1m 15s)
✅ Content generation complete!

Enter topic (or 'quit' to exit): quit
```

### Batch Processing

Create `topics.txt`:
```text
AI in Education
Blockchain for Supply Chain
Future of Electric Vehicles
Metaverse and Virtual Reality
```

Run:
```bash
python main.py batch --file topics.txt
```

---

## API Reference

### Authentication

All API requests require an API key in the header:
```bash
-H "X-API-Key: your_api_key_here"
```

### Endpoints

#### `POST /generate`
Create a new content generation job.

**Request:**
```json
{
  "topic": "string (required, max 200 chars)",
  "email": "string (optional)"
}
```

**Response:**
```json
{
  "job_id": "uuid",
  "status": "processing",
  "message": "Job started"
}
```

#### `GET /status/{job_id}`
Check the status of a generation job.

**Response:**
```json
{
  "job_id": "uuid",
  "status": "completed|processing|failed",
  "topic": "string",
  "created_at": "timestamp",
  "completed_at": "timestamp",
  "result": {
    "report": "path/to/report.md",
    "blog": "path/to/blog.md"
  }
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "timestamp"
}
```

### Rate Limits

| Plan       | Requests/Hour | Requests/Month |
|------------|---------------|----------------|
| Free       | 2             | 10             |
| Pro        | 20            | 100            |
| Enterprise | 100           | 1000           |

---

## Output Examples

### Strategic Report
```markdown
# The Future of Artificial Intelligence in Healthcare

## Executive Summary
AI is revolutionizing healthcare through diagnostic accuracy improvements 
of up to 95%, predictive analytics for patient outcomes, and automation 
of administrative tasks...

## Introduction
The healthcare industry stands at the precipice of a technological 
revolution...

## Current Landscape
### Diagnostic Applications
According to Stanford Medicine (2025), AI-powered diagnostic tools...

[... 2000 words total ...]

## References
1. Stanford Medicine (2025). "AI in Medical Diagnostics"
2. WHO Report (2025). "Global Health Technology Trends"
```

### Blog Post with SEO
```markdown
# Why AI Will Change Healthcare Forever (And What It Means For You)

Have you ever wondered how doctors will diagnose diseases in the future? 
The answer might surprise you...

[... 500 words total ...]

---
**SEO Package:**
- Primary Keyword: AI in Healthcare
- Secondary Keywords: medical AI, healthcare technology, AI diagnosis
- Meta Description: Discover how AI is transforming healthcare with 95% 
  diagnostic accuracy. Learn what this means for patients and doctors.
- URL Slug: ai-healthcare-future-guide
```

---

## Configuration

### Environment Variables
```env
# Required
OPENAI_API_KEY=sk-...
SERPER_API_KEY=...

# Optional
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-3.5-turbo for faster/cheaper
MAX_CONCURRENT_JOBS=5
CREW_MAX_RPM=30
OUTPUT_DIR=output
LOG_DIR=logs
DEBUG=false
```

### Agent Customization

Edit `config/agents.yaml` to customize agent behavior:
```yaml
research_analyst:
  max_iter: 15      # Maximum iterations per task
  verbose: true     # Enable detailed logging
```

### Task Customization

Edit `config/tasks.yaml` to modify task requirements:
```yaml
comprehensive_research_task:
  description: >
    Your custom task description...
  expected_output: >
    Your expected output format...
```

---

## Deployment

### Docker
```bash
# Build image
docker build -t ai-content-crew:latest .

# Run container
docker run -d \
  --name content-crew \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e SERPER_API_KEY=your_key \
  -v $(pwd)/output:/app/output \
  ai-content-crew:latest

# Or use docker-compose
docker-compose up -d
```

### Cloud Platforms

#### Railway.app (Recommended)
```bash
npm install -g @railway/cli
railway login
railway up
```

#### Render
1. Connect GitHub repository
2. Set environment variables in dashboard
3. Deploy

#### AWS EC2
```bash
# SSH into instance
ssh -i key.pem ubuntu@your-ip

# Clone and setup
git clone https://github.com/yourusername/ai-content-crew.git
cd ai-content-crew
pip install -r requirements.txt

# Run with PM2
pm2 start "uvicorn api.server:app --host 0.0.0.0 --port 8000" --name content-crew
```

---

## Troubleshooting

### Common Issues

#### API Key Errors
```bash
Error: 'SERPER_API_KEY'
```
**Solution:** Check your `.env` file has the correct API keys with no extra spaces.

#### Tool Not Found
```bash
KeyError: 'web_search_tool'
```
**Solution:** Ensure you've imported `tool` decorator:
```python
from crewai.project import CrewBase, agent, crew, task, tool
```

#### Slow Execution
**Solution:**
- Reduce `max_iter` in `config/agents.yaml` (15→10)
- Use `gpt-3.5-turbo` instead of `gpt-4`
- Enable caching: `CREW_CACHE=true`

#### Rate Limit Exceeded
**Solution:**
- Upgrade your Serper plan
- Reduce `CREW_MAX_RPM` in settings
- Add delays between requests

### Debug Mode

Enable detailed logging:
```bash
DEBUG=true python main.py run
```

Check logs:
```bash
tail -f logs/app.json
```

### Getting Help

- 📖 [Documentation](./docs)
- 🐛 [GitHub Issues](https://github.com/yourusername/ai-content-crew/issues)
- 📧 Email: support@yourproject.com

---

## 📁 Project Structure
```
ai-content-crew/
├── src/
│   └── research_and_blog_crew/
│       ├── main.py              # Entry point & CLI
│       ├── crew.py              # Crew configuration
│       └── config/
│           ├── agents.yaml      # Agent definitions
│           └── tasks.yaml       # Task definitions
├── api/
│   └── server.py                # FastAPI server
├── database/
│   └── models.py                # Database models
├── utils/
│   ├── logger.py                # Logging utilities
│   └── retry.py                 # Retry logic
├── output/                      # Generated content
├── logs/                        # Application logs
├── .env.example                 # Environment template
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

## Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by Tanish Rajput**

⭐ Star us on GitHub if this project helped you!

</div>