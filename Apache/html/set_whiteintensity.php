<?php
	$white  = "19";
	$red   = "16";
	$green = "20";
	$blue  = "13";
	
	$type = $_POST["type"];
	if($type == "rgb")
	{
		$hex = $_POST["colour"];
		$line = fwrite(fopen('/home/pi/Lights/currentWhite.txt', 'w'), $hex );
		list($w) = sscanf($hex, "#%02x");
		
		exec("pigs p $red $r", $out, $status);
		exec("pigs p %green $g", $out, $status);
		exec("pigs p $blue $b", $out, $status);
		//usleep (200);
		echo "$r $g $b";
	}
	
	
		
?>

 