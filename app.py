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
SITE_NAME = "Nodeus"  # short, one-word, data-structures vibe
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
    # Keeping the original nine members from your earlier list,
    # and pairing them with concise roles aligned to your new outline.
    members = [
        {"name": "Zybert Jio D. Sibolboro", "email": "zybert@gmail.com", "role": "Deque Page", "desc": "Built the Deque page with clean double-ended operations.", "photo": "https://picsum.photos/seed/zybert/220/220"},
        {"name": "John Mike P. Asuncion", "email": "johnmike@gmail.com", "role": "Queue Structure", "desc": "Structured the Queue components for smooth FIFO behavior.", "photo": "https://picsum.photos/seed/johnmike/220/220"},
        {"name": "Angelo Raphael M. Biticon", "email": "angelo@gmail.com", "role": "Contact Page", "desc": "Implemented the Contact page for fast, accessible feedback.", "photo": "https://picsum.photos/seed/angelo/220/220"},
        {"name": "Roswell M. Buñag", "email": "roswell@gmail.com", "role": "Website Design", "desc": "Shaped the core layout and visual system across pages.", "photo": "https://picsum.photos/seed/roswell/220/220"},
        {"name": "Renier G. Dela Cruz", "email": "renier@gmail.com", "role": "Queue Page", "desc": "Developed the Queue interactions and validation UX.", "photo": "https://picsum.photos/seed/renier/220/220"},
        {"name": "Luke Philip L. Lopez", "email": "luke28@gmail.com", "role": "Design & Integration", "desc": "Integrated pages, themes, and component-level styling.", "photo": "https://picsum.photos/seed/luke/220/220"},
        {"name": "Dave Michael P. Sinsioco", "email": "dave.michael@gmail.com", "role": "Queue Page", "desc": "Implemented enqueue/dequeue logic and display state.", "photo": "https://picsum.photos/seed/davems/220/220"},
        {"name": "Rein Gabriel Atienza", "email": "rein@gmail.com", "role": "Animations & Theming", "desc": "Crafted a cohesive, performant dark-theme experience.", "photo": "https://picsum.photos/seed/rein/220/220"},
        {"name": "Dave Casinginan", "email": "dave.c@gmail.com", "role": "Project Coordination", "desc": "Coordinated team tasks and kept delivery on track.", "photo": "https://picsum.photos/seed/davec/220/220"},
    ]
    return render_template("about.html", site_name=SITE_NAME, members=members, page_class="theme-about")

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
