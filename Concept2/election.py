import unittest

class Election:
    
    def __init__(self, processes):
        abstract
        
    def initElection(self, process):
        abstract
        
    def getElectedLeader(self):
        abstract
        
    def getMsgCnt(self):
        abstract
        
    def updateProcesses(self, processes):
        abstract
        
    def getProcesses(self):
        abstract
        
    def killProcess(self, proccess):
        abstract
    

class RingElection(Election):
    
    def __init__(self, processes):
        self.processes = processes
        self.leader = None
        
    def initElection(self, process):
        i = self._findPos(process)
        self.msgCnt = 0
        self.forwarded = [False] * len(self.processes)
        self.elected = [None] * len(self.processes)
        self._sendElectionMsg(self._getNext(i), process)
        
    def getElectedLeader(self):
        return self.leader
        
    def getMsgCnt(self):
        return self.msgCnt
        
    def updateProcesses(self, processes):
        self.processes = processes
        
    def getProcesses(self):
        return self.processes
        
    def killProcess(self, process):
        self.processes.remove(process)
        
    def _sendElectionMsg(self, idx, leader):
        self.msgCnt += 1
        proc = self.processes[idx]
        if leader > proc:
            self.forwarded[idx] = True
            self._sendElectionMsg(self._getNext(idx), leader)
        elif leader < proc and not self.forwarded[idx]:
            self.forwarded[idx] = True
            self._sendElectionMsg(self._getNext(idx), proc)
        elif leader == proc:
            self.leader = proc
            self._sendElected(self._getNext(idx), proc)

    def _sendElected(self, idx, leader):
        self.msgCnt += 1
        proc = self.processes[idx]
        if leader != proc:
            self.elected[idx] = leader
            self._sendElected(self._getNext(idx), leader)
    
    def _findPos(self, process):
        return self.processes.index(process)        
        
    def _getNext(self, i):
        return (i + 1) % len(self.processes)
        
        
class BullyElection(Election):
    
    def __init__(self, processes):
        self.updateProcesses(processes)
        self.leader = None
        self.timeout = 10
        self.knownLeader = {}         
        
    def initElection(self, process):
        # Initialize to empty
        self.msgCnt = 0
        self.knownLeader = {}
        self.electionReply = {}
        self.electionInited = set()
        # Initialize election WITHOUT clearing out all fields
        self._subInitElection(process)
        
    def getElectedLeader(self):
        return self.leader
        
    def getMsgCnt(self):
        return self.msgCnt
        
    def updateProcesses(self, processes):
        higherIds = {}
        for p in processes:
            higherIds[p] = [i for i in processes if i > p]
        self.higherIds = higherIds 
        self.alive = set(processes)
        
    def getProcesses(self):
        return list(self.higherIds)
        
    def killProcess(self, process):
        self.alive.remove(process)
        
    def _subInitElection(self, process):
        
        # Skip if election has already been initiated once
        if process in self.electionInited:
            return
        self.electionInited.add(process)
        
        # If process has highest id, elect itself as leader
        if len(self.higherIds[process]) == 0:
            self._selfElect(process)
            return
            
        # Send election message to all higher id processes
        higherIds = self.higherIds[process]
        for id in higherIds:
            self._recvElectionMsg(id, process)
            
        # Wait for election reply.  If none, elect itself as leader
        if not self._waitElectionReply(process, self.timeout):
            self._selfElect(process)
            return
        
        # Wait for coordinator message.  If none, start election process again
        if not self._waitCoordinatorMsg(process, self.timeout):
            self.initElection(process)        
            
        
    def _selfElect(self, process):
        # Choose itself as the leader
        self.leader = process
        self.knownLeader[process] = process
        
        # Notify all lower id processes the new leader
        lowerIds = filter(lambda i: i < process, self.getProcesses())
        for id in lowerIds:
            self._recvCoordinatorMsg(id, process)        
        
    def _recvElectionMsg(self, id, sender):
        if id not in self.alive:
            return
        # Reply election message with OK
        self._recvElectionReply(sender, "OK")
        # Start its own leader election protocol
        self._subInitElection(id)
        
    def _waitElectionReply(self, process, timeout):
        return process in self.electionReply and self.electionReply[process] == "OK"
        
    def _recvElectionReply(self, process, status):
        self.electionReply[process] = status
        
    def _recvCoordinatorMsg(self, id, leader):
        # Notify process id that leader has been elected
        self.knownLeader[id] = leader
        
    def _waitCoordinatorMsg(self, id, timeout):
        return id in self.knownLeader
        
class ElectionTest(object):
    
    def createAlgo(self):
        return None
        
    def setUp(self):
        self.algo = self.createAlgo()
        
    def testElection(self):
        algo = self.algo
        procs = algo.getProcesses()
        for p in procs:
            algo.initElection(p)
            leader = algo.getElectedLeader()
            self.assertIn(leader, procs)
            self.assertTrue(algo.getMsgCnt() > 0)
            
class RingElectionTest(unittest.TestCase, ElectionTest):
    
    def createAlgo(self):
        processes = [3, 32, 5, 80, 6, 12]
        return RingElection(processes)
            
    def setUp(self):
        ElectionTest.setUp(self)
        
    def testCorrectElection(self):
        algo = self.algo
        algo.initElection(3)
        self.assertEqual(80, algo.getElectedLeader())
        algo.initElection(80)
        self.assertEqual(80, algo.getElectedLeader())
        self.assertEqual(2 * len(algo.getProcesses()), algo.getMsgCnt())
        
class BullyElectionTest(unittest.TestCase, ElectionTest):
    
    def createAlgo(self):
        processes = [3, 32, 5, 80, 6, 12]
        return RingElection(processes)        
        
    def setUp(self):
        ElectionTest.setUp(self)
        
    def testCorrectElection(self):
        algo = self.algo
        algo.killProcess(80)
        algo.initElection(6)
        self.assertEquals(32, algo.getElectedLeader())
        
if __name__ == "__main__":
    unittest.main()
    