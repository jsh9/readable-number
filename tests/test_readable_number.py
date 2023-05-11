from typing import Any, Dict, Optional, Union, Type

import pytest

from readable_number import ReadableNumber

comma = ','
dot = '.'
space = ' '

test_cases = [
    # fmt: off
    (1e+500, 'inf', 0, comma, dot, 3, False, False),
    # fmt: on
    (12345678, '12345678', 0, comma, dot, 3, False, False),
    (12345678, '12,345,678', 3, comma, dot, 3, False, False),
    (12345678, '12,345,678.0', 3, comma, dot, 1, True, False),
    (12345678, '12,345,678.00', 3, comma, dot, 2, True, False),
    (12345678, '12,345,678.000', 3, comma, dot, 3, True, False),
    (12345678, '1234,5678.000', 4, comma, dot, 3, True, False),
    (12345678, '123 45678.000', 5, space, dot, 3, True, False),
    (5, '5', 10, '@', '^', 123, False, False),
    (5, '5?0000000000', 10, '@', '?', 10, True, False),
    (123, '123', 3, comma, dot, 3, False, False),
    (123, '1,2,3', 1, comma, dot, 3, False, False),
    (123, '123', 3, comma, dot, 1, False, True),
    (1234, '1.2k', 3, comma, dot, 1, False, True),
    (1234, '1.2340000k', 3, comma, dot, 7, False, True),
    (12345.234567, '12.35k', 1, '|', '?', 2, True, True),
    (123456.234567, '123.46k', 1, '|', '?', 2, True, True),
    (1234567.234567, '1.23M', 1, '|', '?', 2, True, True),
    (12345678, '12.35M', 3, comma, dot, 2, False, True),
    (12345678, '12.346M', 3, comma, dot, 3, False, True),
    (123456789.0123456, '123.46M', 3, comma, dot, 2, False, True),
    (1234567890.0123456, '1.23B', 3, comma, dot, 2, False, True),
    (123456789012.234567, '123.457B', 1, '|', '?', 3, True, True),
    (1234567890123.234567, '1.23457T', 1, '|', '?', 5, True, True),
    (1.1234567, '1.', 3, comma, dot, 0, True, False),
    (1.1234567, '1.1', 3, comma, dot, 1, True, False),
    (1.1234567, '1.12', 3, comma, dot, 2, True, False),
    (1.1234567, '1.123', 3, comma, dot, 3, True, False),
    (1.1234567, '1.1235', 3, comma, dot, 4, True, False),
    (1.1234567, '1.12346', 3, comma, dot, 5, True, False),
    (1.1234567, '1.123457', 3, comma, dot, 6, True, False),
    (1.1234567, '1.1234567', 3, comma, dot, 7, True, False),
    (1.1234567, '1.12345670', 3, comma, dot, 8, True, False),
    (1.1234567, '1.123456700', 3, comma, dot, 9, True, False),
    (1.1234567, '1.1234567000', 3, comma, dot, 10, True, False),
    (1.1234567, '1.1234567', 3, comma, dot, None, True, False),
    (
        1.1234567890123456789012345,
        '1.123456789012346',
        3,
        comma,
        dot,
        None,
        True,
        False,
    ),
    (
        1.1234567890123456789012345,
        '1.1234567890123460',
        3,
        comma,
        dot,
        16,
        True,
        False,
    ),
    (
        1.1234567890123456789012345,
        '1.12345678901234600',
        3,
        comma,
        dot,
        17,
        True,
        False,
    ),
    (
        1.1234567890123456789012345,
        '1.123456789012346000',
        3,
        comma,
        dot,
        18,
        True,
        False,
    ),
    (0.000_000_012_3, '0.0000000123', 3, comma, dot, None, True, False),
    (0.000_000_012_3, '0.', 3, comma, dot, 0, True, False),
    (0.000_000_012_3, '0.0', 3, comma, dot, 1, True, False),
    (0.000_000_012_3, '0.00', 3, comma, dot, 2, True, False),
    (0.000_000_012_3, '0.000', 3, comma, dot, 3, True, False),
    (0.000_000_012_3, '0.0000', 3, comma, dot, 4, True, False),
    (0.000_000_012_3, '0.00000', 3, comma, dot, 5, True, False),
    (0.000_000_012_3, '0.000000', 3, comma, dot, 6, True, False),
    (0.000_000_012_3, '0.0000000', 3, comma, dot, 7, True, False),
    (0.000_000_012_3, '0.00000001', 3, comma, dot, 8, True, False),
    (0.000_000_012_3, '0.000000012', 3, comma, dot, 9, True, False),
    (0.000_000_012_3, '0.0000000123', 3, comma, dot, 10, True, False),
    (0.000_000_012_3, '0.00000001230', 3, comma, dot, 11, True, False),
    (0.000_000_012_3, '0.000000012300', 3, comma, dot, 12, True, False),
    (0.000_000_012_3, '0.0000000123000', 3, comma, dot, 13, True, False),
    (0.000_000_012_3, '0.00000001230000', 3, comma, dot, 14, True, False),
    (0.000_000_012_3, '0.000000012300000', 3, comma, dot, 15, True, False),
    (0.000_000_012_3, '0.0000000123000000', 3, comma, dot, 16, True, False),
    (0.000_000_012_3, '0.00000001230000000', 3, comma, dot, 17, True, False),
    (0.000_000_012_3, '0.000000012300000000', 3, comma, dot, 18, True, False),
    (0.000_000_067_89, '0.00000006789', 3, comma, dot, None, True, False),
    (0.000_000_067_89, '0.', 3, comma, dot, 0, True, False),
    (0.000_000_067_89, '0.0', 3, comma, dot, 1, True, False),
    (0.000_000_067_89, '0.00', 3, comma, dot, 2, True, False),
    (0.000_000_067_89, '0.000', 3, comma, dot, 3, True, False),
    (0.000_000_067_89, '0.0000', 3, comma, dot, 4, True, False),
    (0.000_000_067_89, '0.00000', 3, comma, dot, 5, True, False),
    (0.000_000_067_89, '0.000000', 3, comma, dot, 6, True, False),
    (0.000_000_067_89, '0.0000001', 3, comma, dot, 7, True, False),
    (0.000_000_067_89, '0.00000007', 3, comma, dot, 8, True, False),
    (0.000_000_067_89, '0.000000068', 3, comma, dot, 9, True, False),
    (0.000_000_067_89, '0.0000000679', 3, comma, dot, 10, True, False),
    (0.000_000_067_89, '0.00000006789', 3, comma, dot, 11, True, False),
    (0.000_000_067_89, '0.000000067890', 3, comma, dot, 12, True, False),
    (0.000_000_067_89, '0.0000000678900', 3, comma, dot, 13, True, False),
    (0.000_000_067_89, '0.00000006789000', 3, comma, dot, 14, True, False),
    (0.000_000_067_89, '0.000000067890000', 3, comma, dot, 15, True, False),
    (0.000_000_067_89, '0.0000000678900000', 3, comma, dot, 16, True, False),
    (0.000_000_067_89, '0.00000006789000000', 3, comma, dot, 17, True, False),
    (0.000_000_067_89, '0.000000067890000000', 3, comma, dot, 18, True, False),
    (0.9050123, '1.', 3, comma, dot, 0, True, False),
    (0.9050123, '0.9', 3, comma, dot, 1, True, False),
    (0.9050123, '0.91', 3, comma, dot, 2, True, False),
    (0.9050123, '0.905', 3, comma, dot, 3, True, False),
    (12.734626, '13.', 9, comma, dot, 0, True, False),
    (12.734626, '12.7', 9, comma, dot, 1, True, False),
    (12.734626, '12.73', 9, comma, dot, 2, True, False),
    (12.734626, '12.735', 9, comma, dot, 3, True, False),
    (12.734626, '12.7346', 9, comma, dot, 4, True, False),
    (12.734626, '12.73463', 9, comma, dot, 5, True, False),
    (12.734626, '12.734626', 9, comma, dot, 6, True, False),
    (12.734626, '12.7346260', 9, comma, dot, 7, True, False),
    (12.734626, '12.73462600', 9, comma, dot, 8, True, False),
    (
        1.12345678901234567890,
        '1.12345678901234600000000000000000000000000000000000',
        3,
        comma,
        dot,
        50,
        True,
        False,
    ),
    (
        1.11111111111111111111,
        '1.11111111111111100000000000000000000000000000000000',
        3,
        comma,
        dot,
        50,
        True,
        False,
    ),
    (
        1.22222222222222222222,
        '1.22222222222222200000000000000000000000000000000000',
        3,
        comma,
        dot,
        50,
        True,
        False,
    ),
    (
        1234567890.734626,
        '1,234,567,890.73462600',
        3,
        comma,
        dot,
        8,
        True,
        False,
    ),
    (1234567890.734626, '1.23456789B', 3, comma, dot, 8, True, True),
    (1234567890.734626, '1.23B', 3, comma, dot, 2, True, True),
    (1234567890.123456789, '1.235B', 3, comma, dot, 3, True, True),
    (1234567890.123456789, '1.2346B', 3, comma, dot, 4, True, True),
    (1234567890.123456789, '1.23457B', 3, comma, dot, 5, True, True),
    (1234567890.123456789, '1.234568B', 3, comma, dot, 6, True, True),
    (1234567890.123456789, '1.2345679B', 3, comma, dot, 7, True, True),
    (1234567890.123456789, '1.23456789B', 3, comma, dot, 8, True, True),
    (1234567890.123456789, '1.234567890B', 3, comma, dot, 9, True, True),
    (1234567890.123456789, '1.2345678901B', 3, comma, dot, 10, True, True),
    (1234567890.123456789, '1.23456789012B', 3, comma, dot, 11, True, True),
    (1234567890.123456789, '1.234567890123B', 3, comma, dot, 12, True, True),
    (1234567890.123456789, '1.2345678901235B', 3, comma, dot, 13, True, True),
    (1234567890.123456789, '1.23456789012346B', 3, comma, dot, 14, True, True),
    (
        1234567890.123456789,
        '1.234567890123457B',
        3,
        comma,
        dot,
        15,
        True,
        True,
    ),
    (
        1234567890.123456789,
        '1.234567890123457B',
        3,
        comma,
        dot,
        16,
        True,
        True,
    ),
    (
        1234567890.123456789,
        '1.234567890123457B',
        3,
        comma,
        dot,
        17,
        True,
        True,
    ),
    (
        1234567890.123456789,
        '1.234567890123457B',
        3,
        comma,
        dot,
        18,
        True,
        True,
    ),
    (
        1234567890.123456789,
        '1.234567890123457B',
        3,
        comma,
        dot,
        19,
        True,
        True,
    ),
    (1_234_567_890_123, '1.235T', 3, comma, dot, 3, True, True),
    (
        123_456_789_234_567_890_123,
        '123456789.235T',
        3,
        comma,
        dot,
        3,
        False,
        True,
    ),
    (12345678.0, '12,345,678.000', 3, comma, dot, 3, True, False),
    (12345678.0, '12,345,678', 3, comma, dot, None, False, False),
    (12345678, '12,345,678', 3, comma, dot, None, False, False),
    (12345678.123, '12,345,678.1230', 3, comma, dot, 4, False, False),
    (1234567890123.234567, '1.23457T', 1, '|', '?', 5, True, True),
    (
        1234567890123.234567,
        '1|234|567|890|123.23',
        3,
        '|',
        dot,
        2,
        True,
        False,
    ),
    (0.0000123, '0.0000123', 3, comma, dot, None, True, False),
    (75.2, '75.', 3, comma, dot, 0, True, True),
    (75.9, '76.', 3, comma, dot, 0, True, True),
    (75.2, '75.2', 3, comma, dot, 1, True, True),
    (75.2, '75.2', 3, comma, dot, None, True, True),
    (75.2, '75.200', 3, comma, dot, 3, True, True),
    (75.26789, '75.268', 3, comma, dot, 3, True, True),
    (1.23456e-2, '0.012', 3, comma, dot, 3, False, True),
    (1.6789e-2, '0.0168', 3, comma, dot, 4, False, True),
    (1.23456789e-3, '0.0012346', 3, comma, dot, 7, False, True),
    (12345e3, '12.3450M', 3, comma, dot, 4, False, True),
    (12345e3, '12,345,000', 3, comma, dot, 4, False, False),
    (12345e10, '123.4500T', 3, comma, dot, 4, False, True),
    (1.23456789e3, '1,234.5679', 3, comma, dot, 4, False, False),
    (1.23456789e3, '1.2346k', 3, comma, dot, 4, False, True),
    (1.23456789e-30, '0.0000', 3, comma, dot, 4, False, True),
    (
        1234567890123.234567,
        '1|234|567|890|123.23',
        3,
        '|',
        dot,
        2,
        True,
        False,
    ),
    (0.000_000_067_89, '0.000000067890000000', 3, comma, dot, 18, True, False),
    (
        123_456_789_234_567_890_123,
        '123456789.235T',
        3,
        comma,
        dot,
        3,
        False,
        True,
    ),
    (
        123_456_789_234_567_890_123,
        '123456789.235T',
        3,
        comma,
        dot,
        3,
        False,
        True,
    ),
    (1234, '1234', 5, comma, dot, 3, False, False),
    (1234, '1234.000', 5, comma, dot, 3, True, False),
    (1234, '1234.00', 5, comma, dot, None, True, False),
    (12, '12.00', 5, comma, dot, None, True, True),
    (12, '12', 5, comma, dot, None, False, True),
    (12, '12.0000', 5, comma, dot, 4, True, True),
    (12, '12', 5, comma, dot, 4, False, True),
    (1e18, '1,000,000,000,000,000,000', 3, comma, dot, 2, False, False),
    (1e18, '1,000,000,000,000,000,000.00', 3, comma, dot, 2, True, False),
    (1e18, '1,000,000,000,000,000,000', 3, comma, dot, 2, False, False),
    (1e18, '1,000,000,000,000,000,000.00', 3, comma, dot, 2, True, False),
    (
        0.000000000000000000000000000000000000000000001,
        '0.0000',
        3,
        comma,
        dot,
        4,
        True,
        False,
    ),
    (
        0.000000000000000000000000000000000000000000001,
        '0.000000000000000000000000000000000000000000001',
        3,
        comma,
        dot,
        None,
        True,
        False,
    ),
    (
        0.000000000000000000000000000000000000000000001,
        '0.00000000000000000000000000000000000000000000100000',
        3,
        comma,
        dot,
        50,
        True,
        False,
    ),
    (2.1e-7, '0.00000021', 3, comma, dot, None, False, False),
    (2.1e-11, '0.000000000021', 3, comma, dot, None, False, False),
    (2.1e-14, '0.000000000000021', 3, comma, dot, None, False, False),
    (2.1e-16, '0.00000000000000021', 3, comma, dot, None, False, False),
    (2.1e-19, '0.00000000000000000021', 3, comma, dot, None, False, False),
    (123456, '123k', 3, comma, dot, None, False, True),
    (123456, '123k', 3, comma, dot, 0, False, True),
    (123456, '123.5k', 3, comma, dot, 1, False, True),
    (123456, '123.46k', 3, comma, dot, 2, False, True),
    (12345678, '12M', 3, comma, dot, None, False, True),
    (12345678, '12M', 3, comma, dot, 0, False, True),
    (12345678, '12.3M', 3, comma, dot, 1, False, True),
    (12345678, '12.35M', 3, comma, dot, 2, False, True),
    (12345678, '12.346M', 3, comma, dot, 3, False, True),
    (1234567890, '1B', 3, comma, dot, None, False, True),
    (1234567890, '1B', 3, comma, dot, 0, False, True),
    (1234567890, '1.2B', 3, comma, dot, 1, False, True),
    (1234567890, '1.23B', 3, comma, dot, 2, False, True),
    (1234567890, '1.235B', 3, comma, dot, 3, False, True),
    (1234567890, '1.2346B', 3, comma, dot, 4, False, True),
    (1234567890, '1.23457B', 3, comma, dot, 5, False, True),
    (123456789, '123,456,789', 3, comma, dot, None, False, False),
    (12345678, '12,345,678', 3, comma, dot, None, False, False),
    (12, '12', 3, comma, dot, None, False, False),
    (123, '123', 3, comma, dot, None, False, False),
    (1234, '1,234', 3, comma, dot, None, False, False),
    (
        1.234568e-41,
        '0.00000000000000000000000000000000000000001234568',
        3,
        comma,
        dot,
        None,
        False,
        False,
    ),
    (1.234568e-41, '0.00', 3, comma, dot, 2, False, False),
    (
        # fmt: off
        0.000000000000000000001234e+30,
        # fmt: on
        '1,234,000,000',
        3,
        comma,
        dot,
        2,
        False,
        False,
    ),
    # fmt: off
    (0.000000000000000000001234e+30, '1.23B', 3, comma, dot, 2, False, True),
    # fmt: on
]

