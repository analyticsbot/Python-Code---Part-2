<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">


<head >
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Ebay Tool</title>
<link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet" type="text/css" />
<link href="http://datatables.github.com/Plugins/integration/bootstrap/2/dataTables.bootstrap.css" rel="stylesheet" type="text/css" />
<link rel="stylesheet" href="../assets/media/css/TableTools.css" />
<!-- include the core styles -->
<link rel="stylesheet" href="../assets/alertify/alertify.core.css" />
<!-- include a theme, can be included into the core instead of 2 separate files -->
<link rel="stylesheet" href="../assets/alertify/alertify.default.css" />
<link rel="stylesheet" href="../assets/guiders/guiders.css" />
<style>
	@import "../assets/media/css/DT_bootstrap.css";
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
     	table  {
            height:70px !important;
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
        .alertify, .alertify-logs{
            z-index: 99999;
        }
        .row_selected {
            background-color:#FFF973  !important;
        } ul.DTTT_dropdown.dropdown-menu {
          z-index: 2003;
        }div.DTTT_collection {
            width: 150px;
            padding: 8px 8px 4px 8px;
            border: 1px solid #ccc;
            border: 1px solid rgba( 0, 0, 0, 0.4 );
            background-color: #f3f3f3;
          background-color: rgba( 255, 255, 255, 0.3 );
            overflow: hidden;
            z-index: 2002;
         
            -webkit-border-radius: 5px;
               -moz-border-radius: 5px;
                -ms-border-radius: 5px;
                 -o-border-radius: 5px;
                    border-radius: 5px;
             
            -webkit-box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
               -moz-box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
                -ms-box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
                 -o-box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
                    box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
        }
</style>
<script src="http://code.jquery.com/jquery-1.7.2.js"></script>
<script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>
<script src="http://heartcode-canvasloader.googlecode.com/files/heartcode-canvasloader-min-0.9.1.js"></script>
<script src="../assets/media/js/jquery.dataTables.js"></script>
<script src="../assets/media/js/DT_bootstrap.js"></script>
<script type="text/javascript" charset="utf-8" src="http://haffoudhijobs.com/Jobs/amazon/assets/media/js/ZeroClipboard.js"></script>
<script src="http://haffoudhijobs.com/Jobs/amazon/assets/media/js/TableTools.js"></script>
<script type="text/javascript" charset="utf-8" src="http://datatables.github.com/Plugins/integration/bootstrap/2/dataTables.bootstrap.js"></script>
<script src="../assets/media/js/jquery.dataTables.columnFilter.js"></script>
<script src="../assets/alertify/alertify.min.js"></script>
<script src="../assets/guiders/guiders.js"></script>

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
				
				 
				<!-- Everything you want hidden at 940px or less, place within here -->
				<div class="nav-collapse collapse">
				<!-- .nav, .navbar-search, .navbar-form, etc -->
					<ul class="nav">
					<li>
						 <img src="../assets/images/logo.jpg" width="107px" height="8px">		
							</li>
						<li>
							<a href="dashboard.php">Dashboard</a>
						</li>
						
						<li>
							<a href="settingaccount.php">My profile</a>
						</li>
								
					   <li class="active">
							<a href="subscription.php">Subscribe in Level</a>
						</li>
					  
					</ul>
						
					</ul>
					<ul class="nav pull-right">
						<li class="dropdown">
						  <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="icon-user icon-white"></i> Hello <?php echo $_SESSION['username'] ?><b class="caret"></b></a>
						  <ul class="dropdown-menu">
							<li><a href="logout.php">Logout</a></li>
							</ul>
						</li>
					</ul>
				</div>
             
            </div>
        </div>
    </div>
 
<div class="container-fluid span12" style="margin-top: 0px">
	<div class="row-fluid">
		
        <section id="global" class="span12">
           
            <form class="form-horizontal" action="" method="post">
                <fieldset>

                <!-- Form Name -->
                <legend>Ebay API Profile</legend>

                <!-- Text input-->
                <div class="control-group">
                  <label class="control-label" for="searchField">SellerID</label>
                  <div class="controls">
                    <input id="SellerID" name="SellerID" placeholder="enter Seller ID" class="input-large" type="text" required="">
                  </div>
                </div>

                <!-- Text input-->
                <div class="control-group">
                  <label class="control-label" for="limit">Site</label>
                  <div class="controls">
                   <select id="GlobalID" name="GlobalID">
                     <option value="EBAY-AU">Australia - EBAY-AU (15) - AUD</option>
                     <option value="EBAY-ENCA">Canada (English) - EBAY-ENCA (2) - CAD</option>
                     <option value="EBAY-DE">Germany - EBAY-DE (77) - EUR</option>
                     <option value="EBAY-GB">United Kingdom - EBAY-GB (3) - GBP</option>
                     <option selected value="EBAY-US">United States - EBAY-US (0) - USD</option>
                   </select>
                  </div>
                </div>

                
                <!-- Button -->
                <div class="control-group">
				   <label class="control-label" for="limit">Items Types</label>
                  <div class="controls">
                   <select id="ItemType" name="ItemType">
                     <option selected value="All">All Item Types</option>
                     <option value="Auction">Auction Items Only</option>
                     <option value="FixedPriced">Fixed Priced Item Only</option>
                   </select>
				   
                  </div>
                </div>
                    <div class="control-group">
				   <label class="control-label" for="limit">Items Sort</label>
                  <div class="controls">
                  <select id="ItemSort" name="ItemSort">
                     <option value="BidCountFewest">Bid Count (fewest bids first) [Applies to Auction Items Only]</option>
                     <option selected value="EndTimeSoonest">End Time (soonest first)</option>
                     <option value="PricePlusShippingLowest">Price + Shipping (lowest first)</option>
                    <option value="CurrentPriceHighest">Current Price Highest</option>
                  </select>
				   
                  </div>
                </div>
                   <div class="control-group">
				   <label class="control-label" for="limit">Debug</label>
                  <div class="controls">
                   <select id="Debug" name="Debug">
                       <option value="1">true</option>
                        <option selected value="0">false</option>
                   </select> 
                  </div>
                </div>
 <div class="control-group">
                  <div class="controls">
                    <button type="submit" id="searchWord" name="searchWord" class="btn btn-primary">search</button>
                  </div>
                </div>
                </fieldset>
            </form>
        <br>
        <div id="firstTableLoad"></div>
       
        
		<div id="firstTable"></div>
         
        </section>
    </div>


	</div>		
			<div class="spacer"></div>
      
    <br>
    <br>

    <script type="text/javascript">
        var ua = navigator.userAgent,
        event = (ua.match(/iPad/i)) ? "touchstart" : "click";
       
        
        $("form").bind("submit", function (ev) {
            ev.preventDefault();
            var SellerID = $("#SellerID").val();
			var GlobalID= $("#GlobalID").val();
			var Debug= $("#Debug").val();
			var ItemType=$("#ItemType").val();
			var ItemSort=$("#ItemSort").val();
			
            alertify.confirm("Search for this SellerID ?", function (e) {
                if (e) {
                    // user clicked "ok"
                    $.ajax({
                        url    : "../Controllers/EbayAction.php",
                        type   : "POST",
                        dataType: "json",
                        data   : "SellerID="+SellerID+"&GlobalID="+GlobalID+"&Debug="+Debug+"&ItemType="+ItemType+"&ItemSort="+ItemSort,
                        beforeSend: function() {
                            alertify.log("Searching Ebay Product , be patient...", "", 3000);
                            $("#firstTableLoad").text("loading...");
                            $("#firstTable").empty();
                         
                        }, 
                        success : function( result) {
                            if(result["state"]=="Ok") {
                                alertify.success("data scraped successfully.");
                                $("#firstTable").html(result["data"]);
								
                                $("#firstTableLoad").text("");
                              
                            } else {
                                alertify.error(result["data"]);
                                $("#firstTableLoad").text("Error occurred");
                            }
                        },
                        error: function() {
                            var msg = "Sorry but an error has occurred; Try again.";
                            alertify.error(msg);
                            $("#firstTableLoad").text("Error occurred");
                        }
                    }); 
                } else {
                    // user clicked "cancel"
                    alertify.error("Action was cancelled.");
                }
            
        })
        })
    </script>

</body>
</html>