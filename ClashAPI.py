import pandas as pd
import numpy as np
import requests
import os


class Request(object):

    def __init__(self):
        self.logWarUrl = "https://api.clashroyale.com/v1/clans/%23LR2VGVRR/warlog"

        self.login = {'Accept': 'application/json',
                      'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjM4YjBhNGFhLTFhNmMtNDE5Mi05MGM2LTJhNDI2YmMxNzVjYSIsImlhdCI6MTU5MDMzOTc5Nywic3ViIjoiZGV2ZWxvcGVyLzc0NDE1ODZiLWYzNjktNWZhYy1iYzU4LWRmYjljMTc5OGYwZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzcuNzAuMTc2LjEzMSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.qMnGABq4K9IQZh6lsy4bKMNYCvX94qQ5HWeQVLYBPodlU-XZb4lM8LrU6HcI0y-AVjxQNQ_1hsyHHYWq3nA8gQ'}

    def getInfoWar(self):
        return requests.get(self.logWarUrl, self.login).json()


class dataProcessing(object):

    def __init__(self, infoLogWar):

        self.__infoLogWar = infoLogWar

    def __settings(self):

        dataW = pd.DataFrame(self.__infoLogWar["items"][0]["participants"]).drop(
            ["battlesPlayed", "collectionDayBattlesPlayed", "numberOfBattles"], axis=1)

        dataW["Points"] = 0
        return dataW.sort_values(by=["wins", "cardsEarned"], ascending=False)

    def __verificationFile(self):

        if os.path.exists("DataFinal.csv"):
            return True
        return False

    def main(self):

        if self.__verificationFile():

            self.__addPoints()
            dfFinal = pd.read_csv("DataFinal.csv").drop("Unnamed: 0", axis=1)
            self.__verificationPlayer(dfFinal)

            dfFinal.to_csv("DataFinal.csv")


        else:

            self.__saveFile(self.__addPoints())

    def __saveFile(self, file):
        file.to_csv("DataFinal.csv")

    def __addPoints(self):

        rank = self.__settings()

        rank.iloc[0, 4] += 10
        rank.iloc[1, 4] += 7
        rank.iloc[2, 4] += 5

        return rank

    def __verificationPlayer(self, file):

        size = file.shape[0] + 1
        dfTemp = self.__settings()

        for i in range(dfTemp.shape[0]):
            if dfTemp.iloc[i]["tag"] not in np.array(file["tag"]):
                file.loc[size] = dfTemp.iloc[i]
                size += 1
            else:  # ESSE ELSE PODE SER MELHORADO
                if i == 0:
                    file.loc[file["tag"] == dfTemp.iloc[i]["tag"], "Points"] += 10
                elif i == 1:
                    file.loc[file["tag"] == dfTemp.iloc[i]["tag"], "Points"] += 7
                elif i == 2:
                    file.loc[file["tag"] == dfTemp.iloc[i]["tag"], "Points"] += 5

        file.sort_values(by=["Points"], inplace=True, ascending=False)

    '''
    def updateValues(self, file):

        dfTemp = self.__settings()

        file.set_index("tag", inplace=True)
        dfTemp.set_index("tag", inplace=True)

        file["wins"] = (file["wins"] + dfTemp["wins"])
        file["cardsEarned"] = (file["cardsEarned"] + dfTemp["cardsEarned"])
        file.reset_index(inplace=True)

    '''


response = Request()

data = dataProcessing(response.getInfoWar())

data.main()

