import json
from datetime import datetime, timedelta
from json import JSONDecodeError
from BST import BinarySearchTree


def load_events():
    try:
        f = open("events.json", "r")
    except FileNotFoundError:
        return

    try:
        event = json.loads(f.read())
    except JSONDecodeError:
        event = {}

    for key in event.keys():
        events.put(datetime.fromisoformat(key), event[key])
    f.close()



def print_events():
    events.print()



def add_events():
    event = input("Digite data, hora e descrição separados por ';': ")
    event = event.split(';')
    event_date_str = [int(x) for x in event[0].split("/")]
    event_time_str = [int(x) for x in event[1].split(":")]

    event_time = datetime(event_date_str[2], event_date_str[1], event_date_str[0],
                          event_time_str[0], event_time_str[1])
    while events.get(event_time):
        event_time = event_time + timedelta(seconds=1)
    events.put(event_time, event[2])



def dt_parser(dt):
    if isinstance(dt, datetime):
        return dt.isoformat()

def save():
    events_dic = events.toDic()
    f = open("events.json", "w")
    f.write(json.dumps(events_dic))
    f.close()


def exit_program():
    save()
    quit()


events = BinarySearchTree()
load_events()

while True:
    options = input("v: ver eventos, a: adicionar evento, s: salvar, d: deletar evento, q: sair> ")
    match(options):
        case 'v':
            print_events()
        case 'a':
            add_events()
        case 's':
            save()
        case 'd':
            pass
        case 'q':
            exit_program()
