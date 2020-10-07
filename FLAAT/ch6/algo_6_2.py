# coding=utf-8
from common.BNFParser import *
from common.Grammar import Grammar

# 删除不能从开始符号派生出的变量
def algo_6_2(G):
    """
    测试数据来源于例6-4
    >>> from common.Grammar import Grammar
    >>> from common.production import Production
    >>> p1 = Production(['S'], [['A', 'B'],['\\"a\\"'],['B','B']])
    >>> p2 = Production(['A'], [['\\"a\\"']])
    >>> p3 = Production(['C'], [['\\"b\\"'], ['A', 'B', '\\"a\\"']])
    >>> g = Grammar(['S', 'A', 'B', 'C'], ['\\"a\\"', '\\"b\\"'], [p1,p2,p3], ['S'])
    >>> _g = algo_6_2(g)
    >>> _g.V == set(['S', 'A', 'B'])
    True
    >>> _g.T == set(['\\"a\\"'])
    True
    """

    old_v = set()
    old_t = set()

    new_v = set(G.S)
    new_t = set()

    for p in G.P:
        if set(p.left) == G.S:
            for opt in p.right:
                vs = set(opt) & G.V
                new_v |= vs
    
                ts = set(opt) & G.T
                new_t |= ts

    while old_v != new_v or old_t != new_t:
        old_v = new_v
        old_t = new_t

        for p in G.P:
            if set(p.left) <= old_v:
                for opt in p.right:
                    vs = set(opt) & G.V
                    new_v |= vs

                    ts = set(opt) & G.T
                    new_t |= ts
    # 转为简单产生式
    simple_plist = []
    for p in G.P:
        simple_plist.extend(Production.toSimpleProduction(p))

    new_p = []
    for p in simple_plist:
        if set(p.left) <= new_v and \
            set(p.right[0]) <= (new_v | new_t):
            new_p.append(p)

    return Grammar(new_v, new_t, new_p, G.S & new_v)