def packet_type(packet):

  if packet is None:
      return "UNKNOWN"
  if isinstance(packet, bytes):
      packet_bytes = packet
  else:
      packet_bytes = bytes(packet)  # Convert Scapy packet to raw bytes

  print(f"Packet (Hex): {packet_bytes.hex()}")
  # print(f"Received Packet (Hex): {packet.hex()}")
  if len(packet_bytes) < 14:
      return "Invalid packet: too short"

  # Extract EtherType (Ethernet header starts at index 12, EtherType is at index 12-13)
  ether_type = int.from_bytes(packet_bytes[12:14], 'big')

  # Check for PPPoE Discovery Stage
  if ether_type == 0x8863:
      # PPPoE Discovery header starts at index 14, so minimum packet length should be 20 bytes
      if len(packet_bytes) < 20:
          return "Invalid PPPoE Discovery packet: too short"
      # Extract the Code field from the PPPoE Discovery header (byte 14)
      code = packet_bytes[15]
      # PPPoE Discovery Codes
      PPPOE_CODES = {
          0x09: 'PADI',
          0x07: 'PADO',
          0x19: 'PADR',
          0x65: 'PADS',
          0xA7: 'PADT'
      }
      return PPPOE_CODES.get(code, "Unknown PPPoE Discovery Packet")

  # Check for PPPoE Session Stage
  elif ether_type == 0x8864:
      # PPPoE Session header starts at index 14, and PPP header starts at index 20 (minimum packet length: 24 bytes)
      if len(packet_bytes) < 24:
          return "Invalid PPPoE Session packet: too short"
      
      # Debug: Print the raw PPPoE and PPP header
      print("PPPoE Header:", packet_bytes[38:40])
      print("PPP Protocol (bytes 20-21):", packet_bytes[38:40])

      # Extract the PPP Protocol field (2 bytes after the PPPoE header, i.e., from byte 20)
      ppp_protocol = int.from_bytes(packet_bytes[20:22], 'big')

      # Debug: Print the extracted PPP protocol value
      print("Extracted PPP Protocol:", hex(ppp_protocol))

      # PPP Protocols
      PPP_PROTOCOLS = {
          0xc021: 'LCP',
          0xc023: 'PAP',
          0xc223: 'CHAP'
      }
      
      # Check for LCP
      if ppp_protocol == 0xc021:
          # Extract LCP Code (byte 22)
          
          lcp_code = int.from_bytes(packet_bytes[22:23], 'big')
          print(hex(lcp_code))
          LCP_CODES = {
              1: 'LCP-CONFREQ',
              2: 'LCP-CONFACK',
              3: 'LCP-CONFNACK',
              # 4: 'LCP Termination Request',
              # 5: 'LCP Termination Acknowledgment',
              # 6: 'LCP Code Reject',
              # 7: 'LCP Protocol Reject',
              #8: 'ECHO-REQ',
              9: 'ECHO-REQ',
              10:'ECHO-REP',
              #11: 'LCP Identification',
              #12: 'LCP Time Stamp Request',
              #13: 'LCP Time Stamp Acknowledgment'
          }
          return LCP_CODES.get(lcp_code, "Unknown LCP Packet")
      elif ppp_protocol == 0x8021:
      # Extract LCP Code (byte 22)
        ipcp_code = int.from_bytes(packet_bytes[22:23], 'big')
        print(hex(ipcp_code))
        IPCP_CODES = {
            1: 'IPCP-CONFREQ',
            2: 'IPCP-CONFACK',
            3: 'IPCP-CONFNACK',
            # 4: 'LCP Termination Request',
            # 5: 'LCP Termination Acknowledgment',
            # 6: 'LCP Code Reject',
            # 7: 'LCP Protocol Reject',
            #8: 'ECHO-REQ',
            9: 'ECHO-REQ',
            10:'ECHO-REP',
            #11: 'LCP Identification',
            #12: 'LCP Time Stamp Request',
            #13: 'LCP Time Stamp Acknowledgment'
        }
        return IPCP_CODES.get(ipcp_code, "Unknown IPCP Packet")

      # Check for PAP
      elif ppp_protocol == 0xc023:
          # Extract PAP Code (byte 22)
#          pap_code = int.from_bytes(packet_bytes[22:23], 'big')
          pap_code = int.from_bytes(packet_bytes[23:24], 'big') 
          print(hex(pap_code))
          PAP_CODES = {
              1: 'PAP-REQ',
              2: 'PAP-ACK',
              3: 'PAP Authentication Reject'
          }
          return PAP_CODES.get(pap_code, "Unknown PAP Packet")

      else:
          return "PPP Session Data"

  else:
      return "Unknown EtherType"
