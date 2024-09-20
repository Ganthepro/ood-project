class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []

class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusTreeNode(is_leaf=True)
        self.order = order

    def insert(self, key):
        node = self.root
        if len(node.keys) == self.order - 1:
            new_root = BPlusTreeNode()
            new_root.children.append(node)
            self._split(new_root, -1)
            self.root = new_root
        self._insert_non_full(node, key)

    def _split(self, parent, index):
        node = parent.children[index]
        new_node = BPlusTreeNode(is_leaf=node.is_leaf)
        mid = node.keys[self.order // 2]
        parent.keys.insert(index, mid)
        parent.children.insert(index + 1, new_node)
        node.keys, new_node.keys = node.keys[:self.order // 2], node.keys[self.order // 2:]
        if not node.is_leaf:
            node.children, new_node.children = node.children[:self.order // 2 + 1], node.children[self.order // 2 + 1:]

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.is_leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.order - 1:
                self._split(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def print_tree(self, node=None, level=0):
        if not node:
            node = self.root
        print(f"Level {level}: {node.keys}")
        if not node.is_leaf:
            for child in node.children:
                self.print_tree(child, level + 1)

BPT = BPlusTree(order=4)

BPT.insert(3)
BPT.insert(5)
BPT.insert(7)
BPT.insert(9)
BPT.insert(11)

BPT.print_tree()