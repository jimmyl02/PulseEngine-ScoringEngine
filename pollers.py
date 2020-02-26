import socket
import requests

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


