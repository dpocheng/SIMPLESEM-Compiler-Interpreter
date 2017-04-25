import re
import sys

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'

class Tokenizer():
    def __init__(self, characters):
        self.tokens = self.lexer(characters)
        self.curPos = 0

    def lex(self, characters, token_exprs):
        pos = 0
        tokens = []
        while pos < len(characters):
            match = None
            for token_expr in token_exprs:
                pattern, tag = token_expr
                regex = re.compile(pattern)
                match = regex.match(characters, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        token = (text, tag)
                        tokens.append(token)
                    break
            if not match:
                print 'Illegal character: %s\\n' % characters[pos]
                sys.exit(1)
            else:
                pos = match.end(0)
        return tokens

    def lexer(self, characters):
        token_exprs = [
                (r'[ \r\n\t]+', None),
                (r'#[^\\n]*',   None),
                (r'set',        RESERVED),
                (r'read',        RESERVED),
                (r'write',        RESERVED),
                (r'halt',        RESERVED),
                (r'jumpt',        RESERVED),
                (r'jump',        RESERVED),
                (r'!=',        RESERVED),
                (r'==',        RESERVED),
                (r'>=',        RESERVED),
                (r'<=',        RESERVED),
                (r'>',        RESERVED),
                (r'<',        RESERVED),
                (r'\+',        RESERVED),
                (r'-',        RESERVED),
                (r'\*',        RESERVED),
                (r'/',        RESERVED),
                (r'%',        RESERVED),
                (r'D',        RESERVED),
                (r',',        RESERVED),
                (r'\(',        RESERVED),
                (r'\)',        RESERVED),
                (r'\[',        RESERVED),
                (r'\]',        RESERVED),
                (r'0|[1-9]+[0-9]*', INT)];

        return self.lex(characters, token_exprs)

    def next(self):
        if self.is_eof(): return None
        toreturn = self.tokens[self.curPos]
        self.curPos += 1
        return toreturn[0]

    def peek(self):
        if self.is_eof(): return None
        return self.tokens[self.curPos][0]

    def is_eof(self):
        return self.curPos == len(self.tokens)

