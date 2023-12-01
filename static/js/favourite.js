'use strict';

window.addEventListener('DOMContentLoaded', () => {

    const btn = document.querySelector('.favourite-toggle');
    const star = document.querySelector('.fa-star');

    btn.addEventListener('click', () => {
        if (star.classList.contains('fa-solid')) {
            star.classList.add('fa-regular')
            star.classList.remove('fa-solid')
        } else {
            star.classList.add('fa-solid')
            star.classList.remove('fa-regular')
        }
    });

});
