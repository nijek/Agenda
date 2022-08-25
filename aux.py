from datetime import datetime
from uuid import uuid4
from json import dumps
from random import randint

dic = {}
for i in range(10):
    time = datetime(randint(1900,2100), randint(1,12), randint(1,28), randint(0,23), randint(0,59)).isoformat()
    dic[time + str(uuid4())] = "teste" + str(i)
print(dumps(dic))