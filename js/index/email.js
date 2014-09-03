function validateEmail(email) {
    var re = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return re.test(email);
}

$(document).ready(function () {
    $('#email_submit').click(function (event) {
        event.preventDefault();
        $('#error_message').html("");
        $('#email').removeClass("error");
		var email = $("#email").val();
        if (validateEmail(email)) {
            data = {};
            data['email'] = email;
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
                    $('.info_text').css({
                        display: 'none'
                    });
                    $('.error_message').css({
                        display: 'block'
                    });
                    $('.error_message').html("You've already registered this email!");
                    $('#email').addClass("error");
				}
			});
        } else {
            $('.info_text').css({
                display: 'none'
            });
            $('.error_message').css({
                display: 'block'
            });
		    $('.error_message').html("Please enter a valid email");
            $('#email').addClass("error"); 
        }
    });

    $('#email').keypress(function() {
        $('.info_text').css({
            display: 'block'
        });
        $('.error_message').css({
            display: 'none'
        });
        $('#error_message').html("");
        $('#email').removeClass("error");
    }); 
});
