from scapy.all import rdpcap, wrpcap, PPPoED
from scapy.all import rdpcap
from scapy.all import *
from generation_fuzzer_main import generation_fuzzer
import random
import os
import socket
import struct
import fcntl
from packet_type import packet_type
from  detect_violation_in_grammar import check_sequence
from harvesting import save_trace_binary
from invalid_cases import simulate_invalid_cases

current_state = "Idle"  # Global variable

class DeviationDetectedException(Exception):
    pass

trace=""
input_packet_sequence=[]
mutate_packet_sequence=[]

def detect_interesting(packet):
    global current_state  # Use the global variable
    
    is_interesting, deviations, current_state = detect_packet_deviation(packet, current_state)

    if is_interesting:
        print("Interesting test case found! Deviations:", deviations)
        raise DeviationDetectedException("Deviation detected. Stopping the program.")
        
    else:
        print("No deviations detected.")
    return is_interesting


LOG_FILE = "fuzzer_bot.log"

# Constants
ETH_P_PPP_DISC = 0x8863  # Protocol for PPPoE Discovery
ETH_P_PPP_SESS = 0x8864  # Protocol for PPPoE Session
BROADCAST_MAC = b'\xff\xff\xff\xff\xff\xff'  # Broadcast address

# Function to get the MAC address of a network interface
def get_mac_address(interface):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(sock.fileno(), 0x8927, struct.pack('256s', interface[:15].encode('utf-8')))
    sock.close()
    return info[18:24]

# Function to read a packet from a PCAP file
def read_packet_from_pcap(filename, index=0):
    packets = rdpcap(filename)
    if index >= len(packets):
        raise IndexError(f"PCAP file contains only {len(packets)} packets.")
    return bytes(packets[index])

# Function to send a raw Ethernet packet
def send_packet(sock, interface, packet, protocol=ETH_P_PPP_DISC):
    addr = (interface, protocol)

    packet_bytes = bytes(packet)

    #VIOLATION START
    global input_packet_sequence
    input_packet_sequence.append(packet)
    global mutate_packet_sequence
    mutate_packet_sequence.append(packet)
    global trace
    packet_name = packet_type(packet_bytes)
    trace += f" {packet_name}"
    #VIOLATION END


    sock.sendto(packet_bytes, addr)
    print(f"Packet sent on {interface}")

    # try:
    #     detect_interesting(packet)
    # except DeviationDetectedException as e:
    #     print(e)
    #     # Stop the program by re-raising the exception
    #     raise
# def send_packet_lcp(sock, interface, packet):
#     addr = (interface, ETH_P_LCP_DISC)
#     sock.sendto(packet, addr)
#     print(f"Packet sent on {interface}")

# def send_packet_sess(sock, interface, packet):
#     addr = (interface, ETH_P_PPP_SESS)
#     sock.sendto(packet, addr)
#     print(f"PPP Session Packet sent on {interface}")


# Function to listen for a response
def listen_for_response(sock):
    try:
        # Receive a response from the socket
        response = sock.recv(2048)

        #VIOLATION START
        global input_packet_sequence 
        input_packet_sequence.append(response)
        global trace
        packet_name = packet_type(response)
        trace += f" {packet_name}"
        #VIOLATION END

        print(f"Received response: {response[:50].hex()}...")
        
        # Check for deviations using detect_interesting
        # try:
        #     detect_interesting(response)
        # except DeviationDetectedException as e:
        #     print(e)
        #     # Stop the program by re-raising the exception
        #     raise

        return response

    except socket.timeout:
        print("No response received.")
        return None

    
