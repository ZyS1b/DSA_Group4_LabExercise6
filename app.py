from flask import Flask, render_template, request
import uuid

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


# ---------------------------
# General Binary Tree (Module Behavior)
# ---------------------------
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        # unique id so reference dropdown handles duplicates safely
        self.id = str(uuid.uuid4())


class BinaryTree:
    def __init__(self):
        self.root = None

    # Level-order insert (first not-full node)
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

    # Insert left w/ subtree shift (module rule)
    def insert_left(self, parent, value):
        new_node = TreeNode(value)
        if parent.left is None:
            parent.left = new_node
        else:
            old = parent.left
            parent.left = new_node
            new_node.left = old
        return True, f"Inserted {value} to LEFT of {parent.value}"

    # Insert right w/ subtree shift (module rule)
    def insert_right(self, parent, value):
        new_node = TreeNode(value)
        if parent.right is None:
            parent.right = new_node
        else:
            old = parent.right
            parent.right = new_node
            new_node.right = old
        return True, f"Inserted {value} to RIGHT of {parent.value}"

    # Search by value (general BT BFS)
    def search_value(self, root, key):
        if root is None:
            return None
        q = [root]
        while q:
            cur = q.pop(0)
            if cur.value == key:
                return cur
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        return None

    # Search by id (for reference dropdown)
    def search_id(self, root, node_id):
        if root is None:
            return None
        q = [root]
        while q:
            cur = q.pop(0)
            if cur.id == node_id:
                return cur
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        return None

    # Deletion by value (general BT):
    # replace target with deepest-rightmost node
    def delete_value(self, key):
        if self.root is None:
            return False

        # single-node tree
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

        # copy deepest-rightmost into target
        target.value = last.value
        target.id = last.id

        # remove deepest-rightmost
        if parent_of_last and parent_of_last.right == last:
            parent_of_last.right = None
        elif parent_of_last and parent_of_last.left == last:
            parent_of_last.left = None

        return True

    # Traversals
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

    # Collect nodes for reference dropdown
    # only_not_full=True -> nodes missing L or R
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
# App State
# ---------------------------
SITE_NAME = "Nodeus"
queue_ds = Queue()
deque_ds = Deque()
tree_ds = BinaryTree()  # ✅ general binary tree (empty)


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
            if tree_ds.root is None:
                message = "Insert a root first."
                category = "warning"
            else:
                parent = tree_ds.search_id(tree_ds.root, parent_id)
                if parent:
                    ok, msg = tree_ds.insert_left(parent, value)
                    message = msg
                    category = "success" if ok else "danger"
                else:
                    message = "Reference parent not found."
                    category = "danger"

        elif action == "insert_right":
            if tree_ds.root is None:
                message = "Insert a root first."
                category = "warning"
            else:
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
