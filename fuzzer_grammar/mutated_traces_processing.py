import os
import struct
from fuzzer_bot_for_mutated_traces import fuzzer_bot_mutation
from detect_violation_in_grammar import check_sequence
from harvesting import save_trace_binary
from packet_type import packet_type

def process_mutated_traces(folder_path):
    interface_name = "enp5s0"

    # Iterate over all .bin files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".bin"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing: {file_path}")

            mutated_trace_padi = None
            mutated_trace_padr = None
            mutated_trace_conf_req = None
            mutated_trace_echo_req = None
            mutated_trace_auth_req = None
            mutated_trace_padt = None

            with open(file_path, "rb") as f:
                data = f.read()
                offset = 0
                print("REACHED1")

                while offset < len(data):
                    if offset + 4 > len(data):
                        print(f"REACHED2: Not enough data at offset {offset}")
                        break  # Prevent out-of-bounds error

                    print("REACHED3")
                    length_bytes = data[offset:offset+4]
                    print(f"Raw length bytes at offset {offset}: {length_bytes.hex()}")

                    # Try both Big-endian and Little-endian
                    packet_length_be = struct.unpack("!I", length_bytes)[0]
                    packet_length_le = struct.unpack("<I", length_bytes)[0]

                    # Choose the correct length based on expected range
                    if 0 < packet_length_be < (len(data) - offset):
                        packet_length = packet_length_be
                    elif 0 < packet_length_le < (len(data) - offset):
                        packet_length = packet_length_le
                    else:
                        print(f"REACHED4: Invalid packet length at offset {offset}")
                        offset += 4  # Skip the length field and continue
                        continue

                    print(f"Packet Length: {packet_length}")
                    offset += 4  # Move past the length field

                    # Ensure we don't read beyond the file
                    if offset + packet_length > len(data):
                        print(f"REACHED4: Packet too large at offset {offset}, skipping.")
                        break

                    print("REACHED5")
                    packet = data[offset:offset+packet_length]
                    offset += packet_length  # Move to the next packet

                    # Identify packet type
                    packet_type_value = packet_type(packet)
                    print(f"Offset: {offset}, Packet Length: {packet_length}, Packet Type: {packet_type_value}")
                    
                    # Assign packet based on its type
                    if packet_type_value == "PADI":
                        mutated_trace_padi = packet
                    elif packet_type_value == "PADR":
                        mutated_trace_padr = packet
                        print(f"Captured PADR: {mutated_trace_padr.hex()}")
                    elif packet_type_value == "LCP-CONFREQ":
                        mutated_trace_conf_req = packet
                        print(f"Captured LCP-CONFREQ: {mutated_trace_conf_req.hex()}")
                    elif packet_type_value == "ECHO-REQ":
                        mutated_trace_echo_req = packet
                    elif packet_type_value == "PAP-REQ":
                        mutated_trace_auth_req = packet
                    elif packet_type_value == "PADT":
                        mutated_trace_padt = packet
                   

            # Ensure we have valid packets before calling fuzzer_bot_mutation
            if any([mutated_trace_padi, mutated_trace_padr, mutated_trace_conf_req,
                    mutated_trace_echo_req, mutated_trace_auth_req, mutated_trace_padt]):
                trace, input_packet_sequence, mutate_input_sequence = fuzzer_bot_mutation(
                    interface_name, mutated_trace_padi, mutated_trace_padr,
                    mutated_trace_conf_req, mutated_trace_echo_req, mutated_trace_auth_req,
                    mutated_trace_padt
                )

                # Print trace and check for violations
                print(trace)
                status = check_sequence(trace)
                if status == "Violation":
                    print("Violation detected, saving trace.")
                    save_trace_binary(input_packet_sequence)
            else:
                print(f"No valid packets found in {file_path}, skipping fuzzer_bot_mutation.")

# Run the function
process_mutated_traces("mutated_traces")
