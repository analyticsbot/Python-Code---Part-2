<?php

include('config.inc.php');

$connexion->exec('TRUNCATE TABLE azon_products');
$result = array("state"=>"Ok", "data"=>'');
	 echo json_encode($result);

?>