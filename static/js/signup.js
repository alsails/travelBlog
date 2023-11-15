$(document).ready(function () {
    $("#signupForm").submit(function (e) {
        e.preventDefault();
        var formData = $(this).serialize();
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        formData += '&csrfmiddlewaretoken=' + csrfToken;

        $.ajax({
            type: "POST",
            url: "/signup/",
            data: formData,
            dataType: 'json',  // Указываем, что ожидаем JSON в ответе
            success: function (data) {
                if (data.status === 'success') {
                    closeModal();
                    location.reload();
                } else if (data.status === 'error') {
                    // Очищаем предыдущие ошибки
                     $(".error").html("");

                    // Обрабатываем ошибки регистрации и отображаем их в форме
                    for (var field in data.errors) {
                        $("#" + field + "_error").html(data.errors[field].join("<br>"));
                    }
                }
            },
            error: function () {
                console.error('Error during signup request');
            }
        });
    });
});
