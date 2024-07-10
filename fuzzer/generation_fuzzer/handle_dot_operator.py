import re
from handle_meta import handle_meta
import struct
from evaluate_value import binary_to_int
# Example usage:
# converted_value = convert_to_type(b'\x00\x01', 'u2', '<')

def split_tokens_by_dot(condition_string):
    tokens = re.findall(r'[^.]+', condition_string)
    return tokens

def split_tokens_to_get_a_dictionary(tokens):
    nested_dict = {}
    current_dict = nested_dict
    
    for token in tokens:
        if '.' in token:
            parts = token.split('.')
            for part in parts[:-1]:
                if part not in current_dict:
                    current_dict[part] = {}
                current_dict = current_dict[part]
            current_dict[parts[-1]] = {}
            current_dict = current_dict[parts[-1]]
        else:
            current_dict[token] = {}
            current_dict = current_dict[token]
    
    return nested_dict
def find_parent(name_attribute, parent):
    for seq_item in parent['seq']:
        if seq_item['id'] == name_attribute:
            return seq_item.get('type')
    return None

def handle_dot_operator(value_string, parent, field, endianness):
  print("Value:string:", value_string)
  tokens = split_tokens_by_dot(value_string)
  nested_dict = split_tokens_to_get_a_dictionary(tokens)
  print("Nested dict:", nested_dict)
  evaluated_value = evaluate_value_dot_operator(nested_dict, parent, endianness, field)
  return evaluated_value  
def evaluate_value_dot_operator(nested_dict, parent, endianness, field):
    for key, value in nested_dict.items():
        if value != {}:
            if key=='_':
                print("Field in evaluate_dot_operator is ", field)
                key= field.get('id')
            parent_type = find_parent(key, parent)
            print("Parent is ", parent_type, "for key ", key)
            print("Parent['types']= ", parent['types'])
            if parent_type is not None:
                return evaluate_value_dot_operator(value, parent['types'][parent_type], endianness, field)
            else:
                raise ValueError(f"Parent type for '{key}' not found.")
        else:
            print("Parent['types']= ", parent)
            for item in parent['seq']:
                if item.get('id') == key:
                    evaluated_value = item.get('expansion')
                    data_type = item.get('type')
                    encoding = item.get('encoding')
                    print(evaluated_value)
                    #if evaluated_value is None:
                    #    raise ValueError(f"No value found for key '{key}' in the 'seq' list.")
                    
                    if data_type is None:
                        # Handle when data type is None
                        return binary_to_int(evaluated_value, endianness)
                    elif data_type == 'str':
                        # Handle when data type is string
                        try:
                            return evaluated_value.decode(encoding)
                        except Exception as e:
                            print(f"Error occurred while decoding binary to string: {e}")
                            return ""
                    else:
                        return binary_to_int(evaluated_value, endianness)
            else:
                raise ValueError(f"Key '{key}' not found in the 'seq' list.")
