#this code is for calculating rating of each players an stroring them into file
#it takes json data to read 
import json
import pandas as pd

with open("use18_8.json","r") as f:
    d = f.read()

data = json.loads(d)
data_dict = {}
data_list =[]
rate = 0.00
i=0
for d in data:
    for item in d["stats"]:
        name = item["name"]
        rating = float(item["rating"])
        try:
            data_dict[name].append(rating)
        except(KeyError):
            data_dict[name] = []
            data_dict[name].append(rating)
#print(data_dict)
for d in data_dict:
    rate = round(sum(data_dict[d])/len(data_dict[d]),2)
    data_list.append({'name':d,'rating':rate,'total matches':len(data_dict[d])})
# with open("rating2.json","w", encoding='utf-8') as fd:
#      fd.write(json.dumps(data_list))
df = pd.DataFrame(data_list)
df.to_csv("rating2.csv",index=False)
print("holaa>>>>>>>>")

