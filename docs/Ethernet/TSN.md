# Ethernet AVB/TSN Architecture in Automotive Networks

## My Understanding
### 1. Technological Evolution & Protocol Adaptation

In 2012, IEEE officially transitioned the **Audio Video Bridging (AVB)** Working Group into the **Time-Sensitive Networking (TSN)** Working Group, expanding its standard suite to support deterministic, ultra-low-latency Ethernet communication.

In automotive E/E architectures, AVB/TSN primarily handles high-bandwidth streaming data, such as raw or compressed video feeds from ADAS cameras. Key adaptation strategies include:

* **Layer-2 Direct Transport**: Because automotive streams operate within localized in-vehicle network domains, network-layer routing is unnecessary. Protocol overhead is minimized by bypassing IP, TCP, and UDP, allowing AVB/TSN frames to run directly over Layer 2 (Ethernet Data Link Layer).
* **Static Configuration over Dynamic Reservation**: Although standard IEEE TSN supports dynamic resource negotiation via the **Stream Reservation Protocol (SRP)**, automotive implementations bypass SRP. Instead, network paths and bandwidth allocations are statically pre-configured at build time to ensure sub-second ECU boot times and deterministic startup behavior.

---

### 2. Network Topology & Entity Roles

Automotive AVB/TSN networks classify participating nodes into three functional entities:

* **Talker (Data Source)**
  * Generates time-critical stream payloads (e.g., surround-view camera modules).
* **Bridge (TSN Switch)**
  * Connects network nodes and handles frame propagation.
  * Must natively support TSN mechanisms, including special MAC Multicast routing, stream queuing, and dynamic PTP timestamp updates.
* **Listener (Data Sink)**
  * Consumes and processes stream data (e.g., domain controllers or IVI displays).

---

### 3. Streaming Data Transport (IEEE 1722 / AVTP)

Data transport is managed by the **IEEE 1722 Audio Video Transport Protocol (AVTP)**:

* **Payload & QoS**: AVTP encapsulates audio, video, and time-critical control frames within its payload. Frames utilize IEEE 802.1Q VLAN tags, enabling priority queuing across switches to guarantee end-to-end latency below **2 ms** while minimizing latency jitter.
* **Synchronized Playout (Presentation Time)**: Each AVTP header contains a normalized **Presentation Time**—a future timestamp indicating the exact moment when the payload must be delivered to the local application layer (e.g., rendering a video frame or outputting audio).

---

### 4. Time Synchronization Infrastructure (gPTP)

To ensure that the Presentation Time is executed simultaneously across distributed endpoints, all network nodes must maintain sub-microsecond clock alignment. 

This synchronization is governed by **Generalized Precision Time Protocol (gPTP / IEEE 802.1AS)**, a profile of IEEE 1588 (PTP) tailored for automotive Ethernet topologies. gPTP compensates for propagation delays across bridges to provide a unified global time base.