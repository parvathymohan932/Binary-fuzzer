meta:
  id: aiff
  title: Audio Interchange File Format
  file-extension: aiff,aif,aifc
  endian: be
doc-ref:
  - https://en.wikipedia.org/wiki/List_of_file_signatures
  - https://en.wikipedia.org/wiki/Audio_Interchange_File_Format
seq:
  - id: form_chunk
    contents: "FORM"
  - id: form_type
    type: aiff_form_type
  - id: common_chunk
    contents: "AIFF"
types:
  aiff_form_type:
    seq:
      - id: form_type
        size: 4
  
