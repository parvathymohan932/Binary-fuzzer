import re
import ast

def preprocess_kaitai_struct(struct_definition):
    dependency_graph = {}
    all_fields = [] #Using a set here, If we care about the order in the all fields, we should use list. Also when using set redundant fields will be overwritten, which means, instead of having error, the set will just consider the last field with same id. 
    for field in struct_definition:
        if 'if' in field:
            dependencies = extract_dependencies(field['if'], struct_definition)#need to add other dependencies like size repeat-expr
            dependency_graph[field] = dependencies
        else:
            # If the field does not have 'if' condition, add it to all_fields set
            all_fields.append(field)
    for field_id in all_fields:
        dependency_graph[field_id] = []

    print("Dependency graph: ", dependency_graph)
    return dependency_graph
def extract_dependencies(condition, struct_definition):
    dependencies = set()
    
    # Define operators used in conditions
    operators = ['if', '!=', '==', '<', '<=', '>', '>=', 'not', 'and', 'or']
    
    # Define regular expression pattern to match operators
    pattern = '|'.join(map(re.escape, operators))
    
    # Split the condition string based on operators
    tokens = re.split(pattern, condition)
    
    # Extract field names from tokens
    for token in tokens:
        # Strip whitespace and check if the token is a valid identifier
        token = token.strip()
        if token and token.isidentifier():
            if not any(field == token for field in struct_definition):
                raise ValueError(f"Field '{token}' referenced in condition is not defined in the Kaitai Struct.")
            dependencies.add(token)

    return dependencies

def dependency_order(dependency_graph):
    # Initialize an empty list to store the processing order
    processing_order = []
    
    # Define a recursive function to traverse the dependency graph
    def traverse(node):
        # If the node has dependencies, recursively traverse them first
        for dependency in dependency_graph.get(node, []):
            traverse(dependency)
        
        # After processing dependencies, add the current node to the processing order
        if node not in processing_order:
            processing_order.append(node)
    
    # Traverse each node in the dependency graph
    for node in dependency_graph.keys():
        traverse(node)
    print("Processing Order: ",processing_order)
    # Return the processing order
    return processing_order
def binary_to_int(value, endianness):
    try:
        if endianness == 'le':
            # Little-endian byte order
            value_int = int.from_bytes(value, byteorder='little')
        else:
            # Big-endian byte order
            value_int = int.from_bytes(value, byteorder='big')
        return value_int
    except Exception as e:
        print(f"Error occurred while converting binary to integer: {e}")
        return 0

# def evaluate_condition(condition_string, item, seq,endian):
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
#             for item_in_seq in seq:
#                 if item_in_seq == token:
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


'''
def topological_sort(dependency_graph):
    # Initialize an empty list to store the sorted order
    order = []

    # Create a set to keep track of visited nodes
    visited = set()

    # Recursive function to perform depth-first search and topological sorting
    def dfs(node):
        visited.add(node)
        if node in dependency_graph:
            for neighbor in dependency_graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)
        order.append(node)

    # Iterate over all nodes in the dependency graph
    for node in dependency_graph:
        if node not in visited:
            dfs(node)

    # Reverse the order list to get the topological sorting
    order.reverse()

    return order
'''
