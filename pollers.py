import socket
import requests
import os

def pollPort(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    result = s.connect_ex((ip,int(port)))
    if result == 0:
      return True
    else:
      return False

def pollHTTP(ip, port, hash):
    try:
        if(hashlib.md5(requests.get("http://" + ip + ":" + port, timeout=3).content).hexdigest() == hash):
            return True
        else:
            return False
    except:
        return False


def pollSSH(ip, port, users, teamName):
    try:
        with open("./users.json") as f:
            usersList = json.load(f)
            team = usersList[teamName]
            for username in team:
                if(subprocess.call("sshpass -f <(printf '%s\n'" + team[username] + ") ssh -q " +  username + "@" + ip + " -p " + port + " exit") != 0):
                    return False
            return True
    except:
        return False
