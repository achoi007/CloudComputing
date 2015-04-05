import unittest

class VotingSet:
    
    def __init__(self, processes, numVotingSets, numSetsPerProcess):
        self.processes = processes
        self._split(numVotingSets, numSetsPerProcess)
        
    def getVotingSet(self, process):
        return self.procToVoteSets[process]
        
    def getProcessesInSet(self, setNum):
        return self.voteSets[setNum]
        
    def getProcessCountInSet(self, process):
        return len(self.getProcessesInSameSet(process))
        
    def getProcessesInSameSet(self, process):
        return self.voteSets[self.getVotingSet(process)]
        
    def _split(self, numVotingSets, numSetsPerProcess):
        voteSets = [set() for i in xrange(numVotingSets)]
        procToVoteSets = {}
        for (i, p) in enumerate(self.processes):
            setNum = i % numVotingSets
            voteSets[setNum].add(p)
            procToVoteSets[p] = setNum
        self.voteSets = voteSets
        self.procToVoteSets = procToVoteSets
        
class VotingSetTest(unittest.TestCase):
    
    def testPerfect(self):
        vs = VotingSet(range(30), 3, 10)
        for i in xrange(3):
            self.assertEquals(10, len(vs.getProcessesInSet(i)))
        for i in xrange(30):
            self.assertEquals(i % 3, vs.getVotingSet(i))
            
    def testImperfect(self):
        vs = VotingSet(range(27), 3, 10)
        for i in xrange(3):
            self.assertEquals(9, len(vs.getProcessesInSet(i)))
        for i in xrange(27):
            self.assertEquals(i % 3, vs.getVotingSet(i))        
        
if __name__ == '__main__':
    unittest.main()

    
        