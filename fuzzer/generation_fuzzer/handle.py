from random_generate import random_based_on_size, random_based_on_type
from pack_list import pack_list
from conditionals_preprocessing import preprocess_kaitai_struct, dependency_order, evaluate_condition
import random

def add_to_child_node(item, value):
    # Add the 'value' key to the current item dictionary and assign the generated value to it
    item['value'] = value


def handle_seq(seq, endian, parent):

    total_expansion= b''
    valid_endian = 'big' if endian == 'le' else 'little'
    endianness = '<' if endian == 'le' else '>'

    dependency_graph= preprocess_kaitai_struct(seq)
    #print("Dependency tree is: ",dependency_graph )

    ordered_list= dependency_order(dependency_graph)
    #print("Ordered list is:", ordered_list)
    #print(ordered_list)
    for field_id in ordered_list:
    # Find the item corresponding to the current field ID
        item = next((item for item in seq if item['id'] == field_id), None)
        if item is None:
            raise ValueError(f"Field ID '{field_id}' not found in the sequence.")
        print(item.get('id'))
        content = item.get('contents')
        item_type = item.get('type')
        size = item.get('size', 0)
        encoding = item.get('encoding')
        condition_string = item.get('if')
        expansion = b''
        #if 'contents' in item:
        #    expansion += pack_list(item['contents'], '<' if endian == 'le' else '>')
        if condition_string is not None:
            print("Seq is: ", seq)
            result = evaluate_condition(condition_string, item,seq,endian)
            print("Result is: ",result)
            if(result==False):
                continue
        if content is not None:
          # If content exists, add it to the current item dictionary as 'value'

          expansion =  pack_list(content, endianness)
          total_expansion+=expansion
          add_to_child_node(item, expansion)
        elif item_type:
            if item_type in ['u1','u2', 'u4', 'u8', 's2', 's4', 's8', 'f2', 'f4', 'f8']:
                expansion = random_based_on_type(size, item_type, '<' if endian == 'le' else '>', encoding)
                add_to_child_node(item, expansion)
                total_expansion+=expansion
            elif item_type == 'str':
                if  item.get('size-eos', False):
                    size=random.randint(1,1024)
                    expansion = random_based_on_type(size, item_type, '<' if endian == 'le' else '>', encoding)
                else:
                    expansion = random_based_on_type(size, item_type, '<' if endian == 'le' else '>', encoding)
                add_to_child_node(item, expansion)
                total_expansion+=expansion
            else:
                expansion= handle_type(parent['types'], endian, item_type)
                #print(expansion)
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
            #print("HEREEEE:  ", types[key].get('value'))
            print("HERE:",types[key].get('value'))
            if types[key].get('value') is None:
                #print("HEREEEE:  ", types[key].get('value'))
                expansion=handle_seq(types[key]['seq'], endian, value)
                add_to_child_node(types[key],expansion )
            else:
                expansion= types[key].get('value')
               
            
    
    return expansion
