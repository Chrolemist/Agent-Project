#!/usr/bin/env python3
"""
Advanced News Team - CrewAI Agents for News Generation
Skapar en komplett nyhetsteam med specialiserade agenter
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Load environment variables
load_dotenv(project_root / "config" / ".env")

from crewai import Agent, Task, Crew, Process
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class NewsTeam:
    """Professionellt nyhetsteam med specialiserade agenter"""
    
    def __init__(self):
        self.setup_agents()
    
    def setup_agents(self):
        """Skapar specialiserade nyhetsteam-agenter"""
        
        # Research Journalist
        self.researcher = Agent(
            role='Senior Research Journalist',
            goal='Hitta och verifiera aktuella nyheter från pålitliga källor',
            backstory="""Du är en erfaren undersökande journalist med 15 års 
            experience inom nyhetsbranschen. Du är expert på att hitta pålitliga 
            källor och verifiera information. Du har ett skarpt öga för detaljer 
            och kan snabbt identifiera viktiga nyheter. Du använder dina kunskaper
            för att skapa trovärdiga och aktuella nyheter även utan direkta sources.""",
            verbose=True,
            allow_delegation=True,
            llm=self.get_gemini_llm()
        )
        
        # News Writer
        self.writer = Agent(
            role='Senior News Writer',
            goal='Skriva engagerande och professionella nyhetsartiklar',
            backstory="""Du är en prisbelönt journalist och författare som 
            specialiserat dig på att skriva fängslande nyhetsartiklar. Du behärskar 
            konsten att förmedla komplexa ämnen på ett enkelt och tillgängligt sätt. 
            Din skrivstil är både informativ och engagerande.""",
            verbose=True,
            allow_delegation=False,
            llm=self.get_gemini_llm()
        )
        
        # Fact Checker
        self.fact_checker = Agent(
            role='Senior Fact Checker',
            goal='Verifiera all information och säkerställa nyheternas riktighet',
            backstory="""Du är en pedantisk fact-checker med oöverträffad 
            uppmärksamhet för detaljer. Du har arbetat för stora nyhetsorganisationer 
            och din uppgift är att säkerställa att varje påstående är korrekt och 
            välunderbyggt. Du kontrollerar källor och ser till att allt är journalistiskt korrekt.""",
            verbose=True,
            allow_delegation=False,
            llm=self.get_gemini_llm()
        )
        
        # Web Developer
        self.web_developer = Agent(
            role='Full-Stack Web Developer',
            goal='Skapa moderna och responsiva webbsidor för nyhetsvisning',
            backstory="""Du är en expert på webbutveckling med djup kunskap inom 
            HTML, CSS, JavaScript och moderna ramverk. Du skapar snygga, responsiva 
            och användarvänliga webbsidor som fungerar perfekt på alla enheter.""",
            verbose=True,
            allow_delegation=False,
            llm=self.get_gemini_llm()
        )
    
    def get_gemini_llm(self):
        """Konfigurerar Gemini LLM"""
        return f"gemini/{os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')}"
    
    def create_news_research_task(self, topic="aktuella nyheter Sverige"):
        """Skapar en forskningsuppgift"""
        return Task(
            description=f"""Forska efter de senaste och viktigaste nyheterna om: {topic}
            
            Dina uppgifter:
            1. Sök efter aktuella nyheter från pålitliga svenska källor
            2. Identifiera de 3-5 viktigaste nyheterna idag
            3. Samla in detaljerad information om varje nyhet
            4. Notera källor och publiceringstid
            5. Prioritera nyheter efter relevans och aktualitet
            
            Resultat ska innehålla:
            - Rubrik för varje nyhet
            - Kort sammanfattning
            - Källa och datum
            - Viktiga detaljer och citat
            """,
            agent=self.researcher,
            expected_output="Strukturerad lista med 3-5 nyheter inklusive rubrik, sammanfattning, källa och detaljer"
        )
    
    def create_news_writing_task(self):
        """Skapar en skrivuppgift för nyhetsartiklar"""
        return Task(
            description="""Baserat på forskningsresultaten, skriv professionella nyhetsartiklar.
            
            För varje nyhet:
            1. Skriv en fängslande rubrik
            2. Skapa en engagerande ingress (lead)
            3. Strukturera artikeln med tydliga stycken
            4. Inkludera relevanta citat och detaljer
            5. Avsluta med relevant kontext eller bakgrund
            
            Artikelformat:
            - Rubrik (H1)
            - Ingress (fet text)
            - Huvudtext uppdelad i stycken
            - Källa och datum i slutet
            
            Skriv på svenska och använd professionell journalistisk stil.
            """,
            agent=self.writer,
            expected_output="3-5 fullständiga nyhetsartiklar i markdown-format",
            context=[self.create_news_research_task()]
        )
    
    def create_fact_check_task(self):
        """Skapar en fact-checking uppgift"""
        return Task(
            description="""Granska alla nyhetsartiklar för riktighet och kvalitet.
            
            Kontrollera:
            1. Faktisk korrekthet av alla påståenden
            2. Att källor är pålitliga och aktuella
            3. Att citat är korrekta och i rätt kontext
            4. Språk och grammatik
            5. Journalistisk standard och etik
            
            Om du hittar fel eller tveksamma påståenden:
            - Markera tydligt vad som behöver korrigeras
            - Föreslå förbättringar
            - Lägg till förslag på ytterligare källor vid behov
            
            Resultat: Godkända artiklar eller lista på nödvändiga korrigeringar.
            """,
            agent=self.fact_checker,
            expected_output="Kvalitetsgranskad rapport med godkända artiklar eller korrigeringslista",
            context=[self.create_news_writing_task()]
        )
    
    def create_website_task(self):
        """Skapar uppgift för att bygga nyhetssida"""
        return Task(
            description="""Skapa en modern nyhetssida för att visa artiklarna.
            
            Krav:
            1. Responsiv design som fungerar på mobil och desktop
            2. Modern och professionell design
            3. Snabb laddning och bra användarupplevelse
            4. Artiklar ska visas i en snygg layout
            5. Navigation mellan olika artiklar
            6. Sökfunktion
            7. Dark/light mode toggle
            
            Tekniska krav:
            - HTML5 semantisk markup
            - Modern CSS med Flexbox/Grid
            - Vanilla JavaScript för interaktivitet
            - Responsive design
            - Tillgänglighet (accessibility)
            
            Skapa separata filer:
            - index.html (huvudsida)
            - styles.css (all styling)
            - script.js (JavaScript funktionalitet)
            - news-data.js (nyhetsdata från artiklarna)
            """,
            agent=self.web_developer,
            expected_output="Komplett webbsida med HTML, CSS och JavaScript filer",
            context=[self.create_fact_check_task()]
        )
    
    def run_news_production(self, topic="aktuella nyheter Sverige"):
        """Kör hela nyhetsproduktionsprocessen"""
        
        # Skapa alla tasks
        research_task = self.create_news_research_task(topic)
        writing_task = self.create_news_writing_task()
        fact_check_task = self.create_fact_check_task()
        website_task = self.create_website_task()
        
        # Skapa crew
        news_crew = Crew(
            agents=[self.researcher, self.writer, self.fact_checker, self.web_developer],
            tasks=[research_task, writing_task, fact_check_task, website_task],
            process=Process.sequential,
            verbose=True
        )
        
        print("🚀 Startar nyhetsproduktion...")
        print(f"📰 Ämne: {topic}")
        print("=" * 50)
        
        # Kör crew
        result = news_crew.kickoff()
        
        return result


def main():
    """Huvudfunktion"""
    print("📰 CrewAI News Team - Avancerad Nyhetsproduktion")
    print("=" * 50)
    
    # Skapa news team
    news_team = NewsTeam()
    
    # Fråga användaren om ämne
    topic = input("Vilket ämne vill du ha nyheter om? (tom för 'aktuella nyheter Sverige'): ").strip()
    if not topic:
        topic = "aktuella nyheter Sverige"
    
    # Kör nyhetsproduktion
    try:
        result = news_team.run_news_production(topic)
        print("\n" + "=" * 50)
        print("✅ Nyhetsproduktion klar!")
        print("📁 Kontrollera 'webapp' mappen för den färdiga nyhetssidan")
        
    except Exception as e:
        print(f"❌ Fel inträffade: {e}")


if __name__ == "__main__":
    main()
