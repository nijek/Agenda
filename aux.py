from datetime import datetime
from uuid import uuid4
from json import dumps

time = "2022-08-11T17:00:00"

dic = {}
for i in range(1000000):
    dic[time + str(uuid4())] = "teste"
print(dumps(dic))