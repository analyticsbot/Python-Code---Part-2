<?php 

include('config.inc.php');
$res=$connexion->query("select * from setting");
        if($res->fetchColumn()==0)
        {
            $connexion->exec("INSERT INTO setting(`awsaccesskey`, `secretkey`, `sellerid`, `marketplaceid`) values('".$_POST['awsaccesskeyid']."','".$_POST['secretkey']."','".$_POST['sellerid']."')");
        }
		else {
		    $connexion->exec("update setting set `awsaccesskey`='".$_POST['awsaccesskeyid']."', `secretkey`='".$_POST['secretkey']."', `sellerid`='".$_POST['sellerid']."', `marketplaceid`='".$_POST['marketplaceid']."'");
       
		}
    $result = array("state"=>"Ok", "data"=> '');
echo json_encode($result);
  


?>