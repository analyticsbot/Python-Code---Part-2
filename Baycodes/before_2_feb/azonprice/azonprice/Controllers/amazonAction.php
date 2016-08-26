<?php
set_time_limit(0);
//require_once (__DIR__ . '/..') . '/SEOstats/bootstrap.php';
include "simple_html_dom.php";
require_once (__DIR__ . '/..') . '/Services/parsecsv.lib.php';
      
require_once (__DIR__ . '/..') . '/Services/Excel/reader.php';
include "config.inc.php";   

/*******Saving Vendor data*********/

    if(isset($_POST['upfile'])&&$_POST['upfile']!="") {

         $allowedExts = array("csv", "xls");
        $temp = explode(".",$_POST['upfile']);
        $extension = end($temp);
       
        if($extension=="csv") {
		 
            $csv = new parseCSV();
			$csv->auto('../assets/uploads/'.$_POST['upfile']);
			
            foreach ($csv->data as $key => $row):
               $asin=$row['asin'];
			       $pattern = '/^B00/';
                 $posasin=preg_match($pattern,$asin, $matches, PREG_OFFSET_CAPTURE);
	            if($posasin||is_numeric($asin)){    
				   $pattern = '/^B00/';
                 $posasin=preg_match($pattern,$asin, $matches, PREG_OFFSET_CAPTURE);
	             if(!$posasin){
                  $apicall=sign_query('UPC',$asin,'ItemAttributes');
	              $respasin = simplexml_load_file($apicall);
		          $asin=$respasin->Items->Item->ASIN;
		           }
			      $result=scraping_amazon($asin);
				  
	                $sql="SELECT * FROM azon_products WHERE asin='".$asin."'";
	               $res=$connexion->query($sql);
	  
	              if(!$res->fetchColumn()){
	               $result=scraping_amazon($asin);
				   if(!isset($result['fbaprice1'])){$result['fbaprice1']="";}
				   if(!isset($result['fbaprice2'])){$result['fbaprice2']="";}
				   if(!isset($result['fbaprice3'])){$result['fbaprice3']="";}
				   if(!isset($result['sellerprice1'])){$result['sellerprice1']="";}
				   if(!isset($result['sellerprice2'])){$result['sellerprice2']="";}
				   if(!isset($result['sellerprice3'])){$result['sellerprice3']="";}
				   
	              $sql="INSERT INTO azon_products(asin,title,category,productrank,amazon_price,fba_price1,fba_price2,fba_price3,seller_price1,seller_price2,seller_price3)
	               values('".$asin."','".$result['title']."','".$result['category']."','".$result['productrank']."','".$result['amazon_price']."','".$result['fbaprice1']."','".$result['fbaprice2']."','".$result['fbaprice3']."','".$result['sellerprice1']."','".$result['sellerprice2']."','".$result['sellerprice3']."')";
	               echo $sql.'<br>';
	              $connexion->exec($sql);
	            
	            
	              }
                sleep(1);				
				} 
			 endforeach;  
          		 if($connexion){
	               $result = array("state"=>"Ok", "data"=>'');
	                echo json_encode($result);
	                }	 
        }
        else

            if($extension=="xls") {

                $data = new Spreadsheet_Excel_Reader();
                $data->setOutputEncoding('CP1251');
                $data->read('../assets/uploads/'.$_POST['upfile']);

                for ($i = 1; $i <=$data->sheets[0]['numRows']; $i++) {
                 
				 $asin=$data->sheets[0]['cells'][$i][1];
				 $upc="";
				 $pattern = '/^B00/';
                 $posasin=preg_match($pattern,$asin, $matches, PREG_OFFSET_CAPTURE);
	            if($posasin||is_numeric($asin)){    
				   $pattern = '/^B00/';
                 $posasin=preg_match($pattern,$asin, $matches, PREG_OFFSET_CAPTURE);
	             if(!$posasin){
				  $upc=$asin; 
                  $apicall=sign_query('UPC',$asin,'ItemAttributes');
	              $respasin = simplexml_load_file($apicall);
		          $asin=$respasin->Items->Item->ASIN;
		          
				   }  
				   	             
				   $sql="SELECT * FROM azon_products WHERE asin='".$asin."'";
	               $res=$connexion->query($sql);
	  
	              if(!$res->fetchColumn()){
				   $result=scraping_amazon($asin);
				   if(!isset($result['fbaprice1'])){$result['fbaprice1']="";}
				   if(!isset($result['fbaprice2'])){$result['fbaprice2']="";}
				   if(!isset($result['fbaprice3'])){$result['fbaprice3']="";}
				   if(!isset($result['sellerprice1'])){$result['sellerprice1']="";}
				   if(!isset($result['sellerprice2'])){$result['sellerprice2']="";}
				   if(!isset($result['sellerprice3'])){$result['sellerprice3']="";}
				   
	              $sql="INSERT INTO azon_products(asin,upc,title,category,productrank,amazon_price,fba_price1,fba_price2,fba_price3,seller_price1,seller_price2,seller_price3)
	               values('".$asin."','".$upc."','".$result['title']."','".$result['category']."','".$result['productrank']."','".$result['amazon_price']."','".$result['fbaprice1']."','".$result['fbaprice2']."','".$result['fbaprice3']."','".$result['sellerprice1']."','".$result['sellerprice2']."','".$result['sellerprice3']."')";
	               echo $sql.'<br>';
				  // die;
	              $connexion->exec($sql);
	            
	              }
            
				  
             }
			 sleep(1);	
			}
			 if($connexion){
	               $result = array("state"=>"Ok", "data"=>'');
	                echo json_encode($result);
	                }
		}	
    }
    else {
       $asin=$_POST['asin'];
	    $pattern = '/^B00/';
		$upc="";
        $posasin=preg_match($pattern,$asin, $matches, PREG_OFFSET_CAPTURE);
	    if($posasin||is_numeric($asin)){    
				   $pattern = '/^B00/';
                 $posasin=preg_match($pattern,$asin, $matches, PREG_OFFSET_CAPTURE);
	             if(!$posasin){
                   $upc=$asin; 
				  $apicall=sign_query('UPC',$asin,'ItemAttributes');
	              $respasin = simplexml_load_file($apicall);
		          $asin=$respasin->Items->Item->ASIN;
		         
				   }  
				   	             
				   $sql="SELECT * FROM azon_products WHERE asin='".$asin."'";
	               $res=$connexion->query($sql);
	  
	              if(!$res->fetchColumn()){
				   $result=scraping_amazon($asin);
				   if(!isset($result['fbaprice1'])){$result['fbaprice1']="";}
				   if(!isset($result['fbaprice2'])){$result['fbaprice2']="";}
				   if(!isset($result['fbaprice3'])){$result['fbaprice3']="";}
				   if(!isset($result['sellerprice1'])){$result['sellerprice1']="";}
				   if(!isset($result['sellerprice2'])){$result['sellerprice2']="";}
				   if(!isset($result['sellerprice3'])){$result['sellerprice3']="";}
				   
	              $sql="INSERT INTO azon_products(asin,upc,title,category,productrank,amazon_price,fba_price1,fba_price2,fba_price3,seller_price1,seller_price2,seller_price3)
	               values('".$asin."','".$upc."','".$result['title']."','".$result['category']."','".$result['productrank']."','".$result['amazon_price']."','".$result['fbaprice1']."','".$result['fbaprice2']."','".$result['fbaprice3']."','".$result['sellerprice1']."','".$result['sellerprice2']."','".$result['sellerprice3']."')";
	               echo $sql.'<br>';
				 
	              $connexion->exec($sql);
	            
	              }
            
				  
             }
	   if($connexion){
	   $result = array("state"=>"Ok", "data"=>'');
	 echo json_encode($result);
	   }
	   }

    
