import election

def q1():
    ring = election.RingElection([10, 3, 2, 4, 7, 6, 8, 9, 5])
    ring.initElection(2)
    return ring.getMsgCnt()
    
if __name__ == "__main__":
    print "Q1", q1()
    
    