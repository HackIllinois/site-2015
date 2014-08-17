function validateEmail() {
    var re = new RegExp("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$")
    return ($("#email").val().match(re));
}

$(document).ready(function () {
    $('#email_submit').click(function (event) {
        event.preventDefault();
        $('#error_message').html("");
        $('#email').removeClass("error");
        if (validateEmail()) {
            data = {};
            data['email'] = $("#email").val();
            $.post('/', data, function(data) {
                if(data === "success"){
                    $('#email_form').css({
                        display: 'none'
                    });
                    $('#thank_you').css({
                        display: 'block'
                    });
				}
                else if(data === "indatabase"){
                    $('#email_form').css({
                        display: 'none'
                    });
                    $('#thank_you').css({
                        display: 'block'
                    });
                    $('#thank_you').html("already in DataBase (change this js\index\email)");
				}
			});
        } else {
		    $('#error_message').html("Please enter a valid email");
            $('#email').addClass("error"); 
        }
    });

    $('#email').keypress(function() {
        $('#error_message').html("");
        $('#email').removeClass("error");
    });
    $('#email').change(function() {
        $('#error_message').html("");
        $('#email').removeClass("error");
    });
});
