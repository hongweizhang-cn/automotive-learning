# Transport Layer Protocols: UDP

## My Understanding
### 1. Layer 4 Fundamentals

There are two main transport protocols in Layer 4 (OSI layer model): TCP and UDP. 

* **TCP (Transmission Control Protocol)** is connection-oriented and packages data into **segments**.
* **UDP (User Datagram Protocol)** is connectionless and packages data into **datagrams**.

The choice between TCP, UDP, or a hybrid approach depends on the application's specific trade-offs between transmission speed, data reliability, and security.

At Layer 3 (Network Layer), the Internet Protocol (IP) handles node-to-node routing to ensure data reaches its destination. Meanwhile, Layer 4 ports act as communication endpoints to multiplex data to higher-layer applications. When a port is open, data can be actively exchanged with its corresponding process or service.

---

### 2. UDP (User Datagram Protocol)

#### 2.1 Overview and Characteristics

UDP (User Datagram Protocol) is a connectionless Layer 4 protocol that enables lightweight datagram transmission. Unlike TCP, UDP provides no built-in mechanisms to guarantee delivery, and senders receive no feedback regarding lost or corrupted datagrams. Consequently, packet retransmission is not supported at the transport layer, though such reliability mechanisms can be implemented within higher-layer protocols if needed.

#### 2.2 Key Advantages of UDP

* **Low Latency and Predictable Timing:** As a connectionless protocol, UDP eliminates the need for handshakes or receiver acknowledgments. The sender transmits data without waiting for feedback, avoiding additional queueing or round-trip delays.
* **Multicast and Broadcast Capabilities:** UDP supports sending datagrams to multiple nodes (Multicast) or all nodes (Broadcast) simultaneously. This significantly reduces total bus load compared to multiple unicast streams.

#### 2.3 IP Encapsulation and Fragmentation

UDP datagrams are encapsulated directly into IP packets, with the IP header specifying UDP as the payload protocol. Since a UDP datagram can be up to 65,535 bytes—exceeding the standard IP payload limit (typically 1,480 bytes)—IP fragmentation is used to divide larger datagrams across multiple IP packets.

During fragmentation, each IP packet receives a unique Identification field and a Fragment Offset to indicate its original position within the complete datagram. The receiving node reassembles these fragments back into the original UDP datagram. If any individual fragment is lost, reassembly fails; because UDP has no retransmission mechanism, the incomplete datagram and all remaining fragments are discarded.