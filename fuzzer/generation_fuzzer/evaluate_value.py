import struct

def convert_with_endianness(value, endian='=', encoding='utf-8'):
    """
    Convert the evaluated value to the specified data type.

    Args:
        value: The evaluated value to be converted.
        endian (str, optional): The endianness of the data. Default is native endianness ('=').
        encoding (str, optional): The encoding to use for string conversion. Default is 'utf-8'.

    Returns:
        The converted value.
    """
    print("Value is ", value)
    if isinstance(value, str):
        return value.encode(encoding)
    elif isinstance(value, bytes):
        return value.decode(encoding)
    else:
       
        format_string = f"{endian}{len(value)}s"
        return struct.unpack(format_string, bytearray(value))[0]

def convert_to_type(value, data_type=None, endian='=', encoding='utf-8'):
    """
    Convert the evaluated value to the specified data type.

    Args:
        value: The evaluated value to be converted.
        data_type (str, optional): The desired data type. Supported types are 'u1', 'u2', 'u4', 'u8',
            's1', 's2', 's4', 's8', 'f2', 'f4', 'f8', and 'str'. Default is None.
        endian (str, optional): The endianness of the data. Default is native endianness ('=').
        encoding (str, optional): The encoding to use for string conversion. Default is 'utf-8'.

    Returns:
        The converted value.
    """
    if data_type is None:
        return convert_with_endianness(value, endian, encoding)

    if data_type == 'str':
        return value.decode(encoding)

    format_dict = {
        'u1': ('B', 1),
        'u2': ('H', 2),
        'u4': ('I', 4),
        'u8': ('Q', 8),
        's1': ('b', 1),
        's2': ('h', 2),
        's4': ('i', 4),
        's8': ('q', 8),
        'f2': ('e', 2),
        'f4': ('f', 4),
        'f8': ('d', 8),
    }

    format_code, size = format_dict[data_type]
    format_string = f"{endian}{format_code}"

    #if len(value) != size:
    #    raise ValueError(f"Value size {len(value)} does not match expected size {size} for data type '{data_type}'.")

    return struct.unpack(format_string, bytearray(value))[0]

# Example usage:
# converted_value = convert_to_type(b'\x0A\x00\x00\x00', endian='<')
# converted_value = convert_to_type(b'\x0A\x00\x00\x00', endian='>')  # big-endian
'''
def integer_from_binary(binary_string, endianness):
    byteorder = 'little' if endianness == 'le' else 'big'
    return int.from_bytes(binary_string, byteorder=byteorder)
'''

def max_value_for_type(type_str):
    max_values = {
        'u1': 0xFF,   
        'u2': 0xFFFF, 
        'u4': 0xFFFFFFFF, 
        'u8': 0xFFFFFFFFFFFFFFFF, 
        's1': 0x7F,   
        's2': 0x7FFF, 
        's4': 0x7FFFFFFF, 
        's8': 0x7FFFFFFFFFFFFFFF, 
    }
    if type_str in max_values:
        return max_values[type_str]
    else:
        raise ValueError("Invalid type string. Type must be one of: u1, u2, u4, u8, s1, s2, s4, s8.")