from datetime import datetime
import json
from json import JSONDecodeError
from uuid import uuid4, UUID
from sys import argv

from Key import Key
from RedBlackTree import RedBlackTree
from Tools import *


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
        try:
            uuid = UUID(date[19:])
        except ValueError:
            uuid = uuid4()

        key = Key(datetime.fromisoformat(date[:19]), uuid)
        events.put(key, event[date])
    f.close()


def add_events(event=None):
    if event is None:
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
    events_dic = tree_to_dic(events)
    f = open("events.json", "w")
    f.write(json.dumps(events_dic))
    f.close()


def delete_event(event=None):
    if event is None:
        events_list = print_events(events)
        num = int(input("Digite o número do evento que quer deletar"))
        event_key = get_nth(events, num)

    else:
        # melhorar isso
        event_key = Key(datetime.fromisoformat(event[:19]), UUID(event[19:]))
    try:
        events.delete(event_key)
        print_events(events)
    except IndexError:
        print("Esse índice não corresponde a nenhum evento")
        return


def exit_program():
    save()
    quit()


events = RedBlackTree()
load_events()

if len(argv) > 1:
    i = 0
    while i < len(argv):
        if argv[i] == "-a":
            i = i + 1
            add_events(argv[i])
        elif argv[i] == "-d":
            i = i + 1
            delete_event(argv[i])
        elif argv[i] == "-v":
            print_events(events)
        i = i + 1
    exit_program()



else:
    while True:
        options = input("v: ver eventos, a: adicionar evento, s: salvar, d: deletar evento, q: sair> ")
        match options:
            case 'v':
                print_events(events)
            case 'a':
                add_events()
            case 's':
                save()
            case 'd':
                delete_event()
            case 'q':
                exit_program()
