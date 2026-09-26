
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

## Questions

### Q1: Why must the client send a final ACK during the third step of the TCP three-way handshake?

**Answer:**

The **TCP Three-Way Handshake** (`SYN` -> `SYN-ACK` -> `ACK`) is the foundational procedure used to establish a reliable, full-duplex Layer 4 connection between two nodes in IP networking.

The final **ACK (Acknowledgment)** packet sent by the client in Step 3 is critical. Without this final step, TCP cannot guarantee synchronized connection states, reliable initial sequence numbers, or protection against half-open connection resources.

---

### 1. Core Architectural Reasons for the Final ACK

#### A. Confirmation of the Server's Initial Sequence Number (ISN)
* **Bidirectional Sequence Synchronization**: TCP requires both endpoints to establish their own **Initial Sequence Number (ISN)** to track byte streams independently in both directions.
  * In **Step 1**, the client sends its $ISN_C$ (`SYN`).
  * In **Step 2**, the server acknowledges $ISN_C$ (`ACK = ISN_C + 1`) and sends its own $ISN_S$ (`SYN`).
  * In **Step 3**, the client MUST send an `ACK` acknowledging $ISN_S$ (`ACK = ISN_S + 1`).
* **Why It Matters**: If the client never sends the final ACK, the server has no way of knowing whether the client received $ISN_S$. Without sequence synchronization on the server-to-client channel, full-duplex data transfer cannot safely commence.

#### B. Prevention of Half-Open Connections and Resource Leaks
* **Server State Transition**: Upon sending the `SYN-ACK` in Step 2, the server enters the **`SYN-RECEIVED`** state and allocates memory resources (transmission control blocks, buffers, and timers).
* **Final ACK Trigger**: The arrival of the final ACK transitions the server from `SYN-RECEIVED` to **`ESTABLISHED`**.
* **Failure Impact**: Without the final ACK, the server remains stuck in `SYN-RECEIVED` until a timeout occurs. If outdated or delayed duplicate `SYN` packets arrive from an old connection, the client uses the final step (or a `RST` segment) to prevent the server from wasting resources on dead connections.

---

### 2. Handshake Execution Flow and State Transitions

* **Step 1: Client -> Server (`SYN`)**
  * **Client Action**: Sends `SYN` segment with $Seq = ISN_C$.
  * **State Transition**: Client moves from `CLOSED` to `SYN-SENT`.

* **Step 2: Server -> Client (`SYN-ACK`)**
  * **Server Action**: Acknowledges client's ISN ($Ack = ISN_C + 1$) and sends its own ISN ($Seq = ISN_S$).
  * **State Transition**: Server moves from `LISTEN` to `SYN-RECEIVED`.

* **Step 3: Client -> Server (`ACK`)**
  * **Client Action**: Acknowledges server's ISN ($Ack = ISN_S + 1$).
  * **State Transition**: Client moves to `ESTABLISHED` upon sending; Server moves to `ESTABLISHED` upon receiving.

---

### 3. What Happens If the Final ACK Is Lost?

| Failure Scenario | Server Reaction | Network Impact |
| :--- | :--- | :--- |
| **Final ACK Lost on Network** | The server remains in `SYN-RECEIVED` and retransmits its `SYN-ACK` segment according to its retransmission timer. | The client (now in `ESTABLISHED`) can immediately begin sending data. When the server receives the client's data segment, the piggybacked ACK in the data header completes the connection transition. |
| **Client Crashes Before Step 3** | The client never sends the final ACK. The server's retransmission timer eventually expires after maximum retries. | The server sends a `RST` or silently closes the socket, releasing allocated buffer memory to prevent `SYN` flooding vulnerabilities. |

---

### 4. Summary

* **Sequence Mutual Sync**: The 2-way exchange syncs client-to-server data; the 3rd step (final ACK) completes server-to-client sequence synchronization.
* **State Finalization**: The final ACK confirms to the server that both directions of the communication path are open, transitioning the server socket from `SYN-RECEIVED` to `ESTABLISHED`.
* **Zero Overhead Penalty**: In standard TCP implementations, the client is allowed to piggyback application payload data directly inside the final ACK segment, making the connection setup optimal and efficient.

### Q2: How are Sequence Numbers (SEQ) and Acknowledgment Numbers (ACK) calculated and updated during TCP data transfer?

