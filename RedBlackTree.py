"""
Fortemente inspirada na implementação do professor Sedgewick
https://algs4.cs.princeton.edu/33balanced/RedBlackBST.java.html
"""
import datetime

RED = True
BLACK = False


# static helpers
def is_red(x):
    if x is None:
        return False
    return x.color == RED


def size(x):
    if x is None:
        return 0
    return x.size


# static getters
def _get(node, key):
    while node is not None:
        if key < node.key:
            node = node.left
        elif key > node.key:
            node = node.right
        else:
            return node.val
    return None


def _get_ceiling(node, key):
    # Base Case
    if node is None:
        return None

    if node.key == key:
        return node.key

        # If root's key is smaller, ceil must be in right subtree
    if node.key < key:
        return _get_ceiling(node.right, key)

        # Else, either left subtree or root has the ceil value
    val = _get_ceiling(node.left, key)
    if val is None or val < key:
        return node.key
    return val


def rotate_left(node):
    x = node.right
    node.right = x.left
    x.left = node
    x.color = node.color
    node.color = RED
    x.size = node.size
    node.size = size(node.left) + size(node.right) + 1
    return x


def rotate_right(node):
    x = node.left
    node.left = x.right
    x.right = node
    x.color = node.color
    node.color = RED
    x.size = node.size
    node.size = size(node.left) + size(node.right) + 1
    return x


def flip_colors(node):
    node.color = not node.color
    node.left.color = not node.left.color
    node.right.color = not node.right.color


def move_red_left(node):
    flip_colors(node)
    if is_red(node.right.left):
        node.right = rotate_right(node.right)
        node = rotate_left(node)
        flip_colors(node)
    return node


def move_red_right(node):
    flip_colors(node)
    if is_red(node.left.left):
        node = rotate_right(node)
        flip_colors(node)
    return node


def balance(node):
    if node is None:
        return
    if (is_red(node.right) and (not is_red(node.left))):
        node = rotate_left(node)
    if (is_red(node.left) and is_red(node.left.left)):
        node = rotate_right(node)
    if (is_red(node.left) and is_red(node.right)):
        flip_colors(node)
    node.size = size(node.left) + size(node.right) + 1

    return node


def _height(node):
    if node is None:
        return -1
    return 1 + max(_height(node.left), _height(node.right))


