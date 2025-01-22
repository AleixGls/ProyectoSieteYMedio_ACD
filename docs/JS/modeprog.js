const buttonMode = document.getElementById('Mode');
const buttonModee = document.getElementById('Modee');
const body = document.querySelector('body');
const navbar = document.querySelector('.navbar');
const navlinks = document.querySelector('.nav-links');
const footer = document.querySelector('.footer');
const tutorial1 = document.querySelector('.programacion-intro');
const tutorial2 = document.querySelectorAll('.programacion-details');
const tutorial3 = document.querySelectorAll('.programacion-item');

function applyDarkTheme() {
    body.classList.add('body-osc');
    navbar.classList.add('navbar-osc');
    footer.classList.add('footer-osc');
    navlinks.classList.add('nav-links-osc');
    tutorial1.classList.add('programacion-intro-osc');
    tutorial2.forEach(step => step.classList.add('programacion-details-osc'));
    tutorial3.forEach(step => step.classList.add('programacion-item-osc'));
    buttonMode.innerHTML = "☀️";
    localStorage.setItem('theme', 'dark');
}

function applyLightTheme() {
    body.classList.add('body');
    navbar.classList.add('navbar');
    footer.classList.add('footer');
    navlinks.classList.add('nav-links');
    tutorial1.classList.add('programacion-intro');
    tutorial2.forEach(step => step.classList.add('programacion-details'));
    tutorial3.forEach(step => step.classList.add('programacion-item'));
    buttonMode.innerHTML = "🌙";
    localStorage.setItem('theme', 'light');
}

function toggleTheme() {
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.remove('body-osc');
        navbar.classList.remove('navbar-osc');
        footer.classList.remove('footer-osc');
        navlinks.classList.remove('nav-links-osc');
        tutorial1.classList.remove('programacion-intro-osc');
        tutorial2.forEach(step => step.classList.remove('programacion-details-osc'));
        tutorial3.forEach(step => step.classList.remove('programacion-item-osc'));

        applyLightTheme();
    } else {
        body.classList.remove('body');
        navbar.classList.remove('navbar');
        footer.classList.remove('footer');
        navlinks.classList.remove('nav-links');
        tutorial1.classList.remove('programacion-intro');
        tutorial2.forEach(step => step.classList.remove('programacion-details'));
        tutorial3.forEach(step => step.classList.remove('programacion-item'));

        applyDarkTheme();
    }
}

// Initialize theme on page load
if (localStorage.getItem('theme') === 'dark') {
    applyDarkTheme();
} else {
    applyLightTheme();
}

// Event listeners
buttonMode.addEventListener('click', toggleTheme);
buttonModee.addEventListener('click', toggleTheme);

const menuIcon = document.getElementById('menuIcon');
const navLinks = document.querySelector('.nav-links');

menuIcon.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});
