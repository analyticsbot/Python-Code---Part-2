<?php 
include('config.inc.php');

$asin=$_POST['asin'];
$cost=$_POST['cost'];

$res=$connexion->query("select * from searchproduct where asin='".$asin."'");
while($row1 = $res->fetch( PDO::FETCH_ASSOC)) {
$payout=$row1['price']*0.85;   
$roi=($payout-$cost)/$cost;
$roi=number_format((float)$roi, 2, '.', '');
$payout=number_format((float)$payout, 2, '.', '');
//echo "UPDATE searchproduct set cost=".$cost.",payout=".$payout.",roi=".$roi." where asin='".$asin."'";die;
$connexion->exec("UPDATE searchproduct set cost=".$cost.",payout=".$payout.",roi=".$roi." where asin='".$asin."'");
 }
 $result = array("state"=>"Ok", "data"=>'');
	 echo json_encode($result);

?>