meta:
  id: webp
  file-extension: webp
seq:
  - id: riff_header
    contents: "RIFF"
  - id: file_size
    type: u4le
    doc: "File Size (in bytes) in little-endian format"
  - id: webp_signature
    contents: "WEBP"
  # Add more structure definitions as needed for the WebP format