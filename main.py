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
    def __init__(self, n, g) -> None:
        self.n = n
        self.g = g

    def __str__(self) -> str:
        return f"{self.n}, {self.g}"

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

    def insert(self, root, data: Room):
        if self.root is None:
            self.root = AVLNode(data)
            return self.root
        else:
            if root is None:
                return AVLNode(data)
            if data.n < root.data.n:
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

    def printTree90(self, node, level = 0):
        if node != None:
            self.printTree90(node.right, level + 1)
            print('     ' * level, node.data)
            self.printTree90(node.left, level + 1)

    def find_successor(self, root, flag = False):
        if not flag and root.right is not None:
            return self.find_successor(root.right, True)
        if root.left is None:
            return root
        return self.find_successor(root.left, flag)

    def delete(self, root, data):
        if root is None:
            return root
        if root.data.n > data:
            root.left = self.delete(root.left, data)
        elif root.data.n < data:
            root.right = self.delete(root.right, data)
        else:
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            succ = self.find_successor(root)
            root.data.n = succ.data.n
            root.right = self.delete(root.right, succ.data.n)
        return self.rebalance(root)
    
    def __str__(self) -> str:
        lines = AVLTree._build_tree_string(self.root, 0, False, "-")[0]
        return "\n" + "\n".join((line.rstrip() for line in lines))
    
    def _build_tree_string(
        root: AVLNode,
        curr_index: int,
        include_index: bool = False,
        delimiter: str = "-") :
        if root is None:
            return [], 0, 0, 0
        line1 = []
        line2 = []
        if include_index:
            node_repr = "{}{}{}".format(curr_index, delimiter, root.data)
        else:
            node_repr = str(root.data)
        new_root_width = gap_size = len(node_repr)
        l_box, l_box_width, l_root_start, l_root_end = AVLTree._build_tree_string(root.left, 2 * curr_index + 1, include_index, delimiter)
        r_box, r_box_width, r_root_start, r_root_end = AVLTree._build_tree_string(root.right, 2 * curr_index + 2, include_index, delimiter)
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
    
def inserts(inp: list, avl: AVLTree):
    lst = inp.copy()
    lst.insert(0, max(lst))
    LEN = len(lst)
    i = 0
    j = len(avl)
    while any(n > 0 for n in lst):
        if lst[i] > 0:
            lst[i] -= 1
            avl.root = avl.insert(avl.root, Room(j, i))
            j += 1
        i = (i + 1) % LEN
    return avl.root

def sign(text = None):
    if text is None:
        text = "Welcome to Infinity Hotel"
    gap = " "
    print("="*48)
    print(f"|{gap:^46}|")
    print(f"|{text:^46}|")
    print(f"|{gap:^46}|")
    print("="*48)
def front_program():
    sign()
    print("กรอกจำนวนห้องพักด้วยค่าตั้งแต่ 1 ถึง N (4 cars is default)")
    car1 = input("Car 1\n-> ")
    car2 = input("Car 2\n-> ")
    car3 = input("Car 3\n-> ")
    car4 = input("Car 4\n-> ")
    cars = [car2, car3, car4]
    number = 5
    print("Add more car ? (Y/N)")    
    add = True if input("-> ") == "Y" else False
    while add:
        car = input(f"Car {number}:")
        cars.append(car)
        print("Add more car ? (Y/N)")    
        add = True if input("->") == "Y" else False
    
    print("Welcome to Infinity Hotel โรงแรมไร้ขีดจำกัด")
    output = car1
    for car in cars:
        output += f"/{car}"
    return output


def print_tree():
    '''Print'''
def find_room():
    ''''''
def delete_room():
    ''''''
def total_room():
    ''''''
def empty_room():
    ''''''

def program():
    sign("How may I assist you today?")    
    choice = 6
    while choice > 0:
        print("1 | Print Tree")
        print("2 | Find Room")
        print("3 | Delete Room")
        print("4 | Count Room")
        print("5 | Empty Room")
        print("0 | Exit")
        choice = int(input("-> "))
        if choice == 1:
            print_tree()
        elif choice == 2:
            find_room()
        elif choice == 3:
            delete_room()
        elif choice == 4:
            total_room()
        elif choice == 5:
            empty_room()
        else:
            print("Exiting...")
            break
        print()


if __name__ == "__main__":
    avl = AVLTree()
    inp = list(map(int, front_program().split("/")))
    avl.root = inserts(inp, avl)
    print(avl)
    print(len(avl))
    program()