#!/usr/local/bin/python3.7
import os
import subprocess
import sys

RUNNING = '<html><head><META HTTP-EQUIV="Refresh" CONTENT="2; URL=."></head><body>Site is starting ... <a href=".">click here<a></body></html>'
RESTARTING='<html><head><META HTTP-EQUIV="Refresh" CONTENT="2; URL=."></head><body>Restarting site ... <a href=".">click here<a></body></html>'

def spawn(cmd):
    try:
        pid = os.fork()
        if pid > 0:
            return
    except OSError as e:
        sys.stderr.write("fork #1 failed: %d (%s)\\n" % (e.errno,
e.strerror))
        sys.exit(1)

    # decouple from parent environment
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #2 failed: %d (%s)\\n" % (e.errno,
e.strerror))
        sys.exit(1)

    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = open('/dev/null', 'r')
    so = open('/dev/null', 'a+')
    se = open('/dev/null', 'a+', 1)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    pid = subprocess.Popen(cmd, shell=True).pid

    # write pidfile
    with open('/home/trackable/webapps/squanchy/pid', 'w') as f: f.write(str(pid))
    sys.exit(1)

# Test if the process is already running
running = False
try:
    # Try to read pid file
    pid = open('/home/trackable/webapps/squanchy/pid').read()
    # Check if this process is up
    lines = os.popen('ps -p %s' % pid).readlines()
    if len(lines) > 1:
        running = True
    else:
        # Delete pid file
        os.remove('/home/trackable/webapps/squanchy/pid')
except IOError:
    pass


if running:
    sys.stdout.write("Content-type: text/html\n\n")
    sys.stdout.write(RUNNING)
else:
    spawn("/usr/local/bin/python3.7 /home/trackable/webapps/squanchy/site.py")
    sys.stdout.write("Content-type: text/html\n\n")
    sys.stdout.write(RESTARTING)

