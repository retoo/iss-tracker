import unittest

class Score(object):
    """Takes several criterias and calculates a overall score"""
    def __init__(self):
        super(Score, self).__init__()
        
        self.criterias = []
        self.total_weight = 0
        
    def add(self, criteria, value, weight = 1):
        """Adds another criteria to the score"""
        self.criterias.append([weight, criteria, value])
        self.total_weight += weight
    
    def score(self):
        """Calculates the current score"""
        if len(self.criterias) == 0:
            raise RuntimeError("No criterias added yet")
            
        total = 0
        
        for weight, criteria, value in self.criterias:
            score = criteria.score(value)
            total += weight * score
            
        return float(total / self.total_weight)
        
    def report(self):
        out = []
        
        total = 0
        for weight, criteria, value in self.criterias:
            score = criteria.score(value)
            total += weight * score
            out.append("%s %i %% Value: %.1f Weight: %.1f" % \
                (criteria.name, score, value, weight))
                
        out.append("Total Score: %.1f %%" % (total / self.total_weight))
        return "\n".join(out) + "\n"

class Criteria(object):
    def __init__(self, name, start, end, max_score = 100):
        self.name = name
        self.start = start
        self.end = end
        self.range = self.end - self.start
        self.max_score = max_score
        pass
        
    def score(self, value):
        score = self.max_score * (value - self.start)  / self.range
        
        if score < 0:
            score = 0
        if score > 100:
            score = 100
            
        return score
        
if __name__ == "__main__":
    class CriteriaTest(unittest.TestCase):
        def testNormal(self):
            c1 = Criteria("c1", 0, 10)
            
            self.assertEquals(c1.score(1), 10)
            self.assertEquals(c1.score(2), 20)     
            self.assertEquals(c1.score(5), 50)
            self.assertEquals(c1.score(10), 100)
            self.assertEquals(c1.score(3), 30)
    
            c2 = Criteria("c2", 5, 10)
            self.assertEquals(c2.score(5), 0)
            self.assertEquals(c2.score(10), 100)
            self.assertEquals(c2.score(7), 40)
            
        def testOffLimit(self):
            c1 = Criteria("c1", 0, 10)
            
            self.assertEquals(c1.score(-1), 0)
            self.assertEquals(c1.score(11), 100)     
        
        def testReversed(self):
            c1 = Criteria("c1", 10, 0)
            
            self.assertEquals(c1.score(0), 100)
            self.assertEquals(c1.score(5), 50)
            self.assertEquals(c1.score(10), 0)
            self.assertEquals(c1.score(11), 0)
            self.assertEquals(c1.score(-1), 100)
            self.assertEquals(c1.score(-2), 100)
            self.assertEquals(c1.score(2), 80)

    class ScoreTest(unittest.TestCase):
        def testNormal(self):
            c1 = Criteria("c1", 0, 10)
            c2 = Criteria("c2", 10, 0)
            c3 = Criteria("c3", 0, 5)
            
            s1 = Score()

        
            s1.add(c1, 3)
            s1.add(c2, 1)
            s1.add(c3, 3, 3)
            self.assertEquals(s1.score(), 60)
            
            s2 = Score()
            s2.add(c1, 0, 0)
            s2.add(c2, 0, 0)
            s2.add(c3, 3, 3)
            self.assertEquals(s2.score(), 3*100/5)
            
            s3 = Score()
            s3.add(c1, 0, 3) # 0
            s3.add(c2, 0, 6) # 100 *6 = 600
            s3.add(c3, 1, 1) #100/5 * 1 =20 
            self.assertEquals(s3.score(), 62) # 600 + 20 = 620 / 10 
            
    unittest.main()