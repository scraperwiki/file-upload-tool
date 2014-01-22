#! /usr/bin/env python

import cgi
import cgitb
# TODO(pwaller): Replace this with a different error reporting mechanism
# e.g, make an excepthook
cgitb.enable()
data = cgi.FieldStorage()

# End headers
print

import sys

import datetime
print "<pre>"
print "Command line arguments: ", sys.argv, data, data['Foo'].value
print
print "Hello, world ", datetime.datetime.now()
print
print open("/home/foo").read()
print "</pre>"

cgi.print_environ()

class MoronError(Exception): pass

raise MoronError("I am a moron")
