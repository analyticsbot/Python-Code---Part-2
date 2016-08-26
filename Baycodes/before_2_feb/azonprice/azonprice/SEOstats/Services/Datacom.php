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

class Datacom extends SEOstats
{
    function gMultiCurl($urlsArray)
    {
        $ua = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0";
        // build the requests
        $ch = array();
        $mh = curl_multi_init();
		$proxyfile = dirname(__FILE__)."/../pro/pro.txt";
		 $file = fopen($proxyfile, "r");
        $i = 0;
        while (!feof($file)) {
       $proxies_array[] = fgets($file);
   }
      fclose($file); 
        for ($i = 0; $i < count($urlsArray); $i++) {    
            $ch[$i] = curl_init($urlsArray[$i]);
            curl_setopt($ch[$i], CURLOPT_SSL_VERIFYPEER, 0);
            curl_setopt($ch[$i], CURLOPT_FOLLOWLOCATION, 1);
            curl_setopt($ch[$i], CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch[$i], CURLOPT_SSL_VERIFYHOST, 0);
            curl_setopt($ch[$i], CURLOPT_MAXREDIRS, 20 );
			curl_setopt($ch[$i], CURLOPT_HTTPHEADER, array("X-Requested-With: XMLHttpRequest"));
            curl_setopt($ch[$i], CURLOPT_COOKIESESSION, true );
            curl_setopt($ch[$i], CURLOPT_COOKIEFILE, dirname(__FILE__) . '/cookie.txt');
            curl_setopt($ch[$i], CURLOPT_COOKIEJAR, dirname(__FILE__) . '/cookie.txt');
            curl_setopt($ch[$i], CURLOPT_HEADER, 0);
            curl_setopt($ch[$i], CURLOPT_USERAGENT, $ua);
       
      $random_key   = array_rand($proxies_array);
$random_proxy   = $proxies_array[$random_key];
$random_proxy   = trim(str_replace("<br />","",$random_proxy)); 
   $new_proxy = explode(":", $random_proxy);  
  $loginpassw = $new_proxy[2].":".$new_proxy[3];
   curl_setopt($ch[$i], CURLOPT_PROXY, $random_proxy);
			
            curl_multi_add_handle($mh, $ch[$i]);
        }
         // execute the requests simultaneously
        $running = 0;
        do {
            curl_multi_exec($mh, $running);
        } while ($running > 0);
        $results = array();
        for ($i = 0; $i < count($urlsArray); $i++) {
            $results[] =curl_multi_getcontent($ch[$i]);
        }
		usleep(100000);
        return $results;
    }
	 
	function getPageData($url, $useCookies=false) 
    {
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, FALSE);
        curl_setopt($curl, CURLOPT_HEADER, false);
        curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($curl, CURLOPT_MAXREDIRS, 20 );
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_REFERER, $url);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, TRUE);
		
		
        if($useCookies) {
            curl_setopt($curl, CURLOPT_HTTPHEADER, array("X-Requested-With: XMLHttpRequest"));
            curl_setopt($curl, CURLOPT_COOKIESESSION, true );
            curl_setopt($curl, CURLOPT_COOKIEFILE, dirname(__FILE__) . '/cookie.txt');
            curl_setopt($curl, CURLOPT_COOKIEJAR, dirname(__FILE__) . '/cookie.txt');
        }
        $ua = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0";
        if (isset($_SERVER["HTTP_USER_AGENT"]) && 0 < strlen($_SERVER["HTTP_USER_AGENT"])) {
            $ua = $_SERVER["HTTP_USER_AGENT"];
        }
        curl_setopt($curl, CURLOPT_USERAGENT, $ua);
        curl_setopt($curl, CURLOPT_MAXREDIRS, 20 );
		
        $str = curl_exec($curl);
       $info = curl_getinfo($curl);
        curl_close($curl);
      return ($info['http_code']!=200) ? false : $str; 
       
    }
	
	
}
