#! /usr/bin/env python


def main(path):
    print "Foo", path


def process(fd):
    yield {"_id": None}

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
