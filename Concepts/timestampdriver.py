import sys
from lamport import LamportTimestamp
from vectorclock import VectorClock

class Driver(object):

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def run(self):
        ts = self.timestamp
        while True:
            try:
                # Read input
                input = raw_input("(c)lear, (s)tep, (m)esg, (t)imstamp, (e)vents, (h)alf send, half (r)eceive, (q)uit: ")
                args = input.split()
                cmd = input[0]
                # Process commands
                if cmd == 'c':
                    ts.clear()
                    print "Cleared"
                elif cmd == 's':
                    proc = int(args[1])
                    ts.addStep(proc)
                    print ts.reportTS(proc)
                elif cmd == 'm':
                    fromProc = int(args[1])
                    toProc = int(args[2])
                    ts.sendMesg(fromProc, toProc)
                    print ts.reportTS(fromProc)
                    print ts.reportTS(toProc)                
                elif cmd == 't':
                    print "Timestamps:", ts.reportTS()
                elif cmd == 'e':
                    print "Num of events:", ts.events
                elif cmd == 'q':
                    break
                elif cmd == 'h':
                    proc = int(args[1])
                    mark = args[2]
                    ts.halfSend(proc, mark)
                    print ts.reportTS(proc)
                elif cmd == 'r':
                    proc = int(args[1])
                    mark = args[2]
                    ts.halfRecv(proc, mark)
                    print ts.reportTS(proc)
            except:
                print "Ignoring error", sys.exc_info()[0]

if __name__ == '__main__':
    numProc = int(raw_input("Number of procs: "))
    systemName = raw_input("(l)amport, (v)ector clock: ")
    if systemName[0] == "l":
        ts = LamportTimestamp(numProc)
    elif systemName[0] == 'v':
        ts = VectorClock(numProc)
    else:
        print "Unknown timestamp system!"
        raise KeyError()

    driver = Driver(ts)
    driver.run()
