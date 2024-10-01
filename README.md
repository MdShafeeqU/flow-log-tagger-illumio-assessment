# Flow Log Tagging Program

## Assumptions
1. The program assumes that the flow logs are provided in the default format specified in the AWS documentation for version 2 flow logs. Custom formats are not supported. 
2. The program currently recognizes only the TCP (6), UDP (17), and ICMP (1) protocols. Additional protocols can be supported by updating the **PROTOCOLS** dictionary in the code.
3. It is assumed that the flow logs contain valid protocol numbers. The program does not validate the protocol numbers and expects that all logs are well-formed in this regard.
4. The lookup table is expected to follow a **CSV-like format** with exactly three columns: `dstport`, `protocol`, and `tag`. The program assumes that the structure of the lookup table is valid and well-formed.
5. The program will terminate with an error if either the `lookup_table.txt` or `flow_logs.txt` file is missing. Both files are required for execution. 
6. Flow logs that have missing or malformed entries (e.g., missing columns) are ignored by the program and will not cause it to crash. These entries will simply be skipped.
7. If the lookup table contains duplicate entries for the same `dstport` and `protocol`, the program will assume that the last occurrence overrides earlier ones.

## How to Run

### Prerequisites
1. **Python Version**: Python 3+ installed on your machine. 
2. **Files Required**:
   - `lookup_table.txt`: Contains destination port, protocol, and tag information.
   - `flow_logs.txt`: Contains the flow log data.

### Running the Program
1. Clone this repository.
2. Navigate to the directory and run the following command:
   ```bash
   python main.py
3. Two output files will be generated:
  - **tag_counts_output.txt**: This file contains the count of each tag that was applied.
  - **port_protocol_counts_output.txt**: This file contains the count of each port/protocol combination.

## Tests Performed

### 1. Functional Testing:

- **Valid Lookup Table and Flow Logs**: The program was run with a valid `lookup_table.txt` and `flow_logs.txt`, both containing valid ports and protocols, to ensure correct tagging and counting.
  
- **Empty Lines in Lookup Table**: The lookup table was tested with a few empty lines to verify that they were skipped during processing.

- **Malformed Lines in Lookup Table**: Lines in the lookup table that didn’t follow the correct format (e.g., missing values) were tested to confirm they were ignored without causing issues.

- **Flow Logs with Unknown Protocols**: Logs with unknown protocol numbers were included to check if the program correctly tagged them as 'Untagged'.

- **Empty Flow Log File**: An empty `flow_logs.txt` was used to ensure the program handled the absence of log entries gracefully and produced empty results.

### 2. Error Handling Tests:

- **File Not Found**: The program was tested without the required input files (`lookup_table.txt` or `flow_logs.txt`) to confirm that it generates meaningful error messages when files are missing.

- **Malformed Lines in Flow Logs**: Flow logs with missing fields or incorrect formats were tested to ensure the program skipped these entries and continued processing the rest.

### 3. Edge Case Testing:

- **Only Untagged Logs**: A test case was run with a flow log file that had no matching port/protocol combinations in the lookup table. The program successfully tagged all logs as 'Untagged'.

- **Single Line Files**: The program was tested with only a single entry in both `lookup_table.txt` and `flow_logs.txt` to ensure proper operation with minimal input.

- **Multiple Matches**: Logs with different combinations of ports and protocols were used to verify that the program correctly counted each match.

- **Duplicate Entries in Lookup Table**: A lookup table with duplicate entries for the same port/protocol combination was tested to confirm that the last entry overrides earlier ones.

- **Mixed Case Protocols in Lookup Table**: Mixed case protocols (e.g., `TCP`, `udp`) were tested in the lookup table to ensure the program matched them in a case-insensitive way.

- **Flow Logs with Missing Fields**: Flow logs with fewer columns than expected were tested to check if the program skipped these malformed lines without issues.

- **Large Flow Log File**: A large flow log file (around 10MB) was processed to ensure the program performs well with larger datasets.


## Analysis
1. The program uses **dictionaries** to process flow logs and the lookup table, enabling fast lookups.
2. The code emphasizes **modular design**, ensuring clear separation of concerns.
3. The program is easily extendable to support additional protocols by updating the **PROTOCOLS** dictionary.
4. Basic **error handling** is included, such as managing missing files and handling malformed data.
5. The program has been thoroughly **tested** with various edge cases, including missing fields, malformed lines, and large datasets.