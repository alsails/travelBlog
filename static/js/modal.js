function openModal() {
    document.getElementById('signinModal').classList.add('modal_opened');
}

function clearFormInputs() {
    $('#signinModal input').val('');
    $('#signupModal input').val('');
    $('.form__error').html('');
}

function closeModal() {
    document.getElementById('signinModal').classList.remove('modal_opened');
    document.getElementById('signupModal').classList.remove('modal_opened');
    clearFormInputs()
}

function closeFirstModal() {
    document.getElementById('signinModal').classList.remove('modal_opened');
    document.getElementById('signupModal').classList.add('modal_opened');
}

// Закрытие модального окна при клике вне его области
window.onclick = function(event) {
    var modal = document.getElementById('myModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}