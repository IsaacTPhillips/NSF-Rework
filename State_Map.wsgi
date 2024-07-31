!/usr/bin/python
import csv, getpass, MySQLdb
#This will connect you to database you need
#Make shure to add your correct information
#Check it worked before moving on
dbcnx=MySQLdb.connect(
  host = 'dbdev.cs.uiowa.edu',
  user = 'itphillips',
  passwd = 'ywY2GDbRZNUg8g0',
  db='db_itphillips')

#Create table (if doen't exist already)
#In this example has column Name and column GPA
create_SQL= """CREATE TABLE IF NOT EXISTS maps State char(50), Pop char(20);"""
cur = dbcnx.cursor()
#Below print can be used to check what command it tries to execute in next line
#print (create_SQL)

cur.execute(create_SQL)
dbcnx.commit()
cur.close()

#If you you got here table is created - check in dbdev
#print("Table created and exists")

#This will open file filename,csv
#It uses csvlibrary

numrows = int(cur.rowcount)

with open('NSF_Files.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    
    #For every row with data - it skips first row with titles of columns
    #you can print row
    #print(row)
    
    cur=dbcnx.cursor()

    #Next line creates sql string that represents
    #one insert sql command and current row data
    #Note row['Need to be one of the cilumn names'] will grab
    #value in current row for that column
    #%s is replaced with first parameter in parentheses - string
    #%f is replaced with second parameter - float
    sql = "INSERT INTO Map VALUES ('%s', %f);" % (row['State'], float(row['AVG_Age']))
    
    #Below print can print sql command - check it legit before executing:)
    #print(sql)
    cur.execute(sql)
    #dbcnx.commit()
    cur.close()
dbcnx.close()
