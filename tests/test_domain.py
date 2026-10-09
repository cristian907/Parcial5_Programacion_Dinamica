"""Unit tests for domain entities and methods."""
import unittest
from src.domain.entities import Edge, Graph, Item, KnapsackProblem, Node
from src.domain.exceptions import NodeNotFoundError


class TestDomainEntities(unittest.TestCase):

    def test_graph_add_and_remove_nodes_edges(self):
        g = Graph("Test Graph")
        n1 = g.add_node(1, "Inicio", 0.0, 0.0)
        n2 = g.add_node(2, "Fin", 10.0, 10.0)

        self.assertEqual(len(g.nodes), 2)
        self.assertEqual(g.nodes[1].label, "Inicio")

        e = g.add_edge(1, 2, 50.0)
        self.assertEqual(len(g.edges), 1)
        self.assertEqual(e.weight, 50.0)

        sucs = g.get_successors(1)
        self.assertEqual(sucs, [(2, 50.0)])

        preds = g.get_predecessors(2)
        self.assertEqual(preds, [(1, 50.0)])

        # Remove edge
        removed_e = g.remove_edge(1, 2)
        self.assertTrue(removed_e)
        self.assertEqual(len(g.edges), 0)

        # Remove node
        removed_n = g.remove_node(1)
        self.assertTrue(removed_n)
        self.assertNotIn(1, g.nodes)

    def test_knapsack_problem_creation(self):
        kp = KnapsackProblem("Mochila", capacity=10.0)
        kp.add_item(1, "Prod A", 2.0, 40.0)
        kp.add_item(2, "Prod B", 3.0, 50.0)

        self.assertEqual(len(kp.items), 2)
        self.assertEqual(kp.items[0].value_per_weight, 20.0)

        kp.remove_item(1)
        self.assertEqual(len(kp.items), 1)
        self.assertEqual(kp.items[0].id, 2)


if __name__ == "__main__":
    unittest.main()
