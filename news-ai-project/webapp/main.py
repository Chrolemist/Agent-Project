import json
import os
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(parent_dir, '.env')
load_dotenv(env_path)

# Add parent directory to path to import our news system
sys.path.append(parent_dir)

app = FastAPI(title="AI News Web App")

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(script_dir, "static")

# Serve static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Global variable to store current news
current_news = [
    {
        "id": 1,
        "title": "AI revolutionerar svenska arbetsplatser",
        "summary": "Ny studie visar omfattande AI-adoption inom svensk industri",
        "source": "TechNews",
        "date": "2025-08-06"
    },
    {
        "id": 2,
        "title": "Klimatförändringar påverkar Sverige", 
        "summary": "Rekordtemperaturer uppmätta i norra Sverige",
        "source": "Klimatnyheterna",
        "date": "2025-08-06"
    },
    {
        "id": 3,
        "title": "Svensk startup får rekordinvestering",
        "summary": "AI-företag samlar in 100 miljoner kronor",
        "source": "Startup Sweden",
        "date": "2025-08-06"
    }
]

class NewsRequest(BaseModel):
    topic: str = "allmänna nyheter"

# Import AI system
try:
    from crewai import Agent, Task, Crew
    from crewai.llm import LLM
    import google.generativeai as genai
    
    # Configure Gemini API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    
    def create_news_agent():
        """Create a simple news generation agent"""
        llm = LLM(
            model="gemini/gemini-1.5-flash",
            api_key=os.getenv('GEMINI_API_KEY')
        )
        
        return Agent(
            role="Nyhetsredaktör",
            goal="Skriva korta nyhetsartiklar på svenska",
            backstory="Du är en svensk journalist som skriver korta, faktabaserade nyheter.",
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
    
    def generate_simple_news(topic):
        """Generate simple news articles"""
        agent = create_news_agent()
        
        task = Task(
            description=f"""Skriv 3 korta nyheter om {topic}. 
            Varje nyhet ska vara 1-2 meningar och ha en tydlig rubrik.
            Skriv BARA rubrik och innehåll, inget annat format.
            
            Exempel:
            Ny AI-teknik lanseras i Sverige
            Svenska forskare har utvecklat en revolutionerande AI-teknik som kan förbättra sjukvården betydligt.
            
            Klimatmål uppnås före tid  
            Sverige når sina klimatmål två år tidigare än planerat tack vare ökad användning av förnybar energi.""",
            agent=agent,
            expected_output="3 korta nyheter med rubrik och innehåll"
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        
        result = crew.kickoff()
        return str(result)
    
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    def generate_simple_news(topic):
        return f"Mock news about {topic}"

# Serve static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse(os.path.join(static_dir, 'index.html'))

@app.get("/api/news")
async def get_news():
    """Get current news articles"""
    return {"news": current_news}

@app.post("/api/generate-news")
async def generate_news(request: NewsRequest):
    """Generate new news using AI system"""
    try:
        if not AI_AVAILABLE:
            return {"status": "error", "message": "AI system not available"}
        
        # Generate news content
        content = generate_simple_news(request.topic)
        
        # Parse the generated content into articles
        articles = parse_news_content(content, request.topic)
        
        if articles:
            global current_news
            current_news = articles
            return {"status": "success", "message": f"Genererade {len(articles)} nya artiklar!", "articles": articles}
        else:
            return {"status": "warning", "message": "Kunde inte generera användbara artiklar"}
            
    except Exception as e:
        return {"status": "error", "message": f"Fel vid nyhetsgenereringen: {str(e)}"}

def parse_news_content(content, topic):
    """Parse AI-generated content into structured articles"""
    articles = []
    lines = content.split('\n')
    
    current_title = ""
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line looks like a title (short and doesn't end with period)
        if len(line) < 100 and not line.endswith('.') and not line.startswith('-'):
            # Save previous article if we have one
            if current_title and current_content:
                articles.append({
                    "id": len(articles) + 1,
                    "title": current_title,
                    "summary": ' '.join(current_content)[:200] + '...' if len(' '.join(current_content)) > 200 else ' '.join(current_content),
                    "source": "AI Nyhetsredaktion",
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
            
            # Start new article
            current_title = line
            current_content = []
        else:
            # Add to current article content
            if current_title:  # Only add content if we have a title
                current_content.append(line)
    
    # Don't forget the last article
    if current_title and current_content:
        articles.append({
            "id": len(articles) + 1,
            "title": current_title,
            "summary": ' '.join(current_content)[:200] + '...' if len(' '.join(current_content)) > 200 else ' '.join(current_content),
            "source": "AI Nyhetsredaktion",
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    
    return articles[:3]  # Max 3 articles

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
