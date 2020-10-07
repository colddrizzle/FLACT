# coding=utf-8

from common.BNFParser import *
from common.production import *

from FLAAT.ch6.algo_6_3 import algo_6_3
from algo_4_2 import algo_4_2
from algo_4_3 import algo_4_3

def canBeEmpty(beta, UV, V):
    if len(beta) == 0:
        return True
    for s in beta:
        if not isVariable(s, V):
            return False
        elif s not in UV:
            return False
    return True

#求语法变量的Follow集合
#我们按照先遍历P的方法来实现

def algo_4_4(G):
    """
    >>> G = parse_grammar("test/CPAT/algo_4_4.txt")
    >>> F = algo_4_4(G)
    >>> F['E'] == F['E1']
    True
    >>> F['E'] == set([')', '#'])
    True

    >>> F['T'] == F['T1']
    True
    >>> F['T'] == set([')', '#', '+'])
    True
    >>> F['F'] == set([')', '#', '+', '*'])
    True
    """
    UV = algo_6_3(G.P)
    FV = algo_4_2(G)

    #转为简单产生式
    simple_plist = []
    for p in G.P:
        simple_plist.extend(Production.toSimpleProduction(p))

    FOLLOW = {}
    # 初始化各个First
    for X in G.V:
        if X not in FOLLOW:
            FOLLOW[X] = set()
    FOLLOW[G.S].add('#')

    changed = True
    while changed:
        changed = False
        for p in simple_plist:
            for i in range(len(p.right[0])):
                s = p.right[0][i]
                if s in G.V:
                    beta = p.right[0][i+1:]
                    
                    pre = len(FOLLOW[s])
                    
                    beta_first = algo_4_3(beta, FV)
                    FOLLOW[s] |= (beta_first - set([EMPTY_SYMBOL_UNI]))
                    #判断beta是否可空
                    if canBeEmpty(beta, UV, G.V):
                        FOLLOW[s] |= FOLLOW[p.left[0]]
                    
                    post = len(FOLLOW[s])
                    if post > pre:
                        changed = True
    return FOLLOW