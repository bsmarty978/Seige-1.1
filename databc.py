import json
import sqlite3
from shutil import which

JSON_FILE = "rating2.json"
DB_FILE = "test.db"

traffic = json.load(open(JSON_FILE))
conn = sqlite3.connect(DB_FILE)

#print(type(traffic))
c = conn.cursor()
c.execute('create table test2 (name, rating, total_matches)')
i=0
for traf in traffic:
    name = traffic[i]["name"]
    rating = traffic[i]["rating"]
    total_matches = traffic[i]["total matches"]

    data = [name, rating, total_matches]
    c.execute('insert into test2 values (?,?,?)', data)

    i=i+1
print("done")
#for github 
conn.commit()
c.close()
conn.close
