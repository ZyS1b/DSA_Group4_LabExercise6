from flask import Flask, render_template, request, jsonify
import uuid
from queue import Queue as PyQueue 
from sorting_routes import sorting_blueprint

app = Flask(__name__)
app.register_blueprint(sorting_blueprint)

# ---------------------------
# Linked-List Data Structures
# ---------------------------
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, item):
        node = Node(item)
        if self.tail:
            self.tail.next = node
            self.tail = node
        else:
            self.head = node
            self.tail = node

    def dequeue(self):
        if self.is_empty():
            return None
        node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        node.next = None
        return node.data

    def display(self):
        cur = self.head
        out = []
        while cur:
            out.append(cur.data)
            cur = cur.next
        return out


class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, item):
        self.enqueue_tail(item)

    def enqueue_head(self, item):
        node = Node(item)
        if self.head:
            node.next = self.head
            self.head = node
        else:
            self.head = node
            self.tail = node

    def enqueue_tail(self, item):
        node = Node(item)
        if self.tail:
            self.tail.next = node
            self.tail = node
        else:
            self.head = node
            self.tail = node

    def dequeue(self):
        return self.dequeue_tail()

    def dequeue_head(self):
        if self.is_empty():
            return None
        node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        node.next = None
        return node.data

    def dequeue_tail(self):
        if self.is_empty():
            return None
        if self.head is self.tail:
            data = self.head.data
            self.head = None
            self.tail = None
            return data
        prev = self.head
        while prev.next is not self.tail:
            prev = prev.next
        data = self.tail.data
        prev.next = None
        self.tail = prev
        return data

    def display(self):
        cur = self.head
        out = []
        while cur:
            out.append(cur.data)
            cur = cur.next
        return out


# ---------------------------
# General Binary Tree (Module Behavior)
# ---------------------------
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.id = str(uuid.uuid4())


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = TreeNode(value)
        if self.root is None:
            self.root = new_node
            return True, f"Inserted root {value}"

        q = [self.root]
        while q:
            cur = q.pop(0)
            if cur.left is None:
                cur.left = new_node
                return True, f"Inserted {value} to LEFT of {cur.value}"
            if cur.right is None:
                cur.right = new_node
                return True, f"Inserted {value} to RIGHT of {cur.value}"
            q.append(cur.left)
            q.append(cur.right)

        return False, "Insert failed."

    def insert_left(self, parent, value):
        new_node = TreeNode(value)
        if parent.left is None:
            parent.left = new_node
        else:
            old = parent.left
            parent.left = new_node
            new_node.left = old
        return True, f"Inserted {value} to LEFT of {parent.value}"

    def insert_right(self, parent, value):
        new_node = TreeNode(value)
        if parent.right is None:
            parent.right = new_node
        else:
            old = parent.right
            parent.right = new_node
            new_node.right = old
        return True, f"Inserted {value} to RIGHT of {parent.value}"

    def search_value(self, root, key):
        if root is None:
            return None
        q = [root]
        while q:
            cur = q.pop(0)
            if cur.value == key:
                return cur
            if cur.left: q.append(cur.left)
            if cur.right: q.append(cur.right)
        return None

    def search_id(self, root, node_id):
        if root is None:
            return None
        q = [root]
        while q:
            cur = q.pop(0)
            if cur.id == node_id:
                return cur
            if cur.left: q.append(cur.left)
            if cur.right: q.append(cur.right)
        return None

    def delete_value(self, key):
        if self.root is None:
            return False

        if self.root.left is None and self.root.right is None:
            if self.root.value == key:
                self.root = None
                return True
            return False

        q = [self.root]
        target = None
        last = None
        parent_of_last = None

        while q:
            last = q.pop(0)
            if last.value == key:
                target = last
            if last.left:
                parent_of_last = last
                q.append(last.left)
            if last.right:
                parent_of_last = last
                q.append(last.right)

        if target is None:
            return False

        target.value = last.value
        target.id = last.id

        if parent_of_last and parent_of_last.right == last:
            parent_of_last.right = None
        elif parent_of_last and parent_of_last.left == last:
            parent_of_last.left = None

        return True

    def inorder(self, root, out):
        if root:
            self.inorder(root.left, out)
            out.append(root.value)
            self.inorder(root.right, out)

    def preorder(self, root, out):
        if root:
            out.append(root.value)
            self.preorder(root.left, out)
            self.preorder(root.right, out)

    def postorder(self, root, out):
        if root:
            self.postorder(root.left, out)
            self.postorder(root.right, out)
            out.append(root.value)

    def collect_nodes(self, root, only_not_full=False, out=None):
        if out is None:
            out = []
        if root:
            if (not only_not_full) or (root.left is None or root.right is None):
                out.append(root)
            self.collect_nodes(root.left, only_not_full, out)
            self.collect_nodes(root.right, only_not_full, out)
        return out

    def first_not_full_node(self):
        nodes = self.collect_nodes(self.root, only_not_full=True)
        return nodes[0] if nodes else None


