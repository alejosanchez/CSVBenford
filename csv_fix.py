#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Give back the columns of a CSV and the in
# http://www.tutorialspoint.com/python/python_cgi_programming.htm

import csv
from   codecs import open as copen

SOURCE_CODEC = "iso-8859-1"
DEST_CODEC   = "utf-8"
DELIM        = ","

def convert_file(srcFile, dstFile, delim = DELIM,
                 src_codec=SOURCE_CODEC, dst_codec=DEST_CODEC):
    '''Convert a CSV file to standard format'''
    # From http://stackoverflow.com/a/191403
    with copen(srcFile, "r", SOURCE_CODEC) as sourceFile:
        with copen(dstFile, "w", DEST_CODEC) as targetFile:
            while True:
                line = sourceFile.readline()
                line = ",".join(line.split(delim))
                if not line:
                    break
                targetFile.write(line)

if __name__ == '__main__':
    from   sys    import argv

    if len(argv) < 3:
        print "Usage:"
        print "\t%s <src_file> <dst_file> [delim] [src_codec] [dst_codec]" % argv[0]
        print "\nExample:\n\t%s source.csv dest.csv %s %s %s" \
               % (argv[0], DELIM, SOURCE_CODEC, DEST_CODEC)
        print '(if delim is ";" in unix escape it as "\;")'
        exit(-1)

    delim     = DELIM        # Source delimiter
    if len(argv) > 3:
        delim     = argv[3]

    src_codec = SOURCE_CODEC
    if len(argv) > 4:
        src_codec = argv[4]

    dst_codec = DEST_CODEC
    if len(argv) > 5:
        src_codec = argv[5]

    convert_file(argv[1], argv[2], delim, src_codec, dst_codec)

