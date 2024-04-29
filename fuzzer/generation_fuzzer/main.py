import os
import yaml


from handle import handle_seq
from handle_meta import handle_meta
from conditionals_preprocessing import preprocess_kaitai_struct, dependency_order
#from repeat import repeat_field


import os
def write_leaf_values_to_file(data_tree, output_directory):
    id = data_tree['meta']['id']
    file_extension = data_tree['meta']['file-extension']
    
    # Determine the file path
    filename = f"{id}.{file_extension}" if file_extension else f"{id}"
    filepath = os.path.join(output_directory, filename)
    
    with open(filepath, 'wb') as file:
        # Write the contents of 'value' field for each item in 'seq' to the file
        for item in data_tree['seq']:
           
           field_value = item.get('value')
           if field_value is not None:
                file.write(field_value)
          #  value=''
          #  if repeat is not None:
            #    value= repeat_field(field_value,repeat)
            #    if value is not None:
             #       file.write(value)
           # else:
                #repeat_field(data_tree, output_directory, field_value, 1)
            #value = item.get('value')
            

output_directory = 'testcases'
os.makedirs(output_directory, exist_ok=True)
# Specify the path to your YAML file
file_path = "C:\\Users\\libna\\OneDrive\\Desktop\\mini_project\\Binary-fuzzer\\kaitai-struct-formats\\image\\xwd.ksy"


# Read the YAML data from the file
with open(file_path, 'r') as file:
    yaml_data = file.read()

# Load YAML data
data_tree = yaml.safe_load(yaml_data)
#print("2704: ", data_tree['seq']['types']['data_descriptor'])
#print(data_tree)
#for i in range(0, 100):
endianness, file_extension,id = handle_meta(data_tree['meta'])

#dependency_graph= preprocess_kaitai_struct(data_tree['seq'])
#print("Dependency tree is: ",dependency_graph )

#ordered_list= dependency_order(dependency_graph)
#print("Ordered list is:", ordered_list)
#expansion = handle_seq(data_tree['seq'], endianness, data_tree)
handle_seq(data_tree['seq'], endianness, data_tree)
print(data_tree)
# Determine the file path
#filename = f"{id}.{file_extension}" if file_extension else f"{id}"
#filepath = os.path.join(output_directory, filename)
write_leaf_values_to_file(data_tree, output_directory)
# Write the output to the file
#with open(filepath, 'wb') as file:
#    file.write(expansion)