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

event_string = ""
alarm_on = False
op_it_string = "v: ver eventos, a: adicionar, s: salvar, d: deletar, " \
               "escolher som do alarme: e, sync: sincronizar, o: parar alarme, q: sair> "
alarms_path = "alarm_sounds/"
chosen_ring = alarms_path + "mixkit-scanning-sci-fi-alarm-905.mp3"
options_array = ["ver eventos", "adicionar eventos",
                 "salvar", "deletar", "sincronizar com dropbox", "parar alarme", "sair"]
currently_selected = []
def alarm_off():
    global alarm_on
    alarm_on = False


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


def retrieve_input(hour_box, day_box, description_box):
    global event_string
    hour = hour_box.get("1.0", 'end-1c')
    day = day_box.get("1.0", 'end-1c')
    description = description_box.get("1.0", 'end-1c')
    event_string = ""
    event_string = day.strip() + ";" + hour.strip() + ";" + description.strip()


def add_events_gui():
    global event_string
    add_event_window = open_centered_window("Adicionar evento", 550, 250)
    day_label = ttk.Label(add_event_window, text="Dia")
    day_label.pack()
    day_text_box = tk.Text(add_event_window, height=1, width=15)
    day_text_box.pack()

    hour_label = ttk.Label(add_event_window, text="Hora")
    hour_label.pack()
    hour_text_box = tk.Text(add_event_window, height=1, width=15)
    hour_text_box.pack()

    description_label = ttk.Label(add_event_window, text="Descri????o")
    description_label.pack()
    description_text_box = tk.Text(add_event_window, height=5, width=30)
    description_text_box.pack()
    ttk.Button(add_event_window, text="adicionar evento", width=20,
               command=lambda: [retrieve_input(hour_text_box, day_text_box,
                                               description_text_box), add_events(event_string),
                                add_event_window.destroy(),
                                refresh_listbox(main_listbox, events)]).pack(pady=15)

    add_event_window.mainloop()


def add_events(event_parameter=None):
    if event_parameter is None:
        return

    global event_string
    event_parameter = event_string
    event_string = None
    if event_parameter is None:
        return

    event_parameter = event_parameter.split(';')
    event_date_str = [int(x) for x in event_parameter[0].split("/")]
    event_time_str = [int(x) for x in event_parameter[1].split(":")]

    event_time = datetime(event_date_str[2], event_date_str[1], event_date_str[0],
                          event_time_str[0], event_time_str[1])
    uuid = uuid4()
    key = Key(event_time, uuid)
    events.put(key, event_parameter[2])


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
        num = int(input("Digite o n??mero do evento que quer deletar"))
        event_key = get_nth(events, num)

    else:
        # melhorar isso
        event_key = Key(datetime.fromisoformat(event[:19]), UUID(event[19:]))
    try:
        events.delete(event_key)
        print_events(events)
    except IndexError:
        print("Esse ??ndice n??o corresponde a nenhum evento")
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
    sync_window = open_centered_window("Sync com o Dropbox", 350, 150)
    ttk.Button(sync_window, text="Baixar a vers??o do Dropbox",
               command=lambda: [dbx.download_file(), load_events(),
                                refresh_listbox(main_listbox, events), sync_window.destroy()]).pack(pady=5)
    ttk.Button(sync_window, text="upar a vers??o para o Dropbox",
               command=lambda: [save(), dbx.upload_file(), sync_window.destroy()]).pack(pady=5)
    ttk.Button(sync_window, text="Ver menu principal",
               command=lambda: sync_window.destroy()).pack(pady=5)

    sync_window.lift()
    sync_window.attributes('-topmost', True)
    sync_window.mainloop()


def alarm():
    key_id = UUID("dc1ed4b2-1442-46d9-8ebe-3bbb5688871b")
    while True:
        events_now = events.nodes_between(Key(datetime.now() - timedelta(seconds=60), key_id),
                                          Key(datetime.now() + timedelta(seconds=60), key_id))

        if events_now:
            alarm_ring(events_now)
        sleep(60)


def refresh_listbox(listbox, events):
    listbox.delete(0, tk.END)
    events_list = get_events(events)
    for event in events_list:
        listbox.insert(tk.END, event)


def delete_events(events_now):
    for event in events_now:
        events.delete(event.key)


def delete_selected_events(listbox=None, events_list=None):
    if events_list:
        for event_index in listbox.curselection():
            events.delete(events_list[event_index].key)
        return
    curse_selection = list(listbox.curselection())
    if not curse_selection:
        return
    keys_to_delete = get_keys_by_index(events, curse_selection)
    for key in keys_to_delete:
        events.delete(key)
    return


def alarm_ring(events_now):
    alarm_window = open_centered_window("Alarme", 550, 250)
    events_alarm = []
    for event in events_now:
        events_alarm.append((event.key, event.val))
    ring_thread = Thread(target=ring, daemon=True)
    ring_thread.start()
    alarm_listbox = grid_print(alarm_window, events_alarm, height=40, width=40)
    buttom_width = 30
    ttk.Button(alarm_window, text="Ok", width=buttom_width,
               command=lambda: [alarm_off(), alarm_window.destroy()]).pack()

    ttk.Button(alarm_window, text="Deletar alarmes selecionados", width=buttom_width,
               command=lambda: [alarm_off(),
                                delete_selected_events(alarm_listbox, events_now),
                                alarm_window.destroy(), refresh_listbox(main_listbox, events)]).pack()

    ttk.Button(alarm_window, text="Deletar todos esses alarmes", width=buttom_width,
               command=lambda: [alarm_off(), alarm_window.destroy(),
                                delete_events(events_now),
                                refresh_listbox(main_listbox, events)]).pack()

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

# Parte gr??fica

main_window = open_centered_window("Agenda", 800, 600)

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

    main_listbox = grid_print(main_window, events)
    ttk.Button(main_window, text="atualizar eventos", width=20,
               command=lambda: refresh_listbox(main_listbox, events)).pack(pady=2)
    ttk.Button(main_window, text="adicionar evento", width=20,
               command=lambda: add_events_gui()).pack(pady=2)
    ttk.Button(main_window, text="deletar evento", width=20,
               command=lambda: [delete_selected_events(listbox=main_listbox),
                                refresh_listbox(main_listbox, events)]).pack(pady=2)
    ttk.Button(main_window, text="salvar", width=20,
               command=lambda: save()).pack(pady=2)
    ttk.Button(main_window, text="sincronizar com dropbox", width=20,
               command=lambda:  sync_events()).pack(pady=2)
    ttk.Button(main_window, text="parar alarme", width=20,
               command=lambda: alarm_off()).pack(pady=2)
    ttk.Button(main_window, text="sair", width=20,
               command=lambda: exit_program()).pack(pady=2)
    main_window.mainloop()
