
# Physical-Layer

## My Understanding
### Physical Layer Highlights (100BASE-T1)

* **Protocol Origin**: 
  Open Alliance BroadR-Reach (OABR) is the foundational technology for Automotive Ethernet, originally developed by Broadcom. It was later standardized by IEEE as **IEEE 100BASE-T1**.

* **Signal Transmission & Echo Cancellation**:
  * IEEE 100BASE-T1 operates over a single Unshielded Twisted Pair (UTP) cable.
  * To achieve full-duplex communication over a single pair, both nodes send and receive data simultaneously on the same frequency band.
  * **Echo Cancellation**: The receiver subtracts its own transmitted signal voltage from the total voltage on the bus to isolate and decode the pure incoming signal from the sender.
  * **Encoding Scheme**: A combined encoding pipeline of **4B3B, 3B2T, and PAM-3** (Pulse Amplitude Modulation 3-level) is used to translate the bitstream into differential voltage signals.

* **Topologies & Coupling Elements**:
  * IEEE 100BASE-T1 naturally supports point-to-point communication.
  * To enable multi-node communication across a network, active coupling elements such as **Switches** are used to forward frames between different branches.

* **Performance & Duplex Mode**:
  * Supports true **full-duplex** communication (simultaneous bidirectional data transfer).
  * Provides a fixed data rate of **100 Mbps**.

* **Clock Synchronization (Master / Slave)**：
  * To ensure precise signal modulation and cancellation, the PHY clocks of both endpoints must be synchronized.
  * One PHY must be configured as **Master** and the other as **Slave**. The Master PHY generates the continuous clock/synchronization stream, to which the Slave PHY aligns itself.
  * The Master/Slave role is typically configured via the microcontroller's Basic Software (BSW) or PHY register settings.

### Comparison of Ethernet Physical Layer Standards (100BASE-T1 vs 100BASE-TX vs 1000BASE-T)

| Feature / Metric | IEEE 100BASE-T1 | IEEE 100BASE-TX | IEEE 1000BASE-T |
| :--- | :--- | :--- | :--- |
| **Standardization Body / Origin** | IEEE 802.3bw (Based on OPEN Alliance OABR) | IEEE 802.3u (Based on FDDI TP-PMD) | IEEE 802.3ab |
| **Primary Domain / Target Application** | Automotive Ethernet | Traditional IT / Industrial Ethernet | Enterprise / Consumer LAN & Data Centers |
| **Encoding / Decoding** | 4B3B + 3B2T + PAM-3 | 4B5B + NRZI + MLT-3 | 8B1Q4 + Trellis / Viterbi + PAM-5 |
| **Physical Medium** | 1 Unshielded Twisted Pair (2 wires) | 2 Twisted Pairs (4 wires: Cat5 or higher) | 4 Twisted Pairs (8 wires: Cat5e or higher) |
| **Speed & Duplex Mode** | 100 Mbps (Full-Duplex) | 100 Mbps (Half/Full-Duplex via 2 pairs) | 1000 Mbps (Full-Duplex) |
| **Key DSP / Physical Layer Mechanism** | Echo Cancellation & Hybrid circuits | Auto-Negotiation (Fast Link Pulse) | Multi-pair Echo Cancellation & NEXT/FEXT Cancellation |
| **Clock Synchronization (Master/Slave)** | **Required** (Roles configured via BSW/register) | **Not Required** (Asynchronous point-to-point) | **Required** (Roles dynamically negotiated during Auto-Negotiation) |

## Questions

## References

- Vector Introduction to Automotive Ethernet
https://certification.vector.com/mod/page/view.php?id=149#maincontent

