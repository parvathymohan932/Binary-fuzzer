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

def binary_to_int(value, endianness):
    try:
        if endianness == 'le':
            # Little-endian byte order
            value_int = int.from_bytes(value, byteorder='little')
        else:
            # Big-endian byte order
            value_int = int.from_bytes(value, byteorder='big')
        return value_int
    except Exception as e:
        print(f"Error occurred while converting binary to integer: {e}")
        return 0


# def binary_to_int(value, endianness):
    
#     try:
#         # Ensure the input value is bytes
#         if not isinstance(value, bytes):
#             raise ValueError("Input value must be a byte sequence")

#         if endianness == 'le':
#             # Little-endian byte order
#             value_int = int.from_bytes(value, byteorder='little')
#         elif endianness == 'be':
#             # Big-endian byte order
#             value_int = int.from_bytes(value, byteorder='big')
#         else:
#             raise ValueError("Invalid endianness specified. Use 'le' for little-endian or 'be' for big-endian.")

#         return value_int
#     except Exception as e:
#         raise ValueError(f"Error occurred while converting binary to integer: {e}")


def pack_value(value, endian,item_type=None):
  if item_type == "u1":
          return struct.pack(f'{endian}B', value)
  elif item_type == "u2":
      return struct.pack(f'{endian}H', value)
  elif item_type == "u4":
      return struct.pack(f'{endian}I', value)
  elif item_type == "u8":
      return struct.pack(f'{endian}Q', value)
#  elif item_type.startswith("enum"):
#      return random.choice(list(enum_values))
  elif item_type == 's2':
      return struct.pack(f'{endian}h', value)
  elif item_type == 's4':
      return struct.pack(f'{endian}i', value)
  elif item_type == 's8':
      return struct.pack(f'{endian}q', value)
  elif item_type == 'f4':
      return struct.pack(f'{endian}f', value)
  elif item_type == 'f8':
      return struct.pack(f'{endian}d', value)
#  elif item_type == 'str':
#      if encoding == 'UTF-8':
#          return ''.join(chr(random_key) for _ in range(size)).encode('utf-8')
#      elif encoding == 'ASCII':
#          return ''.join(chr(random_key) for _ in range(size)).encode('ascii')
#      else:
#          return ''.join(chr(random_key) for _ in range(size)).encode('ascii')
  elif item_type is None:
      return int_to_binary(value, endian)
  else:
      raise ValueError(f"Unsupported item type '{item_type}'.")

def int_to_binary(num, endian='le'):
    if num < 0:
        raise ValueError("Input must be a non-negative integer")
    elif num == 0:
        return b'\x00'
    else:
        # Pack the integer into binary data using struct
        if endian == 'le':
            binary_data = struct.pack('<Q', num)  # Q format represents an unsigned long long (8 bytes) in little-endian
        elif endian == 'be':
            binary_data = struct.pack('>Q', num)  # >Q format represents an unsigned long long (8 bytes) in big-endian
        else:
            raise ValueError("Invalid endianness. Use 'little' or 'big'.")
        return binary_data
