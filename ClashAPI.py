import pandas as pd
import requests
import os

class Data(object):

    def __init__(self):

        self.logWarUrl = "https://api.clashroyale.com/v1/clans/%23LR2VGVRR/warlog"
        self.infoMembers = "https://api.clashroyale.com/v1/clans/%23LR2VGVRR/members"
        self.login = {'Accept': 'application/json', 'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjM4YjBhNGFhLTFhNmMtNDE5Mi05MGM2LTJhNDI2YmMxNzVjYSIsImlhdCI6MTU5MDMzOTc5Nywic3ViIjoiZGV2ZWxvcGVyLzc0NDE1ODZiLWYzNjktNWZhYy1iYzU4LWRmYjljMTc5OGYwZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzcuNzAuMTc2LjEzMSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.qMnGABq4K9IQZh6lsy4bKMNYCvX94qQ5HWeQVLYBPodlU-XZb4lM8LrU6HcI0y-AVjxQNQ_1hsyHHYWq3nA8gQ'}

    def __getInfoWar(self):

        return requests.get(self.logWarUrl, self.login).json()

    def getInfoMembers(self):

        return requests.get(self.infoMembers, self.login).json()

    def dataProcessing(self):

        dataW = pd.DataFrame(self.__getInfoWar()["items"][0]["participants"]).drop(["battlesPlayed", "collectionDayBattlesPlayed", "numberOfBattles"], axis=1)


        dataW["Points"] = 0
        return dataW.sort_values(by=["wins", "cardsEarned"], ascending=False)


class Main(object):

    def __init__(self, infLogWar):
        self.infoLogWar = infLogWar

    def __reCalculate(self, player, ind):
        index = None

        with open("DataFinal.txt", "r") as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if player["tag"] == lines[i].split(" ")[0]:
                    aux = lines[i].split(" ")
                    cards, wins, points = int(aux[-3]), int(aux[-2]), int(aux[-1])
                    index = i

        lines.pop(index)

        string = ("%s %s %s %s %s\n"%(player["tag"], "*"+player["name"]+"*", str(int(player["cardsEarned"]+cards)),
                                    str(int(player["wins"]+wins)), str(int(points+self.__addPoint(ind)))))


        lines.append(string)

        with open("DataFinal.txt", "w") as file:

            file.writelines(lines)


    def __playerVerification(self, tag):

        with open("DataFinal.txt", "r") as file:
            if os.stat("DataFinal.txt").st_size == 0:
                return True
            else:
                line = file.readlines()

                for i in range(3):
                    if tag == line[i].split(" ")[0]:
                        return False
                    else:
                        continue
        return True

    def __addPoint(self, i):

        if i == 0:
            return 10
        elif i == 1:
            return 7
        else:
            return 5


    def saveInFile(self):

        with open("DataFinal.txt", 'a') as file:
            for i in range(3):
                if self.__playerVerification(str(self.infoLogWar.iloc[i]["tag"])):
                    self.infoLogWar.iloc[i, 4] = self.__addPoint(i)
                    file.write("%s %s %i %i %i\n"%(self.infoLogWar.iloc[i]["tag"], "*"+self.infoLogWar.iloc[i]["name"]+"*",
                                                 self.infoLogWar.iloc[i]["cardsEarned"], self.infoLogWar.iloc[i]["wins"],
                                                 self.infoLogWar.iloc[i]["Points"]))

                else:
                    self.__reCalculate(self.infoLogWar.iloc[i], i)




response = Data()
main = Main(response.dataProcessing())
df = pd.DataFrame(response.getInfoMembers()['items'])
df.to_csv("Members")
main.saveInFile()