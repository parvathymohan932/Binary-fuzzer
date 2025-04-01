meta:
  id: padi_packet
  title: "PPPoE Active Discovery Initiation (PADI)"
  application: "PPPoE Discovery Stage"
  file-extension: padi
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
    valid: 0x09
    doc: |
      Code for the PADI packet. It should be 0x09 for Active Discovery Initiation.
  
  - id: session_id
    type: u2
    valid: 0x0000
    doc: |
      Session ID is set to 0 for Discovery packets like PADI.
  
  - id: length
    type: u2
    doc: |
      Length of the payload (in bytes). The entire PADI packet must not exceed 1484 octets, including the PPPoE header.
  
  - id: service_name_tag
    type: service_name_tag
    doc: |
      The PADI packet must contain exactly one Service-Name tag, indicating the service the Host is requesting.

  - id: tags
    type: tag
    repeat: eos
    doc: |
      Optional tags following the Service-Name tag.
    #_root.length - 6  # Adjust for PPPoE header size

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

  tag:
    seq:
      - id: tag_type
        type: u2
        enum: tag_type_enum
      - id: tag_length
        type: u2
        valid:
          min: 0
          max: 12
      - id: tag_value
        size: tag_length

enums:
  tag_type_enum:
    0x0000: end_of_list
    0x0101: service_name
    0x0102: ac_name
    0x0103: host_uniq
    0x0104: ac_cookie
    0x0105: vendor_specific
    0x0110: relay_session_id
    0x0201: service_name_error
    0x0202: ac_system_error
    0x0203: generic_error



    #root.length
