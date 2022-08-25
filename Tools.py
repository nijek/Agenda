from datetime import datetime

def print_events(tree):
    count = 0
    for (key, val) in tree.in_order_traversal():
        count += 1
        print(key.date.strftime(str(count) + ") %d/%m/%Y - %H:%M  ") + val)


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
