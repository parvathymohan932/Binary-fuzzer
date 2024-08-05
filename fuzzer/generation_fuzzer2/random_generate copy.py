import struct
import random
import re
def random_based_on_size(size, endianness):
    byteorder = 'little' if endianness == 'le' else 'big'
    random_number = random.randint(0, 2**(size * 8) - 1)
    return random_number.to_bytes(size, byteorder=byteorder)

def random_based_on_type(size, type_field, endianness, encoding=None):

    if type_field=='u1':
        return struct.pack(f'{endianness}B', random.randint(0, 255))
    elif type_field == 'u2':
        return struct.pack(f'{endianness}H', random.randint(0, 65535))
    elif type_field == 'u4':
        return struct.pack(f'{endianness}I', random.randint(0, 4294967295))
    elif type_field == 'u8':
        return struct.pack(f'{endianness}Q', random.randint(0, 18446744073709551615))
    # elif type_field=='b1':
    #     return struct.pack(f'{endianness}B', random.randint(0, 1))
    # elif type_field=='b4':
    #     value = random.randint(0, 15)
    #     return struct.pack(f'{endianness}B', value & 0b1111)
    # elif type_field == 'b2':
    #     value = random.randint(0, 3)
    #     return struct.pack(f'{endianness}B', value & 0b11)
    # elif type_field=='b5':
    #     value = random.randint(0, 31)
    #     return struct.pack(f'{endianness}B', value & 0b11111)
    elif re.match(r'b\d+', type_field):
        num_bits = int(type_field[1:])
        if num_bits <= 8:
            value = random.randint(0, (1 << num_bits) - 1)
            return struct.pack(f'{endianness}B', value)
        elif num_bits <= 16:
            value = random.randint(0, (1 << num_bits) - 1)
            return struct.pack(f'{endianness}H', value)
        elif num_bits <= 32:
            value = random.randint(0, (1 << num_bits) - 1)
            return struct.pack(f'{endianness}I', value)
        elif num_bits <= 64:
            value = random.randint(0, (1 << num_bits) - 1)
            return struct.pack(f'{endianness}Q', value)
        else:
            raise ValueError(f"Unsupported bit length: {num_bits}")
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
    

def convert_value_to_type(value, type_field, endianness, encoding=None, size=None):
    print(f"Converting value: {value}, type_field: {type_field}, endianness: {endianness}")
    if type_field == 'u1':
        val= struct.pack(f'{endianness}B', value)
        print("Val is ", val)
        return val
    elif type_field == 'b1':
        return struct.pack(f'{endianness}B', value & 0b1)
    elif type_field == 'b4':
        return struct.pack(f'{endianness}B', value & 0b1111)
    elif type_field == 'b2':
        return struct.pack(f'{endianness}B', value & 0b11)
    elif type_field == 'b5':
        return struct.pack(f'{endianness}B', value & 0b11111)
    elif type_field == 'u2':
        return struct.pack(f'{endianness}H', value)
    elif type_field == 'u4':
        return struct.pack(f'{endianness}I', value)
    elif type_field == 'u8':
        return struct.pack(f'{endianness}Q', value)
    elif type_field == 's2':
        return struct.pack(f'{endianness}h', value)
    elif type_field == 's4':
        return struct.pack(f'{endianness}i', value)
    elif type_field == 's8':
        return struct.pack(f'{endianness}q', value)
    elif type_field == 'f4':
        return struct.pack(f'{endianness}f', value)
    elif type_field == 'f8':
        return struct.pack(f'{endianness}d', value)
    elif type_field == 'str':
        value = str(value)
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        if encoding is None:
            encoding = 'ascii'  # Default encoding if none specified
        encoded_value = str(value).encode(encoding)
        if size:
            if len(encoded_value) > size:
                return encoded_value[:size]  # Truncate if too long
            else:
                return encoded_value.ljust(size, b'\x00')  # Pad with null bytes if too short
        else:
            return encoded_value
    else:
        return b''