# ---------------------------
# Binary Search Tree (separate work)
# ---------------------------
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.id = str(uuid.uuid4())


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = BSTNode(value)
            return True, f"Inserted root {value}"
        self.root = self._insert(self.root, value)
        return True, f"Inserted {value} using BST rule."

    def _insert(self, node, value):
        if node is None:
            return BSTNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node

    def search(self, node, value):
        if node is None:
            return None
        if node.value == value:
            return node
        if value < node.value:
            return self.search(node.left, value)
        return self.search(node.right, value)

    def get_max_value(self, node):
        if node is None:
            return None
        cur = node
        while cur.right is not None:
            cur = cur.right
        return cur.value

    def find_height(self, node):
        if node is None:
            return -1
        return 1 + max(self.find_height(node.left), self.find_height(node.right))

    def delete(self, node, value):
        if node is None:
            return None, False

        if value < node.value:
            node.left, deleted = self.delete(node.left, value)
            return node, deleted
        if value > node.value:
            node.right, deleted = self.delete(node.right, value)
            return node, deleted

        if node.left is None and node.right is None:
            return None, True
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        succ_parent = node
        succ = node.right
        while succ.left:
            succ_parent = succ
            succ = succ.left

        node.value = succ.value
        node.id = succ.id

        if succ_parent.left == succ:
            succ_parent.left, _ = self.delete(succ_parent.left, succ.value)
        else:
            succ_parent.right, _ = self.delete(succ_parent.right, succ.value)

        return node, True

    def inorder(self, node, out):
        if node:
            self.inorder(node.left, out)
            out.append(node.value)
            self.inorder(node.right, out)

    def preorder(self, node, out):
        if node:
            out.append(node.value)
            self.preorder(node.left, out)
            self.preorder(node.right, out)

    def postorder(self, node, out):
        if node:
            self.postorder(node.left, out)
            self.postorder(node.right, out)
            out.append(node.value)

from queue import Queue as PyQueue

# ---------------------------
# Graph: Rail map + BFS (MRT/LRT)
# ---------------------------
class RailGraph:
    def __init__(self):
        self.adj = {}  # station -> set(neighbors)

    def add_station(self, name):
        if name not in self.adj:
            self.adj[name] = set()

    def add_edge(self, a, b):
        self.add_station(a)
        self.add_station(b)
        self.adj[a].add(b)
        self.adj[b].add(a)

    def add_line(self, stations):
        for i in range(len(stations) - 1):
            self.add_edge(stations[i], stations[i + 1])

    def shortest_path_bfs(self, start, goal):
        if start not in self.adj or goal not in self.adj:
            return None

        q = PyQueue()
        q.put(start)
        prev = {start: None}
        visited = {start}

        while not q.empty():
            cur = q.get()
            if cur == goal:
                break
            for nxt in self.adj[cur]:
                if nxt not in visited:
                    visited.add(nxt)
                    prev[nxt] = cur
                    q.put(nxt)

        if goal not in prev:
            return None

        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path


