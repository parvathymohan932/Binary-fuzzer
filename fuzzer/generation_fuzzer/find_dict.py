def find_dict(parent_string, data_tree):
    #demo=0
   # print("Parent_string in find_dict",parent_string)
    components = parent_string.split("']['")
    # Remove the opening and closing brackets from the first and last components
    components[0] = components[0].replace("data_tree['", "")
    components[-1] = components[-1].replace("']", "")

    # Initialize current_dict as the root dictionary
    current_dict = data_tree
    #print(current_dict)
    # Iterate through the components and navigate the dictionary
    #print("Components:", components)
    #print("Here2")
    for component in components:
        #print("Here4")
        #print("Current dict", current_dict)
        if component in current_dict:
            current_dict = current_dict[component]
        elif component==components[-1] and component not in current_dict:
            #print("Here7")
            #demo=1
            return current_dict
            
        else:
            print(f"Key '{component}' not found in the dictionary.")
            return {}
    return current_dict