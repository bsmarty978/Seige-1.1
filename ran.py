import random
randomlist = []
playerlist = {"Yung":1.04, "nvK":1.13, "Necrox":1.11, "Canadian":1.26, "geoo":0.90,"Hotancold":0.96, "Nyx":1.07, "POJOMAN":0.84, "Mint":1.16, "Jarvis":0.67}
player = ["Yung", "nvK", "Necrox", "Canadian", "geoo","Hotancold", "Nyx", "POJOMAN", "Mint","Jarvis"]

#RANDOM TEAM GENRATER FOR ANALTZING PURPOSE
lim = 0
while(lim<10):
    lis = random.sample(range(0,10),5)
    randomlist.append(lis)
    lim = lim +1

for l in randomlist:
    team = []
    for j in l:
        team.append((player[j]))
    total_rate = 0
    cap = 0
    j= 0
    for i in team:
        rat = playerlist[i]
        if j == 0 :
            cap = rat*100*2
            j = j+1
        else:
            total_rate = total_rate + rat*100
    if total_rate+cap < 699:
        print(team,">>",total_rate+cap)
        print("__________")
## THIS END HERE

#FOR SURVEY OR OTHER DATA THAT TAKEN REAL