**Answer:**

In **Transmission Control Protocol (TCP)**, reliability, stream ordering, and packet loss recovery depend on two 32-bit fields in the TCP header: the **Sequence Number (SEQ)** and the **Acknowledgment Number (ACK)**.

Unlike packet-oriented protocols, TCP treats data as an unstructured **byte stream**. Sequence and Acknowledgment numbers do not count packets; **they count bytes**.

---

### 1. Core Definitions and Calculation Rules

#### A. Sequence Number (SEQ) Calculation
The Sequence Number identifies the **byte position of the first data byte** carried within the payload of the current TCP segment.

* **During Connection Setup (SYN / SYN-ACK)**:
  * The initial `SEQ` is a randomly generated 32-bit value called the **Initial Sequence Number (ISN)**.
  * **Rule**: Control flags (`SYN` and `FIN`) consume **1 byte** of sequence space, even if no payload data is attached.
  * *Formula*: $\text{Next SEQ} = \text{Current SEQ} + 1$ (for `SYN`/`FIN` segments).

* **During Active Data Transfer**:
  * *Formula*: $\text{Next SEQ} = \text{Current SEQ} + \text{Payload Length (in Bytes)}$
  * Note: IP and TCP header lengths are excluded; only application-layer bytes are counted.

#### B. Acknowledgment Number (ACK) Calculation
The Acknowledgment Number is sent by the receiving peer to confirm received bytes. TCP uses a **cumulative acknowledgment scheme**.

* **Definition**: The ACK number specifies the **next expected sequence number** that the receiver is waiting to receive.
* *Formula*: $\text{ACK} = \text{Received SEQ} + \text{Received Payload Length (in Bytes)}$
* **Meaning**: Sending `ACK = N` informs the sender that all bytes up to `N - 1` have been successfully received and placed into the receive buffer.

---

### 2. Step-by-Step Data Transfer Execution Trace

The following breakdown illustrates how SEQ and ACK numbers update dynamically across a TCP session between a **Client** and a **Server**.

#### Assumptions
* Client Initial Sequence Number: $ISN_C = 1000$
* Server Initial Sequence Number: $ISN_S = 5000$

| Phase | Direction | Segment Type / Payload | SEQ Number | ACK Number | Explanation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Handshake** | Client ➔ Server | `SYN` (0 bytes) | `1000` | `0` | Client sets $ISN_C = 1000$. `SYN` consumes 1 sequence byte. |
| **2. Handshake** | Server ➔ Client | `SYN-ACK` (0 bytes) | `5000` | `1001` | Server sets $ISN_S = 5000$, acknowledges byte `1000` by requesting byte `1001`. |
| **3. Handshake** | Client ➔ Server | `ACK` (0 bytes) | `1001` | `5001` | Client acknowledges $ISN_S$ (`5000`), requesting byte `5001`. Connection is `ESTABLISHED`. |
| **4. Data Transfer** | Client ➔ Server | Data Payload (100 bytes) | `1001` | `5001` | Carries bytes `1001` through `1100`. |
| **5. Data ACK** | Server ➔ Client | `ACK` (0 bytes) | `5001` | `1101` | Server confirms receipt up to byte `1100` by requesting next byte `1101`. |
| **6. Data Transfer** | Server ➔ Client | Data Payload (200 bytes) | `5001` | `1101` | Server sends bytes `5001` through `5200`. |
| **7. Data ACK** | Client ➔ Server | `ACK` (0 bytes) | `1101` | `5201` | Client confirms receipt up to byte `5200` by requesting next byte `5201`. |

---

### 3. Special Scenarios in Sequence Updates

#### A. Piggybacking ACKs
TCP nodes rarely send standalone ACK segments if bidirectional data is flowing. Instead, a host attaches its pending `ACK` number to its outgoing data segments (**piggybacked acknowledgment**).

#### B. Out-of-Order Delivery and Duplicate ACKs
Because TCP uses cumulative acknowledgments, receiving out-of-order segments triggers immediate **Duplicate ACKs**:

* If a receiver gets bytes `1001–1100`, but segment `1101–1200` is dropped on the wire, and segment `1201–1300` arrives next:
* The receiver **cannot** acknowledge byte `1301`. It must re-send `ACK = 1101` (Duplicate ACK) to inform the sender that byte `1101` is missing.

