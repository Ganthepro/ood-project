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

    def __str__(self) -> str:
        return f"{self.room_num}, {self.group}"

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

    @timeit
    def search(self, root, room_num):
        if root is None:
            return False
        if root.data.room_num == room_num:
            return True
        if root.data.room_num > room_num:
            return self.search(root.left, room_num)
        return self.search(root.right, room_num)

    @timeit
    def get_max_room(self, root):
        if root.right is None:
            return root.data.room_num
        return self.get_max_room(root.right)

    @timeit
    def missing_room_count(self, root):
        if root is None:
            return 0
        result = self.get_max_room(root) - len(self) + 1
        return result

    @timeit
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
    print(inp[0])
    return avl.root


if __name__ == "__main__":
    start_time_main = time.time()
    avl = AVLTree()
    inp = list(map(int, input().split("/")))
    avl.root = inserts(inp, avl)
    print(avl)
    print(len(avl))
    
    end_time_main = time.time() 
    print(f"Total execution time in main function: {end_time_main - start_time_main:.6f} seconds")
