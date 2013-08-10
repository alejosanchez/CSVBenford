#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Give back the columns of a CSV and the in
# http://www.tutorialspoint.com/python/python_cgi_programming.htm


from   os      import listdir
from   os.path import isfile, join
from   fnmatch import fnmatch
import cgitb

CSV_DIR = '../csv/' # CSV upload directory

cgitb.enable()      # pretty debugging

csv_files = [ f for f in listdir(CSV_DIR) if fnmatch(f, '*.csv') ]

print '''\
Status: 200\r
Content-Type: application/json;charset=UTF-8\r
\r
{ "csvFiles" : [%s] }\r
''' % ( '"' + '","'.join(csv_files) + '"', )

