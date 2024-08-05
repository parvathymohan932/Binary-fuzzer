from random_generate import convert_value_to_type
from evaluate_value import binary_to_int,max_value_for_type
import random
import re

def dot_operator(expression, parent, endian, root):
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
                            current_value = binary_to_int(expansion, endian)
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

def evaluate_condition(condition_string, parent, endian, root):
    tokens = re.findall(r'\b\w+(?:\.\w+)*\b|[!=<>+*/%-]+', condition_string)
    print("Tokens:", tokens)
    print("Original condition string HEREEE:", condition_string)
    
    # Process each token in the condition string
    for i, token in enumerate(tokens):
        if '.' in token:
            # If the token contains a dot, handle dot operator
            value = dot_operator(token, parent, endian, root)
            print(f"Handling dot operator for token '{token}', got value: {value}")
            tokens[i] = value  # Replace token with its numeric value
        else:
            # Otherwise, search for the token in the parent sequence
            for item_in_seq in parent['seq']:
                if item_in_seq.get('id') == token:
                    expansion = item_in_seq.get('expansion')
                    if expansion is not None:
                        value = binary_to_int(expansion, endian)
                        print(f"Found token '{token}' in parent sequence, got value: {value}")
                        tokens[i] = value  # Replace token with its numeric value
                    else:
                        print(f"Token '{token}' in parent sequence has no expansion")
                    break  # Stop searching once the token is replaced

    # Reconstruct the modified condition string with numeric values
    modified_condition_string = ''.join(map(str, tokens))
    print("Modified condition string:", modified_condition_string)
    
    # Evaluate the modified condition string
    try:
        result = eval(modified_condition_string, {'_': root})
        print("Evaluation result:", result)
        return result
    except (SyntaxError, ValueError, NameError) as e:
        print(f"Error occurred while evaluating condition: {e}")
        return False


def handle_valid(valid_value, field_type, parent, root, endianness, encoding="ASCII"):
    
    if isinstance(valid_value, dict):
        if 'min' in valid_value and 'max' in valid_value:
            min_value = valid_value['min']
            max_value = valid_value['max']
            if isinstance(min_value, str) and '.' in min_value:
                min_value = evaluate_condition(min_value, parent, endianness, root)
            elif isinstance(min_value, str):
                min_value = evaluate_condition(min_value, parent, endianness, root)
            if isinstance(max_value, str) and '.' in max_value:
                max_value = evaluate_condition(max_value, parent, endianness, root)
            elif isinstance(max_value, str) :
                max_value = evaluate_condition(max_value, parent, endianness, root)
            if max_value < 0:
                max_value = 0
            exp = random.randint(min_value, max_value)
            return convert_value_to_type(exp, field_type, endianness, encoding)
        elif 'min' in valid_value:
            min_value = valid_value['min']
            if isinstance(min_value, str) and '.' in min_value:
                min_value = evaluate_condition(min_value, parent, endianness, root)
            elif isinstance(min_value, str):
                min_value = evaluate_condition(min_value, parent, endianness, root)
            max_type = max_value_for_type(field_type)
            exp = random.randint(min_value, max_type)
            return convert_value_to_type(exp, field_type, endianness, encoding)
        elif 'max' in valid_value:
            max_value = valid_value['max']
            if isinstance(max_value, str) and '.' in max_value:
                max_value = evaluate_condition(max_value, parent, endianness, root)
            elif isinstance(max_value, str) :
                max_value = evaluate_condition(max_value, parent, endianness, root)
            if max_value < 0:
                max_value = 0
            exp = random.randint(0, max_value)
            return convert_value_to_type(exp, field_type, endianness, encoding)
        elif 'eq' in valid_value:
            eq_value = valid_value['eq']
            return convert_value_to_type(eq_value, field_type, endianness, encoding)
        elif 'any-of' in valid_value:
            possible_values = valid_value['any-of']
            if field_type == 'str':
                for i in range(len(possible_values)):
                    if isinstance(possible_values[i], str) and possible_values[i].startswith('"') and possible_values[i].endswith('"'):
                        possible_values[i] = possible_values[i][1:-1]
                selected_value = random.choice(possible_values)
                return convert_value_to_type(selected_value, field_type, endianness, encoding)
            selected_value = random.choice(possible_values)
            return convert_value_to_type(selected_value, field_type, endianness, encoding)
        elif 'expr' in valid_value:
            expr = valid_value['expr']
            
            if isinstance(expr, str) and '.' in expr:
                
                expr = evaluate_condition(expr, parent, endianness, root)
                return convert_value_to_type(expr, field_type, endianness, encoding)
            elif isinstance(expr, str):
                max_type=max_value_for_type(field_type)
                max_attempts = 1000
                for _ in range(max_attempts):
                    try:
                        random_value = random.randint(0,max_type)
                        if eval(expr, {'_': random_value}):
                            return convert_value_to_type(random_value, field_type, endianness, encoding)
                    except Exception as e:
                        pass  # Ignore exceptions and retry
                raise ValueError("Unable to find a valid value satisfying the expression within the given range.")
            elif isinstance(expr, dict):
                # Handle dictionary expressions if needed
                pass
    elif valid_value is not None:
        return convert_value_to_type(valid_value, field_type, endianness, encoding)
    
