from vectorclock import VectorClock
from chandylamport import ChandyLamport

def hmwk():
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
    print "Ready?", cl.isGlobalStateReady()

    (states,channels) = cl.getGlobalState()
    for ch in channels:
        channel = channels[ch]
        if len(channel) > 0:
            print ch, channel

if __name__ == '__main__':
    hmwk()
    
    
    
