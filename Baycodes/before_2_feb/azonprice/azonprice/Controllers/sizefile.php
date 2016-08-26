<?php 
require_once (__DIR__ . '/..') . '/Services/parsecsv.lib.php';

require_once (__DIR__ . '/..') . '/Services/Excel/reader.php';

 if(isset($_POST['upfile'])&&$_POST['upfile']!="") {

         $allowedExts = array("csv", "xls");
        $temp = explode(".",$_POST['upfile']);
        $extension = end($temp);
		  if($extension=="xls") {

                $data = new Spreadsheet_Excel_Reader();
                $data->setOutputEncoding('CP1251');
                $data->read('../assets/uploads/'.$_POST['upfile']);
      $result = array("state"=>"Ok", "data"=>$data->sheets[0]['numRows']);
	   echo json_encode($result);
	   
	   
	   }
	   }
?>