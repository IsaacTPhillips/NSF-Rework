import MySQLdb

def application(environ, start_response):
    status = '200 OK'
    output = '<html>\n'
    output += '<head>\n'
    #title
    output += '<title>Weather Report</title>\n'
    #styling
    output += '<style>\n'
    output += 'body {\n'
    output += '    margin: 0;\n'
    output += '}\n'
    #sidebar creation
    output += '#sidebar {\n'
    output += '    height: 100%;\n'
    output += '    width: 200px;\n'
    output += '    position: fixed;\n'
    output += '    z-index: 1;\n'
    output += '    top: 0;\n'
    output += '    left: 0;\n'
    output += '    background-color: #1E1E1E;\n'
    output += '    overflow-x: hidden;\n'
    output += '    padding-top: 20px;\n'
    output += '}\n'
    #sidebar styling
    output += '#sidebar a {\n'
    output += '    padding: 6px 8px 6px 16px;\n'
    output += '    text-decoration: none;\n'
    output += '    font-size: 20px;\n'
    output += '    color: #818181;\n'
    output += '    display: block;\n'
    output += '}\n'
    #sidebar hover color
    output += '#sidebar a:hover {\n'
    output += '    color: #f1f1f1;\n'
    output += '}\n'
    output += '#sidebar h3 {\n'
    output += '    color: #f1f1f1;\n'
    output += '    padding: 10px 10px 10px 16px;\n'
    output += '}\n'
    #top of page navbar creation
    output += '#topbar {\n'
    output += '    height: 50px;\n'
    output += '    width: 100%;\n'
    output += '    position: fixed;\n'
    output += '    z-index: 1;\n'
    output += '    top: 0;\n'
    output += '    left: 200px;\n'
    output += '    background-color: #4CAF50;\n'
    output += '    overflow-x: hidden;\n'
    output += '    padding-top: 10px;\n'
    output += '}\n'
    #top of page navbar styling
    output += '#topbar select {\n'
    output += '    font-size: 20px;\n'
    output += '    padding: 6px 10px;\n'
    output += '    margin: 0 10px;\n'
    output += '    border: none;\n'
    output += '    border-radius: 4px;\n'
    output += '}\n'

    output += '#topbar {\n'
    output += '  display: flex;\n'
    output += '  justify-content: space-evenly;\n'
    output += '}\n'

    output += 'button {\n'
    output += '  margin: 0 10px;\n'
    output += '}\n'

    output += '#content {\n'
    output += '    margin-left: 200px;\n'
    output += '    padding: 20px;\n'
    output += '}\n'

    output += '</style>\n'
    output += '</head>\n'

    output += '<body>\n'
    output += '<div id="sidebar">\n'
    output += '<h3>Select an option:</h3>\n'
    output += '<div class="section">\n'
    output += '<a href="#">Option 1</a>\n'
    output += '<a href="#">Option 2</a>\n'
    output += '<a href="#">Option 3</a>\n'
    output += '</div>\n'
    output += '</div>\n'
    
    output += '<div id="topbar">\n'
    #buttons
    output += '<button id="button1" type="button">Data table</button>\n'
    output += '<button id="button2" type="button">Button 2</button>\n'
    output += '<button id="button3" type="button">Button 3</button>\n'
    output += '<button id="button4" type="button">Button 4</button>\n'
    output += '<button id="button5" type="button">Button 5</button>\n'
    output += '</div>\n'

    #scroll wheel for table
    output += '<script>'
    output += 'table {'
    output += 'display: block;'
    output += 'max-width: -moz-fit-content;'
    output += 'max-width: fit-content;'
    output += 'margin: 0 auto;'
    output += 'overflow-x: auto;'
    output += 'white-space: nowrap;'
    output += '}'
    output += '</script>'
    
    # connect to the database
    dbcnx = MySQLdb.connect(host="dbdev.cs.uiowa.edu", port=3306, user="itphillips", passwd="ywY2GbRZNUg8g0", db="db_itphillips")

    # define the SQL query
    sqlquery="""SELECT * FROM tendayweather;"""

    # create a cursor
    cursor = dbcnx.cursor()

    # execute the SQL query
    cursor.execute(sqlquery)

    # start building the output
    output += '<div id="sidebar">'
    output += '<h2 style="color: white;">Search our Database:</h2>'
    output += '<input type="text" id="searchbox" placeholder="Enter search term">'
    output += '</div>'

    # add the JavaScript for the search box
    output += '<script>'
    output += 'document.getElementById("searchbox").addEventListener("input", function() {'
    output += 'var searchterm = this.value;'
    output += 'var rows = document.getElementsByTagName("tr");'
    output += 'for (var i = 0; i < rows.length; i++) {'
    output += 'var cells = rows[i].getElementsByTagName("td");'
    output += 'var match = false;'
    output += 'for (var j = 0; j < cells.length; j++) {'
    output += 'if (cells[j].textContent.toUpperCase().includes(searchterm.toUpperCase())) {'
    output += 'match = true;'
    output += 'break;'
    output += '}'
    output += '}'
    output += 'if (match) {'
    output += 'rows[i].style.display = "";'
    output += '} else {'
    output += 'rows[i].style.display = "none";'
    output += '}'
    output += '}'
    output += '});'
    output += '</script>'



    output += '<div id="main">'
    output += '<h1>10-day Weather Report for Iowa City</h1>'
    output += '<center><table border="1" style="width:75%; margin-left: 50px">\n'
    output += '<tr><th>Date</th><th>High</th><th>Low</th><th>Forecast</th><th>Rain</th><th>Wind</th></tr>'

    # get the number of rows in the resultset
    numrows = int(cursor.rowcount)

    # get and display one row at a time
    for x in range(0, numrows):
        row = cursor.fetchone()
        output += '<tr><td> %s </td>' % row[1]
        output += '<td> %s </td>' % row[2]
        output += '<td> %s </td>' % row[3]
        output += '<td> %s </td>' % row[4]
        output += '<td> %s </td>' % row[5]
        output += '<td> %s </td></tr>' % row[6]

    output += '</table>'
    output += '</div>'

    # close the cursor and database connection
    cursor.close()
    dbcnx.close()

    output += '</body></html>'

    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]
