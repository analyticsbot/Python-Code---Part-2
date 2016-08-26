var tableData = '';
var barsData = '';
var donutsData = '';
var table2Tab3 = '';
$(document).ready(function(){
Progressbar = $('#bar3');
Progressbar.defaults = {
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
Progressbar.progressbar({display_text: 'fill'});
	// $('#3ndTab').on('click', function (e) {
	// setTimeout(function(){
		// if(table2Tab3 != '') {
			// $('#secondTable').html( table2Tab3 );
			// $('#bar3').width('75%'); 
		// }
	// }, 1000);
	// });

$.ajax({url: "../Controllers/getSocialTab3Controller.php",type: "POST",dataType: 'json', data:"url="+url+"&ComparisonUrls="+comparisonUrls, beforeSend:function() {},success: function(response) {$( "#tab3ContentLoad" ).html("");//$( "#tab3ContentLoad" ).html("");$( "#tab3Content" ).html(response);
	table2Tab3 = response['table2'];
	$('#secondTable').html( table2Tab3 );
	$('#bar3').attr("aria-valuetransitiongoal", 40);
	Progressbar.progressbar({display_text: 'fill'});
} });
$.ajax({url: "../Controllers/getAuthorTab3Controller.php",type: "POST",dataType: 'json', data:"url="+url+"&ComparisonUrls="+comparisonUrls, beforeSend:function() {},success: function(response) {$( "#tab3ContentLoad" ).html("");//$( "#tab3ContentLoad" ).html("");$( "#tab3Content" ).html(response);
	table2Tab3 = response['table3'];
	$('#thirdTable').html( table2Tab3 );
	$('#bar3').attr("aria-valuetransitiongoal", 25);
	Progressbar.progressbar({display_text: 'fill'});
} });
$.ajax({url: "../Controllers/getCompetitiveTab3Controller.php",type: "POST",dataType: 'json', data:"url="+url+"&ComparisonUrls="+comparisonUrls+"&keywords="+keywords, beforeSend:function() {},success: function(response) {$( "#tab3ContentLoad" ).html("");//$( "#tab3ContentLoad" ).html("");$( "#tab3Content" ).html(response);
	table2Tab3 = response['table1'];
	$('#firstTable').html( table2Tab3 );
	$('#bar3').attr("aria-valuetransitiongoal", 100);
	Progressbar.progressbar({display_text: 'fill'});
} });
$.ajax({url: "../Controllers/getSuggestTab3Controller.php",type: "POST",dataType: 'json', data:"url="+url+"&ComparisonUrls="+comparisonUrls+"&keywords="+keywords, beforeSend:function() {},success: function(response) {$( "#tab3ContentLoad" ).html("");//$( "#tab3ContentLoad" ).html("");$( "#tab3Content" ).html(response);
	table2Tab3 = response['table4'];
	$('#fourthTable').html( table2Tab3 );
	$('#bar3').attr("aria-valuetransitiongoal", 75);
	Progressbar.progressbar({display_text: 'fill'});
} });
$.ajax({url: "../Controllers/getBeatableTab3Controller.php",type: "POST",dataType: 'json', data:"url="+url+"&ComparisonUrls="+comparisonUrls+"&keywords="+keywords, beforeSend:function() {},success: function(response) {$( "#tab3ContentLoad" ).html("");//$( "#tab3ContentLoad" ).html("");$( "#tab3Content" ).html(response);
	table2Tab3 = response['table5'];
	$('#fifthTable').html( table2Tab3 );
	$('#bar3').attr("aria-valuetransitiongoal", 60);
	Progressbar.progressbar({display_text: 'fill'});
} });
$.ajax({url: "../Controllers/getOpportunitiesTab3Controller.php",type: "POST",dataType: 'json', data:"url="+url+"&ComparisonUrls="+comparisonUrls+"&keywords="+keywords, beforeSend:function() {},success: function(response) {$( "#tab3ContentLoad" ).html("");//$( "#tab3ContentLoad" ).html("");$( "#tab3Content" ).html(response);
	table2Tab3 = response['table6'];
	$('#sixTable').html( table2Tab3 );
	$('#bar3').attr("aria-valuetransitiongoal", 80);
	Progressbar.progressbar({display_text: 'fill'});
} });
})


