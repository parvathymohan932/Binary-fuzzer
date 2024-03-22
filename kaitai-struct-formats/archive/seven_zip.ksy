meta:
  id: seven_zip
  title: 7-Zip Archive

doc-ref:
  - https://www.7-zip.org/7z.html
  - https://en.wikipedia.org/wiki/7z#
  - https://docs.fileformat.com/compression/7z/

seq:
  - id: signature
    contents: [0x37, 0x7A, 0xBC, 0xAF, 0x27, 0x1C]

  - id: header
    type: header

types:
  header:
    seq:
      - id: major_version
        type: u1
      - id: minor_version
        type: u1
      - id: start_header_crc
        type: u4le
      - id: next_header_offset
        type: u4le
      - id: next_header_size
        type: u2le
      - id: next_header_crc
        type: u4le
