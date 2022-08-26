from datetime import datetime, timedelta
from uuid import uuid4
from json import dumps
from random import randint

dic = {}
for i in range(10):
    time = datetime(randint(1900,2100), randint(1,12), randint(1,28), randint(0,23), randint(0,59)).isoformat()
    dic[time + str(uuid4())] = "teste" + str(i)


for i in range(5):

    time = (datetime.now() + timedelta(minutes=i)).isoformat()
    dic[time + str(uuid4())] = "testenow" + str(i)

print(dumps(dic))