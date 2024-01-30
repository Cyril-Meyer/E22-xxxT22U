def set_bit(x: bytearray, bit_index: int, bit_value: bool):
    mask = 1 << bit_index
    if bit_value:
        x |= mask
    else:
        x &= ~mask
    return x


def set_bits(x: bytearray, bit_indexes, bit_values):
    assert len(bit_indexes) == len(bit_values)
    for i in range(len(bit_indexes)):
        x = set_bit(x, bit_indexes[i], bit_values[i])
    return x
