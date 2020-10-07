# coding=utf-8

# 解析形如 α -> β 的标准bnf产生式
# 终结符或语法变量之间必须使用空格隔开
# 不支持各种扩展变体

# V T分别表示语法变量与终结符
# 若未指定，则用如下约定：

# 语法变量由大写英文字母开头，直到遇到空格为止

# 小写希腊字母表示句型（句型可能全是语法变量，也可能全是终结符）

# 所有的字面量都用单引号括起来

# 终结符是只含有一个字符的字面量


from production import Production
from Grammar import Grammar

# 如果有提供V，则查看是否在V中
# 如果V为空，则按照上面约定判定

def isVariable(symbol, V=[]):
    """
    >>> isVariable("Start")
    True
    >>> isVariable("A_123", ["Start"])
    False

    >>> isVariable("A_123", ["Start", "A_123"])
    True
    """
    if V:
        return symbol in V
    return symbol[0].isupper()

# 如果有提供T，则查看是否在T中
# 如果T为空，则按照上面约定判定 

def isTerminal(symbol, T=[]):
    """
    >>> isTerminal("bracket")
    False

    >>> isTerminal("\\'0\\'")
    True

    >>> isTerminal("bracket", ["hello"])
    False

    >>> isTerminal("\\'bracket\\'", ["hello", "bracket"])
    False

    >>> isTerminal("\\'a\\'")
    True

    >>> isTerminal("a")
    False
    """
    if T:
        return symbol in T
    if isLiteralValue(symbol) and len(symbol) == 3:
        return True
    return False

# 用引号包裹的是字面量

def isLiteralValue(symbol, T=[]):
    """
    >>> isLiteralValue("'123'")
    True

    >>> isLiteralValue("'123")
    False

    >>> isLiteralValue("abc")
    False

    >>> isLiteralValue("\\'abc\\'", ["\\'a\\'","\\'b\\'","\\'c\\'"])
    True

    >>> isLiteralValue("\\'abc\\'", ["\\'a\\'","\\'b\\'"])
    False

    >>> isLiteralValue('0')
    False

    >>> isLiteralValue("\\'123\\"")
    False
    """
    if symbol[0] != symbol[-1]:
        return False
    if symbol[0] == "'" or symbol[0]=='"':
        if T:
            sT = set([x[1:-1] for x in T])
            if set(list(symbol[1:-1])) <= sT:
                return True
            else:
                return False
        return True
    return False


def kind(symbol, V=[], T=[]):
    """
    >>> kind("Start")
    'V'
    >>> kind("\\'a\\'")
    'T'
    >>> kind("\\'123\\'")
    'L'
    >>> kind("123")
    Traceback (most recent call last):
        ...
    Exception: unknown symbol kind
    """
    if isVariable(symbol, V):
        return "V"
    elif isTerminal(symbol, T):
        return "T"
    elif isLiteralValue(symbol):
        return "L"
    else:
        raise Exception("unknown symbol kind")


def isFormedBy(part, symbol_set):
    """
    >>> from production import Production
    >>> p = Production(['A'], ['A', 'b', 'C'])
    >>> isFormedBy(p.right, ['A', 'b', 'C', 'd'])
    True
    >>> isFormedBy(p.right, ['A', 'B', 'C', 'd'])
    False
    """
    for option in part:
        for symbol in option:
            if symbol not in symbol_set:
                return False
    return True


# bnf必须是utf-8编码

def parse(bnf):
    """
    >>> parse("A -> B C a 'a'")
    ['A']->[['B', 'C', 'a', "'a'"]]

    >>> parse("A -> B C | D E")
    ['A']->[['B', 'C'], ['D', 'E']]
    """
    left, right = bnf.strip().split("->")
    left_parts = left.strip().split(" ")
    right_parts = []
    # 虽然有可能会出现字面量'|'，但是我们忽略这种情况
    # 我们的产生式是严格检查过的 仅供实验性质
    options = []
    if right.find("|") > 0:
        options = right.strip().split("|")
    else:
        options.append(right)
    for option in options:
        parts = option.strip().split(" ")
        right_parts.append(parts)
    return Production(left_parts, right_parts)


def parse_file(filepath):
    productions = []
    with open(filepath, "r") as fin:
        for line in fin:
            if line:
                productions.append(parse(line))
    return productions

def parse_grammar(filepath):
    P = []
    V = set()
    T = set()
    S = set()
    with open(filepath, "r") as fin:
        for line in fin:
            if line:
                p = parse(line)
                V |= set(p.right_variables())
                T |= set(p.right_terminals())
                if not S:
                    S |= set(p.left)
                P.append(p)
    return Grammar(V, T, P, S)