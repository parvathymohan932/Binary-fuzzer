import re
import ast

def preprocess_kaitai_struct(struct_definition):
    dependency_graph = {}
    all_fields = []  # Using a set here to avoid redundant fields
    
    # Step 1: Construct the dependency graph
    for field in struct_definition:
        if 'if' in field:
            dependencies = extract_dependencies(field['if'], struct_definition)
            if field['id'] not in dependency_graph:
                dependency_graph[field['id']] = set()
            dependency_graph[field['id']].update(dependencies)
        if 'size' in field:
            size_value = field['size']
            if isinstance(size_value, str):
                dependencies = extract_dependencies(size_value, struct_definition)
            elif isinstance(size_value, int):
                dependencies = set()
                # For integers, there are no dependencies
            else:
                raise ValueError("Invalid type for 'size' field. It must be a string or an integer.")
            if field['id'] not in dependency_graph:
                dependency_graph[field['id']] = set()
            dependency_graph[field['id']].update(dependencies)

        # if 'repeat-expr' in field:
        #     dependencies = extract_dependencies(field['repeat-expr'], struct_definition)
        #     dependency_graph[field['id']].add(dependencies)
        # if 'repeat-until' in field:
        #     dependencies = extract_dependencies(field['repeat-until'], struct_definition)
        #     dependency_graph[field['id']].add(dependencies)
        # if 'enum' in field:
        #     dependencies = extract_dependencies(field['enum'], struct_definition)
        #     dependency_graph[field['id']].add(dependencies)
        # if 'switch' in field:
        #     dependencies = extract_dependencies(field['switch'], struct_definition)
        #     dependency_graph[field['id']].add(dependencies)
        else:
            # If the field does not have 'if' condition, add it to all_fields set

            all_fields.append(field['id'])

    # Add all fields to the dependency graph, even those without dependencies
    for field_id in all_fields:
        if field_id not in dependency_graph:
            dependency_graph[field_id] = set()

    print("Dependency graph: ", dependency_graph)
    return dependency_graph


def extract_dependencies(condition, struct_definition):
    dependencies = set()
    # Define regular expression pattern to match tokens
    pattern = r'\b\w+\b|\w+(?=[\.\s])|[!=<>+*/%\-]+|\w+(?=[=!><+*/%])'
    
    # Extract tokens from the condition string using regular expression
    tokens = re.findall(pattern, condition)
    print("Tokens in extract:", tokens)
    
    # Extract field names from tokens
    for token in tokens:
        # Check if the token is a valid identifier
        if token and token.isidentifier():
            if not any(field['id'] == token for field in struct_definition):
                #raise ValueError(f"Field '{token}' referenced in condition is not defined in the Kaitai Struct.")
                continue
            dependencies.add(token)
    
    print("Dependencies:", dependencies)
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
