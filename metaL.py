## metaL core /Python/

import os, sys

log = open(sys.argv[0][:-3] + '.log', 'w')

## graph

class Object:
    def __init__(self, V):
        self.val = V
        self.slot = {}
        self.nest = []
        self.id = '%x' % id(self)

    ## dump

    def __repr__(self): return self.dump()

    def test(self): return self.dump(test=True)

    def dump(self, depth=0, prefix='', test=False):
        # header
        tree = self.pad(depth) + self.head(prefix, test)
        # block cycles
        if not depth:
            Object.dumped = []
        if self in Object.dumped:
            return tree + ' _/'
        else:
            Object.dumped.append(self)
        # slot{}s
        for i in self.slot:
            tree += self.slot[i].dump(depth + 1, prefix='%s = ' % i)
        # nest[]ed
        idx = 0
        for j in self.nest:
            tree += j.dump(depth + 1, prefix='%s = ' % idx)
            idx += 1
        # subtree
        return tree

    def head(self, prefix='', test=False):
        hdr = '%s<%s:%s>' % (prefix, self._type(), self._val())
        if not test:
            hdr += ' @%s' % self.id
        return hdr

    def pad(self, depth): return '\n' + '\t' * depth

    def _type(self): return self.__class__.__name__.lower()
    def _val(self): return '%s' % self.val

    ## plot

    def plot_g6(self, depth=0, plt='', nodes='', edges='', parent=None, label=''):
        # header
        if not depth:
            plt += 'const data = {\n'
            Object.plotted = []
        # cycles
        if self in Object.plotted:
            return (plt, nodes, edges)
        else:
            Object.plotted.append(self)
        # itself
        nodes += '\n\t\t{id:"%s",label:"%s"},' % (
            self.id, self.head(test=True))
        if parent:
            edges += '\n\t\t{source:"%s",target:"%s",label:"%s"},' % (
                parent.id, self.id, label)
        # slot{}s
        for i in self.slot:
            plt, nodes, edges = self.slot[i].plot_g6(
                depth + 1, plt, nodes, edges, parent=self, label=i)
        # footer
        if not depth:
            plt += '\tnodes: [%s\n\t],\n' % nodes
            plt += '\tedges: [%s\n\t],\n' % edges
            plt += '};\n'
            return plt
        else:
            return (plt, nodes, edges)

    ## operator

    def __getitem__(self, key):
        return self.slot[key]

    def __setitem__(self, key, that):
        self.slot[key] = that
        return self

    def __lshift__(self, that):
        return Object.__setitem__(self, that._type(), that)

    def __rshift__(self, that):
        return Object.__setitem__(self, that._val(), that)
        # return that

    def __floordiv__(self, that):
        self.nest.append(that)
        return self

    ## stack

    def top(self): return self.nest[-1]
    def tip(self): return self.nest[-2]
    def pop(self): return self.nest.pop(-1)
    def pip(self): return self.nest.pop(-2)

    def dup(self): return self // self.top()
    def drop(self): self.pop(); return self
    def swap(self): return self // self.pip()
    def over(self): return self // self.tip()
    def press(self): self.pip(); return self
    def dropall(self): self.nest = []; return self

    ## evaluate

    def eval(self, ctx): return self

    ## html

    def html_head(self): return self.val

    def html(self):
        ht = self.html_head()
        for i in self.slot:
            ht += self.slot[i].html()+'<p>\n'
        for j in self.nest:
            ht += j.html()+'<p>\n'
        return ht


## primitive

class Primitive(Object):
    def eval(self, ctx): return self

class Symbol(Primitive):
    def eval(self, ctx):
        return ctx[self.val]

class String(Primitive):
    def html(self): return self.val

class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))

class Hex(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x10))

    def _val(self):
        return hex(self.val)

class Bin(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x02))

    def _val(self):
        return bin(self.val)

# container

class Container(Object):
    pass

class Vector(Container):
    pass
class Dict(Container):
    pass
class Stack(Container):
    pass

## active

class Active(Object):
    pass

class VM(Active):
    pass


vm = VM('metaL')
vm << vm
env = Vector('env')
vm >> env
for i in os.environ:
    env[i] = String(os.environ[i])


class Command(Active):
    def __init__(self, F):
        Active.__init__(self, F.__name__)
        self.fn = F

    def eval(self, ctx):
        return self.fn(ctx)

    def apply(self, that, ctx):
        return self.fn(that, ctx)

def QQ(that, ctx): print(that, file=log); sys.exit(0)

## debug


vm['??'] = Command(QQ)

## stack

def dup(that, ctx): return that.dup()
def drop(that, ctx): return that.drop()
def swap(that, ctx): return that.swap()
def over(that, ctx): return that.over()
def press(that, ctx): return that.press()
def dropall(that, ctx): return that.dropall()


vm >> Command(dup)
vm >> Command(drop)
vm >> Command(swap)
vm >> Command(over)
vm >> Command(press)
vm >> Command(dropall)

## meta

class Meta(Object):
    pass

