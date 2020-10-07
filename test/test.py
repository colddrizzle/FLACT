"""
run test:
cd FLAAT
python -m test.test

or in VsCode, Run config TestAll

"""
import doctest
import importlib


MODULES = [
# common            
'common.BNFParser',
'common.production',

# FLAAT charpter 6        
'FLAAT.ch6.algo_6_1',
'FLAAT.ch6.algo_6_2',
'FLAAT.ch6.algo_6_3',
'FLAAT.ch6.algo_6_3_1',
'FLAAT.ch6.algo_6_3_2',
'FLAAT.ch6.algo_6_4',

# CPAT charpter 4
'CPAT.ch4.algo_4_2',
'CPAT.ch4.algo_4_3',
'CPAT.ch4.algo_4_4'
]

def test_all(mod_list):
    for mod_name in mod_list:
        mod = importlib.import_module(mod_name)
        r = doctest.testmod(mod, verbose = True)
        if r.failed > 0:
            break

if __name__ == "__main__":
    test_all(MODULES)
