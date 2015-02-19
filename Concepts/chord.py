import unittest

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

    def query(self, node, key, node_list = None, is_hash = False):
        '''
        At node n, query for key.
        Find largest successor/finger entry <= k.  If none exists, send query to successor(n)
        '''
        if not is_hash:
            key = self.hash_func(key)
        finger_tbl = self._finger_tbl[node]
        found = None
        for pos in reversed(range(len(finger_tbl))):
            entry = finger_tbl[pos]
            if entry <= key:
                found = entry
                break
        if found is None:
            s = self.successor(node)
            if node_list != None:
                node_list.append(s)
            return s
        else:
            if node_list != None:
                node_list.append(found)
            return self.query(found, key, node_list, True)

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
        self.assertEquals([16, 32, 45], node_list)

if __name__ == '__main__':
    unittest.main()
    
        
        
        

 
