#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified News Generation System
Genererar bara nyhetsartiklar utan webbkod
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import codecs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Add project paths
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "agents"))

# Import CrewAI components
from crewai import Agent, Task, Crew
import google.generativeai as genai

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

class SimpleNewsGenerator:
    def __init__(self):
        self.setup_agents()
    
    def setup_agents(self):
        """Setup simplified news agents"""
        from crewai.llm import LLM
        
        # Configure LLM
        self.llm = LLM(
            model="gemini/gemini-1.5-flash",
            api_key=os.getenv('GEMINI_API_KEY')
        )
        
        # News Writer Agent
        self.news_writer = Agent(
            role="Senior Nyhetsredaktör",
            goal="Skriva aktuella och engagerande nyhetsartiklar på svenska",
            backstory="""Du är en erfaren svensk journalist med 20 års erfarenhet. 
            Du specialiserar dig på att skriva tydliga, faktabaserade artiklar som engagerar läsarna.
            Du skriver alltid på svenska och följer journalistiska standarder.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def generate_news(self, topic="allmänna nyheter"):
        """Generate news articles on given topic"""
        
        task = Task(
            description=f"""Skriv 3 korta nyhetsartiklar om {topic}.
            
            För varje artikel:
            1. Skriv en fängslande rubrik
            2. Skriv 2-3 stycken med relevant innehåll
            3. Använd aktuella händelser eller trovärdiga scenarion
            4. Skriv på svenska
            
            Format för varje artikel:
            # [Rubrik]
            
            [Innehåll stycke 1]
            
            [Innehåll stycke 2]
            
            Källa: [Lämplig källa]
            Datum: {datetime.now().strftime("%Y-%m-%d")}
            
            ---
            
            """,
            agent=self.news_writer,
            expected_output="3 nyhetsartiklar i markdown-format med rubriker, innehåll, källor och datum"
        )
        
        crew = Crew(
            agents=[self.news_writer],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result

def save_articles(content, output_dir="output/articles"):
    """Save generated articles to files"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Split content by article separator
    articles = str(content).split("---")
    created_files = []
    
    for i, article in enumerate(articles):
        article = article.strip()
        if not article:
            continue
            
        # Extract title from first line
        lines = article.split('\n')
        title = "artikel"
        for line in lines:
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                title = title.replace(' ', '_').replace(':', '').replace('?', '').replace('!', '')[:50]
                break
        
        # Save article
        filename = f"artikel_{i+1}_{title}.md"
        filepath = Path(output_dir) / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(article)
            created_files.append(str(filepath))
            print(f"Skapade: {filepath}")
        except Exception as e:
            print(f"Fel vid skapande av {filename}: {e}")
    
    return created_files

def main():
    """Main function"""
    print("Simplified News Generation System")
    print("=" * 40)
    
    try:
        # Get topic from user input
        topic = input("Ämne för nyheter: ").strip()
        if not topic:
            topic = "allmänna nyheter Sverige"
        
        print(f"Genererar nyheter om: {topic}")
        
        # Generate news
        generator = SimpleNewsGenerator()
        result = generator.generate_news(topic)
        
        # Save articles
        created_files = save_articles(result)
        
        print(f"Genererade {len(created_files)} artiklar")
        print("Klart!")
        
    except Exception as e:
        print(f"Fel: {e}")

if __name__ == "__main__":
    main()
