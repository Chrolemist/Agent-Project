#!/usr/bin/env python3
"""
File Implementation Helper
Hjälper agenter att skapa faktiska filer från deras output
"""

import os
import re
from pathlib import Path
from datetime import datetime

def create_file_from_content(content: str, base_path: str = "webapp") -> dict:
    """
    Skapar filer baserat på agent-content med kodblock
    
    Args:
        content: Agent output med kodblock
        base_path: Bas-sökväg för filer
    
    Returns:
        dict: Status och skapade filer
    """
    created_files = []
    errors = []
    
    # Hitta alla kodblock med filnamn
    pattern = r'```(\w+)?\s*(?:<!--\s*(.+?)\s*-->)?\s*\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    # Alternativt mönster för explicit filnamn
    filename_pattern = r'(?:Fil:|File:|Filename:|Filnamn:)\s*`?([^\n`]+)`?\s*\n```(?:\w+)?\s*\n(.*?)\n```'
    filename_matches = re.findall(filename_pattern, content, re.DOTALL)
    
    # Bearbeta filename_matches först
    for filename, file_content in filename_matches:
        filename = filename.strip()
        try:
            file_path = Path(base_path) / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content.strip())
            
            created_files.append(str(file_path))
            print(f"Skapade: {file_path}")
            
        except Exception as e:
            errors.append(f"Fel vid skapande av {filename}: {e}")
    
    # Bearbeta vanliga kodblock
    for lang, comment, code_content in matches:
        if comment:  # Om det finns en kommentar som kan vara filnamn
            filename = comment.strip()
        else:
            # Gissa filnamn baserat på språk
            if lang == 'html':
                filename = 'index.html'
            elif lang == 'css':
                filename = 'styles.css'
            elif lang == 'javascript' or lang == 'js':
                filename = 'script.js'
            elif lang == 'json':
                filename = 'data.json'
            elif lang == 'python' or lang == 'py':
                filename = 'app.py'
            else:
                continue  # Skippa om vi inte kan gissa filnamn
        
        try:
            file_path = Path(base_path) / filename
            
            # Skippa om filen redan skapats
            if str(file_path) in created_files:
                continue
                
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code_content.strip())
            
            created_files.append(str(file_path))
            print(f"Skapade: {file_path}")
            
        except Exception as e:
            errors.append(f"Fel vid skapande av {filename}: {e}")
    
    return {
        'created_files': created_files,
        'errors': errors,
        'success': len(errors) == 0
    }

def extract_articles_to_markdown(content: str, output_dir: str = "output") -> dict:
    """
    Extraherar nyhetsartiklar till separata markdown-filer
    
    Args:
        content: Agent output med artiklar
        output_dir: Output-mapp
    
    Returns:
        dict: Status och skapade filer
    """
    created_files = []
    errors = []
    
    # Hitta artiklar (markdown headers + content)
    article_pattern = r'#{1,2}\s+(.+?)\n(.*?)(?=\n#{1,2}\s|\Z)'
    articles = re.findall(article_pattern, content, re.DOTALL)
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for i, (title, article_content) in enumerate(articles):
        try:
            # Skapa filnamn från titel
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            filename = f"artikel_{i+1}_{safe_title[:50]}.md"
            
            file_path = output_path / filename
            
            # Skriv artikel med titel
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n{article_content.strip()}\n")
            
            created_files.append(str(file_path))
            print(f"📰 Skapade artikel: {file_path}")
            
        except Exception as e:
            errors.append(f"Fel vid skapande av artikel {i+1}: {e}")
    
    return {
        'created_files': created_files,
        'errors': errors,
        'success': len(errors) == 0
    }

def save_content_to_file(content: str, filename: str, directory: str = "output") -> bool:
    """
    Sparar content till en specifik fil
    
    Args:
        content: Innehåll att spara
        filename: Filnamn
        directory: Mapp
    
    Returns:
        bool: True om lyckat
    """
    try:
        file_path = Path(directory) / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Sparade: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Fel vid sparande av {filename}: {e}")
        return False

def create_project_structure(base_path: str = "webapp") -> None:
    """Skapar grundläggande projektstruktur"""
    
    directories = [
        base_path,
        f"{base_path}/static",
        f"{base_path}/static/css",
        f"{base_path}/static/js",
        f"{base_path}/static/images",
        f"{base_path}/templates",
        "output",
        "output/articles"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print(f"Skapade projektstruktur i {base_path}")

if __name__ == "__main__":
    # Test funktionalitet
    test_content = """
    # Test Artikel
    
    Detta är en test artikel.
    
    ```html
    <!-- index.html -->
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body><h1>Test</h1></body>
    </html>
    ```
    
    ```css
    body { margin: 0; padding: 20px; }
    ```
    """
    
    create_project_structure()
    result = create_file_from_content(test_content)
    print(f"Test resultat: {result}")
