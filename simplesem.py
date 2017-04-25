import sys
import re
import pdb
from tokenizer import Tokenizer

def open_file_read(filename):
    with open(filename, 'r') as fread:
        content = fread.read()
        tokens = Tokenizer(content)
        program(tokens)

def program(tokens):
    print "Program"
    statement(tokens)

    while not tokens.is_eof():
        statement(tokens)

def statement(tokens):
    print "Statement"
    c = tokens.next()
    if c == 'set':
        set(tokens)
    elif c == 'jumpt':
        jumpt(tokens)
    elif c == 'jump':
        jump(tokens)
    elif c == 'halt':
        halt(tokens)
    else:
        print "HUGE ERROR: {0}".format(c)
        sys.exit(0)

def set(tokens):
    print "Set"
    c = tokens.peek()
    if c == 'write':
        c = tokens.next()
    else:
        expr(tokens)
    c = tokens.next() # comma
    c = tokens.peek()
    if c != 'read':
        expr(tokens)
    else:
        c = tokens.next()


def jump(tokens):
    print "Jump"
    expr(tokens)

def jumpt(tokens):
    print "Jumpt"
    expr(tokens)
    c = tokens.next() # should be a comma
    if c != ',':
        print "HUGE ERROR"
    expr(tokens)
    c = tokens.next()
    if c not in ['!=', '==', '>', '<', '>=', '<=']:
        print c
        print "Error"
    expr(tokens)

def expr(tokens):
    print "Expr"
    term(tokens)
    done = False
    while not done:
        c = tokens.peek()
        if c in ['+', '-']:
            c = tokens.next()
            term(tokens)
        else:
            done = True

def term(tokens):
    print "Term"
    factor(tokens)
    done = False
    while not done:
        c = tokens.peek() # this should be * / or %
        if c in ['*', '/', '%']:
            c = tokens.next()
            factor(tokens)
        else:
            done = True

def factor(tokens):
    print "Factor"
    c = tokens.peek()
    if c == 'D':
        c = tokens.next() # D
        c = tokens.next() # [
        expr(tokens)
        c = tokens.next() # ]
    elif c == '(':
        c = tokens.next() # (
        expr(tokens)
        c = tokens.next() # )
    else:
        number(tokens)

def number(tokens):
    print "Number"
    c = tokens.next()

def halt(tokens):
    pass

def main():
    if len(sys.argv) != 2:
        print "Too few or too many arguments"
        print "Input only 1 file"
        sys.exit(0)

    filename = sys.argv[1]
    open_file_read(filename)

if __name__ == "__main__":
    main()
