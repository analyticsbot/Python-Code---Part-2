<?php 
$data=(string)file_get_contents("productexport.txt");
echo $data;die;
 $ndata=preg_split("/[\s]+/",$data)
 ;
print_r($ndata);
 

?>   