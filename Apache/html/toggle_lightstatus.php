<?php
	$white  = "19";
	$red   = "16";
	$green = "20";
	$blue  = "13";
	
	$light_set = $_POST["type"];
	
	$mode = $_POST["mode"];
	//$line = fwrite(fopen('/home/pi/Lights/currentColour.txt', 'w'), $colour );
	//

	
	if(strtolower($light_set) == "override")
	{
		if($mode == "true")
		{
			echo "setting override";
			$file = fopen("/home/pi/Lights/lightStatusOverride.txt","w");
			fwrite($file,"1");
			fclose($file);
		}
		else
		{
			$file = fopen("/home/pi/Lights/lightStatusOverride.txt","w");
			fwrite($file,"0");
			fclose($file);
			$file = fopen("/home/pi/Lights/lightStatusRGB.txt","w");
			fwrite($file,"0");
			fclose($file);
			$file = fopen("/home/pi/LightslightStatusRGBW.txt","w");
			fwrite($file,"0");
			fclose($file);
			
			//run the python to restart
			echo "setting autolights";
			exec("python /home/pi/Lights/autolights.py reboot > /dev/null 2>/dev/null &", $out, $status);
		}
	
	}
	else
	{
		switch (strtolower($light_set)) {
		case "rgb":
			$lightstatus = fgets(fopen('/home/pi/Lights/lightStatusRGB.txt', 'r'));
			if($lightstatus === "1") { 
				exec("pigs p $red 0", $out, $status); 
				exec("pigs p $green 0", $out, $status); 
				exec("pigs p $blue 0", $out, $status); 
				fwrite(fopen('/home/pi/Lights/lightStatusRGB.txt', 'w'), "0" );
			}
			else {
				$hex = fgets(fopen('/home/pi/Lights/currentColour.txt', 'r'));
				list($r, $g, $b) = sscanf($hex, "#%02x%02x%02x");
				exec("pigs p $red $r", $out, $status);
				exec("pigs p $green $g", $out, $status);
				exec("pigs p $blue $b", $out, $status);
				fwrite(fopen('/home/pi/Lights/lightStatusRGB.txt', 'w'), "1" );
				
			}
			break;
		case "rgbw":
			$lightstatus = fgets(fopen('/home/pi/Lights/lightStatusRGBW.txt', 'r'));
			if($lightstatus === "1") { 
				exec("pigs p $white 0", $out, $status); 
				fwrite(fopen('/home/pi/Lights/lightStatusRGBW.txt', 'w'), "0" );
			}
			else {
				$hex = fgets(fopen('/home/pi/Lights/currentWhite.txt', 'r'));
				list($w) = sscanf($hex, "#%02x");
				exec("pigs p $white $w", $out, $status);
				fwrite(fopen('/home/pi/Lights/lightStatusRGBW.txt', 'w'), "1" );
			}
			break;
		
		case "storm":
			$lightstatus = fgets(fopen('/home/pi/Lights/stormStatus.txt', 'r'));
			if($lightstatus === "1") { 
				fwrite(fopen('/home/pi/Lights/stormStatus.txt', 'w'), "0" );
			}
			else {
				fwrite(fopen('/home/pi/Lights/stormStatus.txt', 'w'), "1" );
				
				$file = fopen("/home/pi/Lights/lightStatusRGB.txt","w");
				fwrite($file,"0");
				fclose($file);
				$file = fopen("/home/pi/Lights/lightStatusRGBW.txt","w");
				fwrite($file,"0");
				fclose($file);
			}
			break;
		}
	}
	
	//return array('r' => $r * 255.0, 'g' => $g * 255.0, 'b' => $b * 255.0);
?>

 