def build_rail_graph_with_map():
    g = RailGraph()

    mrt3 = [
        "North Avenue", "Quezon Avenue", "GMA-Kamuning", "Araneta Center-Cubao (MRT-3)",
        "Santolan-Annapolis", "Ortigas", "Shaw Boulevard", "Boni", "Guadalupe",
        "Buendia", "Ayala", "Magallanes", "Taft Avenue"
    ]
    lrt2 = [
        "Recto", "Legarda", "Pureza", "V. Mapa", "J. Ruiz", "Gilmore",
        "Betty Go-Belmonte", "Araneta Center-Cubao (LRT-2)", "Anonas", "Katipunan",
        "Santolan", "Marikina-Pasig", "Antipolo"
    ]
    lrt1 = [
        "Fernando Poe Jr.", "Balintawak", "Monumento", "5th Avenue", "R. Papa",
        "Abad Santos", "Blumentritt", "Tayuman", "Bambang", "Doroteo Jose",
        "Carriedo", "Central Terminal", "United Nations", "Pedro Gil", "Quirino",
        "Vito Cruz", "Gil Puyat", "Libertad", "EDSA", "Baclaran",
        "Redemptorist-Aseana", "MIA Road", "PITX", "Ninoy Aquino Avenue", "Dr. Santos"
    ]

    # Build edges
    g.add_line(mrt3)
    g.add_line(lrt2)
    g.add_line(lrt1)

    # Walk transfers (dashed links)
    transfers = [
        ("Doroteo Jose", "Recto"),
        ("Araneta Center-Cubao (MRT-3)", "Araneta Center-Cubao (LRT-2)"),
        ("EDSA", "Taft Avenue"),
    ]

    # Graph connections for transfers
    for a, b in transfers:
        g.add_edge(a, b)

    # -----------------------------------------
    # MANUAL COORDINATES (EDIT THESE FREELY)
    # viewBox is 0 0 1120 640 in graph.html
    # -----------------------------------------
    coords = {
        # ----- LRT-1 (Red) -----
        "Fernando Poe Jr.": {"x": 335, "y": 70},
        "Balintawak": {"x": 295, "y": 92},
        "Monumento": {"x": 260, "y": 114},
        "5th Avenue": {"x": 230, "y": 136},
        "R. Papa": {"x": 205, "y": 158},
        "Abad Santos": {"x": 185, "y": 180},
        "Blumentritt": {"x": 170, "y": 202},
        "Tayuman": {"x": 160, "y": 224},
        "Bambang": {"x": 150, "y": 246},
        "Doroteo Jose": {"x": 140, "y": 268},  # align with Recto
        "Carriedo": {"x": 130, "y": 290},
        "Central Terminal": {"x": 120, "y": 312},
        "United Nations": {"x": 115, "y": 334},
        "Pedro Gil": {"x": 110, "y": 356},
        "Quirino": {"x": 110, "y": 378},
        "Vito Cruz": {"x": 110, "y": 400},
        "Gil Puyat": {"x": 120, "y": 422},
        "Libertad": {"x": 130, "y": 444},
        "EDSA": {"x": 140, "y": 466},
        "Baclaran": {"x": 150, "y": 488},
        "Redemptorist-Aseana": {"x": 170, "y": 510},
        "MIA Road": {"x": 200, "y": 532},
        "PITX": {"x": 240, "y": 554},
        "Ninoy Aquino Avenue": {"x": 290, "y": 576},
        "Dr. Santos": {"x": 350, "y": 598},

        # ----- LRT-2 (Blue) -----
        "Recto": {"x": 200, "y": 268},   # connected to Doroteo Jose
        "Legarda": {"x": 270, "y": 268},
        "Pureza": {"x": 340, "y": 268},
        "V. Mapa": {"x": 410, "y": 268},
        "J. Ruiz": {"x": 480, "y": 268},
        "Gilmore": {"x": 550, "y": 268},
        "Betty Go-Belmonte": {"x": 620, "y": 268},
        "Araneta Center-Cubao (LRT-2)": {"x": 690, "y": 268},
        "Anonas": {"x": 760, "y": 268},
        "Katipunan": {"x": 830, "y": 268},
        "Santolan": {"x": 900, "y": 300},
        "Marikina-Pasig": {"x": 950, "y": 370},
        "Antipolo": {"x": 950, "y": 430},

        # ----- MRT-3 (Green) -----
        "North Avenue": {"x": 540, "y":90},
        "Quezon Avenue": {"x": 600, "y": 120},
        "GMA-Kamuning": {"x": 650, "y": 170},
        "Araneta Center-Cubao (MRT-3)": {"x": 650, "y": 230},
        "Santolan-Annapolis": {"x": 650, "y": 300},
        "Ortigas": {"x": 620, "y": 326},
        "Shaw Boulevard": {"x": 575, "y": 360},
        "Boni": {"x": 500, "y": 390},
        "Guadalupe": {"x": 410, "y": 410},
        "Buendia": {"x": 340, "y": 425},
        "Ayala": {"x": 280, "y": 440},
        "Magallanes": {"x": 220, "y": 455},
        "Taft Avenue": {"x": 180, "y": 466},  # near EDSA for transfer (adjust as you want)
    }

    # -----------------------------------------
    # Lines config (colors)
    # -----------------------------------------
    lines = [
        {"name": "LRT-1", "color": "#ff3b30", "stations": lrt1},
        {"name": "LRT-2", "color": "#2f5cff", "stations": lrt2},
        {"name": "MRT-3", "color": "#22c55e", "stations": mrt3},
    ]

    # Label shortening (map only)
    label_text = {st: st for st in coords.keys()}
    label_text["Araneta Center-Cubao (MRT-3)"] = "Cubao (MRT-3)"
    label_text["Araneta Center-Cubao (LRT-2)"] = "Cubao (LRT-2)"
    label_text["Betty Go-Belmonte"] = "Betty Go"
    label_text["Santolan-Annapolis"] = "Santolan-Ann."
    label_text["Marikina-Pasig"] = "Marikina"
    label_text["Ninoy Aquino Avenue"] = "NAIA Ave."

    # Label placement meta (edit freely too)
    label_meta = {}
    def set_label(st, dx, dy, anchor):
        label_meta[st] = {"dx": dx, "dy": dy, "anchor": anchor}

    for st in coords.keys():
        set_label(st, 12, 4, "start")  # default right

    # LRT-1 labels left side
    for st in lrt1:
        set_label(st, -12, 4, "end")

    # LRT-2 alternate above/below centered
    for i, st in enumerate(lrt2):
        set_label(st, 0, (20 if i % 2 == 0 else -14), "middle")

    # MRT-3 alternate right/top
    for i, st in enumerate(mrt3):
        set_label(st, 14, 4, "start")

    # transfer tweak labels
    set_label("Doroteo Jose", -12, 4, "end")
    set_label("Recto", 0, 20, "middle")
    set_label("EDSA", -12, 4, "end")
    set_label("Taft Avenue", 0, 20, "middle")
    set_label("Araneta Center-Cubao (MRT-3)", 14, 4, "start")
    set_label("Araneta Center-Cubao (LRT-2)", 26, -14, "middle")

    return g, coords, lines, label_meta, label_text, transfers

