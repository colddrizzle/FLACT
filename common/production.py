# coding=utf-8
import hashlib
import BNFParser

EMPTY_SYMBOL = 'ε'

class Production(object):
    def __init__(self, left, right):
        self._left = left
        self._right = right
    
    @property
    def left(self):
        return self._left
    
    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value

    def __repr__(self):
        return repr(self._left)+"->"+repr(self._right)

    def __hash__(self):
        # sum(self._right, [])将二维变为一维
        return hash(tuple(self._left + sum(self._right, [])))

    def __eq__(self, other):
        """
        >>> p1 = Production(['A'], [['Ab', '\\"c\\"', 'D'], ['\\"a\\"', 'B', 'CD']])
        >>> p2 = Production(['A'], [['Ab', '\\"c\\"', 'D'], ['\\"a\\"', 'B', 'CD']])
        >>> p1 == p2
        True
        """
        return self.__hash__() == other.__hash__()

    def right_variables(self, V = []):
        """
        >>> p = Production(['A'], [['Ab', '\\"c\\"', 'D'], ['\\"a\\"', 'B', 'CD']])
        >>> r = p.right_variables()
        >>> r == ['Ab', 'D', 'B', 'CD']
        True
        """
        r = []
        for opt in self._right:
            for t in opt:
                if BNFParser.isVariable(t, V):
                    r.append(t)
        return r

    def right_terminals(self, T = []):
        """
        >>> p = Production(['A'], [['Ab', '\\"c\\"', 'D'], ['\\"a\\"', 'B', 'CD']])
        >>> r = p.right_terminals()
        >>> r == ['\\"c\\"', '\\"a\\"']
        True
        """
        r = []
        for opt in self._right:
            for t in opt:
                if BNFParser.isTerminal(t, T):
                    r.append(t)
        return r

    def first_symbols(self):
        """
        >>> p = Production(['A'], [['Ab', '\\"c\\"', 'D'], ['\\"a\\"', 'B', 'CD']])
        >>> r = p.first_symbols()
        >>> r == ['Ab', '\\"a\\"']
        True
        """
        r = []
        for opt in self._right:
            r.append(opt[0])
        return r

    @staticmethod
    def merge(one, another):
        """
        >>> pr = Production(['A'], [['Ab', 'c', 'D'], ['a', 'B', 'CD']])
        >>> p1 = Production(['A'], [['Ab', 'c', 'D']])
        >>> p2 = Production(['A'], [['a', 'B', 'CD']])
        >>> r = Production.merge(p1, p2)
        >>> r == pr
        True
        """
        if one.left != another.left:
            raise Exception("can't merge productions")
        return Production(one.left, one.right + another.right)

    #简单产生式 不包含选择符号 | 
    @staticmethod
    def toSimpleProduction(p):
        plist = []
        for opt in p.right:
            plist.append(Production(p.left, [opt]))
        return plist
    
    #判断是否直接推出空的产生式
    @staticmethod
    def isDirectEmpty(p):
        """
        >>> p = Production(['A'], [['\\"ε\\"']])
        >>> Production.isDirectEmpty(p)
        True
        """
        if len(p.right)==1 and len(p.right[0])==1:
            if p.right[0][0] == "'"+EMPTY_SYMBOL+"'" or  p.right[0][0] == '"'+EMPTY_SYMBOL+'"':
                return True
        return False 

