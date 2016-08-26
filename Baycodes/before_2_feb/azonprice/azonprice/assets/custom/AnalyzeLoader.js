var tableData = '';
var barsData = '';
var donutsData = '';
var table2Tab3 = '';
$(document).ready(function(){
var keyword = $( "#keyword" ).val();
var checkedBoxes = getCheckedBoxes("comparisionUrl");
if(checkedBoxes==null ) {
	checkedBoxes = "Nothing";
}
function drawBars(data) {
	var visualization = new google.visualization.arrayToDataTable(data);

	var options = {
		  title: 'Page Shares Per Network',
	      'width':($('.container').width()-200),
	      'height':500,
		  bar: { groupWidth: '50%' },
		  chartArea: { width:"50%", left:100 },
		  isStacked: true,
		};


	var chart = new google.visualization.ColumnChart(document.getElementById('barsChart'));

	chart.draw(visualization, options);
}
function drawChart(data) {
	var data = google.visualization.arrayToDataTable(data);

	var options = {
	  title: 'Total Media Shares Summary',
	  pieHole: 0.4,
	  'width':($('.container').width()-200),
	   'height':500
	};

	var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
	chart.draw(data, options);
}
$('#2ndTab').on('click', function (e) {
	setTimeout(function(){
		if(barsData != '') {
			var arrayForGviz = eval("(" + barsData + ")");
			drawBars(arrayForGviz);
			$('#bar2').width('35%'); 
		}if(donutsData != '') {
			var arrayForGviz = eval("(" + donutsData + ")");
			drawChart(arrayForGviz);
			$('#bar2').width('75%'); 
		}if(tableData != '') {
			$('#tableResults').html( tableData );
			$('#bar2').width('100%'); 
		}
	}, 1000);
	});
	$('#3ndTab').on('click', function (e) {
	setTimeout(function(){
		if(table2Tab3 != '') {
			$('#secondTable').html( table2Tab3 );
			$('#bar3').width('75%'); 
		}
	}, 1000);
	});
// $.ajax({url: "../Controllers/analyzeTab2DonutsActionController.php",type: "POST",dataType: 'json', data:"keywords="+encodeURIComponent(keyword)+"&ComparisonUrls="+encodeURIComponent(checkedBoxes), beforeSend:function() {$( "#donutchart" ).html("");$( "#tab2Content" ).html(""); $( "#tab2ContentLoad" ).html("Fetching data, just wait...");},success: function(response) {//$( "#tab2ContentLoad" ).html("");//$( "#tab2Content" ).html(response);
	// donutsData = response;
	 // var arrayForGviz = eval("(" + donutsData['donuts'] + ")");
	// drawChart(arrayForGviz);
	// $('#bar2').width('50%'); 
// } });


$.ajax({url: "../Controllers/analyzeTab2BarsActionController.php",type: "POST",dataType: 'json', data:"keywords="+encodeURIComponent(keyword)+"&ComparisonUrls="+encodeURIComponent(checkedBoxes), beforeSend:function() {$( "#barsChart" ).html("");$( "#tab2Content" ).html(""); $( "#tab2ContentLoad" ).html("Fetching data, just wait...");},success: function(response) {$( "#tab2ContentLoad" ).html("");//$( "#tab2Content" ).html(response);
	barsData = response['bars'];
	// $('#barsChart').height(500);
	var arrayForGviz = eval("(" + barsData + ")");
	drawBars(arrayForGviz);
	$('#bar2').width('35%'); 
	donutsData = response['donuts'];
	var arrayForGviz2 = eval("(" + donutsData + ")");
	drawChart(arrayForGviz2);
	$('#bar2').width('75%');
	tableData = response['table'];
	// $('#tableResults').height(500);
	$('#tableResults').html( tableData );
	$('#bar2').width('100%'); 
} });
$.ajax({url: "../Controllers/analyzeTab3ActionController.php",type: "POST",dataType: 'json', data:"keywords="+encodeURIComponent(keyword)+"&ComparisonUrls="+encodeURIComponent(checkedBoxes), beforeSend:function() {},success: function(response) {$( "#tab3ContentLoad" ).html("");//$( "#tab3ContentLoad" ).html("");$( "#tab3Content" ).html(response);
	table2Tab3 = response['table2'];
	$('#secondTable').html( table2Tab3 );
	$('#bar3').width('75%'); 
} });

})


