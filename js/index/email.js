function validateEmail() {
    var re = new RegExp("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$")
    return ($("#email").val().match(re));
}

$(document).ready(function () {
    $('#email_submit').click(function (event) {
        event.preventDefault();
        if (validateEmail()) {
            $('#email_form').submit();
        } else {
		    $('#error_message').html("Please enter a valid email");
            $('#email').addClass("error"); 
        }
    });
});
