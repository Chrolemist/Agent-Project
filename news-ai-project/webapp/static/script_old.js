const newsArticles = document.getElementById('news-articles');
const searchInput = document.getElementById('search');
const themeSwitch = document.getElementById('theme-switch');

// Load news when page loads
document.addEventListener('DOMContentLoaded', loadNews);

async function loadNews() {
    try {
        const response = await fetch('/api/news');
        const data = await response.json();
        displayNews(data.news);
    } catch (error) {
        console.error('Error loading news:', error);
        newsArticles.innerHTML = '<p>Fel vid laddning av nyheter</p>';
    }
}

function displayNews(articles) {
    newsArticles.innerHTML = ''; // Clear previous articles

    articles.forEach(article => {
        const articleElement = document.createElement('div');
        articleElement.classList.add('news-article');
        articleElement.innerHTML = `
            <h2>${article.title}</h2>
            <p>${article.summary}</p>
            <small>Publicerad: ${new Date(article.timestamp).toLocaleString('sv-SE')}</small>
        `;
        newsArticles.appendChild(articleElement);
    });
}

function searchNews(query) {
    const filteredArticles = newsData.filter(article =>
        article.title.toLowerCase().includes(query.toLowerCase()) ||
        article.summary.toLowerCase().includes(query.toLowerCase())
    );
    displayNews(filteredArticles);
}


function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

//Initial Display
displayNews(newsData);


//Search functionality
searchInput.addEventListener('input', () => searchNews(searchInput.value));


//Dark Mode Toggle
themeSwitch.addEventListener('change', toggleDarkMode);

//Check Local Storage for Dark Mode
const isDarkMode = localStorage.getItem('darkMode') === 'true';
if(isDarkMode) {
    document.body.classList.add('dark-mode');
    themeSwitch.checked = true;
}