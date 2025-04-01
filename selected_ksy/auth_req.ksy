meta:
  id: authenticate_request
  title: Authenticate-Request Packet
  license: CC0-1.0
  file-extension: areq
  endian: be

seq:
  - id: code
    type: u1
    valid: 1
    doc: |
      Code for Authenticate-Request, must be 1.
  - id: identifier
    type: u1
    valid: 1
    doc: |
      The Identifier field is one octet and aids in matching requests and replies. 
      The Identifier field MUST be changed each time an Authenticate-Request packet is issued.
  - id: length
    type: u2
    valid: 23
    doc: |
      Length of the packet, including the Code, Identifier, Length, Peer-ID Length, Peer-ID, Password Length, and Password.
  - id: peer_id_length
    type: u1
    valid: 9
    doc: |
      The Peer-ID Length field is one octet and indicates the length of the Peer-ID field.
  - id: peer_id
    valid: "gecuser01"
    type: str
    doc: |
      The Peer-ID field is zero or more octets and indicates the name of the peer to be authenticated.
  - id: passwd_length
    type: u1
    valid:
      min: 8
      max: 8
    doc: |
      The Passwd-Length field is one octet and indicates the length of the Password field.
  - id: password
    size: passwd_length
    type: str
    valid: "test#321"
    doc: |
      The Password field is zero or more octets and indicates the password to be used for authentication.
