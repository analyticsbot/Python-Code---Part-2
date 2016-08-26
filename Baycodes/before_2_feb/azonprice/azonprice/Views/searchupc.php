
<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=utf-8">
		
		
		<title>Dashboard Tab</title>
		<link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet" type="text/css" />
		<link rel="stylesheet" type="text/css" href="../assets/fancyBox/source/jquery.fancybox.css?v=2.1.5" media="screen" />
        <!-- include the core styles -->
		<link rel="stylesheet" href="../assets/alertify/alertify.core.css" />
		<!-- include a theme, can be included into the core instead of 2 separate files -->
		<link rel="stylesheet" href="../assets/alertify/alertify.default.css" />
		<link href="http://datatables.github.com/Plugins/integration/bootstrap/2/dataTables.bootstrap.css" rel="stylesheet" type="text/css"/>
		<style type="text/css">
			  @import "../assets/media/css/DT_bootstrap.css";
			  
				@import "../assets/tableTool/media/css/TableTools.css";
				table.table thead .sorting,
				table.table thead .sorting_asc,
				table.table thead .sorting_desc,
				table.table thead .sorting_asc_disabled,
				table.table thead .sorting_desc_disabled {
					cursor: pointer;
					*cursor: hand;
				}
				 
				table.table thead .sorting { background: url('../assets/media/images/sort_both.png') no-repeat center right; }
				table.table thead .sorting_asc { background: url('../assets/media/images/sort_asc.png') no-repeat center right; }
				table.table thead .sorting_desc { background: url('../assets/media/images/sort_desc.png') no-repeat center right; }
				 
				table.table thead .sorting_asc_disabled { background: url('../assets/media/images/sort_asc_disabled.png') no-repeat center right; }
				table.table thead .sorting_desc_disabled { background: url('../assets/media/images/sort_desc_disabled.png') no-repeat center right; }
				.odd {
				font-size:12px;
				height:10px;
				}
			.even {
				font-size:12px;
				height:10px;
				}
				
			
				table  {
				
					height:30px !important;
					table-layout: fixed; // ***********add this
					word-wrap:break-word; // ***********and this 
					-ms-word-break: break-all;
					-ms-word-wrap: break-all;
					-webkit-word-break: break-word;
					-webkit-word-wrap: break-word;
					word-break: break-word;
					word-wrap: break-word;
					-webkit-hyphens: auto;
					-moz-hyphens: auto;
					hyphens: auto; 
				}	
				.fancybox-custom .fancybox-skin {
					box-shadow: 0 0 50px #222;
				}
				.tooltip {
					overflow: auto !important;
					position: fixed;
				}
				.tooltip-inner {
					background-color : #D6D630 !important;
					color : #000033 ;
					width:400px !important;
					white-space:pre-wrap;
					max-width:none;
				}
                .row_selected {
					background-color:#FFF973  !important;
				}input {
					min-height:30px !important;
				}
		</style>
		<script src="http://code.jquery.com/jquery-1.8.2.js"></script>
    <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>
    <script src="http://heartcode-canvasloader.googlecode.com/files/heartcode-canvasloader-min-0.9.1.js"></script>
    <script src="../assets/media/js/jquery.dataTables.js"></script>
    <script src="../assets/media/js/DT_bootstrap.js"></script>
    <script src="../assets/media/js/ZeroClipboard.js"></script>
    <script src="..//assets/media/js/TableTools.js"></script>
    <script type="text/javascript" charset="utf-8" src="http://datatables.github.com/Plugins/integration/bootstrap/2/dataTables.bootstrap.js"></script>
    <script src="../assets/media/js/FixedColumns.js"></script>
    <script src="../assets/media/js/jquery.dataTables.columnFilter.js"></script>
    <script src="../assets/fancyBox/source/jquery.fancybox.js?v=2.1.5"></script>
    <script src="../assets/alertify/alertify.min.js"></script>
		
	</head>
	<body>
    <div class="navbar navbar-inverse">
        <div class="navbar-inner">
            <div class="container">
             
				<!-- .btn-navbar is used as the toggle for collapsed navbar content -->
				<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				</a>
				 
				<!-- Be sure to leave the brand out there if you want it shown -->
				<a class="brand" href="#">Amazon Tool</a>
				 
				<!-- Everything you want hidden at 940px or less, place within here -->
				<div class="nav-collapse collapse">
				<!-- .nav, .navbar-search, .navbar-form, etc -->
					<ul class="nav">		
						<li class="active">
							<a href="#">Search ASINS</a>
						</li>
					
									
					
						
					</ul>
					<ul class="nav pull-right">
						<li class="dropdown">
						  <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="icon-user icon-white"></i> Hello <?php echo $_SESSION['username']?> <b class="caret"></b></a>
						  <ul class="dropdown-menu">
							<li><a href="logout.php">Logout</a></li>
							</ul>
						</li>
					</ul>
				</div>
             
            </div>
        </div>
    </div>
 
