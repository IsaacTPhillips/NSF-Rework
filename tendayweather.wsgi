import MySQLdb
def application(environ, start_response):
    status = '200 OK'
    output = '<html><head><title>Sample Python Script</title></head>\n'
    
    # connect
    dbcnx = MySQLdb.connect(host="dbdev.cs.uiowa.edu",port=3306,user="itphillips",passwd="ywY2GDbRZNUg8g0",db="db_itphillips")
   
    sqlquery="""SELECT * FROM tendayweather;"""
   
    # create a database cursor
    cursor = dbcnx.cursor()
   
    # execute SQL select 
    cursor.execute(sqlquery)
    
    #Link to other page
    output += "<h3>Click Me!</h3>"
    output = '<a href = "https://webdev.divms.uiowa.edu/~itphillips/cs3910/hw1/hourlyweather.wsgi"><img alt = "WeatehrPic2" src = "WeatherPic2.png" width = "100" height = "100"></a>'
   
    output += "<h2> %s </h2>"
    output %= sqlquery
    output += "<body style = background-color:lightblue;></body>"
    output += "<table style = background-color:blue;><tr><th>Weekday</th><th>Date</th><th>High</th><th>Low</th><th>Forecast</th><th>Rain</th><th>Wind</th></tr>\n"
   
    # get the number of rows in the resultset
    numrows = int(cursor.rowcount)
    
  
    
    # get and display one row at a time
    for x in range(0,numrows):
       row = cursor.fetchone()
       output += "<tr><td> %s </td>\n"
       output %= row[0]
       output += "    <td> %s </td>\n"
       output %= row[1]
       output += "    <td> %s </td>\n"
       output %= row[2]
       output += "    <td> %s </td>\n"
       output %= row[3]
       output += "    <td> %s </td>\n"
       output %= row[4]
       output += "    <td> %s </td>\n"
       output %= row[5]
       output += "    <td> %s </td>\n"
       output %= row[6]
       output += "    <td> %s </td>\n"
       output %= row[7]
       output += "    <td> %s </td>\n"
       output %= row[8]
       output += "    <td> %s </td>\n"
       output %= row[9]
       output += "    <td> %s </td>\n"
       output %= row[10]
       output += "    <td> %s </td>\n"
       output %= row[11]
       output += "    <td> %s </td>\n"
       output %= row[12]
       output += "    <td> %s </td>\n"
       output %= row[13]
       output += "    <td> %s </td>\n"
       output %= row[14]
       output += "    <td> %s </td>\n"
       output %= row[15]
       output += "    <td> %s </td>\n"
       output %= row[16]
       output += "    <td> %s </td>\n"
       output %= row[17]
       output += "    <td> %s </td>\n"
       output %= row[18]
       output += "    <td> %s </td></tr>\n"
       output %= row[19]
      
   
    output += "</table>\n"
    #output = '<button type = "button" onclick = "document.getElementById('myH3').style.color = 'red'">Click Me!</button>'


    
    output += "</body></html>\n"
    cursor.close ()
    dbcnx.close ()

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]
