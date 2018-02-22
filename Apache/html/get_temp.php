<?php
	$columnName = $_GET["temperatureProbe"];
	$query = "SELECT time, $columnName FROM temps WHERE id=( SELECT max(id) FROM temps )";
	
	$mysqliDebug = true;
	$mysqli = @new mysqli('localhost', 'mysql-read', 'password', 'temperature_readings');

	// mysqli->connect_errno will return zero if successful
	if ($mysqli->connect_errno) {
		echo '<p>There was an error connecting to the database!</p>';
		if ($mysqliDebug) {
			// mysqli->connect_error returns the latest error message,
			echo $mysqli->connect_error;
		}
		die();
	}

	// Fetch the data
	$result = $mysqli->query( $query );
	$row = mysql_fetch_assoc($result);
		
	// Close the connection
	mysqli_close($mysqli);

	// All good?
	if ( !$result ) {
	  // Nope
	  $message  = 'Invalid query: ' . $mysqli->error . "\n";
	  $message .= 'Whole query: ' . $query;
	  die( $message );
	}
	
	// Print out rows
	$data = array();
	while ( $row = $result->fetch_assoc() ) {
	  $data[] = $row;
	}
	
	echo json_encode( $data );

?>

 