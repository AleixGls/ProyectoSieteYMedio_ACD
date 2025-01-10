const buttonMode = document.getElementById('Mode');
const buttonModee = document.getElementById('Modee');
const body = document.querySelector('body');
const navbar = document.querySelector('.navbar');
const navlinks = document.querySelector('.nav-links');
const footer = document.querySelector('.footer');

if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('body-osc');
    navbar.classList.add('navbar-osc');
    footer.classList.add('footer-osc');
    navlinks.classList.add('nav-links-osc');
    buttonMode.innerHTML = "☀️";
} else {
    body.classList.add('body');
    navbar.classList.add('navbar');
    footer.classList.add('footer');
    navlinks.classList.add('nav-links');
    buttonMode.innerHTML = "🌙";
}

buttonMode.addEventListener('click', () => {
    if (body.classList.contains('body-osc')) {
        body.classList.remove('body-osc');
        navbar.classList.remove('navbar-osc');
        navlinks.classList.remove('nav-links-osc');
        footer.classList.remove('footer-osc');
        buttonMode.innerHTML = "🌙"; 

        body.classList.add('body');
        navbar.classList.add('navbar');
        footer.classList.add('footer');
        navlinks.classList.add('nav-links');
        
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('body');
        navbar.classList.remove('navbar');
        footer.classList.remove('footer');
        navlinks.classList.remove('nav-links');

        body.classList.add('body-osc');
        navbar.classList.add('navbar-osc');
        footer.classList.add('footer-osc');
        navlinks.classList.add('nav-links-osc');
        buttonMode.innerHTML = "☀️";

        localStorage.setItem('theme', 'dark');
    }
});

buttonModee.addEventListener('click', () => {
    if (body.classList.contains('body-osc')) {
        body.classList.remove('body-osc');
        navbar.classList.remove('navbar-osc');
        navlinks.classList.remove('nav-links-osc');
        footer.classList.remove('footer-osc');
        buttonMode.innerHTML = "🌙"; 

        body.classList.add('body');
        navbar.classList.add('navbar');
        footer.classList.add('footer');
        navlinks.classList.add('nav-links');
        
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('body');
        navbar.classList.remove('navbar');
        footer.classList.remove('footer');
        navlinks.classList.remove('nav-links');

        body.classList.add('body-osc');
        navbar.classList.add('navbar-osc');
        footer.classList.add('footer-osc');
        navlinks.classList.add('nav-links-osc');
        buttonMode.innerHTML = "☀️";

        localStorage.setItem('theme', 'dark');
    }
});







const menuIcon = document.getElementById('menuIcon');
const navLinks = document.querySelector('.nav-links');

menuIcon.addEventListener('click', () => {
    navLinks.classList.toggle('active'); 
});
