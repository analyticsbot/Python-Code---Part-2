<?php 
$getSearchPageData=getpagesData($_POST['upc']);
  $formatedTable =getformatPagesData($getSearchPageData);
$htmlTable  = '


		<table cellpadding="0" cellspacing="0" border="0" class="table table-bordered" id="itemsTable" style="height:850px">
                <thead>
                  <tr>
				    <th class="span2">ASIN</th>
                   


                  </tr>
                </thead>
                <tbody>
                </tbody>
              </table>
              
             
     <script>
                var gaiSelected = [];
              
                var oTable;
                 oTable = $("#itemsTable").dataTable({"bCustomFilter":true,
                    "aaSorting": [[ 1, "asc" ]],
                    "sScrollX": "99%",
                    "bAutoWidth": false,
                    "sScrollY": "500px",
                    "bScrollCollapse": true,
					 "sDom": "<\'row-fluid\'<\'span6\'T><\'span6\'f>r>l<\'clearfix\'>t<\'row-fluid\'ip>",
                    "oTableTools": {
                        "sSwfPath": "../assets/media/swf/copy_csv_xls_pdf.swf",
                        "aButtons": [
                            "copy",
                            {
                                "sExtends":    "collection",
                                "sButtonText": \'Save <span class="caret" />\',
                                "aButtons":    [ "csv", "xls", "pdf" ]
                            }
                        ]
                    },
                    "bPaginate": true,
                    "aaData": '.($formatedTable["aaData"]).',
                })
               
                </script> ';


$result = array("state"=>"Ok", "data"=> $htmlTable);
echo json_encode($result);

function getpagesData($upc) {
     
        $resultFinalArray=array();
		
		$upc=rawurlencode($upc);
 
 	   $apicall= sign_query1('ASIN',$upc,'ItemAttributes');
        //$responses = simplexml_load_file($apicall);
		
        //$upc=$responses->Items->Item->ItemAttributes->UPC;
		
        $apicall= sign_query1('UPC',$upc,'ItemAttributes');
        $responses = simplexml_load_file($apicall);
        foreach($responses->Items->Item as $response)
		{  
		    $resultFinal = array('asin'=>'n/a');
			
		  $resultFinal['asin']="<a target='_blank' href=".$response->DetailPageURL.">".$response->ASIN."</a>";
		  //$resultFinal['link']=$response->ItemLinks->ItemLink->URL;
          $resultFinalArray[] = $resultFinal;
		}
  
return  $resultFinalArray;
}


function getformatPagesData($getSearchPageData)
{
    
    $result = array("aaData" => '[ ');
    foreach($getSearchPageData as $item ) {

        $row = '';
        $row .='["'.$item["asin"].'"], ';
       
        $result["aaData"] .= $row;
    }
    $result["aaData"] .= ' ]';

    return $result;

}



function sign_query1($param,$itemid,$response) {
    //sanity check
    if($param=='UPC') {
	
	$parameters = array( 'Operation'     =>'ItemLookup',
        'ResponseGroup' =>$response,
        'Condition'   =>'All',
		'SearchIndex'=>'All',
        'IdType'=>'UPC',
        'ItemId'=>$itemid,
		
    );
  }
  else if($param=='ASIN') {
  $parameters = array( 'Operation'     =>'ItemLookup',
        'ResponseGroup' =>$response,
        'Condition'   =>'All',
        'IdType'=>'ASIN',
        'ItemId'=>$itemid,
		
    );
  }
    if(! $parameters) return '';

    /* create an array that contains url encoded values
       like "parameter=encoded%20value"
       USE rawurlencode !!! */
    $encoded_values = array();
    foreach($parameters as $key=>$val) {
        $encoded_values[$key] = rawurlencode($key) . '=' . rawurlencode($val);
    }

    /* add the parameters that are needed for every query
       if they do not already exist */
    if(! $encoded_values['AssociateTag'])
        $encoded_values['AssociateTag']= 'AssociateTag='.rawurlencode('amazoninvento-20');
    if(! $encoded_values['AWSAccessKeyId'])
        $encoded_values['AWSAccessKeyId'] = 'AWSAccessKeyId='.rawurlencode('AKIAI7TLPEZHY2P3EUYA');
    if(! $encoded_values['Service'])
        $encoded_values['Service'] = 'Service=AWSECommerceService';
    if(! $encoded_values['Timestamp'])
        $encoded_values['Timestamp'] = 'Timestamp=2016-08-25T18%3A01%3A21.000Z';
    if(! $encoded_values['Version'])
        $encoded_values['Version'] = 'Version=2011-08-01';

    /* sort the array by key before generating the signature */
    ksort($encoded_values);


    /* set the server, uri, and method in variables to ensure that the
       same strings are used to create the URL and to generate the signature */
    $server = 'webservices.amazon.com';
    $uri = '/onca/xml'; //used in $sig and $url
    $method = 'GET'; //used in $sig


    /* implode the encoded values and generate signature
       depending on PHP version, tildes need to be decoded
       note the method, server, uri, and query string are separated by a newline */
    $query_string = str_replace("%7E", "~", implode('&',$encoded_values));
    $sig = base64_encode(hash_hmac('sha256', "{$method}\n{$server}\n{$uri}\n{$query_string}",'pyCL8svd2InFmpPgOgf9J6YXp2fDD6r5dB12EZCB', true));

    /* build the URL string with the pieces defined above
       and add the signature as the last parameter */
    $url = "http://{$server}{$uri}?{$query_string}&Signature=" . str_replace("%7E", "~", rawurlencode($sig));
 // $url="http://webservices.amazon.co.uk/onca/xml?AWSAccessKeyId=AKIAI7TLPEZHY2P3EUYA&AssociateTag=amazoninvento-20&Condition=All&IdType=UPC&ItemId=074182262549&Operation=ItemLookup&ResponseGroup=ItemAttributes&SearchIndex=All&Service=AWSECommerceService&Timestamp=2014-09-25T16%3A03%3A50.000Z&Version=2011-08-01&Signature=oeBhQ4Iqud%2BuCqiJIDlZte1q%2FWqR3h99AD5fLf9va5Q%3D";
  // echo $url;die;
  return $url;
	
}
?>