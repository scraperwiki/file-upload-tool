#! /usr/bin/env python

import datetime


def main(path):
    print "Foo", path


def process(fd):
    yield {"_id": None, "_timestamp": datetime.datetime.now()}

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
