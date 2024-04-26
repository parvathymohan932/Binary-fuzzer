import struct
import random
def random_based_on_size(size, endianness):
    byteorder = 'little' if endianness == 'le' else 'big'
    random_number = random.randint(0, 2**(size * 8) - 1)
    return random_number.to_bytes(size, byteorder=byteorder)

def random_based_on_type(size, type_field, endianness, encoding=None):
    if type_field == 'u2':
        return struct.pack(f'{endianness}H', random.randint(0, 65535))
    elif type_field == 'u4':
        return struct.pack(f'{endianness}I', random.randint(0, 4294967295))
    elif type_field == 'u8':
        return struct.pack(f'{endianness}Q', random.randint(0, 18446744073709551615))
    elif type_field == 's2':
        return struct.pack(f'{endianness}h', random.randint(-32768, 32767))
    elif type_field == 's4':
        return struct.pack(f'{endianness}i', random.randint(-2147483648, 2147483647))
    elif type_field == 's8':
        return struct.pack(f'{endianness}q', random.randint(-9223372036854775808, 9223372036854775807))
    elif type_field == 'f4':
        return struct.pack(f'{endianness}f', random.uniform(1.17549435e-38, 3.4028235e+38))
    elif type_field == 'f8':
        return struct.pack(f'{endianness}d', random.uniform(2.2250738585072014e-308, 1.7976931348623157e+308))
    elif type_field == 'str':
        if encoding == 'UTF-8':
            return ''.join(chr(random.randint(33, 126)) for _ in range(size)).encode('utf-8')
        elif encoding == 'ASCII':
            return ''.join(chr(random.randint(33, 126)) for _ in range(size)).encode('ascii')
        else:
            return ''.join(chr(random.randint(33, 126)) for _ in range(size)).encode('ascii')
    else:
        return b''