rail_graph, rail_coords, rail_lines, rail_label_meta, rail_label_text, rail_transfers = build_rail_graph_with_map()

# ---------------------------
# App State
# ---------------------------
SITE_NAME = "Nodeus"
queue_ds = Queue()
deque_ds = Deque()
tree_ds = BinaryTree()
bst_ds = BinarySearchTree()

# ---------------------------
# Sorting Algorithms (Bubble Sort)
# ---------------------------
def build_bubble_sort_actions(values):
    actions = []
    arr = list(values)
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            actions.append({
                "type": "compare",
                "indices": [j, j + 1],
                "desc": f"Compare {arr[j]} with {arr[j + 1]}."
            })

            if arr[j] > arr[j + 1]:
                actions.append({
                    "type": "swap",
                    "i": j,
                    "j": j + 1,
                    "desc": f"Swap {arr[j]} at index {j} with {arr[j + 1]} at index {j + 1}."
                })
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        actions.append({
            "type": "locked", 
            "index": n - 1 - i,
            "desc": f"Value {arr[n - 1 - i]} is now in its sorted position."
        })

        if not swapped:
            break
    actions.append({"type": "done", "desc": "Array sorted."})
    return actions


@app.route("/works/sorting/bubble-steps", methods=["POST"])
def bubble_sort_steps():
    data = request.get_json(silent=True) or {}
    raw_values = data.get("values", [])

    cleaned = []
    for value in raw_values:
        try:
            num = int(value)
        except (TypeError, ValueError):
            continue
        num = max(2, min(99, num))
        cleaned.append(num)
        if len(cleaned) >= 14:
            break

    actions = build_bubble_sort_actions(cleaned)
    return jsonify({"actions": actions, "values": cleaned})