#### C. Zero-Window Probe
When a receiver advertises `Window Size = 0`, the sender periodically transmits 1-byte **Zero-Window Probes**. The SEQ number increments by `1` for each probe segment to keep the connection alive without overflowing the receiver's filled buffer.

---

### 4. Summary Formulas

* **Outgoing Sequence Number**: $\text{SEQ}_{\text{out}} = \text{SEQ}_{\text{previous}} + \text{Bytes}_{\text{sent}}$
* **Outgoing Acknowledgment Number**: $\text{ACK}_{\text{out}} = \text{SEQ}_{\text{received}} + \text{Bytes}_{\text{received}}$
* **SYN / FIN Exception**: Consumes **1 virtual byte** in the sequence index ($+1$).
* **Standard Pure ACKs**: Consume **0 bytes** of sequence space; the SEQ number remains unchanged for subsequent transmissions.

### Q3: In a TCP segment header, does the Window Size field indicate the sender's current sending capacity or the sender's current receiving capacity?

**Answer:**

In a **Transmission Control Protocol (TCP)** segment header, the **Window Size** field (16 bits) explicitly indicates the **sender's current RECEIVING capacity**, NOT its sending capacity.

It is a mechanism used to implement **Layer 4 Flow Control**, preventing a fast sender from overwhelming a slow receiver's internal processing buffers.

---

### 1. Core Concept: Receiver-Side Flow Control

Because TCP communication is full-duplex, every TCP segment acts as both a data container and a feedback mechanism for reverse-path traffic.

* **Owner of the Window Size Value**: The node that generates and transmits the TCP segment header.
* **Meaning of the Field**: "This is how many bytes of unacknowledged payload data **I (the sender of this segment)** am currently prepared to receive into my local RX buffer."
* **Impact on the Peer**: The remote node reading this field must limit its own outgoing transmission rate so that its total in-flight (unacknowledged) data does not exceed this advertised limit.

---

### 2. Dynamic Update Mechanism During Data Exchange

The advertised Window Size changes dynamically based on how quickly the local application reads data out of the TCP receive socket buffer:

| Event / Action | Receive Buffer State | Advertised Window Size | Action Taken by Remote Peer |
| :--- | :--- | :--- | :--- |
| **Normal Processing** | Application reads data at wire speed; buffer stays empty. | **Large Window** (e.g., `64 KB`) | Peer transmits data segments at maximum speed. |
| **Buffer Filling Up** | Application is slow; incoming data accumulates in RX buffer. | **Shrinking Window** (e.g., drops to `8 KB`) | Peer throttles its transmission rate to match the smaller window. |
| **Buffer Full** | RX buffer reaches 100% capacity; no space left. | **Zero Window** (`0 Bytes`) | Peer completely pauses data transmission and starts periodic **Zero Window Probes**. |
| **Buffer Drained** | Application processes buffered data; space frees up. | **Window Update** (e.g., re-opens to `32 KB`) | Peer resumes transmitting data segments up to the new limit. |

---

### 3. Window Scaling Option (RFC 7323)

Standard TCP header fields allocate 16 bits for the Window Size, capping the maximum advertised receive buffer at $2^{16} - 1 = 65,535\text{ bytes}$ ($64\text{ KB}$).

In high-throughput Automotive Ethernet systems (e.g., 1000BASE-T1 camera streams or ADAS raw data logging):
* Both nodes negotiate the **TCP Window Scale Option** during the initial 3-way handshake (`SYN` / `SYN-ACK`).
* A left-shift multiplier (up to 14 bits) is applied to the advertised Window Size field.
* This allows nodes to advertise receive buffers up to **1 Gigabyte**, ensuring maximum throughput over high-bandwidth, high-latency internal networks.

---

### 4. Summary

* **Direct Answer**: The Window Size field indicates the **sender's RECEIVING capacity** (available local RX buffer space).
* **Purpose**: It advertises how much data the local host can accept from the remote peer, enforcing **flow control** across the TCP link.
* **Direction**: It tells the *receiving peer* how much data it is allowed to *send*.

### Q4: Given that TCP requires a connection-oriented handshake, is it possible to use TCP for broadcast or multicast transmission?

**Answer:**

In IP networking and Automotive Ethernet, **TCP (Transmission Control Protocol)** is architecturally incapable of performing **broadcast** or **multicast** transmissions. 

