document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle Functionality
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    const toggleBtn = document.getElementById('toggleBtn');
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
    });
    
    // Navigation Function
    window.navigateTo = function(page) {
        window.location.href = page;
    };
    
    // Fetch predictions from the server
    fetch('/get_predictions')
        .then(response => response.json())
        .then(data => {
            // Update the content divs with the prediction data
            document.getElementById('actSectionContent').textContent = data.act_section;
            document.getElementById('judgementContent').textContent = data.judgment;
        })
        .catch(error => {
            console.error('Error fetching predictions:', error);
            document.getElementById('actSectionContent').textContent = 'Error loading prediction';
            document.getElementById('judgementContent').textContent = 'Error loading prediction';
        });
    
    // Edit Description Button Functionality
    const editDescriptionBtn = document.querySelector('.edit-description-btn');
    if (editDescriptionBtn) {
        editDescriptionBtn.addEventListener('click', function() {
            window.location.href = editDescriptionBtn.getAttribute("data-url"); // Fetch URL dynamically
        });
    }
});