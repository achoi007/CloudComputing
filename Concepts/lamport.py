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

if __name__ == '__main__':

    numProc = int(raw_input("Number of processes:"))
    lt = LamportTimestamp(numProc)

    def reportTS(proc):
        print "Updated ts[", proc, "]: ", lt.ts[proc]
    
    while True:
        try:
            # Read input
            input = raw_input("(c)lear, (s)tep, (m)esg, (t)imstamp, (e)vents, (h)alf send, half (r)eceive, (q)uit: ")
            args = input.split()
            cmd = input[0]
            # Process commands
            if cmd == 'c':
                lt.clear()
                print "Cleared"
            elif cmd == 's':
                proc = int(args[1])
                lt.addStep(proc)
                reportTS(proc)
            elif cmd == 'm':
                fromProc = int(args[1])
                toProc = int(args[2])
                lt.sendMesg(fromProc, toProc)
                reportTS(fromProc)
                reportTS(toProc)                
            elif cmd == 't':
                print "Timestamps:", lt.ts
            elif cmd == 'e':
                print "Num of events:", lt.events
            elif cmd == 'q':
                break
            elif cmd == 'h':
                proc = int(args[1])
                mark = args[2]
                lt.halfSend(proc, mark)
                reportTS(proc)
            elif cmd == 'r':
                proc = int(args[1])
                mark = args[2]
                lt.halfRecv(proc, mark)
                reportTS(proc)
        except:
            print "Ignoring error"
            
    
