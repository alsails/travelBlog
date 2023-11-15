$(document).ready(function () {
    $("#signinForm").submit(function (e) {
        e.preventDefault();  // Предотвратить отправку формы
        var formData = $(this).serialize();
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();  // Получить CSRF токен из формы
        formData += '&csrfmiddlewaretoken=' + csrfToken;  // Добавить CSRF токен к данным
        $.ajax({
            type: "POST",
            url: "/signin/",
            data: formData,
            success: function (data) {
                if (data.status === 'success') {
                    closeModal(); // Закрыть модальное окно
                    location.reload(); // Обновить страницу
                } else if (data.status === 'error') {
                    // Вывести сообщение об ошибке в модальном окне
                    $("#error-container").html('<p class="form__error">' + data.message + '</p>');
                }
            },
            error: function () {
                // Обработка ошибок входа
                console.error('Error during login request');
            }
        });
    });
});