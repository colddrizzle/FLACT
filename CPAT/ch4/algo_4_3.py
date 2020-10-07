# coding=utf-8

from common.production import EMPTY_SYMBOL, EMPTY_SYMBOL_UNI
from common.BNFParser import *
from algo_4_2 import algo_4_2

#求句型的First集合
# 要求是utf-8编码

#算法大致步骤
# 一次检查句型中各个字符，知道遇到终结符或非可空语法变量为止
#
#

# sf 句型
# FV 各变量First集

def algo_4_3(sf,FV):
    """
    >>> G = parse_grammar("test/CPAT/algo_4_2.txt")
    >>> FV = algo_4_2(G)
    >>> F = algo_4_3(['"("', 'E', '")"'], FV)
    >>> F == set(['('])
    True

    """
    F = set()
    V = FV.keys()
    
    for s in sf:
        if isVariable(s, V):
            if EMPTY_SYMBOL_UNI in FV[s]:
                F |= (FV[s]- set([EMPTY_SYMBOL_UNI]))
            else:
                F |= FV[s]
                break
        else:
            assert s[0] == s[-1]
            assert s[0] == "'" or s[0] == '"'

            s = s[1:-1] #字面量 去除引号
            F.add(s[0]) #取第一个符号作为首终结符
            break
    return F