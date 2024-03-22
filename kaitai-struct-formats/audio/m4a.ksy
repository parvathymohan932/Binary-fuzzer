meta:
  id: m4a
  file-extension: m4a
  title: MPEG-4 Audio (M4A) File
doc-ref:
  - https://www.file-recovery.com/m4a-signature-format.htm

seq:
  - id: chunk_size
    size: 4
  - id: chunk_type
    contents: 'ftyp'
  - id: sub_type
    contents: 'M4A '


        
