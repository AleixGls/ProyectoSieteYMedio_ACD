const buttonMode = document.getElementById('Mode');
const buttonModee = document.getElementById('Modee');
const body = document.querySelector('body');
const navbar = document.querySelector('.navbar');
const navlinks = document.querySelector('.nav-links');
const footer = document.querySelector('.footer');
const tutorial1 = document.querySelector('.equip-intro');
const tutorial2 = document.querySelector('.team-list');
const tutorial3 = document.querySelectorAll('.team-member');

function applyDarkTheme() {
    body.classList.add('body-osc');
    navbar.classList.add('navbar-osc');
    footer.classList.add('footer-osc');
    navlinks.classList.add('nav-links-osc');
    tutorial1.classList.add('equip-intro-osc');
    tutorial2.classList.add('team-list-osc');
    tutorial3.forEach(step => step.classList.add('team-member-osc'));
    buttonMode.innerHTML = "☀️";
    localStorage.setItem('theme', 'dark');
}

function applyLightTheme() {
    body.classList.add('body');
    navbar.classList.add('navbar');
    footer.classList.add('footer');
    navlinks.classList.add('nav-links');
    tutorial1.classList.add('equip-intro');
    tutorial2.classList.add('team-list');
    tutorial3.forEach(step => step.classList.add('team-member'));
    buttonMode.innerHTML = "🌙";
    localStorage.setItem('theme', 'light');
}

function toggleTheme() {
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.remove('body-osc');
        navbar.classList.remove('navbar-osc');
        footer.classList.remove('footer-osc');
        navlinks.classList.remove('nav-links-osc');
        tutorial1.classList.remove('equip-intro-osc');
        tutorial2.classList.remove('team-list-osc');
        tutorial3.forEach(step => step.classList.remove('team-member-osc'));
        applyLightTheme();
    } else {
        body.classList.remove('body');
        navbar.classList.remove('navbar');
        footer.classList.remove('footer');
        navlinks.classList.remove('nav-links');
        tutorial1.classList.remove('equip-intro');
        tutorial2.classList.remove('team-list');
        tutorial3.forEach(step => step.classList.remove('team-member'));
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
