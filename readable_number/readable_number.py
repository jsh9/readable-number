import math
import numbers
from typing import Any, Optional, Union, Tuple
from types import MappingProxyType

from dataclasses import dataclass

METRIC_PREFIX_LOOKUP = MappingProxyType(
    {
        0: '',
        1: 'k',
        2: 'M',
        3: 'B',
        4: 'T',
    },
)
MAX_TIER = max(METRIC_PREFIX_LOOKUP.keys())
MAX_DIGITS_IN_DOUBLE_PRECISION: int = 15


@dataclass
class _IntegerAndDecimalParts:
    integer_part_str: str
    integer_part_int: int
    decimal_part_str: str
    decimal_part_float: float
    sign: int


class ReadableNumber:
    """
    A class to hold a number for human-readable printing.

    Parameters
    ----------
    num : numbers.Real or None
        A number to be printed in a readable format.  If ``None``, it
        means you are only initializing an "empty" object with printing
        options. In that case, you can use the `of()` method later to
        print the readable result.
    digit_group_size : int
        The size of the digit group (in the integer part).  For example,
        if 3, the number 123456789 will be printed as 123,456,789.
        If 0, no grouping will happen.  Only non-negative integers
        are allowed. (Default: 3)
    digit_group_delimiter : str
        The symbol to delimit the digit groups.  For example, if it
        is a space, the number 1234567 will be printed as 1 234 567.
        (Default: ",")
    decimal_symbol : str
        The symbol to use as a decimal "point".  Default: "."
    precision : int or None
        How many digits to keep in the decimal part.  For example,
        if 3, the number -4.56789 will be printed as -4.568.  If 0,
        the number -75.924 will be printed as "-76." (including the dot).
        If ``None``, the number will be printed in a "natural" way.  For
        example, 3.1415926 will be printed as "3.1415926".  But if the
        given number has more than 15 digits after the decimal point,
        only the first 15 digits will be preserved due to the limit of
        the double-precision system.
    show_decimal_part_if_integer : bool
        Whether to show the decimal part if the given number is an integer.
        If this is false, it overrides ``precision``.  If this is true,
        the number of digits to show will be determined by ``precision``
        (if ``precision`` is None, 2 digits will be used as per
        convention).
    use_shortform : bool
        If true, for large numbers, use notations such as "12.5k", "5.6M",
        etc. Currently, the largest supported unit is T (trillion). Numbers
        whose absolute values are larger than 1,000 trillion will be
        printed as something like "1535663T".
    use_exponent_for_large_numbers : bool
        Whether to use exponential notation (such as 1.2e+05) to represent
        large numbers. Default: False.
    large_number_threshold : int
        If ``num``'s absolute value is beyond (≥) this cutoff value, we
        consider it a large number. Default: 1,000,000.
    use_exponent_for_small_numbers : bool
        Whether to use exponential notation (such as 1.2e-05) to represent
        small numbers. Default: False.
    small_number_threshold : float
        If ``num``'s absolute value is blow (≤) this cutoff value, we
        consider it to be a small number. Default: 1 × 10⁻⁶.

    Examples
    --------
    >>> from readable_number import ReadableNumber
    >>> str(ReadableNumber(1234.567))
    >>> rn = ReadableNumber()  # alternative way to print numbers
    >>> rn.of(1234.567)
    """

    def __init__(
            self,
            num: Optional[numbers.Real] = None,
            digit_group_size: int = 3,
            digit_group_delimiter: str = ',',
            decimal_symbol: str = '.',
            precision: Optional[int] = None,
            show_decimal_part_if_integer: bool = False,
            use_shortform: bool = False,
            use_exponent_for_large_numbers: bool = False,
            large_number_threshold: int = 1_000_000,
            use_exponent_for_small_numbers: bool = False,
            small_number_threshold: float = 1e-6,
    ) -> None:
        self.num: Optional[numbers.Real] = self._convert_to_num(num)
        self.digit_group_length = digit_group_size
        self.digit_group_delimiter = digit_group_delimiter
        self.decimal_symbol = decimal_symbol
        self.precision = precision
        self.show_decimal_part_if_integer = show_decimal_part_if_integer
        self.use_shortform = use_shortform
        self.use_exponent_for_large_numbers = use_exponent_for_large_numbers
        self.large_number_threshold = large_number_threshold
        self.use_exponent_for_small_numbers = use_exponent_for_small_numbers
        self.small_number_threshold = small_number_threshold

        self._validate_input_params()

    def __repr__(self):
        return str(self.num)

    def __str__(self):
        if self.num is None:
            raise ValueError(
                'Please initialize the object with an actual number,'
                ' or use the `of()` method to pass in a number.',
            )

        if not math.isfinite(self.num):
            return str(self.num)

        if (
            self.use_exponent_for_small_numbers
            and 0 < abs(self.num) <= self.small_number_threshold
        ):
            return self._render_number_in_exponential()

        if (
            self.use_exponent_for_large_numbers
            and abs(self.num) >= self.large_number_threshold
        ):
            return self._render_number_in_exponential()

        self.num_parts = self._get_integer_and_decimal_parts(self.num)

        if self.use_shortform and abs(self.num_parts.integer_part_int) > 1_000:
            return self._render_integer_part_with_shortform()

        if self._is_integer():
            if self.show_decimal_part_if_integer:
                decimal_part = (
                    '00' if self.precision is None else '0'.zfill(self.precision)
                )
                return (
                    self._render_integer_part_in_groups()
                    + self.decimal_symbol
                    + decimal_part
                )

            return self._render_integer_part_in_groups()

        decimal_part: str
        should_carry_1_to_integer: bool
        decimal_part, should_carry_1_to_integer = self._render_decimal_part()

        neg_sign = '-' if self.num_parts.sign == -1 else ''

        return (
            neg_sign
            + self._render_integer_part_in_groups(plus_1=should_carry_1_to_integer)
            + self.decimal_symbol
            + decimal_part
        )

    def of(self, num: numbers.Real) -> str:
        """
        Print the number ``num`` in a readable format.  This method is
        useful when you don't want to repeatedly specify the same options
        when printing many numbers.

        Parameters
        ----------
        num : numbers.Real
            The number to be printed

        Returns
        -------
        str
            The number in a readable format

        Examples
        --------
        >>> from readable_number import ReadableNumber
        >>> rn = ReadableNumber()
        >>> rn.of(1234.567)
        """
        self.num = num
        return self.__str__()

    def _validate_input_params(self) -> None:
        if not isinstance(self.digit_group_length, int):
            raise TypeError('`digit_group_size` not an integer')

        if self.digit_group_length < 0:
            raise ValueError('`digit_group_size` should >= 0')

        if not isinstance(self.digit_group_delimiter, str):
            raise TypeError('`digit_group_delimiter` not a string')

        if self.digit_group_delimiter == '-':
            msg = 'Using "-" as `digit_group_delimiter` can cause ambiguity'
            raise ValueError(msg)

        if not isinstance(self.decimal_symbol, str):
            raise TypeError('`decimal_symbol` not a string')

        if self.decimal_symbol == '-':
            msg = 'Using "-" as `decimal_symbol` can cause ambiguity'
            raise ValueError(msg)

        if self.precision is not None and not isinstance(self.precision, int):
            msg = '`precision` not None and not int'
            raise TypeError(msg)

        if self.precision is not None and self.precision < 0:
            raise ValueError('`precision` should >= 0')

        if not isinstance(self.show_decimal_part_if_integer, bool):
            raise TypeError('`show_decimal_part_if_integer` not a boolean')

        if not isinstance(self.use_shortform, bool):
            raise TypeError('`use_shortform` not a boolean')

        if not isinstance(self.use_exponent_for_large_numbers, bool):
            raise TypeError('`use_exponent_for_large_numbers` not a boolean')

        if not isinstance(self.use_exponent_for_small_numbers, bool):
            raise TypeError('`use_exponent_for_small_numbers` not a boolean')

    def _render_number_in_exponential(self) -> str:
        if self.precision is not None:
            return f'{self.num:.{self.precision}e}'

        temp_result = f'{self.num:.16e}'  # 16: max precision in 64-bit system
        base_part_str, exp_part_str = temp_result.split('e')
        base_part_float = float(base_part_str)
        assert abs(base_part_float) < 10, 'Internal error; please contact the authors'
        processed = str(ReadableNumber(base_part_float, precision=None))
        return processed + 'e' + exp_part_str

    def _render_integer_part_with_shortform(self) -> str:
        num_digits = len(str(abs(self.num_parts.integer_part_int)))
        tier = (num_digits - 1) // 3
        tier = min(tier, MAX_TIER)
        unit_name = METRIC_PREFIX_LOOKUP[tier]

        prec_: int = 0 if self.precision is None else self.precision
        nn: int = min(prec_, MAX_DIGITS_IN_DOUBLE_PRECISION)
        float_part = round(
            self.num / 10 ** (tier * 3),
            ndigits=self.precision,
        )
        float_part_str = '{:.{prec}f}'.format(
            float_part,
            prec=nn,
        )

        return float_part_str + unit_name

    def _render_integer_part_in_groups(self, plus_1: bool = False) -> str:
        counter = 0
        new_chars = []

        integer_part_str = str(
            self.num_parts.integer_part_int + (1 if plus_1 else 0),
        )

        for char in integer_part_str[::-1]:
            counter += 1
            new_chars.append(char)
            if self.digit_group_length > 0 and counter % self.digit_group_length == 0:
                new_chars.append(self.digit_group_delimiter)

        if new_chars[-1] == '-' and new_chars[-2] == self.digit_group_delimiter:
            new_chars.pop(-2)
        elif new_chars[-1] == self.digit_group_delimiter:
            new_chars.pop(-1)

        return ''.join(new_chars[::-1])

    def _render_decimal_part(self) -> Tuple[str, bool]:
        """
        Render the decimal part.

        The 2nd return value means whether to carry to the integer part.
        """
        if self.precision is None:  # "natural" way to display
            nn = min(
                MAX_DIGITS_IN_DOUBLE_PRECISION,  # cap at this many digits
                # if fewer than the upper bound, display naturally:
                len(self.num_parts.decimal_part_str),
            )
        else:
            nn = min(self.precision, MAX_DIGITS_IN_DOUBLE_PRECISION)

        rounded_str: str = '{:.{prec}f}'.format(
            self.num_parts.decimal_part_float,
            prec=nn,
        )
        rounded: float = float(rounded_str)

        decimal_part: str = '' if nn == 0 else rounded_str.split('.')[1][:nn]
        should_carry_1: bool = rounded >= 1

        return decimal_part, should_carry_1

    def _is_integer(self) -> bool:
        return int(self.num) == self.num

    @classmethod
    def _convert_to_num(cls, num: Any) -> numbers.Real:
        if isinstance(num, (float, int, type(None))):
            return num

        if isinstance(num, complex):
            raise TypeError('Complex numbers are not supported.')

        return float(num)  # it would naturally fail if `num` is not valid

    @classmethod
    def _get_integer_and_decimal_parts(
            cls,
            num: Union[float, int],
    ) -> _IntegerAndDecimalParts:
        if num > 0:
            sign = 1
            neg_sign = ''
        elif num < 0:
            sign = -1
            neg_sign = '-'
        else:
            sign = 0
            neg_sign = ''

        if isinstance(num, int):
            return _IntegerAndDecimalParts(
                integer_part_str=str(num),
                integer_part_int=num,
                decimal_part_str='',
                decimal_part_float=0.0,
                sign=sign,
            )

        string_representation: str = str(num)

        if string_representation[0] == '-':
            string_representation = string_representation[1:]

        if 'e-' in string_representation:  # this means |num| is small
            if abs(num) > 1:
                raise ValueError(f'Internal error: num ({num}) is more than 1')

            mantissa_str, exponent_str = string_representation.split('e')
            mantissa_str_parts = mantissa_str.split('.')

            decimal_part_str = mantissa_str_parts[0].zfill(abs(int(exponent_str)))
            if len(mantissa_str_parts) > 1:
                decimal_part_str += mantissa_str_parts[1]

            return _IntegerAndDecimalParts(
                integer_part_str='0',
                integer_part_int=0,
                decimal_part_str=decimal_part_str,
                decimal_part_float=float(neg_sign + '0.' + decimal_part_str),
                sign=sign,
            )

        if 'e+' in string_representation:  # this means |num| is big
            integer_val: int = int(num)
            decimal_val: float = num % 1
            decimal_str = '' if decimal_val == 0 else str(decimal_val).split('.')[1]

            return _IntegerAndDecimalParts(
                integer_part_str=str(integer_val),
                integer_part_int=integer_val,
                decimal_part_str=decimal_str,
                decimal_part_float=decimal_val,
                sign=sign,
            )

        if 'e' in string_representation:
            raise ValueError('Edge case encountered; please contact the authors')

        integer_part_str, decimal_part_str = string_representation.split('.')
        return _IntegerAndDecimalParts(
            integer_part_str=integer_part_str,
            integer_part_int=int(integer_part_str),
            decimal_part_str=decimal_part_str,
            decimal_part_float=float('0.' + decimal_part_str),
            sign=sign,
        )
