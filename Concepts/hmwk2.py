from evttrkvecclock import EventTrackVectorClock
from vectorclock import VectorClock
from chandylamport import ChandyLamport

def vecClockSetUp1():
    vc = EventTrackVectorClock(4)
    vc.halfSend(0, "m1")
    vc.addStep(1, "p1_1")
    vc.halfRecv(2, "m1")
    vc.sendMesg(1, 0, "m3")
    vc.sendMesg(2, 1, "m2")
    vc.addStep(3, "p3_1")
    vc.halfSend(1, "m4")
    vc.halfSend(2, "m6")
    vc.sendMesg(1, 0, "m5")
    vc.addStep(1, "p1_2")
    vc.addStep(2, "p2_1")
    vc.addStep(0, "p0_1")
    vc.sendMesg(0, 2, "m8")
    vc.sendMesg(1, 3, "m7")
    vc.halfRecv(3, "m6")
    vc.sendMesg(2, 3, "m9")
    vc.halfRecv(2, "m4")
    vc.sendMesg(3, 2, "m10")
    return vc
    
def vecClockQuestions():
    vc = vecClockSetUp1()
    # Question 18
    print "Q18 - Ending vec timestamp of P1", vc.getTS(1)
    # Question 19
    print "Q19 - vec timestamp of p2_1", vc.eventTS["p2_1"]
    # Question 20
    print "Q20 - receipt timestamp of m4", vc.eventTS["m4.From"], \
          vc.eventTS["m4.To"]
    # Question 21
    print "Q21 - receipt timestamp of m10", vc.eventTS["m10.From"], \
          vc.eventTS["m10.To"]
    # Question 22
    evtTS = vc.eventTS["m4.From"]
    concurrent = filter(lambda e: VectorClock.isConcurrent(evtTS, vc.eventTS[e]),
                        vc.eventTS)
    print "Q22 - Number of concurrent events to m4.From", concurrent, len(concurrent)
    print evtTS, map(lambda e: vc.eventTS[e], concurrent)

def chandyLamportQuestions():
    vc = VectorClock(3)
    cl = ChandyLamport(vc)
    cl.halfSend(0, "a")
    cl.halfSend(2, "d")
    cl.halfRecv(1, "d")
    cl.initMarker(2)
    cl.halfSend(0, "f")
    cl.recvMarker(2, 0)
    cl.halfSend(1, "b")
    cl.halfSend(1, "e")
    cl.recvMarker(2, 1)
    cl.halfRecv(0, "b")
    cl.halfRecv(2, "e")
    cl.recvMarker(1, 2)
    cl.halfSend(0, "c")
    cl.recvMarker(1, 0)
    cl.halfRecv(2, "f")
    cl.recvMarker(0, 2)
    cl.recvMarker(0, 1)
    cl.halfRecv(2, "c")
    
if __name__ == '__main__':
    vecClockQuestions()
    chandyLamportQuestions()
    
    
    
    
