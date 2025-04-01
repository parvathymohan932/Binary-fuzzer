meta:
  id: lcp_req
  title: PPP Configure-Request Packet
  file-extension: lcp
  endian: be

seq:
  - id: code
    type: u1
    doc: "Code field, should be 1 for Configure-Request."
    valid: 1  # Code value must be 1 for Configure-Request

  - id: identifier
    type: u1
    doc: "Identifier field, changes with each new request."

  - id: length
    type: u2
    doc: "Total length of the packet, including header and options."

  - id: options
    type: config_options
    doc: "Variable-length field containing options."

types:
  config_options:
    seq:
      - id: entries
        type: option_entry
        repeat: eos
        doc: "List of configuration options, repeated until end of stream."

  option_entry:
    seq:
      - id: type
        type: u1
        doc: "Option type. 1 is for MRU."
        valid: 1  # Option type should be 1 for MRU

      - id: length
        type: u1
        doc: "Option length, includes type and length fields."
        valid:  # Ensure valid length to avoid parsing errors
          min: 2

      - id: body
        size: length - 2
        doc: "The actual option data, specific to the option type."
        type: mru_option
          

  mru_option:
    seq:
      - id: maximum_receive_unit
        type: u2
        doc: "Maximum Receive Unit for MRU option."
