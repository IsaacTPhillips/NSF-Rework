import MySQLdb
from cgi import parse_qs, escape

def makeQuery(unparsed_qs):
    
    querydict = parse_qs(unparsed_qs)
    if querydict == {}:
        return 'SELECT * FROM opList LIMIT 100'
    queryKeys = list(querydict.keys())
    if queryKeys == ['ShowNumber']:
        return 'SELECT * FROM opList LIMIT '+ querydict['ShowNumber'][0]
    query = 'SELECT * FROM opList WHERE '
    
    index = 0
    while index < len(querydict):
        i = queryKeys[index]
        
        try:
            if i == "ShowNumber":
                shownumber = querydict[i][0]
            else:
                query += i+ '=' + str(int(querydict[i][0]))
                
        except:
            query += i+ " LIKE '%" + querydict[i][0] + "%'"
        if index != len(querydict) - 1 and i!= "ShowNumber":
            query += ' AND '
        index += 1
    
    try:
        if query[-4:-1] == "AND":
            query = query[:-4]
        query += 'LIMIT ' + shownumber
        return query

    except:
        
        return query + " LIMIT 100"
def makeResultString(unparsed_qs):
    
    querydict = parse_qs(unparsed_qs)
    if querydict == {}:
        return 'Showing all results'
    queryKeys = list(querydict.keys())
    if queryKeys == ['ShowNumber']:
        return 'Showing first '+ querydict['ShowNumber'][0] + ' results'
    query = 'Showing results for '
    
    index = 0
    while index < len(querydict):
        i = queryKeys[index]
        
        try:
            if i!= 'ShowNumber':
                query += i+ '=' + str(int(querydict[i][0]))
        except:       
            query += i+ ": " + querydict[i][0]
        if index != len(querydict) - 2 and i!= "ShowNumber" and len(querydict) != 1:
            query += ', '
        index += 1
    
    
    return query

