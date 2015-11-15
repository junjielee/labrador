var Login = function () {

	var handleLogin = function() {


    $('.login-form input').keypress(function (e) {
        if (e.which == 13) {
           $('.login-form').submit(); //form validation success, call ajax form submit
        }
    });
	}

    return {
        //main function to initiate the module
        init: function () {
        	
            handleLogin();
        }

    };

}();

jQuery(document).ready(function() {
        Login.init();
      });