TCP is strictly restricted to **unicast (1-to-1)** communication pairs due to its connection-oriented state machine, byte-stream tracking mechanisms, and point-to-point flow control models.

---

### 1. Architectural Barriers Preventing TCP Multicast/Broadcast

#### A. Point-to-Point Connection State Machine
* **Connection-Oriented Requirement**: TCP requires an explicit **Three-Way Handshake** (`SYN` -> `SYN-ACK` -> `ACK`) to establish a Transmission Control Block (TCB) between exactly **two socket endpoints** (defined by `Source IP`, `Source Port`, `Destination IP`, `Destination Port`).
* **Multicast Impossibility**: A multicast IP address (e.g., `224.0.0.1` or `239.255.255.250`) represents a group of dynamic receivers, not a single physical endpoint. A host cannot initiate a 3-way handshake with an arbitrary or floating group of nodes.

#### B. Sequence Numbering & Acknowledgment Tracking
* **Byte-Stream Synchronization**: TCP uses **Sequence Numbers (SEQ)** and **Acknowledgment Numbers (ACK)** to track byte delivery, detect missing packets, and retransmit dropped segments.
* **ACK Storms & State Ambiguity**: If a sender transmitted a single TCP segment to a multicast group of 20 ECUs, it would expect 20 distinct `ACK` responses carrying different sequence states. Tracking multiple divergent sequence numbers and acknowledgment states inside a single TCP socket state machine is algorithmically impossible.

#### C. Dynamic Flow Control and Congestion Control
* **Sliding Window Mechanics**: TCP uses the **Window Size** field advertised by the receiver to adjust its transmission window based on available receive buffer space.
* **Congestion Avoidance**: TCP dynamically calculates Round-Trip Time (RTT) and adjusts its Congestion Window (`cwnd`) based on packet loss. In a 1-to-many scenario, different ECUs experience different buffer availability and network latency. A single sender cannot simultaneously maintain different congestion windows for multiple receivers on the same socket stream.

---

### 2. Structural Comparison: TCP Unicast vs. UDP Multicast

| Protocol Characteristic | TCP (Strictly Unicast 1-to-1) | UDP (Multicast / Broadcast 1-to-N) |
| :--- | :--- | :--- |
| **Addressing Support** | Unicast IP addresses only. | Unicast, Broadcast, and Multicast IP ranges. |
| **Connection State** | Connection-oriented (Requires 3-way handshake). | Connectionless (No handshake, no connection state). |
| **Data Delivery Model** | Guaranteed, ordered byte-stream. | Best-effort, message-oriented datagrams. |
| **State Overhead** | High (Tracks SEQ, ACK, RTT, Window size per peer). | Minimal (No per-receiver state tracking). |
| **Retransmission Model** | Automatic retransmission (ARQ) for dropped frames. | No Layer 4 retransmission (handled at L7 if needed). |

---

### 3. How Automotive Systems Achieve Reliable Multicast

Because TCP cannot handle multicast, Automotive Ethernet middleware (such as **SOME/IP** and **DDS**) uses alternative architectural approaches when reliable one-to-many transmission is required:

* **UDP Multicast + Application-Layer Reliability**:
  * Broadcast or multicast frames (e.g., SOME/IP Event notifications or AVTP audio/video streams) are transmitted over **UDP**.
  * If reliability or ordering is needed, an application-layer protocol (e.g., **SOME/IP-TP** or **Reliable DDS**) handles sequence indexing and loss recovery above the UDP layer.

* **Replicated TCP Unicast Streams**:
  * If absolute L4 reliability and point-to-point delivery are non-negotiable, the sender opens $N$ independent **TCP unicast socket connections**, transmitting $N$ separate streams to each receiver individually.

---

### 4. Summary

* **Direct Answer**: **No**, TCP cannot be used for broadcast or multicast transmission.
* **Root Cause**: TCP's core mechanisms—including its 3-way handshake, sequence/ACK byte tracking, sliding window flow control, and congestion management—are explicitly designed to operate between exactly **two stateful endpoints**.
* **Automotive Solution**: One-to-many communication in Software-Defined Vehicles is handled via **UDP Multicast**, with optional reliability mechanisms implemented at the middleware layer (e.g., SOME/IP).