import numpy as np
import unittest

class Scheduler:
    
    def schedule(self, tasks):
        abstract
        
    def calcCompletionTimes(self, tasks):
        acclist = []
        acc = 0
        for t in tasks:
            acc += t
            acclist.append(acc)
        return acclist
        
    def calcAvgCompletionTime(self, tasks):
        acclist = self.calcCompletionTimes(tasks)
        return float(sum(acclist)) / len(acclist)
        
        
class FIFOScheduler(Scheduler):
    
    def schedule(self, tasks):
        return tasks
        
        
class ShortestTaskFirstScheduler(Scheduler):
    
    def schedule(self, tasks):
        if type(tasks) != list:
            tasks = list(tasks)
        tasks.sort()
        return tasks
        
        
class DominantResourceFairness:
    
    def setTotalResourceVector(self, totalRes):
        self.totalRes = np.array(totalRes, dtype=float)
        
    def compute(self, jobs):
        '''
        Compute dominant resource for each job.
        Job is of the form (resource1, resource2, ...) for example
        (1 CPU, 2 GB RAM, ...)
        Return will be a list of tuples of the form (N, ratio) where N
        is the dominant resource and ratio is the % of total resource
        '''
        consumes = [np.array(j, dtype=float) / self.totalRes for j in jobs]
        dominants = [j.argmax() for j in consumes]
        return [(dominants[i], consumes[i][dominants[i]]) for i in xrange(len(dominants))]
        
class SchedulerTest(unittest.TestCase):
    
    def testScheduler(self):
        stf = ShortestTaskFirstScheduler()
        t = stf.schedule((10, 15, 4, 15, 23))
        self.assertAlmostEquals(31.6, stf.calcAvgCompletionTime(t), 2)
        t = stf.schedule([5, 4, 4, 3, 2, 1, 1])
        self.assertAlmostEquals(8.57, stf.calcAvgCompletionTime(t), 2)
        
    def testDRF(self):
        drf = DominantResourceFairness()
        drf.setTotalResourceVector((36, 72))
        res = drf.compute([(1, 4), (3, 1)])
        self.assertEquals(1, res[0][0])
        self.assertEquals(4.0/72, res[0][1])
        self.assertEquals(0, res[1][0])
        self.assertEquals(3.0/36, res[1][1])
        self.assertAlmostEquals(res[0][1]*12, res[1][1]*8, 4)
        
if __name__ == '__main__':
    unittest.main()
        

        
    
        
        
        

