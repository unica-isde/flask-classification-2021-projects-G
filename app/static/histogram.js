/**
 * Simple long polling client based on JQuery
 * https://github.com/sigilioso/long_polling_example/blob/master/static/poll.js
 */

/**
 * Request an update to the server and once it has answered, then update
 * the content and request again.
 * The server is supposed to response when a change has been made on data.
 */
function update(jobId) {
    $.ajax({
        url: `/histogram/${jobId}`,
        success: function (data) {
            console.log(data)
            switch (data['task_status']) {
                case "finished":
                    $('#spinner').hide();
                    $('#waitText').text("");
					plot(data['data']);
                    break;
                case "started":
                    $('#waitText').text("Job started...");
                    $('#spinner').show();
                    setTimeout(function () {
                        update(jobId);
                    }, 1000);
                    break;
                case "queued":
                    $('#waitText').text("Please wait ...");
                    $('#spinner').show();
                    setTimeout(function () {
                        update(jobId);
                    }, 1000);
                    break;
            }

        }
    });
}


$(document).ready(function () {
    var scripts = document.getElementById('histogram');
    var jobID = scripts.getAttribute('jobid');
    update(jobID);
});


function plot(results){
	var xValues = [...Array(256).keys()];

	context = document.getElementById("histogramOutput").getContext("2d");

	new Chart(context, {
			type: "line",
			data: {
				labels: xValues,
				datasets: [{
					data: results[0],
					borderColor: "red",
					fill: false
				},{
					data: results[1],
					borderColor: "green",
					fill: false
				},{
					data: results[2],
					borderColor: "blue",
					fill: false
				}]
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						},
						scaleLabel: {
							display: true,
							labelString: 'Number of pixels'
						},
					}],
					xAxes: [{
						scaleLabel:{
							display: true,
							labelString: 'Intensity'
						}
					}]
				},
			legend: false
		}
	}); 
}


