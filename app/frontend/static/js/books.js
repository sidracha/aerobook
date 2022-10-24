var books = {

	max_notebooks: 10,
	current_notebook_count: 0,

	escape_html: function(unsafe) {

        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    },

	create_notebook_element: function (notebook_id, name) {
		const notebook_anchor_div = $("<div>", {
			class: "notebook-div"
		})
		const notebook_anchor = $("<a>", {
			href: notebook_id,
			class: "notebook-anchor"
		});
		notebook_anchor.html(name)
		const delete_notebook_button = $("<button>", {
			class: "delete-notebook-button",
			"data-id": notebook_id,
			"name": name
		})
		delete_notebook_button.html("x")
		notebook_anchor.appendTo(notebook_anchor_div)
		delete_notebook_button.appendTo(notebook_anchor_div)
		//notebook_anchor.attr("href", notebook_id);
		//notebook_anchor.attr("text", name);
		return notebook_anchor_div
	},
		

	handle_logout_button_click: function () {
		$("#logout-button")[0].onclick = function (e) {
			window.location.href = ("/logout");
		}

	},

	on_initial: function () {
		books.get_and_display_notebooks()
		$.ajax({
			url: "/user",
			method: "GET"
		}).done(function (resp) {
			const email = resp.email
			const profile_pic_link = resp.profile_pic
			$("#email-p").html(email)
			$("#profile-pic").attr("src", profile_pic_link)
		})

	},


	get_and_display_notebooks: function () {
		$.ajax({
			url: "/notebooks?limit=" + books.max_notebooks + "&offset=0",
			method: "GET"
		}).done(function (resp) {
			for (let i=0; i < resp.notebooks.length; i++) {
				books.current_notebook_count += 1;
				notebook_anchor_div = books.create_notebook_element(resp.notebooks[i].notebook_id, resp.notebooks[i].name)
				notebook_anchor_div.prependTo($("#notebooks-div"))
			}
		})
	},


	handle_logout_button_click: function () {
		$("#logout-button")[0].onclick = function (e) {
			window.location.href = ("/logout");
		}
	},

	handle_delete_notebook_button_click: function () {
		$("#notebooks-div")[0].onclick = function (e) {
			target = $(e.target)
			if (target.hasClass("delete-notebook-button")) {
				const name = e.target.getAttribute("name")
				const notebook_id = e.target.getAttribute("data-id")
				if (confirm("Are you sure you want to delete notebook: " + name + "?")) {
					$.ajax({
						url: "/notebook/" + notebook_id,
						method: "DELETE"
					}).done(function (resp) {
						$(e.target).closest(".notebook-div").remove();
					})
				}
			}
			
			
		}
	},

	handle_new_notebook_button_click: function () {
		$("#new-notebook-button")[0].onclick = function () {
			if (books.current_notebook_count === books.max_notebooks) {
				alert("You have reached the max number of notebooks!")
				return;
			}
			let name = prompt("Enter Notebook Name")
			name = name.trim()
			if (name === "") {
				return;
			}
			$.ajax({
				url: "/notebook/" + name,
				method: "POST"
			}).done(function (resp) {
				const notebook_anchor_div = books.create_notebook_element(resp.notebook_id, name)
				notebook_anchor_div.prependTo($("#notebooks-div"));
				books.current_notebook_count += 1;
				console.log(books.current_notebook_count)
			})
		}
	}

}	
	
