meta:
  id: padt_packet
  title: "PPPoE Active Discovery Terminate (PADT)"
  application: "PPPoE Discovery Stage"
  file-extension: padr
  endian: be

seq:
  - id: version_type
    type: u1
    valid: 0x11
    doc: |
      The first 4 bits are the version number (1 for PPPoE).
      The next 4 bits are the type (1 for PPPoE).

  - id: code
    type: u1
    valid: 0xa7
    doc: |
      Code for the PADT packet. It must be 0xa7 for Active Discovery Terminate.

  - id: session_id
    type: u2
    doc: |
      Session ID to indicate which session is to be terminated.

  - id: length
    type: u2
    valid: 0
    doc: |
      Length of the payload (in bytes). The PADT packet may not have a payload,
      so the length is typically 0, but this field is retained for compatibility.

  
