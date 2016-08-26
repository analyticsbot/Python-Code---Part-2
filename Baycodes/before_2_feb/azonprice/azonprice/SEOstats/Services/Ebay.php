<?php
namespace SEOstats\Services;

/**
 * SEOstats extension for Amazon data.
 *
 * @package    SEOstats
 * @author     Stephan Schmitz <eyecatchup@gmail.com>
 * @copyright  Copyright (c) 2010 - present Stephan Schmitz
 * @license    http://eyecatchup.mit-license.org/  MIT License
 * @updated    2013/08/14
 */
 
use SEOstats\Common\SEOstatsException as E;
use SEOstats\SEOstats as SEOstats;
use SEOstats\Config as Config;
use SEOstats\Helper as Helper;




class Ebay extends SEOstats
{
    public static function array_push_associative(&$arr) {
        $args = array();
       $args = func_get_args();
       $ret=0;
       $count=0;
       foreach ($args as $arg) {
            $count++;
            if($count!=2) continue;
           if (is_array($arg)) {
               foreach ($arg as $key => $value) {
                   $arr[] = $value;
                   // $arr[] = $value;
                   $ret++;
               }
           }else{
               $arr[$arg] = "";
           }
       }
       return $ret;
    }
	
	
	public static function getEbayProfileData($siteID, $s_endpoint, $responseEncoding, $s_version, $appID, $debug,$sellerID) 
    {
	
	
 
    $results = '';

    $apicall = "$s_endpoint?callname=GetUserProfile"
		   . "&version=$s_version"
		   . "&siteid=$siteID"
		   . "&appid=$appID"
		   . "&UserID=$sellerID"
		   . "&IncludeSelector=Details,FeedbackHistory"   // need Details to get MyWorld info
		   . "&responseencoding=$responseEncoding";


   // if ($debug) { print "<br />GetUserProfile call = <blockquote>$apicall </blockquote>"; }

    // Load the call and capture the document returned by the Shopping API
    $resp = simplexml_load_file($apicall);

  
	if ($resp) {
        if (!empty($resp->User->MyWorldLargeImage)) {
            $myWorldImgURL = $resp->User->MyWorldLargeImage;
        } else {
            $myWorldImgURL = 'http://pics.ebaystatic.com/aw/pics/community/myWorld/imgBuddyBig1.gif';
        }
	
    $results .= '<table id="example" class="tablesorter" border="0" cellpadding="0" cellspacing="1">' . "";
   
        if (!empty($resp->User->MyWorldLargeImage)) {
            $myWorldImgURL = $resp->User->MyWorldLargeImage;
        } else {
            $myWorldImgURL = 'http://pics.ebaystatic.com/aw/pics/community/myWorld/imgBuddyBig1.gif';
        }
		 
        $results .= "<table><tr>";
        $results .= "<td><a href=\"" . $resp->User->MyWorldURL . "\"><img src=\""
                  . $myWorldImgURL . "\"></a></td>";
        $results .= "<td>Seller : $sellerID <br /> ";
        $results .= "Feedback score : " . $resp->User->FeedbackScore . "<br />";
        $posCount = $resp->FeedbackHistory->UniquePositiveFeedbackCount;
        $negCount = $resp->FeedbackHistory->UniqueNegativeFeedbackCount;
		if($posCount==0)
		  $posCount=1;
		 if ($negCount==0) 
		 $negCount=1;
        $posFeedBackPct = sprintf("%01.1f", (100 * ($posCount / ($posCount + $negCount))));
        $results .= "Positive feedback : $posFeedBackPct%<br />";
        $regDate = substr($resp->User->RegistrationDate, 0, 10);
        $results .= "Registration date : $regDate<br />";
        $results .= "</tr></table>";

    } else {
        $results = "<h3>No user profile for seller $sellerID";
    }
    return $results;
		 
		 	
	}
	
	
	 public static function getNbItems($globalID, $f_endpoint, $responseEncoding, $f_version, $appID, $debug,$sellerID,$itemtype,$itemsort) 
    {
	$maxEntries = 100;

  $itemType  = urlencode (utf8_encode($itemtype));
  $itemSort  = urlencode (utf8_encode($itemsort));

  // Construct the FindItems call
   $apicall = "$f_endpoint?OPERATION-NAME=findItemsAdvanced"
       . "&version=$f_version"
       . "&GLOBAL-ID=$globalID"
       . "&SECURITY-APPNAME=$appID"   // replace this with your AppID
       . "&RESPONSE-DATA-FORMAT=$responseEncoding"
       . "&itemFilter(0).name=Seller"
       . "&itemFilter(0).value=$sellerID"
       . "&itemFilter(1).name=ListingType"
       . "&itemFilter(1).value=$itemType"
       . "&paginationInput.entriesPerPage=$maxEntries"
       . "&sortOrder=$itemSort"
       . "&affliate.networkId=9"        // fill in your information in next 3 lines
       . "&affliate.trackingId=123456789"
       . "&affliate.customId=456";

  
  // Load the call and capture the document returned by the Finding API
  $resp = simplexml_load_file($apicall);
$results='';
  // Check to see if the response was loaded, else print an error
  if ($resp->ack == "Success") {
 $results .= $resp->paginationOutput->totalEntries;
	
	}
	return intval($results);
	}
	
