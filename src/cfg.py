#
# Control Flow Graph
#

from ir import *



class BasicBlock(object):
    """   """
    def __init__(self, instructions):
        self.instructions = instructions


    def length(self):
        """   """
        return len(self.objects)


    def set_instruction(self, index, value):
        """   """
        self.instructions[index] = expr


    def get_instructions(self, index, length):
        """   """
        return self.instructions[index:length]



class CFG(object):
    def __init__(self, object_list):
        pass

    def cfg_to_list(self):
        pass
