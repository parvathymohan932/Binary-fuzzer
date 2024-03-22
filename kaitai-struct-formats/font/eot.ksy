meta:
  id: eot
  file-extension: eot
  endian: be  # Assuming little-endian format

seq:
  - id: magic_number
    contents: [0x80,0x01]

  - id: eot_size
    type: u4
    
  - id: font_data_size
    type: u4
    
  - id: version
    type: u4
    
  - id: flags
    type: u4
   