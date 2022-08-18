from datetime import datetime
from uuid import uuid4
from json import dumps
from random import randint

time = "2022-08-11T17:00:00"

dic = {}
for i in range(1000000):
    time = datetime(randint(1950,2100), randint(1,12), randint(1,28), randint(0,23), randint(0,59)).isoformat()
    dic[time + str(uuid4())] = "teste"
print(dumps(dic))