from optimise import Graph

class OpTest(object):
    """
    Op for testing
    """
    
    def __init__(self, expr):
        self.expr = expr
        expr_split = expr.split(' ')
        self.type = expr_split[0]

        self.arguments = expr_split[1]
        if type(self.arguments) == str:
            self.arguments = [self.arguments]

    def get_jump_target_index(self, index):
        return int(self.arguments[0])

    def __repr__(self):
        return 'Op(%s)' % str(self.expr)

def test():
    lines = [
        "op0 x",        #0
        "op1 y",        #1
        "control 0",    #2
        "op3 z",        #3
        "op4 x",        #4
        "control 0",    #5
        "control 8",    #6
        "control 7"     #7
        ]
    g = Graph(lines, OpTest)

    for b in g.blocks:
        print b


if __name__ == '__main__':
    test()    