class Op(Meta):
    def eval(self, ctx):
        if self.val == '`':
            return self.nest[0]
        if self.val in ['@', ':', '<<', '>>', '//', '.']:
            a = self.nest[0].eval(ctx)
            b = self.nest[1].eval(ctx)
        if self.val == '=':
            if len(self.nest) == 2:
                a = self.nest[0].eval(ctx)
                b = self.nest[1].eval(ctx)
                ctx[a.val] = b
                return b
            if len(self.nest) == 3:
                a = self.nest[0].eval(ctx)
                b = self.nest[1].eval(ctx)
                c = self.nest[2].eval(ctx)
                a[b.val] = c
                return c
            raise TypeError(self)
        if self.val in ['@', ':']:
            return a.apply(b, ctx)
        if self.val == '<<':
            return a << b
        if self.val == '>>':
            return a >> b
        if self.val == '//':
            return a // b
        if self.val == '.':
            return a[b.val]
        raise TypeError(self)

class Class(Meta):
    def __init__(self, C):
        if isinstance(C, str):
            Meta.__init__(self, C)
        else:
            Meta.__init__(self, C.__name__.lower())
            self.cls = C

    def apply(self, that, ctx):
        return self.cls(that.val)


vm >> Class(Class)

class Fn(Object):
    pass
class Method(Fn):
    pass


vm >> Class(Method)

class Module(Meta):
    pass


vm >> Class(Module)

class Section(Meta):
    pass


vm >> Class(Section)


## io

class IO(Object):
    pass
class File(IO):
    pass


vm >> Class(File)

## network

class Net(IO):
    pass

class IP(Net):
    pass


vm >> Class(IP)

class Port(Net):
    pass


vm >> Class(Port)

class Email(Net):
    def html_head(self):
        return '&lt;<a href="mailto:%s">%s</a>&gt;' % (self.val,self.val)

class URL(Net):
    def html_head(self):
        return '<a href="%s">%s</a>' % (self.val,self.val)


## lexer

import ply.lex as lex

tokens = ['nl', 'symbol', 'str', 'number', 'integer', 'email', 'url',
          'tick', 'lshift', 'rshift', 'push', 'colon', 'eq', 'dot',
          'lp', 'rp', 'lq', 'rq']

t_ignore = ' \t\r'
t_ignore_comment = r'\#.*'

states = (('str', 'exclusive'),)

t_str_ignore = ''

def t_str(t):
    r'\''
    t.lexer.push_state('str')
    t.lexer.string = ''
def t_str_str(t):
    r'\''
    t.lexer.pop_state()
    t.value = String(t.lexer.string)
    return t
def t_str_any(t):
    r'.'
    t.lexer.string += t.value
def t_str_nl(t):
    r'\n'
    t.lexer.string += t.value

