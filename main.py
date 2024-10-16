import time, sys
from functools import wraps
import tracemalloc

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} function took {end_time - start_time:.10f} seconds")
        return result

    return wrapper

def memoryit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()  # Start tracking memory
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()  # Get current and peak memory usage
        tracemalloc.stop()  # Stop tracking memory

        current_kb = current / 1024
        peak_kb = peak / 1024

        print(f"Function '{func.__name__}' used {current_kb:.2f} KB of memory at the end")
        print(f"Function '{func.__name__}' reached a peak memory usage of {peak_kb:.2f} KB")

        return result

    return wrapper

class Node:
    def __init__(self, data, prev=None, next=None) -> None:
        self.data = data
        self.prev = prev
        self.next = next

class DoublyLinkedList:
    def __init__(self) -> None:
        self.header = Node(None)
        self.trailer = Node(None, prev=self.header)
        self.header.next = self.trailer

    def append(self, data):
        new_node = Node(data)
        last_node = self.trailer.prev
        last_node.next = new_node
        new_node.prev = last_node
        new_node.next = self.trailer
        self.trailer.prev = new_node

    def remove_head(self):
        if self.header.next == self.trailer:
            return None
        first_node = self.header.next
        self.header.next = first_node.next
        first_node.next.prev = self.header
        return first_node.data

    def is_empty(self):
        return self.header.next == self.trailer


class Queue:
    def __init__(self) -> None:
        self.items = DoublyLinkedList()

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):

        return self.items.remove_head()

    def is_empty(self):
        return self.items.is_empty()



class Room:
    def __init__(self, room_num, group) -> None:
        self.room_num = room_num
        self.group = group

    def __str__(self) -> str:
        return f"{self.room_num}, {self.group}"

    def get_information(self) -> str:
        room_no = "_".join(list(map(str, self.group)))
        return f"{room_no} {self.room_num}"


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
        self.max_room_number = 0

    # @timeit
    def insert(self, root, data: Room):
        if root is None:
            new_node = AVLNode(data)
            return new_node
        if self.max_room_number < data.room_num:
            self.max_room_number = data.room_num
        
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
        if self.max_room_number <= data.room_num:
            self.max_room_number -= 1
        
        if root.data.room_num > data:
            root.left = self.delete(root.left, data)
        elif root.data.room_num < data:
            root.right = self.delete(root.right, data)
        else:
            if root.left is None:
                result = root.right
                self.update_file()  # Update file after deletion
                return result
            if root.right is None:
                result = root.left
                self.update_file()  # Update file after deletion
                return result
            succ = self.find_successor(root)
            root.data.room_num = succ.data.room_num
            root.right = self.delete(root.right, succ.data.room_num)
        return self.rebalance(root)

    def __str__(self) -> str:
        lines = AVLTree._build_tree_string(self.root, 0, False, "-")[0]
        return "\n" + "\n".join((line.rstrip() for line in lines))

    def update_file(self, filename="output.txt"):
        """Rewrite the entire file after a deletion"""
        self.write_file(filename)

    def write_file(self, filename="output.txt"):
        traversal_result = []
        self._inorder_traversal(self.root, traversal_result)
        result_str = "\n".join(traversal_result)

        with open(filename, "w") as f:
            f.write(result_str)

    def clear_file(self, filename="output.txt"):
        """Clear the contents of the file."""
        with open(filename, "w") as f:
            pass 

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

    def get_max_room(self, root):
        return self.max_room_number

    def missing_room_count(self, root):
        if root is None:
            return 0
        result = self.get_max_room(root) - len(self) + 1
        return result

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

@memoryit
@timeit
def inserts(inp: list, avl: AVLTree):
    
    def calculate_room_number(i, j, k, l):
        return (11**0) * (7**i) * (5**j) * (3**k) * (2**l)

    def create_room_group(i, j, k, l, inp):
        room_group = [0]
        for m in range(1, len(inp)):
            if inp[m] <= 0:
                room_group.append(0)
            else:
                room_group.append([i, j, k, l][m - 1])
        return tuple(room_group)

    adjusted_inp = [inp[0]] + [max(1, x) for x in inp[1:-1]] + [inp[-1]]
    
    for i in range(1, adjusted_inp[0] + 1):
        room_num = (11**1) * (7**0) * (5**0) * (3**0) * (2**i)
        room_group = (1, 0, 0, 0, i)
        avl.root = avl.insert(avl.root, Room(room_num, room_group))

    for i in range(1, adjusted_inp[1] + 1):
        for j in range(1, adjusted_inp[2] + 1):
            for k in range(1, adjusted_inp[3] + 1):
                for l in range(1, adjusted_inp[4] + 1):
                    room_num = calculate_room_number(i, j, k, l)
                    room_group_tuple = create_room_group(i, j, k, l, inp)
                    avl.root = avl.insert(avl.root, Room(room_num, room_group_tuple))
                    avl.max_room_number = room_num

    return avl.root

@timeit
def manual_insert(room_num, avl: AVLTree):
    room_group_tuple = (2, 0, 0, 0, 0)
    if avl.search(avl.root, room_num):
        return avl.root
    avl.root = avl.insert(avl.root, Room(room_num, room_group_tuple))
    return avl.root


def main():
    avl = AVLTree()
    inp = list(map(int, input().split("/")))
    avl.clear_file()
    avl.root = inserts(inp, avl)
    avl.write_file()
    # print(avl)
    print(f"Memory Usage : {memory_usage(avl)} Bytes")


def memory_usage(avl: AVLTree):
    def node_size(node):
        if node is None:
            return 0
        return sys.getsizeof(node) + node_size(node.left) + node_size(node.right)

    return node_size(avl.root)


if __name__ == "__main__":
    main()
