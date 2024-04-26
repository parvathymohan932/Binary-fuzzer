def preprocess_kaitai_struct(struct_definition):
    dependency_graph = {}
    
    for field in struct_definition:
        if 'if' in field:
            dependencies = extract_dependencies(field['if'], struct_definition)
            dependency_graph[field['id']] = dependencies

    return dependency_graph

def extract_dependencies(condition, struct_definition):
    dependencies = set()
    
    # Split the condition by operators
    operators = ['if', '!=', '==', '<', '<=', '>', '>=', 'not', 'and', 'or']
    tokens = condition.split(' ')
    
    # Extract field names from tokens
    for token in tokens:
        # Check if the token is an operator
        if token in operators:
            continue
        
        # If not an operator, check if it's a field name
        if token.isidentifier():
            # Check if the field name is defined in the struct definition
            if not any(field['id'] == token for field in struct_definition):
                raise ValueError(f"Field '{token}' referenced in condition is not defined in the Kaitai Struct.")
            dependencies.add(token)

    return dependencies
