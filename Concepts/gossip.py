import random
from pygraph.classes.graph import graph
import unittest

class Gossip:

    INFECTED = 'infected'

    def __init__(self, graph):
        self._graph = graph
        self._infected = set()

    def is_all_infected(self):
        return len(self._infected) == len(self._graph)

    def get_uninfected(self):
        return [n for n in self._graph.nodes() if n not in self._infected]

    def get_infected(self):
        return self._infected

    def push(self, b):
        g = self._graph
        # To be infected
        new_infected = set()
        # For each infected node, pick b random neighbors to be infected
        for infected in self._infected:
            for neighbor in self._random_neighbors(infected, b):
                new_infected.add(neighbor)
        # Infect all nodes at once
        for infected in new_infected:
            self.infect(infected)

    def pull(self, b):
        g = self._graph
        # To be infected
        new_infected = []
        # For each uninfected node, pick b random neighbors.  If any
        # of b random neighbor is infected, then node becomes infected
        # as well
        for uninfected in self.get_uninfected():
            for neighbor in self._random_neighbors(uninfected, b):
                if neighbor in self._infected:
                    new_infected.append(uninfected)
                    break
        # Infect all nodes at once
        for infected in new_infected:
            self.infect(infected)
        

    def infect(self, node):
        if node not in self._infected:
            self._graph.node_attributes(node).append(Gossip.INFECTED)
            self._infected.add(node)            

    def cure(self, node):
        if node in self._infected:
            self._graph.node_attributes(node).remove(Gossip.INFECTED)
            self._infected.remove(node)

    def _random_neighbors(self, node, b):
        neighbors = self._graph.neighbors(node)
        if b >= len(neighbors):
            return neighbors
        else:
            return random.sample(neighbors, b)

class GossipTest(unittest.TestCase):

    def setUp(self):
        # big graph
        g = graph()
        g.add_nodes(xrange(5))
        g.complete()
        self.graph = g
        self.gossip = Gossip(g)
        # small graph
        g = graph()
        g.add_nodes(xrange(5))
        g.add_edge((0, 1))
        g.add_edge((0, 2))
        g.add_edge((0, 3))
        g.add_edge((0, 4))
        self.small_graph = g
        self.small_gossip = Gossip(g)

    def test_infect_cure(self):
        g = self.gossip
        n = len(self.graph)
        # All uninfected
        self.assertFalse(g.is_all_infected())
        self.assertEquals(len(g.get_infected()), 0)
        self.assertEquals(len(g.get_uninfected()), n)
        # Infect every node
        for i in range(n):
            g.infect(i)
        self.assertTrue(g.is_all_infected())
        self.assertEquals(len(g.get_infected()), n)
        self.assertEquals(len(g.get_uninfected()), 0)
        # Cure first node
        g.cure(0)
        self.assertFalse(g.is_all_infected())
        self.assertEquals(len(g.get_infected()), n - 1)
        self.assertEquals(len(g.get_uninfected()), 1)

    def test_push_big_graph(self):
        g = self.gossip
        n = len(self.graph)
        # Push n nodes but no node is infected
        g.push(n)
        self.assertEquals(len(g.get_infected()), 0)
        self.assertEquals(len(g.get_uninfected()), n)
        # Infect 1 node and push n nodes.  Should infect all nodes
        g.infect(0)
        g.push(n)
        self.assertTrue(g.is_all_infected())

    def test_push_small_graph(self):
        g = self.small_gossip
        gr = self.small_graph
        g.infect(0)
        g.push(1)
        # 0 and 1 other node infected
        self.assertEquals(len(g.get_infected()), 2)

    def test_pull(self):
        g = self.small_gossip
        n = len(self.small_graph)
        # No node is infected
        g.pull(n)
        self.assertFalse(g.is_all_infected())
        # Infecting node 2
        g.infect(2)
        # Pull should now infect node 0 also
        g.pull(n)
        self.assertIn(0, g.get_infected())
        self.assertIn(2, g.get_infected())
        self.assertFalse(g.is_all_infected())        
        # Pull again will now infect all nodes
        g.pull(n)
        self.assertTrue(g.is_all_infected())

if __name__ == '__main__':
    unittest.main()
    
    
        
