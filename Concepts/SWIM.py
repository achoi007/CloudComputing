import unittest
import random
from pygraph.classes.graph import graph

class SWIM(object):

    def __init__(self, graph):
        self.graph = graph

    def edge_alive(self, nodeA, nodeB, alive):
        '''
        edge_alive(A, B, True|False)
        '''
        edge = (nodeA, nodeB)
        if alive:
            self.graph.add_edge(edge)
        else:
            self.graph.del_edge(edge)

    def node_alive(self, node, alive):
        '''
        node_alive(A, True|False)
        '''
        if alive:
            self.graph.node_attributes(node).clear()
        else:
            self.graph.node_attributes(node).append("dead")

    def ping(self, nodeStart, nodeEnd, k):
        '''
        NodeStart to ping NodeEnd directly or indirectly through
        K random neighbors.  Return True if nodeEnd receives ping,
        or False otherwise
        '''
        g = self.graph
        # Check if direct ping works        
        if g.has_edge((nodeStart, nodeEnd)) and \
           "dead" not in g.node_attributes(nodeEnd):
            return True
        # Pick k random neighbors and let them ping end node
        for neighbor in self._random_neighbors(nodeStart, k):
            if self.ping(neighbor, nodeEnd, 0):
                return True
        # All pings have failed
        return False

    def _random_neighbors(self, node, b):
        neighbors = self.graph.neighbors(node)
        if len(neighbors) <= b:
            return neighbors
        else:
            return random.sample(neighbors, b)

class SWIMTest(unittest.TestCase):

    def setUp(self):
        g = graph()
        g.add_nodes(xrange(10))
        g.complete()
        self.graph = g
        self.swim = SWIM(g)

    def test_good_ping(self):
        swim = self.swim
        self.assertTrue(swim.ping(0, 1, 0))
        self.assertTrue(swim.ping(1, 3, 0))

    def test_dead_edge_ping(self):
        swim = self.swim
        swim.edge_alive(0, 1, False)
        self.assertFalse(swim.ping(0, 1, 0))
        self.assertTrue(swim.ping(0, 1, 1))
        
    def test_dead_node_ping(self):
        swim = self.swim
        swim.node_alive(2, False)
        self.assertFalse(swim.ping(0, 2, 0))
        self.assertFalse(swim.ping(0, 2, 3))

if __name__ == '__main__':
    unittest.main()

    

    
