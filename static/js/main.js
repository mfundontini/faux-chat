$('.form-section').on("click", "#create-chat", function(event) {
    event.preventDefault();
    var form = $(this).parent();
    var formData = form.serialize()
    var postUrl = "http://localhost:8000/chat/create";
    function handlePostSuccess(data, textStatus, jqXHR){
        document.querySelector(".message-section").insertAdjacentHTML('afterbegin', data.html);
        form[0].reset();

    };
    function handlePostErrors(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    };
    $.ajax({
        method: "POST",
        url: postUrl,
        data: formData,
        success: handlePostSuccess,
        error: handlePostErrors,
    });
});