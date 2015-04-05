import numpy as np

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
        tasks.sort()
        return tasks
        
        
class DominantResourceFairnessScheduler:
    
    def setTotalResourceVector(self, totalRes):
        self.totalRes = np.array(totalRes, dtype=float)
        
    def computeTaskAllocation(self, jobs):
        '''
        Compute and return a vector of task that should be allocated to each
        job based on DRF.  Each job is a vector of resource required, e.g.
        (1 CPU, 8 GB RAM, ...)
        Return: (5 tasks, 3 tasks, ...) which means 5 tasks for job 1, 3 tasks
        for job 2, etc.
        '''
        consumes = [np.array(j, dtype=float) / self.totalRes for j in jobs]
        dominants = [j.argmax() for j in consumes]
        # Compute taskRes so that
        # taskRes[i] * consumes[dominants[i]] is same for all i's
        
    
        
        
        

