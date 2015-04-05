import unittest

class MutualExclusion:
    
    def enter(self, process, callback):
        '''
        Try to enter mutual exclusion region.
        Callback will be called when access to mutual exclusion
        region is granted
        '''
        abstract
        
    def exit(self, process):
        '''
        Release mutual exclusion region access
        '''
        abstract

                
class CentralMasterMutex(MutualExclusion):
    
    def __init__(self):
        self.masterToken = 12345
        self.masterQueue = []
        self.token = {}
        
    def enter(self, process, callback):
        if self.masterToken != None:
            self.token[process] = self.masterToken
            self.masterToken = None
            callback()
        else:
            self.masterQueue.append((process, callback))
        
    def exit(self, process):
        self.masterToken = self.token[process]
        del self.token[process]
        if len(self.masterQueue) > 0:
            (nextProc, callback) = self.masterQueue.pop(0)
            self.enter(nextProc, callback)


class RingMutex(MutualExclusion):
    
    def __init__(self, processes):
        self.processes = processes
        self.ringIdx = 0
        self.wantRing = {}
        self.inMutex = False
    
    def passRing(self):
        # If currently in mutex, don't pass the ring.  Let exit() handle
        # ring passing
        if self.inMutex:
            return
        # Update ring index to next in ring
        self.ringIdx = (self.ringIdx + 1) % len(self.processes)
        # If next process does not want ring, done
        process = self.processes[self.ringIdx]
        if process not in self.wantRing:
            return
        # Give mutex to next process
        callback = self.wantRing[process]
        del self.wantRing[process]
        self.enter(process, callback)
        
    def enter(self, process, callback):
        if process == self.processes[self.ringIdx]:
            self.inMutex = True
            callback()
        else:
            self.wantRing[process] = callback
        
    def exit(self, process):
        self.inMutex = False
        self.passRing()
        
        
class RicartAgrawalaMutex(MutualExclusion):
    
    WANTED = 1
    HELD = 2
    RELEASED = 3
    
    def __init__(self, processes, clock):
        self.processes = processes
        self.state = dict((p, RicartAgrawalaMutex.RELEASED) for p in processes)
        self.queue = dict((p, []) for p in processes)
        self.replies = {}
        self.timestamps = {}
        self.clock = clock
        self.callbacks = {}
        
    def enter(self, process, callback):
        self.state[process] = RicartAgrawalaMutex.WANTED
        self.timestamps[process] = self._getLamportTimestamp(process)
        self.replies[process] = []
        self.callbacks[process] = callback
        self._multicast(process, self.timestamps[process])
        
    def exit(self, process):
        self.state[process] = RicartAgrawalaMutex.RELEASED
        queue = self.queue[process]
        self.queue[process] = []
        for queued in queue:
            self._sendReply(process, queued)
        
    def _getLamportTimestamp(self, process):
        return self.clock.getTimestamp(process)
        
    def _multicast(self, sender, timestamp):
        for receiver in filter(lambda p: p != sender, self.processes):
            state = self.state[receiver]
            delay = False
            # Delay if holding mutex
            if state == RicartAgrawalaMutex.HELD:
                delay = True
            # Delay if wanting access and earlier timestamp or same timestamp
            # but earlier process id
            if state == RicartAgrawalaMutex.WANTED and \
            (timestamp, sender) < (self.timestamps[receiver], receiver):
                delay = True
            # If delay, add to local queue
            if delay:
                self.queue[receiver].append(sender)
            else:
                self._sendReply(receiver, sender)
        
    def _waitForAllReplies(self, process, callback):
        if len(self.replies[process]) == len(self.processes) - 1:
            self.replies[process] = []
            self.state[process] = RicartAgrawalaMutex.HELD
            callback()
        
    def _sendReply(self, sender, receiver):
        self.replies[receiver].append(sender)
        self._waitForAllReplies(receiver, self.callbacks[receiver])
        
                          
class MutualExclusionTest(object):
    
    def createAlgo(self):
        abstract
        
    def doAsyncOps(self):
        pass
        
    def doEnter(self, process):
        self.algo.enter(process, self.createEnterCB(process))
        self.doAsyncOps()
        
    def doExit(self, process):
        self.algo.exit(process)
        self.doAsyncOps()
    
    def setUp(self):
        self.processes = [3, 32, 5, 80, 6, 12]
        self.algo = self.createAlgo()
        self.cbqueue = []
        
    def createEnterCB(self, proc):
        return lambda : self.cbqueue.append(proc)

    def testSimple(self):
        algo = self.algo
        for p in self.processes:
            self.doEnter(p)
            self.doExit(p)
            
    def testContention(self):
        algo = self.algo
        procs = self.processes
        # P0 enters CS
        self.doEnter(procs[0])
        self.assertEquals(procs[0], self.cbqueue.pop())
        # P1 tries to enter and is blocked
        self.doEnter(procs[1])
        self.assertEquals(0, len(self.cbqueue))
        # P0 exits CS
        self.doExit(procs[0])
        # P1 should have entered CS
        self.assertEquals(procs[1], self.cbqueue.pop())
        # P1 exits
        self.doExit(procs[1])
        

class CentralMasterMutexTest(unittest.TestCase, MutualExclusionTest):
    
    def createAlgo(self):
        return CentralMasterMutex()
        
    def setUp(self):
        MutualExclusionTest.setUp(self)

                
class RingMutexTest(unittest.TestCase, MutualExclusionTest):
    
    def createAlgo(self):
        return RingMutex(self.processes)
        
    def doAsyncOps(self):
        for i in xrange(len(self.processes)):
            self.algo.passRing()
        
    def setUp(self):
        MutualExclusionTest.setUp(self)

        
class RicartAgrawalaMutexTest(unittest.TestCase, MutualExclusionTest):
    
    def getTimestamp(self, process):
        return 1
    
    def createAlgo(self):
        return RicartAgrawalaMutex(self.processes, self)
        
    def setUp(self):
        MutualExclusionTest.setUp(self)        

if __name__ == '__main__':
    unittest.main()