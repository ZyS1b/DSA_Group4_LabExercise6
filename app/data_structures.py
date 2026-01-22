import uuid
from queue import Queue as PyQueue


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


class TreeNode:
    def __init__(self, value, node_id=None):
        self.value = value
        self.left = None
        self.right = None
        self.id = node_id or str(uuid.uuid4())


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
            if cur.left:
                q.append(cur.left)
            if cur.right:
                q.append(cur.right)
        return None

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

    @staticmethod
    def node_to_dict(node):
        if node is None:
            return None
        return {
            "id": node.id,
            "value": node.value,
            "left": BinaryTree.node_to_dict(node.left),
            "right": BinaryTree.node_to_dict(node.right),
        }

    @staticmethod
    def dict_to_node(data):
        if not data:
            return None
        node = TreeNode(data.get("value"), data.get("id"))
        node.left = BinaryTree.dict_to_node(data.get("left"))
        node.right = BinaryTree.dict_to_node(data.get("right"))
        return node

    def to_dict(self):
        return self.node_to_dict(self.root)

    @classmethod
    def from_dict(cls, data):
        tree = cls()
        tree.root = cls.dict_to_node(data)
        return tree


class BSTNode:
    def __init__(self, value, node_id=None):
        self.value = value
        self.left = None
        self.right = None
        self.id = node_id or str(uuid.uuid4())


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

    @staticmethod
    def node_to_dict(node):
        if node is None:
            return None
        return {
            "id": node.id,
            "value": node.value,
            "left": BinarySearchTree.node_to_dict(node.left),
            "right": BinarySearchTree.node_to_dict(node.right),
        }

    @staticmethod
    def dict_to_node(data):
        if not data:
            return None
        node = BSTNode(data.get("value"), data.get("id"))
        node.left = BinarySearchTree.dict_to_node(data.get("left"))
        node.right = BinarySearchTree.dict_to_node(data.get("right"))
        return node

    def to_dict(self):
        return self.node_to_dict(self.root)

    @classmethod
    def from_dict(cls, data):
        tree = cls()
        tree.root = cls.dict_to_node(data)
        return tree


class RailGraph:
    def __init__(self):
        self.adj = {}

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
