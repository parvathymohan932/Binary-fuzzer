def find_user_defined_type(type_id, parent_string, data_tree):
    flag=0
    current_dict= find_dict(parent_string, data_tree)
    #if 'types' in current_dict:  # Check if 'types' key exists
    print("Initial Parent string in find_userdefined", parent_string)
    if current_dict is not None and 'types' in current_dict:
      for key, value in current_dict['types'].items():
          if key == type_id:
              print("Here1")
              flag = 1
              parent_string += f"['types']['{type_id}']"

              return current_dict['types'], parent_string
              
  
    components = parent_string.split("']['")

# Remove the opening and closing brackets from the first and last components
    components[0] = components[0].replace("data_tree['", "")
    components[-1] = components[-1].replace("']", "")

    # Remove the last component
    components = components[:-2]

    # Join the components back into a string
    if components:
      new_parent_string = "data_tree['" + "']['".join(components) + "']"
    #return find_parents(type_id, new_parent_string, data_tree)
    #return find_user_defined_type(type_id, new_parent_string, data_tree)
    # if components:
    #     new_parent_string = "data_tree['" + "']['".join(components) + "']['types']"
    else:
         new_parent_string = "data_tree"


    if new_parent_string == parent_string:
            return {}, new_parent_string
    return find_user_defined_type(type_id, new_parent_string, data_tree)
      # else:
      #     components = parent_string.split("']['")
      #     components[0] = components[0].replace("data_tree['", "")
      #     components[-1] = components[-1].replace("']", "")

      #     # Remove the last component
      #     components = components[:-2]

      #     # Join the components back into a string
      #     if components:
      #           new_parent_string = "data_tree['" + "']['".join(components) + "']['types']"
      #     else:
      #           new_parent_string = "data_tree"
      #     return find_user_defined_type(type_id, new_parent_string, data_tree)
#     else:
#       flag = 0
#       #print("Here5")
#       #print("Here3")
#       components = parent_string.split("']['")

# # Remove the opening and closing brackets from the first and last components
#       components[0] = components[0].replace("data_tree['", "")
#       components[-1] = components[-1].replace("']", "")

#       # Remove the last component
#       components = components[:-2]

#       # Join the components back into a string
#       if components:
#                 new_parent_string = "data_tree['" + "']['".join(components) + "']['types']"
#       else:
#                 new_parent_string = "data_tree"
#       return find_user_defined_type(type_id, new_parent_string, data_tree)

        




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