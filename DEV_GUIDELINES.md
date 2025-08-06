# Development Guidelines & Lessons Learned

## ⚠️ VIKTIGA LÄRDOMAR - LÄS DETTA FÖRST!

### 🔴 TERMINAL & ENVIRONMENT HANTERING

**PROBLEM:** Skapande av nya terminaler hela tiden orsakar environment-problem
- Virtuell miljö (venv) aktiveras inte automatiskt i nya terminaler
- Python-versioner blir inkonsistenta mellan terminaler
- Import-problem och "ModuleNotFoundError" uppstår
- Onödigt många terminaler skapas (15+ terminaler observerat)

**LÖSNING:**
1. **ANVÄND EN TERMINAL PER SESSION** - Skapa inte nya terminaler i onödan
2. **Konfigurera Python-miljön FÖRST** med `configure_python_environment`
3. **Aktivera venv KORREKT** innan alla Python-kommandon
4. **Använd samma terminal** för relaterade kommandon
5. **Endast skapa nya terminaler** för bakgrundsprocesser som behöver köra parallellt

**KORREKT ARBETSFLÖDE:**
```bash
# 1. Konfigurera miljön EN GÅNG
configure_python_environment(resourcePath="projekt_path")

# 2. Aktivera venv i EN terminal
cd "C:\Agent project\Agent-Project"
.\venv\Scripts\Activate.ps1

# 3. Använd SAMMA terminal för alla kommandon
cd "specific_project_folder"
python script.py
pip install package
python another_script.py
```

**UNDVIK:**
- ❌ Skapa ny terminal för varje Python-kommando
- ❌ Blanda `isBackground=true` och `isBackground=false` utan kontroll
- ❌ Köra Python utan att verifiera att venv är aktiverat
- ❌ Använda system Python istället för venv Python

### 🔴 API-NYCKEL SÄKERHET

**PROBLEM:** Hårdkodade API-nycklar i koden före Git push
- Risk för att läcka känslig information till GitHub
- API-nycklar synliga i källkod

**LÖSNING:**
1. **ALLTID skapa `.env` fil** för känsliga uppgifter
2. **Använd `python-dotenv`** för att ladda environment variables
3. **Verifiera `.gitignore`** utesluter `.env` filer
4. **Sök efter hårdkodade nycklar** innan Git push
5. **Använd `os.getenv()`** istället för direkta strängar

### 🔴 PROJEKTSTRUKTUR

**PROBLEM:** Konfliktfiler i projektroten skapar förvirring
- Gamla `main.py` i root konfliktar med nya filer
- Python hittar fel filer pga sökvägar

**LÖSNING:**
1. **Organisera i underkataloger** per projekt
2. **Ta bort gamla konfliktfiler** från root
3. **Använd absoluta sökvägar** när nödvändigt
4. **Dokumentera projektstruktur** tydligt

## 📁 NUVARANDE PROJEKTSTRUKTUR

```
Agent-Project/ (ROOT)
├── DEV_GUIDELINES.md        # DENNA FIL - LÄS VID PROBLEM!
├── venv/                   # Python virtual environment  
├── .gitignore             # Exkluderar .env filer
├── README.md              # Projekt översikt
├── requirements.txt       # Global dependencies
├── config/                # Konfigurationsfiler
├── scripts/               # Globala scripts
└── news-ai-project/       # 🗞️ AI NYHETSSYSTEM (KOMPLETT)
    ├── webapp/            # FastAPI webbapp
    ├── agents/            # CrewAI agents
    ├── output/            # Genererade artiklar  
    ├── simple_news.py     # Fristående generator
    ├── .env              # API nycklar (ALDRIG i git!)
    └── README.md         # Projektdokumentation
```

**VIKTIG PRINCIP:** Varje undermapp ska innehålla ETT komplett projekt.

## 🛠️ DEBUGGING CHECKLIST

När Python/import-problem uppstår:

1. **Kontrollera Python-miljö:**
   ```bash
   which python  # Ska peka på venv, inte system
   pip list      # Verifiera installerade paket
   ```

2. **Kontrollera aktuell katalog:**
   ```bash
   pwd           # Var befinner jag mig?
   ls -la        # Vilka filer finns här?
   ```

3. **Kontrollera venv:**
   ```bash
   echo $VIRTUAL_ENV  # Ska visa venv-sökväg
   ```

4. **Om miljöproblem:**
   - Använd `configure_python_environment` verktyget
   - Aktivera venv manuellt: `.\venv\Scripts\Activate.ps1`
   - Använd absolut Python-sökväg vid behov

## 📝 HISTORISKA PROBLEM

### Session Augusti 2025
- **Problem:** 15+ terminaler skapade, environment-kaos
- **Orsak:** Konstant skapande av nya terminaler med `run_in_terminal`
- **Lösning:** Använd EN terminal, konfigurera miljö ordentligt
- **Resultat:** Fungerade perfekt efter fix

### API-säkerhet Implementation
- **Problem:** Hårdkodade API-nycklar i 4 filer
- **Lösning:** Environment variables, .env fil, .gitignore uppdatering
- **Verifiering:** `grep_search` för att hitta alla förekomster

## 🎯 FRAMTIDA FÖRBÄTTRINGAR

1. **Automatisk environment-verifiering** innan Python-kommandon
2. **Terminal-återanvändning** som standard arbetssätt
3. **Säkerhetskontroller** före Git-operationer
4. **Projektmallar** för snabbare setup av nya projekt

---

**VIKTIG PÅMINNELSE:** Om du ser environment- eller terminal-problem, läs denna fil först innan du försöker lösa problemet!
