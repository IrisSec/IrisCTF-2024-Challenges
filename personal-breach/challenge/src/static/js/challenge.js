$("#submit").on("click", function() {

	let answers = {
		q1: $("#form").find("input[name='q1']").val(),
		q2: $("#form").find("input[name='q2']").val(),
		q3: $("#form").find("input[name='q3']").val(),
	};

	$("#q1-img").attr("src", "/static/svg/loading.svg");
	$("#q2-img").attr("src", "/static/svg/loading.svg");
	$("#q3-img").attr("src", "/static/svg/loading.svg");

	$.ajax({
		type: "POST",
		url: "/submit",
		contentType: "application/json",
		data: JSON.stringify(answers),
		statusCode: {
			200: function(response)
			{
				if (response.q1)  $("#q1-img").attr("src", "/static/png/check.png");
				else              $("#q1-img").attr("src", "/static/png/cross.png");

				if (response.q2)  $("#q2-img").attr("src", "/static/png/check.png");
				else              $("#q2-img").attr("src", "/static/png/cross.png");

				if (response.q3)  $("#q3-img").attr("src", "/static/png/check.png");
				else              $("#q3-img").attr("src", "/static/png/cross.png");

				$("#flag").text(response.flag);
			},
			400: function(response)
			{
				alert("You did something unexpected. Please try again or open a support ticket.");
			}
		}
	});
});
