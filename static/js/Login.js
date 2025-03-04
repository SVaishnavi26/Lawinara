// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.toggle-password');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Handle login form submission
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    if (!username || !password) {
        alert('Please fill in all fields');
        return false;
    }
    
    // Show loading overlay
    loadingOverlay.style.display = 'flex';
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            localStorage.setItem('userInfo', JSON.stringify({
                username: data.username,
                isLoggedIn: true,
                loginTime: new Date().toISOString()
            }));
            
            window.location.href = "/home";
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Login failed. Please try again.');
    } finally {
        loadingOverlay.style.display = 'none';
    }
    
    return false;
}