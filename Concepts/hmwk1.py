from chord import Chord

def hash_func(x): return x

chord = Chord(hash_func, 8, [45, 32, 132, 234, 99, 199])
print "Successor of node 199 is", chord.successor(199)

node_list = []
chord = Chord(hash_func, 9, [1, 12, 123, 234, 345, 456, 501])
chord.query(234, 10, node_list)
print "234 => 10:", node_list
print chord._peers

node_list = []
chord = Chord(hash_func, 8, [45, 32, 132, 234, 99, 199])
chord.query(45, 12, node_list)
print "45 => 12:", node_list
print chord._peers

