from vectorclock import VectorClock

class ChandyLamport(VectorClock):

    def __init__(self):
        clear()

    def initMarker(self, proc):
        pass

    def sendMesg(self, fromProc, toProc):
        if self.inMarking:
            pass
        pass

    def halfSend(self, proc, mark):
        if self.inMarking:
            pass
        pass

    def halfRecv(self, proc, mark):
        if self.inMarking:
            pass
        pass

    def isGlobalStateReady(self):
        pass

    def getGlobalState(self):
        pass

    def clear(self):
        self.inMarking = False

    

    


            
        
        
               
        
