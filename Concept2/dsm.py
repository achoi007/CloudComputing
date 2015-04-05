import unittest

class DistSharedMem:
    
    NONE = 0,
    READ = 1,
    WRITE = 2
    
    def __init__(self, numProcs, owner):
        self.states = [DistSharedMem.NONE] * numProcs
        self.owner = owner
        self.states[self.owner] = DistSharedMem.READ
        
    def read(self, process):
        state = self.states[process]
        # No-op if process already has read or write access
        if state == DistSharedMem.READ or state == DistSharedMem.WRITE:
            return
        # Force all other processes to downgrade to read
        for p in self._getProcs():
            if p != process and self.states[p] == DistSharedMem.WRITE:
                self.states[p] = DistSharedMem.READ
        # Mark current process as read
        self.states[process] = DistSharedMem.READ
        
    def write(self, process):
        state = self.states[process]
        # No-op if process already has write access
        if state == DistSharedMem.WRITE:
            return
        # Force all other processes to invalidate
        for p in self._getProcs():
            if p != process and self.states[p] == DistSharedMem.READ:
                self.states[p] = DistSharedMem.NONE
        self.states[process] = DistSharedMem.WRITE
        # If not owner, become owner
        if process != self.owner:
            self.owner = process
            
    def isNone(self, process):
        return self.states[process] == DistSharedMem.NONE
        
    def isRead(self, process):
        return self.states[process] == DistSharedMem.READ
        
    def isWrite(self, process):
        return self.states[process] == DistSharedMem.WRITE
        
    def _getProcs(self):
        return xrange(len(self.states))
        
class DistSharedMemTest(unittest.TestCase):
    
    def setUp(self):
        self.dsm = DistSharedMem(4, 0)
        
    def testBasic(self):
        dsm = self.dsm
        self.assertEquals(0, dsm.owner)
        for i in xrange(4):
            if i != dsm.owner:
                self.assertTrue(dsm.isNone(i))
            else:
                self.assertTrue(dsm.isRead(i))
        
    def testSingle(self):
        dsm = self.dsm
        dsm.read(0)
        self.assertTrue(dsm.isRead(0))
        dsm.write(0)
        self.assertTrue(dsm.isWrite(0))
        dsm.read(0)
        self.assertTrue(dsm.isWrite(0))
    
    def testSharedRead(self):
        dsm = self.dsm
        dsm.read(2)
        dsm.read(3)
        self.assertTrue(dsm.isRead(0))
        self.assertTrue(dsm.isRead(2))
        self.assertTrue(dsm.isRead(3))
        
    def testReadWhenWrite(self):
        dsm = self.dsm
        dsm.write(0)
        dsm.read(1)
        self.assertTrue(dsm.isRead(0))
        self.assertTrue(dsm.isRead(1))
        
    def testWriteWhenRead(self):
        dsm = self.dsm
        dsm.read(2)
        dsm.read(3)
        dsm.write(0)
        self.assertTrue(dsm.isWrite(0))
        self.assertTrue(dsm.isNone(2))
        self.assertTrue(dsm.isNone(3))
        
    def testNonOwnerWriteWhenRead(self):
        dsm = self.dsm
        dsm.read(2)
        dsm.read(3)
        dsm.write(3)
        self.assertTrue(dsm.isNone(0))
        self.assertTrue(dsm.isNone(2))
        self.assertTrue(dsm.isWrite(3))
        self.assertEquals(3, dsm.owner)
        
if __name__ == '__main__':
    unittest.main()
        
    