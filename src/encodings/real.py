from __future__ import annotations

from .binary import BitInput, _normalize_bits


def binary_to_real(genotype: BitInput, lower: float, upper: float) -> float:
    binary = _normalize_bits(genotype)
    if upper == lower:
        raise ValueError("upper and lower bounds must differ.")
    integer = int(binary, 2)
    span = (2 ** len(binary)) - 1
    return lower + integer * (upper - lower) / span


def real_to_binary(value: float, lower: float, upper: float, bits: int) -> str:
    if bits <= 0:
        raise ValueError("bits must be a positive integer.")
    if upper == lower:
        raise ValueError("upper and lower bounds must differ.")
    span = (2 ** bits) - 1
    scaled = round((value - lower) * span / (upper - lower))
    scaled = max(0, min(span, scaled))
    return format(int(scaled), f"0{bits}b")