def generate_echo_reply(echo_request_packet):
    # Ethernet header details
    ethernet_header_length = 14
    pppoe_header_length = 6  # PPPoE header (Version, Type, Code, Identifier, Length)

    # Extract Ethernet header
    ethernet_header = echo_request_packet[:ethernet_header_length]
    dst_mac, src_mac, ethertype = struct.unpack("!6s6sH", ethernet_header)

    # Swap source and destination MAC addresses
    swapped_ethernet_header = src_mac + dst_mac + struct.pack("!H", ethertype)

    # Extract PPPoE header
    pppoe_header = echo_request_packet[ethernet_header_length:ethernet_header_length + pppoe_header_length]
    version_type, code, identifier, length = struct.unpack("!BBBH", pppoe_header[:5])

    # Extract PPP payload (starting after PPPoE header)
    ppp_payload = echo_request_packet[ethernet_header_length + pppoe_header_length:]
    print(code)
    # Validate the input packet
    if code != 0x00:  # Code 0x00 indicates a valid PPPoE Session packet
        raise ValueError("Input is not a valid PPPoE session packet.")

    # Extract LCP fields from PPP payload
    lcp_header_length = 6  # LCP header (Code, Identifier, Length)
    lcp_header = ppp_payload[:lcp_header_length]
    protocol,lcp_code, lcp_identifier, lcp_length = struct.unpack("!HBBH", lcp_header)
    print(lcp_code)
    # Validate LCP Code (should be 1 for Configure-Request)
    if lcp_code != 9:
        raise ValueError("Input is not a valid Echo-Request packet.")

    # Update the LCP Code to 2 (Configure-Ack)
    updated_lcp_header = struct.pack("!HBBH",protocol, 10, lcp_identifier, lcp_length)

    # Retain the rest of the PPP payload (options remain unchanged)
    lcp_options = ppp_payload[lcp_header_length:]
    updated_ppp_payload = updated_lcp_header + lcp_options

    # Construct the final packet
    lcp_reply_packet = swapped_ethernet_header + pppoe_header + updated_ppp_payload

    return lcp_reply_packet
    
def generate_pcap_authentication_request(authentication_request_generated_file, session_id):

    # Path to input PAP Authentication-Request packet data
   # pap_file = "/Users/darshanadask/main_project/19_Nov/authenticate_request0.areq"
    with open(authentication_request_generated_file, "rb") as f:
        pap_data = f.read()

    # Construct Ethernet frame for PPPoE Session
    eth_frame = Ether(src="11:22:33:44:55:66", dst="22:33:44:55:66:77", type=0x8864)  # 0x8864 = PPPoE Session

    # Add PPPoE header
    pppoe_header = PPPoE(version=1, type=1, code=0x00, sessionid=session_id)

    # Add PPP header for PAP (protocol ID = 0xc023)
    ppp_header = PPP(proto=0xc023)

    # Combine everything to form the full frame
    pppoe_packet = eth_frame / pppoe_header / ppp_header / Raw(load=pap_data)

    # Define the output folder and file paths
  #  output_folder = "vbng"
   # output_file = os.path.join(output_folder, "pap_auth_req.pcap")

    # Create the folder if it doesn't exist
  #  os.makedirs(output_folder, exist_ok=True)

    # Write the packet to the pcap file in the specified folder
  #  wrpcap(output_file, [pppoe_packet])

  #  print(f"PAP auth-Request packet saved to {output_file}")

    pcap_file = "configure_request1.pcap"
    wrpcap(pcap_file, [pppoe_packet])

    print(f"PAP auth-Request packet saved to {pcap_file}")
    return pcap_file



def generate_pcap_with_session_id(configure_request_generated_file, session_id):
    # from scapy.all import *

    # # Load your Configure-Request file (raw PPPoE packet)
    # config_request_file = "testcases/configure_request0.cfgreq"
    # with open(config_request_file, "rb") as f:
    #     config_request_data = f.read()

    # # Construct Ethernet frame
    # eth_frame = Ether(src="00:11:22:33:44:55", dst="ff:ff:ff:ff:ff:ff", type=0x8863)  # 0x8863 = PPPoE Discovery
    # pppoe_packet = eth_frame / PPPoED(version=1, type=1, code=0x00, sessionid=0x0001) / PPP(proto=0xc021) / Raw(load=config_request_data)

    # # Write to a pcap file
    # pcap_file = "configure_request.pcap"
    # wrpcap(pcap_file, [pppoe_packet])

    # print(f"Configure-Request packet saved to {pcap_file}")



    # Load your .lcp_echo_request file (raw LCP Echo-Request packet data)
    with open(configure_request_generated_file, "rb") as f:
        lcp_data = f.read()
      
    # Construct Ethernet frame for PPPoE Session
    eth_frame = Ether(src="11:22:33:44:55:66", dst="22:33:44:55:66:77", type=0x8864)  # 0x8864 = PPPoE Session
    
    # Add PPPoE header
    pppoe_header = PPPoE(version=1, type=1, code=0x00, sessionid=session_id)

    # Add PPP header for LCP (protocol ID = 0xc021)
    ppp_header = PPP(proto=0xc021)

    # Combine everything to form the full frame
    pppoe_packet = eth_frame / pppoe_header / ppp_header / Raw(load=lcp_data)

    # Write to a pcap file
    #pcap_file = "configure_request1.pcap"
   # wrpcap(pcap_file, [pppoe_packet])

   # print(f"LCP conf-Request packet saved to {pcap_file}")
    return pppoe_packet




