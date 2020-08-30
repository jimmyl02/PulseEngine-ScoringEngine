# -*- coding: utf-8 -*-
"""
CCDC Scoring Engine

@author: jimmy
"""

import json
import time
import requests
import pollers

from pollers import pollPort, pollHTTP, pollSSH, pollFTP

compId = None
apikey = None
teams = []

def loadConfig():
    global compId, apikey, teams
    loadedConfig = {}

    with open("./config.json", "r") as f:
        try:
            loadedConfig = json.load(f)
            compId = loadedConfig["compId"]
            apikey = loadedConfig["apikey"]
            teams = loadedConfig["teams"]
        except:
            print("[!] Failed to load config")

def sendStatus(teamName, teamServices):
    print(teamName)
    print(teamServices)

def runCheck():
    for team in teams:
        teamname = team["teamname"]
        teamServices = []
        scoreObjects = team["scoredObjects"]
        for scoreObject in scoreObjects:
            if scoreObject["type"] == "port":
                try:
                    result = pollPort(scoreObject["host"], scoreObject["port"])
                    scoredServiceObject = {}
                    scoredServiceObject["name"] = scoreObject["displayName"]
                    scoredServiceObject["status"] = result
                    teamServices.append(scoredServiceObject)
                except Exception as e:
                    print("[!] Port poll failed, likely fault in parameters")
                    print("Detailed exception: " + str(e))
            elif scoreObject["type"] == "http":
                try:
                    result = pollHTTP(scoreObject["host"], scoreObject["port"], scoreObject["md5"])
                    scoredServiceObject = {}
                    scoredServiceObject["name"] = scoreObject["displayName"]
                    scoredServiceObject["status"] = result
                    teamServices.append(scoredServiceObject)
                except Exception as e:
                    print("[!] HTTP poll failed, likely fault in parameters")
                    print("Detailed exception: " + str(e))
            elif scoreObject["type"] == "ftp":
                try:
                    result = pollFTP(scoreObject["host"], scoreObject["port"], scoreObject["users"]) # users must be an array of strings with format username:password
                    scoredServiceObject = {}
                    scoredServiceObject["name"] = scoreObject["displayName"]
                    scoredServiceObject["status"] = result
                    teamServices.append(scoredServiceObject)
                except Exception as e:
                    print("[!] FTP poll failed, likely fault in parameters")
                    print("Detailed exception: " + str(e))
            elif scoreObject["type"] == "ssh":
                try:
                    result = pollSSH(scoreObject["host"], scoreObject["port"], scoreObject["users"]) # users must be an array of strings with format username:password
                    scoredServiceObject = {}
                    scoredServiceObject["name"] = scoreObject["displayName"]
                    scoredServiceObject["status"] = result
                    teamServices.append(scoredServiceObject)
                except Exception as e:
                    print("[!] SSH poll failed, likely fault in parameters")
                    print("Detailed exception: " + str(e))
            else:
                print("Unknown poll type, service was skipped")

        sendStatus(teamname, teamServices)

def main():
    loadConfig()
    print("[*] Config loaded, beginning scoring now")
    while True:
        runCheck()
        time.sleep(10)

if __name__ == "__main__":
    main()