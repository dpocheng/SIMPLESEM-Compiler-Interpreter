import sys
from tokenizer import Tokenizer

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
            self.execute()

    def fetch(self):
        self.IR = self.C[self.PC]

    def incrementPC(self):
        self.PC = self.PC + 1

    def execute(self):
        self.interpretStatement()

    # interpretting grammar
    def interpretStatement(self):
        tokens = Tokenizer(self.IR)
        # YOUR CODE HERE
        c = tokens.next()
        if c == 'set':
            self.interpretSet(tokens)
        elif c == 'jumpt':
            self.interpretJumpt(tokens)
        elif c == 'jump':
            self.interpretJump(tokens)
        elif c == 'halt':
            self.halt()
        else:
            print 'HUGE ERROR: {0}'.format(c)
            sys.exit(0)

    def interpretSet(self, tokens):
        c = tokens.peek()
        inst = 'normal'
        if c == 'write':
            c = tokens.next()
            inst = 'write'
        else:
            lValue = self.interpretExpr(tokens)
        c = tokens.next() # comma
        c = tokens.peek()
        if c != 'read':
            rValue = self.interpretExpr(tokens)
        else:
            c = tokens.next()
            inst = 'read'
        if inst == 'normal':
            self.D[lValue] = rValue
        elif inst == 'write':
            self.write(rValue)
        elif inst == 'read':
            rValue = self.read()
            self.D[lValue] = rValue
        self.incrementPC()

    def interpretJump(self, tokens):
        value = self.interpretExpr(tokens)
        self.PC = value

    def interpretJumpt(self, tokens):
        boolean = False
        value = self.interpretExpr(tokens)
        c = tokens.next() # comma
        lValue = self.interpretExpr(tokens)
        op = tokens.next()
        rValue = self.interpretExpr(tokens)
        if op == '!=':
            if lValue != rValue:
                boolean = True
        elif op == '==':
            if lValue == rValue:
                boolean = True
        elif op == '>':
            if lValue > rValue:
                boolean = True
        elif op == '<':
            if lValue < rValue:
                boolean = True
        elif op == '>=':
            if lValue >= rValue:
                boolean = True
        elif op == '<=':
            if lValue <= rValue:
                boolean = True
        if boolean:
            self.PC = value
        else:
            self.incrementPC()
            

    def interpretExpr(self, tokens):
        lValue = self.interpretTerm(tokens)
        done = False
        while not done:
            c = tokens.peek()
            if c in ['+', '-']:
                c = tokens.next()
                op = c
                rValue = self.interpretTerm(tokens)
                if op == '+':
                    lValue = lValue + rValue
                else:
                    lValue = lValue - rValue
            else:
                done = True
        return lValue

    def interpretTerm(self, tokens):
        lValue = self.interpretFactor(tokens)
        done = False
        while not done:
            c = tokens.peek()
            if c in ['*', '/', '%']:
                c = tokens.next()
                op = c
                rValue = self.interpretFactor(tokens)
                if op == '*':
                    lValue = lValue * rValue
                elif op == '/':
                    lValue = lValue / rValue
                elif op == '%':
                    lValue = lValue % rValue
            else:
                done = True
        return lValue

    def interpretFactor(self, tokens):
        c = tokens.peek()
        if c == 'D':
            c = tokens.next() # D
            c = tokens.next() # [
            value = self.interpretExpr(tokens)
            c = tokens.next() # ]
            lValue = int(self.D[value])
        elif c == '(':
            c = tokens.next() # (
            lValue = self.interpretExpr(tokens)
            c = tokens.next() # )
        else:
            lValue = self.interpretNumber(tokens)
        return lValue

    def interpretNumber(self, tokens):
        c = tokens.next()
        return int(c)

    def halt(self):
        self.run_bit = False

    def printDataSeg(self):
        # DO NOT CHANGE
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
