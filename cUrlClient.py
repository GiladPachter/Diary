
import sys

import urllib
from urllib.parse import urlparse

import pycurl
from io import BytesIO

from sqlWhereOperators import Operators
from tableColumns import ColumnNames


serviceURL = '127.0.0.1:5555/'



def processRequest(apiName, purpose='', apiParams={}):
    print('API:\t\t' + apiName)
    print('apiParams:\t' + str(apiParams))
    print('Purpose:\t' + purpose)

    url = serviceURL + apiName + '?' + urllib.parse.urlencode(apiParams)
    result = sendRequest(url)

    print('result:\t\t' + processResult(result))
    print('\n\r')

    #   'Failed to connect to 127.0.0.5 port 5555: Connection refused'
    if 'Failed to connect to' in result and 'port' in result and ': Connection refused' in result:
        sys.exit();


def sendRequest(url):
    try:
        buffer = BytesIO()
        c = pycurl.Curl()
        #c.setopt(c.URL, 'http://pycurl.io/')
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        return body.decode('iso-8859-1')
    except Exception as ex:
        return str(ex)


def processResult(result):
    if '<title>404 Not Found</title>' in result:
        return 'URL Error: 404 Not Found'

    return result



#processRequest(apiName='hello', outputComment='Hello FLASK API')
#processRequest(apiName='abc', outputComment='FLASK API w/ PARAMS', apiParams={'a': 'a', 'b': 'b' , 'c': 'c'}))


processRequest(apiName='clearDiary', purpose='Create empty [Diary] table')


processRequest(apiName='invalidAPI', purpose='BAD USAGE:    No such API exposed by the server')


processRequest(apiName='writeEntry', purpose='INSERT 1st Entry', apiParams={'Created': '2015-05-05 12:00:00.015', 'Title': 'First Entry' , 'Content': 'Hello World - 1'})
processRequest(apiName='writeEntry', purpose='UPDATE 1st Entry', apiParams={'Created': '2015-05-05 12:00:00.015', 'Title': 'First Entry' , 'Content': 'Hello World - 1 - MODIFIED'})
processRequest(apiName='writeEntry', purpose='INSERT 2nd Entry', apiParams={'Created': '2015-08-08 16:16:16.016', 'Title': 'Second Entry', 'Content': 'Hello World - 2'})
processRequest(apiName='writeEntry', purpose='INSERT 3rd Entry', apiParams={'Created': '2016-05-05 12:00:00.015', 'Title': 'Third Entry' , 'Content': 'Hello World - 3'})


processRequest(apiName='writeEntry', purpose='BAD USAGE:    API w/o required params')
processRequest(apiName='writeEntry', purpose="BAD USAGE:    Corrupted DateTime: 'Created'", apiParams={'Created': 'BAD DATA', 'Title': 'Third Entry' , 'Content': 'Hello World - 3'})
processRequest(apiName='writeEntry', purpose="BAD USAGE:    Missing Parameter: 'Title'",    apiParams={'Created': '2016-05-05 12:00:00.015', 'Content': 'Hello World - 3'})
processRequest(apiName='writeEntry', purpose="BAD USAGE:    Missing Parameter: 'Content'",  apiParams={'Created': '2016-05-05 12:00:00.015', 'Title': 'Third Entry'})


#import ast
#url = serviceURL + 'getAllResults'
#collection = ast.literal_eval(sendRequest(url))
processRequest(apiName='getAllResults', purpose='Retrieve all entries')


processRequest(apiName='queryDiary', purpose='Query by creation time interval - expect 2 out of 3 results', apiParams={'colName': ColumnNames.Created, 'operator': Operators.Between, 'value': "'2015-01-01 12:00:00.000' AND '2016-01-01 12:00:00.000'"})
processRequest(apiName='queryDiary', purpose='Query by Title containing value - expect 1 result',           apiParams={'colName': ColumnNames.Title,   'operator': Operators.Like,    'value': "'%st En%'"})
processRequest(apiName='queryDiary', purpose='Query by Content containing value - expect no results',       apiParams={'colName': ColumnNames.Content, 'operator': Operators.Like,    'value': "'%Worlds%'"})


processRequest(apiName='queryDiary', purpose="BAD USAGE:    Invalid ColumnName: 'Blah Blah'",       apiParams={'colName': 'Blah Blah', 'operator': Operators.Like,    'value': "'%Worlds%'"})


processRequest(apiName='searchCreated', purpose='Query by creation time interval - expect 2 out of 3 results', apiParams={'operator': Operators.Between, 'value': "'2015-01-01 12:00:00.000' AND '2016-01-01 12:00:00.000'"})
processRequest(apiName='searchTitle',   purpose='Query by Title containing value - expect 1 result',           apiParams={'operator': Operators.Like,    'value': "'%st En%'"})
processRequest(apiName='searchContent', purpose='Query by Content containing value - expect 3 results',         apiParams={'operator': Operators.Like,    'value': "'%World%'"})


processRequest(apiName='deleteEntries', purpose="DELETE According to Constraint",       apiParams={'operator': Operators.IsNotNull,    'value': ''})
processRequest(apiName='getAllResults', purpose='Retrieve NOTHING')


print('Bye bye :)')
input("Press Enter to continue...")