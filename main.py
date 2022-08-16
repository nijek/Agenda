import json
from datetime import datetime, timedelta
from json import JSONDecodeError
from BinarySearchTree import BinarySearchTree
from uuid import uuid4
from Key import Key


def load_events():
    try:
        f = open("events.json", "r")
    except FileNotFoundError:
        return

    try:
        event = json.loads(f.read())
    except JSONDecodeError:
        event = {}
    for date in event.keys():
        uuid = uuid4()
        key = Key(datetime.fromisoformat(date[:19]), uuid)
        events.put(key, event[date])
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
    uuid = uuid4()
    key = Key(event_time, uuid)
    events.put(key, event[2])


def save():
    events_dic = events.to_dic()
    f = open("events.json", "w")
    f.write(json.dumps(events_dic))
    f.close()


def delete_event():
    events_list = events.print_with_list()
    num = int(input("Digite o número do evento que quer deletar"))
    events.delete_node(events_list[num - 1])
    events.print()


def exit_program():
    save()
    quit()


events = BinarySearchTree()
load_events()

while True:
    options = input("v: ver eventos, a: adicionar evento, s: salvar, d: deletar evento, q: sair> ")
    match (options):
        case 'v':
            print_events()
        case 'a':
            add_events()
        case 's':
            save()
        case 'd':
            delete_event()
        case 'q':
            exit_program()