def extract_session_id(response):
    """
    Extracts the Session ID from a PADS response.
    Args:
        response (bytes): The raw response packet.
    Returns:
        int: Extracted Session ID or None if the response is invalid.
    """
    if len(response) < 20:  # Minimum length for Ethernet + PPPoE header
        print("Invalid response: Too short.")
        return None

    # Parse PPPoE header
    ethertype = int.from_bytes(response[12:14], byteorder='big')
    if ethertype != 0x8863:
        print(f"Not a PPPoE Discovery packet. Ethertype: {hex(ethertype)}")
        return None

    version_type = response[14]  # Version and Type field
    code = response[15]          # Code field
    session_id = int.from_bytes(response[16:18], byteorder='big')  # Session ID

    # Verify this is a PADS packet (Code = 0x65)
    if code != 0x65:
        print(f"Not a PADS packet. CODE field is {hex(code)}.")
        return None

    print(f"Session ID extracted: {hex(session_id)}")
    return session_id


import struct


import struct

def generate_configure_acknowledge_packet(config_request_packet):
    """
    Generates a Configuration-Ack packet based on the received Configuration-Request packet.
    
    Args:
        config_request_packet (bytes): The raw bytes of the received packet (including Ethernet frame).
    
    Returns:
        bytes: The raw bytes of the generated Configuration-Ack packet.
    """
    # Ethernet header details
    ethernet_header_length = 14
    pppoe_header_length = 6  # PPPoE header (Version, Type, Code, Identifier, Length)

    # Extract Ethernet header
    ethernet_header = config_request_packet[:ethernet_header_length]
    dst_mac, src_mac, ethertype = struct.unpack("!6s6sH", ethernet_header)

    # Swap source and destination MAC addresses
    swapped_ethernet_header = src_mac + dst_mac + struct.pack("!H", ethertype)

    # Extract PPPoE header
    pppoe_header = config_request_packet[ethernet_header_length:ethernet_header_length + pppoe_header_length]
    version_type, code, identifier, length = struct.unpack("!BBBH", pppoe_header[:5])

    # Extract PPP payload (starting after PPPoE header)
    ppp_payload = config_request_packet[ethernet_header_length + pppoe_header_length:]
    print(code)
    # Validate the input packet
    if code != 0x00:  # Code 0x00 indicates a valid PPPoE Session packet
        raise ValueError("Input is not a valid PPPoE session packet.")

    # Extract LCP fields from PPP payload
    lcp_header_length = 6  # LCP header (Code, Identifier, Length)
    lcp_header = ppp_payload[:lcp_header_length]
    protocol,lcp_code, lcp_identifier, lcp_length = struct.unpack("!HBBH", lcp_header)
    print(lcp_code)
    # Validate LCP Code (should be 1 for Configure-Request)
    if lcp_code != 1:
        raise ValueError("Input is not a valid LCP Configure-Request packet.")

    # Update the LCP Code to 2 (Configure-Ack)
    updated_lcp_header = struct.pack("!HBBH",protocol, 2, lcp_identifier, lcp_length)

    # Retain the rest of the PPP payload (options remain unchanged)
    lcp_options = ppp_payload[lcp_header_length:]
    updated_ppp_payload = updated_lcp_header + lcp_options

    # Construct the final packet
    config_ack_packet = swapped_ethernet_header + pppoe_header + updated_ppp_payload

    return config_ack_packet

