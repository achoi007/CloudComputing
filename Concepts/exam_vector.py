from lamport import LamportTimestamp
from vectorclock import VectorClock

def exam_vector(ts):
    ts.sendMesg(4, 3, "m9")
    ts.halfSend(1, "m1")
    ts.halfSend(3, "m8")
    ts.halfSend(4, "m10")
    ts.halfSend(1, "m2")
    ts.halfRecv(2, "m8")
    ts.halfRecv(3, "m1")
    ts.sendMesg(1, 4, "m3")
    ts.halfSend(2, "m6")
    ts.sendMesg(2, 1, "m7")
    ts.sendMesg(1, 3, "m4")
    ts.halfRecv(3, "m6")
    ts.halfSend(1, "m5")
    ts.sendMesg(4, 3, "m11")
    ts.halfRecv(3, "m5")
    ts.halfRecv(2, "m10")
    ts.halfRecv(2, "m2")
    

if __name__ == '__main__':
    ts = VectorClock(5)
    exam_vector(ts)
    
    

    
    
