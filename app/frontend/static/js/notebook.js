var notebook = {

	limit: 2,
	offset: 0,
	current_page: 1,
	last_page: 0,
	count: 0,

	parse_notebook_id: function () {
		let url = window.location.href;
        let x = url.lastIndexOf('/');
        nbid = url.substring(x+1, url.length);
        return nbid;
	},

	escape_html: function(unsafe) {

        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    },

	get_note_count: function () {
		return $.ajax({
			url: "/notebook/" + notebook.parse_notebook_id() + "/count",
			method: "GET",

		})
	},

	on_initial: async function () {
		$.ajax({
			url: "/notebook/" + notebook.parse_notebook_id() + "/name",
			method: "GET"
		}).done(function (resp) {
			const name = resp.name
			console.log(name)
			$("#name").text(name)
		})
		$.ajax({
			url: "/user",
			method: "GET"
		}).done(function (resp) {
			$("#email-p").html(resp.email)
			$("#profile-pic").attr("src", resp.profile_pic)
		})
		let count = await this.get_note_count()
		count = count.count
		this.last_page = Math.ceil(count/this.limit)
		this.count = count
		if (count === 0) {
			this.last_page = 1
		}
		this.get_and_display_notes(this.limit, 0)
		notebook.modify_page_num(1)
	},

	get_and_display_notes: function (limit, offset) {
		$.ajax({
			url: "/notebook/" + notebook.parse_notebook_id() + "/notes?limit=" + limit + "&offset=" + offset,
			method: "GET", 
		}).done(function (resp) {
			console.log(resp)
			for (let i=0; i < resp.notes.length; i++) {
				const note_div = notebook.create_note_element(resp.notes[i].note_id, resp.notes[i].body);
				console.log(note_div);
				note_div.appendTo($("#all-notes-div")[0]);
			}
		})
	},

	add_note: function (body) {
		$.ajax({
			url: "/notebook/" + notebook.parse_notebook_id() + "/note",
			method: "POST",
			dataType: "json",
			data: JSON.stringify({body: body}),
			success: function (resp) {
				const note_id = resp.note_id;
				const body = resp.body;
				note_div = notebook.create_note_element(note_id, body)
				note_div.prependTo($("#all-notes-div")[0]);
				$("#note-field")[0].value = "";
				this.count += 1;
				last_page = Math.ceil(this.count/this.limit)
			}

		})
	},

	modify_page_num: function (num) {
		$("#current-page").text(num)
	},

	create_note_element: function (note_id, body) {
		const note_div = $("<div>", {
			class: "note-div"
		});
		const note_text_div = $("<div>", {
			class: "note-text-div"
		});
		note_text_div.append("<p>" + notebook.escape_html(body) + "</p>");

		const delete_button = $("<button>", {
			class: "delete-note-button",
			"data-id": note_id
		});
		delete_button.html("Delete");
		note_text_div.appendTo(note_div);
		delete_button.appendTo(note_div);
		return note_div
	},



	handle_new_note_button_click: function () {
		$("#new-note-button")[0].onclick = function (e) {
			notebook.new_note()
		}

	},
	
	handle_enter_click: function () {
		$(document).keypress(function (e) {
			const keycode = e.keyCode || e.which;
			if (keycode === 13 && !e.shiftKey) {
				notebook.new_note()
			}
		})
	},

	new_note: function () {
		const body = $("#note-field")[0].value
		if (body.trim().length === 0) {
			return;
		}
		$.ajax({
			url: "/notebook/" + notebook.parse_notebook_id() + "/note",
			method: "POST",
			data: JSON.stringify({body:body})
		}).done(function (resp) {
			notebook.go_to_page(1)
			$("#note-field")[0].value = ""
			this.last_page = Math.ceil(resp.count/notebook.limit)
		})
	},

	go_to_page: function (page) {
		notebook.current_page = page
		notebook.offset = notebook.limit * (page-1)
		$(".note-div").remove()
		notebook.get_and_display_notes(notebook.limit, notebook.offset)
		this.modify_page_num(notebook.current_page)
	},

	handle_next_page_button_click: function () {
		$("#next-page-button")[0].onclick = function (e) {
			console.log(notebook.current_page)
			console.log(notebook.last_page)
			if (notebook.current_page === notebook.last_page) {
				return;
			}

			notebook.go_to_page(notebook.current_page+1)
			notebook.modify_page_num(notebook.current_page)
		}
	},

	handle_previous_page_button_click: function () {
		$("#previous-page-button")[0].onclick = function (e) {
			if (notebook.current_page === 1) {
				return;
			}
			notebook.go_to_page(notebook.current_page-1)
		}
	},

	handle_delete_note_button_click: function () {
		$("#all-notes-div")[0].onclick = function (e) {
			const target = $(e.target);
			if (target.hasClass("delete-note-button")) {
				const note_id = e.target.getAttribute("data-id");
				$.ajax({
					url: "/notebook/" + notebook.parse_notebook_id() + "/note/" + note_id,
					method: "DELETE"
				}).done(function (resp) {
					$(e.target).closest(".note-div").remove();
					notebook.go_to_page(notebook.current_page);
				})
			}
		}
	},

	handle_back_to_notebooks_button_click: function () {
		$("#back-to-notebooks-button")[0].onclick = function (e) {
			window.location.href = "/display/notebooks"
		}
	},

	handle_logout_button_click: function () {
		$("#logout-button")[0].onclick = function (e) {
			window.location.href = "/logout"
		}
	}

}