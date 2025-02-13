const buttonMode = document.getElementById('Mode');
const buttonModee = document.getElementById('Modee');
const body = document.querySelector('body');
const navbar = document.querySelector('.navbar');
const navlinks = document.querySelector('.nav-links');
const footer = document.querySelector('.footer');
const section = document.querySelector('.rules');
const sectionn = document.querySelector('.intro');
const rule = document.querySelectorAll('.rule')



if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('body-osc');
    navbar.classList.add('navbar-osc');
    footer.classList.add('footer-osc');
    navlinks.classList.add('nav-links-osc');
    section.classList.add('rules-osc')
    sectionn.classList.add('intro-osc')
    rule.forEach(rule => rule.classList.add('rule-osc'));
    
    buttonMode.innerHTML = "☀️";
} else {
    body.classList.add('body');
    navbar.classList.add('navbar');
    footer.classList.add('footer');
    navlinks.classList.add('nav-links');
    section.classList.add('rules')
    sectionn.classList.add('intro')
    rule.forEach(rule => rule.classList.add('rule'));
    buttonMode.innerHTML = "🌙";
}

buttonMode.addEventListener('click', () => {
    if (body.classList.contains('body-osc')) {
        body.classList.remove('body-osc');
        navbar.classList.remove('navbar-osc');
        navlinks.classList.remove('nav-links-osc');
        footer.classList.remove('footer-osc');
        section.classList.remove('rules-osc')
        sectionn.classList.remove('intro-osc')
        rule.forEach(rule => {
            rule.classList.remove('rule-osc');
            rule.classList.add('rule');
        });

        buttonMode.innerHTML = "🌙"; 

        body.classList.add('body');
        navbar.classList.add('navbar');
        footer.classList.add('footer');
        navlinks.classList.add('nav-links');
        section.classList.add('rules')
        sectionn.classList.add('intro')

        
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('body');
        navbar.classList.remove('navbar');
        footer.classList.remove('footer');
        navlinks.classList.remove('nav-links');
        section.classList.remove('rules')
        sectionn.classList.remove('intro')
        rule.forEach(rule => {
            rule.classList.remove('rule');
            rule.classList.add('rule-osc');
        });

        body.classList.add('body-osc');
        navbar.classList.add('navbar-osc');
        footer.classList.add('footer-osc');
        navlinks.classList.add('nav-links-osc');
        section.classList.add('rules-osc')
        sectionn.classList.add('intro-osc')
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
        section.classList.remove('rules-osc')
        sectionn.classList.remove('intro-osc')
        buttonMode.innerHTML = "🌙"; 

        body.classList.add('body');
        navbar.classList.add('navbar');
        footer.classList.add('footer');
        navlinks.classList.add('nav-links');
        section.classList.add('rules')
        sectionn.classList.add('intro')
        rule.forEach(rule => {
            rule.classList.remove('rule-osc');
            rule.classList.add('rule');
        });
        
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('body');
        navbar.classList.remove('navbar');
        footer.classList.remove('footer');
        navlinks.classList.remove('nav-links');
        section.classList.remove('rules')
        rule.forEach(rule => {
            rule.classList.remove('rule');
            rule.classList.add('rule-osc');
        });

        body.classList.add('body-osc');
        navbar.classList.add('navbar-osc');
        footer.classList.add('footer-osc');
        navlinks.classList.add('nav-links-osc');
        section.classList.add('rules-osc')
        sectionn.classList.add('intro-osc')
        
        buttonMode.innerHTML = "☀️";

        localStorage.setItem('theme', 'dark');
    }
});







const menuIcon = document.getElementById('menuIcon');
const navLinks = document.querySelector('.nav-links');

menuIcon.addEventListener('click', () => {
    navLinks.classList.toggle('active'); 
});
