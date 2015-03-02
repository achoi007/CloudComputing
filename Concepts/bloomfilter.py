class BloomFilter(object):

    def __init__(self, mbits, hashes):
        self.bits = [0] * mbits
        self.hashes = hashes

    def insert(self, n):
        bitsChanged = []
        for hash in self.hashes:
            i = hash(n) % len(self.bits)
            if self.bits[i] != 1:
                bitsChanged.append(i)
                self.bits[i] = 1
        return bitsChanged

    def contains(self, n):
        for hash in self.hashes:
            if self.bits[hash(n) % len(self.bits)] == 0:
                return False
        return True

    def getBitsSet(self):
        return filter(lambda i: self.bits[i] == 1, range(len(self.bits)))

if __name__ == '__main__':

    def createHashFunc(i):
        def hash(x):
            return (x**2 + x**3)*i
        return hash

    hashes = [createHashFunc(i) for i in xrange(1, 4)]
    bf = BloomFilter(32, hashes)

    while True:
        input = raw_input("[r]eset, [g]et bits set, [i]nsert, [c]ontains:")
        cmd = input[0]
        if cmd == 'r':
            bf = BloomFilter(32, hashes)
            print "Cleared"
        elif cmd == 'g':
            print "Bits set", bf.getBitsSet()
        else:
            try:
                n = int((input.split())[1])
                if cmd == 'i':
                    print "Inserting", n, ":", bf.insert(n)
                elif cmd == 'c':
                    print "Contains", n, ":", bf.contains(n)
            except:
                print "Bad number argument... ignoring"
                
            
        
    

    
