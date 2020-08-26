#!/usr/bin/python
import subprocess
import json

strings = subprocess.Popen("docker ps", shell=True, stdout=subprocess.PIPE).stdout.readlines()

l=list()
for i in range(1,len(strings)):
    pstring = strings[i].split()
    d=dict()
    d["{#ZD_ID}"]=pstring[0]
    d["{#ZD_IMAGE}"]=pstring[1]
    d["{#ZD_NAME}"]=pstring[-1]
    l.append(d)
    s_json=dict()
    s_json["data"]=l

print json.dumps(s_json)


