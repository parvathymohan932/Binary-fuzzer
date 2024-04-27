import random
def handle_enum(enums,enum_name):
    if enum_name in enums:
       enum_values = enums[enum_name]
       return random.choice(list(enum_values.values()))
    else:
       raise ValueError(f"Enumeration '{enum_name}' not found in the provided enums dictionary.")
    # for key,value in enums.items():
    #     if key==enum_name:
    #         enum_values = enums[enum_name]
    #         return random.choice(list(enum_values.values()))
    #     else:
    #         raise ValueError(f"Enumeration '{enum_name}' not found in the provided enums dictionary.")
 