test_cases_expanded = (
    [(-a, '-' + b, c, d, e, f, g, h) for a, b, c, d, e, f, g, h in test_cases]
    + [(+a, b, c, d, e, f, g, h) for a, b, c, d, e, f, g, h in test_cases]
    + [
        (0, '0.00', 3, comma, dot, 2, True, False),
        (0, '0.0000', 3, comma, dot, 4, True, False),
        (0, '0.000000', 3, comma, dot, 6, True, False),
        # fmt: off
        (1e-500, '0', 0, comma, dot, 3, False, False),
        # fmt: on
        (0, '0', 3, comma, dot, 3, False, False),
        (-0, '0', 3, comma, dot, None, False, False),
        (+0, '0', 3, comma, dot, None, False, False),
        (float('nan'), 'nan', 1, comma, dot, 3, True, True),
        (float('Nan'), 'nan', 3, comma, dot, 3, True, False),
        (float('NaN'), 'nan', 3, comma, dot, 3, False, True),
        (float('NAN'), 'nan', 3, comma, dot, 300, True, True),
        (float('-NAN'), 'nan', 3, comma, dot, 300, True, True),
        (float('inf'), 'inf', 3, comma, dot, 3, True, True),
        (float('Inf'), 'inf', 3, comma, dot, 3, True, True),
        (float('INF'), 'inf', 3, comma, dot, 3, True, True),
        (float('-inf'), '-inf', 3, comma, dot, 3, True, True),
        (float('-Inf'), '-inf', 3, comma, dot, 3, True, True),
        (float('-INF'), '-inf', 3, comma, dot, 3, True, True),
    ]
)


