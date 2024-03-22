meta:
  id: graphics3ds
  file-extension: 3ds
  endian: le
doc-ref:
  - https://en.wikipedia.org/wiki/.3ds
  - https://docs.fileformat.com/3d/3ds/
seq:
  - id: header
    type: header_chunk

#  - id: chunks
#    type: chunk
#    repeat: eos

types:
  header_chunk:
    seq:
      - id: magic
        contents: [0x4D, 0x4D]  # MM
      - id: version
        type: u2

#  chunk:
#    seq:
#      - id: chunk_id
#        type: u2
#      - id: len_data
#        type: u4
#      - id: data
#        size: len_data 



