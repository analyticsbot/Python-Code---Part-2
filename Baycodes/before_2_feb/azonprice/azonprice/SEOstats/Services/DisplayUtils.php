<?php
date_default_timezone_set('GMT');

function getPrettyTimeFromEbayTime($eBayTimeString){
    // Input is of form 'PT12M25S'
    $matchAry = array(); // initialize array which will be filled in preg_match
    $pattern = "#P([0-9]{0,3}D)?T([0-9]?[0-9]H)?([0-9]?[0-9]M)?([0-9]?[0-9]S)#msiU";
    preg_match($pattern, $eBayTimeString, $matchAry);

    $days  = (int) $matchAry[1];
    $hours = (int) $matchAry[2];
    $min   = (int) $matchAry[3];    // $matchAry[3] is of form 55M - cast to int
    $sec   = (int) $matchAry[4];

    $retnStr = '';
    if ($days)  { $retnStr .= "$days day"    . pluralS($days);  }
    if ($hours) { $retnStr .= " $hours hour" . pluralS($hours); }
    if ($min)   { $retnStr .= " $min minute" . pluralS($min);   }
    if ($sec)   { $retnStr .= " $sec second" . pluralS($sec);   }

    return $retnStr;
} // function

function pluralS($intIn) {
    // if $intIn > 1 return an 's', else return null string
    if ($intIn > 1) {
        return 's';
    } else {
        return '';
    }
} // function


?>
