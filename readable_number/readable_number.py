import copy
import math
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto
from types import MappingProxyType
from typing import Any, Optional, Tuple, Union

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

MSG_CONTACT_US = 'Please contact the authors.'


class _DecimalPartRenderingMethod(Enum):
    NATURAL = auto()
    HARD_PRECISION = auto()
    SIGNIFICANT_FIGURES = auto()


class InternalError(Exception):
    """For cases that should not have happened"""


@dataclass
class _IntegerAndDecimalParts:
    integer_part_str: str
    integer_part_int: int
    decimal_part_str: str
    decimal_part_float: float
    sign: int
    multiplier: int = 0  # to keep track of numbers with small absolute values


class ReadableNumber:
    """
    A class to hold a number for human-readable printing.

    Showing an arbitrary number in a human-readable way is far from trivial,
    because real-world numbers come in various forms. This is why there are
    many options in this class for users to tune. That said, the default
    options of this class generally give a pretty good result.

    Parameters
    ----------
    num : Optional[Union[float, int]]
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
    precision : Optional[int]
        How many digits to keep in the decimal part.  For example,
        if 3, the number -4.56789 will be printed as -4.568.  If 0,
        the number -75.924 will be printed as "-76." (including the dot).
        If ``None``, the number will be printed in a "natural" way.  For
        example, 3.1415926 will be printed as "3.1415926".  But if the
        given number has more than 15 digits after the decimal point,
        only the first 15 digits will be preserved due to the limit of
        the double-precision system.
    significant_figures : Optional[int]
        How many significant figures to display. "Significant figures"
        and "precision" are different concepts.  Please refer to
        https://en.wikipedia.org/wiki/Significant_figures for more details.
        If one of ``precision`` and ``significant_figures`` is not ``None``,
        the other must be ``None``.  If both are ``None``, the given number
        will be printed in a "natural" way.
    apply_sig_fig_only_to_numbers_less_than_1 : bool
        Apm
    show_decimal_part_if_integer : bool
        Whether to show the decimal part if the given number is an integer.
        If this is false, it overrides ``precision``.  If this is true,
        the number of digits to show will be determined by ``precision``
        (if ``precision`` is None, 2 digits will be used as per
        convention). Default: False.
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
            num: Optional[Union[float, int]] = None,
            digit_group_size: int = 3,
            digit_group_delimiter: str = ',',
            decimal_symbol: str = '.',
            precision: Optional[int] = None,
            significant_figures: Optional[int] = None,
            apply_sig_fig_only_to_numbers_less_than_1: bool = True,
            show_decimal_part_if_integer: bool = False,
            use_shortform: bool = False,
            use_exponent_for_large_numbers: bool = False,
            large_number_threshold: int = 1_000_000,
            use_exponent_for_small_numbers: bool = False,
            small_number_threshold: float = 1e-6,
    ) -> None:
        self.num: Optional[Union[float, int]] = self._convert_to_num(num)
        self.digit_group_length = digit_group_size
        self.digit_group_delimiter = digit_group_delimiter
        self.decimal_symbol = decimal_symbol
        self.precision = precision
        self.significant_figures = significant_figures
        self.apply_sig_fig_only_to_numbers_less_than_1 = (
            apply_sig_fig_only_to_numbers_less_than_1
        )
        self.show_decimal_part_if_integer = show_decimal_part_if_integer
        self.use_shortform = use_shortform
        self.use_exponent_for_large_numbers = use_exponent_for_large_numbers
        self.large_number_threshold = large_number_threshold
        self.use_exponent_for_small_numbers = use_exponent_for_small_numbers
        self.small_number_threshold = small_number_threshold

        self._validate_input_params()

    def __deepcopy__(self, memo: Any) -> 'ReadableNumber':
        return self.deepcopy()

    def __repr__(self) -> str:
        return str(self.num)

    def __str__(self) -> str:
        if self.num is None:
            raise ValueError(
                'Please initialize the object with an actual number,'
                ' or use the `of()` method to pass in a number.',
            )

        if not math.isfinite(self.num):
            return str(self.num)

        # We need to put this before self.use_exponent_for_small_numbers
        # and self.use_exponent_for_large_numbers, because when we show
        # very large/small numbers as exponents, we want to control
        # the significant digits in the result.
        if (
            self.significant_figures is not None
            and not self.apply_sig_fig_only_to_numbers_less_than_1
            and math.fabs(self.num) >= 1
        ):
            rn_copy = self.deepcopy()  # to inherit all original configs
            rn_copy.num = float(f'{self.num:.{self.significant_figures}g}')
            rn_copy.significant_figures = None  # to prevent infinite recursion
            return str(rn_copy)

        if (
            self.use_exponent_for_small_numbers
            and 0 < math.fabs(self.num) <= self.small_number_threshold
        ):
            return self._render_number_in_exponential()

        if (
            self.use_exponent_for_large_numbers
            and math.fabs(self.num) >= self.large_number_threshold
        ):
            return self._render_number_in_exponential()

        self.num_parts = self._get_integer_and_decimal_parts(self.num)

        if self.use_shortform and abs(self.num_parts.integer_part_int) > 1_000:
            return self._render_integer_part_with_shortform()

        decimal_part: str
        if self._is_integer():
            if self.show_decimal_part_if_integer:
                decimal_part = (
                    '00'
                    if self.precision is None
                    else '0'.zfill(self.precision)
                )
                return (
                    self._render_integer_part_in_groups()
                    + self.decimal_symbol
                    + decimal_part
                )

            return self._render_integer_part_in_groups()

        carry: int  # https://en.wikipedia.org/wiki/Carry_(arithmetic)
        decimal_part, carry = self._render_decimal_part()

        return (
            self._render_integer_part_in_groups(carry=carry)
            + self.decimal_symbol
            + decimal_part
        )

    def of(self, num: Union[float, int]) -> str:
        """
        Print the number ``num`` in a readable format.  This method is
        useful when you don't want to repeatedly specify the same options
        when printing many numbers.

        Parameters
        ----------
        num : Union[float, int]
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

    def deepcopy(self) -> 'ReadableNumber':
        """Make a deep copy of itself"""
        new_instance = self.__class__.__new__(self.__class__)
        new_instance.__dict__ = copy.deepcopy(self.__dict__)
        return new_instance

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

        if self.precision is not None and self.significant_figures is not None:
            raise ValueError(
                'Only one of `precision` and `significant_figures` can be non-None.'
            )

        if self.precision is not None and self.precision < 0:
            raise ValueError('`precision` should >= 0')

        if (
            self.significant_figures is not None
            and self.significant_figures <= 0
        ):
            raise ValueError('`significant_figures` should > 0')

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

        if self.significant_figures is not None:
            return f'{self.num:{self.significant_figures - 1}e}'

        temp_result = f'{self.num:.16e}'  # 16: max precision in 64-bit system
        base_part_str, exp_part_str = temp_result.split('e')
        base_part_float = float(base_part_str)
        assert abs(base_part_float) < 10, f'Internal error. {MSG_CONTACT_US}'
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

    def _render_integer_part_in_groups(self, carry: int = 0) -> str:
        counter = 0
        new_chars = []

        # We do `int(self.num_parts.integer_part_str)` because
        # self.num_parts.integer_part_int may be negative, but we don't want
        # to include the negative sign here. The negative sign is handled
        # below (later in this function).
        integer_part_str = str(int(self.num_parts.integer_part_str) + carry)

        for char in integer_part_str[::-1]:
            counter += 1
            new_chars.append(char)
            if (
                self.digit_group_length > 0
                and counter % self.digit_group_length == 0
            ):
                new_chars.append(self.digit_group_delimiter)

        if (
            new_chars[-1] == '-'
            and new_chars[-2] == self.digit_group_delimiter
        ):
            new_chars.pop(-2)
        elif new_chars[-1] == self.digit_group_delimiter:
            new_chars.pop(-1)

        temp_result: str = ''.join(new_chars[::-1])

        if self.num_parts.sign == -1 and not temp_result.startswith('-'):
            return '-' + temp_result

        return temp_result

    def _render_decimal_part(self) -> Tuple[str, int]:
        """
        Render the decimal part.

        The 2nd return value means the amount to carry.

        See more: https://en.wikipedia.org/wiki/Carry_(arithmetic)
        """
        self._sanity_check_for_render_decimal_part()

        method: _DecimalPartRenderingMethod

        if self.significant_figures is not None:
            if math.fabs(self.num) >= 1:  # type: ignore[arg-type]
                # This means `self.significant_figures` has no effect,
                # because |num| ≥ 1
                method = _DecimalPartRenderingMethod.NATURAL
            else:
                method = _DecimalPartRenderingMethod.SIGNIFICANT_FIGURES
        elif self.precision is not None:
            method = _DecimalPartRenderingMethod.HARD_PRECISION
        else:  # both precision and significant_figures are None
            method = _DecimalPartRenderingMethod.NATURAL

        rounded_str: str
        decimal_part: str
        rounded: float
        carry: int

        if _DecimalPartRenderingMethod.SIGNIFICANT_FIGURES == method:
            _num: float = self.num_parts.decimal_part_float  # shorthand
            rounded_str = f'{_num:.{self.significant_figures}g}'

            if 'e' not in rounded_str:
                decimal_part = rounded_str.split('.')[1]
            else:
                rn_copy: 'ReadableNumber' = self.deepcopy()
                rn_copy.num = float(rounded_str)
                rn_copy.significant_figures = None  # to stop inf. recursion
                decimal_part = str(rn_copy).split('.')[1]

            rounded = float(rounded_str)
            carry = 1 if rounded >= 10**self.num_parts.multiplier else 0
        else:
            if _DecimalPartRenderingMethod.NATURAL == method:
                nn = min(
                    MAX_DIGITS_IN_DOUBLE_PRECISION,  # cap at this many digits
                    # if fewer than the upper bound, display naturally:
                    len(self.num_parts.decimal_part_str),
                )
            else:  # _DecimalPartRenderingMethod.HARD_PRECISION
                nn = min(self.precision, MAX_DIGITS_IN_DOUBLE_PRECISION)  # type: ignore[type-var, assignment]

            rounded_str = '{:.{prec}f}'.format(
                self.num_parts.decimal_part_float,
                prec=nn,
            )

            rounded = float(rounded_str)
            decimal_part = '' if nn == 0 else rounded_str.split('.')[1][:nn]
            carry = 1 if rounded >= 10**self.num_parts.multiplier else 0

        if decimal_part.startswith('-'):
            raise InternalError(f"Shouldn't have happened. {MSG_CONTACT_US}")

        return self._post_process_decimal_part(decimal_part, carry)

    def _sanity_check_for_render_decimal_part(self) -> None:
        if self.precision is not None and self.significant_figures is not None:
            raise InternalError(f'Both cannot be non-None. {MSG_CONTACT_US}')

    def _post_process_decimal_part(
            self,
            decimal_part: str,
            carry: int,
    ) -> Tuple[str, int]:
        decimal_part_: str = '0' * self.num_parts.multiplier + decimal_part

        if self.precision is not None:
            precision_ = self.precision
        elif self.significant_figures is not None:
            precision_ = self.significant_figures + self.num_parts.multiplier
        else:
            precision_ = None

        decimal_part__: str = self._round_digits(decimal_part_, precision_)

        overflow_happened: bool
        if precision_ is None:
            overflow_happened = len(decimal_part__) > len(decimal_part_)
        else:
            overflow_happened = len(decimal_part__) > max(
                len(decimal_part_), precision_
            )

        if overflow_happened:
            carry += 1
            decimal_part_final = decimal_part__[:1]
        else:
            decimal_part_final = decimal_part__

        return decimal_part_final, carry

    def _is_integer(self) -> bool:
        return int(self.num) == self.num  # type: ignore[arg-type]

    @classmethod
    def _convert_to_num(cls, num: Any) -> Optional[Union[float, int]]:
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

        mantissa, exponent = cls._decompose_float(num)
        how_many_leading_0s_after_decimal_point: int = -exponent - 1

        if math.fabs(num) < 0.01:
            multiplier = how_many_leading_0s_after_decimal_point

            # More accurate than "num *= 10 ** multiplier"
            num = float(Decimal(num) * Decimal(10**multiplier))
        else:
            multiplier = 0

        string_representation: str = str(num)

        if string_representation[0] == '-':
            string_representation = string_representation[1:]

        if isinstance(num, int):
            return _IntegerAndDecimalParts(
                integer_part_str=string_representation,
                integer_part_int=num,
                decimal_part_str='',
                decimal_part_float=0.0,
                sign=sign,
                multiplier=multiplier,
            )

        if 'e-' in string_representation:  # this means |num| is small
            if math.fabs(num) > 1:
                raise InternalError(f'`num` ({num}) is more than 1')

            mantissa_str, exponent_str = string_representation.split('e')
            mantissa_str_parts = mantissa_str.split('.')

            decimal_part_str = mantissa_str_parts[0].zfill(
                abs(int(exponent_str))
            )
            if len(mantissa_str_parts) > 1:
                decimal_part_str += mantissa_str_parts[1]

            return _IntegerAndDecimalParts(
                integer_part_str='0',
                integer_part_int=0,
                decimal_part_str=decimal_part_str,
                decimal_part_float=float(neg_sign + '0.' + decimal_part_str),
                sign=sign,
                multiplier=multiplier,
            )

        if 'e+' in string_representation:  # this means |num| is big
            integer_val: int = int(num)
            decimal_val: float = num % 1
            decimal_str = (
                '' if decimal_val == 0 else str(decimal_val).split('.')[1]
            )

            return _IntegerAndDecimalParts(
                integer_part_str=str(integer_val),
                integer_part_int=integer_val,
                decimal_part_str=decimal_str,
                decimal_part_float=decimal_val,
                sign=sign,
                multiplier=multiplier,
            )

        if 'e' in string_representation:
            raise InternalError(
                f'"e" in `string_representation`. {MSG_CONTACT_US}'
            )

        integer_part_str, decimal_part_str = string_representation.split('.')
        return _IntegerAndDecimalParts(
            integer_part_str=integer_part_str,
            integer_part_int=int(integer_part_str),
            decimal_part_str=decimal_part_str,
            decimal_part_float=float('0.' + decimal_part_str),
            sign=sign,
            multiplier=multiplier,
        )

    @classmethod
    def _decompose_float(cls, num: Union[float, int]) -> Tuple[float, int]:
        dec = Decimal(math.fabs(num))
        exponent = cls._get_base_10_exp(dec)
        mantissa = float(dec.scaleb(-exponent).normalize())
        if mantissa == 10.0:
            mantissa = 1.0
            exponent += 1

        return mantissa, exponent

    @classmethod
    def _get_base_10_exp(cls, decimal_: Decimal) -> int:
        sign, digits, exponent = decimal_.as_tuple()
        return len(digits) + exponent - 1  # type: ignore[operator]

    @classmethod
    def _round_digits(cls, digits: str, precision: Optional[int]) -> str:
        """For example:

        * digits = '00013245', precision = 5  --> output: '00013'
        * digits = '00013745', precision = 5  --> output: '00014'
        * digits = '00019745', precision = 5  --> output: '00020'
        * digits = '00019745', precision = 10 --> output: '0001974500'
        """
        if precision == len(digits) or digits == '':
            return digits

        if precision is None:  # "natural" way to round: strip 0
            return digits.rstrip('0')

        if precision < 0:
            raise InternalError(f'`precision` should >= 0. {MSG_CONTACT_US}')

        if precision == 0:
            return ''

        if precision > len(digits):
            how_many_0s_to_add: int = precision - len(digits)
            return digits + '0' * how_many_0s_to_add

        digits_to_keep: str = digits[:precision]
        digits_to_throw_away: str = digits[precision:]
        should_carry: bool = digits_to_throw_away[0] >= '5'
        if should_carry:
            digits_to_keep = cls._carry(digits_to_keep)

        return digits_to_keep

    @classmethod
    def _carry(cls, digits: str) -> str:
        if digits == '':
            return '1'

        last_digit: str = digits[-1]
        if last_digit < '9':
            return digits[:-1] + chr(ord(last_digit) + 1)

        return cls._carry(digits[:-1]) + '0'
