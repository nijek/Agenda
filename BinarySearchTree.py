class BinarySearchTree:
    class Node:
        def __init__(self, key=None, val=None, left=None, right=None):
            self.key = key
            self.val = val
            self.left = left
            self.right = right

    def __init__(self, key=None, val=None):
        self.count = 0
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

    def increase_count(self):
        self.count += 1

    def decrease_count(self):
        self.count -= 1

    def set_count(self, count):
        self.count = count

    def get_count(self):
        return self.count

    def _put(self, key, val, node):
        if node is None or (node.key is None):
            self.increase_count()
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
            count_copy = self.count
            self._print_with_list(self.root, self.count, arr)
            self.count = count_copy
        else:
            print("Nenhum evento.")
        return arr

    def _print_with_list(self, node, num, arr):
        if not node:
            return

        self._print_with_list(node.left, num, arr)
        self.decrease_count()
        print(node.key.date.strftime(str(num - self.get_count()) + ") %d/%m/%Y - %H:%M"), node.val)
        arr.append(node.key)
        self._print_with_list(node.right, num, arr)

    def print(self):
        if self.root and self.root.val:
            count_copy = self.count
            self._print(self.root, self.count)
            self.count = count_copy
        else:
            print("Nenhum evento.")

    def _print(self, node, num):
        if not node:
            return

        self._print(node.left, num)
        self.decrease_count()
        print(node.key.date.strftime(str(num - self.get_count()) + ") %d/%m/%Y - %H:%M"), node.val)
        self._print(node.right, num)

    def to_dic(self):
        dic = {}
        self._to_dic(self.root, dic)
        return dic

    def _to_dic(self, node, dic):
        if not node:
            return
        self._to_dic(node.left, dic)
        dic[node.key.date.isoformat() + str(node.key.uuid)] = node.val
        self._to_dic(node.right, dic)

    def min_value_node(self, node):
        current = node

        while (current.left is not None):
            current = current.left

        return current

    def delete_node(self, key):
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            self.decrease_count()
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.min_value_node(root.right)

            root.key = temp.key

            root.right = self._delete_node(root.right, temp.key)

        return root