class RedBlackTree:
    class Node:
        def __init__(self, key=None, val=None, color=None, size=0):
            self.key = key
            self.val = val
            self.left = None
            self.right = None
            self.color = color
            self.size = size

    def __init__(self):
        self.root = None

    def clear_tree(self):
        self.root = None

    def get_root(self):
        return self.root

    # helpers
    def tree_size(self):
        return size(self.root)

    def is_empty(self):
        return self.root is None

    def get(self, key):
        if key is None:
            print("Erro: key = None")
            return None
        return _get(self.root, key)

    def node_max(self):
        if self.root is None:
            return None
        node = self.root
        while node.right is not None:
            node = node.right
        return node

    def get_ceiling(self, key):
        if key is None:
            print("Erro: key = None")
            return None
        ceil = self.ceil(self.root, key)
        if ceil is None:
            return ceil
        return ceil if ceil.key >= key else None

    def get_floor(self, key):
        if key is None:
            print("Erro: key = None")
            return None
        floor = self.floor(self.root, key)
        if floor is None:
            return floor
        return floor if floor.key <= key else None

    def floor(self, node, key):

        if node is None:
            return self.node_max()

        """ If root.data is equal to key """
        if (node.key == key):
            return node

        """ If root.data is greater than the key """
        if (node.key > key):
            return self.floor(node.left, key)

        """ Else, the floor may lie in right subtree
        or may be equal to the root"""
        floor_value = self.floor(node.right, key)
        if floor_value is None:
            return node if node.key <= key else None
        return floor_value if (floor_value.key <= key) else node

    def ceil(self, node, key):

        if node is None:
            return self.node_min()

        """ If root.data is equal to key """
        if node.key == key:
            return node

        """ If root.data is greater than the key """
        if node.key < key:
            return self.ceil(node.right, key)

        """ Else, the floor may lie in right subtree
        or may be equal to the root"""
        ceil_value = self.ceil(node.left, key)
        if ceil_value is None:
            return node if node.key >= key else None
        return ceil_value if (ceil_value.key >= key) else node

    def contains(self, key):
        return self.get(key) is not None

    def put(self, key, val):
        if key is None:
            print("Key is None")
            return
        if val is None:
            self.delete(key)
            return
        self.root = self._put(self.root, key, val)
        self.root.color = BLACK

    def _put(self, node, key, val):
        if node is None:
            return self.Node(key, val, RED, 1)
        if key < node.key:
            node.left = self._put(node.left, key, val)
        elif key > node.key:
            node.right = self._put(node.right, key, val)
        else:
            node.val = val

        if is_red(node.right) and (not is_red(node.left)):
            node = rotate_left(node)
        if is_red(node.left) and is_red(node.left.left):
            node = rotate_right(node)
        if is_red(node.left) and is_red(node.right):
            flip_colors(node)
        node.size = size(node.left) + size(node.right) + 1

        return node

    def delete(self, key):
        if (self.root is None) or (key is None) or (not self.contains(key)):
            return

        if (not is_red(self.root.left)) and (not is_red(self.root.right)):
            self.root.color = RED

        self.root = self._delete(self.root, key)
        if not self.is_empty():
            self.root.color = BLACK

    def _delete(self, node, key):
        if key < node.key:
            if (not is_red(node.left)) and (not is_red(node.left.left)):
                node = move_red_left(node)
            node.left = self._delete(node.left, key)
        else:
            if is_red(node.left):
                node = rotate_right(node)
            if key == node.key and node.right is None:
                return None
            if (not is_red(node.right)) and (not is_red(node.right.left)):
                node = move_red_right(node)
            if key is node.key:
                x = self._min(node.right)
                node.key = x.key
                node.val = x.val
                node.right = self._delete_min(node.right)
            else:
                node.right = self._delete(node.right, key)
        return balance(node)

    def tree_min(self):
        if self.is_empty():
            print("Vazio")
            return
        return self._min(self.root).key

    def node_min(self):
        if self.is_empty():
            print("Vazio")
            return
        return self._min(self.root)

    def _min(self, node):
        if node.left is None:
            return node
        return self._min(node.left)

    def delete_min(self):
        if self.is_empty():
            print("Lista vazia")
            return
        if (not is_red(self.root.left) and (not is_red(self.root.right))):
            self.root.color = RED
        self.root = self._delete_min(self.root)
        if not self.is_empty():
            self.root.color = BLACK

    def _delete_min(self, node):
        if node.left is None:
            return None
        if (not is_red(node.left)) and (not is_red(node.left.left)):
            node = move_red_left(node)
        node.left = self._delete_min(node.left)
        return balance(node)

    def in_order_traversal(self):
        return self._in_order(self.root)

    def nodes_between(self, min_key, max_key):
        nodes = []
        for node in self._nodes_between(self.root, min_key, max_key):
            nodes.append(node)
        return nodes

    def _nodes_between(self, node, min_key, max_key):
        if node is None:
            return
        yield from self._nodes_between(node.left, min_key, max_key)
        if min_key <= node.key <= max_key:
            yield node
        yield from self._nodes_between(node.right, min_key, max_key)

    def _in_order(self, node):
        if node is None:
            return
        yield from self._in_order(node.left)
        yield node.key, node.val
        yield from self._in_order(node.right)

    def in_order_traversal_keys(self):
        return self._in_order_keys(self.root)

    def _in_order_keys(self, node):
        if node is None:
            return
        yield from self._in_order_keys(node.left)
        yield node.key
        yield from self._in_order_keys(node.right)

    def height(self):
        return _height(self.root)

'''
t = RedBlackTree()
for i in range(100):
    t.put(i, "teste" + str(i))
print("---")
a = t.nodes_between(10, 20)
for node in a:
    print(node.key)


for i in {1, 3, 5, 7, 9, 11}:
    print(i)
    j = t.get_ceiling(i)
    k = t.get_floor(i)
    if j is not None:
        print("ceil de " + str(i) + " = " + str(t.get_ceiling(i).key))
    if k is not None:
        print("floor de " + str(i) + " = " + str(t.get_floor(i).key))
'''