@pytest.mark.parametrize(
    'num,expected,grpSize,grpDelim,decSymb,precision,showDec,useShortform',
    test_cases_expanded,
)
def test_readableNumber(
        num: Union[float, int],
        expected: str,
        grpSize: int,
        grpDelim: str,
        decSymb: str,
        precision: int,
        showDec: bool,
        useShortform: bool,
) -> None:
    number = ReadableNumber(
        num=num,
        digit_group_size=grpSize,
        digit_group_delimiter=grpDelim,
        decimal_symbol=decSymb,
        precision=precision,
        show_decimal_part_if_integer=showDec,
        use_shortform=useShortform,
    )
    assert str(number) == expected


@pytest.mark.parametrize(
    'input_string',
    ['test', '-', '.', '!'],
)
def test_readableNumber_invalid_input(input_string: str) -> None:
    with pytest.raises(ValueError):
        ReadableNumber(input_string)  # type: ignore[arg-type]


test_cases_exponent_large_number = [
    (0.1, '0.100000', 1e6, 6),
    (0.01, '0.010000', 1e6, 6),
    (1234, '1,234', 1e6, 6),
    (123456, '123,456', 1e6, 6),
    (1234567, '1.234567e+06', 1e6, 6),
    (12345678, '1.234568e+07', 1e6, 6),
    (123456789, '1.234568e+08', 1e6, 6),
    (123456789123456, '1.234568e+14', 1e6, 6),
    (123456789123456789123456789, '1.234568e+26', 1e6, 6),
    (1.234567e12, '1.234567e+12', 1e6, 6),
    # fmt: off
    (1.234567e+12, '1.234567e+12', 1e6, 6),
    # fmt: on
    (1234567890, '1,234,567,890', 1e100, 6),
    # fmt: off
    (0.000000000000000000001234e90, '1.234000e+69', 1e6, 6),
    (0.000000000000000000001234e+90, '1.234000e+69', 1e6, 6),
    # fmt: on
    (1234, '1.234000e+03', 10, 6),
    (1234, '1.234000e+03', 100, 6),
    (1234, '1.234000e+03', 1000, 6),
    (1234, '1.234000e+03', 1233, 6),
    (1234, '1.234000e+03', 1234, 6),
    (1234, '1,234', 1235, 6),
    (1234, '1.234e+03', 10, None),
    (1234, '1e+03', 10, 0),
    (1234, '1.2e+03', 10, 1),
    (1234, '1.23e+03', 10, 2),
    (1234, '1.234e+03', 10, 3),
    (1234, '1.23400000e+03', 10, 8),
    (1234, '1.234000000000000000000000000000e+03', 10, 30),
    (0.1, '0.1000', 1e6, 4),
    (0.01, '0.0100', 1e6, 4),
    (0.1, '0.1', 1e6, None),
    (0.01, '0.01', 1e6, None),
    # fmt: off
    (1.123e+123, '1.123e+123', 1e6, None),
    (1.123e+456, 'inf', 1e6, None),
    # fmt: on
]

