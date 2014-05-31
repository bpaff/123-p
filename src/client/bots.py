

import os
import sys
import time
import subprocess

path = os.path.dirname(os.path.realpath(__file__))[:-7]
if path not in sys.path:
    sys.path.append(path)


print 'Loading bots....'

processes = []

for _ in range(0, 10):
    process = subprocess.Popen('python client.py True', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append(process)
    time.sleep(0.1)

print 'Bots loaded, press enter to quit'
line = sys.stdin.readline()

for process in processes:
    
    if process.poll() == None:
        os.kill(process.pid, 2)
    
    while True:
        line = process.stdout.read()
        if line == '':
            break
        print line
    
    while True:
        line = process.stderr.read()
        if line == '':
            break
        print line


