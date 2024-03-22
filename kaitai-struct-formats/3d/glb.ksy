meta:
  id: glb
  file-extension: glb
  endian: le
doc-ref:
  - https://docs.fileformat.com/3d/glb/
  - https://imagetostl.com/file-information/glb
  - https://en.wikipedia.org/wiki/GlTF
  - https://visao.ca/what-is-glb-file/
seq:
  - id: header
    type: header
  - id: chunks
    type: chunk
    repeat: eos

types:
  header:
    seq:
      - id: magic
        contents: [0x67, 0x6C, 0x54, 0x46]  # "glTF" 
      - id: version
        type: u4
      - id: length
        type: u4

  chunk:
    seq:
      - id: len_data
        type: u4
      - id: type
        type: str
        encoding: UTF-8
        size: 4
      - id: data
        size: len_data
