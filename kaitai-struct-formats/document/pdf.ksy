meta:
  id: pdf
  file-extension: pdf
  endian: le
doc-ref:
  - https://www.iso.org/standard/63534.html
  - https://www.adobe.com/content/dam/acom/en/devnet/pdf/adobe_supplement_iso32000.pdf
  - https://docs.fileformat.com/pdf/
  - https://en.wikipedia.org/wiki/List_of_file_signatures
seq:
  - id: header
    type: header_chunk
types:
  header_chunk:
    seq:
      - id: magic
        size: 5
        contents: [37, 80, 68, 70, 45]
      - id: version
        type: u2