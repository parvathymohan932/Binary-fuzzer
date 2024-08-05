from handle_dot_operator import handle_dot_operator
#from evaluate_value import convert_to_type
from evaluate_condition import evaluate_condition
def evaluate_size(size_value, endianness, parent, field):
    """
    Evaluate the size value and convert it to the specified data type.

    Args:
        size_value: The size value to be evaluated.
        data_type (str): The desired data type for the conversion.
        endianness (str): The endianness of the data.
        encoding (str): The encoding to use for string conversion.

    Returns:
        The evaluated and converted size value.
    """
    if isinstance(size_value, int):
        # If size_value is already an integer, return it directly
        return size_value
    elif isinstance(size_value, str):
        # If size_value is a string, evaluate it using dot operator and then convert to the specified data types
        print(parent)
        evaluated_value = evaluate_condition(size_value, parent, endianness, field)
        print("Evaluated value for size_value ", size_value, evaluated_value)
        return evaluated_value
    else:
        raise ValueError("Invalid size value. It must be either an integer or a string.")
