'use strict';

window.addEventListener('DOMContentLoaded', () => {

    const btn = document.querySelector('.modal-btn');
    const modal = document.querySelector('.modal-message');

    btn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

});
