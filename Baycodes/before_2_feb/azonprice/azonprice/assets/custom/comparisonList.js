function getCheckedBoxes(chkboxName) {
  var checkboxes = document.getElementsByName(chkboxName);
  var checkboxesChecked = "";
  var keyword = "";
  // loop over them all
  for (var i=0; i<checkboxes.length; i++) {
	 // And stick the checked ones onto an array...
	 if (checkboxes[i].checked) {
		keyword = $(checkboxes[i]).val();
		keyword = keyword.replace(/\s+/g, "+");
		checkboxesChecked += keyword+ ";";
	 }
  }
  // Return the array if it is non-empty, or null
  return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}
$("#content ol").hideMaxListItems({ "max":4, "speed":500, "moreText":"See MORE ([COUNT])" });
$("#compare").click(function(){
	var keyword = $( "#keyword" ).val();
	var checkedBoxes = getCheckedBoxes("comparisionUrl");
	if(checkedBoxes==null ) {
		checkedBoxes = "Nothing";
	}
	$.ajax({url: "../Controllers/analyseActionController.php",type: "POST", data:"keywords="+encodeURIComponent(keyword)+"&ComparisonUrls="+encodeURIComponent(checkedBoxes), beforeSend:function() {$( "#comapareDiv" ).html(""); },success: function(response) {$( "#comapareDiv" ).html(response);
	if($("#loading").text()!="") {
		// $("#loading").appendTo("#comapareDivLoad");
	}
	} });
	
});