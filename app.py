from flask import Flask, render_template, request

app = Flask(__name__)

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

import uuid

# ---------------------------
# Binary Search Tree (BST)
# ---------------------------
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        # unique id so reference dropdown handles duplicates safely
        self.id = str(uuid.uuid4())


class BinarySearchTree:
    def __init__(self):
        self.root = None

    # ---------------------------
    # BST INSERT (auto-place by value)
    # ---------------------------
    def insert(self, value):
        """Insert value following BST rules. Reject duplicates."""
        new_node = TreeNode(value)

        if self.root is None:
            self.root = new_node
            return True, f"Inserted root {value}"

        cur = self.root
        while True:
            if value < cur.value:
                if cur.left is None:
                    cur.left = new_node
                    return True, f"Inserted {value} to LEFT of {cur.value}"
                cur = cur.left
            elif value > cur.value:
                if cur.right is None:
                    cur.right = new_node
                    return True, f"Inserted {value} to RIGHT of {cur.value}"
                cur = cur.right
            else:
                return False, f"Duplicate value {value} not allowed in BST."

    # ---------------------------
    # INSERT LEFT / RIGHT WITH VALIDATION
    # (only if side is empty and value respects BST rule)
    # ---------------------------
    def insert_left(self, parent, value):
        if value >= parent.value:
            return False, f"{value} must be LESS than {parent.value} to insert LEFT."
        if parent.left is not None:
            return False, f"Left child of {parent.value} already exists."
        parent.left = TreeNode(value)
        return True, f"Inserted {value} to LEFT of {parent.value}"

    def insert_right(self, parent, value):
        if value <= parent.value:
            return False, f"{value} must be GREATER than {parent.value} to insert RIGHT."
        if parent.right is not None:
            return False, f"Right child of {parent.value} already exists."
        parent.right = TreeNode(value)
        return True, f"Inserted {value} to RIGHT of {parent.value}"

    # ---------------------------
    # SEARCH
    # ---------------------------
    def search_value(self, root, key):
        """BST search by value."""
        cur = root
        while cur:
            if key < cur.value:
                cur = cur.left
            elif key > cur.value:
                cur = cur.right
            else:
                return cur
        return None

    def search_id(self, root, node_id):
        """Search by unique id (for reference dropdown)."""
        if root is None:
            return None
        if root.id == node_id:
            return root
        left_found = self.search_id(root.left, node_id)
        if left_found:
            return left_found
        return self.search_id(root.right, node_id)

    # ---------------------------
    # TRAVERSALS
    # ---------------------------
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

    # ---------------------------
    # DELETE (BST standard)
    # ---------------------------
    def delete_node(self, root, key):
        if root is None:
            return root, False

        if key < root.value:
            root.left, deleted = self.delete_node(root.left, key)
            return root, deleted
        elif key > root.value:
            root.right, deleted = self.delete_node(root.right, key)
            return root, deleted

        # found node
        if root.left is None and root.right is None:
            return None, True
        if root.left is None:
            return root.right, True
        if root.right is None:
            return root.left, True

        # two children: replace with inorder successor
        succ_parent = root
        succ = root.right
        while succ.left:
            succ_parent = succ
            succ = succ.left

        root.value = succ.value
        root.id = succ.id  # keep id tied to actual node value

        if succ_parent.left == succ:
            succ_parent.left, _ = self.delete_node(succ_parent.left, succ.value)
        else:
            succ_parent.right, _ = self.delete_node(succ_parent.right, succ.value)

        return root, True

    # ---------------------------
    # HELPERS FOR REFERENCE DROPDOWN
    # ---------------------------
    def collect_nodes(self, root, only_not_full=False, out=None):
        if out is None:
            out = []
        if root:
            # preorder collection keeps a nice top-down ref list
            if (not only_not_full) or (root.left is None or root.right is None):
                out.append(root)
            self.collect_nodes(root.left, only_not_full, out)
            self.collect_nodes(root.right, only_not_full, out)
        return out

    def first_not_full_node(self):
        """Return first node that has a missing child."""
        nodes = self.collect_nodes(self.root, only_not_full=True)
        return nodes[0] if nodes else None

# ---------------------------
# App State
# ---------------------------
SITE_NAME = "Nodeus"
queue_ds = Queue()
deque_ds = Deque()
tree_ds = BinarySearchTree()  # start empty BST

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
            ok, msg = tree_ds.insert(val)
            message = msg
            category = "success" if ok else "danger"

        elif action == "search":
            found = tree_ds.search_value(tree_ds.root, val)
            if found:
                found_id = found.id          # pass node id to template
                message = f"Found: {val}"
                category = "success"
            else:
                message = f"{val} not found."
                category = "danger"

        elif action == "delete":
            tree_ds.root, deleted = tree_ds.delete_node(tree_ds.root, val)
            message = f"Deleted {val}." if deleted else f"{val} not found."
            category = "success" if deleted else "danger"

        elif action == "reset":
            tree_ds = BinarySearchTree()
            message = "BST reset (empty)."
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

    return render_template(
        "tree.html",
        site_name=SITE_NAME,
        root=tree_ds.root,
        traversal_type=traversal_type,
        traversal_output=traversal_output,
        message=message,
        category=category,
        found_id=found_id,
        page_class="theme-tree"
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

        {"name": "Roswell M. Buñag", "first": "Roswell", "email": "roswellbunag05@gmail.com",
        "role": "Front-end Developer",
        "desc": "Worked on structuring the works section UI and improving navigation between demos.",
        "photo": "roswell.png"},

        {"name": "Zybert Jio D. Sibolboro", "first": "Zybert", "email": "zybertjiosibolboro@gmail.com",
        "role": "Front-end Developer",
        "desc": "Helped implement interactive visuals and controls for the data structure modules.",
        "photo": "zybert.jpg"},
    ]

    members_sorted = sorted(members, key=lambda m: m["first"].lower())
    return render_template(
        "about.html",
        site_name=SITE_NAME,
        members=members_sorted,
        page_class="theme-about"
    )

@app.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False
    name = None
    if request.method == "POST":
        submitted = True
        name = request.form.get("name")
    return render_template(
        "contact.html",
        site_name=SITE_NAME,
        submitted=submitted,
        name=name,
        page_class="theme-contact"
    )

if __name__ == "__main__":
    app.run(debug=True)
