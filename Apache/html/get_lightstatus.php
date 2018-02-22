<?php
	//returns all the lights status in an echo seperated by commas
	// tank,rgb,rgbw
	$statusMain = fgets(fopen('/home/pi/Lights/lightStatusMain.txt', 'r'));
	$statusRGB = fgets(fopen('/home/pi/Lights/lightStatusRGB.txt', 'r'));
	$statusRGBW = fgets(fopen('/home/pi/Lights/lightStatusRGBW.txt', 'r'));
	$statusOverride = fgets(fopen('/home/pi/Lights/lightStatusOverride.txt', 'r'));
	$stormStatus = fgets(fopen('/home/pi/Lights/stormStatus.txt', 'r'));
	echo "$statusMain,$statusRGB,$statusRGBW,$statusOverride,$stormStatus";
?>