def generate_configure_request_packet(config_request_packet):
    """
    Generates a Configuration-Ack packet based on the received Configuration-Request packet.
    
    Args:
        config_request_packet (bytes): The raw bytes of the received packet (including Ethernet frame).
    
    Returns:
        bytes: The raw bytes of the generated Configuration-Ack packet.
    """
    # Ethernet header details
    ethernet_header_length = 14
    pppoe_header_length = 6  # PPPoE header (Version, Type, Code, Identifier, Length)

    # Extract Ethernet header
    ethernet_header = config_request_packet[:ethernet_header_length]
    dst_mac, src_mac, ethertype = struct.unpack("!6s6sH", ethernet_header)

    # Swap source and destination MAC addresses
    swapped_ethernet_header = src_mac + dst_mac + struct.pack("!H", ethertype)

    # Extract PPPoE header
    pppoe_header = config_request_packet[ethernet_header_length:ethernet_header_length + pppoe_header_length]
    version_type, code, identifier, length = struct.unpack("!BBBH", pppoe_header[:5])

    # Extract PPP payload (starting after PPPoE header)
    ppp_payload = config_request_packet[ethernet_header_length + pppoe_header_length:]
    print(code)
    # Validate the input packet
    if code != 0x00:  # Code 0x00 indicates a valid PPPoE Session packet
        raise ValueError("Input is not a valid PPPoE session packet.")

    # Extract LCP fields from PPP payload
    lcp_header_length = 6  # LCP header (Code, Identifier, Length)
    lcp_header = ppp_payload[:lcp_header_length]
    protocol,lcp_code, lcp_identifier, lcp_length = struct.unpack("!HBBH", lcp_header)
    print(lcp_code)
    # Validate LCP Code (should be 1 for Configure-Request)
    if lcp_code != 1:
        raise ValueError("Input is not a valid LCP Configure-Request packet.")

    # Update the LCP Code to 2 (Configure-Ack)
    updated_lcp_header = struct.pack("!HBBH",protocol, lcp_code, 1, lcp_length)

    # Retain the rest of the PPP payload (options remain unchanged)
    lcp_options = ppp_payload[lcp_header_length:]
    updated_ppp_payload = updated_lcp_header + lcp_options

    # Construct the final packet
    config_ack_packet = swapped_ethernet_header + pppoe_header + updated_ppp_payload

    return config_ack_packet



# Example usage:
# received_packet = <data from socket>
# config_ack_packet = generate_config_ack_with_ethernet(received_packet)
# sock.send(config_ack_packet)

def generate_discovery_phase_packet(generated_discovery_phase_packet, dst_address, source_addr= "11:22:33:44:55:66"):
    #padi_file = "testcases/padi_packet.padi"
    with open(generated_discovery_phase_packet, "rb") as f:
        padi_data = f.read()

    # Construct Ethernet frame
    eth_frame = Ether(src= source_addr, dst=dst_address, type=0x8863)  # 0x8863 = PPPoE Discovery
    pppoe_packet = eth_frame / Raw(load=padi_data)
    return pppoe_packet
    # Write to a pcap file
    #pcap_file = "padi.pcap"
    #wrpcap(pcap_file, [pppoe_packet])


   # print(f"PADI packet saved to {pcap_file}")
def generate_padt_generated_file_with_session_id(padt_generated_file, new_session_id):
    """
    Replace the session_id field in a PADT packet binary file.
    
    :param file_path: Path to the binary file.
    :param new_session_id: New session ID to write (integer).
    """
    # Convert the new session ID to a 2-byte big-endian representation
    new_session_id_bytes = new_session_id.to_bytes(2, byteorder='big')

    # Open the binary file and update the session_id
    with open(padt_generated_file, 'r+b') as f:
        # Seek to the position of the session_id field
        # session_id is located at byte offset 2 (version_type + code)
        f.seek(2)
        
        # Write the new session_id
        f.write(new_session_id_bytes)
    return padt_generated_file
