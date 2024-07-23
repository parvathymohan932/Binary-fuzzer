import re

def handle_enum_operator(enum_reference,enums,parent, endian):
    tokens = split_tokens_by_double_colon(enum_reference)
    print(tokens)
    if len(tokens) != 2:
        raise ValueError(f"Invalid enum reference '{enum_reference}'.")
    enum_name, enum_value = tokens
    # if enum_name in enums:
    #     for key,value in enums.items():
    #         if value == enum_value:
    #             return key
    if enum_name in parent['enums']:
        enum_dict = parent['enums'][enum_name]
        for key, value in enum_dict.items():
            if value == enum_value:
                return key
    else:
        raise ValueError(f"Enum value '{enum_value}' not found in enum '{enum_name}'.")

def split_tokens_by_double_colon(condition_string):
    tokens = condition_string.split('::')
    print("Condition String:", condition_string)  # Debugging: print the condition string
    print("Tokens after splitting by '::':", tokens)
    return tokens