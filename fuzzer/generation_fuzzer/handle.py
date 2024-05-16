from random_generate import random_based_on_size, random_based_on_type
from pack_list import pack_list
from conditionals_preprocessing import preprocess_kaitai_struct, dependency_order
from evaluate_condition import evaluate_condition
import random
import string
from handle_enum import handle_enum
from evaluate_size import evaluate_size
from find_user_defined_type import find_user_defined_type

def add_value_to_node(item, value):
    item['expansion'] = value

def append_value_to_node(item, value):
    if 'expansion' not in item:
        item['expansion'] = b''
    item['expansion'] += value




def handle_field(field, endian, parent, root, parent_string):
    endianness= '<' if endian == 'le' else '>'
    content = field.get('contents')
    field_type = field.get('type')
    size = evaluate_size(field.get('size', 0), endianness, parent )
    encoding = field.get('encoding')
    enum_name=field.get('enum')
    if content is not None:
        expansion = pack_list(content, '<' if endian == 'le' else '>')
    elif field_type:
        if enum_name:
            expansion=handle_enum(root['enums'], enum_name, field_type, '<' if endian == 'le' else '>')
        elif field_type in ['u1','u2', 'u4', 'u8', 's2', 's4', 's8', 'f2', 'f4', 'f8']:
            expansion = random_based_on_type(size, field_type, '<' if endian == 'le' else '>', encoding)
        elif field_type == 'str':
                 if  (field.get('size-eos', False)==True):
                     size=random.randint(1,1024)
                     expansion = random_based_on_type(size, field_type, '<' if endian == 'le' else '>', encoding)
                 else:
                     expansion = random_based_on_type(size, field_type, '<' if endian == 'le' else '>', encoding)
        elif field_type == 'strz':
            if 'size' in field:
                size = field['size']  
            else:
                size = random.randint(1, 1023)  

            if size < 1:
                size = 1
            random_string = generate_random_string(size, encoding)
            expansion = random_string.encode(encoding) + b'\0'

            
        else:
            expansion = handle_type(parent, endian, field_type,root, parent_string)
    else:
        expansion = random_based_on_size(size, endian)
    
    return expansion


def generate_random_string(size, encoding):
    # Generate random string of given size
    # For simplicity, let's assume ASCII characters for now
    random_string = ''.join(random.choice(string.ascii_letters) for _ in range(size))
    print("The random string is", random_string)
    return random_string


def handle_repeat_field(field, endian, parent,root,  parent_string):
    total_expansion = b''
    expansion = handle_field(field, endian, parent,root,parent_string)
    total_expansion += expansion
    append_value_to_node(field, expansion)
    random_repeat_count = random.randrange(1, 100)
    for _ in range(1, random_repeat_count):
        expansion = handle_field(field, endian, parent, root,parent_string)
        total_expansion += expansion
        append_value_to_node(field, expansion)
    
    return total_expansion


def handle_repeat_expr_field(field, endian, seq, parent,root, parent_string):
    total_expansion=b''
    repeat_expr = field.get('repeat-expr')
    expansion = handle_field(field, endian, parent,root, parent_string)  #so that it occurs atleast 1 time
    total_expansion += expansion
    append_value_to_node(field, expansion)
    if repeat_expr is not None:
        result= evaluate_condition(repeat_expr, seq, endian)
    for _ in range(1,result):
        expansion = handle_field(field, endian, parent, root,parent_string)
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


def handle_seq(seq, endian, parent,root, parent_string):
    total_expansion = b''
    dependency_graph = preprocess_kaitai_struct(seq)
    ordered_list = dependency_order(dependency_graph)
    
    print("Parent string in handle_seq", parent_string)
    for field_id in ordered_list:
        print("Reached in handle_seq")
        field = next((item for item in seq if item['id'] == field_id), None)
        print("Field in handle seq: ", field)
        if field is None:
            raise ValueError(f"Field ID '{field_id}' not found in the sequence.")
        condition_string= field.get('if')
        if condition_string is not None:
            #print("Seq is: ", seq)
            result = evaluate_condition(condition_string,parent,endian)
            #print("Result is: ",result)
            if(result==False):
                continue
        
        if field.get('repeat') is None:
            
            expansion = handle_field(field, endian, parent,root, parent_string)
        else:
            if field.get('repeat') == 'eos':
                expansion = handle_repeat_field(field, endian, parent, root,parent_string)
            elif field.get('repeat') == 'expr':
                expansion= handle_repeat_expr_field(field, endian, seq, parent, root, parent_string)
            #elif field.get('repeat') == 'until':
             #   expansion= handle_repeat_until_field(field, endian, seq, parent)
        
        #total_expansion += expansion
        
        add_value_to_node(field, expansion)
    total_expansion= calculate_total_expansion_in_current_seq(parent)
    return total_expansion


def handle_type(parent, endian, user_defined_type,data_tree, parent_string):
    #if parent is None:
    #    raise ValueError(" parent cannot be None.")
    
    expansion = b''
    #types_to_search = []
    
    # if parent is not None and 'types' in parent:
    #     types_to_search.append(parent['types'])
    # if grandparent is not None and 'types' in grandparent:
    #     types_to_search.append(grandparent['types'])
    #print('Parent_string in handle_type', parent_string)
    print("Userdefined type required, initial parent string ", user_defined_type, parent_string)
    types_dict, new_parent_string = find_user_defined_type(user_defined_type, parent_string, data_tree)
    #new_parent_string += "['types']"
    #new_parent_string += f"['{user_defined_type}']"
    print("New_parent_string in handle_type:", new_parent_string)
    print("Type dict in handle_type",types_dict)

    #for types_dict in types_to_search:
    #print("User-defined type is ", user_defined_type,"Type dict: ",  types_dict)
    #if user_defined_type in types_dict:
    type_entry = types_dict[user_defined_type]
    print("Type entry in handle_type",type_entry)
    #print("HERE:", type_entry.get('expansion'))
    #print("PARENT: ",parent)
    #expansion = handle_seq(type_entry['seq'], endian, type_entry, parent)
    #add_value_to_node(type_entry, expansion)
    if type_entry.get('expansion') is None:
            print("HEREEEE:  ", type_entry)
            #parent_string= parent_string.append
            expansion=handle_seq(type_entry['seq'], endian, type_entry,data_tree, new_parent_string)
            add_value_to_node(type_entry,expansion )
    else:
        expansion= type_entry.get('expansion')
    #break
    return expansion

# def find_user_defined_type(parent, user_defined_type):
#     if user_defined_type in parent['types']:
#         return parent['types'][user_defined_type]
#     elif 'parent' in parent:
#         return find_user_defined_type(parent['parent'], user_defined_type)
#     else:
#         return find_user_defined_type()


def calculate_total_expansion_in_current_seq(parent):
    total_expansion_in_current_seq=b''
    # Write the contents of 'expansion' field for each item in 'seq' to the file
    for item in parent['seq']:
        # repeat= item.get('repeat')
        field_value = item.get('expansion')
        if field_value is not None:
            total_expansion_in_current_seq+=field_value
    return total_expansion_in_current_seq
