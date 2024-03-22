meta:
  id: flac
  endian: le
  file-extension: flac

doc-ref:
  - https://xiph.org/flac/format.html
  - https://en.wikipedia.org/wiki/FLAC

seq:
  - id: stream
    type: stream
  - id: metadata_blocks
    type: u4               #metadata_block
    repeat: eos
  - id: frames
    type: u4              #frame
    repeat: eos

types:
  stream:
    seq:
      - id: marker
        contents: "fLaC"

#  metadata_block:
 #   seq:
  #    - id: header
  #      type: metadata_block_header
  #    - id: data
   #     type: metadata_block_data
#
 # metadata_block_header:
  #  seq:
   #   - id: last_metadata_block
    #    type: b1
     # - id: block_type
      #  type: b7
      #- id: length
       # type: b24


#  metadata_block_data:
#    seq:
#      - id: data_block
 #       size: _parent.header.length

  
