var tableData = '';
var competitorTableData = '';
var barsData = '';
var donutsData = '';
var table2Tab3 = '';
Progressbar2 = $('#bar2');
$(document).ready(function(){

Progressbar2.defaults = {
    transition_delay: 300,
    refresh_speed: 50,
    display_text: 'center',
    use_percentage: true,
    percent_format: function(percent) { return percent + '%'; },
    amount_format: function(amount_part, amount_total) { return amount_part + ' / ' + amount_total; },
    update: $.noop,
    done: $.noop,
    fail: $.noop
};
$('#bar2').attr("aria-valuetransitiongoal", 25);
Progressbar2.progressbar({display_text: 'fill'});
function drawBars(data) {
	var visualization = new google.visualization.arrayToDataTable(data);

	var options = {
		  title: '',
	      'width':($('.tabs').width()-100),
	      'height':500,
		  bar: { groupWidth: '75%' },
		  chartArea: { width:"60%", left:0 },
		  isStacked: true,
		  backgroundColor: "transparent"
		};


	var chart = new google.visualization.ColumnChart(document.getElementById('barsChart'));

	chart.draw(visualization, options);
}
function drawChart(data) {
	var data = google.visualization.arrayToDataTable(data);

	var options = {
	  title: '',
	  pieHole: 0.4,
	  'width':($('.tabs').width()-100),
	  'height':500,
      backgroundColor: "transparent"
	};

	var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
	chart.draw(data, options);
}



$.ajax({url: "../Controllers/getSocialTab2Controller.php",type: "POST",dataType: 'json', data:"url="+encodeURIComponent(url), beforeSend:function() {$( "#barsChart" ).html("");$( "#tab2Content" ).html("");},success: function(response) {
	barsData = response['bars'];
	var arrayForGviz = eval("(" + barsData + ")");
	drawBars(arrayForGviz);
	donutsData = response['donuts'];
	var arrayForGviz2 = eval("(" + donutsData + ")");
	drawChart(arrayForGviz2);
	tableData = response['table'];
	$('#tableResults').html( tableData );
	$('#bar2').attr("aria-valuetransitiongoal", 65);
	Progressbar2.progressbar({display_text: 'fill'});
} });
$.ajax({url: "../Controllers/getSocialTab2CompetitorDataController.php",type: "POST",dataType: 'json', data:"ComparisonUrls="+comparisonUrls, beforeSend:function() {$( "#barsChart" ).html("");$( "#tab2Content" ).html("");},success: function(response) {
	competitorTableData = response['table'];
	$('#competitorTableResults').html( competitorTableData );
	$('#bar2').attr("aria-valuetransitiongoal", 100);
	Progressbar2.progressbar({display_text: 'fill'});
} });

})