test_cases_exponent_large_number_expanded = (
    [(-a, '-' + b, c, d) for a, b, c, d in test_cases_exponent_large_number]
    + [(+a, b, c, d) for a, b, c, d in test_cases_exponent_large_number]
    + [
        (0, '0', 1e6, 6),
    ]
)


@pytest.mark.parametrize(
    'num, expected, threshold, precision',
    test_cases_exponent_large_number_expanded,
)
def test_readableNumber_exponent_large_number(
        num: Union[float, int],
        expected: str,
        threshold: int,
        precision: int,
) -> None:
    number = ReadableNumber(
        num=num,
        use_exponent_for_large_numbers=True,
        large_number_threshold=threshold,
        precision=precision,
    )
    assert str(number) == expected


test_cases_exponent_small_number = [
    (0.1, '0.100000', 1e-6, 6),
    (0.01, '0.010000', 1e-6, 6),
    (123456789, '123,456,789', 1e-6, 6),
    (0.00001, '0.000010', 1e-6, 6),
    (0.000001, '1.000000e-06', 1e-6, 6),
    (0.0000001, '1.000000e-07', 1e-6, 6),
    (0.0000000000000000000123, '1.230000e-20', 1e-6, 6),
    (0.000075e-10, '7.500000e-15', 1e-6, 6),
    (1234567890e-50, '1.234568e-41', 1e-6, 6),
    (0.000123, '1.230000e-04', 1e-1, 6),
    (0.000123, '1.230000e-04', 1e-2, 6),
    (0.000123, '1.230000e-04', 1e-3, 6),
    (0.000123, '1.230000e-04', 0.000124, 6),
    (0.000123, '1.230000e-04', 0.000123, 6),
    (0.000123, '0.000123', 0.000122, 6),
    (0.000123, '0.000123', 1e-4, 6),
    (0.000123, '0.000123', 1e-5, 6),
    (0.0000000000123, '0.0000000000123', 1e-20, None),
    (0.00012345, '1e-04', 1e-1, 0),
    (0.00012345, '1.2e-04', 1e-1, 1),
    (0.00012345, '1.23e-04', 1e-1, 2),
    (0.00012345, '1.234e-04', 1e-1, 3),
    (0.00012345, '1.2345e-04', 1e-1, 4),
    (0.00012345, '1.23450e-04', 1e-1, 5),
    (0.00012345, '1.234500e-04', 1e-1, 6),
    (0.00012345, '1.2345000e-04', 1e-1, 7),
    (0.00012345, '1.2345000000e-04', 1e-1, 10),
    (0.00012345, '1.234500000000000e-04', 1e-1, 15),
    (0.00012345, '0.000123450000000', 1e-20, 15),
    (0.00012345, '1.2345e-04', 1e-1, None),
    (0.00012345, '0.00012345', 1e-10, None),
    (1.123e-123, '1.123e-123', 1e6, None),
]

