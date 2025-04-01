import os
import struct
from datetime import datetime

def save_trace_binary(input_packet_sequence, folder="harvested_test_cases"):
    """
    Saves the list of packets in a binary file with length-prefixed format.

    Args:
        folder (str): Directory to save trace files.
    """
    if not input_packet_sequence:
        print("No packets to save.")
        return
    
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin")

    with open(filename, "wb") as f:
        for packet in input_packet_sequence:
            packet_length = len(packet)
            f.write(struct.pack("I", packet_length))  # Store length (4 bytes)
            f.write(bytes(packet))  # Store packet
    
    print(f"Trace saved to {filename}")
