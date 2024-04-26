import yaml
import random
import struct

def pack_list(values, endianness):
    binary_data = b''  

    for value in values:
        if isinstance(value, int):
            binary_data += struct.pack(f'{endianness}B', value)  # Use 'B' for unsigned byte
        elif isinstance(value, float):
            binary_data += struct.pack(f'{endianness}d', value)  
        elif isinstance(value, str):
            string_bytes = value.encode('utf-8')
            binary_data += struct.pack(f'{endianness}{len(string_bytes)}s', string_bytes)

    return binary_data


def pack_value(value, endianness):
    if isinstance(value, int):
        binary_data = struct.pack(f'{endianness}B', value)  # Use 'H' for unsigned short integer
    elif isinstance(value, float):
        binary_data = struct.pack(f'{endianness}d', value)  
    elif isinstance(value, str):
        string_bytes = value.encode('utf-8')
        binary_data = struct.pack(f'{endianness}{len(string_bytes)}s', string_bytes)

    return binary_data


def handle_meta(meta):

    for key, value in meta.items():
        if key == 'file-extension':
            file_extension = value
        elif key == 'endian':
            endianness = value
    return endianness, file_extension

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
    elif type_field == 'f2':
        return struct.pack(f'{endianness}e', random.uniform(1e-45, 3.4028235e+38))
    elif type_field == 'f4':
        return struct.pack(f'{endianness}f', random.uniform(1.17549435e-38, 3.4028235e+38))
    elif type_field == 'f8':
        return struct.pack(f'{endianness}d', random.uniform(2.2250738585072014e-308, 1.7976931348623157e+308))
    elif type_field == 'str':
        if encoding == 'UTF-8':
            # Generate random ASCII characters directly to avoid null bytes
            return ''.join(chr(random.randint(33, 126)) for _ in range(size)).encode('utf-8')
        elif encoding == 'ASCII':
            return ''.join(chr(random.randint(33, 126)) for _ in range(size)).encode('ascii')
        else:
            return ''.join(chr(random.randint(33, 126)) for _ in range(size)).encode('ascii')
    else:
        return b''
def handle_seq(seq, endian, parent):
    expansion = b''

    for item in seq:
        type = None
        size = 0
        encoding = None
        endianness= '>' if endian == 'le' else '<'
        for key, value in item.items():
            if key == 'contents':
                expansion += pack_list(value,endianness)
            elif key == 'size':
                size = value
            elif key == 'type':
                type = value
            elif key == 'encoding':
                encoding = value
            elif key=='valid':
                expansion+= bytes(value)

        if type is None:
            expansion += random_based_on_size(size, endianness)
        elif type in ['u2', 'u4', 'u8', 's2', 's4', 's8', 'str', 'f2', 'f4', 'f8']:
            expansion += random_based_on_type(size, type, endianness, encoding)
        else:
            expansion += handle_type(parent['types'],endian)
    return expansion
def handle_type(types,endianness):
    expansion = b''
    for key, value in types.items():
        if value == 'seq':
            expansion += handle_seq(types[key]['seq'], endianness, types[key])
    return expansion

# Specify the path to your YAML file
file_path = '/Users/darshanadask/mini_project/Working_area/week2/animal_record.ksy'

# Read the YAML data from the file
with open(file_path, 'r') as file:
    yaml_data = file.read()

# Load YAML data
data_tree = yaml.safe_load(yaml_data)

# Call the functions with explicit parent information


# Write to file

for i in range(0,10):
  endianness, file_extension = handle_meta(data_tree['meta'])
  expansion=handle_seq(data_tree['seq'], endianness,data_tree)
  if file_extension:
      with open(f"output{i}.{file_extension}", 'wb') as file:
          file.write(expansion)
