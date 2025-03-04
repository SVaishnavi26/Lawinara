const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleBtn');
const mainContent = document.getElementById('main-content');

// Toggle sidebar
toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
});

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
window.addEventListener('load', checkWindowSize);
window.addEventListener('resize', checkWindowSize);

document.addEventListener('DOMContentLoaded', function() {
    // Make sure mainContent is defined when DOM is loaded
    if (!mainContent) {
        const mainContentElement = document.getElementById('main-content');
        if (mainContentElement) {
            mainContent = mainContentElement;
            checkWindowSize(); // Apply appropriate classes based on window size
        }
    }

    // Animate elements on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });

    // Observe all major sections
    document.querySelectorAll('.law-category, .feature, .highlight-item').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
});