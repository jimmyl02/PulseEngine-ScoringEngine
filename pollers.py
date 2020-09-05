import socket
import requests
import os
from ftplib import FTP
import json
import subprocess
import hashlib

"""
Name: pollPort
Description: Will poll for a specific port and see if it is online
Parameters: ip - ip address to poll, port - port number
"""

def pollPort(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result = s.connect_ex((ip,int(port)))
    if result == 0:
      return True
    else:
      return False

"""
Name: pollHTTP
Description: Will query a url and verify that it is reachable and the md5 content of the page is what is expected
Parameters: url - complete url of the page to query (ex. https://192.168.0.1/login.html), pageHash - expected md5 hash of the page
"""

def pollHTTP(url, pageHash):
    try:
        if(hashlib.md5(requests.get(url, timeout=3).content).hexdigest() == pageHash):
            return True
        else:
            return False
    except:
        return False

"""
Name: pollSSH
Description: Will verify that the SSH service is running on the specific port
Parameters: ip - ip address to poll, port - port number to poll, users - Array of strings of format "username:password" to verify are valid
"""

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

"""
Name: pollFTP
Description: Will verify that the FTP service is running on the specific port
Parameters: ip - ip address to poll, port - port number to poll, users - Array of strings of format "username:password" to verify are valid
"""

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
