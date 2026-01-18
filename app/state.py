from .data_structures import Queue, Deque, BinaryTree, BinarySearchTree
from .graph_data import build_rail_graph_with_map


SITE_NAME = "Nodeus"

queue_ds = Queue()
deque_ds = Deque()
tree_ds = BinaryTree()
bst_ds = BinarySearchTree()

rail_graph, rail_coords, rail_lines, rail_label_meta, rail_label_text, rail_transfers = (
    build_rail_graph_with_map()
)
