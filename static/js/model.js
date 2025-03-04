document.addEventListener('DOMContentLoaded', function() {
    // Get the submit button and description textarea
    const submitButton = document.getElementById('submitCase');
    const descriptionInput = document.getElementById('caseDescription');
    const charCount = document.getElementById('currentCount');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const errorMessage = document.getElementById('errorMessage');
    
    // Character counter
    descriptionInput.addEventListener('input', function() {
        charCount.textContent = this.value.length;
    });
    
    // Sidebar Toggle Functionality
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    const toggleBtn = document.getElementById('toggleBtn');
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
    });
    
    // Add click event listener to submit button
    submitButton.addEventListener('click', function() {
        const description = descriptionInput.value.trim();
        
        if (description === '') {
            showError('Please enter a case description before submitting.');
            return;
        }
        
        if (description.length < 50) {
            showError('Description must be at least 50 characters long.');
            return;
        }
        
        // Show loading overlay
        loadingOverlay.classList.remove('hidden');
        
        // Send data to server
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ case_description: description })
        })
        .then(response => response.json())
        .then(data => {
            loadingOverlay.classList.add('hidden');
            
            if (data.error) {
                showError(data.error);
            } else if (data.redirect) {
                window.location.href = data.redirect;
            }
        })
        .catch(error => {
            loadingOverlay.classList.add('hidden');
            showError('An error occurred while processing your request.');
            console.error('Error:', error);
        });
    });
    
    // Error message handling
    function showError(message) {
        const errorText = errorMessage.querySelector('p');
        errorText.textContent = message;
        errorMessage.classList.remove('hidden');
        
        const closeBtn = errorMessage.querySelector('.close-error');
        closeBtn.addEventListener('click', function() {
            errorMessage.classList.add('hidden');
        });
    }
    
    // Close error on click
    document.querySelector('.close-error').addEventListener('click', function() {
        errorMessage.classList.add('hidden');
    });
});