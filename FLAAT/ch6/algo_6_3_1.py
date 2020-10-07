# coding=utf-8

import itertools

from common.BNFParser import *
from common.Grammar import Grammar

from FLAAT.ch6.algo_6_3 import algo_6_3

# 去除G的空产生式。 教程上只求了可空变量集， 
# 给出去空产生式的算法仅在定理6-7的证明开头提了提了一下。
# 现给出完整算法：
# 1. 将所有产生式处理为简单产生式
# 2. 求出可空变量集U
# 3. 删除直接导出ε的产生式
# 4. 应用定理6-7证明中前部分的过程
#     对所有 A -> X1 X2 X3 .. Xm 属于P，将A -> a1 a2 a3 ...am 放入NEW_P中
#     如果Xi属于可空变量集U，则ai=Xi或ai = ε
#     否则 ai = Xi
#     同一个产生式中，a1 a2 ... am不可同时为ε

# 该算法只跟G的P有关系

def algo_6_3_1(P): 
    """
    测试数据使用6.2.2节文法G1
    >>> from common.production import Production
    >>> p1 = Production(['S'], [['\\"0\\"', 'S', '\\"1\\"']])
    >>> p2 = Production(['S'], [['\\"0\\"', 'A', '\\"1\\"']])
    >>> p3 = Production(['S'], [['\\"0\\"', '\\"1\\"']])
    >>> p4 = Production(['A'], [['\\"2\\"', 'A']])
    >>> p5 = Production(['A'], [['\\"ε\\"']])
    >>> P = [p1, p2, p3, p4, p5]
    >>> new_P = algo_6_3_1(P)
    >>> p6 = Production(['A'], [['\\"2\\"']])
    >>> set(new_P) == set([p1, p2, p3, p4, p6])
    True
    """

    simple_plist = []
    for p in P:
        simple_plist.extend(Production.toSimpleProduction(p))

    u = algo_6_3(P)

    new_p = set()
    for p in simple_plist:
        if Production.isDirectEmpty(p):
            continue
        
        # 求出当前产生式右部的所有可空变量的下标
        # 以及这些可空变量的所有组合    
        # 注意由于右边可能会多次出现相同的可空变量，因此要求下标
    
        ui_in_p = []
        for i in range(len(p.right[0])):
            if p.right[0][i] in u:
                ui_in_p.append(i)

        # 如果可空变量为空，则直接加入
        if not ui_in_p:
            new_p.add(p)
            continue

        #求这些下标的所有组合 除了全选的那种组合之外   
        slots_list = []
        for i in range(len(ui_in_p)):
            slots_list.extend(itertools.combinations(ui_in_p, i))
        
        # 对每种可空变量组合，从当前产生式右部中敲掉这些变量。
        # 敲除可空变量的过程可能会产生相同的产生式
        # 比如 S -> AABC A是可空变量 但我们定义了Production的hash方法，set会自动去重

        for slots in slots_list:
            right = []
            for i in range(len(p.right[0])):
                if i not in slots:
                    right.append(p.right[0][i])
            new_p.add(Production(p.left, [right]))

        #只有产生式右部有非可空变量或者给空终结符的时候，才可以全部删除可空变量
        if len(p.right[0]) > len(ui_in_p):
            right = []
            for i in range(len(p.right[0])):
                if i not in ui_in_p:
                    right.append(p.right[0][i])
            new_p.add(Production(p.left, [right]))

    return list(new_p)
