# coding=utf-8

import itertools

from common.BNFParser import *
from common.Grammar import Grammar

# 引理6-1的代换
# p是简单产生式
# P1里都是简单产生式
def replace_6_1(need_replace, P1):
    for p in need_replace:
        P1.remove(p)
        h = p.right[0][0]
        rest = p.right[0][1:]
        new_p = set()
        for p1 in P1:
            if p1.left[0] == h:
                new_p.add(Production(p.left, [p1.right[0]+rest]))
        P1 |= new_p
    
# 引理6-2的代换
# 新引入的变量命名为B1、B2...，为了与例6-7保持一致
NEW_B_COUNT = 1

def replace_6_2(recursive, non_recursive, P, V, N_V):
    global NEW_B_COUNT
    new_v = "B"+str(NEW_B_COUNT)
    NEW_B_COUNT += 1

    V.add(new_v)
    N_V.append(new_v)
    for p in recursive:
        rest = p.right[0][1:]
        P.remove(p)
        P.add(Production([new_v], [rest]))
        P.add(Production([new_v], [rest +[new_v]]))
    for p in non_recursive:
        P.add(Production(p.left, [p.right[0]+[new_v]]))

def simplify(P):
    simple_plist = []
    for p in P:
        simple_plist.extend(Production.toSimpleProduction(p))
    return simple_plist

# 任意CFG转格雷巴赫范式
# 为了方便应用例6-7进行测试
# 算法中新引入的变量的命名遵循例6-7的做法

# 教程上的算法是由P1到P2到P3，三个集合，
# 实现起来比较麻烦，而且很容易搞不清楚一些产生式应该取自那个集合
# 我们的实现中是通过不断往P1中增删产生式实现的 结合例6-7更好理解

def algo_6_4(G):
    """
    >>> G = parse_grammar('test/FLAAT/algo_6_4.txt')
    >>> expected_p = parse_file('test/FLAAT/algo_6_4_r.txt')
    >>> G1 = algo_6_4(G)
    >>> expected_p = simplify(expected_p)
    >>> P1 = simplify(G1.P)
    >>> set(expected_p) == set(P1)
    True
    """
    
    V1 = set(G.V)
    P1 = set()
    
    simple_plist = simplify(G.P)
    # step 1
    # 引入新变量的方法就是将终结符所有字符改成大写形式
    # 注意需要去掉终结符的引号
    for p in simple_plist:
        t = set(sum(p.right, []))
        if t < set(G.V) or \
            (len(t) == 1 and t < set(G.T)) or \
                (p.right[0][0] in set(G.T) and set(p.right[0][1:]) < set(G.V)):
                P1.add(p)
        else:
            opt = []
            for t in p.right[0]:
                if t in G.T:
                    v = t[1:-1].upper()
                    opt.append(v)
                    P1.add(Production([v], [[t]]))
                    V1.add(v)
                else:
                    opt.append(t)
            p.right = [opt]
            P1.add(p)

    # step 2
    sorted_V = list(V1)
    sorted_V.sort()
    N_V= []
    for k in range(len(sorted_V)):
        for j in range(k):
            need_replace = []
            for p in P1:
                if p.left[0] == sorted_V[k] and \
                    p.right[0][0] == sorted_V[j]:
                    need_replace.append(p)
            replace_6_1(need_replace, P1)

        # 消除左递归
        recursive = []
        non_recursive = []
        for p in P1:
            # p是简单产生式，右部选项只有一个
            if p.left[0] ==  sorted_V[k]:
                if p.right[0][0] == sorted_V[k]:
                    recursive.append(p)
                else:
                    non_recursive.append(p)
        if recursive:
            replace_6_2(recursive, non_recursive, P1, V1, N_V)
        
    # step 3
    k_range = range(len(sorted_V))
    k_range.reverse()
    k_range = k_range[1:]
    for k in k_range:
        need_replace = []
        for p in P1:
            if p.left[0] == sorted_V[k] and \
                isVariable(p.right[0][0], V1) and \
                p.right[0][0] > sorted_V[k]:
                need_replace.append(p)
        if need_replace:
            replace_6_1(need_replace, P1)

    for k in range(len(N_V)):
        need_replace = []
        for p in P1:
            if p.left[0] == N_V[k] and \
                isVariable(p.right[0][0], V1):
                need_replace.append(p)
        if need_replace:
            replace_6_1(need_replace, P1)
    return Grammar(V1, G.T, P1, G.S)