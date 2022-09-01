from datetime import datetime
import tkinter as tk
from tkinter import ttk

def get_events(container):
    events_list = []
    count = 0
    if type(container) is list:
        y = container
    else:
        y = container.in_order_traversal()
    for (key, val) in y:
        count += 1
        events_list.append(key.date.strftime(str(count) + ") %d/%m/%Y - %H:%M  ") + val)
    print(">>>", type(events_list))
    return events_list

def get_each_event(container):
    count = 0
    if type(container) is list:
        y = container
    else:
        y = container.in_order_traversal()
    for (key, val) in y:
        count += 1
        yield key.date.strftime(str(count) + ") %d/%m/%Y - %H:%M  ") + val


def print_events(tree):
    count = 0
    for (key, val) in tree.in_order_traversal():
        count += 1
        print(key.date.strftime(str(count) + ") %d/%m/%Y - %H:%M  ") + val)

def grid_print(window, container, height=40, width=70):
    i = 1
    events_list = get_events(container)
    print(events_list)
    events_list_sv = tk.StringVar(master=window, value=events_list)
    scroll_bar = tk.Scrollbar(window)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    events_text = tk.Listbox(window, listvariable=events_list_sv, selectmode='extended', yscrollcommand=scroll_bar.set, height=height, width=width)
    events_text.pack(side=tk.RIGHT)
    scroll_bar.config(command=events_text.yview())

    return events_text

def tree_to_dic(tree):
    dic = {}
    for (key, val) in tree.in_order_traversal():
        dic[key.date.isoformat() + str(key.uuid)] = val
    return dic


def get_nth(tree, n):
    count = 1
    for key in tree.in_order_traversal_keys():
        if count == n:
            return key
        count += 1
