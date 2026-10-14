from scapy.all import rdpcap, TCP, UDP, IP

# Load the packet capture file
packets = rdpcap("botnet-capture-20110812-rbot.pcap")

# Display formatted headers for the first 20 IPv4 TCP or UDP packets
shown = 0
for pkt in packets:
    if IP in pkt:
        # Filter and display TCP packet details
        if TCP in pkt:
            print(
                f"Source: {pkt[IP].src}"
                f"\tDestination: {pkt[IP].dst}" 
                f"\tProtocol: TCP"
                f"\tSource Port: {pkt[TCP].sport}"
                f"\tDestination Port: {pkt[TCP].dport}"
            )
            shown += 1
        # Filter and display UDP packet details
        elif UDP in pkt:
            print(
                f"Source: {pkt[IP].src}" 
                f"\tDestination: {pkt[IP].dst}" 
                f"\tProtocol: UDP"
                f"\tSource Port: {pkt[UDP].sport}"
                f"\tDestination Port: {pkt[UDP].dport}"
                )
            shown += 1
        # Stop displaying once 20 UDP or TCP packets have been displayed
        if shown == 20:
            break

# Count all TCP packets in the packet capture file
tcp_packets = []
for pkt in packets:
    if TCP in pkt:
        tcp_packets.append(pkt)

print(f"TCP packets: {len(tcp_packets)}")

# Count all UDP packets in  the packet capture file
udp_packets = []
for pkt in packets:
    if UDP in pkt:
        udp_packets.append(pkt)

print(f"UDP packets: {len(udp_packets)}")