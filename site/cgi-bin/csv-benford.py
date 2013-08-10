#!/usr/bin/env python

# Check a CSV file for Benford's Law compliance

import csv
import sys
import codecs
import cgi
import os
import cgitb
from   collections import defaultdict
from   itertools   import imap

CSV_DIR = '../csv/' # CSV upload directory
GROUPING_DEFAULT = 'todos' # No grouping column

# Decimal digits with expected percentage for Benford's Law
BF = [ 30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6 ]

MIN_ELEMENTS = 60

# UTF-8 hack
#      from http://stackoverflow.com/a/11764727
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
# If you need input too, read from char_stream as you would sys.stdin
#char_stream = codecs.getreader('utf-8')(sys.stdin)
# python 2.x sys.stdout.encoding by default is None
# better option would be setting os.environ.get('PYTHONIOENCODING') to UTF-8
cgitb.enable()

# Pearson correlation
#   from http://stackoverflow.com/a/5713856
def pearsonr(x, y):
  # Assume len(x) == len(y)
  n        = len(x)
  sum_x    = float(sum(x))
  sum_y    = float(sum(y))
  sum_x_sq = sum(map(lambda x: pow(x, 2), x))
  sum_y_sq = sum(map(lambda x: pow(x, 2), y))
  psum     = sum(imap(lambda x, y: x * y, x, y))
  num      = psum - (sum_x * sum_y/n)
  den      = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)

  if den == 0:
      return 0

  return num / den

class CheckError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
  
def check_benford(r, col_n, col_v):
    '''Check if iterable (file) column col_v follows Benford's law
       grouping by col_n (-1 for no grouping).
    '''
    dd       = defaultdict(list)      # digits count
    dt       = defaultdict(lambda: 0) # total count (for percentage)
    final    = []
    row_errors = 0

    for row in r:
        col_n_v = GROUPING_DEFAULT # No grouping column
        try:

            if not row[col_v].isdigit():
                # print 'ERROR:', row
                row_errors += 1
                continue # n/d or bad data
            if row[col_v] == '0':
                continue # don't count zeros

            val = row[col_v]
            if col_n > -1:
                col_n_v = row[col_n] # Get grouping column value
            dd[col_n_v].append(str(row[col_v])[0])
            dt[col_n_v] += 1

        except:
            row_errors += 1 # something broke

    insufficient = [] # missing digits, the count for a digit is 0

    # for each filter, sum first digit
    for k, lv in dd.items():

        if lv == None or dt[k] < MIN_ELEMENTS:
            insufficient.append(k)
            continue

        dg   = {} # defaultdict(lambda: 0) # a dictionary of digits

        for v in lv:
            try:
                v = int(v)
            except:
                lv.sort()
                raise CheckError("ERROR:" + k + lv)
            dg[v] = dg.get(v, 0) + 1

        dgl  = []  # List of percentages of occurrence of digits 1-9
        for i in range(1, 10):
            dc = dg.get(i, 0) # counts for this digit
            if dc > 0:
                # Percentage of numbers with this digit over total
                pd = ( float(dg[i]) * 100 ) / dt[k]
                # print k, i, float(dg[i]), dt[k]
                # pd Expected percentage of this digit
                dgl.append(pd)
            else:
                dgl.append(0)  # very dodgy, missing digit

        pc = pearsonr(BF, dgl)
        final.append((pc, k, dgl))

    final.sort()     # Sort by pearson idx, key
    final.reverse()  # Best to worst

    result                 = {}
    result['series']       = []         # Each series with digit percentages
    result['row_errors']   = row_errors
    result['rejected']     = []         # Rejected series, not all digits
    result['insufficient'] = insufficient

    for pc, k, dgl in final:
        if len(dgl) < 9:
             result['rejected'].append(k) # Not enough information?
             continue
        result['series'].append((k.encode('utf-8'), dgl))

    return result

# XXX return rejected, count, series

form      = cgi.FieldStorage()
filename  = form.getvalue('filename')          # Get filename
col_group = int(form.getvalue('column_group')) # Get column to group by
col_check = int(form.getvalue('column_check')) # Get column to check

f         = open(CSV_DIR + filename, 'r')
r         = csv.reader(f, dialect=csv.excel) # Create CSV row reader
col_names = next(r)

c = [col_names[col_group], col_names[col_check]]
colutf8 = '"' + '","'.join(c).encode('utf-8') + '"'

r = check_benford(r, col_group, col_check)

#print 'rejected (%d):' % (len(r['rejected']), )
#for k in r['rejected']:
#    print '%s' % (k, )

rp = [] # convinience string accumulator
for k, v in r['series']:
    rp.append('"' + k + '"'
                  + ':[' + ', '.join([ str(round(vf, 2)) for vf in v]) + ']')

series = ",\n".join(rp)

print '''\
Status: 200\r
Content-Type: application/json;charset=UTF-8\r
\r
{ "columns" : [%s],
  "series":   {%s},
  "rejected": %s,
  "insufficient": ["%s"]
}''' % ( colutf8, series,
         str(r['rejected']),
         '","'.join(r['insufficient']).encode('utf-8'))

