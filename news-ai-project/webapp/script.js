const newsArticles = document.getElementById('news-articles');
const searchInput = document.getElementById('search');
const themeSwitch = document.getElementById('theme-switch');

function displayNews(articles) {
    newsArticles.innerHTML = ''; // Clear previous articles

    articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.classList.add('news-article');
        articleDiv.innerHTML = `
            <img src="${article.image}" alt="${article.title}">
            <h2>${article.title}</h2>
            <p>${article.description}</p>
            <a href="${article.url}" target="_blank">Läs mer</a>
        `;
        newsArticles.appendChild(articleDiv);
    });
}


function searchNews(articles, searchTerm) {
    const filteredArticles = articles.filter(article =>
        article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        article.description.toLowerCase().includes(searchTerm.toLowerCase())
    );
    displayNews(filteredArticles);
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load news data
displayNews(newsData);

// Search functionality
searchInput.addEventListener('input', () => searchNews(newsData, searchInput.value));


// Dark mode toggle
themeSwitch.checked = localStorage.getItem('darkMode') === 'true';
themeSwitch.addEventListener('change', toggleDarkMode);

// Initial dark mode check from localStorage.
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}