// Load news from API
async function loadNews() {
    try {
        const response = await fetch('/api/news');
        const news = await response.json();
        displayNews(news);
    } catch (error) {
        console.error('Error loading news:', error);
        displayError('Kunde inte ladda nyheter');
    }
}

// Generate new news using AI
async function generateNews() {
    const generateBtn = document.getElementById('generate-news');
    const originalText = generateBtn.textContent;
    
    try {
        // Show loading state
        generateBtn.classList.add('loading');
        generateBtn.textContent = 'Genererar nyheter...';
        generateBtn.disabled = true;
        
        const topic = prompt('Välj ämne för nyheter (eller lämna tomt för allmänna nyheter):') || 'aktuella nyheter Sverige';
        
        const response = await fetch('/api/generate-news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic })
        });
        
        if (response.ok) {
            const result = await response.json();
            alert('Nya nyheter genererade! Laddar om...');
            loadNews(); // Reload news
        } else {
            throw new Error('Failed to generate news');
        }
    } catch (error) {
        console.error('Error generating news:', error);
        alert('Kunde inte generera nyheter. Försök igen.');
    } finally {
        // Reset button state
        generateBtn.classList.remove('loading');
        generateBtn.textContent = originalText;
        generateBtn.disabled = false;
    }
}

function displayNews(articles) {
    const newsContainer = document.querySelector('.news-container');
    if (!newsContainer) {
        // Fallback to old structure
        const newsArticles = document.getElementById('news-articles');
        if (newsArticles) {
            newsArticles.innerHTML = '';
            articles.forEach(article => {
                const newsCard = document.createElement('div');
                newsCard.className = 'news-card';
                newsCard.innerHTML = `
                    <h3>${article.title}</h3>
                    <p class="summary">${article.summary}</p>
                    <div class="meta">
                        <span class="source">${article.source}</span>
                        <span class="date">${article.date}</span>
                    </div>
                `;
                newsArticles.appendChild(newsCard);
            });
            return;
        }
        return;
    }
    
    newsContainer.innerHTML = '';
    
    if (!articles || articles.length === 0) {
        newsContainer.innerHTML = '<p>Inga nyheter tillgängliga</p>';
        return;
    }
    
    articles.forEach(article => {
        const newsCard = document.createElement('div');
        newsCard.className = 'news-card';
        newsCard.innerHTML = `
            <h3>${article.title}</h3>
            <p class="summary">${article.summary}</p>
            <div class="meta">
                <span class="source">${article.source}</span>
                <span class="date">${article.date}</span>
            </div>
        `;
        newsContainer.appendChild(newsCard);
    });
}

function displayError(message) {
    const newsContainer = document.querySelector('.news-container') || document.getElementById('news-articles');
    if (newsContainer) {
        newsContainer.innerHTML = `<p class="error">${message}</p>`;
    }
}

// Theme toggle functionality
const themeToggle = document.querySelector('.theme-toggle') || document.getElementById('theme-switch');

if (themeToggle) {
    themeToggle.addEventListener('change', () => {
        document.body.classList.toggle('dark');
        localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
    });
}

// Load saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    document.body.classList.add('dark');
    if (themeToggle && themeToggle.type === 'checkbox') {
        themeToggle.checked = true;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadNews();
    
    // Add event listener for generate button
    const generateBtn = document.getElementById('generate-news');
    if (generateBtn) {
        generateBtn.addEventListener('click', generateNews);
    }
});
