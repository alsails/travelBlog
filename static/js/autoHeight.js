function adjustModalHeight() {
    var modal = document.querySelector('.modal__container');
    var modal__container_signup = document.querySelector('.container');

    // Устанавливаем высоту модального окна равной высоте контейнера
    modal.style.height = modal__container_signup.offsetHeight + 'px';
}

// Вызываем функцию при загрузке страницы и при изменении размеров окна
window.addEventListener('load', adjustModalHeight);
window.addEventListener('resize', adjustModalHeight);
