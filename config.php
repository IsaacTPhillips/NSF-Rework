<?php
define('DBSERVER', 'localhost'); // Database server
define('DBUSERNAME', 'webdev'); // Database username
define('DBPASSWORD', 'yw'); // Database password
define('DBNAME', 'itphillips'); // Database name
 
/* connect to MySQL database */
$db = mysqli_connect(DBSERVER, DBUSERNAME, DBPASSWORD, DBNAME);
 
// Check db connection
if($db === false){
    die("Error: connection error. " . mysqli_connect_error());
}
?>