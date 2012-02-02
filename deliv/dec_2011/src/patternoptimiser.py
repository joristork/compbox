
import ir

class PatternOptimiser(object):
    """
    Optimisation framework using pattern matching on objects.

    """

    pattern = """"""
    
    def __init__(self, lines):
        self.lines = lines

    def optimise(self):
        """
        Try to match the pattern on a set of consecutive lines in self.lines.
        When a match is found, run self.transform on the matching lines. Replace
        the lines with the return value of self.transform.

        """
        print "optimising lines %s with pattern %r" % (self.lines, self.pattern)
        pattern_length = len(self.pattern.splitlines())

        for index in range(len(self.lines)-pattern_length + 1):
            print "matching lines %s with pattern %r" % (self.lines, self.pattern)
            if self.match(self.lines[index:index+pattern_length], self.pattern):
                print "match found"    

                values = []
                for matching_line in self.lines[index:index+pattern_length]:
                    values.extend(matching_line.values())
                
                q = self.transform(values)
                if q:
                    del self.lines[index:index+pattern_length]
                    for r in reversed(q):
                        self.lines.insert(index, r)
                    

    @staticmethod
    def match(lines, pattern):
        print "object pattern: %s" % '\n'.join((line.pattern() for line in lines))
        return '\n'.join((line.pattern() for line in lines)) == pattern
            

    def transform(self,p):
        raise Exception('Subclass this class and overload this method.')



class BlaOptimiser(PatternOptimiser):

    pattern = """move\nmove"""

    def transform(self,p):
        print "transforming values %s" % p
        return [ir.Instr('bla',[])]



class Dollar1Optimiser(PatternOptimiser):

    pattern = """move reg"""

    def transform(self,p):
        print "transforming values %s" % p
        if p[1].expr == '$1':
            return [ir.Instr('move',[ir.Register('$2')])]

if __name__ == '__main__':
    
    x = BlaOptimiser([ir.Instr("move", [ir.Register('$1')]),ir.Instr("move", []),ir.Instr("move", [])])
    x.optimise()
    print x.lines
    y = Dollar1Optimiser(x.lines)
    y.optimise()
    print y.lines
