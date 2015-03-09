from vectorclock import VectorClock
import unittest

class EventTrackVectorClock(VectorClock):

    FROM = ".From"
    TO = ".To"

    def __init__(self, numProc):
        VectorClock.__init__(self, numProc)
        self.clear()

    def clear(self):
        VectorClock.clear(self)
        self.events = 0
        self.eventTS = {}

    def addStep(self, proc, evtName=None):
        VectorClock.addStep(self, proc)
        self._recordEvt(evtName, proc)
        self.events += 1

    def sendMesg(self, fromProc, toProc, evtName=None):
        VectorClock.sendMesg(self, fromProc, toProc)
        if evtName != None:
            self._recordEvt(evtName + EventTrackVectorClock.FROM, fromProc)
            self._recordEvt(evtName + EventTrackVectorClock.TO, toProc)
        self.events += 2

    def halfSend(self, fromProc, mark):
        VectorClock.halfSend(self, fromProc, mark)
        self._recordEvt(mark + EventTrackVectorClock.FROM, fromProc)
        self.events += 1

    def halfRecv(self, toProc, mark):
        VectorClock.halfRecv(self, toProc, mark)
        self._recordEvt(mark + EventTrackVectorClock.TO, toProc)
        self.events += 1

    def getEventTS(self):
        return self.eventTS

    def getEventCount(self):
        return self.events

    def _recordEvt(self, evtName, proc):
        if evtName != None:
            self.eventTS[evtName] = list(self.getTS(proc))

class EventTrackVectorClockTest(unittest.TestCase):

    def setUp(self):
        self.vc = EventTrackVectorClock(3)

    def testEventCount(self):
        vc = self.vc
        vc.addStep(0)
        vc.addStep(1)
        vc.sendMesg(1, 2)
        vc.halfSend(2, "m1")
        self.assertEquals(1 + 1 + 2 + 1, vc.getEventCount())

    def testEventTS(self):
        vc = self.vc
        vc.addStep(0, "s1")
        vc.addStep(1, "s2")
        vc.sendMesg(1, 2, "m1")
        vc.halfSend(2, "m2")
        vc.halfRecv(0, "m2")
        eventTS = vc.getEventTS()
        self.assertEquals([1,0,0], eventTS["s1"])
        self.assertEquals([0,1,0], eventTS["s2"])
        self.assertEquals([0,2,0], eventTS["m1.From"])
        self.assertEquals([0,2,1], eventTS["m1.To"])
        self.assertEquals([0,2,2], eventTS["m2.From"])
        self.assertEquals([2,2,2], eventTS["m2.To"])

if __name__ == '__main__':
    unittest.main()