    public static function getEbayProductData($globalID, $f_endpoint, $responseEncoding, $f_version, $appID, $debug,$sellerID,$itemtype,$itemsort,$nbitems) 
    {
         $resultFinalArray = array();
		
  $nbProducts = $nbitems;
$n = ceil($nbProducts/100);
for ($i=1; $i<=$n; $i++) {
  
  $itemType  = urlencode (utf8_encode($itemtype));
  $itemSort  = urlencode (utf8_encode($itemsort));

  // Construct the FindItems call
   $apicall = "$f_endpoint?OPERATION-NAME=findItemsAdvanced"
       . "&version=$f_version"
       . "&GLOBAL-ID=$globalID"
       . "&SECURITY-APPNAME=$appID"   // replace this with your AppID
       . "&RESPONSE-DATA-FORMAT=$responseEncoding"
       . "&itemFilter(0).name=Seller"
       . "&itemFilter(0).value=$sellerID"
       . "&itemFilter(1).name=ListingType"
       . "&itemFilter(1).value=$itemType"
       . "&paginationInput.entriesPerPage=100"
       . "&sortOrder=$itemSort"
       . "&affliate.networkId=9"        // fill in your information in next 3 lines
       . "&affliate.trackingId=123456789"
       . "&affliate.customId=456"
	   ."&paginationInput.pageNumber=$i";
       

  
  // Load the call and capture the document returned by the Finding API
  $resp = simplexml_load_file($apicall);

  // Check to see if the response was loaded, else print an error
  if ($resp->ack == "Success") {
 
    // If the response was loaded, parse it and build links
	//$totalItems=array('totalitems'=>$resp->paginationOutput->totalEntries); 
    foreach($resp->searchResult->item as $item) {
	    $resultFinal = array('image'=>'n/a','productid'=>'n/a','label'=>'n/a' ,'link'=>'n/a','price'=>'n/a','title'=>'n/a', 'shipping'=>'n/a', 'total'=>'n/a', 'timeleft'=>'n/a','endtime'=>'n/a');
				
      if ($item->galleryURL) {
        $resultFinal['image'] = $item->galleryURL;
      } else {
        $resultFinal['image']= "http://pics.ebaystatic.com/aw/pics/express/icons/iconPlaceholder_96x96.gif";
      }
      $resultFinal['link']  = $item->viewItemURL;
	   $resultFinal['title'] = $item->title;
       $resultFinal['productid'] = $item->itemId;
    
	
	
       $resultFinal['price'] = sprintf("%01.2f", $item->sellingStatus->convertedCurrentPrice);
       $resultFinal['shipping']  = sprintf("%01.2f", $item->shippingInfo->shippingServiceCost);
       $resultFinal['total'] = sprintf("%01.2f", ((float)$item->sellingStatus->convertedCurrentPrice+ (float)$item->shippingInfo->shippingServiceCost));
        /*
        // Determine currency to display - so far only seen cases where priceCurr = shipCurr, but may be others
        $priceCurr = (string) $item->sellingStatus->convertedCurrentPrice['currencyId'];
        $shipCurr  = (string) $item->shippingInfo->shippingServiceCost['currencyId'];
        if ($priceCurr == $shipCurr) {
          $curr = $priceCurr;
        } else {
          $curr = "$priceCurr / $shipCurr";  // potential case where price/ship currencies differ
        }
       */
       $resultFinal['timeleft'] = getPrettyTimeFromEbayTime($item->sellingStatus->timeLeft);
       $endTime = strtotime($item->listingInfo->endTime);   // returns Epoch seconds
       $resultFinal['endtime'] = $item->listingInfo->endTime;
	  
       $resultFinalArray[] = $resultFinal;
    }
	//  $resultFinalArray[]=$totalItems['totalitems'];
  }
  }
 
  
 return  $resultFinalArray;
  }
    
	public static function getformatEbayProductData($getSearchPageData)
    {
        $result = array("aaData" => '[ ');	
        foreach($getSearchPageData as $item ) {
            $row = ''; 
			 $row .= '["'.$item["productid"].'", ';
            $row .= $item["image"]=="n/a" ? '"'.$item["image"].'", ' : ' "<a target=\'_blank\' href=\''.$item["link"].'\'><img width=\'80\' height=\'80\' src=\''.$item["image"].'\'></a>", ';
            $row .='"'.str_replace('"', '\"', $item["title"]).'", ';
			$row .='"'.$item["price"].'", ';
            /*$row .='"'.$item["shipping"].'", ';
            $row .='"'.$item["total"].'", ';
            $row .='"'.$item["timeleft"].'", ';
            $row .='"'.$item["endtime"].'" ], ';
			*/
			$row .='"'.$item["label"].'"], ';
            $result["aaData"] .= $row;
        }
        $result["aaData"] .= ' ]';
        
        return $result;
    }
  
}
