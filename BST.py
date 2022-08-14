class BinarySearchTree:
    class Node:
        def __init__(self, key=None, val=None, left=None, right=None, count=1):
            self.key = key
            self.val = val
            self.left = left
            self.right = right
            self.count = count

    def __init__(self, key=None, val=None):
        self.root = self.Node(key, val)

    def get(self, key):
        current = self.root
        while current is not None:
            if current.key == key:
                return current.val
            if current.key > key:
                current = current.left
            else:
                current = current.right
        return None

    def _put(self, key, val, node):
        if node is None or (node.key is None):
            return self.Node(key, val)
        if key > node.key:
            node.count += 1
            node.right = self._put(key, val, node.right)
        elif key < node.key:
            node.count += 1
            node.left = self._put(key, val, node.left)
        else:
            node.key = val

        return node

    def put(self, key, val):
        self.root = self._put(key, val, self.root)

    def min(self):
        current = self.root
        while current.left:
            current = current.left
        return current.val

    def max(self):
        current = self.root
        while current.right:
            current = current.right
        return current.val

    def size(self):
        return self.root.count

    def level(self, key):
        current = self.root
        if current.key == None:
            print ("No such key")
            return
        level = 1
        while current.key != key:
            if key > current.key:
                current = current.right
            else:
                current = current.left
            if not current:
                print("No such key")
                return
            level += 1
        return level

    def depth(self):
        return self._depth(self.root)

    def _depth(self, node):
        if not node:
            return 0
        if (not node.left) and (not node.right):
            return 1
        return 1 + max(self._depth(node.left), self._depth(node.right))

    def rank(self, key):
        node = self.root
        while (node is not None) and (node.key is not None):
            if node.key == key:
                return node.count
            if node.key > key:
                node = node.left
            else:
                node = node.right

        return 0

    def print(self):
        node = self.root
        self._print(node)

    def _print(self, node):
        if not node:
            return

        self._print(node.left)
        print((node.key).strftime("%d/%m/%Y - %H:%M"), node.val)
        self._print(node.right)

    def toDic(self):
        dic = {}
        self._toDic(self.root, dic)
        return dic

    def _toDic(self, node, dic):
        if not node:
            return
        self._toDic(node.left, dic)
        dic[node.key.isoformat()] = node.val
        self._toDic(node.right, dic)

