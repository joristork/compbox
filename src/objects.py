class Expr(object):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return '<Expr %r>' % (self.expr,)

class Instr(Expr):

    def __init__(self, instr, args):
        self.instr = instr
        self.args = args

    def __repr__(self):
        return '<Instr %r %r>' % (self.instr, self.args)

class Register(Expr):
    def __repr__(self):
        return '<Register %r>' % self.expr

class Raw(Expr):
    def __repr__(self):
        return '<Raw %r>' % self.expr

class Comment(Expr):
    def __repr__(self):
        return '<Comment %r>' % self.expr

class Label(Expr):
    def __repr__(self):
        return '<Label %r>' % self.expr

