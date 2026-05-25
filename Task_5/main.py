import uuid
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="#E0E0E0"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def build_demo_tree() -> Node:
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    return root


def clone_tree(node: Node | None) -> Node | None:
    if node is None:
        return None
    copy = Node(node.val)
    copy.left = clone_tree(node.left)
    copy.right = clone_tree(node.right)
    return copy


def reset_colors(node: Node | None, color: str = "#E0E0E0") -> None:
    if node is None:
        return
    node.color = color
    reset_colors(node.left, color)
    reset_colors(node.right, color)


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"


def visit_color(index: int, total: int, dark: str = "#0A3D7A", light: str = "#A8D4F5") -> str:
    """Колір за порядком відвідування: від темного до світлого."""
    if total <= 1:
        return dark

    ratio = index / (total - 1)
    r1, g1, b1 = hex_to_rgb(dark)
    r2, g2, b2 = hex_to_rgb(light)
    return rgb_to_hex(
        int(r1 + (r2 - r1) * ratio),
        int(g1 + (g2 - g1) * ratio),
        int(b1 + (b2 - b1) * ratio),
    )


def dfs_iterative(root: Node | None) -> list[Node]:
    """Обхід у глибину, через стек"""
    if root is None:
        return []

    stack = [root]
    order: list[Node] = []

    while stack:
        node = stack.pop()
        order.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order


def bfs_iterative(root: Node | None) -> list[Node]:
    """Обхід у ширину через чергу"""
    if root is None:
        return []

    queue = deque([root])
    order: list[Node] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return order


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


def draw_tree(tree_root: Node, title: str = "Бінарне дерево") -> None:
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
    plt.title(title)
    plt.show()


def visualize_traversal(root: Node, visit_order: list[Node], title: str, pause: float = 0.9) -> None:
    """Візуалізація обходу з градієнтом кольорів."""
    reset_colors(root)
    total = len(visit_order)

    plt.ion()
    for step in range(total):
        for index, node in enumerate(visit_order[: step + 1]):
            node.color = visit_color(index, total)

        tree = nx.DiGraph()
        pos = {root.id: (0, 0)}
        tree = add_edges(tree, root, pos)

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
        current = visit_order[step]
        plt.title(f"{title} — крок {step + 1}/{total}, вузол {current.val} ({current.color})")
        plt.pause(pause)
        plt.close()

    plt.ioff()
    draw_tree(root, f"{title} — фінальний результат")


if __name__ == "__main__":
    dfs_root = build_demo_tree()
    dfs_order = dfs_iterative(dfs_root)
    print("DFS (стек):", " -> ".join(str(node.val) for node in dfs_order))
    visualize_traversal(dfs_root, dfs_order, "DFS (обхід у глибину)")

    bfs_root = build_demo_tree()
    bfs_order = bfs_iterative(bfs_root)
    print("BFS (черга):", " -> ".join(str(node.val) for node in bfs_order))
    visualize_traversal(bfs_root, bfs_order, "BFS (обхід у ширину)")
