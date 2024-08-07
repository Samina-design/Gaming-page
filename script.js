// Smooth scrolling
function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}

// Form validation
// script.js
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = e.target.name.value;
    const email = e.target.email.value;
    const message = e.target.message.value;
    if (name && email && message) {
        alert('Form submitted successfully!');
    } else {
        alert('Please fill in all fields.');
    }
});