# ---------------------------
# Sorting Algorithms (Selection Sort)
# ---------------------------
def build_selection_sort_actions(values):
    actions = []
    arr = list(values)

    n = len(arr)
    for i in range(n - 1):
        min_index = i
        actions.append({
            "type": "start_pass",
            "index": i,
            "desc": f"Start pass for position {i}, find min in subarray {i}-{n-1}."
        })
        for j in range(i + 1, n):
            actions.append({
                "type": "compare",
                "indices": [min_index, j],
                "desc": f"Compare current min {arr[min_index]} with {arr[j]}."
            })
            if arr[j] < arr[min_index]:
                min_index = j
                actions.append({
                    "type": "min_found",
                    "index": min_index,
                    "desc": f"New min found: {arr[min_index]} at index {min_index}."
                })
        if min_index != i:
            actions.append({
                "type": "swap",
                "i": i,
                "j": min_index,
                "desc": f"Swap {arr[i]} at index {i} with min {arr[min_index]} at index {min_index}."
            })
            arr[i], arr[min_index] = arr[min_index], arr[i]
        actions.append({
            "type": "sorted",
            "index": i,
            "desc": f"Position {i} is now sorted."
        })

    actions.append({"type": "done", "desc": "Array sorted."})
    return actions


@app.route("/works/sorting/selection-steps", methods=["POST"])
def selection_sort_steps():
    data = request.get_json(silent=True) or {}
    raw_values = data.get("values", [])

    cleaned = []
    for value in raw_values:
        try:
            num = int(value)
        except (TypeError, ValueError):
            continue
        num = max(2, min(99, num))
        cleaned.append(num)
        if len(cleaned) >= 14:
            break

    actions = build_selection_sort_actions(cleaned)
    return jsonify({"actions": actions, "values": cleaned})

# ---------------------------
# Sorting Algorithms (Quick Sort)
# ---------------------------
def build_quick_sort_actions(values):
    actions = []
    arr = list(values)

    def partition(lo, hi):
        pivot_index = hi
        pivot_value = arr[pivot_index]
        actions.append({
            "type": "pivot",
            "index": pivot_index,
            "desc": f"Pick pivot {pivot_value} at index {pivot_index} (range {lo}-{hi})."
        })

        i = lo
        for j in range(lo, hi):
            actions.append({
                "type": "compare",
                "indices": [j, pivot_index],
                "desc": f"Compare {arr[j]} with pivot {pivot_value}."
            })
            if arr[j] <= pivot_value:
                if i != j:
                    actions.append({
                        "type": "swap",
                        "i": i,
                        "j": j,
                        "desc": f"Swap {arr[i]} at index {i} with {arr[j]} at index {j}."
                    })
                    arr[i], arr[j] = arr[j], arr[i]
                i += 1

        if i != hi:
            actions.append({
                "type": "swap",
                "i": i,
                "j": hi,
                "desc": f"Swap {arr[i]} at index {i} with pivot {arr[hi]} at index {hi}."
            })
            arr[i], arr[hi] = arr[hi], arr[i]

        actions.append({
            "type": "pivot_done",
            "index": i,
            "desc": f"Pivot {pivot_value} placed at index {i}."
        })
        return i

    def quick_sort(lo, hi):
        if lo >= hi:
            return
        actions.append({
            "type": "range",
            "range": [lo, hi],
            "desc": f"Sort subarray indices {lo}-{hi}."
        })
        pivot = partition(lo, hi)
        quick_sort(lo, pivot - 1)
        quick_sort(pivot + 1, hi)

    if arr:
        quick_sort(0, len(arr) - 1)
    actions.append({"type": "done", "desc": "Array sorted."})
    return actions


