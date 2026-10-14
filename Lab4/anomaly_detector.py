from scapy.all import rdpcap, TCP, UDP, IP
from collections import defaultdict

# Load the packet capture file
packets = rdpcap("botnet-capture-20110812-rbot.pcap")

# Create dictionary with IP as key and timestamps in a list as the value
ip_timestamps = defaultdict(list)

# Track unique suspicious IPs
suspicious_ips = []

# Process packets
for pkt in packets:
    # Filter for IPv4 TCP or UDP traffic
    if IP in pkt and (TCP in pkt or UDP in pkt):
        src_ip = pkt[IP].src
        current_time = float(pkt.time)
        valid_timestamps = []

        # Keep timestamps within 5 second window
        for t in ip_timestamps[src_ip]:
            if t >= (current_time - 5.0):
                valid_timestamps.append(t)

        # Record the current packet timestamp
        valid_timestamps.append(current_time)

        # Update the dictionary
        ip_timestamps[src_ip] = valid_timestamps

        # Trigger an alert if packet exceeds threshold 
        if len(ip_timestamps[src_ip]) > 20 and src_ip not in suspicious_ips:
            print(f"ALERT: Suspicious activity from {src_ip}")
            suspicious_ips.append(src_ip)