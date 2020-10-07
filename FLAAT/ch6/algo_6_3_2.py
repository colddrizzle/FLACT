# coding=utf-8

import itertools
import copy

from common.BNFParser import *
from common.Grammar import Grammar

# 去除G的单一产生式。 教程上只给出基本原理
# 
# 基本原理很简单，找出所有单一产生式，代换就可以了

# 但要注意，每应用一次代换，就消灭了一条单一产生式，但也可能增加
# 一条单一产生式，比如 S->AB|B  B->CD|E E -> F|GH
# 若是先应用B -> CD|E到S，则消灭了S -> B, 但产生了S -> E
# 为了避免这种情况，需要从低向上代换，先应用E->F|GH到B

# 但是当单一产生式同时还存在环的时候，就不存在最低的符号
# 这时候需要人为指定一个最低符号，然后逐步代换直到产生形如A -> A的产生式
# 然后删掉这种产生式

# 若是不按照这种顺序，每次代换之后都需要重新计算单一产生式
# 重新计算也很简单，因为新生成的单一产生式是由代换产生的，很容易将其找出来

# 这种思路处理环的问题就是，每次单一产生式的集合里先删除直接循环推导，就是形如A->A的推导

# 我们的算法按照第二种思路来

# 现给出完整的大致算法：
# 1. 找出所有单一产生式
# 2. 对每个单一产生式A -> B
#    若有以B为左部的产生式，用B的所有右部去代换A -> B中的B
#       若B本身也是单一产生式的左部，则添加新的单一产生式A -> B的右部的那个单一符号
#    若没有，则什么也不做


# 该算法只跟G的P有关系
# 另外注意该算法没有使用简单产生式

def is_singles(p, singles, single_vlist):
    for item in singles:
        if p == item[0]:
            single_vlist.extend(copy.copy(item[1]))
            return True
    return False


def algo_6_3_2(P):
    """
    >>> P = parse_file('test/FLAAT/t1_algo_6_3_2.txt')
    >>> new_P = algo_6_3_2(P)
    >>> e_p = parse_file("test/FLAAT/t1_algo_6_3_2_r.txt")
    >>> set(new_P) == set(e_p)
    True

    第二个例子包含循环推导的测试
    >>> P = parse_file('test/FLAAT/t2_algo_6_3_2.txt')
    >>> new_P = algo_6_3_2(P)
    >>> e_p = parse_file("test/FLAAT/t2_algo_6_3_2_r.txt")
    >>> set(new_P) == set(e_p)
    True
    """

    # 找出所有的单一产生式 记录其单一的右部符号
    # 右部的单一符号可能有多个
    singles = []
    for p in P:
        ss = [] # single symbol
        for opt in p.right:
            if len(opt) == 1 and isVariable(opt[0]):
                ss.append(opt[0])
        if ss:
            singles.append((p, ss))

    #构造语法变量到产生式的映射
    v_o_map = dict()
    for p in P:
        if p.left[0] not in v_o_map:
            v_o_map[p.left[0]]=[p]
        else:
            v_o_map[p.left[0]].append(p)

    while singles:
        item = singles[0]
        del singles[0]
        p = item[0]

        for single_v in item[1]:
            # 如果item[1]有作为左部的产生式 则代换
            if single_v in v_o_map:

                # 找出p中需要代换的位置应用代换
                while True:
                    replace_i = -1

                    for i in range(len(p.right)):
                        opt = p.right[i]
                        if len(opt) == 1 and opt[0] == single_v:
                            replace_i = i
                            break
                    
                    if replace_i <0:# 没有需要代换的位置
                        break
                    else:
                        # 整合产生式右部，并添加新的单一产生式
                        replacement = []
                        new_single = False
                        single_vlist = [] #_p若是单一产生式，其右部的单一变量  
                        for _p in v_o_map[single_v]:
    
                            # 如果应用的产生式本身也是单一产生式
                            # 则会导致出现新的单一产生式

                            # 若新的单一产生式是直接循环推导产生式，
                            # 则将直接循环推导那个选项删去  且不再加入单一产生式
                            # 否则将新的单一产生式加入到singles中
                             
                                            
                            if is_singles(_p, singles, single_vlist):
                                new_single = True
                                #检查是否导致直接循环推导产生式
                                if p.left[0] in single_vlist:#会导致直接循环推导
                                    if len(single_vlist) == 1:
                                        # 如果_p的右部单一变量只有一个且是导致直接循环推导的变量
                                        # 则删掉它之后不再添加新产生的单一产生式
                                        new_single = False
                                    for opt in _p.right:
                                        if not( len(opt) == 1 and opt[0] == p.left[0] ) :
                                            replacement.append(opt)
                                        
                                else:

                                    replacement += _p.right
                            else:
                                replacement += _p.right

                        #应用代换，但同时去除相同的右部选项

                        #p.right = p.right[:i] + replacement + p.right[i+1:]
                        new_right = p.right[:i]
                        for opt in replacement+p.right[i+1:]:
                            if opt not in new_right:
                                new_right.append(opt)
                        p.right = new_right
                        
                        if new_single:
                            _single_vlist = [ v for v in single_vlist if v!=p.left[0] ]
                            singles.append((p, _single_vlist))
    return P

                
