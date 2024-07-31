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
    key = 'AIzaSyBskp818PVuUaJ_pvZU7D17slVKgEQwmzU'
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

    theads = ['ID','Institution','Site Name','Site URL','Department','City','State','ZIP Code','Country','Contact Name','Contact Phone','Contact Email','Alternative Name','Alternative Phone','Alternative Email','Topics','Comments','Award URL','Cofund 1','Cofund 2','Cofund 3'] 
    row = cursor.fetchone()
    mapquery = key + "&q="+row[1].replace('&','') + "+" + row[5] + "+" + row[6] + "+" + row[7]
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
    output += '<a class="nav-link" href="#">Account</a>\n'
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
    output += '<form action="temp.wsgi">\n'
    
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
    output += '''<script>
    function printj () {
 var printDiv = document.getElementById("contentdiv");
 var printWindow = window.open('', '', 'left=0, top=0, width=800, height=500, toolbar=0, scrollbars=0, status=0');
 printWindow.document.write(printDiv.innerHTML);
 printWindow.document.close();
 printWindow.print();
}
    '''
    output += '</script>'

    output += '<button onclick="history.back()">&#x2190;</button>'
    output += "<br><br><input value='Print this page' type='button' onclick='printj()'/>"
    output += '<div class="col-10" id = "contentdiv">'
    
    
    
    index = 1
    while index < len(row):
        item = row[index]
        blank = False
        if item == "": 
            blank = True
        head = '<strong>' + theads[index] + '</strong>'
        if index == 3 or index == 17 and blank == False:
            if item[:2] == ': ':
                url = 'https://'+item[2:]
            else:
                url = item
            if index == 3:
                output += '<p> <strong>URL</strong>: <a href= %s target="_blank" rel="noopener noreferrer">' % url
                output += url + '</a></p>'
            else:
                output += '<p> <strong> Award URL</strong>: <a href= %s target="_blank" rel="noopener noreferrer">' % url
                output += url + '</a></p>'
        elif index == 10 or index == 13 and blank == False:
            output += '<p><strong>'
            if index == 13: output += 'Alternate '
            output += 'Phone</strong>: <a href = "tel: %s">' % item
            output += item + '</a></p>'
        elif index == 11 or index == 14 and blank == False:
            output += '<p><strong>'
            if index == 14: output += 'Alternate '
            output+= 'Email</strong>: <a href = "mailto: %s">' % item
            output += item + '</a></p>'
        elif index == 15 and blank == False:
            output += '<p>' + str(head) +':'
            for i in item.split(','):
                output += '<a href = tablePage.wsgi?topics=%s' % i.replace(" ","+").replace(".","")
                output += '> %s</a>,' % str(i)
            output += "</p>"
        else:
            if blank == False:

                output += '<p>' + str(head) + ": " + str(item) + '</p>'
        index +=1
        
    output += '''<center><iframe
    width="500"
    height="350"
    style="border:0"
    loading="lazy"
    allowfullscreen
    referrerpolicy="no-referrer-when-downgrade"
    src="https://www.google.com/maps/embed/v1/place?key=%s"></iframe></center>''' % mapquery
    output += '</div>\n'
    
    output += '</div>\n'
    
    output += '</div>\n'
    output += '</div>\n'

    output += '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>\n'

    output += '</body>\n'
    
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