def t_nl(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_tick(t):
    r'`'
    t.value = Op(t.value)
    return t
def t_lshift(t):
    r'<<'
    t.value = Op(t.value)
    return t
def t_rshift(t):
    r'>>'
    t.value = Op(t.value)
    return t
def t_push(t):
    r'//'
    t.value = Op(t.value)
    return t
def t_colon(t):
    r':'
    t.value = Op(t.value)
    return t
def t_eq(t):
    r'='
    t.value = Op(t.value)
    return t
def t_dot(t):
    r'\.'
    t.value = Op(t.value)
    return t

def t_semicolon(t):
    r';'
    return t

def t_lp(t):
    r'\('
    return t
def t_rp(t):
    r'\)'
    return t
def t_lq(t):
    r'\['
    return t
def t_rq(t):
    r'\]'
    return t

def t_number(t):
    r'[+\-]?[0-9]+\.[0-9]+([eE][+\-]?[0-9]+)?'
    t.value = Number(t.value)
    return t
def t_integer(t):
    r'[+\-]?[0-9]+'
    t.value = Integer(t.value)
    return t

def t_email(t):
    r'[a-z]+@([a-z]+\.)+([a-z]+)'
    t.value = Email(t.value)
    return t
def t_url(t):
    r'https?://[^ \t\r\n]+'
    t.value = URL(t.value)
    return t
def t_symbol(t):
    r'[^ \t\r\n\#\:\;\<\>\/\.\(\)\[\]\{\}]+'
    t.value = Symbol(t.value)
    return t

def t_ANY_error(t): raise SyntaxError(t)


lexer = lex.lex()

## parser

import ply.yacc as yacc

def p_REPL_none(p):
    r' REPL : '
def p_REPL_nl(p):
    r' REPL : REPL nl '
def p_REPL_recur(p):
    r' REPL : REPL ex nl '
    print(p[2], file=log)
    print(p[2].eval(vm), file=log)
    print(vm, file=log)
    print('-' * 66, file=log)

def p_op_parens(p):
    r' ex : lp ex rp %prec parens '
    p[0] = p[2]
def p_op_tick(p):
    r' ex : tick ex '
    p[0] = p[1] // p[2]
def p_op_lshift(p):
    r' ex : ex lshift ex '
    p[0] = p[2] // p[1] // p[3]
def p_op_rshift(p):
    r' ex : ex rshift ex '
    p[0] = p[2] // p[1] // p[3]
def p_op_push(p):
    r' ex : ex push ex '
    p[0] = p[2] // p[1] // p[3]
def p_op_colon(p):
    r' ex : ex colon ex '
    p[0] = p[2] // p[1] // p[3]


precedence = (
    ('right', 'eq'),
    # ('nonassoc', 'lvalue'),
    # ('nonassoc', 'rvalue'),
    ('left', 'lshift', 'rshift', 'push'),
    ('left', 'dot'),
    ('left', 'apply'),
    ('nonassoc', 'colon'),
    ('nonassoc', 'tick'),
    ('nonassoc', 'parens'),
)


# def p_op_dot_lvalue(p):
#     r' ex : ex dot ex eq ex %prec lvalue '
#     p[0] = p[4] // p[1] // p[3] // p[5]
# def p_op_dot_rvalue(p):
#     r' ex : ex dot ex %prec rvalue '
#     p[0] = p[2] // p[1] // p[3]
def p_op_assign(p):
    r' ex : ex lq ex rq eq ex '
    p[0] = p[5] // p[1] // p[3] // p[6]
def p_op_eq(p):
    r' ex : ex eq ex '
    p[0] = p[2] // p[1] // p[3]
def p_op_dot(p):
    r' ex : ex dot ex '
    p[0] = p[2] // p[1] // p[3]

def p_apply(p):
    r' ex : ex ex %prec apply '
    p[0] = Op('@') // p[1] // p[2]

def p_ex_symbol(p):
    r' ex : symbol '
    p[0] = p[1]
def p_ex_number(p):
    r' ex : number '
    p[0] = p[1]
def p_ex_integer(p):
    r' ex : integer '
    p[0] = p[1]
def p_ex_str(p):
    r' ex : str '
    p[0] = p[1]
def p_ex_email(p):
    r' ex : email '
    p[0] = p[1]
def p_ex_url(p):
    r' ex : url '
    p[0] = p[1]

def p_error(p): raise SyntaxError(p)


parser = yacc.yacc(debug=False, write_tables=False)


## document

class Doc(Object):
    pass

class Color(Doc):
    pass


vm >> Class(Color)

class Font(Doc):
    pass


vm >> Class(Font)

class Size(Doc, Primitive):
    pass


vm >> Class(Size)


## web

class Web(Net):

    extra_files = []

    def apply(self, that, ctx):

        self.ctx = that

        import flask, flask_wtf, wtforms

        app = flask.Flask(self.val)
        app.config['SECRET_KEY'] = os.urandom(32)

        class CLI(flask_wtf.FlaskForm):
            pad = wtforms.TextAreaField('pad',
                                        render_kw={'rows': 5,
                                                   'autofocus': 'true'},
                                        default='# metaL commands...')
            go = wtforms.SubmitField('Ctrl + Enter',
                                     render_kw={'style': 'btn btn-default'})

        @app.route('/', methods=['GET', 'POST'])
        def index():
            form = CLI()
            if form.validate_on_submit():
                lexer.file = '%s' % form
                parser.parse(form.pad.data + '\n')
            return flask.render_template('index.html', ctx=self.ctx, web=self, form=form)

        @app.route('/css.css')
        def csscss():
            return flask.Response(
                flask.render_template('css.css', web=self), mimetype='text/css')

        @app.route('/<path:path>.css')
        def css(path): return app.send_static_file(path + '.css')

        @app.route('/<path:path>.png')
        def png(path): return app.send_static_file(path + '.png')

        @app.route('/<path:path>.js')
        def js(path): return app.send_static_file(path + '.js')

        def split(path):
            ctx = self.ctx
            for i in path.split('/'):
                if i:
                    ctx = ctx[i]
            return ctx

        @app.route('/g6/<path:path>')
        def g6(path):
            return flask.render_template('g6.html', ctx=split(path), web=self)

        @app.route('/dump/<path:path>')
        def dump(path):
            return flask.render_template('dump.html', vm=vm, ctx=split(path), web=self)

        @app.route('/<path:path>')
        def path(path):
            return flask.render_template('html.html', vm=vm, ctx=split(path), web=self)

        app.run(host=self['ip'].val, port=self['port'].val,
                debug=True, extra_files=Web.extra_files)


vm >> Class(Web)

## rosatom

class RA(Object):
    def html_head(self): return '<h1>%s</h1>\n' % self.val

vm >> Class(RA)

class ГОСТ(RA):
    def html_head(self): return '<p><b>ГОСТ %s</b>\n' % self.val

vm >> Class(ГОСТ)

class Название(RA):
    def html_head(self): return '<i>%s</i>\n' % self.val

vm >> Class(Название)

class ОКС(RA):
    def html_head(self): return '<b>ОКС:%s</b>\n' % self.val

vm >> Class(ОКС)

## init

def init():
    for srcfile in sys.argv[1:]:
        Web.extra_files.append(srcfile)
        with open(srcfile) as src:
            lexer.file = srcfile
            parser.parse(src.read())


if __name__ == '__main__':
    init()
