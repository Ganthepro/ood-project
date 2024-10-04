import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} function took {end_time - start_time:.10f} seconds")
        return result
    return wrapper

class Queue:
    def __init__(self) -> None:
        self.items = []

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):
        t = self.items[0]
        self.items.pop(0)
        return t

    def is_empty(self):
        return len(self.items) == 0


class Room:
    def __init__(self, room_num, group) -> None:
        self.room_num = room_num
        self.group = group
        self.desc = 'newcomer' if not isinstance(group, int) else 'pre_existed'

    def __str__(self) -> str:
        return f"{self.room_num}, {self.group}"
    
    def get_information(self) -> str:
        if isinstance(self.group, int):
            return f'roomNo{self.room_num}_{self.group}, {self.desc}'
        
        room_no = "_".join([str(n) for n in list(self.group)])
        return f'roomNo{self.room_num}_{room_no}, {self.desc}'

class AVLNode:
    def __init__(self, data):
        self.data: Room = data
        self.left = None
        self.right = None
        self.height = self.set_height()

    def get_height(self, node):
        return node.height if node else -1

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right)

    def set_height(self):
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))
        return self.height


class AVLTree:
    def __init__(self) -> None:
        self.root = None

    @timeit
    def insert(self, root, data: Room):
        if root is None:
            return AVLNode(data)
        if data.room_num == root.data.room_num:
            return root
        elif data.room_num < root.data.room_num:
            root.left = self.insert(root.left, data)
        else:
            root.right = self.insert(root.right, data)
        return self.rebalance(root)

    def rebalance(self, root):
        balance = root.get_balance(root)
        if balance == 2:
            if root.get_balance(root.left) == -1:
                root.left = self.rotate_left(root.left)
            root = self.rotate_right(root)
        elif balance == -2:
            if root.get_balance(root.right) == 1:
                root.right = self.rotate_right(root.right)
            root = self.rotate_left(root)
        root.set_height()
        return root
    
    def rotate_right(self, root):
        new_root = root.left
        root.left = new_root.right
        new_root.right = root
        root.set_height()
        new_root.set_height()
        return new_root

    def rotate_left(self, root):
        new_root = root.right
        root.right = new_root.left
        new_root.left = root
        root.set_height()
        new_root.set_height()
        return new_root

    def __len__(self):
        if self.root is None:
            return 0
        q = Queue()
        q.enqueue(self.root)
        l = 0
        while not q.is_empty():
            n = q.dequeue()
            l += 1
            if n.left:
                q.enqueue(n.left)
            if n.right:
                q.enqueue(n.right)
        return l
    
    def printTree90(self, node, level=0):
        if node != None:
            self.printTree90(node.right, level + 1)
            print("     " * level, node.data)
            self.printTree90(node.left, level + 1)

    def find_successor(self, root, flag=False):
        if not flag and root.right is not None:
            return self.find_successor(root.right, True)
        if root.left is None:
            return root
        return self.find_successor(root.left, flag)

    @timeit
    def delete(self, root, data):
        if root is None:
            return root
        if root.data.room_num > data:
            root.left = self.delete(root.left, data)
        elif root.data.room_num < data:
            root.right = self.delete(root.right, data)
        else:
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            succ = self.find_successor(root)
            root.data.room_num = succ.data.room_num
            root.right = self.delete(root.right, succ.data.room_num)
        return self.rebalance(root)

    def __str__(self) -> str:
        lines = AVLTree._build_tree_string(self.root, 0, False, "-")[0]
        return "\n" + "\n".join((line.rstrip() for line in lines))

    def write_file(self, filename="output.txt"):
        traversal_result = []
        self._inorder_traversal(self.root, traversal_result)
        result_str = "\n".join(traversal_result)
        
        with open(filename, "w") as f:
            f.write(result_str)

    def _inorder_traversal(self, node, traversal_result):
        if node:
            self._inorder_traversal(node.left, traversal_result)
            traversal_result.append(f"{node.data.get_information()}") 
            self._inorder_traversal(node.right, traversal_result)

    def _build_tree_string(
        root: AVLNode,
        curr_index: int,
        include_index: bool = False,
        delimiter: str = "-",
    ):
        if root is None:
            return [], 0, 0, 0
        line1 = []
        line2 = []
        if include_index:
            node_repr = "{}{}{}".format(curr_index, delimiter, root.data)
        else:
            node_repr = str(root.data)
        new_root_width = gap_size = len(node_repr)
        l_box, l_box_width, l_root_start, l_root_end = AVLTree._build_tree_string(
            root.left, 2 * curr_index + 1, include_index, delimiter
        )
        r_box, r_box_width, r_root_start, r_root_end = AVLTree._build_tree_string(
            root.right, 2 * curr_index + 2, include_index, delimiter
        )
        if l_box_width > 0:
            l_root = (l_root_start + l_root_end) // 2 + 1
            line1.append(" " * (l_root + 1))
            line1.append("_" * (l_box_width - l_root))
            line2.append(" " * l_root + "/")
            line2.append(" " * (l_box_width - l_root))
            new_root_start = l_box_width + 1
            gap_size += 1
        else:
            new_root_start = 0
        line1.append(node_repr)
        line2.append(" " * new_root_width)
        if r_box_width > 0:
            r_root = (r_root_start + r_root_end) // 2
            line1.append("_" * r_root)
            line1.append(" " * (r_box_width - r_root + 1))
            line2.append(" " * r_root + "\\")
            line2.append(" " * (r_box_width - r_root))
            gap_size += 1
        new_root_end = new_root_start + new_root_width - 1
        gap = " " * gap_size
        new_box = ["".join(line1), "".join(line2)]
        for i in range(max(len(l_box), len(r_box))):
            l_line = l_box[i] if i < len(l_box) else " " * l_box_width
            r_line = r_box[i] if i < len(r_box) else " " * r_box_width
            new_box.append(l_line + gap + r_line)
        return new_box, len(new_box[0]), new_root_start, new_root_end
    
    @timeit
    def search(self, root, room_num):
        if root is None:
            return False
        if root.data.room_num == room_num:
            return True
        if root.data.room_num > room_num:
            return self.search(root.left, room_num)
        return self.search(root.right, room_num)

    # @timeit
    def get_max_room(self, root):
        if root.right is None:
            return root.data.room_num
        return self.get_max_room(root.right)

    # @timeit
    def missing_room_count(self, root):
        if root is None:
            return 0
        result = self.get_max_room(root) - len(self) + 1
        return result

    # @timeit
    def find_missing_rooms(self, root) -> list:
        if root is None:
            return []
        missing_rooms = []
        current_room = 0
        max_room = self.get_max_room(root)

        def inorder_traversal(node):
            nonlocal current_room
            if node is None:
                return
            inorder_traversal(node.left)
            while current_room < node.data.room_num:
                missing_rooms.append(current_room)
                current_room += 1
            current_room = node.data.room_num + 1
            inorder_traversal(node.right)
        
        inorder_traversal(root)

        while current_room < max_room:
            missing_rooms.append(current_room)
            current_room += 1

        return missing_rooms


@timeit
def inserts(inp: list, avl: AVLTree):
    existed_room_count = 0
    for i in range(inp[1]):
        for j in range(inp[2]):
            for k in range(inp[3]):
                for l in range(inp[4]):
                    room_num = (3 ** l) * (5 ** k) * (7 ** j) * (11 ** i)
                    avl.root = avl.insert(avl.root, Room(room_num, (i, j, k, l)))
        if inp[0] > 0:
            existed_room_count += 1
            avl.root = avl.insert(avl.root, Room(room_num * (2 ** existed_room_count), (0)))
            inp[0] -= 1
    if inp[0] > 0:
        for i in range(inp[0]):
            avl.root = avl.insert(avl.root, Room(avl.get_max_room(avl.root) + 1, (0)))
    return avl.root

@timeit
def main():
    avl = AVLTree()
    inp = list(map(int, input().split("/")))
    avl.root = inserts(inp, avl)
    print(avl)
    print(len(avl))
    avl.write_file()

if __name__ == "__main__":
    main()