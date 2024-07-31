import MySQLdb
def application(environ, start_response):
    status = '200 OK'
    output = '<html><head><title>Sample Python Script</title></head>\n'

    # connect
    dbcnx = MySQLdb.connect(host="dbdev.cs.uiowa.edu",port=3306,user="itphillips",passwd="ywY2GDbRZNUg8g0",db="db_itphillips")
   
    sqlquery="""SELECT * FROM shop;"""
   
    # create a database cursor
    cursor = dbcnx.cursor()
   
    # execute SQL select 
    cursor.execute(sqlquery)
    
    output += "<h2> %s </h2>"
    output %= sqlquery
    output += "<table><tr><th>id</th><th>name</th><th>price</th></tr>\n"
   
    # get the number of rows in the resultset
    numrows = int(cursor.rowcount)
   
    # get and display one row at a time
    for x in range(0,numrows):
       row = cursor.fetchone()
       output += "<tr><td> %s </td>\n"
       output %= row[0]
       output += "    <td> %s </td>\n"
       output %= row[1]
       output += "    <td> %s </td></tr>\n"
       output %= row[2]
   
    output += "</table>\n"
    output += "</body></html>\n"
    cursor.close ()
    dbcnx.close ()

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]
