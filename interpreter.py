import sys
from tokenizer import Tokenizer
import pdb

class Interpreter:
    def __init__(self, codefile, infile):
        DATA_SEG_SIZE = 100

        outfile = "{0}.out".format(codefile)
        self.D = [0 for i in range(DATA_SEG_SIZE)]
        self.PC = 0
        self.input_tokens = iter(open(infile, 'r').read().split('\n'))
        self.outhandle = open(outfile, 'w')
        self.IR=''
        self.run_bit = True

        with open(codefile, 'r') as fread:
            self.C = fread.read().split('\n')


    def runProgram(self):
        while self.run_bit:
            self.fetch()
            self.incrementPC()
            self.execute()

    def fetch(self):
        self.IR = self.C[self.PC]

    def incrementPC(self):
        self.PC += 1

    def execute(self):
        self.interpretStatement()

    def interpretStatement(self):
        tokens = Tokenizer(self.IR)
        c = tokens.next()

        # parse the code and interpret
        if c == 'set':
            self.interpretSet(tokens)
        elif c == 'jumpt':
            self.interpretJumpt(tokens)
        elif c == 'jump':
            line = self.interpretJump(tokens)
            self.PC = line
        elif c == 'halt':
            self.interpretHalt(tokens)
        else:
            print "HUGE ERROR: {0}".format(c)
            sys.exit(0)

    def interpretJump(self, tokens):
        value = self.interpretExpr(tokens)
        return value

    def interpretJumpt(self, tokens):
        line = self.interpretExpr(tokens)
        c = tokens.next() # should be a comma
        firstexpr = self.interpretExpr(tokens)
        c = tokens.next()
        if c not in ['!=', '==', '>', '<', '>=', '<=']:
            print c
            print "Error"
        secondexpr = self.interpretExpr(tokens)
        cond = False
        if c == '!=': cond = (firstexpr != secondexpr)
        elif c == '==': cond = (firstexpr == secondexpr)
        elif c == '>': cond = (firstexpr > secondexpr)
        elif c == '<': cond = (firstexpr < secondexpr)
        elif c == '>=': cond = (firstexpr >= secondexpr)
        elif c == '<=': cond = (firstexpr <= secondexpr)

        if cond:
            self.PC = line

    def interpretSet(self, tokens):
        c = tokens.peek()
        is_write = False
        is_read = False
        if c == 'write':
            c = tokens.next()
            is_write = True
        else:
            dest = self.interpretExpr(tokens)

        c = tokens.next() # comma

        c = tokens.peek()
        if c == 'read':
            c = tokens.next()
            is_read = True
        else:
            source = self.interpretExpr(tokens)

        if is_write:
            self.write(source)
        elif is_read:
            self.D[dest] = self.read()
        else: #D[destination] = source
            self.D[dest] = source


    def interpretExpr(self, tokens):
        total = self.interpretTerm(tokens)
        done = False
        while not done:
            c = tokens.peek()
            if c == '+':
                c = tokens.next()
                total += self.interpretTerm(tokens)
            elif c == '-':
                c = tokens.next()
                total -= self.interpretTerm(tokens)
            else:
                done = True
        return total

    def interpretTerm(self, tokens):
        total = self.interpretFactor(tokens)
        done = False
        while not done:
            c = tokens.peek() # this should be * / or %
            if c in ['*', '/', '%']:
                c = tokens.next()
                value = self.interpretFactor(tokens)
                if c == '*':
                    total = total * value
                elif c == '/':
                    total = total / value
                elif c == '%':
                    total = total % value
            else:
                done = True

        return total

    def interpretFactor(self, tokens):
        c = tokens.peek()
        if c == 'D':
            c = tokens.next() # D
            c = tokens.next() # [
            value = self.D[self.interpretExpr(tokens)]
            c = tokens.next() # ]
        elif c == '(':
            c = tokens.next() # (
            value = self.interpretExpr(tokens)
            c = tokens.next() # )
        else:
            value = self.interpretNumber(tokens)
        return value

    def interpretNumber(self, tokens):
        c = tokens.next()
        return int(c)

    def interpretHalt(self, tokens):
        self.run_bit = False

    # DO NOT CHANGE
    def printDataSeg(self):
        self.outhandle.write("Data Segment Contents\n")
        for i in range(len(self.D)):
            self.outhandle.write('{0}: {1}\n'.format(i, self.D[i]))

    # read in value from file
    # DO NOT CHANGE
    def read(self):
        return self.input_tokens.next()

    # write out the file
    # DO NOT CHANGE
    def write(self, value):
        self.outhandle.write('{0}\n'.format(value))

def main():
    if len(sys.argv) != 3:
        print "Wrong usage: python interpreter.py <programfile> <inputfile>"
        sys.exit(0)

    codepath = sys.argv[1]
    inputpath = sys.argv[2]

    # init the interpreter
    interpreter = Interpreter(codepath, inputpath)

    # running the program
    interpreter.runProgram()

    # print out the data segment
    interpreter.printDataSeg()

if __name__ == "__main__":
    main()
