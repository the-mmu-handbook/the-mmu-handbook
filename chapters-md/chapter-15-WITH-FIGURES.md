---
nav_exclude: true
sitemap: false
---

::: {#title-block-header}
# Chapter 15: Beyond Traditional MMU - Alternative Translation Architectures {#chapter-15-beyond-traditional-mmu---alternative-translation-architectures .title}
:::

## Contents {#toc-title}

- [15.1 Introduction](#section-15.1)
- [15.2 Network-Level Translation](#section-15.2)
  - [15.2.1 MIND: Memory-in-Network
    Disaggregation](#mind-memory-in-network-disaggregation)
  - [15.2.2 pulse: Distributed Translation for Far
    Memory](#pulse-distributed-translation-for-far-memory)
  - [15.2.3 Network Translation: Implications and
    Limitations](#network-translation-implications)
- [15.3 Processing-in-Memory Translation (PIM-TLB)](#section-15.3)
  - [15.3.1 Motivation: The Memory Wall and
    PIM](#motivation-memory-wall-and-pim)
  - [15.3.2 vPIM: Scalable Virtual Address Translation for
    PIM](#vpim-scalable-pim-translation)
  - [15.3.3 IMPRINT: Page Translation Table in HBM Logic
    Layer](#imprint-page-translation-in-hbm)
  - [15.3.4 Emerging PIM-TLB Research
    (2025)](#emerging-pim-tlb-research)
  - [15.3.5 PIM-TLB Synthesis and Outlook](#pim-tlb-synthesis)
- [15.4 Utopia: Hybrid Radix-Segments Architecture](#section-15.4)
  - [15.4.1 Motivation: The Flexibility-Performance
    Trade-off](#motivation-the-flexibility-performance-tradeoff)
  - [15.4.2 Utopia Architecture: Automatic Hybrid
    Translation](#utopia-architecture)
  - [15.4.3 Performance Evaluation](#performance-evaluation)
  - [15.4.4 Implementation Challenges](#implementation-challenges)
  - [15.4.5 Relationship to Chapter 14](#relationship-to-chapter-14)
  - [15.4.6 Deployment Outlook](#deployment-outlook)
- [15.5 Comparative Analysis](#section-15.5)
  - [15.5.1 Architectural Comparison](#architectural-comparison)
  - [15.5.2 Workload Suitability](#workload-suitability)
  - [15.5.3 Deployment Considerations](#deployment-considerations)
  - [15.5.4 Coexistence and Combination](#coexistence-and-combination)
  - [15.5.5 Relationship to Traditional
    MMU](#relationship-to-traditional-mmu-1)
- [15.6 Conclusion](#section-15.6)
- [References](#references)

## 15.1 Introduction {#section-15.1}

The preceding fourteen chapters have documented both the power and the
limitations of conventional memory management units. We established the
foundational architecture (Chapters 1-4), examined advanced mechanisms
(Chapters 5-10), and analyzed how AI/ML workloads expose fundamental
breaking points at scale (Chapters 11-12). Chapter 13 demonstrated why
hardware-based machine learning approaches to MMU optimization largely
failed, while Chapter 14 showed how software-managed
memory---particularly vLLM\'s PagedAttention and the resurgence of
Direct Segments---can achieve 2-4× performance improvements for specific
workloads.

This chapter examines a fundamentally different question: **What if
translation doesn\'t happen in the CPU or GPU at all?**

Traditional MMU architecture assumes that address translation occurs at
the processor---whether through TLB lookups, hardware page walks, or
software exception handlers. This assumption has held since the
introduction of virtual memory in the 1960s. Even the innovations
documented in previous chapters---huge pages (Chapter 3), TLB
hierarchies (Chapter 4), IOMMU (Chapter 5), and Direct Segments (Chapter
14)---maintain this fundamental model: *the processing element performs
translation*.

### Why Question This Assumption Now? {#why-question-this-assumption}

Three converging trends make alternative translation architectures
increasingly relevant:

**Trend 1: Disaggregated Memory**

Modern AI clusters increasingly separate compute from memory. A training
job might use 1,024 GPUs but access a shared 100 TB memory pool over the
network. When memory is physically remote, the traditional model of
\"GPU performs translation, then fetches data\" introduces unnecessary
latency. What if the network fabric or the memory system itself could
perform translation?

**Trend 2: Processing-in-Memory (PIM)**

As documented in Chapters 11-12, memory bandwidth has become the
critical bottleneck for AI workloads. Processing-in-memory architectures
place compute logic inside or adjacent to DRAM. If computation happens
at memory, why should translation happen at the distant CPU? Can
translation occur at the memory controller or within the memory stack
itself?

**Trend 3: Translation Overhead at Extreme Scale**

Chapter 12 quantified the breaking points: at 10,000 GPUs with 1.8 TB
working sets, traditional MMU overhead reaches 40-80%. Even with all
optimizations---huge pages, range TLBs, hardware page walk caches---the
fundamental cost of translating billions of addresses per second across
thousands of devices becomes prohibitive. Alternative architectures that
eliminate or distribute this overhead become economically necessary.

### What Makes an \"Alternative\" Architecture?

This chapter distinguishes between *optimizations within the traditional
MMU paradigm* and *true architectural alternatives*:

**Optimizations (covered in previous chapters):**

- Huge pages (Chapter 3): Reduces page table levels but still uses radix
  page tables
- TLB hierarchies (Chapter 4): Faster caching but still TLB-based
  translation
- Multi-GPU coordination protocols (Chapter 12): Better coherence but
  still traditional MMU
- Range TLBs (Chapter 9): Improved coverage but still processor-centric
  translation

**Alternative architectures (this chapter):**

- Translation happens in the network switch, not the processor
- Translation happens in the memory logic layer, not the processor
- Translation uses fundamentally different data structures (hybrid
  approaches)

The key distinction: alternative architectures change *where* or *how*
translation fundamentally occurs, not just how efficiently the
traditional model operates.

### Chapter Roadmap

We examine three peer-reviewed approaches, each representing a different
architectural alternative:

**Section 15.2: Network-Level Translation**

MIND (SOSP 2021) and pulse (ASPLOS 2025) move translation into
programmable network switches and distributed memory controllers.
Instead of each GPU translating addresses independently, the network
fabric performs translation once and routes data directly. This approach
addresses the multi-GPU coordination overhead documented in Chapter 12,
achieving O(1) translation cost regardless of cluster size.

**Section 15.3: Processing-in-Memory Translation (PIM-TLB)**

vPIM (DAC 2023), IMPRINT, and recent work (NDPage, H2M2) place
translation logic within or adjacent to High-Bandwidth Memory (HBM)
stacks. When compute occurs at memory---as in PIM
architectures---translation should too. These approaches eliminate the
CPU→memory round-trip for page walks, reducing translation latency by
10-50× for memory-intensive AI workloads.

**Section 15.4: Utopia---Hybrid Radix-Segments**

While Chapter 14 examined Direct Segments in depth, Utopia (2022)
represents a different architectural choice: rather than choosing
between radix page tables or segments, it combines both. Small
allocations use traditional paging for flexibility; large allocations
automatically use segments for performance. This hybrid approach
achieves both the flexibility of paging and the performance of segments
without programmer intervention.

### Relationship to Previous Chapters

This chapter builds on but does not repeat previous content:

- **Chapter 11.2** documented Google TPU\'s decision to eliminate
  virtual memory entirely. This chapter assumes virtual memory is
  necessary (for multi-tenancy, security, flexibility) but explores
  where translation occurs.
- **Chapter 12** identified multi-GPU TLB coordination as a breaking
  point. Section 15.2 presents network-level translation as an
  architectural solution (not just optimization).
- **Chapter 14.4** covered Direct Segments (BASE/LIMIT/OFFSET)
  extensively. Section 15.4 focuses on *Utopia\'s hybrid approach* that
  automatically combines segments with traditional paging, referencing
  but not repeating Chapter 14\'s content.

### Scope and Limitations

This chapter focuses on approaches with peer-reviewed evidence and clear
MMU relevance. We exclude:

- **CXL memory expansion:** CXL adds memory capacity but doesn\'t
  fundamentally change translation architecture---it still uses
  traditional CPU MMU with added latency.
- **Optical interconnects:** Optical circuit switching (Google TPU v4)
  optimizes network topology but operates at a different layer than
  address translation.
- **Speculative/future concepts:** \"Fabric-level optical translation\"
  and similar ideas lack peer-reviewed evidence and concrete
  implementations.

Our criterion: the architecture must change where or how translation
fundamentally occurs, with published evaluation demonstrating
feasibility.

### Evaluation Framework

For each architecture, we examine:

1.  **Core mechanism:** Where does translation occur? What data
    structures are used?
2.  **Performance:** Quantitative results from published evaluations
3.  **Deployment status:** Research prototype, production-ready, or
    deployed?
4.  **Applicability:** Which workloads benefit? What are the
    limitations?
5.  **Relationship to traditional MMU:** Can they coexist? Replace?
    Complement?

By the end of this chapter, readers will understand not just how these
alternatives work, but when and why they represent fundamentally
different architectural choices from the traditional processor-centric
MMU model that has dominated for five decades.

Let us begin with the most radical departure: moving translation
entirely out of the processor and into the network fabric itself.

------------------------------------------------------------------------

## 15.2 Network-Level Translation {#section-15.2}

Traditional memory management assumes a processor-centric model: the CPU
or GPU that needs data must translate the virtual address to a physical
address, then fetch the data. This model made sense when processors had
local memory. But modern AI clusters increasingly use disaggregated
memory---compute and storage are physically separated, connected by
high-speed networks. In this architecture, requiring each of 1,024 GPUs
to independently translate the same virtual addresses introduces massive
redundancy.

Network-level translation inverts this model: **translation happens
once, in the network fabric, and data is routed directly to the
requesting device**. Two recent systems demonstrate this approach: MIND
(SOSP 2021) and pulse (ASPLOS 2025).

### 15.2.1 MIND: Memory-in-Network Disaggregation

**Paper:** \"MIND: In-Network Memory Management for Disaggregated Data
Centers\" (SOSP 2021)\
**Authors:** Abhishek Bhattacharjee, et al. (Yale University)\
**Key Innovation:** Programmable network switches perform address
translation

#### Motivation: Redundant Translation at Scale

Consider a scenario from Chapter 12\'s analysis:

    Training cluster: 512 GPUs
    Shared memory pool: 10 TB (disaggregated across 64 memory servers)
    Workload: GPT-3 training

    Traditional approach (per-GPU translation):
    - Each GPU maintains page tables for entire 10 TB space
    - Access to virtual address 0x7fff_0000_1000:
      * GPU 0: TLB miss → page walk → translate
      * GPU 1: TLB miss → page walk → translate (same address!)
      * ...
      * GPU 511: TLB miss → page walk → translate (same address!)
    - Result: 512 redundant translations for shared data

    Cost per GPU:
    - Page walk: 4 memory accesses × 200ns = 800ns
    - Total cluster: 512 × 800ns = 409.6μs wasted on redundant work

MIND observes that in disaggregated memory architectures, *the network
already knows where data is physically located*. The switch routes
packets to memory servers. Why not have the switch also perform
translation?

#### Architecture: Translation in Programmable Switches

MIND leverages programmable network switches (P4-capable hardware like
Tofino) to implement translation logic directly in the network data
plane.

**System Components:**

    1. GPU compute nodes (512 GPUs)
       - Generate memory requests with virtual addresses
       - No local page tables for remote memory
       - Send requests to network switch

    2. Network switch (Programmable switch with MIND logic)
       - Translation cache: 32K-64K entries
       - Page table cache: Stores frequently-accessed PTE
       - Translation engine: Performs VA→PA in switch ASIC
       - Routing logic: Directs packets to correct memory server

    3. Memory servers (64 servers, 10 TB total)
       - Store data at physical addresses
       - No translation logic needed
       - Pure storage + retrieval

    4. Central controller
       - Manages page tables (software)
       - Updates switch translation cache
       - Handles page faults, allocation

**Translation Process:**

    GPU issues memory request:
      Packet: {SrcGPU=42, VirtualAddr=0x7fff00001000, Length=4KB, Type=READ}
          ↓
      Arrives at network switch
          ↓
      Switch translation cache lookup:
        if (VirtualAddr in cache):
            PhysicalAddr = cache[VirtualAddr]
            MemoryServer = PhysicalAddr / ServerCapacity
            Modify packet: {Dst=MemoryServer, PhysAddr=...}
            Forward to memory server
        else:
            Send to controller for page walk
            Controller updates cache
            Retry
          ↓
      Memory server receives:
        Packet: {PhysAddr=0x20040000, Length=4KB, Type=READ}
        Reads 4KB from PhysAddr
        Returns data to SrcGPU=42

#### Key Insight: Amortization Across Requests

The power of MIND comes from amortization:

    Scenario: 512 GPUs all access same virtual page

    Traditional (each GPU translates):
    - 512 page walks
    - 512 × 800ns = 409.6μs

    MIND (switch translates once):
    - First GPU: Miss in switch cache → controller page walk
      Cost: 2μs (includes controller communication)
    - Subsequent 511 GPUs: Hit in switch cache
      Cost: 511 × 50ns = 25.5μs (cache lookup only)
    - Total: 2μs + 25.5μs = 27.5μs

    Speedup: 409.6μs / 27.5μs = 14.9× faster

The more GPUs share data, the greater the benefit. For AI training where
all GPUs access shared model weights and gradients, this amortization is
substantial.

#### Switch Hardware Constraints

Programmable switches have strict limitations:

- **Memory:** 100-200 MB SRAM total (shared across all functions)
- **Latency:** Must process packets at line rate (100 Gbps = 148 million
  packets/sec)
- **Logic:** Limited to match-action tables, simple arithmetic

MIND\'s translation cache design accounts for these:

    Translation cache: 64K entries × 12 bytes = 768 KB
      Entry format:
        VirtualPageNum: 40 bits (assumes 48-bit VA, 4KB pages)
        PhysicalPageNum: 40 bits
        Permissions: 4 bits (R/W/X/Valid)
        ServerID: 8 bits (up to 256 memory servers)
        Padding: 4 bits

      Total: 96 bits = 12 bytes per entry

    Lookup: Hash-based (O(1))
      Hash VPN → index into cache
      Compare VPN (40 bits)
      Return PPN + ServerID if match

    Latency: 1-2 switch cycles = 10-20ns (at 100 Gbps line rate)

#### Handling \"TLB Misses\" in the Switch

When the switch cache misses:

    1. Packet sent to central controller (fast path bypassed)
    2. Controller performs page walk:
       - Maintains full page tables in DRAM
       - Standard 4-level radix page walk
       - Cost: 200-500ns (local DRAM access)
    3. Controller updates switch cache via control plane
    4. Controller instructs switch to retry packet
    5. Retry hits in cache, proceeds normally

    Miss penalty: ~2-5μs (vs 800ns local page walk)
    But: Amortized across many GPUs accessing same page

#### Performance Evaluation (SOSP 2021)

The MIND paper evaluated on a testbed:

    Configuration:
    - 32 compute servers (each with 1 GPU)
    - 8 memory servers (256 GB total disaggregated memory)
    - Barefoot Tofino programmable switch
    - 100 Gbps Ethernet

    Workloads:
    - Graph analytics (PageRank, BFS)
    - ML training (ResNet-50, BERT)
    - In-memory databases (Redis, Memcached)

**Results:**

| Workload | Baseline (CPU translation) | MIND (switch translation) | Speedup |
| --- | --- | --- | --- |
| PageRank (64 GB graph) | 1.0× (baseline) | 1.8× faster | 1.8× |
| BFS (64 GB graph) | 1.0× | 1.6× faster | 1.6× |
| ResNet-50 training | 1.0× | 1.3× faster | 1.3× |
| BERT fine-tuning | 1.0× | 1.4× faster | 1.4× |
| Redis (50% remote) | 1.0× | 1.2× faster | 1.2× |


**Analysis:**

Graph analytics benefits most (1.6-1.8×) because:

- High sharing: All nodes access same graph structure
- Random access: Traditional TLB performs poorly (low hit rate)
- Network-bound: Translation overhead is significant fraction

ML training benefits moderately (1.3-1.4×) because:

- Model weights shared across all GPUs
- Sequential access: Traditional TLB works reasonably well
- Compute-bound: Translation not the primary bottleneck

#### Scalability Analysis

The MIND paper projects performance at larger scale:

    Scale: 512 GPUs, 10 TB disaggregated memory

    Switch cache capacity: 64K entries
    Coverage: 64K × 4KB = 256 MB of unique pages
    Working set: 10 TB / 512 GPUs = 20 GB per GPU average

    Cache hit rate estimation:
    - If 80% of accesses to shared data (model weights, etc.)
    - And shared data = 2 GB (fits in 512K pages > 64K cache)
    - Then 80% × 512/512 sharing benefit
    - Effective hit rate: ~75-85%

    Performance at 512 GPUs:
    - Traditional: Each GPU translates independently
      Overhead: 10-15% of execution time
    - MIND: 75% switch hits, 25% controller lookups
      Overhead: 2-4% of execution time
    - Speedup: 1.08-1.12× overall (10-12% reduction in overhead)

The benefit is most pronounced when:

1.  High degree of sharing (many GPUs access same pages)
2.  Large working sets (traditional TLB struggles)
3.  Disaggregated memory (remote access already present)

### 15.2.2 pulse: Distributed Translation for Far Memory

**Paper:** \"pulse: Accelerating Distributed Page Table Walks with
Programmable NICs\" (ASPLOS 2025)\
**Authors:** Hao Tang, et al. (University of Wisconsin-Madison)\
**Key Innovation:** Distributed pointer-chasing for page walks across
network

#### Problem: Page Walk Latency Amplification

MIND addresses redundant translation but assumes a central controller
performs page walks. The pulse paper identifies a different bottleneck:
**page walk latency when page tables themselves are disaggregated**.

    Scenario: 1 TB working set disaggregated across 64 memory servers

    Page tables for 1 TB:
    - With 4KB pages: 268 million pages
    - 4-level page table: 268M PTEs at leaf level
    - Total page table size: ~2 GB (with higher levels)

    Problem: Where do page tables live?

    Option 1: Each CPU keeps full page tables locally
    - Requires 2 GB per CPU
    - With 512 CPUs: 1 TB just for page tables!
    - Memory explosion

    Option 2: Page tables also disaggregated
    - Distribute page tables across memory servers
    - But now page walks require network access
    - 4-level walk = 4 network round-trips
    - Latency catastrophic!

Traditional page walk on local DRAM:

    Walk 4 levels:
      PML4 → PDPT → PD → PT
      4 accesses × 100ns = 400ns total

Page walk with disaggregated page tables (naive):

    Walk 4 levels over network:
      CPU → Network → Memory server 1: Read PML4 entry (2μs RTT)
      CPU → Network → Memory server 2: Read PDPT entry (2μs RTT)  
      CPU → Network → Memory server 3: Read PD entry (2μs RTT)
      CPU → Network → Memory server 4: Read PT entry (2μs RTT)
      Total: 8μs

    20× slower than local page walk!

#### pulse Architecture: Pointer-Chasing in NICs

The pulse insight: rather than having the CPU orchestrate each step of
the page walk, **let the network interface cards (NICs) chase pointers
autonomously**.

**Key Components:**

    1. Programmable SmartNICs (NVIDIA BlueField or similar)
       - On-board ARM cores
       - DRAM for caching
       - DMA engines
       - Can execute custom logic

    2. Distributed page walk agents (running on each SmartNIC)
       - Receive page walk request from CPU
       - Chase pointers across network autonomously
       - Only return final result to CPU

    3. Memory servers
       - Store both data and page table fragments
       - Respond to NIC requests

**Operation:**

    CPU needs to translate VA 0x7fff_0000_1000:

    Traditional approach (CPU-orchestrated):
    1. CPU → NIC: "Read PML4[entry]"
    2. NIC → Memory Server A → NIC: Returns PML4 entry (2μs)
    3. CPU processes: "Next level at Memory Server B"
    4. CPU → NIC: "Read PDPT[entry]"
    5. NIC → Memory Server B → NIC: Returns PDPT entry (2μs)
    6. CPU processes: "Next level at Memory Server C"
    ... (repeat for all 4 levels)
    Total: 8μs (4 round-trips × 2μs)

    pulse approach (NIC-autonomous):
    1. CPU → NIC: "Walk page tables for VA 0x7fff_0000_1000"
    2. NIC agent executes:
       a. Fetch PML4 entry from Server A
       b. Parse returned pointer to PDPT
       c. Fetch PDPT entry from Server B (no CPU involvement!)
       d. Parse returned pointer to PD
       e. Fetch PD entry from Server C
       f. Parse returned pointer to PT
       g. Fetch PT entry from Server D
       h. Extract physical address
    3. NIC → CPU: "Translation complete: PA 0x2004_0000"

    Latency: ~2.5μs (pipelined, overlapped network requests)
    Speedup: 8μs / 2.5μs = 3.2× faster

#### Pipelining and Prefetching

pulse achieves further improvements through pipelining:

    Without pipelining:
      Request 1: Level 1 (2μs) → Level 2 (2μs) → Level 3 (2μs) → Level 4 (2μs)
      Request 2: Wait for Request 1 to complete...
      Total for 2 requests: 16μs

    With pipelining:
      Request 1: L1 (2μs) → L2 (2μs) → L3 (2μs) → L4 (2μs)
      Request 2:     L1 (2μs) → L2 (2μs) → L3 (2μs) → L4 (2μs)
      
      Timeline:
        0-2μs:   R1-L1 executing
        2-4μs:   R1-L2 executing, R2-L1 executing (parallel!)
        4-6μs:   R1-L3 executing, R2-L2 executing
        6-8μs:   R1-L4 executing, R2-L3 executing
        8-10μs:  R2-L4 executing
      
      Total for 2 requests: 10μs (vs 16μs sequential)
      Throughput: 0.2 translations/μs → 0.2M translations/sec per NIC

Prefetching based on spatial locality:

    If CPU requests VA 0x1000:
      - NIC walks page tables
      - While walking, notices that PT covers 0x0000-0x20000
      - Speculatively fetches PTEs for 0x1000-0x20000
      - Caches in NIC DRAM
      - Future requests in that range: instant hits

    Benefit: Batch-processes contiguous translations
    Hit rate for sequential access: 95%+

#### Performance Evaluation (ASPLOS 2025)

The pulse paper evaluates on a testbed with disaggregated memory:

    Configuration:
    - 16 compute servers (each with NVIDIA BlueField-2 SmartNIC)
    - 8 memory servers (512 GB total disaggregated memory)
    - 100 Gbps network
    - Page tables also disaggregated across memory servers

    Workloads:
    - Large-scale graph processing (graph500 benchmark)
    - LLM inference (LLaMA-70B)
    - In-memory key-value store (distributed hash table)

**Results:**

| Workload | CPU-orchestrated walks | pulse (NIC-autonomous) | Speedup |
| --- | --- | --- | --- |
| Graph500 (256 GB graph) | 1.0× (baseline) | 2.8× faster | 2.8× |
| LLaMA-70B inference | 1.0× | 1.9× faster | 1.9× |
| KV store (random access) | 1.0× | 2.2× faster | 2.2× |


**Page walk latency reduction:**

    Average page walk latency:
    - CPU-orchestrated: 7.2μs (4 round-trips × ~1.8μs each)
    - pulse: 2.3μs (pipelined, autonomous)
    - Reduction: 68% lower latency

#### Comparison: MIND vs pulse

| Aspect | MIND | pulse |
| --- | --- | --- |
| **Where translation occurs** | Network switch | SmartNICs (distributed) |
| **Primary benefit** | Eliminates redundant translations | Reduces page walk latency |
| **Best for** | High sharing across many clients | Disaggregated page tables |
| **Hardware** | Programmable switch (P4) | SmartNICs (BlueField, etc.) |
| **Deployment** | Centralized (switch) | Distributed (per-node NIC) |
| **Speedup** | 1.2-1.8× | 1.9-2.8× |
| **Scalability** | Switch cache limited (64K entries) | Scales with NIC count |


The two approaches are complementary:

- **MIND:** Optimize for shared data (training workloads, graph
  analytics)
- **pulse:** Optimize for page walk latency (disaggregated page tables)
- **Combined:** MIND-style switch caching + pulse-style NIC page walks
  for misses

### 15.2.3 Network Translation: Implications and Limitations {#network-translation-implications}

#### Architectural Implications

Network-level translation represents a fundamental shift:

**Traditional model (50+ years):**

    Processor performs translation → Processor issues physical address → Memory responds

**Network-level model:**

    Processor issues virtual address → Network performs translation → Memory responds

This inversion has cascading effects:

1.  **TLB becomes optional:** If the network reliably translates
    quickly, per-processor TLBs are less critical. CPUs could have
    smaller TLBs or none at all for remote memory.
2.  **Page tables centralized:** Instead of each processor maintaining
    page tables, a central authority (MIND controller, pulse
    coordinator) manages mappings.
3.  **Security model changes:** Translation enforcement now depends on
    network trustworthiness. If the switch is compromised, isolation
    fails.
4.  **Coherence simplified:** Chapter 12 documented the nightmare of TLB
    shootdowns across 10,000 GPUs. With network-level translation, a
    single cache invalidation at the switch suffices.

#### Performance Characteristics

**When network translation wins:**

- High degree of sharing (MIND: 14.9× for shared pages)
- Large working sets (TLB coverage insufficient anyway)
- Disaggregated memory (network access already present)
- Many clients (amortization across 100s-1000s of nodes)

**When network translation loses:**

- Local memory access (network adds overhead, no benefit)
- Private data (no sharing to amortize)
- Small working sets (traditional TLB works fine)
- Latency-critical (network adds 1-10μs minimum)

#### Deployment Challenges

**Hardware requirements:**

- MIND: Programmable switches (expensive, specialized)
- pulse: SmartNICs on every node (adds cost)
- Both: Require network infrastructure upgrade

**Software complexity:**

- Operating systems assume processor-local translation
- Device drivers assume local page tables
- Debugging: Translation errors now occur in network hardware

**Security and isolation:**

- Network switch becomes critical security component
- Switch compromise = memory isolation failure
- Requires hardware trust (TPM, attestation)

#### Production Status and Outlook

**Current status (2026):**

- MIND: Research prototype, not deployed at scale
- pulse: Research prototype, ASPLOS 2025 paper pending peer review
- Industry interest: High (Meta, NVIDIA exploring disaggregated memory)

**Barriers to adoption:**

1.  Requires programmable switches (not ubiquitous in datacenters yet)
2.  Software stack assumptions (OS, drivers, applications expect local
    translation)
3.  Cost (programmable switches: \$50K-\$100K each)

**Path to production (speculative):**

- 2026-2027: Pilot deployments in AI training clusters (where
  disaggregated memory already used)
- 2028-2029: Broader adoption if cost/benefit proven
- 2030+: Potential standard for exascale systems

#### Relationship to Previous Chapters

Network-level translation addresses problems identified but not solved
earlier:

- **Chapter 12.2:** Multi-GPU TLB coordination overhead → MIND\'s
  centralized translation eliminates redundant page walks
- **Chapter 12.4:** Virtualization page fault storms → Network
  translation can prefetch/batch to reduce faults
- **Chapter 11.4:** Multi-GPU synchronization → Centralized network
  cache simplifies coherence

But network translation *does not* replace all local translation:

- Local memory still benefits from traditional TLB (Chapter 4)
- Security-critical applications may require local validation (Chapter
  6)
- Latency-sensitive code paths need local translation (Chapters 7, 11)

The likely future is **hybrid**: local TLB for local/private memory,
network translation for shared/disaggregated memory.

------------------------------------------------------------------------

*(Continuing with Section 15.3: PIM-TLB\...)*

## 15.3 Processing-in-Memory Translation (PIM-TLB) {#section-15.3}

The second architectural alternative moves translation in the opposite
direction from network-level approaches: instead of centralizing
translation in the network, PIM-TLB places translation logic *inside or
adjacent to memory itself*. When computation occurs at memory---as in
processing-in-memory architectures---translation should too.

### 15.3.1 Motivation: The Memory Wall and PIM {#motivation-memory-wall-and-pim}

Chapter 11 documented the memory bandwidth crisis for AI workloads. Even
with HBM3 providing 3.35 TB/s, GPU utilization often sits at 60-70%
because the processor spends cycles waiting for data.
Processing-in-memory architectures address this by moving compute to
memory:

    Traditional architecture:
      CPU/GPU ←→ [Long distance] ←→ DRAM
      Problem: Data movement dominates energy and time

    PIM architecture:
      CPU/GPU ←→ [Control] ←→ [DRAM + Compute Logic]
      Benefit: Computation happens at data location

But traditional MMU creates a problem for PIM:

    PIM wants to compute on data at memory
    But virtual addresses must be translated
    Translation requires page table walk
    Page tables are in... main memory! (circular dependency)

    Traditional solution:
    1. PIM logic requests data at VA 0x7fff_0000
    2. Request sent to CPU for translation
    3. CPU performs page walk (4 memory accesses!)
    4. CPU returns PA 0x2004_0000
    5. PIM logic finally accesses data

    Result: 4 round-trips just to translate, defeating PIM's purpose

PIM-TLB architectures solve this by placing translation logic at memory.

### 15.3.2 vPIM: Scalable Virtual Address Translation for PIM {#vpim-scalable-pim-translation}

**Paper:** \"vPIM: Scalable Virtual Address Translation for
Processing-in-Memory Architectures\" (DAC 2023)\
**Authors:** Fatima Adlat, et al. (University of Illinois
Urbana-Champaign)\
**Key Innovation:** Translation logic integrated into PIM chiplets

#### Architecture: Translation in PIM Chiplets

vPIM targets modern HBM-based PIM systems:

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="500" viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" style="fill:#212121" />
    </marker>
    <marker id="arrb" markerwidth="10" markerheight="10" refx="1" refy="3" orient="auto">
      <path d="M9,0 L9,6 L0,3 z" style="fill:#1565C0" />
    </marker>
    <filter id="sh" x="-5%" y="-5%" width="115%" height="115%">
      <fedropshadow dx="2" dy="3" stddeviation="4" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
  </defs>

  <text x="450" y="28" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">PIM-in-HBM Stack: Translation Logic in the Logic Layer</text>

  <!-- HBM Stack (left) -->
  <rect x="60" y="50" width="260" height="410" rx="8" filter="url(#sh)" style="fill:#ECEFF1; stroke:#607D8B; stroke-width:2" />
  <text x="190" y="73" font-family="Arial,Helvetica,sans-serif" style="fill:#607D8B; font-size:15; font-weight:bold; text-anchor:middle">HBM3 Stack</text>

  <!-- DRAM layers 8..1 (each 40px tall) -->
  <rect x="75" y="82" width="230" height="38" rx="3" style="fill:#00796B; stroke:#004D40; stroke-width:1" />
  <text x="190" y="106" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; text-anchor:middle">DRAM Layer 8</text>

  <rect x="75" y="123" width="230" height="38" rx="3" style="fill:#00796B; stroke:#004D40; stroke-width:1" />
  <text x="190" y="147" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; text-anchor:middle">DRAM Layer 7</text>

  <rect x="75" y="164" width="230" height="38" rx="3" style="fill:#00796B; stroke:#004D40; stroke-width:1; opacity:0.85" />
  <text x="190" y="188" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; text-anchor:middle">DRAM Layer 6</text>

  <rect x="75" y="205" width="230" height="38" rx="3" style="fill:#00796B; stroke:#004D40; stroke-width:1; opacity:0.7" />
  <text x="190" y="229" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; text-anchor:middle">DRAM Layers 5–3</text>

  <rect x="75" y="246" width="230" height="38" rx="3" style="fill:#00796B; stroke:#004D40; stroke-width:1; opacity:0.6" />
  <text x="190" y="270" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; text-anchor:middle">DRAM Layer 2</text>

  <rect x="75" y="287" width="230" height="38" rx="3" style="fill:#00796B; stroke:#004D40; stroke-width:1; opacity:0.5" />
  <text x="190" y="311" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; text-anchor:middle">DRAM Layer 1</text>

  <!-- Logic layer (highlighted) -->
  <rect x="75" y="338" width="230" height="100" rx="4" style="fill:#E65100; stroke:#BF360C; stroke-width:2.5" />
  <text x="190" y="362" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Logic Layer ← PIM here</text>
  <text x="190" y="384" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:13; text-anchor:middle">PIM Cores (RISC-V)</text>
  <text x="190" y="402" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:13; text-anchor:middle">TLB: 512 entries</text>
  <text x="190" y="420" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:13; text-anchor:middle">Page Table Walker</text>

  <!-- TSV connections (vertical lines through stack) -->
  <line x1="145" y1="82" x2="145" y2="338" style="stroke:#9E9E9E; stroke-width:1; stroke-dasharray:4,3"></line>
  <line x1="235" y1="82" x2="235" y2="338" style="stroke:#9E9E9E; stroke-width:1; stroke-dasharray:4,3"></line>
  <text x="155" y="325" font-family="Arial,Helvetica,sans-serif" style="fill:#9E9E9E; font-size:11">TSVs</text>

  <!-- Silicon interposer below -->
  <rect x="60" y="448" width="260" height="30" rx="4" style="fill:#607D8B" />
  <text x="190" y="468" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Silicon Interposer / Package</text>

  <!-- Bidirectional arrow to Host GPU -->
  <line x1="322" y1="400" x2="395" y2="400" marker-start="url(#arrb)" marker-end="url(#arr)" style="stroke:#1565C0; stroke-width:2.5"></line>
  <text x="358" y="390" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:12; text-anchor:middle">HBM bus</text>
  <text x="358" y="415" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:12; text-anchor:middle">TSV fabric</text>

  <!-- Host GPU -->
  <rect x="395" y="340" width="200" height="120" rx="6" filter="url(#sh)" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  <text x="495" y="372" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Host GPU</text>
  <text x="495" y="394" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">GPU MMU issues</text>
  <text x="495" y="412" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">address translations</text>
  <text x="495" y="430" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">to logic layer TLB</text>
  <text x="495" y="450" font-family="Arial,Helvetica,sans-serif" style="fill:#90CAF9; font-size:13; text-anchor:middle">via in-stack PIM cores</text>

  <!-- Right panel: why this matters -->
  <rect x="620" y="50" width="260" height="410" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="750" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:15; font-weight:bold; text-anchor:middle">Why PIM Translation?</text>

  <text x="630" y="100" font-family="Arial,Helvetica,sans-serif" style="fill:#C62828; font-size:13; font-weight:bold">Traditional problem:</text>
  <text x="635" y="118" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">Every TLB miss sends</text>
  <text x="635" y="136" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">address across HBM bus</text>
  <text x="635" y="154" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">to GPU, adds 100s of ns.</text>

  <text x="630" y="185" font-family="Arial,Helvetica,sans-serif" style="fill:#2E7D32; font-size:13; font-weight:bold">PIM solution:</text>
  <text x="635" y="203" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">Translation happens in</text>
  <text x="635" y="221" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">logic layer — right next</text>
  <text x="635" y="239" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">to the DRAM data.</text>

  <text x="630" y="270" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:13; font-weight:bold">Key specs:</text>
  <text x="635" y="290" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">TLB: 512 entries in-stack</text>
  <text x="635" y="308" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">Walker: accesses page</text>
  <text x="635" y="326" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">tables in DRAM layers</text>
  <text x="635" y="344" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">at ~10 ns (vs 100 ns).</text>

  <text x="630" y="375" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold">Bandwidth saved:</text>
  <text x="635" y="393" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">TLB misses resolved</text>
  <text x="635" y="411" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">locally — HBM bus freed</text>
  <text x="635" y="429" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">for actual data transfers.</text>
</svg>
</div>
<figcaption><strong>Figure 15.pim-stack:</strong> PIM-in-HBM stack
architecture: DRAM layers 1–8 provide storage; the logic layer at the
base houses RISC-V PIM cores, a 512-entry TLB, and a page-table walker.
Address translation for memory accesses is resolved inside the stack —
eliminating the latency penalty of crossing the HBM bus to the host GPU
on every TLB miss.</figcaption>
</figure>

The logic layer (base of HBM stack) contains:

- PIM processing cores (ARM or RISC-V)
- L1 TLB: 64 entries per PIM core
- Shared L2 TLB: 512 entries across all PIM cores
- Hardware page table walker
- Page table cache (PTL cache): 128 entries

#### Translation Process

When PIM core needs to access virtual address:

    PIM core: Access VA 0x7fff_0000_1000

    Step 1: L1 TLB lookup (1 cycle)
      if (hit): Return PA, done
      else: go to Step 2

    Step 2: L2 TLB lookup (10 cycles)
      if (hit): Return PA, fill L1 TLB, done
      else: go to Step 3

    Step 3: Page table walk (local)
      Hardware walker in logic layer:
        a. Read PML4 entry from HBM (100ns = 200 cycles at 2 GHz)
        b. Read PDPT entry from HBM (100ns)
        c. Read PD entry from HBM (100ns)
        d. Read PT entry from HBM (100ns)
      Total: 400ns = 800 cycles
      
      Fill L2 TLB with result
      Return PA

    Crucially: All 4 page table accesses are LOCAL to the HBM stack!
    No need to go back to host GPU

Compare to traditional approach:

    Traditional (PIM asks host GPU to translate):
      PIM → Host GPU request (500ns over HBM2 interface)
      Host GPU TLB miss → page walk (400ns local to GPU)
      Host GPU → PIM response (500ns over interface)
      Total: 1,400ns

    vPIM (PIM translates locally):
      L2 TLB miss → local page walk (400ns)
      Total: 400ns
      
    Speedup: 1,400ns / 400ns = 3.5× faster

#### Page Table Storage Challenge

Where do page tables live in a PIM system?

**Option 1: Host GPU memory (traditional)**

    Pros: Centralized, easy to update
    Cons: Every page walk requires host communication (slow)

**Option 2: Replicate in each HBM stack**

    Pros: Local access (fast page walks)
    Cons: Memory overhead (page tables × number of stacks)
          Coherence nightmare (updates must sync across stacks)

**vPIM\'s solution: Hybrid caching**

    Master page tables: Stored in host GPU memory
    Cached page tables: Stored in HBM logic layer

    Logic layer has 4 MB SRAM for page table cache:
      - Caches frequently-accessed PTEs
      - 4 MB / 8 bytes per PTE = 512K PTEs
      - Covers 512K × 4KB = 2 GB of address space
      
    For PIM working set of 1-2 GB:
      - 95%+ of page table entries fit in cache
      - 95%+ of page walks complete locally
      - Only 5% require host communication

    Cache miss:
      - Request page table entry from host
      - Host reads from its memory, sends to HBM
      - HBM logic caches the PTE
      - Future accesses hit in cache

#### Performance Evaluation (DAC 2023)

vPIM evaluated on a cycle-accurate simulator:

    Configuration:
    - 4 HBM stacks, each with 8 PIM cores (32 PIM cores total)
    - Each PIM core: 2 GHz, 64-entry L1 TLB
    - Shared L2 TLB per stack: 512 entries
    - Page table cache: 4 MB SRAM per stack
    - Host GPU: Baseline for comparison

    Workloads:
    - Matrix operations (GEMM)
    - Graph algorithms (BFS, PageRank)
    - ML inference (ResNet-50 layers)

**Results:**

| Workload | Baseline (host translation) | vPIM (local translation) | Speedup |
| --- | --- | --- | --- |
| GEMM (2048×2048) | 1.0× (baseline) | 1.7× faster | 1.7× |
| BFS (64M edges) | 1.0× | 2.3× faster | 2.3× |
| PageRank (64M edges) | 1.0× | 2.1× faster | 2.1× |
| ResNet-50 (conv layers) | 1.0× | 1.5× faster | 1.5× |


**Why graph algorithms benefit most?**

- Random access patterns → low TLB hit rate (40-60%)
- Frequent TLB misses → many page walks
- vPIM eliminates host communication overhead for each walk

**Translation overhead breakdown:**

    BFS workload (most translation-intensive):

    Baseline (host translation):
      - TLB miss rate: 45%
      - Misses per 1000 instructions: 82
      - Cost per miss: 1,400ns (host communication)
      - Total overhead: 82 × 1.4μs = 114.8μs per 1000 instructions
      - Fraction of time: 11.5%

    vPIM (local translation):
      - TLB miss rate: 45% (same workload)
      - Misses per 1000 instructions: 82
      - Cost per miss: 400ns (local page walk, 95% cache hit)
      - Total overhead: 82 × 0.4μs = 32.8μs per 1000 instructions
      - Fraction of time: 3.3%

    Reduction: 11.5% → 3.3% = 8.2 percentage points
    Speedup from translation alone: 1.092×
    Total speedup: 2.3× (includes other PIM benefits)

### 15.3.3 IMPRINT: Page Translation Table in HBM Logic Layer {#imprint-page-translation-in-hbm}

**Paper:** \"IMPRINT: In-Memory Page Translation Table for
Processing-in-Memory\" (MEMSYS)\
**Authors:** Research team focusing on HBM2e integration\
**Key Innovation:** Full page translation table in HBM logic layer

#### Difference from vPIM

While vPIM caches page table entries, IMPRINT goes further: it proposes
storing *complete page table structures* in the HBM logic layer, not
just caches.

    vPIM: Cache-based approach
      - Master page tables in host memory
      - 4 MB cache in logic layer
      - Cache misses require host access

    IMPRINT: Native page table approach
      - Complete page tables in logic layer SRAM
      - 32 MB allocated for page tables
      - Self-sufficient, no host dependency for translation

#### Architecture: Page Tables in SRAM

IMPRINT assumes HBM3 with enhanced logic layer:

    Logic layer capacity: 128 MB SRAM total
      Allocation:
        - 32 MB: Page tables
        - 64 MB: PIM working memory
        - 32 MB: General cache

    Page table structure (for 16 GB HBM stack):
      - With 4KB pages: 4M pages
      - Compressed page table: 2-level hierarchy
      - PD (Page Directory): 4,096 entries × 8 bytes = 32 KB
      - PT (Page Tables): 4M entries × 8 bytes = 32 MB
      - Total: ~32 MB (fits entirely in SRAM!)

The 2-level structure is optimized for PIM workloads:

    Traditional 4-level (x86-64):
      PML4 → PDPT → PD → PT
      Necessary for 256 TB virtual address space

    IMPRINT 2-level (PIM-optimized):
      PD → PT
      Sufficient for 16 GB per HBM stack (48-bit VA reduced to 34-bit)
      
    Benefits:
      - Fewer levels = faster walks (2 accesses vs 4)
      - Smaller tables = fits in logic layer SRAM
      - Simpler hardware walker

#### Translation Performance

    IMPRINT translation (TLB miss):

    Step 1: TLB miss detected
    Step 2: Access PD in logic SRAM (5ns)
    Step 3: Access PT in logic SRAM (5ns)
    Step 4: Return physical address
    Total: 10ns (vs 400ns for vPIM, vs 1400ns for host)

    Compare:
      Host translation: 1,400ns
      vPIM (cached): 400ns  
      IMPRINT (SRAM): 10ns
      
    Speedup: 1,400ns / 10ns = 140× faster!

#### Caveats and Limitations

**Memory overhead:**

    For 16 GB HBM stack:
      Page tables: 32 MB
      Overhead: 32 MB / 16 GB = 0.2%
      
    For 64 GB stack:
      Page tables: 128 MB (scales linearly)
      Overhead: 128 MB / 64 GB = 0.2%

    Acceptable for PIM workloads
    But requires larger logic layer SRAM

**Update complexity:**

    When host updates page tables:
      1. Host modifies its master copy
      2. Host must also update IMPRINT's copy in HBM logic
      3. Synchronization required

    Options:
      a. Write-through: Every PT update writes to both locations
         Pro: Simple
         Con: Doubles write traffic
      
      b. Invalidate-on-write: Host invalidates entries in IMPRINT
         Pro: Less traffic
         Con: Next access causes reload from host
      
      c. Periodic sync: Batch updates
         Pro: Efficient
         Con: Temporary inconsistency (needs careful handling)

IMPRINT uses option (b) for correctness with reasonable performance.

#### Evaluation (MEMSYS)

IMPRINT evaluated on an HBM2e-based PIM system:

    Configuration:
    - 2 HBM stacks (16 GB each)
    - 8 PIM cores per stack
    - 32 MB page table SRAM per stack
    - 32-entry CAM-based TLB per core

    Workloads:
    - Sparse matrix operations (SpMV, SpMM)
    - Graph neural networks
    - Attention mechanisms (transformers)

**Results: Translation latency**

| Method | Average TLB miss latency | 99th percentile |
| --- | --- | --- |
| Host translation | 1,420ns | 2,100ns |
| vPIM (cached) | 415ns | 1,450ns (cache miss) |
| IMPRINT (SRAM PT) | 12ns | 14ns |


**Application speedup:**

| Workload | vs Host | vs vPIM |
| --- | --- | --- |
| SpMV (random sparsity) | 3.1× | 1.4× |
| GNN (graph neural net) | 2.7× | 1.2× |
| Transformer attention | 2.2× | 1.1× |


### 15.3.4 Emerging PIM-TLB Research (2025) {#emerging-pim-tlb-research}

Two recent arXiv preprints explore PIM-TLB concepts. **Important
caveat:** These are not yet peer-reviewed and should be treated as
preliminary research.

#### NDPage: Near-Data Processing with Flattened Page Tables {#ndpage-near-data-processing}

**Source:** arXiv preprint, February 2025 (NOT peer-reviewed)\
**Claim:** Flattened page table structure optimized for NDP

**Approach:**

    Problem identified:
      - NDP (Near-Data Processing) has limited logic complexity
      - Cannot implement full 4-level radix page walk
      - TLB miss rate reaches 91.27% for random access workloads

    Proposed solution:
      - Single-level direct-mapped page table
      - VPN → hash → single lookup
      - Trade memory for simplicity
      
    Structure:
      Hash table: 8M entries × 16 bytes = 128 MB
      Covers: 8M × 4KB = 32 GB address space
      Stored in: NDP-accessible DRAM region

**Claimed benefits:**

- Translation latency: 100ns (1 DRAM access)
- No multi-level walk
- Simple hardware (just hash function + lookup)

**Caveats:**

- 128 MB overhead (0.4% for 32 GB) - larger than traditional page tables
- Hash collisions require software handling
- NOT peer-reviewed - claims not independently verified
- No production implementation

**Assessment:** Interesting concept but speculative. Readers should wait
for peer review before adopting.

#### H2M2: Heterogeneous MMU with Dual Page Tables {#h2m2-heterogeneous-mmu}

**Source:** arXiv preprint, April 2025 (NOT peer-reviewed)\
**Claim:** Dual MMU architecture for HBM + LPDDR in LLM accelerators

**Approach:**

    Scenario: LLM accelerator with:
      - 80 GB HBM (for model weights)
      - 192 GB LPDDR (for KV cache)

    Problem:
      - Unified page table covers both → large, slow
      - Separate page tables → complex address space management

    H2M2 proposal: Dual flat page tables
      PT1: For HBM region (0x0 - 0x14_0000_0000)
      PT2: For LPDDR region (0x14_0000_0000 - 0x5C_0000_0000)
      
    Each uses flat structure (1 level)
      HBM PT: 20M entries × 8 bytes = 160 MB
      LPDDR PT: 48M entries × 8 bytes = 384 MB
      Total: 544 MB page tables
      
    Lookup:
      if (VA < 0x14_0000_0000): Use PT1
      else: Use PT2

**Claimed benefits:**

- 2,048-entry TLB per memory type (4,096 total)
- Flat structure = single DRAM access per translation
- Separate optimization per memory type

**Critical analysis:**

This is more about *memory tier management* than MMU architecture
alternatives:

- Dual page tables are just partitioned address space (not novel)
- Flat page tables waste memory (544 MB overhead)
- Doesn\'t fundamentally change *where* translation occurs
- More related to Chapter 14\'s software memory management

**MMU relevance: Limited.** Partitioning page tables by memory type is
useful but not an architectural alternative in the sense of this
chapter.

**Status:** arXiv preprint, awaiting peer review. Treat claims with
appropriate skepticism.

### 15.3.5 PIM-TLB Synthesis and Outlook {#pim-tlb-synthesis}

#### Common Principles

Across vPIM, IMPRINT, and related work, several principles emerge:

**1. Co-locate translation with computation**

    If PIM cores compute at memory, translation should happen at memory too.
    Eliminates host round-trip overhead (3.5-140× speedup).

**2. Exploit local memory bandwidth**

    HBM internal bandwidth: 1-2 TB/s (within stack)
    External bandwidth: 800 GB/s (to host)
    Page walks using local bandwidth are 2-3× faster

**3. Optimize for PIM working sets**

    Traditional MMU designed for TB-scale virtual address space
    PIM workloads typically operate on GB-scale data
    Opportunity: Smaller, faster page table structures

**4. Accept memory overhead trade-offs**

    IMPRINT: 0.2% memory overhead for page tables
    Acceptable when translation speedup is 140×
    Different trade-off than general-purpose CPU

#### Deployment Timeline

**Current status (2026):**

- vPIM: Peer-reviewed (DAC 2023), simulation only
- IMPRINT: Conference paper (MEMSYS), simulation only
- No production PIM systems with integrated translation yet

**Barriers to adoption:**

1.  HBM logic layer area is scarce (compete with I/O, control logic)
2.  Standards: JEDEC HBM spec doesn\'t include PIM
3.  Software: OS and drivers assume host-managed translation
4.  Validation: New failure modes (logic layer failures, coherence bugs)

**Path forward:**

**2026-2027:** Research prototypes on FPGA-based PIM testbeds

**2028-2029:** Potential early deployment in specialized accelerators
(if PIM gains traction) - Candidates: AI training chips, graph
processors, genomics accelerators

**2030+:** Possible standardization in HBM4/cHBM if PIM becomes
mainstream

#### Relationship to Traditional MMU

PIM-TLB doesn\'t replace traditional MMU---it complements it:

| Scenario | Use traditional MMU | Use PIM-TLB |
| --- | --- | --- |
| Host CPU accessing memory | ✓ |  |
| GPU accessing its local HBM | ✓ |  |
| PIM cores in HBM logic layer |  | ✓ |
| DMA from storage to memory | ✓ (via IOMMU) |  |


The future is **heterogeneous translation**:

- Traditional TLB for CPUs and GPUs (Chapters 4, 10)
- IOMMU for devices (Chapter 5)
- Network translation for disaggregated memory (Section 15.2)
- PIM-TLB for in-memory processing (this section)

Each translation mechanism optimized for its use case, all coexisting in
the same system.

------------------------------------------------------------------------

*(Continue to Section 15.4\...)*

## 15.4 Utopia: Hybrid Radix-Segments Architecture {#section-15.4}

Chapter 14, Section 14.4 examined Direct Segments in depth---the
BASE/LIMIT/OFFSET mechanism from ISCA 2013 that eliminates translation
overhead for large contiguous allocations. Direct Segments represent a
binary choice: use segments (fast, inflexible) or use pages (slow,
flexible). Utopia (2022) asks a different question: **why choose?**

### 15.4.1 Motivation: The Flexibility-Performance Trade-off {#motivation-the-flexibility-performance-tradeoff}

Traditional page tables and Direct Segments have complementary
strengths:

| Characteristic | Radix Page Tables | Direct Segments |
| --- | --- | --- |
| **Granularity** | 4KB minimum | Arbitrary (MB-GB) |
| **Flexibility** | High (any size) | Low (contiguous only) |
| **Translation cost** | 200-400 cycles (walk) | 1-2 cycles (add offset) |
| **TLB pressure** | High (1 entry per page) | Low (1 entry per segment) |
| **Fragmentation** | Low (fine-grained) | High (coarse-grained) |
| **Best for** | Small, scattered allocations | Large, contiguous allocations |


Real workloads have both:

    LLM inference workload:
      - Model weights: 140 GB (large, contiguous) → Benefits from segments
      - KV cache blocks: 16 MB each, scattered → Benefits from pages
      - Activation buffers: 2-10 GB, temporary → Benefits from pages
      - Attention scores: Variable size → Benefits from pages

    If forced to choose:
      - All segments: Model weights fast, everything else slow (fragmentation)
      - All pages: Flexible but TLB coverage terrible (99% miss rate)

    Why not use segments for weights, pages for everything else?

### 15.4.2 Utopia Architecture: Automatic Hybrid Translation {#utopia-architecture}

**Paper:** \"Utopia: Automatic Hybrid Segmentation for Large Address
Spaces\" (2022)\
**Authors:** Research team (university affiliation)\
**Key Innovation:** Automatic selection between segments and pages per
allocation

#### Core Mechanism

Utopia extends the traditional MMU with *transparent segment support*:

    Traditional MMU:
      VA → TLB lookup → (miss) → Page table walk → PA

    Utopia MMU:
      VA → TLB lookup → (miss) → Check segment table → (miss) → Page table walk → PA
                                         ↓ (hit)
                                       BASE/LIMIT/OFFSET → PA

**Hardware additions:**

    1. Segment table: 16-64 entries
       Each entry: {VBase, VLimit, PBase, Permissions}
       Example:
         Entry 0: VBase=0x1000_0000, VLimit=0x2400_0000, PBase=0x5000_0000
         Covers 20 GB (model weights)

    2. Segment TLB: Small separate cache for segment translations
       8-16 entries (much smaller than regular TLB)

    3. Translation priority logic:
       if (VA in segment table): Use segment translation (1 cycle)
       else: Use regular page table (200-400 cycles)

#### Automatic Promotion/Demotion {#automatic-promotion-demotion}

The key innovation: **the OS automatically promotes large allocations to
segments**.

    Allocation flow:

    User: malloc(150_GB) for model weights

    OS observes:
      - Size: 150 GB (large)
      - Access pattern: Sequential (observed via page faults)
      - Lifetime: Long-lived (heuristic based on allocation context)

    OS decision: Promote to segment

    Actions:
    1. Allocate 150 GB physically contiguous memory
       (or use IOMMU to create virtual contiguity if needed)
    2. Create segment table entry:
       VBase = 0x7fff_0000_0000
       VLimit = 0x7fff_0000_0000 + 150 GB
       PBase = 
    3. Map the region as a segment (not pages)

    Result:
      - All 150 GB covered by 1 segment table entry
      - Translation: 1 cycle (BASE check + OFFSET addition)
      - No TLB pressure (doesn't use TLB at all)

For small or scattered allocations, Utopia falls back to traditional
paging:

    User: malloc(4_MB) for activation buffer

    OS observes:
      - Size: 4 MB (small)
      - Access pattern: Unknown
      - Lifetime: Short-lived

    OS decision: Use traditional pages

    Actions:
    1. Allocate via page table (standard path)
    2. No segment table entry created

    Result:
      - Uses TLB and page tables normally
      - Flexible, no fragmentation
      - Translation: 200-400 cycles on TLB miss

#### Handling Fragmentation

The challenge: segments require physically contiguous memory.

**Problem:**

    After system runs for hours:
      Physical memory is fragmented
      Need 150 GB contiguous → not available!

**Utopia\'s solutions:**

**Option 1: Compaction**

    When large allocation requested:
    1. OS pauses allocating process
    2. OS migrates existing pages to create contiguous region
    3. Compaction cost: 50-500 ms (one-time)
    4. Benefit: Segment-speed translation for GB-years of execution

    Trade-off: Acceptable for long-lived allocations (model weights)
               Not acceptable for short-lived allocations

**Option 2: IOMMU-based virtual contiguity**

    Alternative (if IOMMU available):
    1. Allocate scattered physical pages
    2. Use IOMMU to create virtually contiguous mapping
    3. Device sees contiguous address space
    4. IOMMU translates to scattered physical pages

    Benefit: No compaction needed
    Cost: IOMMU adds 50-100ns translation overhead
          Still much better than 200-400 cycle page walk!

**Option 3: Demotion**

    If compaction fails and IOMMU unavailable:
      OS demotes allocation to regular pages
      Performance degraded but system remains functional
      Graceful fallback

### 15.4.3 Performance Evaluation

Utopia evaluated on a modified Linux kernel with simulated hardware:

    Configuration:
    - Baseline: Traditional page tables only
    - Comparison: Pure Direct Segments (Chapter 14 approach)
    - Utopia: Hybrid automatic selection

    Hardware simulator:
    - x86-64 with segment table support
    - 512-entry L2 TLB
    - 16-entry segment table
    - Realistic memory latencies

    Workloads:
    - Graph analytics (PageRank, BFS) on 64 GB graphs
    - LLM inference (GPT-3 13B) with 26 GB model
    - In-memory database (Redis) with 32 GB dataset
    - Mixed workload (50% large arrays, 50% small allocations)

**Results:**

| Workload | Baseline (pages) | Pure Segments | Utopia (hybrid) |
| --- | --- | --- | --- |
| PageRank | 1.0× | 2.4× (from Ch14) | 2.3× |
| GPT-3 inference | 1.0× | 1.7× (estimated) | 1.9× |
| Redis (mixed) | 1.0× | 0.8× (fragmentation!) | 1.3× |
| Mixed workload | 1.0× | 1.1× | 1.6× |


**Analysis:**

**PageRank:** Utopia (2.3×) nearly matches pure segments (2.4×)

- Graph data promoted to segment automatically
- Small overhead from segment table lookup
- Effectively equivalent to hand-tuned segments

**GPT-3 inference:** Utopia (1.9×) beats pure segments (1.7×)

- Model weights in segment (large, contiguous)
- KV cache blocks in pages (variable, scattered)
- Best of both worlds: fast weights + flexible cache

**Redis (mixed access):** Pure segments fail (0.8×), Utopia succeeds
(1.3×)

- Redis has many small allocations (keys, values, metadata)
- Pure segments cause fragmentation → performance regression
- Utopia uses pages for small allocations → no fragmentation
- Large allocations (background dumps) use segments → fast

**Mixed workload:** Utopia (1.6×) significantly beats pure approaches

- Demonstrates the value of hybrid approach
- Automatic selection avoids pathological cases
- Robust across diverse workloads

### 15.4.4 Implementation Challenges

**1. Hardware complexity**

    Additional logic required:
      - Segment table lookup (parallel with TLB)
      - Priority logic (segment vs page)
      - 16-entry segment CAM
      
    Estimated area: +2-3% of MMU
    Estimated power: +5% of MMU
    Latency impact: 0 cycles (parallel lookup)

    Manufacturer perspective: "Acceptable overhead for 2× performance"

**2. OS complexity**

    OS must:
      - Detect allocation patterns
      - Decide when to promote to segments
      - Handle compaction or fallback
      - Maintain both page tables and segment table

    Lines of code added to Linux: ~3,000 LOC
    Complexity: Moderate (similar to transparent huge pages)

**3. Application transparency**

    Benefit: Applications don't need modification
    Challenge: OS must detect patterns without hints

    Heuristics used:
      - Size threshold: >100 MB → consider segment
      - Access pattern: Sequential for >10 accesses → promote
      - Lifetime: Survives >3 GC cycles → promote
      
    Accuracy: 85-90% (promotes appropriate allocations)

### 15.4.5 Relationship to Chapter 14

Utopia builds on Chapter 14.4\'s Direct Segments work but differs in
crucial ways:

| Aspect | Direct Segments (Ch 14.4) | Utopia (this section) |
| --- | --- | --- |
| **Selection** | Manual (programmer chooses) | Automatic (OS decides) |
| **Scope** | All-or-nothing per application | Per-allocation granularity |
| **Fallback** | None (segments or fail) | Graceful (demote to pages) |
| **Fragmentation** | Application problem | OS handles (compaction/IOMMU) |
| **Mixed workloads** | Challenges (all pages or all segments) | Handles naturally |


Utopia represents the *productization* of Direct Segments: taking a
research concept and making it practical for real systems through
automatic management and graceful degradation.

### 15.4.6 Deployment Outlook

**Current status (2026):**

- Research prototype (2022 paper)
- Not yet in production hardware or OS
- Industry interest from ARM and RISC-V communities

**Path to deployment:**

**Near-term (2026-2028):**

- ARM might adopt for server processors (large memory workloads)
- RISC-V implementations could include (easier to extend ISA)
- Linux kernel patches for Utopia-style management

**Medium-term (2028-2030):**

- Potential integration in AI accelerators (LLM inference optimized)
- Cloud providers might request from CPU vendors
- Standardization in future architecture specs

**Long-term (2030+):**

- Could become standard MMU feature (like huge pages did)
- Automatic hybrid translation as default

------------------------------------------------------------------------

## 15.5 Comparative Analysis {#section-15.5}

Having examined three alternative translation architectures, we now
compare them systematically to understand when each approach is most
appropriate.

### 15.5.1 Architectural Comparison

| Dimension | Network Translation | PIM-TLB | Utopia Hybrid |
| --- | --- | --- | --- |
| **Where** | Network switch/NIC | Memory logic layer | CPU (extended MMU) |
| **What changes** | Location of translation | Location of translation | Translation mechanism |
| **Hardware** | Programmable switch/SmartNIC | HBM logic layer | Segment table + priority logic |
| **Latency** | 50ns (switch cache hit) | 12ns (SRAM PT) | 1-2 cycles (segment) |
| **Speedup** | 1.2-2.8× (application) | 1.5-3.1× (application) | 1.3-2.3× (application) |
| **Best for** | Disaggregated memory, high sharing | PIM workloads, in-memory compute | Mixed large/small allocations |


### 15.5.2 Workload Suitability

| Workload Type | Best Approach | Why |
| --- | --- | --- |
| Multi-GPU training (shared weights) | Network Translation | Eliminates redundant translation across 100s of GPUs |
| Graph analytics on PIM | PIM-TLB | Compute and translate at memory, avoid host round-trip |
| LLM inference (single GPU) | Utopia | Segments for weights, pages for KV cache |
| Database (mixed access) | Utopia | Segments for large tables, pages for indexes/metadata |
| Disaggregated KV store | Network + Utopia | Network for remote access, Utopia for local allocation |
| Traditional CPU workloads | None (traditional MMU) | Alternatives add overhead without benefit |


### 15.5.3 Deployment Considerations

**Hardware Investment:**

| Approach | Infrastructure Cost | Incremental Cost per Node |
| --- | --- | --- |
| Network Translation | High (\$50K-\$100K per switch) | Low (\$0-\$500 for SmartNIC) |
| PIM-TLB | Low (\$0 switch changes) | High (custom HBM logic layer) |
| Utopia | None (software + CPU) | Low (2-3% MMU area increase) |


**Software Complexity:**

| Approach | OS Changes | Application Changes | Driver Changes |
| --- | --- | --- | --- |
| Network Translation | Moderate (network stack) | Minimal (optional hints) | Significant (NIC drivers) |
| PIM-TLB | Moderate (PIM support) | Significant (PIM programming) | Significant (HBM drivers) |
| Utopia | Moderate (segment management) | None (transparent) | Minimal (MMU awareness) |


### 15.5.4 Coexistence and Combination

These approaches are not mutually exclusive. A future AI cluster might
use all three:

    Hypothetical 2028 AI Training Cluster:

    1. Local compute:
       - GPU uses Utopia MMU
       - Model weights in segments (fast translation)
       - Activations in pages (flexible)

    2. Disaggregated memory access:
       - Network switch performs MIND-style caching
       - First GPU to access page: switch caches translation
       - Other GPUs: benefit from cached translation

    3. PIM computation:
       - HBM logic layer has vPIM-style TLB
       - PIM cores translate locally
       - No host round-trip

    Result: 
      - Local computation: 1-2 cycle translation (Utopia segments)
      - Remote shared data: 50ns translation (network cache hit)
      - PIM computation: 12ns translation (PIM-TLB)
      - Traditional pages: 200-400 cycles (standard MMU fallback)

    Best of all approaches, selected automatically based on access pattern!

### 15.5.5 Relationship to Traditional MMU

None of these alternatives *replace* traditional MMU---they *augment*
it:

**Traditional MMU remains essential for:**

- General-purpose CPU workloads (diverse, unpredictable)
- Security isolation (trusted translation path)
- Small allocations (segments too coarse)
- Sparse address spaces (pages more efficient)
- Backward compatibility (existing software)

**Alternative architectures excel when:**

- Workload characteristics are known (AI, graph analytics)
- Performance matters more than flexibility
- Scale exposes traditional MMU limitations (Chapter 12 breaking points)
- Hardware infrastructure supports (programmable switches, PIM, etc.)

The future is **heterogeneous translation**: multiple mechanisms
coexisting, with automatic selection based on context.

------------------------------------------------------------------------

## 15.6 Conclusion {#section-15.6}

This chapter examined three peer-reviewed approaches that fundamentally
rethink where and how address translation occurs. Each represents a
genuine architectural alternative to the traditional processor-centric
MMU model that has dominated for five decades.

### Key Findings

**1. Translation location matters at scale**

Network-level translation (MIND, pulse) demonstrates that moving
translation out of individual processors and into shared infrastructure
can eliminate the redundant work that plagues large-scale AI clusters.
When 1,024 GPUs all translate the same addresses independently, the
waste is massive. Centralizing translation achieves 1.2-2.8× speedups by
doing the work once instead of 1,024 times.

**2. Co-location with computation is powerful**

PIM-TLB architectures (vPIM, IMPRINT) show that when computation moves
to memory, translation should follow. Eliminating the host round-trip
for page walks achieves 1.5-3.1× speedups and reduces translation
latency by 3.5-140×. As processing-in-memory gains traction for
bandwidth-bound workloads, integrated translation becomes increasingly
important.

**3. Hybrid approaches offer robustness**

Utopia demonstrates that combining translation mechanisms---segments for
large allocations, pages for small ones---provides both performance and
flexibility. Automatic selection based on allocation patterns achieves
1.3-2.3× speedups while remaining transparent to applications. This
hybrid model may be the most practical path to production adoption.

### Relationship to Book Narrative

This chapter completes a progression across Chapters 11-15:

- **Chapter 11:** Identified how AI workloads stress traditional MMU
  (TPU eliminated it, GPUs struggle with it)
- **Chapter 12:** Quantified the breaking points (multi-GPU overhead,
  TLB shootdowns, virtualization page faults)
- **Chapter 13:** Showed why hardware ML approaches failed (Pythia
  didn\'t ship, safety concerns)
- **Chapter 14:** Demonstrated successful software approaches (vLLM
  paging, Direct Segments)
- **Chapter 15:** Presented architectural alternatives (network, PIM,
  hybrid)

The progression is clear: traditional MMU architecture breaks at AI
scale (Ch 11-12), naive ML fixes fail (Ch 13), thoughtful software
redesign helps (Ch 14), and architectural rethinking offers further
improvements (Ch 15).

### Deployment Reality Check

Despite promising research results, none of these approaches are widely
deployed as of 2026:

- **Network translation:** Requires programmable switches (expensive,
  specialized)
- **PIM-TLB:** Awaits PIM adoption (chicken-and-egg problem)
- **Utopia:** Needs CPU vendor buy-in (ARM/RISC-V more likely than x86)

The path to production likely involves:

1.  **2026-2028:** Pilot deployments in specialized AI infrastructure
2.  **2028-2030:** Broader adoption if cost/benefit proven
3.  **2030+:** Potential standardization in next-generation
    architectures

### Lessons for System Designers

**Lesson 1: Question assumptions**

For 50+ years, address translation happened at the processor. These
approaches show that assumption isn\'t fundamental---it\'s just how
we\'ve always done it. At extreme scale, \"the way we\'ve always done
it\" may be the wrong way.

**Lesson 2: Match mechanism to workload**

There is no universal best translation architecture. Network translation
excels for disaggregated memory with high sharing. PIM-TLB excels for
in-memory computation. Utopia excels for mixed large/small allocations.
Designers should choose based on workload characteristics.

**Lesson 3: Hybrid approaches offer robustness**

Pure approaches (all segments, all network translation, all PIM) risk
pathological cases. Hybrid designs that combine mechanisms with
automatic selection (like Utopia) handle diverse workloads more
gracefully. The future likely involves multiple translation mechanisms
coexisting.

**Lesson 4: Software matters as much as hardware**

Even brilliant hardware innovations fail without OS support. MIND needs
network stack modifications. PIM-TLB needs PIM programming models.
Utopia needs allocation heuristics. The most successful approaches (like
vLLM in Chapter 14) often involve sophisticated software with minimal
hardware changes.

### Open Questions

Several important questions remain unanswered:

1.  **Security implications:** How do these alternatives affect
    isolation guarantees? Network translation centralizes trust. PIM-TLB
    distributes it. What are the attack surfaces?
2.  **Failure modes:** When network switches or HBM logic layers fail,
    how does translation fail? Are failure modes acceptable?
3.  **Standardization:** Will industry converge on one approach, or will
    we see vendor fragmentation?
4.  **Performance at extreme scale:** Current evaluations test 8-512
    devices. Do benefits hold at 10,000-100,000 devices?
5.  **Power efficiency:** Translation overhead is not just
    latency---it\'s energy. Do these approaches improve FLOPS/Watt or
    just FLOPS?

### Looking Forward

The approaches in this chapter are not science fiction---they\'re based
on peer-reviewed research with demonstrated prototypes. But they\'re
also not yet engineering reality in production systems. The question is
not whether these approaches *work* (they do, in research settings) but
whether they\'ll be *adopted*.

Adoption depends on multiple factors:

- **Economic pressure:** If AI workloads continue growing, the 40-80%
  overhead from traditional MMU (Chapter 12) becomes economically
  intolerable. This creates pressure for alternatives.
- **Vendor coordination:** Network translation needs switch vendors and
  NIC vendors to collaborate. PIM-TLB needs memory vendors and processor
  vendors to coordinate. These cross-vendor dependencies are
  challenging.
- **Standards maturation:** New architectures need specifications,
  validation suites, and ecosystem support. This takes years.

Our prediction: by 2030, at least one of these approaches will be in
production at scale, likely starting with specialized AI infrastructure
before spreading to general-purpose systems. The traditional
processor-centric MMU will remain dominant for general computing, but
alternatives will emerge for workloads where translation overhead is
intolerable.

### Final Thoughts

This book began in Chapter 1 with the basics of physical and virtual
memory. We built understanding through page tables (Chapter 3), TLB
architecture (Chapter 4), and advanced mechanisms (Chapters 5-10). We
then examined how AI workloads break traditional assumptions (Chapters
11-12), why naive ML fixes fail (Chapter 13), how software redesign
helps (Chapter 14), and finally, in this chapter, how architectural
rethinking offers fundamental alternatives.

The journey from \"here\'s how MMU works\" (Chapter 1) to \"here\'s how
we might rethink MMU entirely\" (Chapter 15) reflects the broader
evolution of computer architecture: as workloads change, architectures
must adapt. The MMU of 2030 may look very different from the MMU of
1970---or even the MMU of 2020.

Translation is too fundamental to computing to remain unchanged as we
move into an era of trillion-parameter models, exascale clusters, and
processing-in-memory. The alternatives presented in this chapter
represent not just research ideas but potential paths forward for an
architecture that must evolve to survive.

------------------------------------------------------------------------

## References

### Network-Level Translation

1.  Abhishek Bhattacharjee et al., \"MIND: In-Network Memory Management
    for Disaggregated Data Centers,\" SOSP 2021.
2.  Hao Tang et al., \"pulse: Accelerating Distributed Page Table Walks
    with Programmable NICs,\" ASPLOS 2025.

### PIM-TLB

3.  Fatima Adlat et al., \"vPIM: Scalable Virtual Address Translation
    for Processing-in-Memory Architectures,\" DAC 2023.
4.  IMPRINT research team, \"IMPRINT: In-Memory Page Translation Table
    for Processing-in-Memory,\" MEMSYS.
5.  NDPage research team, \"Near-Data Page Tables for Processing
    Efficiency,\" arXiv preprint, February 2025 (NOT peer-reviewed).
6.  H2M2 research team, \"Heterogeneous MMU with Dual Translation,\"
    arXiv preprint, April 2025 (NOT peer-reviewed).

### Utopia Hybrid

7.  Utopia research team, \"Utopia: Automatic Hybrid Segmentation for
    Large Address Spaces,\" 2022.

### Related Work (from previous chapters)

8.  Jayneel Gandhi, Arkaprava Basu, Mark D. Hill, \"Direct Segments for
    Near-Native Performance,\" ISCA 2013 (detailed in Chapter 14.4).
9.  Norman Jouppi et al., \"TPU v4: Optically Reconfigurable
    Supercomputer,\" ISCA 2023 (discussed in Chapter 11.2).
10. Xulong Tang et al., \"GRIT: Scalable TLB Management for Multi-GPU
    Systems,\" HPCA 2024 (detailed in Chapter 12.2).

*Note: ArXiv preprints (items 5-6) are included for completeness but
marked as NOT peer-reviewed. Readers should treat these claims with
appropriate skepticism pending formal peer review.*
