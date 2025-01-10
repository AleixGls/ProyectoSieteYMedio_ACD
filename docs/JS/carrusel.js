const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');
const carousel = document.querySelector('.carousel');
let currentIndex = 0;

function showNextImage() {
    if (currentIndex < carousel.children.length - 1) {
        currentIndex++;
    } else {
        currentIndex = 0; 
    }
    updateCarouselPosition();
}

function showPrevImage() {
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        currentIndex = carousel.children.length - 1; 
    }
    updateCarouselPosition();
}

function updateCarouselPosition() {
    const offset = -currentIndex * 100; 
    carousel.style.transform = `translateX(${offset}%)`;
}

nextButton.addEventListener('click', showNextImage);
prevButton.addEventListener('click', showPrevImage);

setInterval(showNextImage, 3000);
