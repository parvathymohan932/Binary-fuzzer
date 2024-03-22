meta:
  id: ply
  title: PLY (Polygon File Format)
  file-extension: ply
  endian: le
  license: MIT

doc: |
  The PLY (Polygon File Format) is a file format for representing 3D geometry.

seq:
  - id: header
    type: header
    doc: PLY file header

types:
  header:
    seq:
      - id: magic
        contents: 'ply'
  
