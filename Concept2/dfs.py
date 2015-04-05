import unittest

class NFS:

    SERVER_COPY = 1,
    CLIENT_COPY = 2,
    SERVER_TIMESTAMP = 3
    
    @staticmethod
    def isValid(now, freshness, clntLastValid, clntLastMod, servLastMod):
        return (now - clntLastValid < freshness) or (clntLastMod >= servLastMod)
        
    @staticmethod
    def computeAction(now, freshness, clntLastValid, clntLastMod, servLastMod):
        if now - clntLastValid < freshness:
            return NFS.CLIENT_COPY
        if servLastMod <= clntLastMod:
            return NFS.SERVER_TIMESTAMP
        return NFS.SERVER_COPY
        
class NFSTest(unittest.TestCase):
    
    def testComputeAction(self):
        self.assertEquals(NFS.SERVER_COPY,
                          NFS.computeAction(1225, 3, 1203, 1135, 1136))
        self.assertEquals(NFS.CLIENT_COPY,
                          NFS.computeAction(1225, 30, 1203, 1135, 1136))
                          

if __name__ == '__main__':
    unittest.main()