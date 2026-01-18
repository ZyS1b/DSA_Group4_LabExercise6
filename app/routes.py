from flask import Blueprint, current_app, render_template, request

from . import state
from .data_structures import BinarySearchTree, BinaryTree, Deque, Queue


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    site_name = current_app.config.get("SITE_NAME", state.SITE_NAME)
    return render_template("index.html", site_name=site_name, page_class="theme-home")


@main_blueprint.route("/works")
def works():
    site_name = current_app.config.get("SITE_NAME", state.SITE_NAME)
    return render_template("works.html", site_name=site_name, page_class="theme-works")


@main_blueprint.route("/works/queue", methods=["GET", "POST"])
def works_queue():
    message = None
    category = None

    if request.method == "POST":
        action = request.form.get("action")
        value = (request.form.get("value") or "").strip()

        if action == "enqueue":
            if value:
                state.queue_ds.enqueue(value)
                message = f"Enqueued: {value}"
                category = "success"
            else:
                message = "Please enter a value to enqueue."
                category = "warning"

        elif action == "dequeue":
            removed = state.queue_ds.dequeue()
            if removed is None:
                message = "Queue is empty."
                category = "danger"
            else:
                message = f"Dequeued: {removed}"
                category = "success"

        elif action == "reset":
            state.queue_ds = Queue()
            message = "Queue has been reset."
            category = "success"

    items = state.queue_ds.display()
    site_name = current_app.config.get("SITE_NAME", state.SITE_NAME)
    return render_template(
        "queue.html",
        site_name=site_name,
        items=items,
        page_class="theme-queue",
        message=message,
        category=category,
    )


@main_blueprint.route("/works/deque", methods=["GET", "POST"])
def works_deque():
    message = None
    category = None

    if request.method == "POST":
        action = request.form.get("action")
        value = (request.form.get("value") or "").strip()

        if action == "enqueue":
            if value:
                state.deque_ds.enqueue_tail(value)
                message = f"Enqueued at tail: {value}"
                category = "success"
            else:
                message = "Please enter a value."
                category = "warning"

        elif action == "enqueue_head":
            if value:
                state.deque_ds.enqueue_head(value)
                message = f"Enqueued at head: {value}"
                category = "success"
            else:
                message = "Please enter a value."
                category = "warning"

        elif action == "dequeue":
            removed = state.deque_ds.dequeue_tail()
            if removed is None:
                message = "Deque is empty."
                category = "danger"
            else:
                message = f"Dequeued at tail: {removed}"
                category = "success"

        elif action == "dequeue_head":
            removed = state.deque_ds.dequeue_head()
            if removed is None:
                message = "Deque is empty."
                category = "danger"
            else:
                message = f"Dequeued at head: {removed}"
                category = "success"

        elif action == "reset":
            state.deque_ds = Deque()
            message = "Deque has been reset."
            category = "success"

    items = state.deque_ds.display()
    site_name = current_app.config.get("SITE_NAME", state.SITE_NAME)
    return render_template(
        "deque.html",
        site_name=site_name,
        items=items,
        page_class="theme-deque",
        message=message,
        category=category,
    )