<div class="container-fluid span8" style="margin-top: 0px">
	
    <div class="row-fluid">
		
      <section id="global" class="span14">
          
			<div class="row-fluid">
		
        <section id="global" class="span7">
		<fieldset class="form-horizontal">
		<legend>Amazon Product API </legend>

 
			</fieldset>	
            <form id="amazonForm" class="form-horizontal" action="" method="post">
                <fieldset>

                <!-- Form Name -->
                

                <!-- Text input-->
  
				
				<div class="control-group">
                  <label class="control-label" for="searchField">UPC</label>
                  <div class="controls">
                    <input id="SellerID" name="upc" placeholder="enter UPC Code" class="input-large" type="text">
				    
					
                  </div>
                </div>
               
    <div class="control-group">
                  <div class="controls">
                    <button type="submit" id="searchWord" name="searchWord" class="btn btn-primary">search</button>
                  </div>
                </div>
        </fieldset>
   </form>
    
        
        </section>     
    </div>

		<div id="firstTable">
	</div>
</div>
	</div>		
	<div class="spacer"></div>

<script>
var ua = navigator.userAgent,
     event = (ua.match(/iPad/i)) ? "touchstart" : "click";
$("#amazonForm").bind("submit", function(ev){
			ev.preventDefault();
			
			// alert(username);
			
					alertify.confirm("Get list products?", function (e) {
						if (e) {
							// user clicked "ok"
							var data = $("#amazonForm").serialize();
							
							$.ajax({
								url    : "../Controllers/searchASINAction.php",
								type   : "POST",
								dataType: "json",  
								data   : data,
								beforeSend: function() {
								  
									alertify.log("Checking provided data...", "", 8000);
								}, 
								success : function( result ) {
									if(result["state"]=="Ok") {
										      //oTable.fnDraw();                                
                                          $("#firstTable").html(result["data"]);                                              
										alertify.success("Data displayed successfully.");
                                                              
                                                                               
									} else {
										alertify.error(result["data"]);
									}
									
								},
								error: function() {
									var msg = "Sorry but an error has occurred; Try again.";
									alertify.error(msg);
								}
							}); 
						} else {
							// user clicked "cancel"
							alertify.error("Action was cancelled.");
						}
						
						// form.submit();
					});
				
			})
			
			 $("#clear").live(event, function(ev){
      ev.preventDefault();
	 
	    
	     
		 alertify.confirm("Clear Search ?", function (e) {
                if (e) {
                    // user clicked "ok"
                    $.ajax({
                        url    : "../Controllers/clearAction.php",
                        type   : "POST",
                        dataType: "json",
                        //data   : "cost="+cost+"&asin="+asin,
                        beforeSend: function() {
                           alertify.log("Checking provided data...", "", 3000);
                            
                        }, 
                        success : function( result) {
                            if(result["state"]=="Ok") {
                                alertify.success("List cleared successfully");
                                oTable.fnDraw();
                            } else {
                                alertify.error(result["data"]);
                                 oTable.fnDraw();
								 }
                        },
                        error: function() {
                            var msg = "Sorry but an error has occurred; Try again.";
                            alertify.error(msg);
                            }
                    }); 
                } else {
                    // user clicked "cancel"
                    alertify.error("Action was cancelled.");
                }
            
        })
       

			})
			  
			   $("#btncost").live(event, function(ev){
      ev.preventDefault();
	 
	     var asin=$(this).val();
		//alert(asin);
		var cost=$("#inputcost"+$(this).val()).val();
	     
		
                
                    // user clicked "ok"
                    $.ajax({
                        url    : "../Controllers/calculateAction.php",
                        type   : "POST",
                        dataType: "json",
                        data   : "cost="+cost+"&asin="+asin,
                        beforeSend: function() {
                           alertify.log("Checking provided data...", "", 3000);
                            
                        }, 
                        success : function( result) {
                            if(result["state"]=="Ok") {
                                alertify.success("ROI calculated successfully");
                                oTable.fnDraw();
                            } else {
                                alertify.error(result["data"]);
                                 oTable.fnDraw();
								 }
                        },
                        error: function() {
                            var msg = "Sorry but an error has occurred; Try again.";
                            alertify.error(msg);
                            }
                    }); 
              
            
       
       

			})
			

	 function CuteWebUI_AjaxUploader_OnTaskComplete(task)
	{
		$("#filename").val(task.FileName);
	}
	
	</script>	        

</script>

	
</body>
</html>