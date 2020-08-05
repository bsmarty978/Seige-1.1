import json
import sqlite3
from shutil import which

JSON_FILE = "ex4aug.json"
DB_FILE = "test.db"

traffic = json.load(open(JSON_FILE))
conn = sqlite3.connect(DB_FILE)

#print(type(traffic))
c = conn.cursor()
c.execute('create table test1 (foo, bar)')
i=0
for traf in traffic:
    foo = traffic[i]["title"]
    bar = traffic[i]["result"]

    data = [foo, bar]
    c.execute('insert into test1 values (?,?)', data)

    i=i+1
print("done")
#for github 
conn.commit()
c.close()

# foo = traffic[0]["title"]
# bar = traffic[0]["result"]

# data = [foo, bar]

# c = conn.cursor()
# c.execute('create table testyyy (foo, bar)')
# c.execute('insert into testyyy values (?,?)', data)

# conn.commit()
# c.close()
