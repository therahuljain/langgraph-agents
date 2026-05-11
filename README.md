# LangGraph Agents

A multi-agent chatbot built with LangGraph that intelligently routes user messages to specialized agents based on message classification.

## Overview

This project demonstrates an agentic workflow where incoming messages are classified as either **emotional** or **logical**, and then routed to the appropriate agent:

- **Therapist Agent**: Responds with empathy and emotional support to messages expressing feelings or personal experiences
- **Logical Agent**: Provides analytical and informative responses to fact-based or problem-solving queries

The system uses LLM-powered classification to determine the optimal response style for each user message.

## Features

- 🤖 Message classification using structured LLM outputs
- 🔀 Intelligent routing to specialized agents
- 🧠 Context-aware responses using LangGraph state management
- 💬 Interactive chat interface
- 🔐 Secure API key management via environment variables

## Setup

### Prerequisites

- Python 3.11+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd langgraph-agents
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the chatbot:
```bash
python main.py
```

Then interact with the chatbot by typing messages. Type `exit` to quit.

### Example Interactions

**Emotional Message:**
```
Message: I'm feeling really overwhelmed with work lately
```
→ Routed to Therapist Agent for empathetic support

**Logical Message:**
```
Message: How do I optimize database queries?
```
→ Routed to Logical Agent for technical analysis

## Project Structure

```
langgraph-agents/
├── main.py              # Main application with graph definition
├── pyproject.toml       # Project metadata and dependencies
├── .env                 # Environment variables (not tracked in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## How It Works

1. **Classify**: User message is analyzed and classified as emotional or logical
2. **Route**: The classifier result routes the message to the appropriate agent
3. **Respond**: The selected agent generates a contextually appropriate response
4. **Output**: Response is returned to the user

## Dependencies

- `langgraph`: Agentic workflow orchestration
- `langchain`: LLM integrations and utilities
- `langchain-openai`: OpenAI model support
- `python-dotenv`: Environment variable management

## Technologies

- **LLM**: GPT-4o Mini (OpenAI)
- **Framework**: LangGraph
- **Language**: Python 3.11+

## License

MIT