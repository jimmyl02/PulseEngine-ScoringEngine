# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 22:09:39 2019

@author: jimmy
"""

import json
import socket
import time
import requests
import hashlib

loadedConfig = {}

def loadConfig():
    
    global loadedConfig

    with open("./config.json", "r") as f:
        
        try:
            loadedConfig = json.load(f)
        
        except:
            
            print("Failed to load config")
        
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

def runCheck():
    
    for teamName in loadedConfig:
        
        scoredObjects = loadedConfig[teamName]["scoredObjects"]
        
        for scoredObject in scoredObjects:
            
            if scoredObject["type"] == "port":
                
                scoredObject["checksAttempt"] += 1
                scoredObject["prevCheck"] = False
                
                try:
                    
                    result = pollPort(scoredObject["host"], scoredObject["port"])
                    
                    if result == True:
                        
                        scoredObject["checksUp"] += 1
                        scoredObject["prevCheck"] = True
                    
                except:
                    
                    print("Port poll failed, likely fault in parameters")
                
            else:
                
                print("Unknown type, nothing happening")
                
def genHTML():
    
    template = """
    <html>
<style>
        body{
            background-color:black;
            color:white;
            text-align:center;
            font-family: Verdana, sans-serif;
        }
        .heading{
            margin-top: 20px;
            margin-bottom: 20px;
            font-size: 25px;
        }
        #wrapper {
            margin-bottom: 50px;
        }
        #wrapper,#wrapper2 {
            margin-left: auto;
            margin-right: auto;
            width: 900px;
        }
        #console {
            height: 400px;
            width: 800px;
            background: #242424;
            margin-left: auto;
            margin-right: auto;
            margin-top: 10px;
            text-align: left;
            font-family: "Courier New", Courier, monospace;
            font-size: 10pt;
        }
        .row{
            height: 30px;
            width: 100%;
        }

        .block{
            display: block;
            float: left;
            width: 19.8%;
            height: 100%;
            margin-right: 1px;
            margin-bottom: 1px;
            background: gray;
        }
        .block_center{
            line-height: 25px;
        }


        .up {
            background: #006500;
        }
        .down {
            background: #ca0000;
        }

        .clearfix:after {
            content: ".";
            display: block;
            clear: both;
            visibility: hidden;
            line-height: 0;
            height: 0;
        }

        .clearfix {
            display: inline-block;
        }

        html[xmlns] .clearfix {
            display: block;
        }

        * html .clearfix {
            height: 1%;
        }
        a:link
        {
        color:#FF0000;
        }

        a:visited
        {
        color:#FFFFFF;
        }

        a:hover
        {
        color:#00FDF5;
        }


    </style>

    <div id="wrapper">
        <div class="heading">Troy HS CCDC Scoring Engine v1.0<br></div>
        <div class="heading">Last Update: """ + time.ctime() +  """</div>
        <div class="row">
            <div class="block">
                <div class="block_center">Team</div>
            </div>
            <div class="block">
                <div class="block_center">Service</div>
            </div>
            <div class="block">
                <div class="block_center">Attempts</div>
            </div>
            <div class="block">
                <div class="block_center">Successful</div>
            </div>
            <div class="block">
                <div class="block_center">Uptime</div>
            </div>
        </div>
    	
    """
    for teamName in loadedConfig:
        
        scoredObjects = loadedConfig[teamName]["scoredObjects"]
        
        for scoredObject in scoredObjects:
            
            template += """<div class="row">"""
            
            template += """    <div class="block">"""
            
            template += """        <div class="block_center">""" + teamName + """</div>"""
            
            template += """    </div>"""
            
            if scoredObject["prevCheck"] == True:
                
                template += """    <div class="block up">"""
                
                template += """        <div class="block_center">""" + scoredObject["displayName"] + """</div>"""
                
                template += """    </div>"""
                
            else:
                
                template += """    <div class="block down">"""
                
                template += """        <div class="block_center">""" + scoredObject["displayName"] + """</div>"""
                
                template += """    </div>"""
                
            template += """    <div class="block">"""
            
            template += """        <div class="block_center">""" + str(scoredObject["checksAttempt"]) + """</div>"""
            
            template += """    </div>"""
            
            template += """    <div class="block">"""
            
            template += """        <div class="block_center">""" + str(scoredObject["checksUp"]) + """</div>"""
            
            template += """    </div>"""
            
            template += """    <div class="block">"""
            
            template += """        <div class="block_center">""" + str(round(100 * float(scoredObject["checksUp"]) / float(scoredObject["checksAttempt"]), 3)) + """% </div>"""
            
            template += """    </div>"""
            
            template += """</div>"""
        
    template += """
    
    By: Jimmy Li and Christo Bakis, contact us if anything is broken
    
        </div>
    
    </html>
    """
    
    with open("./index.html", "w+") as f:
        
        f.write(template)
        
def saveConfig():
    
    with open("./config_save.json", "w+") as f:
        
        json.dump(loadedConfig, f)

loadConfig()

sleepTime = 30

while True:
    
    runCheck()
    genHTML()
    saveConfig()
    time.sleep(30)
