def packet_type(packet):
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
                1: 'LCP Configuration Request',
                2: 'LCP Configuration Acknowledgment',
                3: 'LCP Configuration Reject',
               # 4: 'LCP Termination Request',
               # 5: 'LCP Termination Acknowledgment',
               # 6: 'LCP Code Reject',
               # 7: 'LCP Protocol Reject',
                8: 'LCP Echo Request',
                9: 'LCP Echo Acknowledgment',
               # 10: 'LCP Discard Request',
                #11: 'LCP Identification',
                #12: 'LCP Time Stamp Request',
                #13: 'LCP Time Stamp Acknowledgment'
            }
            return LCP_CODES.get(lcp_code, "Unknown LCP Packet")

        # Check for PAP
        elif ppp_protocol == 0xc023:
            # Extract PAP Code (byte 22)
            pap_code = int.from_bytes(packet_bytes[40:41], 'big')
            print(hex(pap_code))
            PAP_CODES = {
                1: 'PAP Authentication Request',
                2: 'PAP Authentication Acknowledgment',
                3: 'PAP Authentication Reject'
            }
            return PAP_CODES.get(pap_code, "Unknown PAP Packet")

        else:
            return "PPP Session Data"

    else:
        return "Unknown EtherType"


# Example Usage
# packet = bytes.fromhex('407b1b001210000024cd1ac0886411000277001402020012010405d3050619434bca0304c02301000000000000000000')
# print(packet)
# result = analyze_ethernet_header(packet)
# print(f"Packet type: {result}")

expected_transitions = {
    "Idle": {"PADI": "PADI Sent"},
    "PADI Sent": {"PADO": "PADO Received"},
    "PADO Received": {"PADR": "PADR Sent"},
    "PADR Sent": {"PADS": "PADS Received"},
    "PADS Received": {"LCP Configuration Request": "LCP Negotiation"},
    "LCP Negotiation": {"LCP Configuration Acknowledgment": "Authentication Stage"},
    "Authentication Stage": {
        "CHAP": "CHAP Challenge Sent",
        "PAP Authentication Request": "PAP Auth Request Sent"
    },
    "CHAP Challenge Sent": {"CHAP Response": "Authentication Completed"},
    "PAP Auth Request Sent": {"PAP Authentication Acknowledgment": "Authentication Completed"},
    "Authentication Completed": {"NCP Complete": "Online"},
    "Online": {"PADT": "Idle"},
}


# def preprocess_packet(packet):
#     # Ensure packet is bytes
#     if not isinstance(packet, bytes):
#         packet = bytes(packet)

#     # Validate minimum length
#     if len(packet) < 14:
#         raise ValueError("Packet is too short to be valid (minimum 14 bytes).")

#     return packet
def detect_packet_deviation(packet, current_state):
    """
    Detect deviations from the expected state transitions based on classified packets.
    
    Args:
        packets (list of bytes): List of raw packets.
        expected_transitions (dict): Expected state transitions based on packet types.
    
    Returns:
        bool: True if deviation detected (interesting test case), False otherwise.
        list: List of deviations detected.
    """
    #current_state = "Idle"
    deviations = []
   # processed_packet = preprocess_packet(packet)
    #for packet in packets:
        # Classify the packet
    packet_type_str = packet_type(packet)
    
    # Debugging: Print the packet type and current state
    print(f"Packet: {packet_type_str}, Current State: {current_state}")
    
    # Check if packet type is expected in current state
    if packet_type_str in expected_transitions.get(current_state, {}):
        current_state = expected_transitions[current_state][packet_type_str]
    else:
        # Deviation detected
        deviations.append((current_state, packet_type_str))
    
    return len(deviations) > 0, deviations, current_state