@app.route("/works/sorting/quick-steps", methods=["POST"])
def quick_sort_steps():
    data = request.get_json(silent=True) or {}
    raw_values = data.get("values", [])

    cleaned = []
    for value in raw_values:
        try:
            num = int(value)
        except (TypeError, ValueError):
            continue
        num = max(2, min(99, num))
        cleaned.append(num)
        if len(cleaned) >= 14:
            break

    actions = build_quick_sort_actions(cleaned)
    return jsonify({"actions": actions, "values": cleaned})


# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html", site_name=SITE_NAME, page_class="theme-home")


@app.route("/works")
def works():
    return render_template("works.html", site_name=SITE_NAME, page_class="theme-works")


@app.route("/works/queue", methods=["GET", "POST"])
def works_queue():
    global queue_ds
    message = None
    category = None

    if request.method == "POST":
        action = request.form.get("action")
        value = (request.form.get("value") or "").strip()

        if action == "enqueue":
            if value:
                queue_ds.enqueue(value)
                message = f"Enqueued: {value}"
                category = "success"
            else:
                message = "Please enter a value to enqueue."
                category = "warning"

        elif action == "dequeue":
            removed = queue_ds.dequeue()
            if removed is None:
                message = "Queue is empty."
                category = "danger"
            else:
                message = f"Dequeued: {removed}"
                category = "success"

        elif action == "reset":
            queue_ds = Queue()
            message = "Queue has been reset."
            category = "success"

    items = queue_ds.display()
    return render_template(
        "queue.html",
        site_name=SITE_NAME,
        items=items,
        page_class="theme-queue",
        message=message,
        category=category
    )


@app.route("/works/deque", methods=["GET", "POST"])
def works_deque():
    global deque_ds
    message = None
    category = None

    if request.method == "POST":
        action = request.form.get("action")
        value = (request.form.get("value") or "").strip()

        if action == "enqueue":
            if value:
                deque_ds.enqueue_tail(value)
                message = f"Enqueued at tail: {value}"
                category = "success"
            else:
                message = "Please enter a value."
                category = "warning"

        elif action == "enqueue_head":
            if value:
                deque_ds.enqueue_head(value)
                message = f"Enqueued at head: {value}"
                category = "success"
            else:
                message = "Please enter a value."
                category = "warning"

        elif action == "dequeue":
            removed = deque_ds.dequeue_tail()
            if removed is None:
                message = "Deque is empty."
                category = "danger"
            else:
                message = f"Dequeued at tail: {removed}"
                category = "success"

        elif action == "dequeue_head":
            removed = deque_ds.dequeue_head()
            if removed is None:
                message = "Deque is empty."
                category = "danger"
            else:
                message = f"Dequeued at head: {removed}"
                category = "success"

        elif action == "reset":
            deque_ds = Deque()
            message = "Deque has been reset."
            category = "success"

    items = deque_ds.display()
    return render_template(
        "deque.html",
        site_name=SITE_NAME,
        items=items,
        page_class="theme-deque",
        message=message,
        category=category
    )


