meta:
  id: woff
  endian: le
  file-extension: woff

seq:
  - id: signature
    contents: "wOFF"

  - id: flavor
    type: u4  # UInt32

  - id: length
    type: u4  # UInt32

  - id: num_tables
    type: u2  # UInt16

  - id: reserved
    type: u2  # UInt16

  - id: total_sfnt_size
    type: u4  # UInt32

  - id: major_version
    type: u2  # UInt16

  - id: minor_version
    type: u2  # UInt16

  - id: meta_offset
    type: u4  # UInt32

  - id: meta_length
    type: u4  # UInt32

  - id: meta_orig_length
    type: u4  # UInt32

  - id: priv_offset
    type: u4  # UInt32

  - id: priv_length
    type: u4  # UInt32