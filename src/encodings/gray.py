from __future__ import annotations

from .binary import BitInput, _normalize_bits


def binary_to_gray(binary: BitInput) -> str:
    b = _normalize_bits(binary)
    gray = [b[0]]
    for i in range(1, len(b)):
        gray.append(str(int(b[i - 1]) ^ int(b[i])))
    return "".join(gray)


def gray_to_binary(gray: BitInput) -> str:
    g = _normalize_bits(gray)
    binary = [g[0]]
    for i in range(1, len(g)):
        binary.append(str(int(binary[i - 1]) ^ int(g[i])))
    return "".join(binary)
