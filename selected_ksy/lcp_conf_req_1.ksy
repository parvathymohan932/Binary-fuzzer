meta:
  id: configure_request
  title: PPP Configure-Request Packet
  file-extension: cfgreq
  endian: be

seq:
  - id: code
    type: u1
    doc: "Code field, should be 1 for Configure-Request."
    valid: 1  # Code value must be 1 for Configure-Request

  - id: identifier
    type: u1
    valid: 1
    doc: "Identifier field, changes with each new request."

  - id: length
    type: u2
    valid: 20
    doc: "Total length of the packet, including header and options."

  - id: mru_option
    type: option_entry
    doc: "Variable-length field containing options."
  - id: magic_number_option
    type: magic_number_data
    doc: "Variable-length field containing options."
  - id: authentication_protocol_option
    type: authentication_protocol_data
    doc: "Variable-length field containing options."
  - id: trailing
    contents: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    type: u1

types:
  option_entry:
    seq:
      - id: type
        type: u1
        valid: 1
        doc: "Option type. 1 is for MRU."

      - id: length
        type: u1
        doc: "Option length, includes type and length fields."
        valid: 4

      - id: maximum_receive_unit
        type: u2
        valid: 1470
        doc: "The actual option data, specific to the option type."
  magic_number_data:
    seq:
      - id: type
        type: u1
        valid: 5
        doc: "Magic number for loopback detection. Must not be zero."
      - id: length
        type: u1
        valid: 6
        doc: "Magic number for loopback detection. Must not be zero."
      - id: magic_number
        type: u4
        doc: "Magic number for loopback detection. Must not be zero."

  authentication_protocol_data:
    seq:
      - id: type
        type: u1
        valid: 3
        doc: "Magic number for loopback detection. Must not be zero."
      - id: length
        type: u1
        valid: 4
        doc: "Magic number for loopback detection. Must not be zero."
      - id: protocol
        type: u2
        valid: 0xc023
        doc: "Authentication protocol (e.g., c023 for PAP, c223 for CHAP)."

    #  - id: additional_data
     #   type: u1
      #  valid: 0
       # repeat: 10
    
        #doc: "Additional data for the protocol, if any."
          