@app.route("/works/tree", methods=["GET", "POST"])
def works_tree():
    global tree_ds
    message = None
    category = None
    traversal_type = "inorder"
    traversal_output = None
    found_id = None

    if request.method == "POST":
        action = request.form.get("action")
        value = (request.form.get("value") or "").strip()
        parent_id = (request.form.get("parent_id") or "").strip()
        traversal_type = request.form.get("traversal_type", "inorder")

        if action in ("insert", "insert_left", "insert_right", "search", "delete") and not value:
            message = "Please enter a value."
            category = "warning"

        elif action == "insert":
            ok, msg = tree_ds.insert(value)
            message = msg
            category = "success" if ok else "danger"

        elif action == "insert_left":
            parent = tree_ds.search_id(tree_ds.root, parent_id)
            if parent:
                ok, msg = tree_ds.insert_left(parent, value)
                message = msg
                category = "success" if ok else "danger"
            else:
                message = "Reference parent not found."
                category = "danger"

        elif action == "insert_right":
            parent = tree_ds.search_id(tree_ds.root, parent_id)
            if parent:
                ok, msg = tree_ds.insert_right(parent, value)
                message = msg
                category = "success" if ok else "danger"
            else:
                message = "Reference parent not found."
                category = "danger"

        elif action == "search":
            found = tree_ds.search_value(tree_ds.root, value)
            if found:
                found_id = found.id
                message = f"Found: {value}"
                category = "success"
            else:
                message = f"{value} not found."
                category = "danger"

        elif action == "delete":
            deleted = tree_ds.delete_value(value)
            message = f"Deleted {value}." if deleted else f"{value} not found."
            category = "success" if deleted else "danger"

        elif action == "reset":
            tree_ds = BinaryTree()
            message = "Tree reset (empty)."
            category = "success"

        elif action == "traversal":
            traversal_output = []
            if tree_ds.root:
                if traversal_type == "inorder":
                    tree_ds.inorder(tree_ds.root, traversal_output)
                elif traversal_type == "preorder":
                    tree_ds.preorder(tree_ds.root, traversal_output)
                elif traversal_type == "postorder":
                    tree_ds.postorder(tree_ds.root, traversal_output)

    nodes_for_ref = tree_ds.collect_nodes(tree_ds.root, only_not_full=True)
    default_ref = tree_ds.first_not_full_node()
    default_ref_id = default_ref.id if default_ref else None

    return render_template(
        "tree.html",
        site_name=SITE_NAME,
        root=tree_ds.root,
        nodes_for_ref=nodes_for_ref,
        default_ref_id=default_ref_id,
        traversal_type=traversal_type,
        traversal_output=traversal_output,
        message=message,
        category=category,
        found_id=found_id,
        page_class="theme-tree"
    )


@app.route("/works/bst", methods=["GET", "POST"])
def works_bst():
    global bst_ds
    message = None
    category = None
    traversal_type = "inorder"
    traversal_output = None
    found_id = None
    max_value = None
    height_value = None

    if request.method == "POST":
        action = request.form.get("action")
        raw_value = (request.form.get("value") or "").strip()
        traversal_type = request.form.get("traversal_type", "inorder")

        def parse_int(x):
            try:
                return int(x)
            except:
                return None

        val = parse_int(raw_value) if raw_value else None

        if action in ("insert", "search", "delete") and val is None:
            message = "BST only accepts integer values."
            category = "warning"

        elif action == "insert":
            ok, msg = bst_ds.insert(val)
            message = msg
            category = "success"

        elif action == "search":
            found = bst_ds.search(bst_ds.root, val)
            if found:
                found_id = found.id
                message = f"Found: {val}"
                category = "success"
            else:
                message = f"{val} not found."
                category = "danger"

        elif action == "delete":
            bst_ds.root, deleted = bst_ds.delete(bst_ds.root, val)
            message = f"Deleted {val}." if deleted else f"{val} not found."
            category = "success" if deleted else "danger"

        elif action == "get_max":
            max_value = bst_ds.get_max_value(bst_ds.root)
            message = f"Max value: {max_value}" if max_value is not None else "BST is empty."
            category = "success" if max_value is not None else "danger"

        elif action == "height":
            height_value = bst_ds.find_height(bst_ds.root)
            message = f"Height (edges): {height_value}" if bst_ds.root else "BST is empty."
            category = "success" if bst_ds.root else "danger"

        elif action == "reset":
            bst_ds = BinarySearchTree()
            message = "BST reset (empty)."
            category = "success"

        elif action == "traversal":
            traversal_output = []
            if bst_ds.root:
                if traversal_type == "inorder":
                    bst_ds.inorder(bst_ds.root, traversal_output)
                elif traversal_type == "preorder":
                    bst_ds.preorder(bst_ds.root, traversal_output)
                elif traversal_type == "postorder":
                    bst_ds.postorder(bst_ds.root, traversal_output)

    return render_template(
        "bst.html",
        site_name=SITE_NAME,
        root=bst_ds.root,
        traversal_type=traversal_type,
        traversal_output=traversal_output,
        message=message,
        category=category,
        found_id=found_id,
        max_value=max_value,
        height_value=height_value,
        page_class="theme-bst"
    )


