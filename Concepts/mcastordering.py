from Queue import PriorityQueue
import unittest

class MCastOrdering(object):

    def __init__(self, numProcs, deliverCB):
        '''
        numProcs - number of processes
        deliverCB - deliverCB(fromProc, toProc, msg)
        '''
        pass

    def sendMcast(self, proc, msg):
        pass

    def recvMcast(self, proc, msg):
        pass


class BaseMCastOrdering(MCastOrdering):

    def __init__(self, numProcs, deliverCB, clock):
        self.numProcs = numProcs
        self.deliverCB = deliverCB
        self.clock = clock
        self.ts = []
        self.msg = {}
        self.buffer = {}

    def _sendMcast(self, proc, msg, ts):
        self.msg[msg] = [proc, ts]

    def _deliver(self, toProc, msg):
        (fromProc, ts) = self.msg[msg]
        self.deliverCB(fromProc, toProc, msg)

    def _buffer(self, fromProc, toProc, msg, priority):
        key = (fromProc, toProc)
        if key not in self.buffer:
            self.buffer[key] = PriorityQueue()
        queue = self.buffer[key]
        queue.put((priority, msg))

    def _deliverAllSequential(self, fromProc, toProc, nextPriority):
        # Deliver all messages in buffer with consecutive priorities starting at
        # nextPriority.  For example, if nextPriority=5, and queue has (5,6,7,10,11), deliver 5,6,7
        key = (fromProc, toProc)
        if key not in self.buffer:
            return
        queue = self.buffer[key]
        lastPriorityDelivered = None
        while not queue.empty():
            (msgPriority, msg) = queue.get()
            if msgPriority == nextPriority:
                self._deliver(toProc, msg)
                lastPriorityDelivered = msgPriority
                nextPriority += 1
            else:
                queue.put(msgPriority, msg)
                break
        return lastPriorityDelivered
            


class FIFOMCastOrdering(BaseMCastOrdering):

    def __init__(self, numProcs, deliverCB):
        BaseMCastOrdering.__init__(self, numProcs, deliverCB, None)
        # Each Pi maintains a vector of seq numbers Pi[1 .. N]
        # Pi[j] is latest seq num Pi has received from Pj
        self.seqNums = [range(numProcs) for i in xrange(numProcs)]

    def sendMcast(self, proc, msg):
        seqNums = self.seqNums[proc]
        seqNums[proc] += 1
        self._sendMcast(proc, msg, seqNums[proc])

    def recvMcast(self, toProc, msg):
        (fromProc, fromSeqNum) = self.msg[msg]
        seqNums = self.seqNums[toProc]
        if fromSeqNum == seqNums[fromProc] + 1:
            self._deliver(toProc, msg)
            seqNums[fromProc] = fromSeqNum
            lastPriorityDelivered = self._deliverAllSequential(fromProc, toProc, fromSeqNum + 1)
            if lastPriorityDelivered != None:
                seqNums[fromProc] = lastPriorityDelivered
        else:
            self._buffer(fromProc, toProc, msg, fromSeqNum)

class MCastOrderingTest(unittest.TestCase):

    def setUp(self):
        self.msgList = []
        deliverCB = lambda f,t,m: self.msgList.append((f,t,m))
        self.fifo = FIFOMCastOrdering(4, deliverCB)
        self.msgIdx = 0

    def checkMsg(self, fromProc, toProc, msg):
        self.assertEquals((fromProc, toProc, msg), self.msgList[self.msgIdx])
        self.msgIdx += 1

    def testFIFO(self):
        fifo = self.fifo
        # First mcast
        fifo.sendMcast(0, "m1")
        fifo.recvMcast(1, "m1")
        self.checkMsg(0, 1, "m1")
        fifo.recvMcast(3, "m1")
        self.checkMsg(0, 3, "m1")
        # Second mcast
        fifo.sendMcast(0, "m2")
        fifo.recvMcast(2, "m2") # buffered... waiting for m1
        fifo.recvMcast(2, "m1")
        self.checkMsg(0, 2, "m1")
        self.checkMsg(0, 2, "m2")
        fifo.recvMcast(1, "m2")
        self.checkMsg(0, 1, "m2")
        # Third mcast
        fifo.sendMcast(2, "m3")
        fifo.recvMcast(3, "m3") # No buffering
        fifo.recvMcast(3, "m2")
        self.checkMsg(2, 3, "m3")
        self.checkMsg(0, 3, "m2")
        fifo.recvMcast(0, "m3")
        fifo.recvMcast(1, "m3")
        self.checkMsg(2, 0, "m3")
        self.checkMsg(2, 1, "m3")

if __name__ == '__main__':
    unittest.main()
    


    
        
    

    
