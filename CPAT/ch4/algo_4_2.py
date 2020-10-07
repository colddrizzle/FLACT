# coding=utf-8 

from common.BNFParser import *
from common.production import *
from FLAAT.ch6.algo_6_3 import algo_6_3

# 求所有语法变量的First集
# 需要利用algo_6_3来求可空变量集

def algo_4_2(G):
    """
    >>> 
    >>> 
    
    """

    UV = algo_6_3(G.P)

    #转为简单产生式
    simple_plist = []
    for p in G.P:
        simple_plist.extend(Production.toSimpleProduction(p))

    FIRST = {}
    # 初始化各个First
    for X in G.V:
        if X in FIRST:
            pass
        else:
            FIRST[X] = set()

    #迭代直到各First不再发生变化
    changed = True
    while changed:
        changed = False
        for p in simple_plist:
            X = p.left[0]
            is_all_UV = True
            for s in p.right[0]:
                # 我们的BNF产生式允许出现字面量，而终结符是字面量的一种
                # 这里应该用是否字面量来判断
                if isLiteralValue(s, G.T):
                    is_all_UV = False
                    # 字面量带有引号，当取下标为1的字符为首终结符
                    # 这样取的终结符不带有引号
                    pre = len(FIRST[X])
                    FIRST[X].add(s[1])
                    post = len(FIRST[X])
                    if post > pre:
                        changed = True
                    break
                elif isVariable(s, G.V):
                    if s not in UV:
                        is_all_UV = False
                        pre = len(FIRST[X])
                        FIRST[X] |= FIRST[s]
                        post = len(FIRST[X])
                        if post > pre:
                            changed = True
                        break
                    else:
                        pre = len(FIRST[X])
                        FIRST[X] |= (FIRST[s] -  set(EMPTY_SYMBOL))
                        post = len(FIRST[X])
                        if post > pre:
                            changed = True
            if is_all_UV:
                FIRST[X].add(EMPTY_SYMBOL)

    return FIRST
                
