import uuid

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def build_heap_tree(heap: list, index: int = 0) -> Node | None:
    """Будує бінарне дерево з масиву бінарної купи."""
    if index >= len(heap):
        return None

    node = Node(heap[index])
    node.left = build_heap_tree(heap, 2 * index + 1)
    node.right = build_heap_tree(heap, 2 * index + 2)
    return node


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            left_x = x - 1 / 2**layer
            pos[node.left.id] = (left_x, y - 1)
            add_edges(graph, node.left, pos, x=left_x, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            right_x = x + 1 / 2**layer
            pos[node.right.id] = (right_x, y - 1)
            add_edges(graph, node.right, pos, x=right_x, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root: Node) -> None:
    """Візуалізує бінарне дерево (купу) за допомогою NetworkX."""
    if tree_root is None:
        print("Купа порожня — немає що малювати.")
        return

    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=colors,
        font_size=10,
        font_weight="bold",
    )
    plt.title("Візуалізація бінарної купи")
    plt.show()


def draw_heap(heap: list) -> None:
    """Створює дерево з масиву купи та візуалізує його."""
    root = build_heap_tree(heap)
    draw_tree(root)


if __name__ == "__main__":
    # Max-heap: батько >= діти
    max_heap = [15, 10, 8, 5, 3, 1]
    print("Max-heap (масив):", max_heap)
    draw_heap(max_heap)
