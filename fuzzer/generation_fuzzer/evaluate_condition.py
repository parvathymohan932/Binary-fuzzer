import re
from evaluate_value import binary_to_int
from handle_dot_operator import handle_dot_operator
# def evaluate_condition(condition_string, item, parent, endian):
#     # Access the entire parent dictionary
#     if isinstance(condition_string, int):
#         return condition_string
    
#     tokens = re.findall(r'\b\w+\b|[!=<>+*/%-]+', condition_string)
#     print("Tokens:", tokens)
#     print(condition_string)
#     for i, token in enumerate(tokens):
#         # Check if the token is an integer
#         if token.isdigit():
#             tokens[i] = token  # If it's an integer, keep it as it is
#         else:
#             # Otherwise, look for the corresponding item in the sequence

#             #print("PARENT LIST", parent)
#             for item_in_seq in parent['seq']:
#                 print("Evaluate condition item_in_seq: ", item_in_seq)
#                 if item_in_seq.get('id') == token:
#                     tokens[i] = str(binary_to_int(item_in_seq.get('expansion'), endian))
#                     break  
#     modified_condition_string = ''.join(tokens)
#     print("String is", modified_condition_string)

#     try:
#         result = eval(modified_condition_string)
#         print("Result is :", result)
#         return result
#     except (SyntaxError, ValueError) as e:
#         print(f"Error occurred while evaluating condition: {e}")
#         return False


def evaluate_condition(condition_string, parent,endian):
     tokens = re.findall(r'\b\w+(?:\.\w+)*\b|[!=<>+*/%-]+', condition_string)

     print("Tokens:", tokens)
     print(condition_string)
     for i, token in enumerate(tokens):
        if '.' in token:
        # If the token contains a dot, handle dot operator
            value = handle_dot_operator(token, parent, endian)
            tokens[i] = str(value)
        else:
            # Otherwise, search for the token in the parent sequence
            for item_in_seq in parent['seq']:
                if item_in_seq.get('id') == token:
                    tokens[i] = str(binary_to_int(item_in_seq.get('expansion'), endian))
                    break  # Stop searching once the token is replaced

     # Reconstruct the modified condition string
     modified_condition_string = ''.join(tokens)
     print("Modified string is ",modified_condition_string)
     # Evaluate the modified condition string
     try:
         result = eval(modified_condition_string)
         return result
     except (SyntaxError, ValueError) as e:
         print(f"Error occurred while evaluating condition: {e}")
         return False
   