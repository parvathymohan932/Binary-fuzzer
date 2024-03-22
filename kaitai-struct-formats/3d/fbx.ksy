meta:
  id: fbx
  file-extension: fbx
  endian: le

doc-ref:
  - https://en.wikipedia.org/wiki/FBX
  - https://code.blender.org/2013/08/fbx-binary-file-format-specification/

seq:
  - id: fbx_header
    type: fbx_header

types:
  fbx_header:
    seq:
      - id: magic
        contents: "Kaydara FBX Binary  \x00"
      - id: unknown
        contents: [0x1A, 0x00]
      - id: reserved
        size: 21
#should define the node record format