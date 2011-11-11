#!/usr/bin/env python


parse_op


def parse(self, expr):
    if expr[0] = '\t':
        pattern = re.compile('[\s,]+')
        expr_elements = pattern.split(expr.lstrip(' ,'))
        self.type = expr_elements[0]
        if expr_elements[0].startswith("B"):
            offset = int(expr_elements[-1])
            self.destinations.append(offset + self.original_line_nr)