# Main fuzzer bot functionality
def fuzzer_bot(interface, padi_generated_file, padr_generated_file, configure_request_generated_file, echo_request_generated_file, authentication_request_generated_file, padt_generated_file, source_addr= "11:22:33:44:55:66"):

    
    # Create a raw socket
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_PPP_DISC))
    sock.bind((interface, 0))
    sock.settimeout(5)  # Set a timeout for receiving packets

    # Step 1: Read PADI packet from PCAP
    padi_packet= generate_discovery_phase_packet(padi_generated_file, "ff:ff:ff:ff:ff:ff", source_addr)
    try:
      #  padi_packet = read_packet_from_pcap(padi_pcap_file, index=0)  # Assuming first packet is PADI
       print(f"PADI Packet: {padi_packet.summary()}")
    except Exception as e:
        print(f"Error reading PADI packet: {e}")
        return [],[] ##temporary
    # Step 2: Send PADI and collect PADO response
    send_packet(sock, interface, padi_packet)
    #INTERESTING
    pado_response = listen_for_response(sock)

    with open(LOG_FILE, "ab") as log_file:
        if pado_response:
            log_file.write(pado_response)

    #whypadr_generated_file
    # Step 4: Read PADR packet from PCAP
    padr_packet = generate_discovery_phase_packet(padr_generated_file, "22:33:44:55:66:77")
    try:
        print(f"PADR Packet: {padr_packet.summary()}")
    except Exception as e:
        print(f"Error reading PADR packet: {e}")
        return [],[] ##temporary

    # Step 5: Send PADR and collect PADS response
    send_packet(sock, interface, padr_packet)
    pads_response = listen_for_response(sock)

    with open(LOG_FILE, "ab") as log_file:
        if pads_response:
            log_file.write(pads_response)
    
    session_id=extract_session_id(pads_response)

    configure_request_packet= generate_pcap_with_session_id(configure_request_generated_file, session_id)
    #modified_configure_request_pcap_file= "modified_configure_request_pcap_file.pcap"
    
    
    # conf_request_1= listen_for_response(sock)
    
    
    # # Step 7: Read LCP Configuration Request packet from PCAP
    
      # Step 8: Send LCP Configuration Request and collect response

    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_PPP_SESS))
    
    ##CONFIGURATION ACKNOWLEDGEMENT

    lcp_response1= listen_for_response(sock)
    configure_acknowledge_packet= generate_configure_acknowledge_packet(lcp_response1)
    send_packet(sock, interface, configure_acknowledge_packet, protocol=ETH_P_PPP_SESS)


    # ##CONFIGURATION REQUEST
    try:
       #  configure_request_packet = read_packet_from_pcap(configure_request_pcap_file, index=0)
       print(f"Configuration Request Packet: {configure_request_packet.summary()}")
    except Exception as e:
         print(f"Error reading LCP Configuration Request packet: {e}")
         return [],[] ##temporary
    
    #configure_request_packet= generate_configure_request_packet(lcp_response1)
    send_packet(sock, interface, configure_request_packet, protocol=ETH_P_PPP_SESS)
    lcp_response = listen_for_response(sock)

    
    #ECHO REPLY
    # try:
    #     echo_request_packet = read_packet_from_pcap(echo_request_pcap, index=0)
        
    # except Exception as e:
    #     print(f"Error reading echo request  packet: {e}")
    #     return
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_PPP_SESS))
    
    lcp_response2 = listen_for_response(sock)
    #temporary
    while(packet_type(lcp_response2)!='ECHO-REQ'):
       lcp_response2 = listen_for_response(sock) 
    #temporary end
    echo_reply_packet = generate_echo_reply(lcp_response2)
    send_packet(sock, interface, echo_reply_packet, protocol=ETH_P_PPP_SESS)
    


    ##ECHO REQUEST
    echo_request_packet= generate_pcap_with_session_id(echo_request_generated_file, session_id)
    try:
        #echo_request_packet = read_packet_from_pcap(echo_request_pcap, index=0)  # Assuming first packet is PADI
        print(f"Echo Request Packet: {echo_request_packet.summary()}")
    except Exception as e:
        print(f"Error reading PADI packet: {e}")
        return [],[] ##temporary

    send_packet(sock, interface, echo_request_packet, protocol=ETH_P_PPP_SESS )
    lcp_response = listen_for_response(sock)

    #AUTHENTICATION REQUEST
    authentication_request_pcap_file= generate_pcap_authentication_request(authentication_request_generated_file, session_id)
    try:
        authentication_request_packet = read_packet_from_pcap(authentication_request_pcap_file, index=0)  # Assuming first packet is PADI
    except Exception as e:
        print(f"Error reading PADI packet: {e}")
        return [],[] ##temporary
    send_packet(sock, interface, authentication_request_packet, protocol=ETH_P_PPP_SESS)
    lcp_response = listen_for_response(sock)

    ##CONFIGURATION ACKNOWLEDGEMENT1
    lcp_response_ack1= listen_for_response(sock)
    configure_acknowledge_packet= generate_configure_acknowledge_packet(lcp_response_ack1)
    send_packet(sock, interface, configure_acknowledge_packet, protocol=ETH_P_PPP_SESS)


    #ECHO REPLY

    # try:
    #     echo_request_packet = read_packet_from_pcap(echo_request_pcap, index=0)
        
    # except Exception as e:
    #     print(f"Error reading echo request  packet: {e}")
    #     return
   # sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_PPP_SESS))
    lcp_response2 = listen_for_response(sock)
    echo_reply_packet = generate_echo_reply(lcp_response2)
    send_packet(sock, interface, echo_reply_packet, protocol=ETH_P_PPP_SESS)
    
    # Step 9: Log LCP response
    with open(LOG_FILE, "ab") as log_file:
        if lcp_response:
            log_file.write(lcp_response)
    

    

    

    number_of_times = random.randint(1, 1)
    while(number_of_times>0):
        ##ECHO REPLY 2
        lcp_response_echo2 = listen_for_response(sock)
        echo_reply_packet = generate_echo_reply(lcp_response_echo2)
        send_packet(sock, interface, echo_reply_packet, protocol=ETH_P_PPP_SESS)
        ##ECHO REQUEST
        send_packet(sock, interface, echo_request_packet, protocol=ETH_P_PPP_SESS )
        print("ECHO REQ")
        lcp_response = listen_for_response(sock)
        number_of_times-=1
    
    ##PADT 
    padt_generated_file_with_session_id = generate_padt_generated_file_with_session_id(padt_generated_file, session_id)
    padt_packet= generate_discovery_phase_packet(padt_generated_file_with_session_id, "22:33:44:55:66:77")
    try:
        #padt_packet = read_packet_from_pcap(padt_pcap, index=0)  # Assuming first packet is PADI
        print(f"PADT Packet: {padt_packet.summary()}")
    except Exception as e:
        print(f"Error reading PADI packet: {e}")
        return [],[] ##temporary

    send_packet(sock, interface, padt_packet, protocol=ETH_P_PPP_SESS )
    #lcp_response = listen_for_response(sock)

    sock.close()
    print(f"Fuzzer bot operation completed. Logs saved in {LOG_FILE}")
    return trace, input_packet_sequence ##temporary

# Entry point
if __name__ == "__main__":

    interface_name = "enp5s0"
    count=0
    threshold=10
  ##temporary off 
    while(True):
        
        padi_generated_file = generation_fuzzer("selected_ksy/padi5.ksy")
        padr_generated_file = generation_fuzzer("selected_ksy/padr4.ksy")
        configure_request_generated_path = generation_fuzzer("selected_ksy/lcp_conf_req_1.ksy")
        authentication_request_generated_file = generation_fuzzer("selected_ksy/auth_req.ksy")
        echo_request_generated_file =  generation_fuzzer("selected_ksy/lcp_echo.ksy")
        padt_generated_file = generation_fuzzer("selected_ksy/padt.ksy")
        fuzzer_bot(interface_name, padi_generated_file, padr_generated_file, configure_request_generated_path, echo_request_generated_file, authentication_request_generated_file,padt_generated_file)
        #VIOLATION START
        print(trace)
        status= check_sequence(trace)
        if(status=="Violation"):
            print("Violation")
            save_trace_binary(input_packet_sequence)
            save_trace_binary(mutate_packet_sequence,"harvested_for_mutation")
        else:
            print("No Violation")
        
        #INVALID CASES temporary
       #simulate_invalid_cases()
       # count+=1
