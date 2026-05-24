import heapq
from math import inf


class Graph:
    def __init__(self):
        self.adjacency: dict[str, list[tuple[str, float]]] = {}

    def add_vertex(self, vertex: str) -> None:
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []

    def add_edge(self, from_vertex: str, to_vertex: str, weight: float) -> None:
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        self.adjacency[from_vertex].append((to_vertex, weight))

    def get_vertices(self) -> list[str]:
        return list(self.adjacency.keys())


def dijkstra(graph: Graph, start: str) -> dict[str, float]:
    """Алгоритм Дейкстри з бінарною купою (heapq)."""
    if start not in graph.adjacency:
        raise ValueError(f"Вершина '{start}' відсутня в графі")

    distances = {vertex: inf for vertex in graph.get_vertices()}
    distances[start] = 0

    # мін-купа: (відстань, вершина)
    heap: list[tuple[float, str]] = [(0, start)]

    while heap:
        current_distance, current_vertex = heapq.heappop(heap)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph.adjacency[current_vertex]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(heap, (new_distance, neighbor))

    return distances


def build_demo_graph() -> Graph:
    graph = Graph()

    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
    ]

    for from_vertex, to_vertex, weight in edges:
        graph.add_edge(from_vertex, to_vertex, weight)

    return graph


if __name__ == "__main__":
    graph = build_demo_graph()
    start = "A"

    print(f"Граф (орієнтований, зважений):")
    for vertex in sorted(graph.get_vertices()):
        neighbors = ", ".join(f"{n}({w})" for n, w in graph.adjacency[vertex])
        print(f"  {vertex} -> {neighbors}")

    print(f"\nНайкоротші шляхи від вершини '{start}':")
    shortest_paths = dijkstra(graph, start)

    for vertex in sorted(shortest_paths):
        distance = shortest_paths[vertex]
        if distance is inf:
            print(f"  {start} -> {vertex}: недосяжна")
        else:
            print(f"  {start} -> {vertex}: {distance}")