test_cases_exponent_small_number_expanded = (
    [(-a, '-' + b, c, d) for a, b, c, d in test_cases_exponent_small_number]
    + [(+a, b, c, d) for a, b, c, d in test_cases_exponent_small_number]
    + [
        (0, '0', 1e-6, 6),
        (1.123e-999, '0', 1e6, None),
    ]
)


@pytest.mark.parametrize(
    'num, expected, threshold, precision',
    test_cases_exponent_small_number_expanded,
)
def test_readableNumber_exponent_small_number(
        num: Union[float, int],
        expected: str,
        threshold: float,
        precision: Optional[int],
) -> None:
    number = ReadableNumber(
        num=num,
        use_exponent_for_small_numbers=True,
        small_number_threshold=threshold,
        precision=precision,
    )
    assert str(number) == expected


test_cases_sig_figure = [
    (1234567, '1,230,000', 3, {}),
    (1234567.890123, '1,230,000', 3, {}),
    (1234567, '1,23,00,00', 3, {'digit_group_size': 2}),
    (1234567, '1|230|000', 3, {'digit_group_delimiter': '|'}),
    (1234_45678, '123M', 4, {'use_shortform': True}),
    (1234_45678, '123M', 4, {'use_shortform': True}),
    (1234_56789, '123M', 6, {'use_shortform': True}),
    (1234_56789, '123M', 6, {'use_shortform': True}),
    (1234_56789, '123M', 5, {'use_shortform': True}),
    (1234_56789, '124M', 4, {'use_shortform': True}),
    (1234_56789, '123M', 3, {'use_shortform': True}),
    (1234_56789, '120M', 2, {'use_shortform': True}),
    (1234_56789, '100M', 1, {'use_shortform': True}),
    (1234_56789, '124M', 4, {'use_shortform': True}),
    (
        1234_56789,
        '1.235e+08',
        4,
        {'use_exponent_for_large_numbers': True},
    ),
    (
        1234_56789,
        '1.2346e+08',
        5,
        {'use_exponent_for_large_numbers': True},
    ),
    (
        1234_56789,
        '1.2346e+08',
        5,
        {'use_exponent_for_large_numbers': True},
    ),
    (0.123456, '0.1', 1, {}),
    (0.123456, '0.12', 2, {}),
    (0.123456, '0.123', 3, {}),
    (0.123456, '0.1235', 4, {}),
    (0.123456, '0.12346', 5, {}),
    (0.123456, '0.123456', 6, {}),
    (0.123456, '0.1234560', 7, {}),
    (0.123456, '0.12345600', 8, {}),
    (0.123456, '0.123456000', 9, {}),
    (0.123456, '0.123456000000000', 15, {}),
    (0.00123456, '0.001', 1, {}),
    (0.00123456, '0.0012', 2, {}),
    (0.00123456, '0.00123', 3, {}),
    (0.00123456, '0.001235', 4, {}),
    (0.00123456, '0.0012346', 5, {}),
    (0.00123456, '0.00123456', 6, {}),
    (0.00123456, '0.001234560', 7, {}),
    (0.00123456, '0.0012345600', 8, {}),
    (0.00123456, '0.00123456000', 9, {}),
    (0.00000123456, '0.000001', 1, {}),
    (0.00000123456, '0.0000012', 2, {}),
    (0.00000123456, '0.00000123', 3, {}),
    (0.00000123456, '0.000001235', 4, {}),
    (0.00000123456, '0.0000012346', 5, {}),
    (0.00000123456, '0.00000123456', 6, {}),
    (0.00000123456, '0.000001234560', 7, {}),
    (0.00000123456, '0.0000012345600', 8, {}),
    (0.00000123456, '0.00000123456000', 9, {}),
    (0.0000000000123456, '0.00000000001', 1, {}),
    (0.0000000000123456, '0.000000000012', 2, {}),
    (0.0000000000123456, '0.0000000000123', 3, {}),
    (0.0000000000123456, '0.00000000001235', 4, {}),
    (0.0000000000123456, '0.000000000012346', 5, {}),
    (0.0000000000123456, '0.0000000000123456', 6, {}),
    (0.0000000000123456, '0.00000000001234560', 7, {}),
    (0.0000000000123456, '0.000000000012345600', 8, {}),
    (0.0000000000123456, '0.0000000000123456000', 9, {}),
    (0.0000000000000123456, '0.00000000000001', 1, {}),
    (0.0000000000000123456, '0.000000000000012', 2, {}),
    (0.0000000000000123456, '0.0000000000000123', 3, {}),
    (0.0000000000000123456, '0.00000000000001235', 4, {}),
    (0.0000000000000123456, '0.000000000000012346', 5, {}),
    (0.0000000000000123456, '0.0000000000000123456', 6, {}),
    (0.0000000000000123456, '0.00000000000001234560', 7, {}),
    (0.0000000000000123456, '0.000000000000012345600', 8, {}),
    (0.0000000000000123456, '0.0000000000000123456000', 9, {}),
    (0.0000000000000000123456, '0.00000000000000001', 1, {}),
    (0.0000000000000000123456, '0.000000000000000012', 2, {}),
    (0.0000000000000000123456, '0.0000000000000000123', 3, {}),
    (0.0000000000000000123456, '0.00000000000000001235', 4, {}),
    (0.0000000000000000123456, '0.000000000000000012346', 5, {}),
    (0.0000000000000000123456, '0.0000000000000000123456', 6, {}),
    (0.0000000000000000123456, '0.00000000000000001234560', 7, {}),
    (0.0000000000000000123456, '0.000000000000000012345600', 8, {}),
    (0.0000000000000000123456, '0.0000000000000000123456000', 9, {}),
    (1.23456e-17, '0.000000000000000012', 2, {}),
    (1.23456e-17, '0.0000000000000000123456000', 9, {}),
]

