from math import log

def calcReplicaCount(availability, numNines):
    failure = 1 - float(availability)
    prob = float("." + "9" * numNines)
    # prob = (1 - failure**k) => k = log(1 - prob)/log(failure)
    return log(1 - prob) / log(failure)
    
