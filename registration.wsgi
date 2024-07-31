import MySQLdb
def application(environ, start_response):
    status = '200 OK'

    # works as the config php
    db=MySQLdb.connect(host = 'dbdev.cs.uiowa.edu',
    user = 'itphillips',
    passwd = 'ywY2GDbRZNUg8g0',
    db='db_itphillips')

    # define the SQL query
    #sqlquery="""SELECT * FROM user;"""

    # create a cursor
    cur = db.cursor()

    username = " "
    firstname = " "
    lastname = " "
    email = " "
    password = " "

    output += '''
    <!DOCTYPE html>
    <html>
    <head>
	    <title>User Registration | PHP</title>
	    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
    </head>
    <body>
<!--
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
            -->
    </div>
    <!--Asking for input for user database -->
    <div>
	    <form action="registration.php" method="post">
		    <div class="container">
			
			    <div class="row">
				    <div class="col-md-12">
					    <h1>Registration</h1>
					    <p>Fill up the form with correct values.</p>
					    <hr class="mb-3">
					    <label for="firstname"><b>First Name</b></label>
					    <input class="form-control" id="firstname" type="text" name="firstname" required>

					    <label for="lastname"><b>Last Name</b></label>
					    <input class="form-control" id="lastname"  type="text" name="lastname" required>

					    <label for="email"><b>Email Address</b></label>
					    <input class="form-control" id="email"  type="email" name="email" required>

					    <label for="phonenumber"><b>Phone Number</b></label>
					    <input class="form-control" id="phonenumber"  type="text" name="phonenumber" required>

					    <label for="password"><b>Password</b></label>
					    <input class="form-control" id="password"  type="password" name="password" required>
					    <hr class="mb-3">
					    <input class="btn btn-primary" type="submit" id="register" name="create" value="Sign Up">
				    </div>
			    </div>
		    </div>
	    </form>
    </div>
    <!-- google sign in 
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@8"></script>
    -->
    </body>
    </html>
    '''


    sql = "INSERT INTO user (firstname, lastname, email, phonenumber, password) VALUES (?, ?, ?, ?, ?)";


    cur.execute(sql, (username, firstname, lastname, email, password))
            
    # Commit the changes to the database
    db.commit()

    # Close the database connection
    db.close()


    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
