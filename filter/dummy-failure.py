#! /usr/bin/env python

def main(path):
    print "Foo", path
    raise RuntimeError("expected test failure")

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
