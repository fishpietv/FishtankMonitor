<?php
	exec('/usr/bin/python /home/pi/TemperatureSensor/toggle_smsstatus.py', $out, $status);
	echo $out[0];
?>

 