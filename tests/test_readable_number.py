import pytest
from readable_number import ReadableNumber

comma = ','
dot = '.'
space = ' '

long_num = 1.1234567890123456789012345

test_cases = [
    (12345678, '12345678', 0, comma, dot, 3, False, False),
    (12345678, '12,345,678', 3, comma, dot, 3, False, False),
    (12345678, '12,345,678.0', 3, comma, dot, 1, True, False),
    (12345678, '12,345,678.00', 3, comma, dot, 2, True, False),
    (12345678, '12,345,678.000', 3, comma, dot, 3, True, False),
    (12345678, '1234,5678.000', 4, comma, dot, 3, True, False),
    (12345678, '123 45678.000', 5, space, dot, 3, True, False),
    (0, '0', 3, comma, dot, 3, False, False),
    (0, '0.00', 3, comma, dot, 2, True, False),
    (0, '0.0000', 3, comma, dot, 4, True, False),
    (0, '0.000000', 3, comma, dot, 6, True, False),
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
    (-12345678, '-12.35M', 3, comma, dot, 2, False, True),
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
    (long_num, '1.123456789012346', 3, comma, dot, None, True, False),
    (long_num, '1.123456789012346', 3, comma, dot, 16, True, False),
    (long_num, '1.123456789012346', 3, comma, dot, 17, True, False),
    (long_num, '1.123456789012346', 3, comma, dot, 18, True, False),
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
    (0.000_000_012_3, '0.000000012300000', 3, comma, dot, 16, True, False),
    (0.000_000_012_3, '0.000000012300000', 3, comma, dot, 17, True, False),
    (0.000_000_012_3, '0.000000012300000', 3, comma, dot, 18, True, False),
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
    (0.000_000_067_89, '0.000000067890000', 3, comma, dot, 16, True, False),
    (0.000_000_067_89, '0.000000067890000', 3, comma, dot, 17, True, False),
    (0.000_000_067_89, '0.000000067890000', 3, comma, dot, 18, True, False),
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
    (1.12345678901234567890, '1.123456789012346', 3, comma, dot, 50, True, False),
    (1.11111111111111111111, '1.111111111111111', 3, comma, dot, 50, True, False),
    (1.22222222222222222222, '1.222222222222222', 3, comma, dot, 50, True, False),
    (1234567890.734626, '1,234,567,890.73462600', 3, comma, dot, 8, True, False),
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
    (1234567890.123456789, '1.234567890123457B', 3, comma, dot, 15, True, True),
    (1234567890.123456789, '1.234567890123457B', 3, comma, dot, 16, True, True),
    (1234567890.123456789, '1.234567890123457B', 3, comma, dot, 17, True, True),
    (1234567890.123456789, '1.234567890123457B', 3, comma, dot, 18, True, True),
    (1234567890.123456789, '1.234567890123457B', 3, comma, dot, 19, True, True),
    (1_234_567_890_123, '1.235T', 3, comma, dot, 3, True, True),
    (123_456_789_234_567_890_123, '123456789.235T', 3, comma, dot, 3, False, True),
    (-12345678, '-12,345,678.000', 3, comma, dot, 3, True, False),
    (-12345678, '-12,345,678', 3, comma, dot, 3, False, False),
    (-12345678.123, '-12,345,678.1230', 3, comma, dot, 4, False, False),
    (-1234567890123.234567, '-1.23457T', 1, '|', '?', 5, True, True),
    (-1234567890123.234567, '-1|234|567|890|123.23', 3, '|', dot, 2, True, False),
    (-1234567890.123456789, '-1.234567890123457B', 3, comma, dot, 19, True, True),
    (-123_456_789_234_567_890_123, '-123456789.235T', 3, comma, dot, 3, False, True),
    (-0.0000123, '-0.0000123', 3, comma, dot, None, True, False),
    (-0.000_000_067_89, '-0.000000067890000', 3, comma, dot, 18, True, False),
    (-75.2, '-75.', 3, comma, dot, 0, True, True),
    (-75.9, '-76.', 3, comma, dot, 0, True, True),
    (-75.2, '-75.2', 3, comma, dot, 1, True, True),
    (-75.2, '-75.2', 3, comma, dot, None, True, True),
    (-75.2, '-75.200', 3, comma, dot, 3, True, True),
    (-75.26789, '-75.268', 3, comma, dot, 3, True, True),
    (1.23456e-2, '0.012', 3, comma, dot, 3, False, True),
    (1.6789e-2, '0.0168', 3, comma, dot, 4, False, True),
    (1.23456789e-3, '0.0012346', 3, comma, dot, 7, False, True),
    (12345e3, '12.3450M', 3, comma, dot, 4, False, True),
    (12345e3, '12,345,000', 3, comma, dot, 4, False, False),
    (12345e10, '123.4500T', 3, comma, dot, 4, False, True),
    (1.23456789e3, '1,234.5679', 3, comma, dot, 4, False, False),
    (1.23456789e3, '1.2346k', 3, comma, dot, 4, False, True),
    (1.23456789e-30, '0.0000', 3, comma, dot, 4, False, True),
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
    ('-1234567890123.234567', '-1|234|567|890|123.23', 3, '|', dot, 2, True, False),
    ('-0.000_000_067_89', '-0.000000067890000', 3, comma, dot, 18, True, False),
    ('-123_456_789_234_567_890_123', '-123456789.235T', 3, comma, dot, 3, False, True),
    ('123_456_789_234_567_890_123', '123456789.235T', 3, comma, dot, 3, False, True),
    (1234, '1234', 5, comma, dot, 3, False, False),
    (1234, '1234.000', 5, comma, dot, 3, True, False),
    (1234, '1234.00', 5, comma, dot, None, True, False),
    (12, '12.00', 5, comma, dot, None, True, True),
    (12, '12', 5, comma, dot, None, False, True),
    (12, '12.0000', 5, comma, dot, 4, True, True),
    (12, '12', 5, comma, dot, 4, False, True),
    (1e18, '1,000,000,000,000,000,000', 3, comma, dot, 2, False, False),
    (1e18, '1,000,000,000,000,000,000.00', 3, comma, dot, 2, True, False),
    (-1e18, '-1,000,000,000,000,000,000', 3, comma, dot, 2, False, False),
    (-1e18, '-1,000,000,000,000,000,000.00', 3, comma, dot, 2, True, False),
    (
        -0.000000000000000000000000000000000000000000001,
        '-0.0000',
        3,
        comma,
        dot,
        4,
        True,
        False,
    ),
    (
        -0.000000000000000000000000000000000000000000001,
        '-0.000000000000000',
        3,
        comma,
        dot,
        None,
        True,
        False,
    ),
    (
        -0.000000000000000000000000000000000000000000001,
        '-0.000000000000000',
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
    (2.1e-16, '0.000000000000000', 3, comma, dot, None, False, False),
    (2.1e-19, '0.000000000000000', 3, comma, dot, None, False, False),
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
    (-123456789, '-123,456,789', 3, comma, dot, None, False, False),
    (-12345678, '-12,345,678', 3, comma, dot, None, False, False),
    (-12, '-12', 3, comma, dot, None, False, False),
    (-123, '-123', 3, comma, dot, None, False, False),
    (-1234, '-1,234', 3, comma, dot, None, False, False),
    (-0, '0', 3, comma, dot, None, False, False),
    (1.234568e-41, '0.000000000000000', 3, comma, dot, None, False, False),
    (1.234568e-41, '0.00', 3, comma, dot, 2, False, False),
    (
        -0.000000000000000000001234e+30,
        '1,234,000,000',
        3,
        comma,
        dot,
        2,
        False,
        False,
    ),
    (-0.000000000000000000001234e+30, '-1.23B', 3, comma, dot, 2, False, True),
]


@pytest.mark.parametrize(
    'num,expected,grpSize,grpDelim,decSymb,precision,showDec,useShortform',
    test_cases,
)
def test_readableNumber(
        num,
        expected,
        grpSize,
        grpDelim,
        decSymb,
        precision,
        showDec,
        useShortform,
):
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
def test_readableNumber_invalid_input(input_string):
    with pytest.raises(ValueError):
        ReadableNumber(input_string)


@pytest.mark.parametrize(
    'num, expected',
    [
        (0, '0'),
        (0.1, '0.1'),
        (-0.01, '-0.01'),
        (1234, '1,234'),
        (123456, '123,456'),
        (1234567, '1.234567e+06'),
        (-1234567, '-1.234567e+06'),
        (-12345678, '-1.234568e+07'),
        (-123456789, '-1.234568e+08'),
        (-123456789123456, '-1.234568e+14'),
        (-123456789123456789123456789, '-1.234568e+26'),
        (-1.234567e12, '-1.234567e+12'),
        (-0.000000000000000000001234e+90, '-1.234000e+69'),
    ],
)
def test_readableNumber_exponent_large_number(num, expected):
    number = ReadableNumber(
        num=num,
        use_exponent_for_large_numbers=True,
    )
    assert str(number) == expected


@pytest.mark.parametrize(
    'num, expected',
    [
        (0, '0'),
        (0.1, '0.1'),
        (-0.01, '-0.01'),
        (123456789, '123,456,789'),
        (0.00001, '0.00001'),
        (0.000001, '1.000000e-06'),
        (-0.0000001, '-1.000000e-07'),
        (-0.0000000000000000000123, '-1.230000e-20'),
        (-0.000075e-10, '-7.500000e-15'),
        (1234567890e-50, '1.234568e-41'),
    ],
)
def test_readableNumber_exponent_small_number(num, expected):
    number = ReadableNumber(
        num=num,
        use_exponent_for_small_numbers=True,
    )
    assert str(number) == expected


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
def test_readableNumber_invalid_params(param, val, expected_error):
    kwarg = {param: val}
    with pytest.raises(expected_error):
        ReadableNumber(1.2345, **kwarg)
