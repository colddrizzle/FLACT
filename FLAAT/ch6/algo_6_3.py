# coding=utf-8
from common.BNFParser import *
from common.Grammar import Grammar

# 求文法G的可空变量集
# 该算法只跟G的P有关系
def algo_6_3(P): 
    """
    测试数据来源于第6章习题12(2)

    >>> from common.production import Production
    >>> p1 = Production(['S'], [['A', 'B', 'D', 'C']])
    >>> p2 = Production(['A'], [['B', 'D'], ['\\"a\\"', '\\"a\\"'], ['\\"ε\\"']])
    >>> p3 = Production(['B'], [['\\"a\\"', 'B'], ['\\"a\\"']])
    >>> p4 = Production(['C'], [['D','C'], ['\\"c\\"'], ['\\"ε\\"']])
    >>> p5 = Production(['D'], [['\\"ε\\"']])
    >>> p = [p1, p2, p3, p4, p5]
    >>> u = algo_6_3(p)
    >>> set(u) == set(['A', 'C', 'D'])
    True
    """
    simple_plist = []
    for p in P:
        simple_plist.extend(Production.toSimpleProduction(p))

    old_u = set()
    new_u = set()
    for p in simple_plist:
        if Production.isDirectEmpty(p):
            new_u.add(p.left[0])
    
    while new_u != old_u:
        old_u = new_u
        for p in simple_plist:
            if set(p.right[0]) <= old_u:
                new_u.add(p.left[0])
    
    return new_u
