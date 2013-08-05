#!/usr/bin/python

# Based on examples from
# http://www.tutorialspoint.com/python/python_cgi_programming.htm

import sys
import cgi
import os
import cgitb
cgitb.enable()

CSV_DIR = '../csv/' # CSV upload directory

form = cgi.FieldStorage()

fileitem = form['filename'] # Get filename

# Check if the file was uploaded
if fileitem.filename:
    # strip leading path from file name to avoid 
    # directory traversal attacks
    fn = os.path.basename(fileitem.filename)
    open('../csv/' + fn, 'wb').write(fileitem.file.read())

    print 'Status: 204\r\n\r\n' # Success, don't reload page

else:
    # Error, send a message
    print """\
Status: 200\r\n
Content-Type: text/html;charset=UTF-8\n
<html>
<body>
   <p>Error: No se subi&oacute; el archivo.</p>
</body>
</html>
    """

