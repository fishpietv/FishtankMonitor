<?php
	// Connect to MySQL
	 $mysqliDebug = true;
		
	// connect to your database
	// if you use a single database, passing it will simplify your queries
	$mysqli = @new mysqli('localhost', 'mysql-read', 'password', 'temperature_readings');

	// mysqli->connect_errno will return zero if successful
	if ($mysqli->connect_errno) {
		echo '<p>There was an error connecting to the database!</p>';
		if ($mysqliDebug) {
			// mysqli->connect_error returns the latest error message,
			// hopefully clarifying the problem
			// NOTE: supported as of PHP 5.2.9
			echo $mysqli->connect_error;
		}
		// since there is no database connection your queries will fail,
		// quit processing
		die();
	}

	// Fetch the data
	$query = "
		SELECT r.*
			FROM ( 
				SELECT tankTemp, roomTemp, time
				FROM temps
				WHERE time >= (CURDATE() - INTERVAL 30 DAY)
			) r
		CROSS
		JOIN ( SELECT @i := 0 ) s
		HAVING ( @i := @i + 1) MOD 20 = 1
	  ";
	$result = $mysqli->query( $query );
		
	// Close the connection
	mysqli_close($mysqli);

	// All good?
	if ( !$result ) {
	  // Nope
	  $message  = 'Invalid query: ' . $mysqli->error . "\n";
	  $message .= 'Whole query: ' . $query;
	  die( $message );
	}
	
	/// Print out rows
		$data = array();
		while ( $row = $result->fetch_assoc() ) {
		  $data[] = $row;
		}
		
		echo json_encode( $data );

?>