def application(environ, start_response):
    status = '200 OK'
    # connect to the database
    dbcnx = MySQLdb.connect(host="dbdev.cs.uiowa.edu", port=3306, user="cs3910_team2_deploy", passwd="eech6yaP.thish0Ma", db="db_cs3910_team2")

    # define the SQL query
    sqlquery= makeQuery(environ['QUERY_STRING'])
    resultstring = makeResultString(environ['QUERY_STRING'])
    formDict = parse_qs(environ['QUERY_STRING'])
    # create a cursor
    cursor = dbcnx.cursor()
    cursor2 = dbcnx.cursor()
    # execute the SQL query
    cursor.execute(sqlquery)
    cursor2.execute("SELECT * FROM opList ORDER BY RAND ( )LIMIT 10")
    output = '<html>\n'
    output += '<head>\n'
    output += '<meta charset="utf-8">\n'
    output += '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    output += '<title>REU Opportunities</title>\n'
    output += '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">\n'
    output += '<link rel="stylesheet" href="style.css" />\n'
    output += '</head>\n'
    output += '<body>\n'
    output += '''<style>
                /* (A) STANDARD ROW HEIGHT */
            .vwrap, .vitem {
            height: 30px;
            line-height: 30px;
            }
            
            /* (B) FIXED WRAPPER */
            .vwrap {
            overflow: hidden; /* HIDE SCROLL BAR */
            background: #eee;
            }
            /* (C) TICKER ITEMS */
            .vitem { text-align: center; }
            
            /* (D) ANIMATION - MOVE ITEMS FROM TOP TO BOTTOM */
            /* CHANGE KEYFRAMES IF YOU ADD/REMOVE ITEMS */
            .vmove { position: relative; }
            @keyframes tickerv {
            0% { bottom: 0; } /* FIRST ITEM */
            30% { bottom: 30px; } /* SECOND ITEM */
            60% { bottom: 60px; } /* THIRD ITEM */
            90% { bottom: 90px; } /* FORTH ITEM */
            100% { bottom: 0; } /* BACK TO FIRST */
            }
            .vmove {
            animation-name: tickerv;
            animation-duration: 15s;
            animation-iteration-count: infinite;
            animation-timing-function: ease-out;
            }
            .vmove:hover { animation-play-state: paused; }
        </style>
    '''
    output +='''
    <div class="vwrap">
        <div class="vmove">
        '''
    numrows = int(cursor2.rowcount)
    for x in range(0, numrows):
        row2 = cursor2.fetchone()
        outString = row2[1] + ' ' + row2[2] + ' <a href= oppPage.wsgi?id=%s>See More</a>' %row2[0]
        output += '<div class="vitem">%s</div>' % outString
    output+='''</div></div>'''

    output += '<div class="container">\n'
    output += '<div class="row">\n'
    output += '<div class="col-1">\n'

    output += '<img src="nsfLogo.png" class="form-control">\n'
    output += '</div>\n'
    output += '<div class="col-10 offset-1">\n'
    output += '<ul id="menuBar" class="nav nav-tabs pt-3">\n'
    output += '<li class="nav-item">\n'
    output += '<a class="nav-link" href ="mapPage.wsgi">Map</a>\n'
    output += '</li>'
    output += '<li class="nav-item">\n'
    output += '<a class="nav-link active" href="tablePage.wsgi">Table View</a>\n'
    output += '</li>\n'
    output += '<li class="nav-item">\n'
    output += '<a class="nav-link" href="https://www.nsf.gov/">NSF Site</a>\n'
    output += '</li>\n'
    output += '<li class="nav-item">\n'
    output += '</li>\n'
    output += '<li class="nav-item dropdown">\n'
    output += '<a class="nav-link dropdown-toggle" href="#" id = "settingsDropdown" role ="button" data-bs-toggle="dropdown" aria-expanded = "false">Settings</a>\n'
    output += '<ul class="dropdown-menu" aria-labelledby="settingsDropdown">\n'
    output += '<li><button id="dark-mode-toggle" class ="dropdown-item">Dark Mode</button></li>\n'
    output += '<li><div id="google_translate_element" class = "dropdown-item"></div></li>\n'
    output += '</li>\n'
    output += '</ul>\n'
    output += '</div>\n'
    output += '</div>\n'
    output += '<div class="row">\n'
    output += '<div class="col-2 mx-auto">\n'
    output += '<form action="tablePage.wsgi">\n'
    
    output += '<input type="text" id="state" name="state" class="form-control" placeholder="Enter State:" style = "margin-top: 20px; margin-bottom:20px;">\n'
    output += '<input type="text" id="city" name="city" class="form-control" placeholder="Enter City:" style = "margin-bottom:20px;">'
    output += '<input type="text" id="topics" name="topics" class="form-control" placeholder="Enter Keyword:" style = "margin-bottom:20px;">\n'
    for i in formDict:
        if i in ['state','city','topics']:
            output += '<script> document.getElementById("%s")' % str(i)
            output += '.value = ' + str(formDict[i]) + '</script>'
    output += '<select class= "form-select" name="ShowNumber" id="ShowNumber"><option value="5">Max results: 5</option> <option value="10">Max results: 10</option> <option value="15">Max results: 15</option> <option value=100 selected># of results</option> </select>'
    output += '<button class="btn btn-primary" type="submit" style = "margin-top:20px;">Submit</button>\n'
    output += '</form>\n'
    
    output += '</div>\n'
    output += '<div class="col-10">\n'
    output += '<input type="text" id="searchbox" class="form-control" placeholder="Search Page:">\n'

    #JavaScript for translate
    output += '''<script type="text/javascript">
    function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'en', layout: google.translate.TranslateElement.InlineLayout.SIMPLE,autoDisplay: false},'google_translate_element');
    }
	'''
    output+= ' </script>'

    output += '''<script type="text/javascript"src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit">
	'''
    output += '</script>'

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
    output += '''
                function sortTable(columnNum) {

            var table, rows, switching, i, x, y, shouldSwitch;
            table = document.getElementById("mainTable");
            switching = true;
            allTH = document.getElementsByTagName("TH");
            for (i = 0; i < (allTH.length); i++){
                console.log(allTH[i].innerHTML);
                console.log(allTH[i].innerHTML.slice(-1));
                console.log(allTH[i].innerHTML.slice(-1) == ' ');

                if (allTH[i].innerHTML.slice(-1) == ' '){
                    allTH[i].innerHTML = allTH[i].innerHTML.slice(0,-2);
                }
            }
            selectedTH = document.getElementById("th " + columnNum);

            selectedTH.innerHTML += '&#11015; ';
            /* Make a loop that will continue until
            no switching has been done: */
            while (switching) {
                // Start by saying: no switching is done:
                switching = false;
                rows = table.rows;
                /* Loop through all table rows (except the
                first, which contains table headers): */
                for (i = 1; i < (rows.length - 1); i++) {
                // Start by saying there should be no switching:
                shouldSwitch = false;
                /* Get the two elements you want to compare,
                one from current row and one from the next: */
                x = rows[i].getElementsByTagName("TD")[columnNum];
                y = rows[i + 1].getElementsByTagName("TD")[columnNum];
                // Check if the two rows should switch place:
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
                }
                if (shouldSwitch) {
                /* If a switch has been marked, make the switch
                and mark that a switch has been done: */
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
                }
            }
            }
            
    '''
    output += '</script>'
    output += '<h1>Search Results:</h1>'
    output += '''<center><h2>'''
    output += resultstring + '</h2>'
    
    output += '<table id="mainTable" class="table form-control table-hover">\n'
    output += '<thead>\n'
    
    output += '<tr>\n'
    output += '<th id = "th 0" onclick = "sortTable(0)" scope="col" style = "cursor:pointer">Institution</th>'
    output += '<th id = "th 1" onclick = "sortTable(1)" scope="col" style = "cursor:pointer">Title</th>'
    output += '<th id = "th 2" onclick = "sortTable(2)" style = "cursor:pointer" scope="col">URL</th>'
    output += '<th id = "th 3" onclick = "sortTable(3)" style = "cursor:pointer" scope="col">Department</th>'
    output += '<th id = "th 4" onclick = "sortTable(4)" style = "cursor:pointer" scope="col">City</th>'
    output += '<th id = "th 5" onclick = "sortTable(5)" style = "cursor:pointer" scope="col">State</th>'

    #output += '<th id = "th 6" onclick = "sortTable(6)" style = "cursor:pointer" scope="col">Zip Code</th>'
    output += '<th id = "th 7" scope="col">Select</th>'
    output += '<th id = "th 8" ></th>'

    output += '</tr>\n'

    # get the number of rows in the resultset
    numrows = int(cursor.rowcount)

    # get and display one row at a time
    for x in range(0, numrows):
        row = cursor.fetchone()
        if row[3][:2] == ': ':
            url = 'https://'+row[3][2:]
        else:
            url = row[3]
        output += '<tr><td> %s </td>' % row[1]
        output += '<td> %s </td>' % row[2]
        output += '<td style="word-wrap: break-word; max-width: 200px; font-size:12px"> <a href= %s target="_blank" rel="noopener noreferrer">' % url
        output += '%s</a> </td>' % url
        output += '<td> %s </td>' % row[4]
        output += '<td> %s </td>' % row[5]
        output += '<td> %s </td>' % row[6]
        #output += '<td> %s </td>' % row[7]
        output += '<td><input type="checkbox" class="row-checkbox"></td>'
        output += '<td style="word-wrap: break-word; max-width: 200px; font-size:12px"> <a href= oppPage.wsgi?id=%s>See More</a> </td></tr>' % row[0]

        

    output += '</table>\n'
    output += '<button class="btn btn-primary" id="download-btn">Download Selected Rows</button>\n'
    output += '</div>\n'
    output += '</div>\n'
    output += '</div>\n'

    output += '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>\n'
    
    output += '</body>\n'

    output += '<script>'
    output += '''
    function downloadSelectedRows() {
        var rows = document.querySelectorAll("tr");
        var selectedRows = [];

        for (var i = 1; i < rows.length; i++) {
            var checkbox = rows[i].querySelector(".row-checkbox");

            if (checkbox.checked) {
                var rowData = [];

                var cells = rows[i].querySelectorAll("td");
                for (var j = 0; j < cells.length - 1; j++) {
                    rowData.push(cells[j].textContent);
                }

                selectedRows.push(rowData.join(", "));
            }
        }

        if (selectedRows.length === 0) {
            alert("No rows selected. Please select at least one row to download.");
            return;
        }

        var data = selectedRows.join("\\n");
        var blob = new Blob([data], { type: "text/plain;charset=utf-8" });
        var url = URL.createObjectURL(blob);

        var link = document.createElement("a");
        link.href = url;
        link.download = "selected-rows.txt";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("download-btn").addEventListener("click",  downloadSelectedRows);
    });
    '''
    output += '</script>'
    output += '''<script>
    // Add or remove the dark-mode class when the toggle is clicked
    function toggleDarkMode() {
        const darkModeEnabled = document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', darkModeEnabled);
    }

    // Check the user's preference when the page loads
    document.addEventListener('DOMContentLoaded', () => {
        const darkModeEnabled = localStorage.getItem('darkMode') === 'true';
        if (darkModeEnabled) {
            document.body.classList.add('dark-mode');
        }
    });
    </script>'''

    output += '</html>\n'

    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]
