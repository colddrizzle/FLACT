class Grammar(object):
    def __init__(self, V, T, P, S):
        self._V = set(V) 
        self._T = set(T)
        self._P = P 
        self._S = set(S) 

    @property
    def V(self):
        return self._V 
    
    @property
    def T(self):
        return self._T

    @property
    def P(self):
        return self._P 

    @property
    def S(self):
        return self._S