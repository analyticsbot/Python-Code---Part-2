
$('#submit').click(function(){
    
    var lines = $( "#Competitor" ).val().split('\n');
    
    var pib = '';
    for(var i = 0;i < lines.length;i++){
        //code here using lines[i] which will give you each line
        lines[i] = lines[i].replace(/\s+/g, '');
         pib = pib + lines[i]+';';
        
    }
    var dataString = 'Competitor='+pib+'&Action=overview';
    if(pib!='' ) {
    
    $.ajax({
      type: "POST",
      url: "overview2Action.php",
      datatype: "html",
      data: dataString,
      beforeSend:     
        function() {    
            $( "#regNumLoad" ).html( "Fetching data, just wait..." );
            
                // var oTable = $("#example tbody").html("");
                // var oTable = $("#example").dataTable();
                // oTable.fnDestroy();
            
        },
      success: function(response) {
         $( "#regNumLoad" ).text( "" );
        $( "#regNum" ).html(response);
        // if(response=='success') {
             
            
            // var oTable = $("#example1").dataTable({
                // "bProcessing": true,
                // "bDestroy": true, 
                // "sAjaxSource": "ajax.txt",     
               // "sScrollX": "100%",
                // "sScrollXInner": "150%",
                // "sScrollY": "500px",
                // "bScrollCollapse": true,
                // "bPaginate": true
            // });
            // if ( $.browser.webkit ) {
            // setTimeout( function () {
                // oTable.fnAdjustColumnSizing();
            // }, 10 );
            // }
            // new FixedColumns( oTable, {
                        // "iLeftColumns": 2,
                    // } );
            
            
        // }
        },
      error: function() {
        var msg = "Sorry but there was an error; Try again ";
        $( "#regNum" ).html( msg );
        },
    complete: 
        function() {
            $( "#regNumLoad" ).html( "" );
        }
    });
    }
    else if(pib =='' ) {
        $( "#regNum" ).text('No Competitor Url');
    }

});
$('#organic').click(function(){
    
    var lines = $( "#Competitor" ).val().split('\n');
    
    var pib = '';
    for(var i = 0;i < lines.length;i++){
        //code here using lines[i] which will give you each line
        lines[i] = lines[i].replace(/\s+/g, '');
         pib = pib + lines[i]+';';
        
    }
    var dataString = 'Competitor='+pib+'&Action=organic';
    if(pib!='' ) {
    
    $.ajax({
      type: "POST",
      url: "organicAction.php",
      datatype: "html",
      data: dataString,
      beforeSend:     
        function() {    
            $( "#regNumLoad" ).html( "Fetching data, just wait..." );
            
                // var oTable = $("#example tbody").html("");
                var oTable = $("#example").dataTable();
                // oTable.fnDestroy();
            
        },
      success: function(response) {
         $( "#regNumLoad" ).text( "" );
        $( "#regNum" ).html("");
        if(response=='success') {
             
            
            var oTable = $("#example1").dataTable({
                "bProcessing": true,
                "bDestroy": true, 
                "sAjaxSource": "ajax.txt",     
               "sScrollX": "100%",
                "sScrollXInner": "200%",
                "sScrollY": "500px",
                "bScrollCollapse": true,
                "bPaginate": true
            });
            if ( $.browser.webkit ) {
            setTimeout( function () {
                oTable.fnAdjustColumnSizing();
            }, 10 );
            }
            //new FixedHeader( oTable, { "bottom": true, "left": true  } );
            new FixedColumns( oTable, {
                        "iLeftColumns": 1,
                    } );
            
            
        }
        },
      error: function() {
        var msg = "Sorry but there was an error; Try again ";
        $( "#regNum" ).html( msg );
        },
    complete: 
        function() {
            $( "#regNumLoad" ).html( "" );
        }
    });
    }
    else if(pib =='' ) {
        $( "#regNum" ).text('Insert some Domains');
    }

});
$('#adwords').click(function(){
    
    var lines = $( "#Competitor" ).val().split('\n');
    
    var pib = '';
    for(var i = 0;i < lines.length;i++){
        //code here using lines[i] which will give you each line
        lines[i] = lines[i].replace(/\s+/g, '');
         pib = pib + lines[i]+';';
        
    }
    var dataString = 'Competitor='+pib+'&Action=adwords';
    if(pib!='' ) {
    
    $.ajax({
      type: "POST",
      url: "adwordsAction.php",
      datatype: "html",
      data: dataString,
      beforeSend:     
        function() {    
            $( "#regNumLoad" ).html( "Fetching data, just wait..." );
            
                // var oTable = $("#example tbody").html("");
                var oTable = $("#example").dataTable();
                // oTable.fnDestroy();
            
        },
      success: function(response) {
         $( "#regNumLoad" ).text( "" );
        $( "#regNum" ).html("");
        if(response=='success') {
             
            
            var oTable = $("#example1").dataTable({
                "bProcessing": true,
                "bDestroy": true, 
                "sAjaxSource": "ajax.txt",     
                "sScrollX": "100%",
                "sScrollXInner": "250%",
                "sScrollY": "500px",
                "bScrollCollapse": true,
                "bPaginate": true
            });
            if ( $.browser.webkit ) {
            setTimeout( function () {
                oTable.fnAdjustColumnSizing();
            }, 10 );
            }
            //new FixedHeader( oTable, { "bottom": true, "left": true  } );
            new FixedColumns( oTable, {
                        "iLeftColumns": 1,
                    } );
            
            
        }
        },
      error: function() {
        var msg = "Sorry but there was an error; Try again ";
        $( "#regNum" ).html( msg );
        },
    complete: 
        function() {
            $( "#regNumLoad" ).html( "" );
        }
    });
    }
    else if(pib =='' ) {
        $( "#regNum" ).text('Insert some Domains');
    }

});
$('#keyword').click(function(){
    
    var pib = $( "#phrase" ).val();
        
    if(pib!='' ) {
    
     $.ajax({url: "parseRushPhraseApi.php",type: "POST",dataType: 'json', data:"Phrase="+encodeURIComponent(pib), beforeSend:function() {alertify.log("Fetching data, please be patient...", "", 3000);$( "#bestKeywordsTables" ).html( "" );$( "#leftBestKeywordsClicks" ).html( "Checking credit..." );},success: function(data) {
		$( "#bestKeywordsTables" ).html( data['bestKeywordsTables'] );
		$( "#leftBestKeywordsClicks" ).html( data['leftBestKeywordsClicks'] );
		if(data['leftBestKeywordsClicks']== 'You can perform <font color="red">0</font> more searches') {
			$( "#bestKeywordsButton" ).html( '<input type="button" class="btn btn-success" value="Find Best Keywords" disabled>' );
			alertify.error("You are out of credits", "", 3000);
		}
		alertify.success("Data loaded successfully.");
    },error: function() { var msg = "Sorry but an error has occurred, Try again.";alertify.error(msg);}
    })
	
    }
    else if(pib =='' ) {
        alertify.error("Try to enter a phrase first.");
    }

});
