meta:
  id: amr
  endian: le
seq:
  - id: header
    type: header
  - id: frames
    type: frame
    repeat: eos
types:
  header:
    seq:
      - id: magic
        contents: "#!AMR"
  frame:
    seq:
      - id: frame_data
        size: 1  # Adjust the size based on the actual frame size in your AMR file
