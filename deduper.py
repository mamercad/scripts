#!/usr/bin/python

import argparse
import hashlib
import os
import pprint
import sys

try:
    parser = argparse.ArgumentParser(description='depuplicate a directory')
    parser.add_argument(
        '--directory', help='directory to deduplicate', required=True)
    parser.add_argument('--suffix', default='DUP',
                        help='suffix to add to dupes', required=False)
    args = parser.parse_args()

    # hash em up
    total = 0
    dupes = 0
    d = {}
    for root, dirs, files in os.walk(args.directory):
        for name in files:
            if name.endswith('.' + args.suffix):
                continue
            f = os.path.join(root, name)
            h = hashlib.sha256(open(f, 'rb').read()).hexdigest()
            if h not in d.keys():
                d[h] = [f]
            else:
                d[h].append(f)
                dupes = dupes + 1
            total = total + 1

    # clean em up
    for h in d.keys():
        if len(d[h]) > 1:
            print "DUPE", d[h]
            for f in d[h][1:]:
                os.rename(f, f + '.' + args.suffix)
                print "  RENAME", f, "to", f + '.' + args.suffix
        else:
            print "UNIQ", d[h][0]
    print "TOTAL:", total, "DUPES:", dupes

except Exception as e:
    print e
    sys.exit(1)
