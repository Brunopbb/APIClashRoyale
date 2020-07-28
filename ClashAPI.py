#!/usr/bin/python

import pandas as pd
import numpy as np
import requests
import os

locationDataFinal = "/home/bruno/Documentos/clash/APIClashRoyale/DataFinal.csv"
locationWarStatus = "/home/bruno/Documentos/clash/APIClashRoyale/stateWar.txt"
locationMembers = "/home/bruno/Documentos/clash/APIClashRoyale/Members.csv"
locationelder = "/home/bruno/Documentos/clash/APIClashRoyale/elder.csv"

class Request(object):
    def __init__(self):
        self.__logWarUrl = "https://api.clashroyale.com/v1/clans/%23LR2VGVRR/warlog"
        self.__infoMembers = "https://api.clashroyale.com/v1/clans/%23LR2VGVRR/members"
        self.__urlCurrentWar = "https://api.clashroyale.com/v1/clans/%23LR2VGVRR/currentwar"

        self.__login = {'Accept': 'application/json',
                      'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjM3OGZkYmJjLTVjOWUtNDVhMy1hNjQyLTEwZWEwNjdjNjI1YiIsImlhdCI6MTU5NTc3NjQ2OCwic3ViIjoiZGV2ZWxvcGVyLzc0NDE1ODZiLWYzNjktNWZhYy1iYzU4LWRmYjljMTc5OGYwZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzcuNzAuMTc3Ljk5Il0sInR5cGUiOiJjbGllbnQifV19.FFczPDyFxTYH7CYAnn_bru6c_BMG1TjH0B9HQ-bKU6xf19f_WnI27pgJMusk_rbGSQcRGIet9LePsgvSfNnrrQ'}

    def getInfoWar(self):
        return requests.get(self.__logWarUrl, self.__login).json()

    def getInfoMembers(self):
        return requests.get(self.__infoMembers, self.__login).json()

    def getCurrentWarStatus(self):

        return requests.get(self.__urlCurrentWar, self.__login).json()


class dataProcessing(object):

    def __init__(self, infoLogWar, infoMembers):

        self.__infoLogWar = infoLogWar
        self.__infoMembers = infoMembers

    def __settingsWar(self):

        dataW = pd.DataFrame(self.__infoLogWar["items"][0]["participants"]).drop(["battlesPlayed", "collectionDayBattlesPlayed", "numberOfBattles"], axis=1)

        aux = dataW.loc[(dataW["name"] == "Bruno") | (dataW["name"] == "Candio") | (dataW["name"] == "FB.GG/Boigas")]
        dataW.drop(aux.index, inplace=True)
        dataW["Points"] = 0

        return dataW.sort_values(by=["wins", "cardsEarned"], ascending=False)


    def settingsMembers(self):

        members = pd.DataFrame(self.__infoMembers["items"])
        aux = members.loc[(members["name"] == "Bruno") | (members["name"] == "Candio") | (members["name"] == "FB.GG/Boigas")]
        members.drop(aux.index, inplace=True)
        return members.drop(["lastSeen", "arena", "clanRank", "previousClanRank", "donationsReceived", "clanChestPoints"], axis=1).sort_values(by=["donations"], ascending=False)

    def __verificationFile(self, file):

        if os.path.exists(file):
            return True
        return False

    def main(self):

        if self.__verificationFile(locationDataFinal):

            dfAtual = self.__addPoints()

            dfFinal = pd.read_csv(locationDataFinal).drop("Unnamed: 0", axis=1)
            self.__verificationPlayer(dfFinal, dfAtual)

            dfFinal.to_csv(locationDataFinal)


        else:

            self.__saveFile(self.__addPoints())

    def __saveFile(self, file):
        file.to_csv(locationDataFinal)

    def __addPoints(self):

        rank = self.__settingsWar()

        rank.iloc[0, 4] += 10
        rank.iloc[1, 4] += 7
        rank.iloc[2, 4] += 5

        return rank

    def analyze(self):

        elder = self.settingsMembers()

        elder = elder[elder["role"] == "elder"]

        elder.to_csv(locationelder)


    def __verificationPlayer(self, file, dfAtual):

        size = file.shape[0] + 1
        dfTemp = dfAtual
        for i in range(dfTemp.shape[0]):
            if dfTemp.iloc[i]["tag"] not in np.array(file["tag"]):
                file.loc[size] = dfTemp.iloc[i]
                size += 1
            else:  # ESSE ELSE PODE SER MELHORADO

                file.loc[file["tag"] == dfTemp.iloc[i]["tag"], "wins"] += dfTemp.iloc[i, 3]
                file.loc[file["tag"] == dfTemp.iloc[i]["tag"], "cardsEarned"] += dfTemp.iloc[i, 2]

                if i == 0:
                    file.loc[file["tag"] == dfTemp.iloc[i]["tag"], "Points"] += 10
                elif i == 1:
                    file.loc[file["tag"] == dfTemp.iloc[i]["tag"], "Points"] += 7
                elif i == 2:
                    file.loc[file["tag"] == dfTemp.iloc[i]["tag"], "Points"] += 5



        file.sort_values(by=["Points", "wins", "cardsEarned"], inplace=True, ascending=False)


response = Request()

data = dataProcessing(response.getInfoWar(), response.getInfoMembers())

#current = response.getCurrentWarStatus()["state"]
current = "collectionDay" #linha de debug

control = 0

file = open(locationWarStatus, "r")
aux = file.readlines()[0].split(" ")
file.close()

if current != aux[0]:

    file = open(locationWarStatus, "w")

    control = int(aux[1]) + 1

    if control == 2:

        control = 0

        file.write(current + " " + str(control))
        data.main()
        data.analyze()

    else:

        file.write(current + " " + str(control))

data.settingsMembers().to_csv(locationMembers)

file.close()













