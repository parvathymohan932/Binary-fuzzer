import os
import struct
from packet_type import packet_type
def load_trace_binary(filename):
    """
    Reads packets from a binary file and checks if the first packet is of type "PADI".

    Args:
        filename (str): Path to the trace file.
    """
    packets = []

    with open(filename, "rb") as f:
        while True:
            length_data = f.read(4)  # Read packet length (4-byte integer)
            if not length_data:
                break  # Stop if no more data
            
            packet_length = struct.unpack("I", length_data)[0]  # Extract length
            packet = f.read(packet_length)  # Read packet
            
            if not packets:  # First packet
                packet_name = packet_type(packet)  # Identify packet type
                if packet_name == "PADI":
                    print(f"{filename}: First packet is PADI ✅")
                else:
                    print(f"{filename}: First packet is {packet_name} ❌")

            packets.append(packet)  # Store packet

    return packets


# Process all traces in the "packet_logs" folder
packet_logs_folder = "packet_logs"

if __name__ == "__main__":
    for filename in os.listdir(packet_logs_folder):
        file_path = os.path.join(packet_logs_folder, filename)
        if os.path.isfile(file_path):  # Ensure it's a file
            load_trace_binary(file_path)
