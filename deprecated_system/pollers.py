import socket
import requests
import os
from ftplib import FTP
import json
import subprocess
import hashlib

def pollPort(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result = s.connect_ex((ip,int(port)))
    if result == 0:
      return True
    else:
      return False

def pollHTTP(ip, port, pageHash):
    try:
        if(hashlib.md5(requests.get("http://" + ip + ":" + port, timeout=3).content).hexdigest() == pageHash):
            return True
        else:
            return False
    except:
        return False


def pollSSH(ip, port, users):
    try:
        for user in users:
            if ":" not in user:
                continue
            username = user.split(":")[0]
            password = user.split(":")[1]
            if(subprocess.call("sshpass -p \"" + password + "\" ssh -q -o \"UserKnownHostsFile=/dev/null\" -o \"StrictHostKeyChecking=no\" " +  username + "@" + ip + " -p " + port + " exit", shell=True) != 0):
                    return False
        return True
    except:
        return False


def pollFTP(ip, port, users):
    try:
        ftp = FTP()
        ftp.connect(ip, int(port), timeout=3)
        for user in users:
            if ":" not in user:
                continue
            username = user.split(":")[0]
            password = user.split(":")[1]
            ftp.login(username, password)
        return True
    except:
        return False