# ---------------------------
# Graph Route
# ---------------------------
@app.route("/works/graph", methods=["GET", "POST"])
def works_graph():
    message = None
    category = None
    start = None
    end = None
    path = None

    stations = sorted(rail_graph.adj.keys(), key=lambda s: s.lower())

    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")

        if not start or not end:
            message = "Please select both start and destination stations."
            category = "warning"
        elif start == end:
            path = [start]
            message = "Start and destination are the same station."
            category = "success"
        else:
            path = rail_graph.shortest_path_bfs(start, end)
            if path is None:
                message = "No path found (check if stations are connected)."
                category = "danger"
            else:
                message = f"Shortest path found: {len(path)-1} stops."
                category = "success"

    transfers = [
        ["Doroteo Jose", "Recto"],
        ["Araneta Center-Cubao (MRT-3)", "Araneta Center-Cubao (LRT-2)"],
        ["EDSA", "Taft Avenue"]
    ]

    return render_template(
        "graph.html",
        site_name=SITE_NAME,
        stations=stations,
        start=start,
        end=end,
        path=path,
        coords=rail_coords,
        lines=rail_lines,
        label_meta=rail_label_meta,
        label_text=rail_label_text,
        transfers=rail_transfers,
        message=message,
        category=category,
        page_class="theme-graph"
    )



@app.route("/about")
def about():
    members = [
        {"name": "Angelo Raphael M. Biticon", "first": "Angelo", "email": "angelobiticon@gmail.com",
         "role": "Front-end Developer",
         "desc": "Worked on building responsive UI components and improving user interaction across the portfolio.",
         "photo": "angelo.png"},
        {"name": "Dave D. Casinginan", "first": "Dave", "email": "davecasinginan@gmail.com",
         "role": "Front-end Developer",
         "desc": "Contributed to interface design and interactive controls for the data structure demos.",
         "photo": "dave.jpg"},
        {"name": "Dave Michael P. Sinsioco", "first": "Dave", "email": "sinciocodave@gmail.com",
         "role": "Back-end Developer",
         "desc": "Implemented core data structure logic and server-side operations for the application.",
         "photo": "michael.jpg"},
        {"name": "John Mike P. Asuncion", "first": "John", "email": "johnmikeasuncion17@gmail.com",
         "role": "Front-end Developer",
         "desc": "Helped develop the base layout system and styling to keep the UI consistent and clean.",
         "photo": "mike.jpg"},
        {"name": "Luke Philip L. Lopez", "first": "Luke", "email": "lukephilip299@gmail.com",
         "role": "Back-end Developer",
         "desc": "Supported back-end logic and routing, ensuring the demos function correctly end-to-end.",
         "photo": "luke.jpg"},
        {"name": "Rein Gabriel Atienza", "first": "Rein", "email": "atienza.reingabriel308129@gmail.com",
         "role": "Back-end Developer",
         "desc": "Assisted with implementing and validating algorithms and structure behavior on the server side.",
         "photo": "rein.jpg"},
        {"name": "Renier G. Dela Cruz", "first": "Renier", "email": "renier@gmail.com",
         "role": "Front-end Developer",
         "desc": "Contributed to page layouts, UI polish, and overall visual consistency of the portfolio.",
         "photo": "renier.jpg"},
        {"name": "Roswell M. Buñag", "first": "Roswell", "email": "roswell@gmail.com",
         "role": "Front-end Developer",
         "desc": "Worked on structuring the works section UI and improving navigation between demos.",
         "photo": "roswell.png"},
        {"name": "Zybert Jio D. Sibolboro", "first": "Zybert", "email": "zybertjiosibolboro@gmail.com",
         "role": "Front-end Developer",
         "desc": "Helped implement interactive visuals and controls for the data structure modules.",
         "photo": "zybert.jpg"},
    ]
    members_sorted = sorted(members, key=lambda m: m["first"].lower())
    return render_template("about.html", site_name=SITE_NAME, members=members_sorted, page_class="theme-about")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False
    name = None
    if request.method == "POST":
        submitted = True
        name = request.form.get("name")
    return render_template("contact.html", site_name=SITE_NAME, submitted=submitted, name=name, page_class="theme-contact")


if __name__ == "__main__":
    app.run(debug=True)
