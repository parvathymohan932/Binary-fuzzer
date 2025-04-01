meta:
  id: lcp_echo_request
  title: LCP Echo-Request Packet
  endian: be
  description: |
    Represents an LCP Echo-Request packet as defined in the PPP 
    (Point-to-Point Protocol). Includes fields for Identifier, 
    Magic-Number, and optional Data.

seq:
  - id: code
    type: u1
    doc: |
      Code for the LCP Echo-Request packet. This must always be 9.
    valid: 9
  - id: identifier
    type: u1
    valid: 1
    doc: |
      A unique value to match the Echo-Request with the corresponding
      Echo-Reply:
      - Must change whenever the Data field changes.
      - Must change after receiving a valid reply for the previous request.
      - May remain unchanged for retransmissions.
  - id: length
    type: u2
    valid: 4
    doc: |
      Total length of the packet, including header and data fields.
      The minimum value is 8 (header size) plus the size of the Data field.
  - id: magic_number
    type: u4
    doc: |
      A 32-bit value used to detect loopback links:
      - Initially, this field must be zero until successful negotiation
        of the Magic-Number Configuration Option.
      - The sender assigns a unique non-zero value after negotiation to
        help detect loopback conditions.
 # - id: data
  #  size: length - 8
   # doc: |
    #  Optional field containing zero or more octets of uninterpreted data:
     # - Can consist of any binary value.
     # - Its content is defined by the sender.
     # - The end of the Data field is determined by the Length field.

