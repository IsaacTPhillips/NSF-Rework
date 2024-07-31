import MySQLdb
def application(environ, start_response):
    status = '200 OK'
    output = '<html><head><title>Sample Python Script</title></head>\n'
   
    # connect
    dbcnx = MySQLdb.connect(host="dbdev.cs.uiowa.edu",port=3306,user="itphillips",passwd="ywY2GDbRZNUg8g0",db="db_itphillips")
   
    sqlquery="""SELECT * FROM hourlyweather;"""
   
    # create a database cursor
    cursor = dbcnx.cursor()
   
    # execute SQL select 
    cursor.execute(sqlquery)

    #link to other page(works)
    output += "<h3>Click Me!</h3>"
    output += '<a href = "https://webdev.divms.uiowa.edu/~itphillips/cs3910/hw1/tendayweather.wsgi"><img alt = "WeatehrPic1" src = "WeatherPic1.jpeg" width = "100" height = "100"></a>'

    #output += '<button type="button" onclick= document.getElementById(H3).style.color = "lightblue";>Click Me!</button>\n'


    output += "<h2> %s </h2>"
    output %= sqlquery
    output += "<table><tr><th>Time</th><th>Temperature</th><th>Forecast</th><th>Rain</th><th>Wind</th></tr>\n"
   
    # get the number of rows in the resultset
    numrows = int(cursor.rowcount)

   
    # get and display one row at a time

    for x in range(0,numrows):
       row = cursor.fetchone()
       #output += '<div style = "position:relative; right:80px; top:2px; background-color:yellow;">'
       output += "<tr><td> %s </td>\n"
       output %= row[0]
       output += "    <td> %s </td>\n"
       output %= row[1]
       output += "    <td> %s </td>\n"
       output %= row[2]
       output += "    <td> %s </td>\n"
       output %= row[3]
       output += "    <td> %s </td></tr>\n"
       output %= row[4]
       
   
	 

    
    output += "</table>\n"

#Image(doesnt work)
   #output += '<button type="button" onclick= document.getElementById(H3).style.color = "lightblue">Click Me!</button>\n'


    output += "</body></html>\n"
    cursor.close ()
    dbcnx.close ()

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]
