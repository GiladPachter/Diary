"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

#   < FLASK INFRASTRUCTURE >  ---  DO NOT TOUCH

from flask import Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Handling URL Parameters
from flask import request

## FLASK DEBUG
#from flask_debug import Debug

#   < / FLASK INFRASTRUCTURE >



#   < FW IMPORTS >

import sys, os

#   < / FW IMPORTS >



#   < SQLite3 CONNECTIVITY >  ---  DO NOT TOUCH

import sqlite3
#from datetime import date, datetime, timedelta
import datetime

def dbConnect():
    print('Connecting to SQLite DB: ' + os.path.abspath('Diary.db'))
    conn = sqlite3.connect('Diary.db')
    cur = conn.cursor()
    return conn, cur
def dbDisconnect(conn):
    conn.close()
    print('Disconnected from SQLite DB')

conn, cur = dbConnect()

#   < / SQLite3 CONNECTIVITY >



#   < PROJECT IMPORTS >

from sqlWhereOperators import Operators
from tableColumns import ColumnNames

#   < / PROJECT IMPORTS >



#   < FLASK Helpers >

def dbReadAll(qry):
    cur.execute(qry)
    result = cur.fetchall()
    return result

def dbReadOne(qry):
    cur.execute(qry)
    result = cur.fetchone()
    return result

def validateRecordValues(Created, Title , Content):
    if Created == None or Created == '':    raise ValueError("Missing/Empty Web API Parameter: 'Created'")
    if Title == None   or Title == '':      raise ValueError("Missing/Empty Web API Parameter: 'Title'")
    if Content == None or Content == '':    raise ValueError("Missing/Empty Web API Parameter: 'Content'")

    #print('Created: ' + Created)
    #print('Title: ' + Title)
    #print('Content: ' + Content)

    strToDatetime(Created)    # validate timestamp


def strToDatetime(sDatetime):
    DATE_FORMATS = ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S.%f", "%Y/%m/%d %H:%M:%S"]
    for date_format in DATE_FORMATS:
        try:
            my_date = datetime.datetime.strptime(sDatetime, date_format)
        except ValueError:
            pass
        else:
          break
    else:
        raise ValueError("'sDatetime' is not formatted correctly! ('" + sDatetime + "')")

    return my_date

#   < / FLASK Helpers >



#   < FLASK APIs >

@app.route('/hello')     # URL:  Server/
def hello():
    return "Hello World!"   # Renders a sample page

#@app.route("/abc", methods=['GET'])
##  INCORRECT:  def abc(a,b,c):
#def abc():
#    a = request.args.get('a')
#    b = request.args.get('b')
#    c = request.args.get('c')
#    return a + b + c

@app.route("/clearDiary")
def clearDiary():
    try:
        #raise IOError("TEST IOError")
        cur.execute("DROP TABLE IF EXISTS Diary")
        conn.commit()
        cur.execute("CREATE TABLE Diary (Created timestamp NOT NULL, Title text, Content text, CONSTRAINT Diary_PK PRIMARY KEY (Created))")
        conn.commit()
        return '[Diary] Cleared.'
    except IOError as ioe:
        return "Server Error: 'clearDiary' (IOError)! " + str(ioe)
    except Exception as ex:
        return "Server Error: 'clearDiary' (Exception)! " + str(ex)
    except:
        return "Server Error: 'clearDiary'! UNKNOWN ERROR"

@app.route("/writeEntry", methods=['GET'])
def writeEntry():
    try:
        Created = request.args.get('Created')
        Title     = request.args.get('Title')
        Content   = request.args.get('Content')

        validateRecordValues(Created, Title , Content)

        qry = "INSERT OR IGNORE INTO Diary (Created, Title, Content) VALUES ('{0}','{1}','{2}')".format(Created, Title, Content)
        cur.execute(qry)
        qry = "UPDATE Diary SET Title = '{1}', Content = '{2}' WHERE Created = '{0}'".format(Created, Title, Content)
        cur.execute(qry)
        conn.commit()
        return 'Entry inserted/updated successfully.'
    except Exception as ex:
        return "Server Error: 'writeEntry'! " + str(ex)
    except:
        return "Server Error: 'writeEntry'! UNKNOWN ERROR"

