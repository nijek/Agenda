from time import sleep
from datetime import timedelta
import json
from json import JSONDecodeError
from uuid import uuid4, UUID
from sys import argv
from threading import *
from playsound import playsound
from Key import Key
from RedBlackTree import RedBlackTree
from Tools import *
from dbx import *
from os import listdir
from os.path import isfile, join

alarm_on = False
op_it_string = "v: ver eventos, a: adicionar, s: salvar, d: deletar, " \
               "escolher som do alarme: e, sync: sincronizar, o: parar alarme, q: sair> "
alarms_path = "alarm_sounds/"
chosen_ring = alarms_path + "mixkit-scanning-sci-fi-alarm-905.mp3"
options_array = ["ver eventos", "adicionar eventos",
          "salvar", "deletar", "sincronizar com dropbox", "parar alarme", "sair"]

def button_clicked(option):
    print("Buttom clicked: " + option)
    options(option)


def options(option=None):
    if option is None:
        option = input(op_it_string)
    match option:
        case 'v':
            print_events(events)
        case 'a':
            add_events()
        case 'e':
            load_alarms()
        case 's':
            save()
        case 'd':
            delete_event()
        case 'q':
            exit_program()
        case 'sync':
            sync_events()
        case 'o':
            global alarm_on
            alarm_on = False
            pass


def load_alarms():
    alarms = [f for f in listdir(alarms_path) if isfile(join(alarms_path, f))]
    # todo
    for alarm in alarms:
        pass


def load_events():
    try:
        f = open("events.json", "r")
    except FileNotFoundError:
        return

    try:
        event = json.loads(f.read())
    except JSONDecodeError:
        event = {}
    events.clear_tree()
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
    if dbx.is_logged():
        dbx.upload_file()
    f.close()


def delete_event(event=None):
    if event is None:
        print_events(events)
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


def sync_events():
    if not dbx.is_logged():
        try:
            dbx.login()
        except Exception:
            return

    op = input("b: baixar a versão do dropbox, u: upar a versão para o dropbox, m:ver menu principal: ")
    if op == "b":
        dbx.download_file()
        load_events()
    elif op == "u":
        save()
        dbx.upload_file()
    elif op == "m":
        return
    return


def alarm():
    key_id = UUID("dc1ed4b2-1442-46d9-8ebe-3bbb5688871b")
    while True:
        events_now = events.nodes_between(Key(datetime.now() - timedelta(seconds=60), key_id),
                                          Key(datetime.now() + timedelta(seconds=60), key_id))

        if events_now:
            alarm_ring(events_now)
        sleep(60)


def alarm_ring(events_now):
    print("ALARME")
    alarm_window = tk.Tk()
    alarm_window.title("ALARME")
    window_width = 500
    window_height = 200


    screen_width = alarm_window.winfo_screenwidth()
    screen_height = alarm_window.winfo_screenheight()


    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)


    alarm_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    events_alarm = []
    for event in events_now:
        events_alarm.append((event.key, event.val))
    ring_thread = Thread(target=ring, daemon=True)
    ring_thread.start()
    i = grid_print(alarm_window, events_alarm, height= 40, width=40)
    ttk.Button(alarm_window, text="Ok", width=20, command=lambda: [button_clicked("o"), alarm_window.destroy()]).pack()

    alarm_window.lift()
    alarm_window.attributes('-topmost', True)

    alarm_window.mainloop()
    return


def ring():
    global alarm_on
    alarm_on = True
    while alarm_on:
        playsound(chosen_ring)
    return

dbx = Dbx()
events = RedBlackTree()
load_events()

#Parte gráfica

window = tk.Tk()
window.title("Agenda")
window_width = 800
window_height = 600

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
window.minsize(200, 300)
window.maxsize(screen_width, screen_height)


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
    alarm_thread = Thread(target=alarm, daemon=True)
    alarm_thread.start()

    grid_print(window, events)
    ttk.Button(window, text="ver eventos", width=20, command=lambda: button_clicked("v")).pack(pady=2)
    ttk.Button(window, text="adicionar evento",width=20, command=lambda: button_clicked("a")).pack(pady=2)
    ttk.Button(window, text="deletar evento", width=20,command=lambda: button_clicked("d")).pack(pady=2)
    ttk.Button(window, text="sincronizar com dropbox", width=20,command=lambda: button_clicked("sync")).pack(pady=2)
    ttk.Button(window, text="parar alarme", width=20,command=lambda: button_clicked("o")).pack(pady=2)
    ttk.Button(window, text="sair", width=20,command=lambda: button_clicked("q")).pack(pady=2)
    window.mainloop()
