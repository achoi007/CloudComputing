from vectorclock import VectorClock
import unittest

class ChandyLamport(object):

    def __init__(self, vclock):
        self.vclock = vclock
        self.clear()

    def clear(self):
        self.state = {}
        self.recording = {}
        self.channels = {}
        self.sendFrom = {}

    def getGlobalState(self):
        return (self.state, self.channels)

    def isGlobalStateReady(self):
        n = self.vclock.getNumProcs()
        return len(self.state) == n and len(self.channels) == n*n - n

    def initMarker(self, i):
        '''
        Process Pi initiates global snapshot
        '''
        # Pi records its own state
        self._recordState(i)
        # Starts recording incoming messages for channels Cji for Pi
        for p in self._allProcsExcept(i):
            self._startRecording(p, i)
        # Pi sends out marker message on outgoing channels Cij
        for p in self._allProcsExcept(i):
            self._sendMarker(i, p)            

    def recvMarker(self, k, i):
        '''
        Process Pi receives marker message on channel Cki
        '''
        channel = (k, i)        
        if i in self.state:
            # Already seen marker message
            self.channels[channel] = list(self.recording[channel])
        else:
            # First time marker is seen
            self._recordState(i)
            self.channels[channel] = []
            for p in self._allProcsExcept(i):
                self._startRecording(p, i)
            for p in self._allProcsExcept(i):
                self._sendMarker(i, p)

    def halfSend(self, fromProc, mark):
        self.vclock.halfSend(fromProc, mark)
        self.sendFrom[mark] = fromProc

    def halfRecv(self, toProc, mark):
        self.vclock.halfRecv(toProc, mark)
        fromProc = self.sendFrom[mark]
        channel = (fromProc, toProc)
        if channel in self.recording:
            self.recording[channel].append(mark)

    def _sendMarker(self, i, j):
        pass

    def _recordState(self, i):
        self.state[i] = list(self.vclock.getTS(i))

    def _startRecording(self, i, j):
        self.recording[(i, j)] = []

    def _allProcsExcept(self, proc):
        return filter(lambda p: p != proc, xrange(self.vclock.getNumProcs()))

class ChandyLamportTest(unittest.TestCase):

    def setUp(self):
        self.vclock = VectorClock(3)
        self.cl = ChandyLamport(self.vclock)
        vc = self.vclock
        for i in xrange(self.vclock.getNumProcs()):
            for j in xrange(i+1):
                vc.addStep(i)  # Pi => (i+1,0,0)        

    def testNotRecording(self):
        vc = VectorClock(3)
        cl = ChandyLamport(vc)
        cl.halfSend(0, "m1")
        cl.halfRecv(1, "m1")
        self.assertEquals([1,0,0], vc.getTS(0))
        self.assertEquals([1,1,0], vc.getTS(1))
        self.assertEquals([0,0,0], vc.getTS(2))

    def testSimpleEmptyChannels(self):
        cl = self.cl
        vc = self.vclock
        n = vc.getNumProcs()
        # P0 starts global snapshot process
        cl.initMarker(0)
        cl.recvMarker(0, 1)
        self.assertFalse(cl.isGlobalStateReady())
        cl.recvMarker(0, 2)
        vc.addStep(0)
        self.assertFalse(cl.isGlobalStateReady())
        cl.recvMarker(1, 0)
        vc.addStep(1)
        self.assertFalse(cl.isGlobalStateReady())
        cl.recvMarker(1, 2)
        self.assertFalse(cl.isGlobalStateReady())
        vc.addStep(2)
        cl.recvMarker(2, 0)
        self.assertFalse(cl.isGlobalStateReady())
        cl.recvMarker(2, 1)
        # After all markers are received, check global state capture
        self.assertTrue(cl.isGlobalStateReady())
        # Check states
        (state,channels) = cl.getGlobalState()
        self.assertEquals([1,0,0], state[0])
        self.assertEquals([0,2,0], state[1])
        self.assertEquals([0,0,3], state[2])
        # Check channels
        for i in xrange(n):
            for j in xrange(n):
                if i != j:
                    ch = (i, j)
                    self.assertIn(ch, channels)
                    self.assertEquals([], channels[ch])
        
    def testNonEmptyChannels(self):
        cl = self.cl
        vc = self.vclock
        n = vc.getNumProcs()
        # P0 starts global snapshot process
        cl.initMarker(0)
        cl.halfSend(1, "m1")
        cl.halfSend(1, "m2")
        cl.recvMarker(0, 1)
        cl.halfRecv(0, "m1")
        cl.halfRecv(0, "m2")
        cl.recvMarker(0, 2)
        cl.recvMarker(1, 0)
        cl.halfSend(1, "m3")
        cl.halfRecv(0, "m3")
        cl.recvMarker(1, 2)
        cl.halfSend(2, "m4")
        cl.halfRecv(1, "m4")
        cl.recvMarker(2, 0)
        cl.recvMarker(2, 1)
        cl.halfSend(2, "m5")
        cl.halfRecv(0, "m5")
        self.assertTrue(cl.isGlobalStateReady())
        # Check channels
        (states,channels) = cl.getGlobalState()
        self.assertEquals(["m1", "m2"], channels[(1,0)])
        self.assertEquals(["m4"], channels[(2,1)])

if __name__ == '__main__':
    unittest.main()