//return $resultFinalArray;

function scraping_amazon($asin){

$result=array();

$url="http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=".$asin;

$data=getPage($url);
 $html = str_get_html($data);
 foreach($html->find('div[class=a-column a-span12 a-text-center] a[class=a-link-normal a-text-normal]') as $href) {
$url=$href->href;
 break;
 }
 $tasin=explode('/',$url);
$asin=$tasin[5];
 
$data=getPage($url);

  $html = str_get_html($data);
$result['title']="";   
 foreach($html->find('h1[id=title] span[id=productTitle]') as $title) {
$result['title']=$title->plaintext;
break;
}
$result['title']=str_replace("'","\'",$result['title']);
//echo $result['title'];die;
$result['asin']=$asin;
$result['category']="";
 foreach($html->find('ul div[class=detailBreadcrumb]') as $breadcrumb) {
   foreach($breadcrumb->find('li a') as $category) {
    $result['category'].=$category->plaintext.'>';
}
}
foreach($html->find('div[id=wayfinding-breadcrumbs_feature_div] ul') as $breadcrumb) {
   foreach($breadcrumb->find('li a') as $category) {
    $result['category'].=$category->plaintext.'>';
}
}
 
 
$result['category']=trim($result['category']);
$result['category']=substr($result['category'],0,strlen($result['category'])-1);
//echo trim($result['category']);die;
 $result['productrank']="";
 foreach($html->find('li[id=SalesRank]') as $salerank) {
 $result['productrank']=$salerank->plaintext;
}
foreach($html->find('tr[id=SalesRank] td[class=value]') as $salerank) {

$result['productrank']=$salerank->plaintext;

}

$pos1=strpos($result['productrank'],'(');

$result['productrank']=substr($result['productrank'],0,$pos1);

$trank=explode(':',$result['productrank']);
if(!isset($trank[1])){
$result['productrank']=trim($trank[0]);
}
else {
$result['productrank']=trim($trank[1]);
}

$result['amazon_price']="";

$amazon_price=scrape_amazonprice($asin);
//echo $amazon_price;die;
if($amazon_price!=""){
 $result['amazon_price']=substr(trim($amazon_price),1,strlen(trim($amazon_price))); 
 }
elseif($result['amazon_price']=="") {
 foreach($html->find('span[id=priceblock_ourprice]') as $price) {
$amzprice=substr($price->plaintext,1,strlen($price->plaintext));
$result['amazon_price']=$amzprice;
break;
}
}
if($result['amazon_price']==""){
foreach($html->find('span[id=priceblock_saleprice]') as $price) {
$amzprice=substr($price->plaintext,1,strlen($price->plaintext));
$result['amazon_price']=$amzprice;
break;
}
}

$fbaprice=scrape_fbaprice($asin);

$result['fbaprice1']="";
$result['fbaprice2']="";
$result['fbaprice3']="";

if($fbaprice[0]!=""){
$result['fbaprice1']=substr(trim($fbaprice[0]),1,strlen(trim($fbaprice[0])));
}
if($fbaprice[1]!=""){
$result['fbaprice2']=substr(trim($fbaprice[1]),1,strlen(trim($fbaprice[1])));
}
if($fbaprice[2]!=""){
$result['fbaprice3']=substr(trim($fbaprice[2]),1,strlen(trim($fbaprice[2])));
}

$result['sellerprice1']="";
$result['sellerprice2']="";
$result['sellerprice3']="";

$sellerprice=scrape_sellerprice($asin);

if($sellerprice[0]!=""){
$result['sellerprice1']=substr(trim($sellerprice[0]),1,strlen(trim($sellerprice[0])));

}
if($sellerprice[1]!=""){
$result['sellerprice2']=substr(trim($sellerprice[1]),1,strlen(trim($sellerprice[1])));
}
if($sellerprice[2]!=""){
$result['sellerprice3']=substr(trim($sellerprice[2]),1,strlen(trim($sellerprice[2])));
}
 


 return $result;
	 }


