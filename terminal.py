import os
import time
import subprocess
from queue import Queue, Empty
import threading
import sys
from threading import Thread
import fcntl
ON_POSIX = 'posix' in sys.builtin_module_names


class Terminal:
    def __init__(self, command):
        self.command = command + " 2>&1"

        cmd = self.command
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, env=os.environ.copy())
        fd = proc.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        self.last_out = ""
        self.proc = proc
        self.consumed = ""
       
    def poll(self):
        dec = ""
        time.sleep(0.6)
        stdout = self.proc.stdout.read()
        #print(stdout)
        if stdout: 
            d = stdout.decode("utf-8")
            dec += d
            self.consumed += d
        if stdout == self.last_out and self.last_out != "":
            print(self.consumed)
            print("[Requesting input]")
            return True, self.consumed # Input required
        self.last_out = stdout

    def send(self, text, line=True):
        if line: text += "\n"
        self.proc.stdin.write(bytes(text, "utf-8"))
        self.consumed = ""
        self.proc.stdin.flush()


terminal = Terminal("bash")

while True:
    if terminal.poll():
        terminal.send(input())







        
        


