""" 
File:         peephole.py
Course:       Compilerbouw 2011
Author:       Joris Stork, Lucas Swartsenburg, Jeroen Zuiddam

The peephole module

Description:
    blah

"""


class Peephole(object):
    """ Contains an iterable list of instructions """

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
            self.current_instruction = self.block[self.start_index + self.counter]
            self.counter += 1
        return self.current_instruction


    def __getitem__(self, index):
        """   """

        try:
            return self.block[self.start_index + index]
        except TypeError:
            return self.block[self.start_index + index.start:self.start_index + index.stop]


    def __setitem__(self, index, value):
        """   """

        self.block[self.start_index + index] = value


    def __delitem__(self, index):
        """   """

        try:
            del self.block.instructions[self.start_index + index]
        except TypeError:
            del self.block.instructions[self.start_index + index.start:self.start_index + index.stop]
        self.size = self.size - 1


    def __len__(self):
        """   """

        return len(self.block[self.start_index:self.size])



class Peeper(object):
    """   """

    def __init__(self, block, peephole_size):
        self.block = block
        """ raise an error here if attempt to set size too big """
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
        


