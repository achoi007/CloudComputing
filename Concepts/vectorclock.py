import unittest

class VectorClock(object):

    def __init__(self, numProc):
        self.ts = [[0] * numProc for i in xrange(numProc)]
        self.events = 0
        self.marks = {}

    def addStep(self, proc):
        self._inc(proc)
        self.events += 1

    def sendMesg(self, fromProc, toProc):
        self._inc(fromProc)
        fromTS = self.ts[fromProc]
        self.ts[toProc] = self._merge(fromTS, toProc)
        self.events += 2

    def halfSend(self, fromProc, mark):
        self._inc(fromProc)
        self.marks[mark] = list(self.ts[fromProc])
        self.events += 1

    def halfRecv(self, toProc, mark):
        fromTS = self.marks[mark]
        self.ts[toProc] = self._merge(fromTS, toProc)
        self.events += 1

    def clear(self):
        numProc = len(self.ts)
        self.ts = [[0] * numProc for i in xrange(numProc)]
        self.events = 0
        self.marks = {}

    def reportTS(self, proc=None):
        if proc == None:
            return self.ts
        else:
            return "ts[%d]=%s" % (proc, self.ts[proc])

    def _inc(self, proc):
        self.ts[proc][proc] += 1

    def _merge(self, fromTS, toProc):
        toTS = self.ts[toProc]
        # V_i[i] = V_i[i] + 1
        vp = toTS[toProc] + 1
        # V_i[j] = max(V_mesg[j], V_i[j]) for j != i
        toTS = [max(fromTS[i], toTS[i]) for i in xrange(len(fromTS))]
        toTS[toProc] = vp
        return toTS

    @staticmethod
    def lessEq(ts1, ts2):
        return all(ts1[i] <= ts2[i] for i in xrange(len(ts1)))

    @staticmethod
    def isCasuallyRelated(ts1, ts2):
        return VectorClock.lessEq(ts1, ts2) and any(ts1[i] < ts2[i] for i in xrange(len(ts1)))

    @staticmethod
    def isConcurrent(ts1, ts2):
        return not VectorClock.lessEq(ts1, ts2) and not VectorClock.lessEq(ts2, ts1)
    
class VectorClockTest(unittest.TestCase):

    def setUp(self):
        self.vclock = VectorClock(3)

    def testStep(self):
        vc = self.vclock
        vc.addStep(1)
        vc.addStep(2)
        vc.addStep(2)
        self.assertEquals(vc.ts[1][1], 1)
        self.assertEquals(vc.ts[2][2], 2)

    def testSendMesg(self):
        vc = self.vclock
        vc.addStep(0)
        vc.sendMesg(0, 1)
        self.assertEquals(vc.ts[0][0], 2)
        self.assertEquals(vc.ts[1][1], 1)
        self.assertEquals(vc.ts[1][0], 2)

    def testHalfSend(self):
        vc = self.vclock
        vc.halfSend(0, "m1")
        self.assertEquals(vc.ts[0][0], 1)

    def testHalfRecv(self):
        vc = self.vclock
        vc.halfSend(0, "m1")    # [1 0 0 0]
        vc.addStep(0)           # [2 0 0 0]
        vc.addStep(1)           # [0 1 0 0]
        vc.addStep(1)           # [0 2 0 0]
        vc.halfRecv(1, "m1")    # [1 3 0 0]
        self.assertEquals(vc.ts[1][0], 1)
        self.assertEquals(vc.ts[1][1], 3)

    def testLessEq(self):
        self.assertTrue(VectorClock.lessEq([3,4,5], [4,5,6]))
        self.assertTrue(VectorClock.lessEq([3,4,5], [3,4,5]))
        self.assertFalse(VectorClock.lessEq([3,4,5], [4,5,3]))

    def testCasuallyRelated(self):
        self.assertTrue(VectorClock.isCasuallyRelated([3,4,5], [3,4,6]))
        self.assertFalse(VectorClock.isCasuallyRelated([3,4,5], [3,4,5]))

    def testConcurrent(self):
        self.assertFalse(VectorClock.isConcurrent([3,4,5], [3,4,5]))
        self.assertFalse(VectorClock.isConcurrent([3,4,5], [3,4,6]))
        self.assertTrue(VectorClock.isConcurrent([3,4,5], [3,5,4]))
        

if __name__ == '__main__':
    unittest.main()
