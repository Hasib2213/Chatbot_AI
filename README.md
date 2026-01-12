# Mobile App Support Chatbot

A FastAPI-based AI chatbot powered by Groq API that provides 24/7 intelligent support for mobile applications.

## 🎯 Features

- **24/7 Availability**: Real-time AI-powered support
- **Multi-Language Support**: Responds in user's preferred language
- **Fast Responses**: Powered by Groq's fast LLM inference
- **REST API**: Easy integration with frontend applications
- **Error Handling**: Comprehensive error messages and logging

## 📋 Requirements

- Python 3.8+ or Docker
- Groq API Key (Get from https://console.groq.com)
- FastAPI, Uvicorn, Pydantic, python-dotenv

## 🚀 Quick Start

### Option 1: Local Setup (Python Virtual Environment)

#### 1. Clone or Download the Project
```bash
cd ChatbotAI
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
MODEL=llama-3.3-70b-versatile
TEMPERATURE=0.7
MAX_TOKENS=1000
```

**Get your API Key:**
1. Go to https://console.groq.com
2. Sign up or log in
3. Create an API key
4. Copy and paste it in `.env` file

#### 5. Run the Application
```bash
# Option A: Direct Python
python main.py

# Option B: Using Uvicorn
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at: `http://127.0.0.1:8000`

---

### Option 2: Docker Setup

#### Prerequisites
- Docker installed on your system ([Download Docker](https://www.docker.com/products/docker-desktop))

#### 1. Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
MODEL=llama-3.3-70b-versatile
TEMPERATURE=0.7
MAX_TOKENS=1000
```

#### 2. Build and Run with Docker Compose
```bash
# Build and start the container
docker-compose up --build

# Run in background (detached mode)
docker-compose up -d --build

# View logs
docker-compose logs -f chatbot

# Stop the container
docker-compose down
```

#### 3. Or Build and Run Docker Image Manually
```bash
# Build the image
docker build -t chatbot-ai .

# Run the container
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_groq_api_key_here \
  -e MODEL=llama-3.3-70b-versatile \
  -e TEMPERATURE=0.7 \
  -e MAX_TOKENS=1000 \
  chatbot-ai
```

The API will be available at: `http://localhost:8000`

#### Docker Compose Services
- **chatbot**: Main API service running on port 8000

---

## 🐳 Docker Information

### Dockerfile
- Base image: `python:3.11-slim` (lightweight Python image)
- Exposes port: `8000`
- Auto-starts uvicorn server

### docker-compose.yml
- Automatically loads environment variables from `.env` file
- Mounts current directory for live code changes
- Includes volume mapping for development
- Auto-restart policy enabled

### Common Docker Commands
```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View container logs
docker logs chatbot-ai

# Stop container
docker stop chatbot-ai

# Remove container
docker rm chatbot-ai

# Remove image
docker rmi chatbot-ai
```

## 📚 API Endpoints

### Health Check
```bash
GET /health
```
**Response:**
```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile"
}
```

### Generate Response
```bash
POST /api/generate
```

**Request:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I add money to my wallet?"
    }
  ],
  "user_id": "user123"
}
```

**Response:**
```json
{
  "response": "To add money:\n- Go to Wallet → + Add Credits\n- Choose amount ($10, $25, $50, $100, $250, $500 or custom)\n- Pay with card → Balance added instantly.",
  "success": true,
  "error": null
}
```

## 📁 Project Structure

```
ChatbotAI/
├── main.py                 # FastAPI application
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── README.md              # This file
└── app/
    ├── LLM_Service/
    │   └── ai_service.py  # Groq service
    ├── prompts/
    │   └── system_prompt.py
    └── schema/
        └── schema.py      # Pydantic schemas
```

## 🔧 Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL=llama-3.3-70b-versatile
TEMPERATURE=0.7
MAX_TOKENS=1000
```

Get your API Key at: https://console.groq.com

## 📚 API Endpoints

### Health Check
```bash
GET /health
```

### Generate Response
```bash
POST /api/generate_chat
```

**Request:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Your question here"
    }
  ],
  "user_id": "user123"
}
```

**Response:**
```json
{
  "response": "AI response here",
  "success": true,
  "error": null
}
```

## 📝 Example Requests

### Using cURL
```bash
curl -X POST 'http://127.0.0.1:8000/api/generate_chat' \
  -H 'Content-Type: application/json' \
  -d '{
  "messages": [{"role": "user", "content": "Your question"}],
  "user_id": "user123"
}'
```

### Using Python
```python
import requests

response = requests.post(
    'http://127.0.0.1:8000/api/generate_chat',
    json={
        'messages': [{'role': 'user', 'content': 'Your question'}],
        'user_id': 'user123'
    }
)
print(response.json())
```

### Using JavaScript
```javascript
const response = await fetch('http://127.0.0.1:8000/api/generate_chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    messages: [{role: "user", content: "Your question"}],
    user_id: "user123"
  })
});
const data = await response.json();
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `GROQ_API_KEY not configured` | Check `.env` file, get key from https://console.groq.com |
| `Model has been decommissioned` | Update MODEL in `.env` to supported model |
| `Address already in use` | Change port: `uvicorn main:app --port 8001` |
| `Connection refused` | Ensure uvicorn is running and internet is connected |
| `Empty response` | Check max_tokens setting and message content |

## 🔐 Security

- API keys are protected in `.env` (not committed)
- Input validation on all endpoints
- Environment variables stored locally only
- Error handling prevents sensitive data leakage

## 📄 License

This project is for the Mobile App Support Platform.

**Support:** nikoo@app.com
