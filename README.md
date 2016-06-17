# Files to note:
================
- Launch.py: 				the script for testing the assignment
- FlaskDiarySvr.py:			the server
- cUrlClient.py:			the tester client
- Diary.db:					the SQLite database file
- sqlWhereOperators.py:		contains a class that holds valid SQL comparison statements
- tableColumns.py:			contains a class that holds the column names of [Diary] table



# 'Diary' assignment - External Dependencies:
=============================================
- Flask: the HTTP library used to implement the server.
- cURL: the HTTP client used to test the server
- SQLite3: single-file local DB



# Time frame limitation notes:
==============================
- 'FlaskDiarySvr.py' contains 3 methods with nearly identical code. I am aware that using the python parallel to .Net delegates and c++ function pointers is a better code implementation.
- Given more time, I'd created a more formal unittest, with setUp and tearDown I'd find appropriate.
- Didn't work #continuously# with git, because I used VS-2012 for debugging and faster code editing, and saw no point in synchronizing >50MB that .Net dumps intop the folder with GITHUB.
- Could be more elegant to run client and server in different cmd windows. Worth exploring.
