class BinarySearchTree:
    class Node:
        def __init__(self, key=None, val=None, left=None, right=None):
            self.key = key
            self.val = val
            self.left = left
            self.right = right

    def __init__(self, key=None, val=None):
        self.root = self.Node(key, val)

    def get(self, key):
        current = self.root
        while current and current.key:
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
            node.right = self._put(key, val, node.right)
        elif key < node.key:
            node.left = self._put(key, val, node.left)
        else:
            node.key = val

        return node

    def put(self, key, val):
        self.root = self._put(key, val, self.root)

    def print_with_list(self):
        arr = []
        if self.root.val:
            self._print_with_list(self.root, 1, arr)
        else:
            print("Nenhum evento.")
        return arr

    def _print_with_list(self, node, num, arr):
        if not node:
            return

        self._print_with_list(node.left, num + 1, arr)
        print((node.key).strftime(str(num) + ") %d/%m/%Y - %H:%M"), node.val)
        arr.append(node.key)
        self._print_with_list(node.right, num + 1, arr)

    def print(self):
        if self.root and self.root.val:
            self._print(self.root, 1)
        else:
            print("Nenhum evento.")

    def _print(self, node, num):
        if not node:
            return

        self._print(node.left, num + 1)
        print((node.key).strftime(str(num) + ") %d/%m/%Y - %H:%M"), node.val)
        self._print(node.right, num + 1)

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

    def minValueNode(self, node):
        current = node

        while (current.left is not None):
            current = current.left

        return current

    def deleteNode(self, key):
        self.root = self._deleteNode(self.root, key)

    def _deleteNode(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self._deleteNode(root.left, key)
        elif (key > root.key):
            root.right = self._deleteNode(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.minValueNode(root.right)

            root.key = temp.key

            root.right = self._deleteNode(root.right, temp.key)

        return root
