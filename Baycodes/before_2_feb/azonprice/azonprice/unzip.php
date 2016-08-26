<?php
$zip = new ZipArchive;
$file = $_GET['file'];
$to = $_GET['to'];
$res = $zip->open($file);
if ($res === TRUE) {
  $zip->extractTo($to);
  $zip->close();
  echo 'Complete!';
} else {
  echo 'False!';
}
?>