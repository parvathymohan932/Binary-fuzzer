from random_generate import random_based_on_size, random_based_on_type
from pack_list import pack_list

def add_to_child_node(item, value):
    # Add the 'value' key to the current item dictionary and assign the generated value to it
    item['value'] = value


def handle_seq(seq, endian, parent):

    total_expansion= b''
    valid_endian = 'big' if endian == 'le' else 'little'
    endianness = '<' if endian == 'le' else '>'

    for item in seq:
        content = item.get('contents')
        item_type = item.get('type')
        size = item.get('size', 0)
        encoding = item.get('encoding')
        expansion = b''
        #if 'contents' in item:
        #    expansion += pack_list(item['contents'], '<' if endian == 'le' else '>')
        if content is not None:
          # If content exists, add it to the current item dictionary as 'value'

          expansion =  pack_list(content, endianness)
          total_expansion+=expansion
          add_to_child_node(item, expansion)
        elif item_type:
            if item_type in ['u2', 'u4', 'u8', 's2', 's4', 's8', 'str', 'f2', 'f4', 'f8']:
                expansion = random_based_on_type(size, item_type, '<' if endian == 'le' else '>', encoding)
                add_to_child_node(item, expansion)
                total_expansion+=expansion
            else:
                expansion += handle_type(parent['types'], endian, item_type)
                print(expansion)
                add_to_child_node(item, expansion)
                total_expansion+=expansion
        else:
            expansion= random_based_on_size(size, endianness)
            add_to_child_node(item,expansion )
            total_expansion+=expansion
    #print(expansion)
    return total_expansion

def handle_type(types, endian, user_defined_type):
    expansion = b''
    
    for key, value in types.items():
        if key == user_defined_type:
            expansion+=handle_seq(value.get('seq', []), endian, value)
    
    return expansion
