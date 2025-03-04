document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('toggleBtn');

  // Toggle sidebar functionality
  toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
  });

  function navigateTo(page) {
      const baseUrl = window.location.origin; // Gets the current domain (useful for deployment)
      window.open(`${baseUrl}/${page}`, '_blank'); // FIXED: Used template literal
  }

  // Assign navigation to all buttons
  const navButtons = document.querySelectorAll('.nav-btn');
  navButtons.forEach(button => {
      button.addEventListener('click', () => {
          const page = button.getAttribute('data-page');
          if (page) {
              navigateTo(page);
          }
      });
  });

  // Responsive handling
  function handleResponsiveness() {
      if (window.innerWidth <= 768) {
          sidebar.classList.add('collapsed');
      } else {
          sidebar.classList.remove('collapsed');
      }
  }

  // Check on load and resize
  handleResponsiveness();
  window.addEventListener('resize', handleResponsiveness);
});