@app.route("/getAllResults", methods=['GET'])
def getAllResults():
    return str(dbReadAll("SELECT * FROM Diary"))

@app.route("/queryDiary", methods=['GET'])
def queryDiary():
    try:
        colName  = request.args.get('colName')
        operator = request.args.get('operator')
        value    = request.args.get('value')

        if ColumnNames.getMemberName(colName) == None:
            raise ValueError("Invalid Column Name '{0}'".format(colName))

        qry = "SELECT * FROM Diary WHERE ({0} {1} {2})".format(colName, operator, value)
        return str(dbReadAll(qry))
    except ValueError as ve:
        return "Server Error: 'queryDiary' (ValueError)! " + str(ve)
    except Exception as ex:
        return "Server Error: 'queryDiary' (Exception)! " + ex
    except:
        return "Server Error: 'queryDiary'! UNKNOWN ERROR"

@app.route("/searchCreated", methods=['GET'])
def searchCreated():
    try:
        operator = request.args.get('operator')
        value    = request.args.get('value')

        if Operators.getMemberName(operator) == None:
            raise ValueError("Invalid SQL Operator '{0}'".format(operator))

        elements = str(value).split(' AND ')
        for elem in elements:
            strToDatetime(str(elem).strip("' "))

        qry = "SELECT * FROM Diary WHERE (Created {0} {1})".format(operator, value)
        return str(dbReadAll(qry))
    except ValueError as ve:
        return "Server Error: 'searchCreated' (ValueError)! " + str(ve)
    except Exception as ex:
        return "Server Error: 'searchCreated' (Exception)! " + str(ex)
    except:
        return "Server Error: 'searchCreated'! UNKNOWN ERROR"

@app.route("/searchTitle", methods=['GET'])
def searchTitle():
    try:
        operator = request.args.get('operator')
        value    = request.args.get('value')
        
        if Operators.getMemberName(operator) == None:
            raise ValueError("Invalid SQL Operator '{0}'".format(operator))
        if operator == Operators.Between:
            raise ValueError("'BETWEEN' operator not supported for strings")

        qry = "SELECT * FROM Diary WHERE (Title {0} {1})".format(operator, value)
        return str(dbReadAll(qry))
    except ValueError as ve:
        return "Server Error: 'searchCreated' (ValueError)! " + str(ve)
    except Exception as ex:
        return "Server Error: 'searchCreated' (Exception)! " + str(ex)
    except:
        return "Server Error: 'searchCreated'! UNKNOWN ERROR"

@app.route("/searchContent", methods=['GET'])
def searchContent():
    try:
        operator = request.args.get('operator')
        value    = request.args.get('value')
        
        if Operators.getMemberName(operator) == None:
            raise ValueError("Invalid SQL Operator '{0}'".format(operator))
        if operator == Operators.Between:
            raise ValueError("'BETWEEN' operator not supported for strings")

        qry = "SELECT * FROM Diary WHERE (Content {0} {1})".format(operator, value)
        return str(dbReadAll(qry))
    except ValueError as ve:
        return "Server Error: 'searchCreated' (ValueError)! " + str(ve)
    except Exception as ex:
        return "Server Error: 'searchCreated' (Exception)! " + str(ex)
    except:
        return "Server Error: 'searchCreated'! UNKNOWN ERROR"

@app.route("/deleteEntries", methods=['GET'])
def deleteEntries():
    try:
        operator = request.args.get('operator')
        value    = request.args.get('value')
        qry = "DELETE FROM Diary WHERE (Created {0} {1})".format(operator, value)
        cur.execute(qry)
        return '{0} rows affected'.format(cur.rowcount)
    except IOError as ioe:
        return "Server Error: 'deleteEntries' (IOError)! " + str(ioe)
    except Exception as ex:
        return "Server Error: 'deleteEntries' (Exception)! " + str(ex)
    except:
        return "Server Error: 'deleteEntries'! UNKNOWN ERROR"

#   < / FLASK APIs >




# Launch Server
if __name__ == '__main__':
    #HOST = os.environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(os.environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    HOST = 'localhost'
    PORT = 5555

    print("HOST: {0} , PORT: {1}".format(HOST, PORT))

    app.run(HOST, PORT)

    dbDisconnect(conn)
