meta:
  id: dwf
  file-extension: dwf
doc-ref:
  - https://docs.fileformat.com/cad/dwf/
seq:
  - id: header
    type: dwf_header

types:
  dwf_header:
    seq:
      - id: magic
        contents: '(DWF V'
      - id: version
        type: str
        encoding: ASCII
        size: 5

