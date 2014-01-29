#! /usr/bin/env python


def main(path):
    print "Foo", path
    raise RuntimeError("expected test failure")


def process(fd):
	# A generator which yields nothing
    return
    yield


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
