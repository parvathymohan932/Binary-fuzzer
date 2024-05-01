from random_generate import random_based_on_size, random_based_on_type ,convert_value_to_type
from pack_list import pack_list
from conditionals_preprocessing import preprocess_kaitai_struct, dependency_order, evaluate_condition
import random
import string
from handle_enum import handle_enum
from evaluate_size import evaluate_size

def add_value_to_node(item, value):
    item['value'] = value

def append_value_to_node(item, value):
    if 'value' not in item:
        item['value'] = b''
    item['value'] += value


def handle_field(field, endian, parent, root, grandparent):
    endianness= '<' if endian == 'le' else '>'
    content = field.get('contents')
    field_type = field.get('type')
    size = evaluate_size(field.get('size', 0), endianness, parent)
    encoding = field.get('encoding')
    enum_name = field.get('enum')
    valid_value = field.get('valid')


    if content is not None:
        expansion = pack_list(content, '<' if endian == 'le' else '>')
    elif valid_value is not None:
        expansion = handle_valid(valid_value, field_type, endianness, encoding)
        print("The valid value is", expansion)
    elif field_type:
        if enum_name:
            expansion = handle_enum(root['enums'], enum_name, field_type, '<' if endian == 'le' else '>')
        elif field_type in ['u1','u2', 'u4', 'u8', 's2', 's4', 's8', 'f2', 'f4', 'f8']:
            expansion = random_based_on_type(size, field_type, '<' if endian == 'le' else '>', encoding)
        elif field_type == 'str':
            if field.get('size-eos', False):
                size = random.randint(1, 1024)
            expansion = random_based_on_type(size, field_type, '<' if endian == 'le' else '>', encoding)
        elif field_type == 'strz':
            if 'size' in field:
                size = field['size']
            else:
                size = random.randint(1, 1023)
            if size < 1:
                size = 1
            random_string = generate_random_string(size-1, encoding)
            expansion = random_string.encode(encoding) + b'\0'
        else:
            expansion = handle_type(parent, endian, field_type, root, grandparent)
    else:
        expansion = random_based_on_size(size, endian)
    
    return expansion

def handle_valid(valid_value, field_type, endianness, encoding=None):
    if isinstance(valid_value, dict):
        if 'min' in valid_value and 'max' in valid_value:
            min_value = valid_value['min']
            max_value = valid_value['max']
            exp = random.randint(min_value, max_value)
            return convert_value_to_type(exp, field_type, endianness, encoding)
        elif 'eq' in valid_value:
            eq_value = valid_value['eq']
            return convert_value_to_type(eq_value, field_type, endianness, encoding)
    elif valid_value is not None:
        return convert_value_to_type(valid_value, field_type, endianness, encoding)


def generate_random_string(size, encoding):
    
    random_string = ''.join(random.choice(string.ascii_letters) for _ in range(size))
    #print("The random string is", random_string)
    return random_string


def handle_repeat_field(field, endian, parent,root,  grandparent):
    total_expansion = b''
    expansion = handle_field(field, endian, parent,root,grandparent)
    total_expansion += expansion
    append_value_to_node(field, expansion)
    random_repeat_count = random.randrange(1, 100)
    for _ in range(1, random_repeat_count):
        expansion = handle_field(field, endian, parent, root,grandparent)
        total_expansion += expansion
        append_value_to_node(field, expansion)
    
    return total_expansion


def handle_repeat_expr_field(field, endian, seq, parent,root, grandparent):
    total_expansion=b''
    repeat_expr = field.get('repeat-expr')
    expansion = handle_field(field, endian, parent,root, grandparent)  #so that it occurs atleast 1 time
    total_expansion += expansion
    append_value_to_node(field, expansion)
    if repeat_expr is not None:
        result= evaluate_condition(repeat_expr,field, seq, endian)
    for _ in range(1,result):
        expansion = handle_field(field, endian, parent, root,grandparent)
        total_expansion += expansion
        append_value_to_node(field, expansion)
    
    return total_expansion
'''
def handle_repeat_until_field(field, endian, seq, parent):
    total_expansion=b''
    repeat_expr = field.get('repeat-until')
    expansion = handle_field(field, endian, parent)
    total_expansion += expansion
    append_value_to_node(field, expansion)
    if repeat_expr is not None:
        result= evaluate_condition(repeat_expr,field, seq, endian)
        print("Result new: ", result)
    for _ in range(1, result):
        expansion = handle_field(field, endian, parent)
        total_expansion += expansion
        append_value_to_node(field, expansion)
    
    return total_expansion

'''


def handle_seq(seq, endian, parent,root, grandparent=None):
    total_expansion = b''
    dependency_graph = preprocess_kaitai_struct(seq)
    ordered_list = dependency_order(dependency_graph)
    
    
    for field_id in ordered_list:
        field = next((item for item in seq if item['id'] == field_id), None)
        
        if field is None:
            raise ValueError(f"Field ID '{field_id}' not found in the sequence.")
        condition_string= field.get('if')
        if condition_string is not None:
            print("Seq is: ", seq)
            result = evaluate_condition(condition_string, field,seq,endian)
            print("Result is: ",result)
            if(result==False):
                continue
        
        if field.get('repeat') is None:
            
            expansion = handle_field(field, endian, parent,root, grandparent)
        else:
            if field.get('repeat') == 'eos':
                expansion = handle_repeat_field(field, endian, parent, root,grandparent)
            elif field.get('repeat') == 'expr':
                expansion= handle_repeat_expr_field(field, endian, seq, parent, root, grandparent)
            #elif field.get('repeat') == 'until':
             #   expansion= handle_repeat_until_field(field, endian, seq, parent)
        
        #total_expansion += expansion
        
        add_value_to_node(field, expansion)
    total_expansion= calculate_total_expansion_in_current_seq(parent)
    return total_expansion


def handle_type(parent, endian, user_defined_type,root, grandparent=None):
    if parent is None and grandparent is None:
        raise ValueError("Both parent and grandparent cannot be None.")
    
    expansion = b''
    types_to_search = []
    
    if parent is not None and 'types' in parent:
        types_to_search.append(parent['types'])
    if grandparent is not None and 'types' in grandparent:
        types_to_search.append(grandparent['types'])
    
    for types_dict in types_to_search:
        print("User-defined type is ", user_defined_type,"Type dict: ",  types_dict)
        if user_defined_type in types_dict:
            type_entry = types_dict[user_defined_type]
            print("HERE:", type_entry.get('value'))
            print("PARENT: ",parent)
            #expansion = handle_seq(type_entry['seq'], endian, type_entry, parent)
            #add_value_to_node(type_entry, expansion)
            if type_entry.get('value') is None:
                 #print("HEREEEE:  ", types[key].get('value'))
                 expansion=handle_seq(type_entry['seq'], endian, type_entry,root, parent)
                 add_value_to_node(type_entry,expansion )
            else:
                expansion= type_entry.get('value')
            break
    
    return expansion



def calculate_total_expansion_in_current_seq(parent):
    total_expansion_in_current_seq=b''
    # Write the contents of 'value' field for each item in 'seq' to the file
    for item in parent['seq']:
        # repeat= item.get('repeat')
        field_value = item.get('value')
        if field_value is not None:
            total_expansion_in_current_seq+=field_value
    return total_expansion_in_current_seq
