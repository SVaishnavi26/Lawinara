document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    const toggleBtn = document.getElementById('toggleBtn');
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');

    // Toggle sidebar
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
    });

    // Search functionality
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });

    function handleSearch() {
        const searchTerm = searchInput.value.trim();
        if (searchTerm) {
            fetch(`/search?q=${encodeURIComponent(searchTerm)}`)
                .then(response => response.json())
                .then(data => console.log('Search Results:', data))
                .catch(error => console.error('Error:', error));
        }
    }

    // Navigation Function
    function navigateTo(page) {
        window.location.href = page;
    }

    // Responsive Sidebar
    function checkWindowSize() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('expanded');
        } else {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('expanded');
        }
    }

    // Check window size on load and resize
    window.addEventListener('resize', checkWindowSize);
    checkWindowSize();

    // Check login state on page load
    function checkLoginState() {
        fetch('/check-login')
            .then(response => response.json())
            .then(data => {
                if (data.loggedIn) {
                    document.querySelector('.auth-buttons').style.display = 'none';
                }
            })
            .catch(error => console.error('Error:', error));
    }

    checkLoginState();
});