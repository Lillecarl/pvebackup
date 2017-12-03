#!/usr/bin/python

import sys
import os

os.environ["DUPLICACY_B2_ID"] = ""
os.environ["DUPLICACY_B2_KEY"] = ""
targeturlkvm = "/var/lib/vz/targetkvm"
targeturllxc = "/var/lib/vz/targetlxc"

print  sys.argv[1:]

task = sys.argv[1]

if task == "backup-end":
    vm = sys.argv[3]
    vmtype = os.environ["VMTYPE"]
    dumpdir= os.environ["DUMPDIR"]
    tarfile = os.environ["TARFILE"]
    duplirepo = os.path.join(dumpdir,vm)
    print tarfile

    if not os.path.isdir(duplirepo):
        os.makedirs(duplirepo)
        os.chdir(duplirepo)

        if vmtype == "qemu":
            os.system("duplicacy init -min-chunk-size 65536 -max-chunk-size 65536 -chunk-size 65536 " + vm + " " + targeturlkvm)
        else:
            os.system("duplicacy init " + vm + " " + targeturllxc)

    os.chdir(duplirepo)
    newtarfile = tarfile.replace(dumpdir,duplirepo)
    os.rename(tarfile, newtarfile)
    os.system("duplicacy backup -threads 40")
    os.remove(newtarfile)

if task == "log-end":
    dumpdir = os.environ["DUMPDIR"]
    logfile = os.environ["LOGFILE"]
    logdir = os.path.join(dumpdir, "logs")

    if not os.path.isdir(logdir):
        os.makedirs(logdir)

    os.rename(logfile, logfile.replace(dumpdir, logdir))
