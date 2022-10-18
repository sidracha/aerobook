var books = {

	limit: 5000,
	offset: 0,

	escape_html: function(unsafe) {

        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    },

	create_notebook_element: function (notebook_id, name) {

		const notebook_anchor = $("<a " + "href=" + notebook_id + ">" + name + "</a>");
		console.log(notebook_anchor)
		//notebook_anchor.attr("href", notebook_id);
		//notebook_anchor.attr("text", name);
		return notebook_anchor

		
	},


	get_and_display_notebooks: function () {
		$.ajax({
			url: "/notebooks?limit=" + books.limit + "&offset=" + books.offset,
			method: "GET"
		}).done(function (resp) {
			for (let i=0; i < resp.notebooks.length; i++) {
				notebook_anchor = books.create_notebook_element(resp.notebooks[i].notebook_id, resp.notebooks[i].name)
				notebook_anchor.prependTo($("#notebooks-div"))

			}
		})
	},


	handle_logout_button_click: function () {
		$("#logout-button")[0].onclick = function (e) {
			window.location.href = ("/logout");
		}
	},

	


}