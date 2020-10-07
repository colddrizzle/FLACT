# coding=utf-8
from common.BNFParser import *
from common.Grammar import Grammar

# 纯终结符句型
# pure terminal sentential form
def isPTSF(p, T=[]):
    """
    >>> from common.production import Production
    >>> p = Production(['A'], [['\\"a\\"', '\\"b\\"'],['\\"cde\\"']])
    >>> isPTSF(p)
    True

    >>> p = Production(['A'], [['\\"a\\"', '\\"b\\"'],['\\"cde\\"']])
    >>> isPTSF(p, ['a', 'b', 'c', 'd', 'e'])
    True

    >>> p = Production(['A'], [['\\"a\\"', '\\"b\\"'],['\\"cde\\"']])
    >>> isPTSF(p, ['a'])
    False

    >>> p = Production(['A'], [['a', 'b'],['Ade']])
    >>> isPTSF(p)
    False
    """
    for opt in p.right:
        for symbol in opt:
            if not isLiteralValue(symbol, T):
                return False
    return True


# 删除派生不出只有终极符号行的变量

def algo_6_1(G):
    """
    测试数据来源于例6-4
    >>> from common.Grammar import Grammar
    >>> from common.production import Production
    >>> p1 = Production(['S'], [['A', 'B'],['\\"a\\"'],['B','B']])
    >>> p2 = Production(['A'], [['\\"a\\"']])
    >>> p3 = Production(['C'], [['\\"b\\"'], ['A', 'B', '\\"a\\"']])
    >>> g = Grammar(['S', 'A', 'B', 'C'], ['a', 'b'], [p1,p2,p3], ['S'])
    >>> _g = algo_6_1(g)
    >>> _g.V == set(['S', 'A', 'C'])
    True
    >>> _g.T == set(['a', 'b'])
    True
    """
    simple_plist = []
    for p in G.P:
        simple_plist.extend(Production.toSimpleProduction(p))

    old_v = set()
    new_v = set()
    # init new_v
    for p in simple_plist:
        if isPTSF(p, G.T):
            new_v.add(p.left[0])
    
    while old_v != new_v:
        old_v = new_v
        for p in simple_plist:
            ss = set()
            ss |= set(G.T)
            ss |= old_v

            if isFormedBy(p.right, ss):
                new_v.add(p.left[0])
    
    new_p = []
    for p in simple_plist:
        ss = set()
        ss |= set(G.T)
        ss |= new_v

        if isFormedBy(p.left, new_v) and \
            isFormedBy(p.right, ss):
            new_p.append(p)

    return Grammar(new_v, G.T, new_p, G.S)

