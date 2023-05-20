# readable-number

A Python library to print numbers in human readable format

## 1. Installation

```
pip install readable-number
```

This library does not depend on any third-party libraries, so installing it will not break your Python environment.

## 2. Usage

### 2.1. Import and basic usage


```python
from readable_number import ReadableNumber

str(ReadableNumber(-1.23))  # -1.23
str(ReadableNumber(-123))  # -123
```

Print many numbers with the same config:

```python
rn = ReadableNumber(precision=2, digit_group_size=4)
rn.of(123456789)  # 1,2345,6789
rn.of(0.123456789)  # 0.12
rn.of(1e15)  # 1000,0000,0000,0000
```

### 2.2. Print large integers

#### 2.2.1. Print in groups


```python
str(ReadableNumber(-123))  # -123
str(ReadableNumber(-1234))  # -1,234
str(ReadableNumber(-123456789))  # -123,456,789
str(ReadableNumber(-12345.6789))  # -12,345.6789
str(ReadableNumber(-1.23456e18))  # -1,234,560,000,000,000,000
```

#### 2.2.2. Custom grouping (in locales other than en-US)

```python
str(ReadableNumber(-123456789, digit_group_size=4))  # -1,2345,6789
str(ReadableNumber(-123456789, digit_group_delimiter='|'))  # -123|456|789
```

#### 2.2.3. Print in shortform

```python
str(ReadableNumber(12345, use_shortform=True))  # 12k
str(ReadableNumber(12345, use_shortform=True, precision=1))  # 12.3k
str(ReadableNumber(12345678, use_shortform=True))  # 12M
str(ReadableNumber(12345678, use_shortform=True, precision=2))  # 12.35M
str(ReadableNumber(1234567890, use_shortform=True, precision=2))  # 1.23B
```

### 2.3. Setting precision or significant figures

#### 2.3.1. Without setting precision or significant figures

Numbers are printed in a "natural" way:

```python
str(ReadableNumber(0.12345))  # 0.12345
str(ReadableNumber(0.0000012345))  # 0.0000012345
```

#### 2.3.2. Precision

```python
str(ReadableNumber(0.12345, precision=None))  # 0.12345
str(ReadableNumber(0.12345, precision=2))  # 0.12
str(ReadableNumber(0.12345, precision=20))  # 0.123450000000000
```

#### 2.3.3. Significant figures

```python
str(ReadableNumber(0.12345, significant_figures_after_decimal_point=3))  # 0.123
str(ReadableNumber(12345, significant_figures_after_decimal_point=3))  # 12,345
str(ReadableNumber(0.00012345, significant_figures_after_decimal_point=3))  # 0.000123
str(ReadableNumber(-1.2345e-50, significant_figures_after_decimal_point=3))
# -0.0000000000000000000000000000000000000000000000000123
```

### 2.4. Exponential notations

#### 2.4.1. Print large numbers in exponential notation

```python
str(ReadableNumber(1234567890, use_exponent_for_large_numbers=True))  # 1.234568e+09

str(ReadableNumber(
    1234567890,
    use_exponent_for_large_numbers=True,
    precision=2,
))  # 1.23e+09

str(ReadableNumber(
    1234567890,
    use_exponent_for_large_numbers=True,
    precision=None,
))  # 1.23456789e+09

str(ReadableNumber(
    1234567890,
    use_exponent_for_large_numbers=True,
    large_number_threshold=1e20,  # only show in exp if we exceed this
    precision=None,
))  # 1,234,567,890

str(ReadableNumber(
    1234567890,
    use_exponent_for_large_numbers=True,
    large_number_threshold=1e20,  # only show in exp if we exceed this
    significant_figures_after_decimal_point=5,
))  # 1.2346e+09
```

#### 2.4.2. Print small numbers in exponential notation

```python
str(ReadableNumber(0.000000012, use_exponent_for_small_numbers=True))  # 1.200000e-08

str(ReadableNumber(
    -0.000000123456,
    use_exponent_for_small_numbers=True,
    precision=2,
))  # -1.23e-07

str(ReadableNumber(
    -0.000012345,
    use_exponent_for_small_numbers=True,
    precision=None,
    small_number_threshold=1e-2,
))  # -1.2345e-05

str(ReadableNumber(
    -0.00000012345,
    use_exponent_for_small_numbers=True,
    significant_figures_after_decimal_point=2,
))  # -1.23e-07
```

## 3. Full API documentation

Please visit this site: https://readable-number.readthedocs.io/en/stable/
