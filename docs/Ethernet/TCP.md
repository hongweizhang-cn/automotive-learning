
# Transport Layer Protocols: TCP

## My Understanding
### 1. Layer 4 Fundamentals

There are two main transport protocols in Layer 4 (OSI layer model): TCP and UDP. 

* **TCP (Transmission Control Protocol)** is connection-oriented and packages data into **segments**.
* **UDP (User Datagram Protocol)** is connectionless and packages data into **datagrams**.

The choice between TCP, UDP, or a hybrid approach depends on the application's specific trade-offs between transmission speed, data reliability, and security.

At Layer 3 (Network Layer), the Internet Protocol (IP) handles node-to-node routing to ensure data reaches its destination. Meanwhile, Layer 4 ports act as communication endpoints to multiplex data to higher-layer applications. When a port is open, data can be actively exchanged with its corresponding process or service.

---

### 2. TCP (Transmission Control Protocol)

#### 2.1 Overview and Characteristics

Unlike UDP, TCP (Transmission Control Protocol) is a connection-oriented, point-to-point transport protocol. An explicit logical connection must be established between two endpoints—identified by their IP addresses and port numbers—before application data transmission begins.

#### 2.2 Connection Establishment: The Three-Way Handshake

1. **Step 1 (SYN):** The initiator transmits a TCP segment with the `SYN` flag set. This segment includes a randomly generated Initial Sequence Number (ISN), a receive window size, and optional parameters. The sequence number tracks the segment's position within the overall byte stream, allowing the receiver to reassemble data in the correct order. The window field advertises the sender’s available buffer space to prevent buffer overflow. Since TCP is full-duplex, both endpoints must advertise their receive window sizes to each other.
2. **Step 2 (SYN-ACK):** The responder returns a segment with both `SYN` and `ACK` flags set. This acknowledges the initial connection request while simultaneously transmitting the responder's own ISN and window size, confirming mutual node identification.
3. **Step 3 (ACK):** The initiator sends a final `ACK` segment to confirm connection setup. Once received, the connection is fully established, and bidirectional data transfer begins.

#### 2.3 Reliability and Flow Control Mechanisms

Because TCP relies on explicit unicast connections, it does **not** support Multicast or Broadcast messaging. Instead, it provides end-to-end reliability and flow control through several core mechanisms:

* **Data Integrity:** A Checksum (calculated over the header and payload) protects segments against bit corruption during transit.
* **In-Order Delivery:** Sequence numbers allow the receiver to correctly reorder out-of-sequence segments.
* **Positive Acknowledgment:** The receiver sends `ACK` segments containing valid Acknowledgment Numbers to confirm error-free delivery.
* **Flow Control:** Each segment updates the receive window field, dynamically informing the sender how much data the receiver can currently buffer.
* **Retransmission (RTO):** Every transmitted segment triggers an independent Retransmission Timer. If an `ACK` is not received before the timer expires—indicating packet loss or corruption—the sender retransmits the segment. Upon receiving a valid `ACK`, the corresponding timer is cleared.

#### 2.4 Connection Termination (Four-Way Wave)

Once data exchange is complete, either node can initiate connection teardown by sending a segment with the `FIN` flag set. The receiving node acknowledges this with an `ACK`, entering a half-closed state. When the receiver is also ready to close its side of the connection, it transmits its own `FIN` segment. Upon final acknowledgment from the original sender, the connection is officially closed, preventing any further data transmission.