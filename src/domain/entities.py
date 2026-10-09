"""Domain entities and value objects."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Node:
    """Represents a node in a graph."""
    id: int
    label: str
    x: float = 0.0
    y: float = 0.0

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(frozen=True)
class Edge:
    """Represents a directed weighted edge between two nodes."""
    source: int
    target: int
    weight: float

    def __hash__(self) -> int:
        return hash((self.source, self.target, self.weight))


@dataclass
class Graph:
    """Domain entity representing a directed weighted graph."""
    name: str = "Grafo de Programación Dinámica"
    nodes: Dict[int, Node] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)

    def add_node(self, node_id: int, label: Optional[str] = None, x: float = 0.0, y: float = 0.0) -> Node:
        lbl = label if label else f"Nodo {node_id}"
        node = Node(id=node_id, label=lbl, x=x, y=y)
        self.nodes[node_id] = node
        return node

    def add_edge(self, source: int, target: int, weight: float) -> Edge:
        if source not in self.nodes:
            self.add_node(source)
        if target not in self.nodes:
            self.add_node(target)
        edge = Edge(source=source, target=target, weight=weight)
        # Avoid exact duplicates
        self.edges = [e for e in self.edges if not (e.source == source and e.target == target)]
        self.edges.append(edge)
        return edge

    def remove_edge(self, source: int, target: int) -> bool:
        prev_len = len(self.edges)
        self.edges = [e for e in self.edges if not (e.source == source and e.target == target)]
        return len(self.edges) < prev_len

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.edges = [e for e in self.edges if e.source != node_id and e.target != node_id]
            return True
        return False

    def get_successors(self, node_id: int) -> List[Tuple[int, float]]:
        """Returns list of (target_node_id, weight) outgoing from node_id."""
        return [(e.target, e.weight) for e in self.edges if e.source == node_id]

    def get_predecessors(self, node_id: int) -> List[Tuple[int, float]]:
        """Returns list of (source_node_id, weight) incoming to node_id."""
        return [(e.source, e.weight) for e in self.edges if e.target == node_id]

    def get_node_ids(self) -> List[int]:
        return sorted(list(self.nodes.keys()))

    def clone(self) -> "Graph":
        g = Graph(name=self.name)
        for nid, n in self.nodes.items():
            g.add_node(nid, n.label, n.x, n.y)
        for e in self.edges:
            g.add_edge(e.source, e.target, e.weight)
        return g


@dataclass(frozen=True)
class Item:
    """Represents a product/item for the Cargo Volume (Knapsack) problem."""
    id: int
    name: str
    weight: float
    price: float

    @property
    def value_per_weight(self) -> float:
        return self.price / self.weight if self.weight > 0 else 0.0


@dataclass
class KnapsackProblem:
    """Represents the Cargo Volume problem formulation."""
    name: str
    capacity: float
    items: List[Item] = field(default_factory=list)
    allow_repetition: bool = False

    def add_item(self, item_id: int, name: str, weight: float, price: float) -> Item:
        item = Item(id=item_id, name=name, weight=weight, price=price)
        self.items = [it for it in self.items if it.id != item_id]
        self.items.append(item)
        return item

    def remove_item(self, item_id: int) -> bool:
        prev_len = len(self.items)
        self.items = [it for it in self.items if it.id != item_id]
        return len(self.items) < prev_len


@dataclass(frozen=True)
class TrueFalseQuestion:
    """Represents a theoretical True/False exam question."""
    id: str
    statement: str
    correct_answer: bool
    justification: str
