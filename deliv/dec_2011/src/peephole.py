""" 
File:         peephole.py
Course:       Compilerbouw 2011
Author:       Joris Stork, Lucas Swartsenburg, Jeroen Zuiddam

The peephole module

Description:
    Contains the Peephole and Peeper classes used for optimising code.

"""


class Peephole(object):
    """ 
    wrapper for an iterable list of instructions; implemented to emulate a
    standard Python iterable object; optimisations are made on one Peephole
    instance at a time
    
    """

    def __init__(self, block, start, size):
        self.block = block
        self.start_index = start
        self.size = size
        self.instructions = self.block[start:size]
        self.counter = 0


    def __iter__(self):
        return self


    def next(self):
        if self.counter >= self.size:
            raise StopIteration
        else:
            index1 = self.start_index + self.counter
            self.current_instruction = self.block[index1]
            self.counter += 1
        return self.current_instruction


    def __getitem__(self, index):
        """   """

        try:
            return self.block[self.start_index + index]
        except TypeError:
            index1 = self.start_index + index.start
            index2 = self.start_index + index.stop
            return self.block[index1:index2]


    def __setitem__(self, index, value):
        """   """

        self.block[self.start_index + index] = value


    def __delitem__(self, index):
        """   """

        try:
            del self.block.instructions[self.start_index + index]
        except TypeError:
            index1 = self.start_index + index.start
            index2 = self.start_index + index.stop
            del self.block.instructions[index1:index2]
        self.size = self.size - 1


    def __len__(self):
        """   """

        return len(self.block[self.start_index:self.size])



class Peeper(object):
    """ 
    generates successive peepholes so that these "slide" over a basic block
    of instructions 
    
    """

    def __init__(self, block, peephole_size):
        self.block = block
        self.p_size = peephole_size
        self.counter = 0


    def __iter__(self):
        return self


    def next(self):
        if self.p_size + self.counter > len(self.block):
            raise StopIteration
        else:
            self.peephole = Peephole(self.block, self.counter, self.p_size)
            self.counter += 1
        return self.peephole
        