@main_blueprint.route("/works/tree", methods=["GET", "POST"])
def works_tree():
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
            ok, msg = state.tree_ds.insert(value)
            message = msg
            category = "success" if ok else "danger"

        elif action == "insert_left":
            parent = state.tree_ds.search_id(state.tree_ds.root, parent_id)
            if parent:
                ok, msg = state.tree_ds.insert_left(parent, value)
                message = msg
                category = "success" if ok else "danger"
            else:
                message = "Reference parent not found."
                category = "danger"

        elif action == "insert_right":
            parent = state.tree_ds.search_id(state.tree_ds.root, parent_id)
            if parent:
                ok, msg = state.tree_ds.insert_right(parent, value)
                message = msg
                category = "success" if ok else "danger"
            else:
                message = "Reference parent not found."
                category = "danger"

        elif action == "search":
            found = state.tree_ds.search_value(state.tree_ds.root, value)
            if found:
                found_id = found.id
                message = f"Found: {value}"
                category = "success"
            else:
                message = f"{value} not found."
                category = "danger"

        elif action == "delete":
            deleted = state.tree_ds.delete_value(value)
            message = f"Deleted {value}." if deleted else f"{value} not found."
            category = "success" if deleted else "danger"

        elif action == "reset":
            state.tree_ds = BinaryTree()
            message = "Tree reset (empty)."
            category = "success"

        elif action == "traversal":
            traversal_output = []
            if state.tree_ds.root:
                if traversal_type == "inorder":
                    state.tree_ds.inorder(state.tree_ds.root, traversal_output)
                elif traversal_type == "preorder":
                    state.tree_ds.preorder(state.tree_ds.root, traversal_output)
                elif traversal_type == "postorder":
                    state.tree_ds.postorder(state.tree_ds.root, traversal_output)

    nodes_for_ref = state.tree_ds.collect_nodes(state.tree_ds.root, only_not_full=True)
    default_ref = state.tree_ds.first_not_full_node()
    default_ref_id = default_ref.id if default_ref else None
    site_name = current_app.config.get("SITE_NAME", state.SITE_NAME)

    return render_template(
        "tree.html",
        site_name=site_name,
        root=state.tree_ds.root,
        nodes_for_ref=nodes_for_ref,
        default_ref_id=default_ref_id,
        traversal_type=traversal_type,
        traversal_output=traversal_output,
        message=message,
        category=category,
        found_id=found_id,
        page_class="theme-tree",
    )


@main_blueprint.route("/works/bst", methods=["GET", "POST"])
def works_bst():
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

        def parse_int(value):
            try:
                return int(value)
            except (TypeError, ValueError):
                return None

        val = parse_int(raw_value) if raw_value else None

        if action in ("insert", "search", "delete") and val is None:
            message = "BST only accepts integer values."
            category = "warning"

        elif action == "insert":
            ok, msg = state.bst_ds.insert(val)
            message = msg
            category = "success"

        elif action == "search":
            found = state.bst_ds.search(state.bst_ds.root, val)
            if found:
                found_id = found.id
                message = f"Found: {val}"
                category = "success"
            else:
                message = f"{val} not found."
                category = "danger"

        elif action == "delete":
            state.bst_ds.root, deleted = state.bst_ds.delete(state.bst_ds.root, val)
            message = f"Deleted {val}." if deleted else f"{val} not found."
            category = "success" if deleted else "danger"

        elif action == "get_max":
            max_value = state.bst_ds.get_max_value(state.bst_ds.root)
            message = f"Max value: {max_value}" if max_value is not None else "BST is empty."
            category = "success" if max_value is not None else "danger"

        elif action == "height":
            height_value = state.bst_ds.find_height(state.bst_ds.root)
            message = f"Height (edges): {height_value}" if state.bst_ds.root else "BST is empty."
            category = "success" if state.bst_ds.root else "danger"

        elif action == "reset":
            state.bst_ds = BinarySearchTree()
            message = "BST reset (empty)."
            category = "success"

        elif action == "traversal":
            traversal_output = []
            if state.bst_ds.root:
                if traversal_type == "inorder":
                    state.bst_ds.inorder(state.bst_ds.root, traversal_output)
                elif traversal_type == "preorder":
                    state.bst_ds.preorder(state.bst_ds.root, traversal_output)
                elif traversal_type == "postorder":
                    state.bst_ds.postorder(state.bst_ds.root, traversal_output)

    site_name = current_app.config.get("SITE_NAME", state.SITE_NAME)
    return render_template(
        "bst.html",
        site_name=site_name,
        root=state.bst_ds.root,
        traversal_type=traversal_type,
        traversal_output=traversal_output,
        message=message,
        category=category,
        found_id=found_id,
        max_value=max_value,
        height_value=height_value,
        page_class="theme-bst",
    )


