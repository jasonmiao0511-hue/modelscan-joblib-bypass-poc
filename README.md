# modelscan Joblib Bypass PoC

## Summary

Demonstrates that `modelscan` (<= 0.8.5) can be bypassed by malicious `.joblib` files
because `marshal` and `types` modules are missing from its `unsafe_globals` blacklist.

## Affected

- modelscan <= 0.8.5
- joblib >= 0.10

## Reproduction

```bash
pip install modelscan joblib

# Step 1: scan reports "No issues" (BYPASSED)
modelscan scan -p rce.joblib

# Step 2: loading the file executes arbitrary code
python -c "import joblib; joblib.load('rce.joblib')"
# Check: cat pwned_p4.txt  ->  PWNED_P4
```

## Files

- `rce.joblib` — Malicious joblib PoC file (~270 bytes)
- `rce_joblib.py` — Generator script
- `README.md` — This file

## Vulnerability Class

This is the same root cause as our previously reported pickle bypass (2026-05-14),
extending the attack surface to `.joblib` format (widely used in scikit-learn,
Dask, and Ray pipelines).

## Suggested Fix

Add to modelscan `unsafe_globals` blacklist:
- `marshal.loads`
- `types.FunctionType`
- `types.CodeType`
- `builtins.eval`
- `builtins.exec`

Long-term: switch from blacklist to whitelist for global imports in serialized files.

## Disclosure

- Discovered by: jasonmiao0511-hue
- Reported via: huntr.com Model Format Vulnerability Form
- Date: 2026-06-14
