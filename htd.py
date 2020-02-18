#!/usr/bin/python3

from mca66 import *
from sys import argv

#print("------------------------")
#print("Called HTD python script")
#print("Argument 1: ", argv[1])
#print("Argument 2: ", argv[2])
#print("Argument 3: ", argv[3])


htd = mca66()

if argv[1] == "setvol":
	htd.setVol(int(argv[2]),int(argv[3]))

if argv[1] == "pwr":
	htd.setPower(int(argv[2]),int(argv[3]))

if argv[1] == "mute":
	htd.toggleMute(int(argv[2]))

if argv[1] == "querypwr":
	htd = mca66()
	detail = htd.queryZone_returndetail(int(argv[2]))

if argv[1] == "getzone":
	htd = mca66()
	detail = htd.queryZone(int(argv[2]))
