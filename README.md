# readable-number
A Python library to print numbers in human readable format

## 1. Installation

```
pip install readable-number
```

This library does not depend on any third-party libraries, so installing it will not break your Python environment.

## 2. Usage

```python
from readable_number import ReadableNumber

# Print digit in groups
str(ReadableNumber(-123))  # -123
str(ReadableNumber(-1234))  # -1,234
str(ReadableNumber(-123456789))  # -123,456,789
str(ReadableNumber(-12345.6789))  # -12,345.6789
str(ReadableNumber(-1.23456e18))  # -1,234,560,000,000,000,000

# Custom grouping (in other locales)
str(ReadableNumber(-123456789, digit_group_size=4))  # -1,2345,6789
str(ReadableNumber(-123456789, digit_group_delimiter='|'))  # -123|456|789

# Convert to human-readable shortform (with k, M, B, and T as unit)
str(ReadableNumber(12345, use_shortform=True))  # 12k
str(ReadableNumber(12345, use_shortform=True, precision=1))  # 12.3k
str(ReadableNumber(12345678, use_shortform=True))  # 12M
str(ReadableNumber(12345678, use_shortform=True, precision=2))  # 12.35M

# Numbers with small absolute values
str(ReadableNumber(0.12345))  # 0.12345
str(ReadableNumber(0.0000012345))  # 0.0000012345
str(ReadableNumber(0.12345, precision=None))  # 0.12345
str(ReadableNumber(0.12345, precision=2))  # 0.12
str(ReadableNumber(0.12345, precision=20))  # 0.123450000000000

# Digits beyond double-precision limit are discarded
str(ReadableNumber(0.12345678901234567890, precision=90))  # 0.123456789012346
str(ReadableNumber(1.23e-20, precision=90))  # 0.000000000000000

# Print large/small numbers in exponantial notation
str(ReadableNumber(1234567890, use_exponent_for_large_numbers=True))  # 1.234568e+09
str(ReadableNumber(0.000000012, use_exponent_for_small_numbers=True))  # 1.200000e-08
```

## 3. Full API documentation

Please visit this site: https://readable-number.readthedocs.io/en/stable/
