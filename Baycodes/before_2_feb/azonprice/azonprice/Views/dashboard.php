<?php 
session_start();
require_once "../Services/phpuploader/include_phpuploader.php" ?>
<?php require_once "../Services/phpuploader/smart_resize_image.function.php" ?>
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
			  
				@import "../assets/media/css/TableTools.css";
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
						.meter { 
			height: 20px;  /* Can be anything */
			position: relative;
			margin: 60px 0 20px 0; /* Just for demo spacing */
			background: #555;
			-moz-border-radius: 5px;
			-webkit-border-radius: 5px;
			border-radius: 25px;
            width: 30%;	
		}
		.meter > span {
			display: block;
			height: 100%;
    width:0%;
            -webkit-border-top-right-radius: 8x;
			-webkit-border-bottom-right-radius: 8x;
			 -moz-border-radius-topright: 8px;
			    -moz-border-radius-bottomright: 8px;
			           border-top-right-radius: 8px;
			        border-bottom-right-radius: 8px;
			    -webkit-border-top-left-radius: 8px;
			 -webkit-border-bottom-left-radius: 8px;
			        -moz-border-radius-topleft: 8px;
			     -moz-border-radius-bottomleft: 8px;
			            border-top-left-radius: 8px;
			         border-bottom-left-radius: 8px;
			background-color: rgb(43,194,83);
			background-image: -webkit-gradient(
			  linear,
			  left bottom,
			  left top,
			  color-stop(0, rgb(43,194,83)),
			  color-stop(1, rgb(84,240,84))
			 );
			background-image: -moz-linear-gradient(
			  center bottom,
			  rgb(43,194,83) 37%,
			  rgb(84,240,84) 69%
			 );
			-webkit-box-shadow: 
			  inset 0 2px 9px  rgba(255,255,255,0.3),
			  inset 0 -2px 6px rgba(0,0,0,0.4);
    		  
			-moz-box-shadow: 
			  inset 0 2px 9px  rgba(255,255,255,0.3),
			  inset 0 -2px 6px rgba(0,0,0,0.4);
    
			box-shadow: 
			  inset 0 2px 9px  rgba(255,255,255,0.3),
			  inset 0 -2px 6px rgba(0,0,0,0.4);
			position: relative;
			overflow: hidden;
    
		}
		.meter > span:after, .animate > span > span {
	
			content: "";
			position: absolute;
			top: 0; left: 0; bottom: 0; right: 0;
			background-image: 
			   -webkit-gradient(linear, 0 0, 100% 100%, 
			      color-stop(.25, rgba(255, 255, 255, .2)), 
			      color-stop(.25, transparent), color-stop(.5, transparent), 
			      color-stop(.5, rgba(255, 255, 255, .2)), 
			      color-stop(.75, rgba(255, 255, 255, .2)), 
			      color-stop(.75, transparent), to(transparent)
			   );
			background-image: 
        	      
				-moz-linear-gradient(
				  -45deg, 
			      rgba(255, 255, 255, .2) 25%, 
			      transparent 25%, 
			      transparent 50%, 
			      rgba(255, 255, 255, .2) 50%, 
			      rgba(255, 255, 255, .2) 75%, 
			      transparent 100%;

			   );
			z-index: 1;
			-webkit-background-size: 50px 50px;
			-moz-background-size: 2px 2px;
			-webkit-animation: move 2s linear infinite;
			   -webkit-border-top-right-radius: 8px;
			-webkit-border-bottom-right-radius: 8px;
			       -moz-border-radius-topright: 8px;
			    -moz-border-radius-bottomright: 8px;
			           border-top-right-radius: 8px;
			        border-bottom-right-radius: 8px;
			    -webkit-border-top-left-radius: 8px;
			 -webkit-border-bottom-left-radius: 8px;
			        -moz-border-radius-topleft: 8px;
			     -moz-border-radius-bottomleft: 8px;
			            border-top-left-radius: 8px;
			         border-bottom-left-radius: 8px;
			overflow: hidden;
    			  
		}
		
		.animate > span:after {
			display: none;
		}
		
		@-webkit-keyframes move {
		    100%{
		       background-position: 0 0;
		    }
		    100% {
		       background-position: 50px 50px;
		    }
		}
	
		
		.red > span {

			background-color: #f0a3a3;
			background-image: -moz-linear-gradient(top, #f0a3a3, #f42323);
			background-image: -webkit-gradient(linear,left top,left bottom,color-stop(0, #f0a3a3),color-stop(1, #f42323));
			background-image: -webkit-linear-gradient(#f0a3a3, #f42323);
		}
		
		

		</style>
		<script src="http://code.jquery.com/jquery-1.8.2.js"></script>
    <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>
    <script src="http://heartcode-canvasloader.googlecode.com/files/heartcode-canvasloader-min-0.9.1.js"></script>
    <script src="../assets/media/js/jquery.dataTables.js"></script>
    <script src="../assets/media/js/DT_bootstrap.js"></script>
    <script src="../assets/media/js/ZeroClipboard.js"></script>
    <script src="../assets/media/js/TableTools.js"></script>
    <script type="text/javascript" charset="utf-8" src="http://datatables.github.com/Plugins/integration/bootstrap/2/dataTables.bootstrap.js"></script>
    <script src="../assets/media/js/FixedColumns.js"></script>
    <script src="../assets/media/js/jquery.dataTables.columnFilter.js"></script>
    <script src="../assets/fancyBox/source/jquery.fancybox.js?v=2.1.5"></script>
    <script src="../assets/alertify/alertify.min.js"></script>
        <script type="text/javascript" src="jquery.keepAlive.js"></script>
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
							<a href="dashboard.php">Dashboard</a>
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
 
<div class="container-fluid span14" style="margin-top: 0px">
	
    <div class="row-fluid">
		
      <section id="global" class="span14">
          
			<div class="row-fluid">
		
        <section id="global" class="span12">
		<fieldset class="form-horizontal">
		<legend>Amazon Product API </legend>

 <div class="control-group">
                  <label class="control-label" for="searchField">Upload from</label>
                  <div class="controls">
                  <?php
			$uploader=new PhpUploader();
			
			$uploader->MultipleFilesUpload=false;
			$uploader->InsertText="Upload File (Max 10M)";
			
			$uploader->MaxSizeKB=1024000;	
			$uploader->AllowedFileExtensions="xls,csv";
			
			//Where'd the files go?
			$uploader->SaveDirectory="../assets/uploads";
			
			$uploader->Render();?>
                  </div>
                </div>
			</fieldset>	
            <form id="amazonForm" class="form-horizontal" action="" method="post">
                <fieldset>

                <!-- Form Name -->
                

                <!-- Text input-->

				
				<div class="control-group">
                  <label class="control-label" for="searchField">Or Asin/UPC</label>
                  <div class="controls">
                    <input id="asin" name="asin" placeholder="enter Asin/UPC Code" class="input-large" type="text">
				    <input id="filename" name="upfile" type="hidden" value="">
					
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
	<div id="progress" style="display:none;">
	<div id="page-wrap">
	
		<div class="meter red">
            <span style="width:5%"></span>
			
		</div>
         
	</div>
	
     capturing data for product <span id="percent">0</span>/<span id="nbrows"></span>
	</div>
	<br>
	 <div class="btn-group">
				<button id="clear" class="btn btn-warning">Clear search</button>
			</div>
	<?php include('../Controllers/amazondafaultlist.php'); ?>
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
						var data = $("#amazonForm").serialize();
						if($("#asin").val()==""){
						  $("#progress").show();
							
							$.ajax({
								url    : "../Controllers/sizefile.php",
								type   : "POST",
								dataType: "json",  
								data   : data,
								success : function( result ) {
									if(result["state"]=="Ok") {
									$("#nbrows").html(result["data"]);
                                     //$("#nbrows").html(20);  									
                                         var step =  0;
                                      var m=0;
									var total=parseInt($("#nbrows").html());
						             
                          console.log(step);
                          var interval = setInterval(function () {
                          
						  step += 1;
						   pas=(100*step)/total;
		                  $("#percent").html(step);
							
							oTable.fnDraw(); 
                         $('#page-wrap span').animate({width: pas+"%"}, {duration:30000, easing: 'linear'});
                            if(pas ==100){
		                    clearInterval(interval);
							alertify.success("Data displayed successfully.");
							oTable.fnDraw(); 
							}
                           }, 30000);
                        
                                                                               
									} else {
										alertify.error(result["data"]);
									}
									
								}
								});
								$.ajax({
								url    : "../Controllers/amazonAction.php",
								type   : "POST",
								dataType: "json",  
								data   : data,
								
								beforeSend: function() {
									 
								}, 
								success : function( result ) {
									if(result["state"]=="Ok") {
										      oTable.fnDraw();                                
                                          //$("#firstTable").html(result["data"]);                                              
										//alertify.success("Data displayed successfully.");
                                                              
                                                                               
									} else {
										alertify.error(result["data"]);
									}
									
								},
								error: function() {
									//var msg = "Sorry but an error has occurred; Try again.";
										 //oTable.fnDraw(); 
										//alertify.success("Data displayed successfully.");
								}
							}); 
						
						 }
                          else {
						  
						  $.ajax({
								url    : "../Controllers/amazonAction.php",
								type   : "POST",
								dataType: "json",  
								data   : data,
								
								beforeSend: function() {
									 alertify.log("Checking provided data...", "",8000); 
								}, 
								success : function( result ) {
									if(result["state"]=="Ok") {
										      oTable.fnDraw();                                
                                          //$("#firstTable").html(result["data"]);                                              
										alertify.success("Data displayed successfully.");
                                                              
                                                                               
									} else {
										alertify.error(result["data"]);
									}
									
								},
								error: function() {
									//var msg = "Sorry but an error has occurred; Try again.";
										 oTable.fnDraw(); 
										alertify.success("Data displayed successfully.");
								}
							}); 
						  
						  }						 
                         	
							// user clicked "ok"
							 
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