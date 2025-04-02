meta:
  id: padr_packet
  title: "PPPoE Active Discovery Request (PADR)"
  application: "PPPoE Discovery Stage"
  file-extension: padr
  endian: be

seq:
  - id: version_type
    type: u1
    valid: 0x11
    doc: |
      The first 4 bits are the version number (should be 1 for PPPoE).
      The next 4 bits are the type (should be 1 for PPPoE).
  
  - id: code
    type: u1
    valid: 0x19
    doc: |
      Code for the PADR packet. It should be 0x19 for Active Discovery Request.
  
  - id: session_id
    type: u2
    valid: 0x0000
    doc: |
      Session ID is set to 0 for Discovery packets like PADR.
  
  - id: length
    type: u2
    valid: 
      min: 0
      max: 12
    doc: |
      Length of the payload (in bytes). The total size of the PADR packet (including headers) must not exceed 1484 bytes.
  
  - id: service_name_tag
    type: service_name_tag  
    size: length
    doc: |
      The PADR packet must contain exactly one Service-Name tag, indicating the service the Host is requesting.

types:
  service_name_tag:
    seq:
      - id: tag_type
        type: u2
        valid: 0x0101  
      - id: tag_length
        type: u2
        valid:
          min: 1
          max: 1460 
      - id: tag_value
        size: tag_length