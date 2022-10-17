var books = {

	handle_logout_button_click: function () {
		$("#logout-button")[0].onclick = function (e) {
			window.location.href = ("/logout");
		}
	},

	handle_new_notebook_button_click: function () {
		$("#new-notebook-button")[0].onclick = function (e) {
			$.ajax({
				url: "/notebook/mfs",
				method: "POST",
				statusCode: {
					500: function () {
						alert("Notebook Limit Exceeded");
					}
				},
				success: function (resp) {
					console.log(resp);
				}


			})
		}
	},

	handle_session_button_click: function () {
		$("#session-button")[0].onclick = function (e) {
			window.location.href = "/session";
		}
	},

	handle_count_button_click: function () {
		$("#count-button")[0].onclick = function (e) {
			$.ajax({
				url: "/test",
				method: "GET"
			}).done(function (resp) {
				console.log(resp)
			})
		}
	},

	handle_get_notebooks_button_click: function () {
		$("#get-notebooks-button")[0].onclick = function (e) {
			$.ajax({
				url: "/notebooks",
				method: "GET",
				success: function (resp) {
					for (let i=0; i < resp.notebooks.length; i++) {
						console.log(resp.notebooks[i])
					}
				}
			})
		}
	},

	handle_delete_button_click: function () {
		$("#delete-button")[0].onclick = function (e) {
			const notebook_id = $("#id-input")[0].value
			$.ajax({
				url: "/notebook/" + notebook_id,
				method: "DELETE",
				success: function (resp) {
					console.log(resp)
				}
			})
		}
	},
	
	handle_add_note_button_click: function () {
		$("#add-note-button")[0].onclick = function (e) {
			console.log("here")
			const notebook_id = $("#id-input")[0].value
			const body = $("#note-body")[0].value
			
			$.ajax({
				url: "/notebook/" + notebook_id + "/note",
				method: "POST",
				data: JSON.stringify({
					body: body
				}),
				success: function (resp){
					console.log(resp)
				}
			})
			
		}
	}

}