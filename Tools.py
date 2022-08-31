from datetime import datetime
import tkinter as tk
from tkinter import ttk

def get_events(container):
    text = ""
    count = 0
    if type(container) is list:
        y = container
    else:
        y = container.in_order_traversal()
    for (key, val) in y:
        count += 1
        text += key.date.strftime(str(count) + ") %d/%m/%Y - %H:%M  ") + val + "\n"
    return (text, count)

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

    scroll_bar = tk.Scrollbar(window)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    events_text = tk.Text(window, height=height, width=width, yscrollcommand=scroll_bar.set)
    events_text.pack(side=tk.RIGHT)
    scroll_bar.config(command=events_text.yview())
    events = get_events(container)[0]
    events_text.insert(tk.END, events)
    i += 1
    return i

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
