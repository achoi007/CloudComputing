import unittest
from collections import defaultdict
from itertools import combinations, product, ifilter

class SerialEquivalence:
    '''
    2 txns are serially equivalent iff all pairs of conflicting ops (pair
    containing 1 op from each txn) are executed in same order (txn order) for
    all objects they both access.
    
    Conflicting ops are:
        * read(x) and write(x)
        * write(x) and read(x)
        * write(x) and write(x)
        * NOT read(x) and read(x)
        * NOT read/write(x) and read/write(y)
        
    * Take all pairs of conflict ops - 1 from T1 and 1 from T2
    * If T1 op was reflected first on server, mark pair as (T1, T2) else (T2, T1)
    * All pairs should either be (T1, T2) or (T2, T1)
    '''
    
    WRITE = 1
    READ = 2
    
    @staticmethod
    def check(txns):
        return all(map(SerialEquivalence.checkPairs, combinations(txns, 2)))
        
    @staticmethod
    def checkPairs(txnPair):
        currOrder = None
        for (t1, t2) in SerialEquivalence.iterateConflicts(txnPair):
            # If op in T1 is before op in T2, generate (T1, T2) else generate
            # (T2, T1)
            t1time = t1[2]
            t2time = t2[2]
            if t1time < t2time:
                order = (1, 2)
            elif t1time > t2time:
                order = (2, 1)
            else:
                order = (1, 2)
            # If there is no current order, make this current order.
            if currOrder == None:
                currOrder = order
            # Otherwise, if order is different from previous order, the pair
            # is not serially equivalent.
            elif currOrder != order:
                return False
        return True     
    
    @staticmethod
    def iterateConflicts(txnPair):
        return ifilter(SerialEquivalence.inConflict, product(*txnPair))
            
    @staticmethod
    def inConflict(ops):
        '''
        Conflicting ops are:
        * read(x) and write(x)
        * write(x) and read(x)
        * write(x) and write(x)
        * NOT read(x) and read(x)
        * NOT read/write(x) and read/write(y)        
        '''
        op1,op2 = ops
        return op1[1] == op2[1] and \
        not(op1[0] == SerialEquivalence.READ and op2[0] == SerialEquivalence.READ)
        

        
class SerialEquivalenceTest(unittest.TestCase):
    
    def readTxn(self, txnId, objId=None):
        self.addTxn(txnId, SerialEquivalence.READ, objId)
        
    def writeTxn(self, txnId, objId=None):
        self.addTxn(txnId, SerialEquivalence.WRITE, objId)
        
    def addTxn(self, txnId, txnType, objId):
        if objId == None:
            objId = self.defaultObjId
        self.txns[txnId].append((txnType, objId, self.timestamp))
        self.timestamp += 1
        
    def getTxns(self):
        return self.txns.values()
        
    def setUp(self):
        self.timestamp = 0
        self.txns = defaultdict(list)
        self.defaultObjId = "abc"
        
    def testAllRead(self):
        self.readTxn(0)
        self.readTxn(1)
        self.readTxn(0)
        self.readTxn(1)
        txns = self.getTxns()
        self.assertTrue(SerialEquivalence.check(txns))
        
    def testLostUpdate(self):
        self.readTxn(0)
        self.readTxn(1)
        self.writeTxn(0)
        self.writeTxn(1)
        txns = self.getTxns()
        self.assertFalse(SerialEquivalence.check(txns))
        
    def testInconsistentRetrieval(self):
        self.readTxn(0, "123")
        self.readTxn(0, "789")
        self.writeTxn(0, "123")
        self.readTxn(1, "123")
        self.readTxn(1, "789")
        self.writeTxn(0, "789")
        txns = self.getTxns()
        self.assertFalse(SerialEquivalence.check(txns))
        
    def testReadWriteQ11(self):
        self.readTxn(0, "x")
        self.writeTxn(1, "x")
        self.writeTxn(1, "y")
        self.readTxn(0, "x")
        self.writeTxn(0, "y")
        txns = self.getTxns()
        self.assertFalse(SerialEquivalence.check(txns))
        
    def testReadWriteQ12(self):
        self.writeTxn(1, "y")
        self.writeTxn(1, "x")
        self.writeTxn(1, "y")
        self.readTxn(0, "x")
        self.writeTxn(1, "y")
        self.writeTxn(0, "y")
        txns = self.getTxns()        
        self.assertTrue(SerialEquivalence.check(txns))
        
    def testReadWriteQ13(self):
        self.writeTxn(1, "a")
        self.readTxn(2, "b")
        self.writeTxn(2, "b")
        self.readTxn(1, "b")
        self.writeTxn(2, "a")
        self.readTxn(1, "a")
        txns = self.getTxns()        
        self.assertFalse(SerialEquivalence.check(txns))
    
    def testThreeTxns(self):
        self.readTxn("v", "x")
        self.readTxn("v", "y")
        self.writeTxn("u", "x")
        self.readTxn("u", "y")
        self.readTxn("v", "x")
        self.readTxn("u", "y")
        self.readTxn("v", "y")
        self.readTxn("v", "x")
        self.readTxn("v", "y")
        self.readTxn("t", "x")
        self.writeTxn("t", "y")
        txns = self.getTxns()
        self.assertFalse(SerialEquivalence.check(txns))
        
    def testReadWriteQ15(self):
        self.readTxn(2, "b")
        self.writeTxn(1, "a")
        self.readTxn(1, "b")
        self.readTxn(1, "a")
        self.writeTxn(2, "b")
        self.writeTxn(2, "a")
        txns = self.getTxns()
        self.assertTrue(SerialEquivalence.check(txns))
        
    def testExam1(self):
        self.readTxn(98, "x")
        self.writeTxn(99, "x")
        self.writeTxn(99, "y")
        self.readTxn(99, "y")
        self.writeTxn(98, "x")
        self.writeTxn(99, "y")
        self.writeTxn(98, "y")
        txns = self.getTxns()
        self.assertFalse(SerialEquivalence.check(txns))
        
    def testExam2(self):
        self.readTxn(1, "x")
        self.readTxn(3, "x")
        self.readTxn(3, "y")
        self.readTxn(2, "x")
        self.readTxn(2, "y")
        self.writeTxn(3, "x")
        self.readTxn(2, "x")
        self.readTxn(3, "y")
        self.readTxn(3, "x")
        self.readTxn(3, "y")
        self.writeTxn(1, "y")
        txns = self.getTxns()
        self.assertFalse(SerialEquivalence.check(txns))        
    
if __name__ == '__main__':
    unittest.main()