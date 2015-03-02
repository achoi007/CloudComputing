class LamportTimestamp(object):

    def __init__(self, numProc):
        self.ts = [0] * numProc
        self.events = 0        
        self.marks = {}

    def addStep(self, proc):
        self.ts[proc] += 1
        self.events += 1

    def sendMesg(self, fromProc, toProc):
        fromTS = self.ts[fromProc] + 1
        self.ts[fromProc] = fromTS
        toTS = max(self.ts[toProc], fromTS) + 1
        self.ts[toProc] = toTS
        self.events += 2

    def halfSend(self, fromProc, mark):
        fromTS = self.ts[fromProc] + 1
        self.ts[fromProc] = fromTS
        self.marks[mark] = fromTS
        self.events += 1

    def halfRecv(self, toProc, mark):
        toTS = max(self.ts[toProc], self.marks[mark]) + 1
        self.ts[toProc] = toTS
        self.events += 1

    def clear(self):
        self.ts = [0] * len(self.ts)
        self.events = 0
        self.marks = {}

    def reportTS(self, proc=None):
        if proc == None:
            return self.ts
        else:
            return "ts[%d]=%d" % (proc, self.ts[proc])


    
