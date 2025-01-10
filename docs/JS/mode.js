const buttonMode = document.getElementById('Mode');
const body = document.querySelector('body');
const navbar = document.querySelector('.navbar');
const navlinks = document.querySelector('.nav-links');
const footer = document.querySelector('.footer');

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
    }
});



const buttonModee = document.getElementById('Modee');


buttonModee.addEventListener('click', () => {
    if (body.classList.contains('body-osc')) {
        body.classList.remove('body-osc');
        navbar.classList.remove('navbar-osc');
        navlinks.classList.remove('nav-links-osc');
        footer.classList.remove('footer-osc');
        buttonModee.innerHTML = "🌙"; 

        body.classList.add('body');
        navbar.classList.add('navbar');
        footer.classList.add('footer');
        navlinks.classList.add('nav-links');
    } else {
        body.classList.remove('body');
        navbar.classList.remove('navbar');
        footer.classList.remove('footer');
        navlinks.classList.remove('nav-links');

        body.classList.add('body-osc');
        navbar.classList.add('navbar-osc');
        footer.classList.add('footer-osc');
        navlinks.classList.add('nav-links-osc');
        buttonModee.innerHTML = "☀️";
    }
});
