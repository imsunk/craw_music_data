#!/usr/bin/env python
import os, sys
import datetime, time

if len(sys.argv) < 2:
    sys.exit(-1)

if len(sys.argv[1]) != len(sys.argv[2]):
    print >> sys.stderr, "two argument must have same length"
    sys.exit(-1)

if len(sys.argv[1]) == 6:
    date_format = '%y%m%d'
elif len(sys.argv[1]) == 8:
    date_format = '%Y%m%d'
else:
    date_format = '%Y%m%d%H'

stime = datetime.datetime(*(time.strptime( sys.argv[1], date_format )[0:6]))
if len(sys.argv) > 2:
    etime = datetime.datetime(*(time.strptime( sys.argv[2], date_format )[0:6]))
else:
    etime = stime + datetime.timedelta(hours = 1)

while stime <= etime:
    print >> sys.stdout, stime.strftime(date_format)
    stime += datetime.timedelta(hours = 1)