test_cases_significant_figure_expanded = [
    (-a, '-' + b, c, d) for a, b, c, d in test_cases_sig_figure
] + [(+a, b, c, d) for a, b, c, d in test_cases_sig_figure]


@pytest.mark.parametrize(
    'num, expected, sig_fig, other_options',
    test_cases_significant_figure_expanded,
)
def test_significant_number__apply_sig_fig_only_to_numbers_less_than_1_False(
        num: Union[float, int],
        expected: str,
        sig_fig: bool,
        other_options: Dict[str, Any],
) -> None:
    rn = ReadableNumber(
        significant_figures=sig_fig,
        apply_sig_fig_only_to_numbers_less_than_1=False,
        **other_options,
    )
    assert rn.of(num) == expected


@pytest.mark.parametrize(
    'param, val, expected_error',
    [
        ('digit_group_size', -1, ValueError),
        ('digit_group_size', '1', TypeError),
        ('digit_group_delimiter', 2, TypeError),
        ('digit_group_delimiter', 2.1, TypeError),
        ('digit_group_delimiter', '-', ValueError),
        ('decimal_symbol', [1, 2, 3], TypeError),
        ('decimal_symbol', 2.2, TypeError),
        ('decimal_symbol', '-', ValueError),
        ('precision', -0.5, TypeError),
        ('precision', -5, ValueError),
        ('precision', 1.2, TypeError),
        ('precision', {'a': 1}, TypeError),
        ('show_decimal_part_if_integer', 0, TypeError),
        ('show_decimal_part_if_integer', 1, TypeError),
        ('use_shortform', 0, TypeError),
        ('use_shortform', 1, TypeError),
    ],
)
def test_readableNumber_invalid_params(
        param: str,
        val: Any,
        expected_error: Type[Exception],
) -> None:
    kwarg = {param: val}
    with pytest.raises(expected_error):
        ReadableNumber(1.2345, **kwarg)


@pytest.mark.parametrize(
    'num, options, expected',
    [
        (
            12345678,
            {'use_exponent_for_large_numbers': True, 'precision': 4},
            '1.2346e+07',
        ),
        (
            -0.000000123456789,
            {'use_exponent_for_small_numbers': True, 'precision': None},
            '-1.23456789e-07',
        ),
        (1234567890, {}, '1,234,567,890'),
    ],
)
def test_of_method(
        num: Union[float, int],
        options: Dict[str, Any],
        expected: str,
) -> None:
    rn = ReadableNumber(**options)
    assert rn.of(num) == expected


@pytest.mark.parametrize(
    'input_, expected',
    [
        ('', '1'),
        ('1', '2'),
        ('9', '10'),
        ('00012', '00013'),
        ('00013', '00014'),
        ('00019', '00020'),
        ('00149', '00150'),
        ('00199', '00200'),
        ('89999', '90000'),
        ('99999', '100000'),
    ],
)
def test_carry(input_: str, expected: str) -> None:
    output = ReadableNumber._carry(input_)
    assert output == expected
