<?php
	exec('/usr/bin/python /home/pi/TemperatureSensor/get_smsstatus.py', $out, $status);
	echo $out[0];
?>

 