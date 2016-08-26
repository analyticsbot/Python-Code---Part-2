<html>
    <body>
    <p id="f1_upload_process">Loading...<br/><img src="loader.gif" /></p>
    <p id="result"></p>
    <form action="upload.php" method="post" enctype="multipart/form-data" target="upload_target" onsubmit="startUpload();" >
    File: <input name="myfile" type="file" />
    <input type="submit" name="submitBtn" value="Upload" />
    </form>
     
    <iframe id="upload_target" name="upload_target" src="#" style="width:0;height:0;border:0px solid #fff;"></iframe>
    <script>
	    function startUpload(){
    document.getElementById('f1_upload_process').style.visibility = 'visible';
    return true;
    }
	    function stopUpload(success){
    var result = '';
    if (success == 1){
    document.getElementById('result').innerHTML =
    '<span class="msg">The file was uploaded successfully!<\/span><br/><br/>';
    }
    else {
    document.getElementById('result').innerHTML =
    '<span class="emsg">There was an error during file upload!<\/span><br/><br/>';
    }
    document.getElementById('f1_upload_process').style.visibility = 'hidden';
    return true;
    }
	
	</script>
	<?php
$destination_path = getcwd().DIRECTORY_SEPARATOR;
 
$result = 0;
 
$target_path = $destination_path . basename( $_FILES['myfile']['name']);
 
if(@move_uploaded_file($_FILES['myfile']['tmp_name'], $target_path)) {
$result = 1;
}
 
sleep(1);
?>
	
	</body>
</html>	