#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Give back the columns of a CSV and the in
# http://www.tutorialspoint.com/python/python_cgi_programming.htm

import cgi
import csv
import sys
import codecs
import cgitb

CSV_DIR = '../csv/' # CSV upload directory

# UTF-8 hack
#      from http://stackoverflow.com/a/11764727
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
# If you need input too, read from char_stream as you would sys.stdin
#char_stream = codecs.getreader('utf-8')(sys.stdin)
# python 2.x sys.stdout.encoding by default is None
# better option would be setting os.environ.get('PYTHONIOENCODING') to UTF-8

cgitb.enable() # pretty debugging

form      = cgi.FieldStorage()
filename  = form.getvalue('dataset')

f         = open(CSV_DIR + filename, 'r')
r         = csv.reader(f, dialect=csv.excel)        # Create CSV row reader
col_names = next(r)

print '''\
Status: 200\r
Content-Type: application/json;charset=UTF-8\r
Cache-Control: public, max-age=3600\r
\r
{ "columns" : [%s] }\r
''' % ( '"' + '","'.join(col_names).encode('utf-8') + '"', )

