import election

def q1():
    ring = election.RingElection([10, 3, 2, 4, 7, 6, 8, 9, 5])
    ring.initElection(2)
    return ring.getMsgCnt()
    
def q2():
    ring = election.RingElection([2015, 2001, 2003, 2005, 2002, 2004])
    ring.initElection(2003)
    return ring.getMsgCnt()
    
if __name__ == "__main__":
    print "Q1", q1()
    print "Q2", q2()
    
    
    