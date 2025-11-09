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
    """Linked-list based FIFO queue (enqueue at tail, dequeue at head)."""
    def __init__(self):
        self.head = None  # dequeue here
        self.tail = None  # enqueue here

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
    """Linked-list based double-ended queue using head & tail."""
    def __init__(self):
        self.head = None  # front
        self.tail = None  # rear

    def is_empty(self):
        return self.head is None

    # enqueue (default) -> tail
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

    # dequeue (default) -> tail
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
# App State
# ---------------------------
SITE_NAME = "Nodeus"
queue_ds = Queue()
deque_ds = Deque()


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
    message = None
    category = None
    if request.method == "POST":
        action = request.form.get("action")
        value = (request.form.get("value") or "").strip()

        if action == "enqueue":
            if value:
                deque_ds.enqueue(value)
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
            removed = deque_ds.dequeue()
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

    items = deque_ds.display()
    return render_template(
        "deque.html",
        site_name=SITE_NAME,
        items=items,
        page_class="theme-deque",
        message=message,
        category=category
    )

@app.route("/about")
def about():
    """
    Photos are expected to be placed under:
      static/images/
    using FirstName.jpg (or .png). For duplicate first names,
    this setup uses an initial to avoid collisions (e.g., DaveC.jpg, DaveS.jpg).
    """
    members = [
        # Role mapping (your list):
        # 1. Home Page - Dela Cruz
        # 2. Works Page - Ros
        # 3. Queue Page - Casinginan
        # 4. Deque Page - Sibolboro
        # 5. About Page - Cute  -> assume Luke as "Cute"
        # 6. Contact Page - Biticon
        # 7. Queue Structure - Asuncion
        # 8. Deque Structure - Dave S.
        # 9. Base Template & Styling - Atienza
        {"name": "Angelo Raphael M. Biticon", "first": "Angelo", "email": "angelo@gmail.com",
         "role": "Contact Page", "desc": "Implemented a clean, accessible contact workflow and form handling.",
         "photo": "angelo.png"},

        {"name": "Dave Casinginan", "first": "Dave", "email": "dave.c@gmail.com",
         "role": "Queue Page", "desc": "Designed and implemented the Queue page operations and UI.",
         "photo": "dave.png"},

        {"name": "Dave Michael P. Sinsioco", "first": "Dave", "email": "dave.michael@gmail.com",
         "role": "Deque Structure", "desc": "Engineered the linked-list Deque internals for efficient two-ended ops.",
         "photo": "michael.jpg"},

        {"name": "John Mike P. Asuncion", "first": "John", "email": "johnmike@gmail.com",
         "role": "Queue Structure", "desc": "Structured the FIFO logic with a robust linked-list implementation.",
         "photo": "mike.jpg"},

        {"name": "Luke Philip L. Lopez", "first": "Luke", "email": "luke28@gmail.com",
         "role": "About Page", "desc": "Authored and organized the team profile and summary content.",
         "photo": "luke.jpg"},

        {"name": "Rein Gabriel Atienza", "first": "Rein", "email": "rein@gmail.com",
         "role": "Base Template & Styling", "desc": "Built the base layout and neon theme for a cohesive look.",
         "photo": "rein.jpg"},

        {"name": "Renier G. Dela Cruz", "first": "Renier", "email": "renier@gmail.com",
         "role": "Home Page", "desc": "Crafted the landing copy and hero layout to introduce the project.",
         "photo": "renier.jpg"},

        {"name": "Roswell M. Buñag", "first": "Roswell", "email": "roswell@gmail.com",
         "role": "Works Page", "desc": "Built the Works overview and navigation to Queue/Deque demos.",
         "photo": "roswell.jpg"},

        {"name": "Zybert Jio D. Sibolboro", "first": "Zybert", "email": "zybert@gmail.com",
         "role": "Deque Page", "desc": "Implemented the Deque page controls and display behavior.",
         "photo": "zybert.jpg"},
    ]

    # Sort alphabetically by the first name for rendering
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
    return render_template("contact.html", site_name=SITE_NAME, submitted=submitted, name=name, page_class="theme-contact")


if __name__ == "__main__":
    app.run(debug=True)
