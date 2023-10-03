from __future__ import division

import math
import sys
import sp

try:
    import readline
except ImportError:
    pass

class Calc(dict):

    def __init__(self):
        dict.__init__(self)
        _fy = lambda f, y: lambda x: f(x, y)
        _fg = lambda f, g: lambda x: g(f(x))
        _ = lambda x: x
        fx = lambda f, x: f(x)
        xf = lambda x, f: f(x)
        def reduce(x, fs):
            for f in fs: x = f(x)
            return x
        self.parser = sp.compile(r"""

            ident = r'[a-zA-Z_]\w*' ;

            real = r'(?:\d+\.\d*|\d*\.\d+)(?:[eE][-+]?\d+)?|\d+[eE][-+]?\d+' : `float` ;
            int = r'\d+' : `int` ;
            var = ident : `self.__getitem__`;

            add_op = '+'    `lambda x, y: x + y` ;
            add_op = '-'    `lambda x, y: x - y` ;
            add_op = '|'    `lambda x, y: x | y` ;
            add_op = '^'    `lambda x, y: x ^ y` ;

            mul_op = '*'    `lambda x, y: x * y` ;
            mul_op = '/'    `lambda x, y: x / y` ;
            mul_op = '%'    `lambda x, y: x % y` ;
            mul_op = '&'    `lambda x, y: x & y` ;
            mul_op = '>>'   `lambda x, y: x << y` ;
            mul_op = '<<'   `lambda x, y: x >> y` ;

            pow_op = '**'   `lambda x, y: x ** y` ;

            un_op = '+'     `lambda x: +x` ;
            un_op = '-'     `lambda x: -x` ;
            un_op = '~'     `lambda x: ~x` ;

            post_un_op = '!'    `math.factorial` ;

            separator: r'\s+';

            !S = ident '=' expr :: `self.__setitem__`
               | expr
               ;

            expr = term (add_op term :: `_fy`)* :: `reduce` ;
            term = fact (mul_op fact :: `_fy`)* :: `reduce` ;
            fact = un_op fact :: `fx` | pow ;
            pow = postfix (pow_op fact :: `_fy`)? :: `reduce` ;

            #postfix = atom post_un_op :: `xf` | atom ;
            postfix = atom _postfix :: `xf` ;
            _postfix = post_un_op _postfix :: `_fg` | `_` ;

            atom = '(' expr ')' ;
            atom = real | int ;
            atom = var ;

        """)

    def __call__(self, input):
        return self.parser(input)

def exc():
    e = getattr(sys, 'exc_value', None)
    if e is None:
        info = getattr(sys, 'exc_info', None)
        if info is not None: e = info()[1]
    return e

try: input
except NameError: input = input

calc = Calc()

while True:
    expr = input(": ")
    sp.clean()
    try:
        val = calc(expr)
        if val is not None:
            print("= %s"%calc(expr))
    except:
        print("! %s"%exc())
    print("")
