import unittest
import bisect

class Chord(object):

    def __init__(self, hash_func, m, addresses):
        self.m = m
        self.hash_func = hash_func
        # Calculate peer ring
        self._peers = [self._compute_peer_id(addr) for addr in addresses]
        self._peers.sort()
        # Calculate finger table for each peer
        finger_tbl = {}
        for peer in self._peers:
            tbl = self._compute_finger_table(peer)
            finger_tbl[peer] = tbl
        self._finger_tbl = finger_tbl

    def _compute_peer_id(self, address):
        # Perform consistent hash on node's peer address (IP + port)
        return self.hash_func(address) % (2 ** self.m)
        
    def _compute_finger_table(self, peer):
        # i-th entry at peer with id n is first peer with
        # id >= (n + 2^i) % 2^m
        m = 2 ** (self.m)
        return [self.find_next_larger((peer + 2 ** i) % m) for i in xrange(self.m)]

    def find_next_larger(self, peer):
        for p in self._peers:
            if p >= peer:
                return p
        return self._peers[0]

    def query(self, node, key, node_list = None):
        # Hash the key
        key = self.hash_func(key)
        # Find node which has the key
        pos = bisect.bisect(self._peers, key)
        if pos < len(self._peers):
            key_at_node = self._peers[pos]
        else:
            key_at_node = self._peers[0]
        # See if path to find node is needed.  If so, compute it
        if node_list != None:
            self._compute_search_path(node, key_at_node, node_list)
        return key_at_node

    def _compute_search_path(self, start_node, final_node, node_list):
        # If start node is final node, done
        if final_node == start_node:
            node_list.append(start_node)
            return
        finger_tbl = self._finger_tbl[start_node]
        fingers = filter(lambda i: i <= final_node, finger_tbl)
        if len(fingers) > 0:
            new_start_node = max(fingers)
        else:
            new_start_node = finger_tbl[-1]
        node_list.append(start_node)
        self._compute_search_path(new_start_node, final_node, node_list)

    def _query_helper(self, node, key, node_list):
        '''
        At node n, query for key.
        Find largest successor/finger entry <= k.  If none exists, send query to successor(n)
        '''
        # Done if node has key
        if self.contains(node, key):
            return node
        # Find largest finger entry <= key
        fingers = [f for f in self._finger_tbl[node] if f <= key]
        # If none exists, send query to successor
        if len(fingers) == 0:
            next_node = self.successor(node)
        # otherwise, send query to largest finger entry <= key
        else:
            next_node = max(fingers)
        node_list.append(next_node)
        return self._query_helper(next_node, key, node_list)

    def contains(self, node, key):
        if key == node:
            return True
        # Find out where key is 
        pos = bisect.bisect(self._peers, key)
        # If position is before the last peer, check if next node after position is
        # current node.
        if pos < len(self._peers):
            return self._peers[pos] == node
        # If position is after the last peer, the first peer is the node which contains key
        return self._peers[0] == node
        

    def successor(self, node):
        peers = self._peers
        for i in xrange(len(peers) - 1):
            if peers[i] == node:
                return peers[i+1]
        return peers[0]
        

class ChordTest(unittest.TestCase):

    def setUp(self):
        self.chord = Chord(lambda x: x, 7, [32, 45, 80, 96, 112, 128 + 16])

    def test_peers(self):
        self.assertEquals([16, 32, 45, 80, 96, 112], self.chord._peers)

    def test_finger_tbl(self):
        tbl = self.chord._finger_tbl[80]
        self.assertEquals(tbl, [96, 96, 96, 96, 96, 112, 16])

    def test_successor(self):
        ch = self.chord
        self.assertEquals(45, ch.successor(32))
        self.assertEquals(80, ch.successor(45))
        self.assertEquals(96, ch.successor(80))
        self.assertEquals(16, ch.successor(112))
        
    def test_query(self):
        ch = self.chord
        self.assertEquals(45, ch.query(80, 42))
        node_list = []
        ch.query(80, 42, node_list)
        self.assertEquals([80, 16, 32, 45], node_list)

if __name__ == '__main__':
    unittest.main()
    
        
        
        

 
