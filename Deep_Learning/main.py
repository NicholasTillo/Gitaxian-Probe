
import json
dataRaw = open("Deeplearning/default-cards-20240302220650.json", encoding="utf-8")
dataLoaded = json.load(dataRaw)
x = dataLoaded[3].keys()

for i in dataLoaded:
    print(type(i["legalities"]))
    break


