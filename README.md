# CrewAI News Production System

Ett avancerat AI-drivet nyhetssystem som använder CrewAI för att skapa professionella nyhetsartiklar och webbsidor.

## ✨ Funktioner

- 🤖 **AI-Nyhetsteam**: Specialiserade agenter för research, skrivande, fact-checking och webbutveckling
- 📰 **Automatisk Nyhetsproduktion**: Från ämne till färdig webbsida
- 🌐 **Modern Webbsida**: Responsiv design med dark/light mode
- 🔍 **Fact-Checking**: Automatisk verifiering av källor och information
- 📱 **Responsiv Design**: Fungerar på alla enheter

## 🏗️ Projektstruktur

```
Agent-Project/
├── main.py                 # Huvudapplikation
├── requirements.txt        # Python dependencies
├── config/                 # Konfigurationsfiler
│   ├── .env               # Environment variabler
│   └── .env.example       # Exempel på environment
├── agents/                 # AI-agenter
│   └── news_team.py       # Nyhetsteam implementation
├── scripts/               # Hjälpskript
│   └── file_helper.py     # Filhantering
├── webapp/                # Genererad webbapplikation
│   ├── main.py           # FastAPI server
│   ├── static/           # Statiska filer
│   └── templates/        # HTML templates
└── output/               # Genererat innehåll
    ├── articles/         # Nyhetsartiklar
    └── full_output_*.md  # Komplett agent-output
```

## 🚀 Snabbstart

### 1. Installation

```bash
# Klona eller ladda ner projektet
cd Agent-Project

# Skapa virtual environment
python -m venv venv

# Aktivera virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installera dependencies
pip install -r requirements.txt
```

### 2. Konfiguration

Kopiera `.env.example` till `.env` och lägg till dina API-nycklar:

```bash
cp config\.env.example config\.env
```

Redigera `config\.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
SERPER_API_KEY=your_serper_api_key_here  # Optional för web search
```

### 3. Kör applikationen

```bash
python main.py
```

## 👥 AI-Agenter

### Research Journalist
- Söker och verifierar aktuella nyheter
- Använder pålitliga källor
- Samlar detaljerad information

### Senior News Writer
- Skriver engagerande artiklar
- Professionell journalistisk stil
- Strukturerat och lättläst innehåll

### Fact Checker
- Verifierar all information
- Kontrollerar källor och citat
- Säkerställer kvalitet

### Web Developer
- Skapar moderna webbsidor
- Responsiv design
- Modern UI/UX

```
Agent-Project/
├── venv/           # Virtuell Python-miljö
├── .git/           # Git repository
├── .gitignore      # Git ignore-filer
├── README.md       # Denna fil
└── news_agent/     # 📰 News Agent - AI-driven nyhetsanalys
    ├── main.py           # Huvudfil med fullständig nyhetsagent
    ├── simple_test.py    # Enkel testversion utan API-nycklar
    ├── .env.example      # Mall för miljövariabler
    └── README.md         # Projektdokumentation
```

## Projekt

### 📰 News Agent
En multi-agent system som:
- Hittar viktiga nyheter från olika källor
- Analyserar nyheternas betydelse och påverkan
- Skapar strukturerade sammanfattningar
- Genererar dagliga nyhetsrapporter

**Kör testet:**
```bash
cd news_agent
python simple_test.py
```

## Nästa steg

- [x] Skapa första AI-agenten (News Agent)
- [x] Testa multi-agent samarbete
- [ ] Lägg till riktiga nyhetskällor (NewsAPI)
- [ ] Utforska fler verktyg och integrationer
- [ ] Bygg automatiska schemalagda rapporter