function scrape_amazonprice($asin) {

$url="http://www.amazon.com/gp/offer-listing/".$asin."/ref=dp_olp_new?ie=UTF8&condition=new";
$data=getPage($url);
$pass=0;
$amazon_price="";
  $html = str_get_html($data);
  foreach($html->find('div[class=a-section a-spacing-double-large]') as $html1) {
  foreach($html1->find('div[class=a-row a-spacing-mini olpOffer]') as $html2) {
      foreach($html2->find('div[class=a-column a-span2 olpSellerColumn] img') as $html3) {
	   if($html3->src=='http://ecx.images-amazon.com/images/I/01dXM-J1oeL.gif'){
	   $pass=1;
	 
	   }
	   
	  }
	  if($pass==1){
     
	  foreach($html2->find('div[class=a-column a-span2]') as $html3) {
	    foreach($html3->find('span[class=a-size-large a-color-price olpOfferPrice a-text-bold]') as $html4) {
	    
		 $amazon_price=trim($html4->plaintext);
		return $amazon_price;
        //return trim($amazon_price;         
		}
		
			}
	}
  else {continue;}	
	  }
}

return $amazon_price;
}	

function scrape_fbaprice($asin) {

$url="http://www.amazon.com/gp/offer-listing/".$asin."/ref=dp_olp_new?ie=UTF8&condition=new";

$data=getPage($url);


$fba_price=array();
  $html = str_get_html($data);
  foreach($html->find('div[class=a-section a-spacing-double-large]') as $html1) {
  
  foreach($html1->find('div[class=a-row a-spacing-mini olpOffer]') as $html2) {
       $nb=0;
	  foreach($html2->find('div[class=a-column a-span3 olpDeliveryColumn] div[class=olpBadgeContainer] a') as $html3) {
	   // echo $html3->plaintext;die;
	   if(trim($html3->plaintext)=='Fulfillment by Amazon'){
	   $nb=1;
	   }
	   
	  }
	  if($nb==1){
    
	  foreach($html2->find('div[class=a-column a-span2]') as $html3) {
	    foreach($html3->find('span[class=a-size-large a-color-price olpOfferPrice a-text-bold]') as $html4) {
	    
		 $fba_price[]=$html4->plaintext;
        //return trim($amazon_price);         
		break;
		}
		break;
			}
	}

	  }
	
}
return  $fba_price;
} 
function scrape_sellerprice($asin) {


$url="http://www.amazon.com/gp/offer-listing/".$asin."/ref=dp_olp_new?ie=UTF8&condition=new";
$data=getPage($url);
$amaz=0;
$seller=0;
$fba=0;
  $html = str_get_html($data);
  foreach($html->find('div[class=a-section a-spacing-double-large]') as $html1) {
   
  foreach($html1->find('div[class=a-row a-spacing-mini olpOffer]') as $html2) {
    $amaz=0;
     $seller=0;
       $fba=0;
      foreach($html2->find('div[class=a-column a-span2 olpSellerColumn] img') as $html3) {
	   if($html3->src=='http://ecx.images-amazon.com/images/I/01dXM-J1oeL.gif'){
	   $amaz=1;
	 
	   }
	   }
	  foreach($html2->find('div[class=a-column a-span2 olpSellerColumn] a img') as $html3) {
	   $seller=1;
	   
	  }
	   foreach($html2->find('div[class=a-column a-span3 olpDeliveryColumn] div[class=olpBadgeContainer] a') as $html3) {
	   // echo $html3->plaintext;die;
	   if(trim($html3->plaintext)=='Fulfillment by Amazon'){
	   $fba=1;
	   }
	   
	  }

	  foreach($html2->find('div[class=a-column a-span2 olpSellerColumn] span[class=a-size-medium a-text-bold]') as $html3) {
	  
	  $seller=1;
	   
	  }
	
	  if($seller==1&&$amaz==0&&$fba==0){
       
	  foreach($html2->find('div[class=a-column a-span2]') as $html3) {
	  $amazonprice="";
	    foreach($html3->find('span[class=a-size-large a-color-price olpOfferPrice a-text-bold]') as $html4) {
	     
		 $amazonprice=substr(trim($html4->plaintext),1,strlen(trim($html4->plaintext)));
          break;        
		}
		  $shippingprice="";
		  foreach($html3->find('p[class=olpShippingInfo] span[class=olpShippingPrice]') as $html4) {
	     
		 $shippingprice=substr(trim($html4->plaintext),1,strlen(trim($html4->plaintext)));
           break;      
		}
		$price=$amazonprice+$shippingprice;
		
		$amazonsellerprice[]='$'.$price;
			}
	}

	  }
}

return $amazonsellerprice; 
}
	


function sign_query($param,$itemid,$response) {
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
   //echo $url;die;
  return $url;
	
}



function getPage($url)
{
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_MAXREDIRS, 20 );
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 500);
    curl_setopt($ch, CURLOPT_TIMEOUT, 500);
    $ua = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0";
    curl_setopt($ch, CURLOPT_USERAGENT, $ua);

    $str = curl_exec($ch);
   
    curl_close($ch);
    sleep(6);

    return $str;

}

?>
