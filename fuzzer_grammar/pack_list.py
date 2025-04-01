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