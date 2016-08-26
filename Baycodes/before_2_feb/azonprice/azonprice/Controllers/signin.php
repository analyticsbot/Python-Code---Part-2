<?php
 $itemid='B002DQLGHU';
$query = array( 'Operation'     =>'ItemLookup', 
                'ResponseGroup' =>'ItemAttributes',
                'Condition'   =>'All',
				'IdType'=>'ASIN',
				'ItemId'=>$itemid,
                 );
$signed_url = sign_query($query);
 echo $signed_url;die; 
/* Use CURL to retrieve the data so that http errors can be examined */
$ch = curl_init($signed_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 7);
$xml_string = curl_exec($ch);
$curl_info = curl_getinfo($ch);
curl_close($ch);
 
if($curl_info['http_code']==200) {
    $xml_obj = simplexml_load_string($xml_string);
}
else {
    /* examine the $curl_info to discover why AWS returned an error 
       $xml_string may still contain valid XML, and may include an
       informative error message */
}
 
 
 
 
 
function sign_query($parameters) {
    //sanity check
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
        $encoded_values['Timestamp'] = 'Timestamp=2014-08-25T18%3A01%3A21.000Z';
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
    return $url;
}
?>