@main_blueprint.route("/works/graph", methods=["GET", "POST"])
def works_graph():
    message = None
    category = None
    start = None
    end = None
    path = None

    stations = sorted(state.rail_graph.adj.keys(), key=lambda s: s.lower())

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
            path = state.rail_graph.shortest_path_bfs(start, end)
            if path is None:
                message = "No path found (check if stations are connected)."
                category = "danger"
            else:
                message = f"Shortest path found: {len(path) - 1} stops."
                category = "success"

    site_name = current_app.config.get("SITE_NAME", state.SITE_NAME)
    return render_template(
        "graph.html",
        site_name=site_name,
        stations=stations,
        start=start,
        end=end,
        path=path,
        coords=state.rail_coords,
        lines=state.rail_lines,
        label_meta=state.rail_label_meta,
        label_text=state.rail_label_text,
        transfers=state.rail_transfers,
        message=message,
        category=category,
        page_class="theme-graph",
    )


@main_blueprint.route("/about")
def about():
    members = [
        {
            "name": "Angelo Raphael M. Biticon",
            "first": "Angelo",
            "email": "angelobiticon@gmail.com",
            "role": "Front-end Developer",
            "desc": "Worked on building responsive UI components and improving user interaction across the portfolio.",
            "photo": "angelo.png",
        },
        {
            "name": "Dave D. Casinginan",
            "first": "Dave",
            "email": "davecasinginan@gmail.com",
            "role": "Front-end Developer",
            "desc": "Contributed to interface design and interactive controls for the data structure demos.",
            "photo": "dave.jpg",
        },
        {
            "name": "Dave Michael P. Sinsioco",
            "first": "Dave",
            "email": "sinciocodave@gmail.com",
            "role": "Back-end Developer",
            "desc": "Implemented core data structure logic and server-side operations for the application.",
            "photo": "michael.jpg",
        },
        {
            "name": "John Mike P. Asuncion",
            "first": "John",
            "email": "johnmikeasuncion17@gmail.com",
            "role": "Front-end Developer",
            "desc": "Helped develop the base layout system and styling to keep the UI consistent and clean.",
            "photo": "mike.jpg",
        },
        {
            "name": "Luke Philip L. Lopez",
            "first": "Luke",
            "email": "lukephilip299@gmail.com",
            "role": "Back-end Developer",
            "desc": "Supported back-end logic and routing, ensuring the demos function correctly end-to-end.",
            "photo": "luke.jpg",
        },
        {
            "name": "Rein Gabriel Atienza",
            "first": "Rein",
            "email": "atienza.reingabriel308129@gmail.com",
            "role": "Back-end Developer",
            "desc": "Assisted with implementing and validating algorithms and structure behavior on the server side.",
            "photo": "rein.jpg",
        },
        {
            "name": "Renier G. Dela Cruz",
            "first": "Renier",
            "email": "renier@gmail.com",
            "role": "Front-end Developer",
            "desc": "Contributed to page layouts, UI polish, and overall visual consistency of the portfolio.",
            "photo": "renier.jpg",
        },
        {
            "name": "Roswell M. BuAñag",
            "first": "Roswell",
            "email": "roswell@gmail.com",
            "role": "Front-end Developer",
            "desc": "Worked on structuring the works section UI and improving navigation between demos.",
            "photo": "roswell.png",
        },
        {
            "name": "Zybert Jio D. Sibolboro",
            "first": "Zybert",
            "email": "zybertjiosibolboro@gmail.com",
            "role": "Front-end Developer",
            "desc": "Helped implement interactive visuals and controls for the data structure modules.",
            "photo": "zybert.jpg",
        },
    ]
    members_sorted = sorted(members, key=lambda member: member["first"].lower())
    site_name = current_app.config.get("SITE_NAME", state.SITE_NAME)
    return render_template(
        "about.html",
        site_name=site_name,
        members=members_sorted,
        page_class="theme-about",
    )


@main_blueprint.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False
    name = None
    if request.method == "POST":
        submitted = True
        name = request.form.get("name")
    site_name = current_app.config.get("SITE_NAME", state.SITE_NAME)
    return render_template(
        "contact.html",
        site_name=site_name,
        submitted=submitted,
        name=name,
        page_class="theme-contact",
    )
