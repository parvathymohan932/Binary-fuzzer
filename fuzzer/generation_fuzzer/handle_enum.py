import random
import struct
def handle_enum(enums, enum_name, item_type,endian):
    if enum_name in enums:
        enum_values = enums[enum_name]
        key = random_based_on_enum_type(item_type,enum_values,endian)
        return key
    else:
        raise ValueError(f"Enumeration '{enum_name}' not found in the provided enums dictionary.")

def random_based_on_enum_type(item_type, enum_values,endian):
    random_key = random.choice(list(enum_values.keys()))
    if item_type == "u1":
        return struct.pack(f'{endian}B', random_key)
    elif item_type == "u2":
        return struct.pack(f'{endian}H', random_key)
    elif item_type == "u4":
        return struct.pack(f'{endian}I', random_key)
    elif item_type == "u8":
        return struct.pack(f'{endian}Q', random_key)
   #  elif item_type.startswith("enum"):
   #      return random.choice(list(enum_values))
    elif item_type == 's2':
        return struct.pack(f'{endian}h', random_key)
    elif item_type == 's4':
        return struct.pack(f'{endian}i', random_key)
    elif item_type == 's8':
        return struct.pack(f'{endian}q', random_key)
    elif item_type == 'f4':
        return struct.pack(f'{endian}f', random_key)
    elif item_type == 'f8':
        return struct.pack(f'{endian}d', random_key)
   #  elif item_type == 'str':
   #      if encoding == 'UTF-8':
   #          return ''.join(chr(random_key) for _ in range(size)).encode('utf-8')
   #      elif encoding == 'ASCII':
   #          return ''.join(chr(random_key) for _ in range(size)).encode('ascii')
   #      else:
   #          return ''.join(chr(random_key) for _ in range(size)).encode('ascii')
    else:
        raise ValueError(f"Unsupported item type '{item_type}'.")




# for key,value in enums.items():
    #     if key==enum_name:
    #         enum_values = enums[enum_name]
    #         return random.choice(list(enum_values.values()))
    #     else:
    #         raise ValueError(f"Enumeration '{enum_name}' not found in the provided enums dictionary.")
 
# import random
# from pack_list import pack_list
# def handle_enum(enums,enum_name, endian):
#     endianness= '<' if endian == 'le' else '>'
#     if enum_name in enums:
#        enum_values = enums[enum_name]
#        #print("Enum_value: ", enum_values, "Enum name:", enum_name)
#        #print("List is ", list(enum_values.values()))
#        return pack_list(str(random.choice(list(enum_values.keys()))), endianness)
#     else:
#        raise ValueError(f"Enumeration '{enum_name}' not found in the provided enums dictionary.")