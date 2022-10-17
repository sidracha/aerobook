var home = {

	handle_google_login_click: function () {
		$("#google-login-button")[0].onclick = function (e) {
			window.location.href = ("/google-login");
		}
	}

}