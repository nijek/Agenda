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
    events_list_sv = tk.StringVar(master=window, value=events_list)
    scroll_bar = tk.Scrollbar(window)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    events_text = tk.Listbox(window, listvariable=events_list_sv, selectmode='extended', yscrollcommand=scroll_bar.set,
                             height=height, width=width)
    events_text.pack(side=tk.RIGHT)
    scroll_bar.config(command=events_text.yview())

    return events_text


def tree_to_dic(tree):
    dic = {}
    for (key, val) in tree.in_order_traversal():
        dic[key.date.isoformat() + str(key.uuid)] = val
    return dic


def get_nth(tree, n):
    count = 0
    for key in tree.in_order_traversal_keys():
        if count == n:
            return key
        count += 1


def get_keys_by_index(tree, index_list):
    if not index_list:
        return
    keys = []
    count = 0
    index_list.sort()
    max = index_list[-1]
    min = index_list[0]
    for key in tree.in_order_traversal_keys():
        if count > max:
            break
        elif count < min:
            count += 1
            continue
        else:
            if count in index_list:
                keys.append(key)
            count += 1
    return keys


def open_centered_window(title=None, width=70, height=70):
    centered_window = tk.Tk()
    if title:
        centered_window.title(title)
        window_width = width
        window_height = height

        screen_width = centered_window.winfo_screenwidth()
        screen_height = centered_window.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        centered_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        centered_window.maxsize(screen_width, screen_height)
        return centered_window
