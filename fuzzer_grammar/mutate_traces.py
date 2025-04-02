import os
import struct
import random
from packet_type import packet_type

def load_trace_binary(filename):
    """Reads packets from a binary file."""
    packets = []
    
    with open(filename, "rb") as f:
        while True:
            length_data = f.read(4)  # Read packet length (4-byte integer)
            if not length_data:
                break  # Stop if no more data
            
            packet_length = struct.unpack("I", length_data)[0]  # Convert bytes to integer
            packet = f.read(packet_length)  # Read packet data
            packets.append((packet_length, packet))  # Store as tuple
    
    return packets

def save_trace_binary(filename, packets):
    """Saves modified packets back to a binary file."""
    with open(filename, "wb") as f:
        for length, packet in packets:
            f.write(struct.pack("I", length))  # Write packet length
            f.write(packet)  # Write packet data

def identify_packet_indices(trace):
    """Identifies PADI and PADR packets and returns their indices."""
    padi_indices = [i for i, (_, packet) in enumerate(trace) if packet_type(packet) == "PADI"]
    padr_indices = [i for i, (_, packet) in enumerate(trace) if packet_type(packet) == "PADR"]
    return padi_indices, padr_indices

def swap_padi_padr_packets(trace1, trace2):
    """Swaps one PADI and one PADR packet between two traces."""
    padi1, padr1 = identify_packet_indices(trace1)
    padi2, padr2 = identify_packet_indices(trace2)

    swapped_info = []

    if padi1 and padi2:
        idx1, idx2 = random.choice(padi1), random.choice(padi2)
        trace1[idx1], trace2[idx2] = trace2[idx2], trace1[idx1]
        swapped_info.append((idx1, idx2, "PADI"))

    if padr1 and padr2:
        idx1, idx2 = random.choice(padr1), random.choice(padr2)
        trace1[idx1], trace2[idx2] = trace2[idx2], trace1[idx1]
        swapped_info.append((idx1, idx2, "PADR"))

    return swapped_info

# Main script
packet_logs_folder = "harvested_for_mutation"
output_folder = "mutated_traces"
os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

trace_files = [os.path.join(packet_logs_folder, f) for f in os.listdir(packet_logs_folder) if f.endswith(".bin")]

if len(trace_files) < 2:
    print("Not enough traces to perform mutation.")
else:
    count=0
    while(count<10):
        count+=1
        file1, file2 = random.sample(trace_files, 2)
        trace1, trace2 = load_trace_binary(file1), load_trace_binary(file2)
        
        swapped_packets = swap_padi_padr_packets(trace1, trace2)

        if swapped_packets:
            save_trace_binary(os.path.join(output_folder, os.path.basename(file1).replace(".bin", "_mutated.bin")), trace1)
            save_trace_binary(os.path.join(output_folder, os.path.basename(file2).replace(".bin", "_mutated.bin")), trace2)

            print(f"Mutation complete. Mutated traces saved in {output_folder}.")
            print(f"Traces chosen: {file1}, {file2}")
            for idx1, idx2, packet_type in swapped_packets:
                print(f"Swapped {packet_type} packets: Index {idx1} in {file1} ↔ Index {idx2} in {file2}")
        else:
            print("No PADI or PADR packets found in one or both traces. No mutation performed.")
