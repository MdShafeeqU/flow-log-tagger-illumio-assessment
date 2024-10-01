def parse_lookup_table(lookup_file):
    """
    Reads the lookup table from a file and stores each (dstport, protocol)
    combination with its corresponding tag in a dictionary.

    Args:
        lookup_file (str): Path to the lookup table file.

    Returns:
        dict: A dictionary where keys are (dstport, protocol) tuples, and 
              values are the corresponding tags.
    """
    lookup_table = {}

    with open(lookup_file, 'r') as file:
        next(file)  
        for line in file:
            if not line.strip():
                continue  

            parts = line.strip().split(',')
            if len(parts) != 3 or not parts[0] or not parts[1] or not parts[2]:
                continue 

            dstport = int(parts[0])  
            protocol = parts[1].lower()  
            tag = parts[2].lower()  
            
            lookup_table[(dstport, protocol)] = tag  

    return lookup_table

PROTOCOLS = {
    6: 'tcp',
    17: 'udp',
    1: 'icmp'
}

def parse_flow_logs(flow_log_file, lookup_table):
    """
    Reads the flow logs, matches each log entry to a tag based on the 
    lookup table, and counts occurrences of both tags and port/protocol combinations.

    Args:
        flow_log_file (str): Path to the flow log file.
        lookup_table (dict): Dictionary of (dstport, protocol) -> tag.

    Returns:
        tuple: Two dictionaries, one for tag counts and one for port/protocol combination counts.
    """
    tag_counts = {}  
    port_protocol_counts = {}  

    with open(flow_log_file, 'r') as file:
        for line in file:
            if not line.strip():
                continue  

            parts = line.strip().split()  
            if len(parts) < 8: 
                continue

            dstport = int(parts[5])  
            protocol_number = int(parts[7])  

            # protocol number to protocol name (e.g., 6 -> 'tcp')
            protocol = map_protocol_number(protocol_number)

            # find the corresponding tag from the lookup table, 'Untagged' if not found
            tag = lookup_table.get((dstport, protocol), 'Untagged')

            tag_counts[tag] = tag_counts.get(tag, 0) + 1

            key = (dstport, protocol)
            port_protocol_counts[key] = port_protocol_counts.get(key, 0) + 1

    return tag_counts, port_protocol_counts


def map_protocol_number(protocol_number):
    """
    Maps a protocol number to a human-readable string using the PROTOCOLS dictionary.

    Args:
        protocol_number (int): The protocol number from the flow logs.

    Returns:
        str: The protocol as a string (e.g., 'tcp', 'udp', 'icmp').
    """
    return PROTOCOLS.get(protocol_number, 'unknown')


def write_dict_to_file(data, headers, output_file, is_tuple_key=False):
    """
    Generic function to write a dictionary to a file with given headers.
    
    Args:
        data (dict): Dictionary to write to the file.
        headers (str): Header row to write at the top of the file.
        output_file (str): File path to write to.
        is_tuple_key (bool): If True, indicates the keys are tuples (for port/protocol).
    """
    try:
        with open(output_file, 'w') as file:
            file.write(f"{headers}\n")
            for key, value in data.items():
                if is_tuple_key:  # if key is a tuple (for port/protocol), unpack it
                    file.write(f"{key[0]},{key[1]},{value}\n")
                else:
                    file.write(f"{key},{value}\n")
        print(f"Data written to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")


if __name__ == "__main__":
    lookup_file = 'lookup_table.txt'
    flow_log_file = 'flow_logs.txt'
    tag_counts_output_file = 'tag_counts_output.txt'
    port_protocol_counts_output_file = 'port_protocol_counts_output.txt'
    
    # load the lookup table into memory
    lookup_table = parse_lookup_table(lookup_file)
    
    # process the flow logs and match them with tags
    tag_counts, port_protocol_counts = parse_flow_logs(flow_log_file, lookup_table)
    
    write_dict_to_file(tag_counts, "Tag,Count", tag_counts_output_file)
    write_dict_to_file(port_protocol_counts, "Port,Protocol,Count", port_protocol_counts_output_file, is_tuple_key=True)


