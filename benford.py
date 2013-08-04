#!/usr/bin/env python

# Check a CSV file for Benford's Law compliance
# 
# Usage:
#    a csv file
#    a column to filter as (usually a name)
#    a column to assign as values of that name to check
#
import csv
from   collections import defaultdict
from   itertools   import imap


# Decimal digits with expected percentage for Benford's Law
BF = [ 30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6 ]

# Pearson correlation by http://stackoverflow.com/a/5713856
def pearsonr(x, y):
  # Assume len(x) == len(y)
  n = len(x)
  sum_x = float(sum(x))
  sum_y = float(sum(y))
  sum_x_sq = sum(map(lambda x: pow(x, 2), x))
  sum_y_sq = sum(map(lambda x: pow(x, 2), y))
  psum = sum(imap(lambda x, y: x * y, x, y))
  num = psum - (sum_x * sum_y/n)
  den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
  if den == 0: return 0
  return num / den

def check_benford(r, col_n, col_v):
    '''Check if iterable (file) column col_v follows Benford's law
       grouping by col_n.
    '''

    dd = defaultdict(list)      # digits count
    dt = defaultdict(lambda: 0) # total count (for percentage)
    final = []
    next(r)
    rejected = 0
    for row in r:
        try:
            if str(row[col_v])[0] == 'n':
                continue # n/d
            if row[col_v] == '0':
                continue # don't count
            val = row[col_v]
            dd[row[col_n]].append(str(row[col_v])[0])
            dt[row[col_n]] += 1
        except:
            rejected += 1

    if rejected:
        print "rejected", rejected, "rows"

    # for each filter, sum first digit
    for k, lv in dd.items():
        if lv == None:
            continue
        dg = {} # defaultdict(lambda: 0) # a dictionary of digits
        for v in lv:
            try:
                v = int(v)
            except:
                lv.sort()
                print "ERROR:", k, lv
                break
            dg[v] = dg.get(v, 0) + 1
        dgl  = []
        dglr = []
        for i in range(1, 10):
            try:
                # Percentage of numbers with this digit over total
                pd = ( float(dg[i]) * 100 ) / dt[k]
                # print k, i, float(dg[i]), dt[k]
                # pd Expected percentage of this digit
                dgl.append(round(pd, 1))
                dglr.append(abs(1 - pd / BF[i - 1]))
            except:
                print "ERROR for", k, i
        pc         = pearsonr(BF, dgl)
        final.append((pc, k, dgl))
        print k, \
            "\n\t Expected ", BF,  \
            "\n\t Dataset  ", dgl, \
            "\n\t", pc
            # "\n\t", dglr, \
    final.sort()
    final.reverse()
    for pc, k, dgl in final:
        if len(dgl) < 9:
             print "// ", k, "not enough information"
             continue
        print '''
                }, {
                    name:    '%s',
                    data:    %s,
                    visible: false''' % (k, dgl)
##print k.ljust(25), round(v, 2), dgl

if __name__ == '__main__':

    import sys
    if len(sys.argv) != 4:
        print "Usage:\n", sys.argv[0], \
                    " [CSV file] [filter column] [number column]"
        exit(-1)

    fname = sys.argv[1]
    col_n = int(sys.argv[2])
    col_v = int(sys.argv[3])

    f = open(fname, 'r')     # Open input CSV file
    r = csv.reader(f, dialect=csv.excel)        # Create CSV row reader
    check_benford(r, col_n, col_v)

