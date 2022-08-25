"""
Fortemente inspirada na implementação do professor Sedgewick
https://algs4.cs.princeton.edu/33balanced/RedBlackBST.java.html
"""

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

        if (is_red(node.right) and (not is_red(node.left))):
            node = rotate_left(node)
        if (is_red(node.left) and is_red(node.left.left)):
            node = rotate_right(node)
        if (is_red(node.left) and is_red(node.right)):
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

    def min(self):
        if self.is_empty():
            print("Vazio")
            return
        return self._min(self.root).key

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
