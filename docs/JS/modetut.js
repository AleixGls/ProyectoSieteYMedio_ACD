const buttonMode = document.getElementById('Mode');
const buttonModee = document.getElementById('Modee');
const body = document.querySelector('body');
const navbar = document.querySelector('.navbar');
const navlinks = document.querySelector('.nav-links');
const footer = document.querySelector('.footer');
const tutorial1 = document.querySelector('.tutorial-intro');
const tutorial2 = document.querySelector('.tutorial-content');
const tutorial3 = document.querySelectorAll('.tutorial-step');
const tutorial4 = document.querySelector('.tutorial-video');
const tutorial5 = document.querySelector('.tutorial-content2');


function applyDarkTheme() {
    body.classList.add('body-osc');
    navbar.classList.add('navbar-osc');
    footer.classList.add('footer-osc');
    navlinks.classList.add('nav-links-osc');
    tutorial1.classList.add('tutorial-intro-osc');
    tutorial2.classList.add('tutorial-content-osc');
    tutorial4.classList.add('tutorial-video-osc');
    tutorial5.classList.add('tutorial-content2-osc');
    tutorial3.forEach(step => step.classList.add('tutorial-step-osc'));
    buttonMode.innerHTML = "☀️";
    localStorage.setItem('theme', 'dark');
}

function applyLightTheme() {
    body.classList.add('body');
    navbar.classList.add('navbar');
    footer.classList.add('footer');
    navlinks.classList.add('nav-links');
    tutorial1.classList.add('tutorial-intro');
    tutorial2.classList.add('tutorial-content');
    tutorial4.classList.add('tutorial-video');
    tutorial5.classList.add('tutorial-content2');

    tutorial3.forEach(step => step.classList.add('tutorial-step'));
    buttonMode.innerHTML = "🌙";
    localStorage.setItem('theme', 'light');
}

function toggleTheme() {
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.remove('body-osc');
        navbar.classList.remove('navbar-osc');
        footer.classList.remove('footer-osc');
        navlinks.classList.remove('nav-links-osc');
        tutorial1.classList.remove('tutorial-intro-osc');
        tutorial2.classList.remove('tutorial-content-osc');
        tutorial4.classList.remove('tutorial-video-osc');
        tutorial5.classList.remove('tutorial-content2-osc');

        tutorial3.forEach(step => step.classList.remove('tutorial-step-osc'));
        applyLightTheme();
    } else {
        body.classList.remove('body');
        navbar.classList.remove('navbar');
        footer.classList.remove('footer');
        navlinks.classList.remove('nav-links');
        tutorial1.classList.remove('tutorial-intro');
        tutorial2.classList.remove('tutorial-content');
        tutorial4.classList.remove('tutorial-video');
        tutorial5.classList.remove('tutorial-content2');
        tutorial3.forEach(step => step.classList.remove('tutorial-step'));
        applyDarkTheme();
    }
}

if (localStorage.getItem('theme') === 'dark') {
    applyDarkTheme();
} else {
    applyLightTheme();
}

buttonMode.addEventListener('click', toggleTheme);
buttonModee.addEventListener('click', toggleTheme);

const menuIcon = document.getElementById('menuIcon');
const navLinks = document.querySelector('.nav-links');

menuIcon.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});
