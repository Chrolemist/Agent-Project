# AI News Generator

Ett CrewAI-baserat system för att generera svenska nyhetsartiklar med artificiell intelligens.

## Funktioner

- **AI-genererade nyheter** med Gemini 1.5 Flash
- **FastAPI webapp** för webbaserat gränssnitt
- **Multi-agent system** med specialiserade roller
- **Säker API-nyckel hantering** med environment variables

## Projektstruktur

```
news-ai-project/
├── webapp/           # FastAPI webbapplikation
├── agents/          # CrewAI agent definitioner
├── simple_news.py   # Fristående nyhetsgenerator
├── .env            # API nycklar (ej i git)
└── README.md       # Detta dokument
```

## Installation

1. Installera beroenden:
```bash
pip install crewai fastapi uvicorn python-dotenv google-generativeai
```

2. Skapa `.env` fil med din Gemini API-nyckel:
```
GEMINI_API_KEY=din_api_nyckel_här
```

## Användning

### Web App
```bash
cd webapp
python main.py
```
Öppna sedan http://localhost:8000

### Fristående Generator
```bash
python simple_news.py
```

## Säkerhet

- API-nycklar lagras i `.env` fil som är utesluten från git
- Alla känsliga data hanteras via environment variables

## Utveckling

Detta är en del av ett större Agent-Project som demonstrerar CrewAI:s kapaciteter.
