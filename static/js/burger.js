'use strict';

window.addEventListener('DOMContentLoaded', () => {

    const burgerBtn = document.querySelector('#burger');
    const navPagesMobile = document.querySelector('.nav__pages-mobile');

    burgerBtn.addEventListener('click', () => {
        burgerBtn.classList.toggle('active');
        if (burgerBtn.classList.contains('active')) {
            navPagesMobile.classList.add('active')
        } else {
            navPagesMobile.classList.remove('active')
        }
    });

    document.addEventListener('click', (event) => {
        if (!navPagesMobile.contains(event.target) && !burgerBtn.contains(event.target)) {
            burgerBtn.classList.remove('active');
            navPagesMobile.classList.remove('active');
        }
    });

});