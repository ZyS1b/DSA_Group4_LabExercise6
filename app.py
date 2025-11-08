from flask import Flask, render_template, request

app = Flask(__name__)

# ---------- Static Pages ----------
@app.route("/")
def home():
    # Member #1
    return render_template("index.html")

@app.route('/works', methods=['GET', 'POST'])
def works():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()
    return render_template('works.html', result=result)

@app.route("/work/queue", methods=["GET", "POST"])
def queue_work():
    # Member #3
    return render_template("queue.html")

@app.route("/work/deque", methods=["GET", "POST"])
def deque_work():
    global my_deque
    
    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("inputValue")

        if action == "enqueue_front" and value:
            my_deque.appendleft(value)
        elif action == "enqueue_rear" and value:
            my_deque.append(value)
        elif action == "dequeue_front":
            if my_deque:
                my_deque.popleft()
        elif action == "dequeue_rear":
            if my_deque:
                my_deque.pop()

    deque_contents = " ← ".join(my_deque) if my_deque else "[ empty ]"
    return render_template("deque.html", deque_contents=deque_contents)


@app.route("/about")
def about():
    # Member #5
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    # Member #6
    return render_template("contact.html")


# ---------- Queue Structure ----------
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        # Member #7
        pass

    def dequeue(self):
        # Member #7
        pass

    def display(self):
        # Member #7
        pass


# ---------- Deque Structure ----------
class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class Deque:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        # Member #8
        pass

    def enqueue_head(self, data):
        # Member #8
        pass

    def dequeue(self):
        # Member #8
        pass

    def dequeue_head(self):
        # Member #8
        pass

    def display(self):
        # Member #8
        pass


# ---------- Run App ----------
if __name__ == "__main__":
    # Member #9
    app.run(debug=True)
