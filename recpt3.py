#!/usr/local/bin/python

import sys
import os
import json
import subprocess
import time

def load_channel_list():
    f = open("channel.json","r")
    j = f.read()
    f.close()
    ch = json.loads(j)
    if not ch.has_key("channels"):
        return None
    return ch["channels"]

def usage():
    print "%s [device] [channel]" % (sys.argv[0])

def tunning(dev,ch):
    mib = "dev.ptx.0.%s.freq" % (dev)
    subprocess.call("sysctl %s=%d > /dev/null 2>&1" % (mib,ch["freq"]),shell=True)
    # wait for reception to stabilize
    time.sleep(5)

def recording(dev):
    dev = "/dev/ptx0.%s" % dev
    f = open(dev,"rb")
    while True:
        buf = f.read(1024)
        sys.stdout.write(buf)

def main(argv):
    if len(argv) < 3:
        usage()
        return

    channel = load_channel_list()

    if channel is None:
        print "invalid channel.json"
        return -1

    node = argv[1]
    ch = argv[2]

    if not channel.has_key(ch):
        print "channel '%s' is not defined" % ch
        return -2

    ch = channel[ch]
    tunning(node, ch)
    recording(node)
    
    return 0

if __name__ == "__main__":
    exit(main(sys.argv))
