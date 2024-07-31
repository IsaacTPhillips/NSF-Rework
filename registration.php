<?php
require_once('config.php');
?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Sign Up</title>
		<link rel="stylesheet" type = "text/css" href="css/bootstrap.min.css">
	</head>
    <nav>
        <ul>
          <li><a href='Page1.html'>Home Page</a></li>
          <li><a href='index.html'>Active</a>
          <li><a href='tendayweather.wsgi'>Search</a></li>
          <li><a href='test.wsgi'>Map</a></li>
          <li><a href='ContactUs.html'>Contact Us</a></li>
        </ul>
    </nav>
	<body>
    <div>
            <?php
            if(isset($_POST['create'])){
                $username       = $_POST['username'];
                $firstname      = $_POST['firstname'];
                $lastname       = $_POST['lastname'];
                $email          = $_POST['email'];
                $password       = $_POST['pasword'];

                echo $username + " " + $firstname + " " + $lastname + " " + $email + " " + $password;
            }
            ?>
    </div>
		<div class="signup">
			<h1>Register</h1>
			<form action="registration.php" method="post">

                <label for="username"><b class="fas fa-user"></b></label>
				<input type="text" name="username" placeholder="username" id="username" required>

                <label for="firstname"><b class="fas fa-user"></b></label>
				<input type="text" name="firstname" placeholder="firstname" id="firstname" required>

                <label for="lasname"><b class="fas fa-user"></b></label>
				<input type="text" name="lastname" placeholder="lastname" id="lastname" required>

                <label for="email"><b class="fas fa-user"></b></label>
				<input type="text" name="email" placeholder="email" id="email" required>

				<label for="password"><b class="fas fa-lock"></b></label>
				<input type="password" name="password" placeholder="password" id="password" required>

				<input class = "btn btn-primary" type="submit" name = "create" value="Signup">
			</form>
		</div>
	</body>
</html>