from math import log

def calcReplicaCount(availability, numNines):
    '''
    Calculates how many replicas are needed to guarantee numNines availability
    (e.g. 3 9's means .999 availability given the P(single node is up)
    '''
    failure = 1 - availability
    prob = float("." + "9" * numNines)
    # prob = (1 - failure**k) => k = log(1 - prob)/log(failure)
    return log(1 - prob) / log(failure)
    
