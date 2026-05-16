from __future__ import annotations

from typing import Sequence, Union

BitInput = Union[str, Sequence[int]]


def _normalize_bits(bits: BitInput) -> str:
    if isinstance(bits, str):
        normalized = bits.strip()
    else:
        normalized = "".join(str(int(b)) for b in bits)
    if not normalized:
        raise ValueError("Bit string must not be empty.")
    if any(ch not in "01" for ch in normalized):
        raise ValueError("Bit string must contain only 0 or 1.")
    return normalized


def binary_to_integer(genotype: BitInput) -> int:
    binary = _normalize_bits(genotype)
    return int(binary, 2)


def integer_to_binary(value: int, bits: int) -> str:
    if bits <= 0:
        raise ValueError("bits must be a positive integer.")
    if value < 0:
        raise ValueError("value must be non-negative.")
    return format(value, f"0{bits}b")
