
import re
from handle_meta import handle_meta
import struct
from evaluate_value import binary_to_int

def evaluate_value_dot_operator(nested_dict, parent, endianness, root):
    for key, value in nested_dict.items():
        if key == '_root':
            # Handle _root specially
            return evaluate_value_dot_operator(value, root, endianness, root)
        if value != {}:
            parent_type = find_parent(key, parent)
            if parent_type is not None:
                if 'types' in parent:
                    return evaluate_value_dot_operator(value, parent['types'][parent_type], endianness, root)
                else:
                    raise ValueError(f"'types' key not found in parent for key '{key}'.")
            else:
                raise ValueError(f"Parent type for '{key}' not found.")
        else:
            for item in parent['seq']:
                if item.get('id') == key:
                    evaluated_value = item.get('expansion')
                    data_type = item.get('type')
                    encoding = item.get('encoding')
                    if evaluated_value is None:
                        raise ValueError(f"No value found for key '{key}' in the 'seq' list.")
                    
                    if data_type is None:
                        return binary_to_int(evaluated_value, endianness)
                    else:
                        return binary_to_int(evaluated_value, endianness)
            else:
                raise ValueError(f"Key '{key}' not found in the 'seq' list.")


def handle_dot_operator(expression, parent, endian, root):
    tokens = expression.split('.')
    print(f"Handling dot operator for expression '{expression}', tokens: {tokens}")
    
    current_value = root if tokens[0] == '_root' else parent
    for token in tokens[1:]:
        if isinstance(current_value, dict):
            if 'seq' in current_value:
                found = False
                for item in current_value['seq']:
                    if item.get('id') == token:
                        expansion = item.get('expansion')
                        print("Dot operator",expansion)
                        if expansion is not None:
                            current_value = binary_to_decimal(expansion, endian)
                        else:
                            current_value = None
                        found = True
                        break
                if not found:
                    current_value = current_value.get(token, None)
            else:
                current_value = current_value.get(token, None)
        else:
            current_value = None
        print(f"Current value after handling token '{token}': {current_value}")
    
    if current_value is None:
        raise ValueError(f"Unable to resolve expression '{expression}'")
    
    return current_value
def binary_to_decimal(binary_value, endianness):
    try:
        # Convert binary bytes to integer
        byteorder = 'little' if endianness == 'le' else 'big'
        decimal_value = int.from_bytes(binary_value, byteorder)
        return decimal_value
    except Exception as e:
        print(f"Error converting binary to decimal: {e}")
        return None


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

def binary_to_int(binary_data, endianness):
    if endianness == 'be':
        return int.from_bytes(binary_data, 'big')
    else:
        return int.from_bytes(binary_data, 'little')

def convert_value_to_type(value, field_type, endianness, encoding="ASCII"):
    if field_type == 'u2':
        return struct.pack(f'{endianness}H', value)
    elif field_type == 'u4':
        return struct.pack(f'{endianness}I', value)
    elif field_type == 'str':
        if encoding == "ASCII":
            return value.encode('ascii')
        elif encoding == "UTF-8":
            return value.encode('utf-8')
    else:
        raise ValueError(f"Unsupported field type '{field_type}'.")