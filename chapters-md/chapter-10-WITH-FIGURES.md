::: {#title-block-header}
# Chapter 10: Hardware Accelerators and External MMU Access {#chapter-10-hardware-accelerators-and-external-mmu-access .title}
:::

- [Chapter 10: Hardware Accelerators and External MMU
  Access](#chapter-10-hardware-accelerators-and-external-mmu-access){#toc-chapter-10-hardware-accelerators-and-external-mmu-access}
  - [10.1 Introduction: Beyond the CPU
    Core](#introduction-beyond-the-cpu-core){#toc-introduction-beyond-the-cpu-core}
    - [The Evolution of Device Memory
      Access](#the-evolution-of-device-memory-access){#toc-the-evolution-of-device-memory-access}
    - [What This Chapter
      Covers](#what-this-chapter-covers){#toc-what-this-chapter-covers}
    - [Why These Mechanisms
      Matter](#why-these-mechanisms-matter){#toc-why-these-mechanisms-matter}
    - [Relationship to Previous
      Chapters](#relationship-to-previous-chapters){#toc-relationship-to-previous-chapters}
  - [10.2 IOMMU Architecture Deep
    Dive](#iommu-architecture-deep-dive){#toc-iommu-architecture-deep-dive}
    - [The Core Challenge: Per-Device
      Isolation](#the-core-challenge-per-device-isolation){#toc-the-core-challenge-per-device-isolation}
    - [Intel VT-d
      Architecture](#intel-vt-d-architecture){#toc-intel-vt-d-architecture}
    - [IOMMU Page Fault
      Handling](#iommu-page-fault-handling){#toc-iommu-page-fault-handling}
    - [Performance Case Study: NVMe with
      IOMMU](#performance-case-study-nvme-with-iommu){#toc-performance-case-study-nvme-with-iommu}
    - [AMD IOMMU (AMD-Vi)
      Differences](#amd-iommu-amd-vi-differences){#toc-amd-iommu-amd-vi-differences}
    - [ARM SMMU (System Memory Management
      Unit)](#arm-smmu-system-memory-management-unit){#toc-arm-smmu-system-memory-management-unit}
  - [10.3 PCIe ATS and Address Translation
    Services](#pcie-ats-and-address-translation-services){#toc-pcie-ats-and-address-translation-services}
    - [The ATS Innovation](#the-ats-innovation){#toc-the-ats-innovation}
    - [ATS Protocol
      Messages](#ats-protocol-messages){#toc-ats-protocol-messages}
    - [PASID: Process Address Space
      ID](#pasid-process-address-space-id){#toc-pasid-process-address-space-id}
    - [PRI: Page Request
      Interface](#pri-page-request-interface){#toc-pri-page-request-interface}
  - [10.4 RDMA and Memory
    Registration](#rdma-and-memory-registration){#toc-rdma-and-memory-registration}
    - [The RDMA Model](#the-rdma-model){#toc-the-rdma-model}
    - [Traditional Memory
      Registration](#traditional-memory-registration){#toc-traditional-memory-registration}
    - [The Registration Problem in
      Practice](#the-registration-problem-in-practice){#toc-the-registration-problem-in-practice}
    - [Solution 1:
      Pre-Registration](#solution-1-pre-registration){#toc-solution-1-pre-registration}
    - [Solution 2: Memory Registration
      Cache](#solution-2-memory-registration-cache){#toc-solution-2-memory-registration-cache}
    - [Solution 3: On-Demand Paging
      (ODP)](#solution-3-on-demand-paging-odp){#toc-solution-3-on-demand-paging-odp}
    - [Hybrid Approach: Explicit +
      ODP](#hybrid-approach-explicit-odp){#toc-hybrid-approach-explicit-odp}
    - [Case Study: Redis with
      RDMA](#case-study-redis-with-rdma){#toc-case-study-redis-with-rdma}
  - [10.5 Smart NICs and Data Processing
    Units](#smart-nics-and-data-processing-units){#toc-smart-nics-and-data-processing-units}
    - [NVIDIA BlueField DPU
      Architecture](#nvidia-bluefield-dpu-architecture){#toc-nvidia-bluefield-dpu-architecture}
    - [Accessing Host Memory from
      DPU](#accessing-host-memory-from-dpu){#toc-accessing-host-memory-from-dpu}
    - [Use Case 1: OVS
      Offload](#use-case-1-ovs-offload){#toc-use-case-1-ovs-offload}
    - [Use Case 2: NVMe-oF
      Target](#use-case-2-nvme-of-target){#toc-use-case-2-nvme-of-target}
    - [Coherency
      Challenges](#coherency-challenges){#toc-coherency-challenges}
    - [Real-World Deployment: Cloud Provider
      Networking](#real-world-deployment-cloud-provider-networking){#toc-real-world-deployment-cloud-provider-networking}
    - [Intel PAC (Programmable Acceleration Card) with
      CCI-P](#intel-pac-programmable-acceleration-card-with-cci-p){#toc-intel-pac-programmable-acceleration-card-with-cci-p}
    - [FPGA → CPU Memory Access
      Example](#fpga-cpu-memory-access-example){#toc-fpga-cpu-memory-access-example}
    - [Use Case: Genomics
      Alignment](#use-case-genomics-alignment){#toc-use-case-genomics-alignment}
    - [Cache Coherency
      Protocol](#cache-coherency-protocol){#toc-cache-coherency-protocol}
    - [AMD CCIX (Cache Coherent Interconnect for
      Accelerators)](#amd-ccix-cache-coherent-interconnect-for-accelerators){#toc-amd-ccix-cache-coherent-interconnect-for-accelerators}
  - [10.7 Video and Media
    Accelerators](#video-and-media-accelerators){#toc-video-and-media-accelerators}
    - [Intel QuickSync
      Architecture](#intel-quicksync-architecture){#toc-intel-quicksync-architecture}
    - [NVIDIA NVENC/NVDEC](#nvidia-nvencnvdec){#toc-nvidia-nvencnvdec}
  - [10.8 Multi-Device Coherency and
    Coordination](#multi-device-coherency-and-coordination){#toc-multi-device-coherency-and-coordination}
    - [The TLB Shootdown
      Problem](#the-tlb-shootdown-problem){#toc-the-tlb-shootdown-problem}
    - [Batching TLB
      Invalidations](#batching-tlb-invalidations){#toc-batching-tlb-invalidations}
    - [Cross-Device
      Ordering](#cross-device-ordering){#toc-cross-device-ordering}
    - [Deadlock Avoidance](#deadlock-avoidance){#toc-deadlock-avoidance}
    - [System
      Architecture](#system-architecture){#toc-system-architecture}
    - [Memory Layout and
      Sharing](#memory-layout-and-sharing){#toc-memory-layout-and-sharing}
    - [IOMMU
      Configuration](#iommu-configuration){#toc-iommu-configuration}
    - [Device
      Synchronization](#device-synchronization){#toc-device-synchronization}
    - [TLB Coherency Across
      Devices](#tlb-coherency-across-devices){#toc-tlb-coherency-across-devices}
    - [Performance
      Results](#performance-results){#toc-performance-results}
  - [10.10 Summary and Best
    Practices](#summary-and-best-practices){#toc-summary-and-best-practices}
    - [Key Techniques
      Recap](#key-techniques-recap){#toc-key-techniques-recap}
    - [Common Pitfalls to Avoid: Detailed
      Analysis](#common-pitfalls-to-avoid-detailed-analysis){#toc-common-pitfalls-to-avoid-detailed-analysis}
    - [Decision Framework](#decision-framework){#toc-decision-framework}
    - [Looking Forward](#looking-forward){#toc-looking-forward}
    - [References](#references){#toc-references}

# Chapter 10: Hardware Accelerators and External MMU Access {#chapter-10-hardware-accelerators-and-external-mmu-access}

## 10.1 Introduction: Beyond the CPU Core

On a March afternoon in 2018, engineers at a high-frequency trading firm
discovered an anomaly that would cost them \$1.2 million in a single
trading session. Their RDMA-based market data feed---carefully optimized
to deliver sub-microsecond latency---was experiencing sporadic 50-100
millisecond stalls. In high-frequency trading, 100 milliseconds is an
eternity. Competitors were exploiting price discrepancies that the
firm\'s systems should have caught first.

The root cause surprised everyone. The firm had recently enabled
Intel\'s IOMMU for security isolation, protecting their systems against
malicious PCIe devices. The IOMMU was doing its job---translating device
memory accesses through page tables just like the CPU does. But nobody
had accounted for what happens when the IOMMU\'s translation cache (the
IOTLB) misses and needs to perform a full page table walk. That walk,
happening at PCIe speed rather than CPU cache speed, was introducing
latency spikes that the trading algorithms couldn\'t tolerate.

This incident illustrates a fundamental shift in how we must think about
memory management. For decades, the MMU was synonymous with the CPU---a
piece of silicon sitting next to the processor cores, translating
virtual addresses as instructions executed. But modern systems have
evolved far beyond this simple model. Today\'s servers contain dozens of
devices that independently access memory: network cards pulling packet
data, GPUs rendering graphics, storage controllers moving files, AI
accelerators processing neural networks, and FPGAs running custom logic.

Each of these devices needs virtual memory. They need it for the same
reasons CPUs do: protection (preventing one device from corrupting
another\'s memory), flexibility (allowing devices to work with virtual
addresses rather than managing physical memory layout), and efficiency
(enabling zero-copy data sharing between devices and CPUs). But these
devices don\'t have CPUs. They can\'t execute the complex page table
walking code that handles CPU page faults. They need specialized
hardware and protocols to participate in the system\'s memory management
infrastructure.

This chapter explores that infrastructure---the mechanisms that allow
non-CPU devices to access the memory management unit and participate in
virtual memory. We\'ll see how IOMMUs provide per-device page tables,
how PCIe Address Translation Services cache translations at the device,
how RDMA NICs handle memory registration and page faults, how Smart NICs
with embedded processors access host memory, and how FPGAs can
participate in cache coherency protocols. Understanding these mechanisms
is critical for anyone building or optimizing systems that push data
between devices at high speeds.

### The Evolution of Device Memory Access

The journey from simple DMA to modern IOMMU-based translation reveals
three distinct eras, each solving problems created by the previous
generation.

**Era 1: Physical Addressing Only (pre-2005)**

Early devices used direct memory access with physical addresses only:

    Application allocates buffer:
      void *buf = malloc(1MB);
      
    Kernel pins pages (prevents swapping):
      mlock(buf, 1MB);
      
    Kernel walks page tables to get physical addresses:
      for each 4KB page:
        virt_addr → page_table_walk → phys_addr
        
    Device receives list of physical addresses:
      DMA_descriptor[0] = 0x12340000 (physical)
      DMA_descriptor[1] = 0x12341000 (physical)
      ...

This approach was simple but had severe limitations that became
increasingly untenable as systems evolved. The simplicity was
appealing---device drivers could directly translate virtual to physical
addresses using the same page table walk the kernel performed for CPU
accesses. But this simplicity came at enormous cost.

Pinned memory couldn\'t be swapped, wasting precious RAM when devices
weren\'t actively using it. Consider a network card with 10 GB of
pre-allocated buffers for packet reception. Even when the network was
idle (no packets arriving), those 10 GB remained locked in physical
memory, unusable for other purposes. On a server with 128 GB total RAM,
nearly 8% was wasted on idle buffers. Multiply this across all devices
(storage controllers, GPUs, etc.) and the waste compounds.

Applications had to know physical addresses, breaking the fundamental
abstraction that virtual memory provides. This meant device drivers
needed special privileges to walk page tables---a security risk. It also
meant applications couldn\'t easily share buffers across devices since
each device needed its own translation to physical addresses. The lack
of abstraction created tight coupling between software and hardware.

Devices could potentially access any physical memory, creating
catastrophic security vulnerabilities. A malicious or buggy device
driver could program the device to DMA to arbitrary physical addresses.
Since there was no isolation layer, the device would happily comply,
potentially reading cryptographic keys from kernel memory or overwriting
critical data structures. In multi-tenant cloud environments, this would
allow one customer\'s device to access another customer\'s memory---a
complete failure of isolation.

And the scatter-gather lists grew enormous for large transfers since
physical memory fragments over time. After a week of system uptime,
physical memory becomes highly fragmented due to allocation and
deallocation churn. A 1 GB logically contiguous region might be
scattered across thousands of physical frames. Describing this to the
device required thousands of scatter-gather list entries, consuming
memory and taking time to program into the device.

This fragmentation problem is actually why many pre-IOMMU systems used
techniques like memory pools and slab allocators that never freed
memory---they allocated buffers at boot time and kept them forever to
maintain physical contiguity. But this wasted even more memory and
limited flexibility.

This approach but had severe limitations. Pinned memory couldn\'t be
swapped, wasting precious RAM. Applications had to know physical
addresses, breaking abstraction. Devices could potentially access any
physical memory, creating security vulnerabilities. And the
scatter-gather lists grew enormous for large transfers since physical
memory is fragmented.

**Era 2: IOMMU Translation (2005-2015)**

Intel VT-d and AMD-Vi introduced Input-Output Memory Management Units.
These provided per-device page tables, allowing devices to use virtual
addresses:

    Device perspective:
      DMA to virtual address 0x7fff_1000
      
    IOMMU intercepts:
      Device ID: 03:00.0 (Bus 3, Device 0, Function 0)
      Lookup device's page table
      Walk: PGD → P4D → PUD → PMD → PTE
      Find physical address: 0x1234_5000
      Complete DMA to physical address

This solved many problems elegantly by inserting a translation layer
between devices and physical memory---exactly the same abstraction that
virtual memory provides for CPUs. The IOMMU became the device equivalent
of the CPU\'s MMU, providing per-device page tables that isolated
address spaces and enabled virtualization.

Memory could be scattered across physical RAM but appear contiguous to
the device, completely solving the fragmentation problem. From the
device\'s perspective, its DMA buffer was a single contiguous 1 GB
region at virtual address 0x7000_0000. The IOMMU transparently mapped
this to whatever physical frames the kernel allocated, scattered
arbitrarily across physical RAM. This meant the kernel could use normal
allocation mechanisms without worrying about physical contiguity.

Devices couldn\'t access memory they weren\'t explicitly granted,
providing hardware-enforced isolation. Each device had its own page
tables controlled by the kernel or hypervisor. If a device tried to
access an unmapped address, the IOMMU would block the access and
generate a fault. This prevented both malicious attacks and buggy device
drivers from corrupting memory. In virtualized environments, it enabled
assigning physical devices directly to VMs without risking cross-VM
attacks.

And the kernel could swap pages, though most systems initially didn\'t
due to the complexity of handling device page faults. The hardware was
there---if a device accessed a swapped-out page, the IOMMU could detect
this and notify the CPU---but actually handling such faults required
coordination between device firmware, IOMMU driver, and kernel memory
management that most systems didn\'t implement. This capability remained
mostly theoretical until PRI was standardized.

But IOMMU translation introduced a new bottleneck that early adopters
didn\'t anticipate. Every device memory access now required an IOMMU
translation. The IOMMU had a TLB (called IOTLB) to cache translations,
but it was small (typically 256-512 entries) and shared across many
devices. For a high-bandwidth network card processing millions of
packets per second, each touching different pages, the IOTLB miss rate
could exceed 99%.

Each miss required a full page table walk---accessing the root table,
context table, and four levels of page tables, each from main memory at
\~100 ns per access. Total: 600+ ns per miss. For a device that
previously accessed memory in 100 ns (DRAM access latency), this
represented a 6× slowdown. The HFT firm\'s experience in our opening
story directly reflects this bottleneck---enabling IOMMU provided
security but destroyed latency-sensitive performance.

This bottleneck shaped the evolution toward Era 3. This solved many
problems. Memory could be scattered across physical RAM but appear
contiguous to the device. Devices couldn\'t access memory they weren\'t
explicitly granted. And the kernel could swap pages (though most
didn\'t, initially). But IOMMU translation introduced a new
bottleneck---every device memory access required an IOMMU translation,
and the IOMMU\'s TLB (called IOTLB) was small and shared across many
devices.

**Era 3: Device-Side Caching and Faulting (2015+)**

Modern systems add two critical capabilities: devices can cache
translations locally (PCIe ATS), and devices can page fault (PCIe PRI):

    First access to address 0x7fff_1000:
      Device checks local ATC (Address Translation Cache)
      Miss - send translation request to IOMMU
      IOMMU walks page tables, returns translation
      Device caches: 0x7fff_1000 → 0x1234_5000
      Device completes DMA
      
    Second access to 0x7fff_1000:
      Device checks ATC
      Hit! Use cached translation 0x1234_5000
      No IOMMU involvement - fast path
      
    Access to unmapped address 0x8000_0000:
      Device checks ATC - miss
      Device requests translation from IOMMU
      IOMMU detects page not present
      IOMMU sends Page Request to CPU
      CPU allocates page, updates page tables
      IOMMU returns translation to device
      Device retries DMA - success

This third era provides the performance of physical addressing with the
safety and flexibility of virtual memory. But it adds tremendous
complexity. Page faults now occur on devices, requiring coordination
between device firmware, IOMMU hardware, and CPU kernel. TLB
invalidations must reach not just CPU cores but also devices. And subtle
timing issues emerge when multiple devices access the same memory
simultaneously.

### What This Chapter Covers

We\'ll explore device memory access across seven domains, starting with
the IOMMU itself and progressing to increasingly specialized device
types:

**IOMMU Architecture** examines how Intel VT-d, AMD-Vi, and ARM SMMU
provide per-device page tables. We\'ll see the root/context table
structures that map device IDs to page tables, the IOTLB organization,
and the page fault handling flow. Real measurements show IOTLB misses
adding 500-2000 cycles---negligible for disk I/O but catastrophic for
low-latency networking.

**PCIe ATS (Address Translation Services)** explores how devices cache
translations locally in their ATC (Address Translation Cache). This
moves the TLB from the IOMMU to the device itself, eliminating IOMMU
round-trips for cached translations. We\'ll see the ATS protocol
messages, PASID (Process Address Space ID) for multi-process device
sharing, and PRI (Page Request Interface) for device-initiated page
faults.

**RDMA and Memory Registration** addresses the challenge of zero-copy
networking. Traditional memory registration pins gigabytes of RAM and
takes 50-200 milliseconds. Modern on-demand paging (ODP) eliminates
pinning but introduces page fault latency. We\'ll examine the trade-offs
and see how registration caching provides a middle ground.

**Smart NICs and DPUs** shows how network cards with embedded ARM
processors access host memory via PCIe. NVIDIA BlueField and Intel IPU
run Linux on the NIC and can read/write host RAM as if it were local,
but with microseconds of latency instead of nanoseconds. Use cases
include offloading OVS and running storage virtualization.

**FPGA Coherent Accelerators** demonstrates cache-coherent FPGA-to-CPU
memory access via Intel CCI-P and AMD CCIX. Unlike traditional FPGA
designs that copy data via DMA, coherent FPGAs participate in the CPU\'s
cache coherency protocol, eliminating copies at the cost of some
latency.

**Multi-Device Coherency** tackles the hardest problem: coordinating TLB
invalidations and cache coherency when CPUs, GPUs, NICs, and FPGAs all
access the same memory. A single page unmap requires invalidating TLBs
on potentially 100+ devices, taking 10-100 microseconds and serializing
the operation.

**Real-World Integration** synthesizes these concepts with a complete
multi-device video pipeline case study showing CPU, GPU, video encoder,
and NIC all sharing buffers via IOMMU.

### Why These Mechanisms Matter

The impact extends across multiple dimensions:

**Performance and Latency:** In high-frequency trading, 100 microseconds
determines profit or loss. In real-time video, frame drops create
visible artifacts. In storage, IOMMU overhead directly impacts IOPS.
Understanding when device translation adds latency vs. when it\'s
negligible separates performant systems from mediocre ones.

**Memory Efficiency:** Without IOMMU-based virtual addressing, devices
require pinned memory that can\'t be swapped or relocated. A server
running RDMA workloads might pin 200 GB of RAM, rendering it useless for
other purposes. On-demand paging eliminates this waste, but requires
understanding the page fault handling path.

**Security Isolation:** IOMMU is critical for multi-tenant cloud
security. Without it, a malicious PCIe device in one VM could DMA into
another VM\'s memory, stealing data or injecting code. But IOMMU
overhead can reduce performance by 20-50% if misconfigured. Balancing
security and performance requires detailed knowledge of IOMMU operation.

**Scalability:** Modern deep learning training uses 100s to 1000s of
GPUs exchanging gradients via RDMA. The scalability of this
communication directly depends on IOMMU/ATS efficiency. A poorly
configured IOMMU can limit scaling to 64 GPUs where optimal
configuration scales to 512+.

**System Complexity:** Device page faults introduce new failure modes.
What happens when a device page faults but the CPU is busy? When a page
is being written by a device and simultaneously unmapped by the CPU?
When TLB invalidation fails to reach a device? Production systems must
handle these scenarios gracefully.

### Relationship to Previous Chapters

This chapter builds directly on the foundations established earlier:

Chapter 3 examined page table structures---the PGD/P4D/PUD/PMD/PTE
hierarchy that CPUs walk. Now we see devices walking these same
structures via IOMMU hardware. The formats are identical (on x86-64,
IOMMU page tables use the same layout as CPU page tables), but the
access patterns and performance characteristics differ dramatically.

Chapter 4 explored the TLB and showed how caching translations
eliminates expensive page table walks. We now extend this to device-side
TLBs---the IOTLB in the IOMMU and the ATC in the device itself. The
principles are the same, but the cache sizes, associativity, and
invalidation protocols all differ.

Chapter 5 briefly introduced IOMMU for GPU memory access. We now dive
much deeper, covering the full protocol stack from device identification
through page fault handling, and extending to RDMA, FPGAs, and Smart
NICs.

Chapter 9 optimized CPU page table structures for concurrency and memory
efficiency. Now we face similar challenges with device page tables, but
with additional constraints---devices can\'t execute arbitrary code to
handle complex cases, and cross-device synchronization requires
microsecond-latency protocols.

Let\'s begin by examining the IOMMU itself---the central piece of
hardware that enables device virtual memory.

------------------------------------------------------------------------

## 10.2 IOMMU Architecture Deep Dive

The Input-Output Memory Management Unit sits between devices and system
memory, intercepting every DMA transaction and translating virtual
addresses to physical addresses. Unlike the CPU MMU which is optimized
for the instruction stream of a single core, the IOMMU must handle
memory accesses from dozens of independent devices
simultaneously---network cards, GPUs, storage controllers, and more.
This fundamental difference shapes its architecture.

### The Core Challenge: Per-Device Isolation

Consider a server with 20 PCIe devices. Each device might belong to a
different process or even a different virtual machine. Without
isolation, any device could read or write any physical memory:

    Without IOMMU:
      GPU in VM1 issues DMA to 0x1000_0000 (physical address)
      Hardware completes transaction - no checking
      
      Problem: If that physical address belongs to VM2, VM1 just read VM2's memory!
      Security violation - game over

The IOMMU solves this by maintaining separate page tables for each
device. When a device issues a DMA request, the IOMMU:

1.  Identifies the device (using its PCIe Bus:Device:Function
    identifier)
2.  Looks up that device\'s page table
3.  Translates the virtual address using that page table
4.  Allows or denies the access based on permissions

This provides the same isolation for devices that the CPU MMU provides
for processes.

### Intel VT-d Architecture

Intel\'s Virtualization Technology for Directed I/O (VT-d) is the most
widely deployed IOMMU architecture. Understanding its internals reveals
the trade-offs inherent in device memory translation.

#### Device Identification: BDF

PCIe devices are identified by a 16-bit address composed of three
fields:

    Bus (8 bits) : Device (5 bits) : Function (3 bits)

    Example: 0000:03:00.1
      Domain: 0000 (usually 0 for single-host systems)
      Bus:    03
      Device: 00
      Func:   1

    Addressing:
      256 buses × 32 devices × 8 functions = 65,536 possible devices

This BDF address is how the IOMMU identifies which device is requesting
a translation. Every DMA transaction carries its source BDF.

#### Root and Context Tables

VT-d uses a two-level lookup structure to map BDFs to page tables:

    Root Table (single 4KB page):
      256 entries (one per bus number)
      Each entry points to a Context Table
      
    Context Table (4KB page per bus):
      256 entries (one per device:function combination)
      Each entry points to a page table base

The lookup flow:

``` {.sourceCode .c}
// Simplified VT-d address translation
paddr_t vtd_translate(uint16_t bdf, vaddr_t vaddr) {
    uint8_t bus = (bdf >> 8) & 0xFF;
    uint8_t devfn = bdf & 0xFF;  // device:function
    
    // Step 1: Index root table by bus number
    root_entry_t *root = root_table_base[bus];
    if (!root->present)
        return TRANSLATION_FAULT;
        
    // Step 2: Index context table by device:function
    context_table_t *ctx_table = root->context_table_ptr;
    context_entry_t *ctx = &ctx_table[devfn];
    if (!ctx->present)
        return TRANSLATION_FAULT;
        
    // Step 3: Walk page tables (same as CPU page walk)
    paddr_t paddr = walk_page_tables(ctx->page_table_base, vaddr);
    
    return paddr;
}
```

Each context entry is 128 bits containing:

``` {.sourceCode .c}
struct context_entry {
    uint64_t lo;
    uint64_t hi;
};

// Lower 64 bits:
//   [0]:     Present
//   [1]:     Fault Processing Disable  
//   [3:2]:   Translation Type (00=legacy, 10=4-level, 11=5-level)
//   [11:4]:  Reserved
//   [63:12]: Second Level Page Table Pointer (SLPTPTR)
//
// Upper 64 bits:
//   [2:0]:   Address Width (001=39bit, 010=48bit, etc.)
//   [7:3]:   Available
//   [22:8]:  Domain Identifier
//   [63:23]: Reserved
```

The key field is SLPTPTR---this points to the PGD (top-level page table)
for this device, exactly like the CR3 register does for CPU page tables.

#### Page Table Format

Intel made a critical design decision: VT-d page tables use exactly the
same format as CPU page tables. For a device configured with 4-level
paging:

    Device Virtual Address (48 bits):
      [47:39] → PML4 index (9 bits, 512 entries)
      [38:30] → PDPT index (9 bits, 512 entries)  
      [29:21] → PD index (9 bits, 512 entries)
      [20:12] → PT index (9 bits, 512 entries)
      [11:0]  → Offset within page (4KB)

    Page table entry format:
      Identical to CPU PTEs:
      [0]:     Present
      [1]:     Read/Write
      [2]:     User/Supervisor (ignored by VT-d)
      [6]:     Dirty
      [7]:     PS (Page Size) - for huge pages
      [63:12]: Physical frame number

This compatibility is powerful. The CPU and devices can literally share
the same page tables. A process can map memory once, and both the CPU
and a device can access it through the same translations. This is the
foundation of modern Unified Virtual Addressing.

However, the page table walk cost is substantial. Unlike CPU page table
walks which hit L1/L2/L3 caches, IOMMU page table walks must access main
memory:

    IOMMU page table walk cost:
      Read root table entry:    ~100 ns (DRAM access)
      Read context table entry: ~100 ns (DRAM access)  
      Read PML4 entry:         ~100 ns (DRAM access)
      Read PDPT entry:         ~100 ns (DRAM access)
      Read PD entry:           ~100 ns (DRAM access)
      Read PT entry:           ~100 ns (DRAM access)
      
    Total: ~600 ns per translation miss

    Compare to CPU TLB miss:
      PWC (Page Walk Cache) hit: ~10 ns
      Full walk: ~100 ns
      
    IOMMU is 6× slower!

This latency makes the IOTLB critical.

\[Content continues...\] \#### IOTLB Structure and Behavior

The IOTLB caches recent translations, avoiding expensive page table
walks:

    Intel VT-d IOTLB (typical high-end configuration):
      Entries: 256-512 (shared across ALL devices)
      Associativity: Fully associative or 4-way set-associative
      Entry format:
        Device ID (16 bits - BDF)
        Virtual Page Number (36 bits for 48-bit addressing)
        Domain ID (16 bits)
        Physical Frame Number (40 bits)
        Permissions (R/W/X)
        Page Size (4KB/2MB/1GB)

The critical constraint that determines IOTLB effectiveness is the
shared nature of the cache. Unlike CPU TLBs which are typically per-core
(Intel: 64 L1 DTLB entries per core, 1536 L2 TLB entries shared by a few
cores), the IOTLB serves all devices connected to a particular IOMMU. On
modern server motherboards, a single IOMMU might serve dozens of PCIe
devices.

This sharing creates contention that doesn\'t exist in CPU TLBs. When a
GPU and a network card both need translations, they compete for the same
512 IOTLB entries. If the GPU has a 2 GB working set and the NIC has a 1
GB working set, they need 786,432 and 262,144 translations respectively
(with 4 KB pages) to avoid misses. But they share 512 entries---a
capacity mismatch of 2,000× to 500,000×.

The IOMMU hardware typically uses a replacement policy like LRU (Least
Recently Used) or a variant to decide which entries to evict when the
IOTLB fills. But with such severe capacity underprovisioning, the
replacement policy barely matters. The IOTLB thrashes---entries are
constantly evicted before they can be reused, making the cache
effectively useless.

The critical constraint: the IOTLB is shared by all devices on this
IOMMU. A server might have:

    1× IOMMU serving:
      2× 100 Gbps NICs
      4× NVMe SSDs  
      2× GPUs
      1× FPGA
      Miscellaneous (USB, SATA, etc.)
      
    Total: 10+ active devices sharing 256-512 IOTLB entries

    Per-device average: 25-50 entries

For a high-bandwidth device like a 100 Gbps NIC processing packets
across a 1 GB working set:

    Working set: 1 GB
    Page size: 4 KB
    Pages: 262,144

    IOTLB capacity: 50 entries (device's share)
    IOTLB coverage: 50 × 4KB = 200 KB

    Hit rate: 200 KB / 1 GB = 0.019% (!)

This is catastrophically bad. Nearly every transaction will miss the
IOTLB and require a 600 ns page table walk.

**Optimization 1: Huge Pages**

Using 2 MB pages dramatically improves IOTLB coverage:

    Working set: 1 GB
    Page size: 2 MB
    Pages: 512

    IOTLB capacity: 50 entries
    IOTLB coverage: 50 × 2MB = 100 MB

    Hit rate: 100 MB / 1 GB = 10%

Still not great, but 500× better than with 4 KB pages. With 1 GB pages:

    Working set: 1 GB
    Page size: 1 GB
    Pages: 1

    IOTLB capacity: 50 entries
    IOTLB coverage: 50 GB

    Hit rate: 100% (entire working set cached!)

This is why huge pages are critical for IOMMU performance---they
multiply IOTLB effectiveness.

**Optimization 2: IOMMU Passthrough**

For trusted devices, bypass the IOMMU entirely:

``` {.sourceCode .c}
// Configure device for passthrough (no translation)
struct context_entry *ctx = &context_table[devfn];
ctx->translation_type = 0b00;  // Legacy mode (no translation)
ctx->present = 1;

// Device now uses physical addresses directly
// Zero IOMMU overhead
// But: Security isolation lost
```

Passthrough is appropriate for: - Devices in single-tenant systems (no
isolation needed) - Devices with hardware memory protection (e.g., some
SR-IOV NICs) - Performance-critical devices where IOMMU overhead is
unacceptable

But it\'s inappropriate for multi-tenant cloud environments where
isolation is mandatory.

#### IOTLB Invalidation

When page tables change, the IOMMU must invalidate cached translations.
VT-d provides three invalidation granularities:

``` {.sourceCode .c}
// Global invalidation (flush entire IOTLB)
void iotlb_global_invalidate(iommu_t *iommu) {
    write_iommu_reg(iommu, IOTLB_REG_GLOBAL_INVALIDATE, 1);
    wait_for_completion(iommu);
}

// Domain-selective (flush one domain's entries)  
void iotlb_domain_invalidate(iommu_t *iommu, uint16_t domain_id) {
    write_iommu_reg(iommu, IOTLB_REG_DOMAIN_ID, domain_id);
    write_iommu_reg(iommu, IOTLB_REG_DOMAIN_INVALIDATE, 1);
    wait_for_completion(iommu);
}

// Page-selective (flush specific virtual address)
void iotlb_page_invalidate(iommu_t *iommu, vaddr_t addr, 
                           uint16_t domain_id) {
    write_iommu_reg(iommu, IOTLB_REG_INVAL_ADDR, addr);
    write_iommu_reg(iommu, IOTLB_REG_INVAL_DOMAIN, domain_id);
    write_iommu_reg(iommu, IOTLB_REG_PAGE_INVALIDATE, 1);
    wait_for_completion(iommu);
}
```

The wait_for_completion() is critical---the IOMMU operates
asynchronously, and the invalidation may not complete immediately. The
kernel must wait before considering the TLB flushed.

Latency measurements:

    IOTLB global flush: ~5-10 µs
    IOTLB domain flush: ~2-5 µs
    IOTLB page flush:   ~1-2 µs

    Compare to CPU TLB flush:
    Single core: ~100 ns
    64 cores (IPI): ~8 µs

    IOTLB flush is comparable to multi-core CPU TLB flush!

### IOMMU Page Fault Handling

Modern IOMMUs support page fault reporting via the Page Request
Interface (PRI), part of the PCIe spec. When a device accesses an
unmapped page:

    Device DMA timeline with page fault:
      T0:   Device DMAs to virtual address 0x7fff_0000
      T1:   IOMMU translates: lookup context, walk page tables
      T2:   PTE not present → page fault
      T3:   IOMMU generates Page Request
      T4:   CPU interrupt handler receives Page Request
      T5:   CPU allocates page (or swaps in from disk)
      T6:   CPU updates page table entry
      T7:   CPU invalidates IOTLB  
      T8:   CPU sends Page Response to IOMMU
      T9:   IOMMU signals device to retry
      T10:  Device retries DMA
      T11:  Translation succeeds, DMA completes
      
    Total latency: 10-500 µs (depending on whether disk I/O needed)

Compare this to a CPU page fault which typically completes in 1-5 µs for
minor faults (page allocated from RAM) or 5-20 ms for major faults (page
read from disk). The device page fault is inherently slower due to the
roundtrip through the PCIe link and IOMMU hardware.

**Implementation complexity:**

Not all devices support page faults. The device must:

1.  Implement PRI protocol (optional part of PCIe spec)
2.  Handle asynchronous completion (DMA might fail, need retry later)
3.  Maintain request queues (so other requests can proceed while one is
    faulting)
4.  Implement timeout/recovery (what if page fault never completes?)

These requirements make device page faulting complex and somewhat rare.
As of 2024, mainstream devices that support PRI include:

- High-end NICs (Mellanox ConnectX-5+, Intel E810)
- Enterprise GPUs (NVIDIA A100/H100 with some limitations)
- Some NVMe controllers (Intel Optane, Samsung Z-NAND)

Consumer devices typically don\'t implement PRI due to cost and
complexity.

### Performance Case Study: NVMe with IOMMU

Let\'s examine real-world NVMe storage performance with various IOMMU
configurations.

**Setup:** - Intel Xeon Gold 6248R (24 cores @ 3.0 GHz) - Intel Optane
P5800X (1.6 TB NVMe SSD, 1.5M IOPS capable) - Workload: Random 4KB
reads - Block: 256 outstanding I/Os

**Configuration A: IOMMU Disabled**

``` {.sourceCode .bash}
# Boot with iommu=off
dmesg | grep -i iommu
# IOMMU: disabled

# Benchmark
fio --name=test --ioengine=libaio --direct=1 --bs=4k \
    --rw=randread --numjobs=1 --iodepth=256
```

Results:

    IOPS: 1.47 million
    Latency avg: 174 µs
    Latency p99: 290 µs
    CPU usage: 18%

**Configuration B: IOMMU Enabled, 4KB Pages**

``` {.sourceCode .bash}
# Boot with intel_iommu=on
# Default page size: 4KB

fio (same command)
```

Results:

    IOPS: 780,000 (47% reduction!)
    Latency avg: 328 µs (+88%)
    Latency p99: 512 µs (+76%)
    CPU usage: 28% (+10% absolute)
    IOTLB miss rate: 89% (from perf)

The IOMMU translation overhead is devastating. For every I/O, the IOMMU
must translate the buffer address, missing the IOTLB 89% of the time and
walking page tables.

**Configuration C: IOMMU Enabled, 2MB Pages**

``` {.sourceCode .bash}
# Enable huge pages for buffer allocation
echo always > /sys/kernel/mm/transparent_hugepage/enabled

fio (same command)
```

Results:

    IOPS: 1.38 million (94% of baseline)
    Latency avg: 186 µs (+7% vs baseline)
    Latency p99: 310 µs (+7% vs baseline)
    CPU usage: 19%
    IOTLB miss rate: 11%

Huge pages reduce IOTLB misses from 89% to 11%, recovering most of the
performance. The remaining 6% gap comes from the few IOTLB misses that
still occur and the additional latency of the IOMMU hardware being in
the path.

**Lessons:**

1.  IOMMU overhead is real---up to 50% for high-IOPS devices
2.  Huge pages are mandatory for acceptable performance
3.  For trusted environments, passthrough (iommu=off) maximizes
    performance
4.  For multi-tenant cloud, IOMMU+huge pages provides security with
    acceptable overhead

### AMD IOMMU (AMD-Vi) Differences

AMD\'s IOMMU architecture differs in structure but achieves the same
goals:

**Device Table:** Instead of root + context tables, AMD uses a single
large Device Table:

    Device Table: up to 16 MB (256K entries × 64 bytes)
      Indexed directly by BDF (no two-level lookup)
      
    Device Table Entry (64 bytes):
      [0]:     Valid
      [1]:     Translation Valid
      [4:2]:   Paging Mode (number of page table levels)
      [11:9]:  Domain ID
      [51:12]: Page Table Root Pointer
      ... additional fields for interrupt remapping, etc.
      
    Advantage: O(1) lookup (vs Intel's two-level)
    Disadvantage: Wastes memory (must allocate 16MB even if only using a few devices)

**Per-Device IOTLBs:** AMD provides dedicated IOTLB entries per device:

    Each device gets:
      16-64 dedicated IOTLB entries (model-dependent)
      
    vs Intel:
      All devices share 256-512 entries
      
    Advantage: No inter-device IOTLB thrashing
    Disadvantage: Can't dynamically allocate IOTLB capacity to busiest devices

In practice, both approaches work well. Intel\'s shared IOTLB is more
flexible (devices with high traffic naturally get more entries), while
AMD\'s per-device IOTLB provides more predictable performance.

### ARM SMMU (System Memory Management Unit)

ARM servers use the System MMU (SMMU), particularly SMMUv3 in recent
designs:

**Stream Tables:** Map device identifiers (StreamIDs) to page tables:

    Stream Table (configurable size):
      Linear (up to 64K entries) or 2-level (larger)
      Each entry → Stream Table Entry (STE)
      
    Stream Table Entry → Context Descriptor
      Stage 1 Translation: Device VA → IPA (Intermediate Physical Address)
      Stage 2 Translation: IPA → PA (Physical Address)
      
    Two-stage translation enables nested virtualization:
      Guest OS controls Stage 1
      Hypervisor controls Stage 2

The two-stage design is elegant for virtualization:

    Example: GPU in VM accessing guest virtual memory

    Stage 1 (controlled by guest OS):
      Device VA 0x7fff_0000 → Guest Physical 0x4000_0000
      
    Stage 2 (controlled by hypervisor):
      Guest Physical 0x4000_0000 → Host Physical 0x8234_5000
      
    Combined:
      Device VA 0x7fff_0000 → Host Physical 0x8234_5000

This allows the guest OS to manage its devices\' virtual memory without
hypervisor involvement, while the hypervisor maintains isolation between
guests.

**TLB Hierarchy:**

    Micro-TLB: 8-32 entries per device interface
      Fast lookup for recent translations
      Per-stage (Stage 1 TLB, Stage 2 TLB)
      
    Main TLB: 256-2048 entries (shared)
      Larger capacity for working set
      Combined Stage 1+2 entries
      
    Walk Cache: Caches intermediate page table levels
      Similar to Intel's PWC (Page Walk Cache)
      Reduces average page walk latency

ARM\'s two-stage translation adds overhead when both stages are enabled,
but for non-virtualized workloads, Stage 2 can be bypassed:

    Non-virtualized mode:
      Stage 1 only: Device VA → PA directly
      Latency: Similar to Intel/AMD single-stage
      
    Virtualized mode:
      Stage 1 + Stage 2: Device VA → IPA → PA
      Latency: ~50% higher (two translation walks)

------------------------------------------------------------------------

## 10.3 PCIe ATS and Address Translation Services

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
<defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
<marker id="a" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
<marker id="ao" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
<marker id="ag" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker></defs>
<text x="450" y="26" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Figure 10.1 - PCIe ATS Architecture and RDMA Memory Registration</text>
<rect x="30" y="40" width="400" height="295" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
<rect x="30" y="40" width="400" height="28" rx="6" style="fill:#1565C0" />
<text x="230" y="59" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">PCIe Address Translation Services (ATS)</text>
<rect x="48" y="76" width="150" height="50" rx="5" filter="url(#sh)" style="fill:#1565C0" />
<text x="123" y="97" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">NIC / GPU</text>
<text x="123" y="114" style="fill:white; font-size:12; text-anchor:middle">ATS-capable device</text>
<rect x="48" y="76" width="150" height="28" rx="3" style="fill:#E65100; fill-opacity:0.7" />
<text x="123" y="94" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">Device ATCache (ATC)</text>
<rect x="283" y="76" width="130" height="50" rx="5" filter="url(#sh)" style="fill:#00796B" />
<text x="348" y="97" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">IOMMU</text>
<text x="348" y="114" style="fill:white; font-size:12; text-anchor:middle">Translation agent</text>
<line x1="198" y1="100" x2="283" y2="100" marker-end="url(#a)" style="stroke:#1565C0; stroke-width:2"></line>
<text x="240" y="94" style="fill:#1565C0; font-size:11; text-anchor:middle">ATS Req (VA)</text>
<line x1="283" y1="116" x2="198" y2="116" marker-end="url(#ag)" style="stroke:#00796B; stroke-width:2"></line>
<text x="240" y="132" style="fill:#00796B; font-size:11; text-anchor:middle">ATS Resp (PA)</text>
<text x="230" y="158" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">ATS Flow: Device caches own translations</text>
<rect x="48" y="166" width="365" height="22" rx="3" style="fill:#1565C0" />
<text x="230" y="182" style="fill:white; font-size:12; text-anchor:middle">1. Device sends ATS Request with VA to IOMMU</text>
<rect x="48" y="192" width="365" height="22" rx="3" style="fill:#00796B" />
<text x="230" y="208" style="fill:white; font-size:12; text-anchor:middle">2. IOMMU walks I/O page tables, returns PA + perms</text>
<rect x="48" y="218" width="365" height="22" rx="3" style="fill:#E65100" />
<text x="230" y="234" style="fill:white; font-size:12; text-anchor:middle">3. Device caches PA in ATC (device-side TLB)</text>
<rect x="48" y="244" width="365" height="22" rx="3" style="fill:#9E9E9E" />
<text x="230" y="260" style="fill:white; font-size:12; text-anchor:middle">4. Subsequent DMAs use cached PA (bypass IOMMU)</text>
<text x="230" y="286" style="fill:#212121; font-size:13; text-anchor:middle">Benefit: Eliminates per-DMA IOMMU lookup latency</text>
<text x="230" y="305" style="fill:#616161; font-size:12; text-anchor:middle">ATC invalidated by IOMMU via PCIe INVAL_REQ message</text>
<rect x="460" y="40" width="410" height="295" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
<rect x="460" y="40" width="410" height="28" rx="6" style="fill:#1565C0" />
<text x="665" y="59" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">RDMA Memory Registration</text>
<text x="665" y="88" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">ibv_reg_mr(): Pin and translate a VA region</text>
<rect x="475" y="96" width="380" height="50" rx="4" style="fill:#1565C0" />
<text x="665" y="118" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">Application Buffer (Virtual Address space)</text>
<text x="665" y="136" style="fill:white; font-size:12; text-anchor:middle">VA: 0x7f8000000000, len: 64 MB</text>
<line x1="665" y1="146" x2="665" y2="166" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2"></line>
<text x="775" y="160" style="fill:#E65100; font-size:12">ibv_reg_mr()</text>
<rect x="475" y="166" width="380" height="70" rx="4" style="fill:#E65100; stroke:#E65100; fill-opacity:0.2; stroke-width:1.5" />
<text x="665" y="186" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Kernel: Pin Pages + Build MR</text>
<text x="665" y="204" style="fill:#212121; font-size:12; text-anchor:middle">1. Walk page tables: translate all VAs to PAs</text>
<text x="665" y="220" style="fill:#212121; font-size:12; text-anchor:middle">2. Pin pages (prevent eviction)</text>
<text x="665" y="236" style="fill:#212121; font-size:12; text-anchor:middle">3. Program IOMMU with VA-&gt;PA mapping</text>
<line x1="665" y1="236" x2="665" y2="256" marker-end="url(#ag)" style="stroke:#00796B; stroke-width:2"></line>
<rect x="475" y="256" width="380" height="50" rx="4" style="fill:#00796B" />
<text x="665" y="278" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">Memory Region (MR): lkey + rkey handles</text>
<text x="665" y="296" style="fill:white; font-size:12; text-anchor:middle">NIC can DMA directly using rkey token</text>
<text x="665" y="320" style="fill:#212121; font-size:13; text-anchor:middle">Cost: ibv_reg_mr is expensive (O(pages))</text>
<text x="665" y="336" style="fill:#616161; font-size:12; text-anchor:middle">MR cache: re-use pinned registrations across ops</text>
<rect x="30" y="358" width="840" height="178" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
<rect x="30" y="358" width="840" height="28" rx="6" style="fill:#00796B" />
<text x="450" y="377" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">SmartNIC / DPU Memory Architecture</text>
<text x="220" y="410" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Traditional NIC</text>
<text x="220" y="428" style="fill:#212121; font-size:13; text-anchor:middle">DMA to host RAM via PCIe</text>
<text x="220" y="446" style="fill:#212121; font-size:13; text-anchor:middle">Host CPU processes packets</text>
<text x="220" y="464" style="fill:#616161; font-size:12; text-anchor:middle">Host interrupt per packet</text>
<text x="220" y="482" style="fill:#616161; font-size:12; text-anchor:middle">PCIe bandwidth bottleneck</text>
<text x="220" y="500" style="fill:#616161; font-size:12; text-anchor:middle">~40 Gbps practical limit</text>
<line x1="440" y1="390" x2="440" y2="515" style="stroke:#9E9E9E; stroke-width:1"></line>
<text x="665" y="410" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">SmartNIC / DPU</text>
<text x="665" y="428" style="fill:#212121; font-size:13; text-anchor:middle">ARM cores on NIC offload packet processing</text>
<text x="665" y="446" style="fill:#212121; font-size:13; text-anchor:middle">Own MMU, own page tables, own DRAM</text>
<text x="665" y="464" style="fill:#616161; font-size:12; text-anchor:middle">PCIe peer-to-peer DMA to GPU</text>
<text x="665" y="482" style="fill:#00796B; font-size:12; text-anchor:middle">Zero-copy: NIC DMA direct to GPU VRAM</text>
<text x="665" y="500" style="fill:#616161; font-size:12; text-anchor:middle">BlueField-3: 400 Gbps, 16 ARM cores</text>
</svg>
</div>
<figcaption><strong>Figure 10.1:</strong> PCIe ATS and RDMA memory
registration. ATS lets ATS-capable devices (NICs, GPUs) cache their own
VA→PA translations in a device-side Address Translation Cache (ATC),
eliminating per-DMA IOMMU lookups. RDMA memory registration (ibv_reg_mr)
pins pages and programs the IOMMU once; subsequent DMA operations use
the cached lkey/rkey without OS involvement. SmartNIC/DPU architectures
add ARM cores on the NIC for packet offload and zero-copy GPU-direct
paths.</figcaption>
</figure>

The IOMMU provides translation, but it\'s fundamentally a bottleneck.
Every device access must go through the IOMMU\'s IOTLB, and with only
256-512 entries shared across all devices, misses are frequent. Address
Translation Services (ATS) solve this by moving the translation cache
from the IOMMU into the device itself.

### The ATS Innovation

ATS, defined in the PCIe specification, allows a device to request
translations from the IOMMU and cache them locally in an Address
Translation Cache (ATC):

    Traditional (pre-ATS):
      Every DMA:
        Device → IOMMU → Check IOTLB → Maybe walk page tables → Memory
      
    With ATS:
      First DMA to address:
        Device → Check ATC (miss) → Send Translation Request to IOMMU
        IOMMU → Walk page tables → Return translation
        Device → Cache in ATC → Complete DMA
        
      Subsequent DMAs to same address:
        Device → Check ATC (hit) → Directly access memory
        IOMMU not involved!

The win is substantial because it transforms the translation
architecture from centralized to distributed. Instead of all translation
traffic flowing through a bottleneck (the IOMMU), each device handles
its own translations after the first cache miss. This is analogous to
the difference between a single server handling all requests versus a
distributed cache where clients cache responses locally.

Consider the bandwidth saved. In the traditional IOMMU model, a 100 Gbps
NIC generating 1 billion transactions per second (small packets, worst
case) would send 1 billion translation requests to the IOMMU. Even if we
optimistically assume 50% IOTLB hit rate, that\'s still 500 million page
table walks per second. Each walk requires reading six page table levels
(root, context, PML4, PDPT, PD, PT) from memory = 3 billion memory reads
per second just for translations. At 64 bytes per cache line, that\'s
192 GB/s of memory bandwidth consumed purely by page table walks. This
is more bandwidth than many systems have available in total!

With ATS, the same NIC maintains its own 1024-entry ATC. After a brief
warmup period where the working set loads into the ATC, the hit rate
might reach 95% for a well-behaved workload. Now only 50 million
transactions per second miss the ATC and require IOMMU involvement. This
reduces the IOMMU\'s load by 10× and memory bandwidth for translations
by 10×. The NIC\'s local ATC lookups happen in its own logic at
negligible cost.

An ATC hit completes in the device\'s local logic---typically 10-50
cycles depending on the implementation. This is comparable to a CPU TLB
hit (1-5 cycles). Compare this to an IOTLB lookup which requires a PCIe
round-trip (300-500 cycles for the request/response) plus the IOMMU
lookup time (another 50-100 cycles for an IOTLB hit, 600+ cycles for a
miss and walk). Even in the best case (IOTLB hit), ATS is 10× faster. In
the worst case (IOTLB miss), ATS is 50× faster.

The win is substantial. An ATC hit completes in the device\'s local
logic (\~10-50 cycles), while an IOTLB lookup takes a full PCIe
roundtrip (\~300-500 cycles for the request/response, plus the IOMMU
lookup time).

### ATS Protocol Messages

ATS operates via PCIe Transaction Layer Packets (TLPs). The device and
IOMMU exchange three message types:

**1. Translation Request**

When the device\'s ATC misses, it sends a Translation Request:

    Translation Request TLP:
      Type: ATS Translation Request
      Requester ID: Device BDF
      Address: Virtual address to translate (aligned to 4KB)
      Length: Number of bytes (for multi-page requests)
      Attributes:
        NW (No Write): 1 if read-only translation requested
        U (Untranslated): Always 1 (this is a request)

The IOMMU receives this, performs the translation (potentially walking
page tables), and responds.

**2. Translation Completion**

The IOMMU responds with a Translation Completion:

    Translation Completion TLP:
      Type: ATS Translation Completion
      Completer ID: IOMMU identifier
      Tag: Matches the request tag
      Status: Success / Unsupported Request / Translation Fault
      Data (if success):
        Translated Address: Physical address
        Permissions: R (Read), W (Write), Pr (Privileged)
        N (PASID): Process Address Space ID (if applicable)
        U (Untranslated): 0 (this is translated)

The device caches this translation in its ATC and completes the original
DMA.

**3. Invalidation Request**

When the OS modifies page tables, it must invalidate stale ATC entries.
The IOMMU sends Invalidation Requests to devices:

    Invalidation Request TLP:
      Type: ATS Invalidation Request
      Target: Device BDF
      Address: Virtual address to invalidate
      PASID: Process ID (if applicable)
      Granularity:
        Global: Flush entire ATC
        PASID: Flush all entries for this process
        Page: Flush specific page
        Range: Flush address range

The device must flush matching ATC entries and respond with Invalidation
Completion:

    Invalidation Completion TLP:
      Type: ATS Invalidation Completion
      Completer ID: Device BDF

Only after receiving all completion responses can the OS consider the
invalidation complete.

### PASID: Process Address Space ID

A critical extension to ATS is PASID---Process Address Space ID. This
allows a single device to access multiple independent address spaces
simultaneously.

**The Problem Without PASID:**

    Traditional (one address space per device):
      Device → Single page table
      All DMA uses same virtual address space
      
    Problem:
      Can't have different processes sharing the device safely
      Each process needs own page table for isolation

**PASID Solution:**

    With PASID:
      Device → Multiple page tables (one per PASID)
      PASID is a 20-bit identifier (up to 1 million address spaces)
      
    Example:
      Process A: PASID 1000
      Process B: PASID 2000
      Process C: PASID 3000
      
    Device can DMA to all three simultaneously:
      DMA with PASID 1000 → Uses Process A's page tables
      DMA with PASID 2000 → Uses Process B's page tables
      DMA with PASID 3000 → Uses Process C's page tables

The ATC entries now include the PASID:

``` {.sourceCode .c}
struct atc_entry {
    vaddr_t virtual_address;
    paddr_t physical_address;
    uint32_t pasid;           // Process ID
    uint8_t permissions;      // R/W/X
    bool valid;
};

// ATC lookup with PASID
atc_entry_t *atc_lookup(vaddr_t vaddr, uint32_t pasid) {
    for (each entry in ATC) {
        if (entry->virtual_address == (vaddr & PAGE_MASK) &&
            entry->pasid == pasid &&
            entry->valid) {
            return entry;
        }
    }
    return NULL;  // Miss
}
```

**Use Case: SR-IOV NIC with PASID**

Consider a single 100 Gbps NIC with SR-IOV, creating 8 Virtual Functions
(VFs):

    Physical Function (PF):
      Managed by host OS/hypervisor
      
    Virtual Functions (VFs):
      VF0 → Container A (PASID 100)
      VF1 → Container B (PASID 101)
      VF2 → Container C (PASID 102)
      VF3 → Container D (PASID 103)
      VF4 → Container E (PASID 104)
      VF5 → Container F (PASID 105)
      VF6 → Container G (PASID 106)
      VF7 → Container H (PASID 107)

Each VF can DMA into its container\'s private virtual address space:

    Container A sends packet:
      VF0 reads buffer from virtual address 0x7fff_0000 with PASID 100
      IOMMU translates using Container A's page tables
      Physical address: 0x1234_5000
      VF0 DMAs packet from 0x1234_5000
      
    Container B sends packet (simultaneously):
      VF1 reads buffer from virtual address 0x7fff_0000 with PASID 101
      IOMMU translates using Container B's page tables
      Physical address: 0x5678_9000 (different!)
      VF1 DMAs packet from 0x5678_9000
      
    Same virtual address, different physical addresses, complete isolation!

### PRI: Page Request Interface

PASID enables multi-process sharing, but there\'s still a problem: what
if a device accesses an unmapped page? Traditional devices would simply
fail the DMA. PRI (Page Request Interface) allows devices to request
that the OS handle the page fault.

**PRI Protocol Flow:**

    Device attempts DMA to unmapped virtual address:
      T0: Device checks ATC → miss
      T1: Device sends ATS Translation Request to IOMMU
      T2: IOMMU walks page tables → PTE not present
      T3: IOMMU sends Page Request Message to root complex
      T4: Root complex interrupts CPU
      T5: CPU page fault handler allocates/swaps in page
      T6: CPU updates page table entry
      T7: CPU invalidates IOTLB/ATC for this address
      T8: CPU sends Page Response Message
      T9: IOMMU forwards response to device
      T10: Device retries Translation Request
      T11: IOMMU walks page tables → success
      T12: Device caches in ATC, completes DMA
      
    Total: 50-500 µs (vs 1-2 µs for normal DMA)

**Page Request Message Format:**

    Page Request:
      Requester ID: Device BDF
      PASID: Process address space ID
      Address: Faulting virtual address
      Type: Read or Write fault
      Private Data: Device-specific context (to match response)
      Last Request: Is this the last in a group?
      PRG Index: Page Request Group index

**Page Response Message:**

    Page Response:
      Responder ID: Root complex
      PASID: Process address space ID
      Private Data: Echo from request
      Response Code:
        Success: Page allocated, retry
        Invalid Request: PASID invalid, fail permanently
        Response Failure: Could not handle, retry later

**Device Implementation Requirements:**

Supporting PRI requires sophisticated device logic:

``` {.sourceCode .c}
// Simplified device PRI state machine
enum pri_state {
    PRI_IDLE,
    PRI_REQUEST_SENT,
    PRI_WAITING_RESPONSE,
    PRI_RETRY
};

struct dma_request {
    vaddr_t address;
    uint32_t pasid;
    size_t length;
    enum pri_state state;
    uint64_t timeout;
};

void handle_dma_request(dma_request_t *req) {
    switch (req->state) {
    case PRI_IDLE:
        // Check ATC
        atc_entry_t *entry = atc_lookup(req->address, req->pasid);
        if (entry) {
            // ATC hit - complete DMA immediately
            complete_dma(req, entry->physical_address);
            return;
        }
        
        // ATC miss - request translation
        send_ats_translation_request(req);
        req->state = PRI_REQUEST_SENT;
        req->timeout = current_time() + ATS_TIMEOUT;
        break;
        
    case PRI_REQUEST_SENT:
        // Waiting for translation completion or page request
        if (current_time() > req->timeout) {
            // Timeout - fail the DMA
            fail_dma(req, TIMEOUT);
        }
        break;
        
    case PRI_WAITING_RESPONSE:
        // Waiting for page response from OS
        if (current_time() > req->timeout) {
            // Timeout - retry or fail
            if (req->retries++ < MAX_RETRIES) {
                req->state = PRI_RETRY;
            } else {
                fail_dma(req, PAGE_FAULT_TIMEOUT);
            }
        }
        break;
        
    case PRI_RETRY:
        // Retry the translation request
        send_ats_translation_request(req);
        req->state = PRI_REQUEST_SENT;
        req->timeout = current_time() + ATS_TIMEOUT;
        break;
    }
}
```

The complexity is significant. The device must: - Queue pending requests
(can\'t block) - Handle timeouts (page faults might take milliseconds) -
Implement retry logic (transient failures) - Coordinate with other
pending DMAs (ordering)

This is why PRI support is uncommon in consumer devices.

\[Content continues in next section...\] \### Performance Analysis: RDMA
with ATS

A production deployment at a financial services firm provides concrete
data on ATS effectiveness.

**Setup:** - Mellanox ConnectX-5 100 Gbps NIC (ATS capable) - Workload:
RDMA Write throughput test - Buffer size: 8 GB (spread across many
connections)

**Configuration A: Traditional (Pinned Memory, no IOMMU)**:

    Memory registration time: 180 ms (one-time cost)
    Throughput: 95 Gbps
    Latency: 1.2 µs
    Memory pinned: 8 GB (can't be swapped)

**Configuration B: IOMMU enabled, no ATS (4KB pages)**:

    Setup: Enable IOMMU, disable ATS on NIC
    Throughput: 62 Gbps (35% reduction!)
    Latency: 1.8 µs (+50%)
    IOTLB miss rate: 87%
    Memory: Not pinned (can be swapped)

**Configuration C: IOMMU + ATS (4KB pages)**:

    Setup: Enable both IOMMU and ATS
    Throughput: 78 Gbps (18% reduction from baseline)
    Latency: 1.5 µs (+25%)
    ATC size: 1024 entries
    ATC hit rate: 62%
    Memory: Not pinned

**Configuration D: IOMMU + ATS (2MB pages)**:

    Setup: IOMMU + ATS + huge pages
    Throughput: 91 Gbps (96% of baseline!)
    Latency: 1.3 µs (+8%)
    ATC hit rate: 94%
    Memory: Not pinned, can be swapped

**Lessons learned:** 1. ATS significantly improves IOMMU performance (62
→ 78 Gbps) 2. But huge pages are still critical (78 → 91 Gbps) 3. The
combination nearly eliminates IOMMU overhead 4. Flexibility (non-pinned
memory) with minimal performance cost

------------------------------------------------------------------------

## 10.4 RDMA and Memory Registration

Remote Direct Memory Access (RDMA) promises zero-copy
networking---applications can read and write remote memory directly
without kernel involvement. But RDMA\'s interaction with virtual memory
creates a fundamental tension: RDMA NICs need stable physical addresses,
while virtual memory allows pages to move. Memory registration is how we
resolve this conflict.

### The RDMA Model

Traditional networking involves the kernel at every step:

    Traditional send():
      1. Application calls send(socket, buffer, size)
      2. Kernel copies data from user buffer to kernel buffer
      3. TCP/IP stack processes data
      4. NIC DMAs from kernel buffer
      5. Kernel buffers freed after acknowledgment
      
    Total: 2 data copies (user→kernel, kernel→NIC)
    CPU overhead: High (copy + protocol processing)
    Latency: ~50-100 µs

RDMA eliminates the kernel from the data path:

    RDMA Write:
      1. Application calls ibv_post_send(qp, &wr)
      2. NIC DMAs directly from user buffer
      3. NIC sends data over network
      4. Remote NIC writes directly to remote user buffer
      
    Total: 0 data copies
    CPU overhead: Minimal (just posting work request)
    Latency: ~1-2 µs

The win is enormous---10× lower latency and 80% less CPU usage. But
there\'s a catch: the NIC must know the physical addresses of user
buffers, and those addresses can\'t change while RDMA operations are in
flight.

### Traditional Memory Registration

To enable RDMA, applications must register memory regions with the NIC:

``` {.sourceCode .c}
// Register 1 GB buffer for RDMA
void *buffer = malloc(1GB);

struct ibv_pd *pd = ibv_alloc_pd(context);
struct ibv_mr *mr = ibv_reg_mr(pd, buffer, 1GB, 
                                IBV_ACCESS_LOCAL_WRITE |
                                IBV_ACCESS_REMOTE_WRITE |
                                IBV_ACCESS_REMOTE_READ);

// mr now contains a key (rkey) that remote hosts use to access this buffer
```

Behind the scenes, ibv_reg_mr() performs several expensive operations:

``` {.sourceCode .c}
// Simplified kernel memory registration
int ibv_reg_mr_kernel(void *addr, size_t length, int access) {
    struct page **pages;
    int nr_pages = length / PAGE_SIZE;
    
    // Step 1: Pin all pages (prevent swapping)
    pages = kmalloc(nr_pages * sizeof(struct page *), GFP_KERNEL);
    for (int i = 0; i < nr_pages; i++) {
        // Walk page tables to get physical page
        pages[i] = follow_page(vma, addr + i * PAGE_SIZE);
        // Pin the page (increment refcount, mark as pinned)
        get_page(pages[i]);
        SetPagePinned(pages[i]);
    }
    
    // Step 2: Build translation table for NIC
    dma_addr_t *dma_addrs = build_dma_table(pages, nr_pages);
    
    // Step 3: Program NIC with mapping
    program_nic_translation(mr->key, addr, dma_addrs, nr_pages);
    
    return 0;
}
```

The cost is substantial:

    Registering 1 GB (262,144 pages):
      Pin pages: 262,144 × mlock() = ~80 ms
      Build DMA table: ~20 ms
      Program NIC: ~50 ms
      Total: ~150 ms

    Registering 10 GB: ~1.5 seconds!

For applications that dynamically allocate buffers, this overhead is
prohibitive. A key-value store handling millions of requests per second
can\'t afford 150 ms to register each value buffer.

### The Registration Problem in Practice

Consider a distributed key-value store using RDMA for remote GETs:

``` {.sourceCode .c}
// Client requests value from remote server
int rdma_get(char *key) {
    // Lookup returns location of value in remote server's memory
    remote_addr_t remote = lookup_key(key);
    
    // Allocate local buffer for result
    void *local_buf = malloc(remote.size);
    
    // PROBLEM: Must register buffer before RDMA read
    struct ibv_mr *mr = ibv_reg_mr(pd, local_buf, remote.size, 
                                    IBV_ACCESS_LOCAL_WRITE);
    // This takes 50-200 ms for large values!
    
    // RDMA Read
    rdma_read(local_buf, remote.addr, remote.size, remote.rkey);
    
    // Deregister
    ibv_dereg_mr(mr);  // Also expensive (~10 ms)
    
    return 0;
}
```

For a 1 MB value:

    Registration: 50 ms
    RDMA read: 0.01 ms (1 µs)
    Deregistration: 10 ms
    Total: 60 ms

    Overhead: 6000× the useful work!

This is absurd. The 1 µs RDMA operation is buried under 60 ms of
registration overhead.

### Solution 1: Pre-Registration

The obvious solution: register memory at startup and never deregister:

``` {.sourceCode .c}
// At startup
void *huge_buffer = malloc(100GB);
struct ibv_mr *mr = ibv_reg_mr(pd, huge_buffer, 100GB,
                                IBV_ACCESS_LOCAL_WRITE |
                                IBV_ACCESS_REMOTE_WRITE |
                                IBV_ACCESS_REMOTE_READ);

// At runtime - no registration needed!
void *buf = allocate_from_pool(huge_buffer, size);
rdma_read(buf, remote_addr, size, remote_rkey);
```

This works, but has severe drawbacks:

**Memory overhead:**

    Pre-registered: 100 GB pinned
      - Can't be swapped
      - Can't be relocated (memory fragmentation)
      - Wastes RAM if not fully utilized
      
    Actual usage: 40 GB average
    Wasted: 60 GB pinned but unused

**Inflexibility:**

    What if application needs 120 GB temporarily?
      - Pre-registered pool is 100 GB
      - Must either:
        a) Fail the allocation
        b) Register additional memory (expensive)
        c) Over-allocate at startup (wasteful)

For cloud environments where memory is a premium resource, pinning 100
GB per application is unacceptable.

### Solution 2: Memory Registration Cache

A middle ground: cache memory registrations and reuse them:

``` {.sourceCode .c}
struct mr_cache {
    void *addr;
    size_t length;
    struct ibv_mr *mr;
    int refcount;
    struct list_head lru_list;
    time_t last_used;
};

struct ibv_mr *cached_reg_mr(void *addr, size_t length) {
    struct mr_cache_entry *entry;
    
    // Check cache
    entry = lookup_cache(addr, length);
    if (entry) {
        // Cache hit!
        entry->refcount++;
        entry->last_used = current_time();
        return entry->mr;
    }
    
    // Cache miss - register new
    struct ibv_mr *mr = ibv_reg_mr(pd, addr, length, access_flags);
    
    // Add to cache
    entry = alloc_cache_entry();
    entry->addr = addr;
    entry->length = length;
    entry->mr = mr;
    entry->refcount = 1;
    entry->last_used = current_time();
    add_to_cache(entry);
    
    return mr;
}

void cached_dereg_mr(struct ibv_mr *mr) {
    struct mr_cache_entry *entry = find_cache_entry(mr);
    
    entry->refcount--;
    if (entry->refcount == 0) {
        // Don't actually deregister - keep in cache!
        // Will be deregistered later if cache is full
    }
}
```

**Cache invalidation challenge:**

The cache must be invalidated when virtual memory changes:

``` {.sourceCode .c}
// Application calls munmap()
munmap(addr, length);

// Problem: Cached MR for this region is now invalid!
// NIC still thinks it can DMA to these physical pages
// But OS might reallocate them to another process

// Solution: MMU notifiers
void mmu_notifier_invalidate_range(mm, start, end) {
    // Kernel callback when virtual memory changes
    
    // Invalidate cache entries overlapping [start, end)
    for_each_cache_entry(entry) {
        if (ranges_overlap(entry->addr, entry->length, start, end-start)) {
            // Deregister immediately
            ibv_dereg_mr_real(entry->mr);
            remove_from_cache(entry);
        }
    }
}
```

**Performance with cache:**

    First access to 1 MB buffer:
      Registration: 50 ms (cache miss)
      RDMA: 0.01 ms
      Total: 50 ms
      
    Subsequent accesses to same buffer:
      Cache lookup: 0.001 ms
      RDMA: 0.01 ms
      Total: 0.011 ms (4500× faster!)
      
    Hit rate (typical workload): 85-95%

For workloads with locality (common), the cache eliminates most
registration overhead.

### Solution 3: On-Demand Paging (ODP)

Modern RDMA NICs support on-demand paging---the NIC can page fault just
like a CPU:

``` {.sourceCode .c}
// Register memory with ODP flag
struct ibv_mr *mr = ibv_reg_mr(pd, buffer, size,
                                IBV_ACCESS_LOCAL_WRITE |
                                IBV_ACCESS_ON_DEMAND);  // Magic flag!

// Registration returns IMMEDIATELY - no pinning!
// Pages are allocated on-demand when NIC accesses them
```

How it works:

    First RDMA access to address 0x7fff_0000:
      1. NIC DMAs to virtual address 0x7fff_0000
      2. NIC checks ATC (Address Translation Cache) - miss
      3. NIC sends ATS translation request to IOMMU
      4. IOMMU walks page tables - PTE not present
      5. IOMMU sends Page Request to CPU
      6. CPU allocates page (or swaps in from disk)
      7. CPU updates PTE
      8. CPU sends Page Response to IOMMU
      9. IOMMU returns translation to NIC
      10. NIC caches in ATC
      11. NIC completes DMA
      
    Latency: 50-100 µs (first access)
      
    Subsequent accesses:
      1. NIC checks ATC - hit!
      2. NIC completes DMA
      
    Latency: 1-2 µs (normal)

**ODP performance characteristics:**

    Registration time:
      Traditional: 50-200 ms
      ODP: <1 ms (no pinning!)
      
    First access (cold):
      Traditional: 1-2 µs
      ODP: 50-100 µs (page fault)
      
    Subsequent access (warm):
      Traditional: 1-2 µs
      ODP: 1-2 µs (ATC hit)
      
    Memory usage:
      Traditional: All registered memory pinned
      ODP: Only active pages pinned (automatically unpinned when idle)

**When ODP helps:**

    Dynamic memory allocation:
      - Don't know what to register upfront
      - Many small buffers
      - Temporary allocations
      
    Large address spaces:
      - Registering terabytes
      - Sparse access patterns
      - Working set << registered size
      
    Memory overcommit:
      - More registered memory than physical RAM
      - Kernel can swap inactive pages

**When ODP hurts:**

    Latency-sensitive:
      - 50-100 µs page fault unacceptable
      - Need deterministic performance
      - Example: High-frequency trading
      
    Random access:
      - No locality
      - ATC thrashing
      - Constant page faults
      
    Small ATC:
      - NIC has limited ATC entries (512-4096)
      - Large working set
      - Low hit rate

### Hybrid Approach: Explicit + ODP

Production systems often combine techniques:

``` {.sourceCode .c}
// Hot path: Pre-registered pool
void *hot_pool = malloc(10GB);
struct ibv_mr *hot_mr = ibv_reg_mr(pd, hot_pool, 10GB,
                                    IBV_ACCESS_LOCAL_WRITE);

// Cold path: ODP for dynamic allocations  
struct ibv_mr *cold_mr = ibv_reg_mr(pd, NULL, 1TB,  // Huge virtual range
                                     IBV_ACCESS_ON_DEMAND);

// At runtime
if (is_hot_path(request)) {
    buf = allocate_from_pool(hot_pool);  // No registration needed
} else {
    buf = malloc(size);  // ODP handles registration
}
```

This provides: - **Predictable latency** for hot path (no page faults) -
**Flexibility** for cold path (ODP handles arbitrary allocations) -
**Memory efficiency** (only hot data pinned)

### Case Study: Redis with RDMA

A production Redis deployment illustrates the trade-offs.

**Setup:** - Redis with RDMA-enabled GET operations - Workload: 80% hits
(cached), 20% misses (from disk) - Value sizes: 100 bytes to 10 MB (long
tail distribution)

**Traditional approach (pinned memory):**

    At startup:
      Register 32 GB buffer pool
      Time: 8 seconds
      Memory pinned: 32 GB (can't swap)
      
    Runtime (GET for 1 MB value):
      Allocate from pool: 0.01 ms
      RDMA read: 0.01 ms
      Total: 0.02 ms
      
    Problem: 32 GB pinned always, even if only using 15 GB

**ODP approach:**

    At startup:
      Register 128 GB virtual range with ODP
      Time: 0.5 ms
      Memory pinned: 0 GB initially
      
    Runtime (first GET for 1 MB value - cold):
      malloc(): 0.01 ms
      RDMA read triggers page fault: 80 µs
      Total: 80 µs
      
    Runtime (subsequent GETs - warm):
      RDMA read (ATC hit): 0.01 ms
      Total: 0.01 ms
      
    Actual memory usage:
      Working set: 18 GB
      Memory pinned: ~18 GB (automatically managed)
      OS can swap inactive pages

**Performance comparison:**

| Metric | Traditional | ODP |
| --- | --- | --- |
| Startup time | seconds | .5 ms |
| Memory pinned | 2 GB | 8 GB |
| P50 latency | µs | µs |
| P99 latency | µs | µs |
| P99.9 latency | µs | 0 µs  ← |
| Throughput: | 0K ops/sec | 0K ops/ |


**Decision:** The team chose ODP despite slightly higher tail latency
because: 1. Memory savings (32 GB → 18 GB) allowed more Redis instances
per server 2. Startup time improvement (8 sec → 0.5 ms) enabled faster
deployments 3. P99.9 latency spike (50 → 180 µs) was acceptable for
their SLA (200 µs)

For a high-frequency trading system with sub-microsecond latency
requirements, they would choose traditional registration instead.

------------------------------------------------------------------------

## 10.5 Smart NICs and Data Processing Units

A Smart NIC or DPU (Data Processing Unit) is a network card with
embedded general-purpose processors---typically ARM cores running Linux.
Unlike traditional NICs that offload specific functions (TCP checksum,
RDMA), Smart NICs can run arbitrary software, making them programmable
infrastructure accelerators.

The memory management challenge: how does the DPU\'s CPU access host
memory? The DPU is a separate computer connected via PCIe. It has its
own RAM, its own OS, and its own page tables. Accessing host memory
requires going through the PCIe link and the IOMMU.

### NVIDIA BlueField DPU Architecture

The NVIDIA BlueField-2 exemplifies modern DPU design:

**Hardware:**

    Compute:
      8× ARM Cortex-A72 cores @ 3.0 GHz
      L1: 32 KB I-cache + 32 KB D-cache per core
      L2: 1 MB per 4-core cluster
      
    Memory (on DPU):
      16 GB DDR4-2933 (local to ARM cores)
      Bandwidth: ~45 GB/s
      
    Networking:
      2× 100 Gbps Ethernet ports
      RDMA (RoCE v2) support
      
    Host Interface:
      PCIe Gen 4.0 x16
      Bandwidth: 64 GB/s (bidirectional)
      
    Accelerators:
      Crypto: AES-GCM, IPsec
      Regex engine for deep packet inspection
      Compression: gzip, LZ4

**Memory Architecture:**

The DPU has three memory domains:

    1. DPU Local Memory (16 GB DDR4):
       - Fast access for DPU CPUs (100 ns)
       - Stores DPU OS, application code, data structures
       
    2. Host Memory (512 GB typical):
       - Accessed via PCIe
       - Slow access for DPU CPUs (1-3 µs)
       - Stores bulk data that DPU processes
       
    3. Network Buffers (in DPU or host):
       - Can be in either location
       - DPU DMA engine moves data

### Accessing Host Memory from DPU

When the DPU CPU wants to access host memory, it goes through multiple
layers:

    DPU CPU memory access to host:
      1. DPU CPU executes: ldr x0, [x1]  // Load from address in x1
      2. DPU MMU translates (using DPU's page tables)
      3. DPU MMU recognizes address is in "host memory range"
      4. DPU MMU generates PCIe Memory Read Request
      5. PCIe TLP sent to host
      6. Host IOMMU intercepts (if enabled)
      7. Host IOMMU translates using host page tables
      8. Physical memory read
      9. Data returned via PCIe
      10. DPU CPU receives data
      
    Latency: 1-3 µs (vs 100 ns for local memory)

**Address Space Mapping:**

The DPU and host have separate virtual address spaces. The DPU kernel
maps host memory into the DPU\'s address space:

``` {.sourceCode .c}
// On DPU, map host memory region
void *dpu_addr = dpu_map_host_memory(host_paddr, size);

// Now DPU can access:
*(uint64_t *)dpu_addr = 0x1234;  // Writes to host memory via PCIe
```

Behind the scenes:

``` {.sourceCode .c}
void *dpu_map_host_memory(uint64_t host_paddr, size_t size) {
    // Allocate virtual address range on DPU
    void *dpu_vaddr = dpu_vmalloc(size);
    
    // Create page table entries that point to host
    for (offset = 0; offset < size; offset += PAGE_SIZE) {
        pte_t *pte = dpu_pte_offset(dpu_vaddr + offset);
        
        // Special PTE format that triggers PCIe transaction
        pte_set_pcie_target(pte, host_paddr + offset);
    }
    
    return dpu_vaddr;
}
```

### Use Case 1: OVS Offload

Open vSwitch (OVS) is software-defined networking for virtualization.
Traditionally it runs on the host CPU, consuming 20-40% of CPU cycles
for packet forwarding. Offloading OVS to the DPU frees those cycles for
applications.

**Architecture:**

    Traditional (OVS on host):
      Packet arrives at NIC
      ↓ DMA to host memory
      ↓ Interrupt to host CPU
      ↓ OVS processes (flow table lookup, actions)
      ↓ Forward decision
      ↓ DMA from host memory
      ↓ NIC transmits
      
      CPU overhead: 30% of one core per 10 Gbps
      Latency: 50-100 µs

**Offloaded (OVS on DPU):**

      Packet arrives at DPU NIC ports
      ↓ DPU receives packet (in DPU memory)
      ↓ DPU CPUs run OVS
      ↓ Flow table lookup (in DPU memory)
      ↓ Forward decision
      ↓ DPU transmits packet
      
      Host CPU overhead: 0%!
      DPU CPU usage: 15% of one ARM core per 10 Gbps
      Latency: 10-20 µs

**Flow Table Access Pattern:**

    Flow table: 1 million entries (typical datacenter)
      Size: ~100 MB
      Access pattern: Random (hash table lookups)
      Update rate: 1000 updates/sec

**Challenge**: Should flow table reside in DPU memory or host memory?

**Option A: DPU Memory**

    Pros:
      Fast access (100 ns per lookup)
      No PCIe overhead
      
    Cons:
      Uses DPU's limited 16 GB RAM
      Synchronization complexity (host also needs to access)

**Option B: Host Memory**

    Pros:
      Host has more RAM (512 GB typical)
      Shared data structure (host can also access)
      
    Cons:
      Slow access (1-3 µs per lookup)
      PCIe bandwidth consumed

**Hybrid Solution:**

``` {.sourceCode .c}
// Hot entries cached in DPU memory
struct flow_cache {
    flow_entry_t hot[10000];  // In DPU RAM
    void *cold;               // Points to host memory
};

int ovs_lookup(packet_t *pkt) {
    uint32_t hash = flow_hash(pkt);
    
    // Check hot cache (DPU local)
    flow_entry_t *entry = lookup_hot_cache(hash);
    if (entry) {
        // Fast path: 100 ns
        return apply_actions(entry, pkt);
    }
    
    // Check cold table (host memory via PCIe)
    entry = lookup_host_table(hash);  // 1-3 µs
    if (entry) {
        // Promote to hot cache
        insert_hot_cache(entry);
        return apply_actions(entry, pkt);
    }
    
    return FLOW_MISS;
}
```

**Performance:**

    95% flows: Hit hot cache (100 ns lookup)
    5% flows: Miss to host memory (1.5 µs lookup)

    Average lookup: 0.95×100ns + 0.05×1500ns = 170 ns

    vs OVS on host CPU: 5-10 µs average lookup

    Speedup: 30-60×

### Use Case 2: NVMe-oF Target

The DPU can act as an NVMe-over-Fabrics target, presenting local NVMe
SSDs to remote hosts via RDMA:

    Traditional storage server:
      Host CPU runs NVMe-oF target software
      CPU overhead: 60% for 10 GB/s throughput
      
    DPU-offloaded:
      DPU runs NVMe-oF target
      DPU handles:
        - RDMA connections
        - NVMe command processing
        - Data movement (SSD ↔ Network)
      Host CPU overhead: 0%
      DPU CPU overhead: 20% for 10 GB/s

**Memory Access Pattern:**

    Metadata (in host memory):
      Namespace configuration
      Block mapping tables
      Access control lists
      
    Data (in DPU-attached SSDs):
      Actual block data
      DPU reads from SSD, sends via RDMA

The DPU accesses host memory for metadata:

``` {.sourceCode .c}
// DPU code for NVMe read command
void nvme_read(nvme_cmd_t *cmd) {
    // Metadata lookup in host memory
    block_map_t *map = host_memory_lookup(cmd->namespace_id);
    // PCIe read: 1-2 µs
    
    lba_t lba = map->logical_to_physical(cmd->lba);
    
    // Read data from local SSD
    void *data = nvme_ssd_read(lba, cmd->length);  // 50-100 µs
    
    // RDMA write to remote host
    rdma_write(cmd->remote_addr, data, cmd->length, cmd->rkey);
}
```

The metadata access (1-2 µs via PCIe) is negligible compared to SSD
latency (50-100 µs).

### Coherency Challenges

When both host CPU and DPU access the same data, coherency issues
emerge:

**Problem:**

    T0: Host CPU writes metadata: table[X] = new_value
    T1: Value in host CPU cache (not yet in DRAM)
    T2: DPU reads table[X] via PCIe
    T3: DPU gets stale value from DRAM (cache not visible to PCIe)

**Solution 1: Software Cache Flushing**

``` {.sourceCode .c}
// Host side
update_metadata(table, X, new_value);
clflush(&table[X]);  // Flush CPU cache line
wmb();               // Write memory barrier

// Now DPU PCIe read will see new value
```

**Solution 2: Uncached Memory**

``` {.sourceCode .c}
// Host allocates uncached memory for shared structures
void *shared = mmap(NULL, size, PROT_READ | PROT_WRITE,
                    MAP_SHARED | MAP_ANONYMOUS, -1, 0);

// Set memory type to uncached
set_memory_uc(shared, size);

// All accesses bypass CPU cache
// Always coherent but slow (100 ns vs 5 ns)
```

**Solution 3: Message Passing** (Avoid Sharing)

``` {.sourceCode .c}
// Don't share memory - use message queues

// Host sends update to DPU
send_message_to_dpu(UPDATE_METADATA, new_value);

// DPU updates its local copy
receive_message_from_host();
update_local_metadata(new_value);
```

**Performance Comparison:**

    Shared memory (cached):
      Host write: 5 ns
      DPU read: 1.5 µs
      Problem: Coherency issues
      
    Shared memory (uncached):
      Host write: 100 ns
      DPU read: 1.5 µs
      No coherency issues but slow host access
      
    Message passing:
      Host send: 2 µs
      DPU receive: 2 µs
      Total: 4 µs
      Slower but cleanly separates data

For infrequent updates (e.g., configuration changes), message passing is
preferred. For high-frequency access (e.g., packet metadata), shared
uncached memory or explicit cache flushing is necessary.

### Real-World Deployment: Cloud Provider Networking

A cloud provider deployed BlueField-2 DPUs across 10,000 servers:

**Before (OVS on host CPU):**

    Per-server CPU usage for networking: 35%
      12 cores dedicated to OVS out of 48 total
      
    Available for customer VMs: 36 cores
    Customer VM density: 72 VMs (2 vCPU each)

**After (OVS on DPU):**

    Host CPU usage for networking: 2%
      0.5 cores overhead for DPU management
      
    Available for customer VMs: 47.5 cores
    Customer VM density: 95 VMs (2 vCPU each)

    Increase: 23 additional VMs per server (+32%)

**Economic Impact:**

    10,000 servers × 23 VMs = 230,000 additional VMs
    At $50/VM/month: $11.5M additional monthly revenue
    DPU cost: $500 per server × 10,000 = $5M
    ROI: 5 months payback period

The deployment succeeded because: 1. OVS workload fit DPU capabilities
(packet processing, not compute-intensive) 2. Flow tables fit in DPU
memory (with host memory fallback) 3. Latency improvement (50 µs → 15
µs) enhanced customer experience 4. Host CPU freed for
revenue-generating workloads

\[Continue with sections 10.6-10.10 in next file...\] \## 10.6 FPGA
Coherent Accelerators

Field-Programmable Gate Arrays (FPGAs) offer reconfigurable hardware
acceleration for custom algorithms. Traditional FPGA designs require
explicit data movement---copy data from CPU memory to FPGA memory,
process it, copy results back. Coherent FPGAs eliminate this overhead by
participating in the CPU\'s cache coherency protocol.

### Intel PAC (Programmable Acceleration Card) with CCI-P

Intel\'s PAC connects FPGAs to CPUs via CCI-P (Core Cache Interface)---a
coherent interconnect that extends the CPU\'s cache coherency fabric to
the FPGA.

**Architecture:**

    CPU Complex:
      Cores → L1/L2 caches → L3 cache (LLC)
      ↓
      CCI-P interface
      ↓
    FPGA:
      Custom logic (user-programmable)
      Local SRAM buffers
      CCI-P request/response channels

**Memory Access Modes:**

CCI-P supports multiple coherency modes:

    1. Uncached (UC):
       FPGA → LLC → DRAM
       Bypasses cache, direct DRAM access
       Fast for sequential scans of large data
       
    2. Write-Through (WT):
       FPGA → LLC (read) / DRAM (write)
       Reads check cache, writes go to DRAM
       Good for read-heavy workloads
       
    3. Write-Back (WB):
       FPGA ↔ LLC ↔ DRAM
       Fully cached, coherent with CPU
       Best for shared data structures

### FPGA → CPU Memory Access Example

``` {.sourceCode .verilog}
// FPGA code to read host memory
module memory_reader (
    input  clk,
    input  reset,
    output ccip_c0_tx_t c0_tx,  // Request channel
    input  ccip_c0_rx_t c0_rx   // Response channel
);

    reg [63:0] read_addr;
    reg        read_valid;
    
    // Issue read request
    always @(posedge clk) begin
        if (!c0_tx.full && need_data) begin
            c0_tx.valid <= 1'b1;
            c0_tx.hdr.vc_sel <= eVC_VA;  // Virtual channel
            c0_tx.hdr.req_type <= eREQ_RDLINE_I;  // Read Line Invalidate (cache coherent)
            c0_tx.hdr.address <= read_addr[47:6];  // 64-byte aligned
            
            read_addr <= read_addr + 64;  // Next cache line
        end
    end
    
    // Receive response
    always @(posedge clk) begin
        if (c0_rx.rspValid) begin
            // Got 64 bytes of data
            process_data(c0_rx.data);  // 512 bits
        end
    end
endmodule
```

**Translation Path:**

    FPGA issues read to virtual address 0x7fff_1000:
      1. CCI-P request from FPGA
      2. Integrated IOMMU translates virtual → physical
         (FPGA can use virtual addresses!)
      3. Cache lookup in CPU's LLC
         - Hit: Return data from cache (200-300 ns)
         - Miss: Read from DRAM (500-1000 ns)
      4. Data returned to FPGA
      
    Compare to traditional FPGA DMA:
      1. CPU copies data to FPGA DRAM
      2. FPGA processes from local memory
      3. CPU copies results back
      
    Latency: 10-100 µs for DMA transfers

The coherent path is 50-100× faster for small, random accesses.

### Use Case: Genomics Alignment

Genomic sequencing generates enormous datasets---a human genome is 3
billion base pairs. Aligning reads to a reference genome is
computationally intensive. FPGAs can accelerate the Smith-Waterman
alignment algorithm.

**Traditional Approach:**

``` {.sourceCode .c}
// CPU allocates buffers
char *reference = malloc(3GB);  // Reference genome
char *reads = malloc(1GB);      // Sequencing reads
char *results = malloc(100MB);  // Alignment scores

// Load reference genome
read_from_disk(reference, 3GB);

// DMA to FPGA
fpga_dma_write(fpga, reference, 3GB);  // 60-100 ms!
fpga_dma_write(fpga, reads, 1GB);      // 20-30 ms

// FPGA processes
fpga_execute_alignment();  // 2 seconds

// DMA results back
fpga_dma_read(fpga, results, 100MB);   // 2-5 ms

Total: ~2.2 seconds (100ms DMA overhead)
```

**Coherent Approach:**

``` {.sourceCode .c}
// CPU allocates buffers (in host memory)
char *reference = malloc(3GB);
char *reads = malloc(1GB);
char *results = malloc(100MB);

// Load reference genome
read_from_disk(reference, 3GB);

// Pass pointers to FPGA (virtual addresses!)
fpga_set_reference_ptr(fpga, reference);
fpga_set_reads_ptr(fpga, reads);
fpga_set_results_ptr(fpga, results);

// FPGA processes - reads directly from host memory via CCI-P
fpga_execute_alignment();  // 2.1 seconds

// Results already in host memory - no DMA needed!

Total: 2.1 seconds (no DMA overhead)
```

The coherent approach saves 100 ms of DMA time---5% speedup. More
importantly, it simplifies programming (no explicit memory management)
and reduces memory footprint (no FPGA-side copy of reference genome).

**Performance Breakdown:**

    FPGA alignment algorithm:
      Memory reads: 4 GB (reference + reads)
      Memory writes: 100 MB (results)
      
    CCI-P bandwidth: ~15 GB/s (read), ~10 GB/s (write)
      Read time: 4 GB / 15 GB/s = 267 ms
      Write time: 100 MB / 10 GB/s = 10 ms
      Compute time: 1.8 seconds (overlapped with memory access)
      
    Total: 2.1 seconds (compute-bound, not memory-bound)

    Traditional DMA bandwidth: ~30 GB/s (theoretical)
      But requires 2× transfers (to FPGA, from FPGA)
      And cannot overlap with compute (sequential)

### Cache Coherency Protocol

When both CPU and FPGA access shared data, CCI-P maintains coherency
automatically:

**Example: Producer-Consumer**

``` {.sourceCode .c}
// CPU (producer) writes data
for (int i = 0; i < N; i++) {
    buffer[i] = compute_value(i);
}

// FPGA (consumer) reads data
```

**Without Coherency:**

    CPU writes buffer[0] → CPU cache (not visible to FPGA)
    FPGA reads buffer[0] → Reads stale value from DRAM
    Result: WRONG!

**With CCI-P Coherency:**

    FPGA reads buffer[0]:
      1. FPGA sends CCI-P read request
      2. CPU cache controller snoops request
      3. Cache sees it has modified data for buffer[0]
      4. Cache sends data directly to FPGA
      5. FPGA receives correct value

This happens in hardware, transparently. No software intervention
needed.

**Coherency Performance Cost:**

    FPGA read with coherency:
      Cache hit (data in CPU cache): 200-300 ns
      Cache miss (data in DRAM): 500-1000 ns
      
    FPGA read without coherency (uncached):
      Always DRAM: 100-300 ns
      
    Coherency overhead: 100-200 ns per access

The overhead is worth it when data is frequently modified by the CPU
(high chance of being in cache). For read-only data, uncached mode is
faster.

### AMD CCIX (Cache Coherent Interconnect for Accelerators)

While Intel\'s CCI-P is proprietary to Intel CPUs, CCIX is an open
standard for cache-coherent accelerator interfaces. It works over PCIe
physical layers.

**CCIX Benefits:**

    1. Standard protocol (works with any CCIX-compliant CPU)
       - AMD EPYC
       - ARM Neoverse
       - RISC-V implementations
       
    2. Flexible topology
       - Point-to-point
       - Switch-based
       - Multi-hop
       
    3. Quality of Service (QoS)
       - Priority levels for transactions
       - Bandwidth guarantees

**CCIX vs CCI-P Performance:**

                        CCI-P              CCIX
    Latency (cache hit) 200-300 ns        300-500 ns
    Bandwidth (read)    15 GB/s           25 GB/s
    Bandwidth (write)   10 GB/s           25 GB/s
    CPU compatibility   Intel only        Multi-vendor

CCIX has higher latency (due to PCIe serialization) but higher bandwidth
(newer PCIe generations). The choice depends on whether latency or
bandwidth is the bottleneck.

------------------------------------------------------------------------

## 10.7 Video and Media Accelerators

Video encode/decode engines are specialized accelerators found on most
modern CPUs and GPUs. They access memory differently than
general-purpose devices---highly sequential patterns with large buffers.

### Intel QuickSync Architecture

Intel\'s QuickSync is a fixed-function video encoder/decoder integrated
into the CPU die:

**Memory Access Pattern for H.264 Decode:**

    Input:
      Compressed bitstream (sequential read)
      - Example: 5 MB/s for 1080p60
      - Mostly sequential, occasional random access for seeking
      
    Output:
      Decoded frames (sequential write)
      - 1920×1080×1.5 bytes (YUV) = 3 MB per frame
      - 60 fps = 180 MB/s
      
    Reference frames (random access):
      - H.264 uses up to 16 reference frames
      - Decoder randomly reads previous frames
      - Access pattern: Unpredictable
      - Size: 16 × 3 MB = 48 MB

**Page Table Interaction:**

    QuickSync uses IOMMU (if enabled):
      Bitstream address: 0x7fff_0000 (virtual)
      Output frame address: 0x8000_0000 (virtual)
      
    IOMMU translates:
      For each 4 KB of access, IOTLB lookup
      
    Sequential bitstream:
      5 MB/s = 1,280 pages/sec
      IOTLB entry lifetime: ~100 ms
      IOTLB entries needed: 128 (minimal)
      
    Random reference frames:
      16 frames × 768 pages/frame = 12,288 pages
      IOTLB entries (if all cached): 12,288
      Actual IOTLB size: 256
      Miss rate: 95%+

The reference frame access kills IOTLB effectiveness.

**Optimization: Huge Pages**

``` {.sourceCode .c}
// Allocate frame buffers with huge pages
for (int i = 0; i < 32; i++) {
    frame_buffer[i] = mmap(NULL, 3MB, PROT_READ | PROT_WRITE,
                          MAP_PRIVATE | MAP_ANONYMOUS | MAP_HUGETLB,
                          -1, 0);
    // Each frame is 1-2 huge pages (2 MB pages)
}

// Now IOTLB can cache all reference frames:
  16 frames × 2 pages/frame = 32 IOTLB entries
  Fits comfortably in 256-entry IOTLB
```

**Performance Impact:**

    Without IOMMU:
      Decode latency: 16 ms per frame (consistent)
      Throughput: 62.5 fps
      
    With IOMMU (4 KB pages):
      Decode latency: 21 ms per frame (+31%)
      IOTLB miss stalls: 5 ms
      Throughput: 47.6 fps
      
    With IOMMU (2 MB pages):
      Decode latency: 16.5 ms per frame (+3%)
      IOTLB misses: Rare
      Throughput: 60.6 fps

Huge pages are essential for maintaining video decode performance with
IOMMU enabled.

### NVIDIA NVENC/NVDEC

NVIDIA\'s video encoders/decoders reside on the GPU and share GPU memory
and the GPU MMU:

**Memory Architecture:**

    GPU Memory (VRAM):
      Typical: 16-80 GB HBM
      Bandwidth: 1-3 TB/s
      
    Video encoder accesses:
      - Input frames (from GPU memory or system memory)
      - Output bitstream (to GPU memory, then copied to system)
      
    Shared with:
      - CUDA kernels
      - Graphics rendering
      - Display controller

**Zero-Copy Path:**

``` {.sourceCode .c}
// Capture frame from camera (in system memory)
void *frame = capture_frame();

// Traditional: Copy to GPU memory
cudaMemcpy(gpu_frame, frame, size, cudaMemcpyHostToDevice);  // 30 ms!
nvenc_encode(gpu_frame);  // 10 ms

// Zero-copy: Encode directly from system memory
cudaHostRegister(frame, size, cudaHostRegisterMapped);
nvenc_encode_from_host(frame);  // 12 ms (no copy!)
```

The zero-copy approach uses the GPU\'s ability to access system memory
via PCIe:

    GPU encoder reads from system memory:
      1. GPU memory controller issues PCIe read
      2. Host IOMMU translates virtual address
      3. Physical memory read
      4. Data returned via PCIe
      5. GPU encoder processes
      
    Latency: 500-1000 ns per 64-byte read
    Bandwidth: ~20 GB/s (limited by PCIe)

For 1080p60 encode (180 MB/s input), PCIe bandwidth is sufficient. The
extra 2 ms (12 ms vs 10 ms) is acceptable compared to 30 ms copy
overhead.

------------------------------------------------------------------------

## 10.8 Multi-Device Coherency and Coordination

When multiple devices access the same memory simultaneously,
coordinating TLB invalidations and cache coherency becomes the hardest
challenge.

### The TLB Shootdown Problem

Consider a server with:

    64 CPU cores
    2 GPUs (each with device MMU)
    2 100 Gbps NICs (with ATS/ATC)
    4 NVMe SSDs (with IOMMU)
    1 FPGA
    = 73 devices with translation caches

When the OS unmaps a page, it must invalidate TLBs on all devices:

``` {.sourceCode .c}
void unmap_page_global(struct mm_struct *mm, vaddr_t addr) {
    pte_t *pte = lookup_pte(mm, addr);
    
    // Step 1: Clear PTE
    pte_clear(pte);
    
    // Step 2: Flush all CPU TLBs (64 cores)
    flush_tlb_all_cpus(mm, addr);  // Send 64 IPIs
    
    // Step 3: Flush GPU TLBs (2 GPUs)
    for_each_gpu(gpu) {
        gpu_tlb_invalidate(gpu, addr);  // PCIe transaction
    }
    
    // Step 4: Flush NIC ATCs (2 NICs)
    for_each_nic(nic) {
        nic_send_ats_invalidate(nic, addr);  // PCIe ATS Invalidate
        wait_for_completion(nic);
    }
    
    // Step 5: Flush IOMMU IOTLBs (1 IOMMU for SSDs + FPGA)
    iommu_iotlb_flush(iommu, addr);
    
    // Only now is it safe to free the page!
}
```

**Latency Breakdown:**

    CPU TLB flush (64 cores):
      Send IPIs: 64 × 100 ns = 6.4 µs
      Wait for acks: ~2 µs
      Total: ~8 µs
      
    GPU TLB flush (2 GPUs):
      PCIe request: 2 × 1 µs = 2 µs
      GPU invalidate: 2 × 3 µs = 6 µs
      Total: ~8 µs
      
    NIC ATC flush (2 NICs):
      ATS Invalidate message: 2 × 2 µs = 4 µs
      Wait for completion: 2 × 1 µs = 2 µs
      Total: ~6 µs
      
    IOMMU flush:
      Register write + wait: ~2 µs
      
    Grand total: 8 + 8 + 6 + 2 = 24 µs per page unmap!

For a munmap() of 10,000 pages done naively:

    10,000 pages × 24 µs = 240 milliseconds!

This is unacceptable. Applications would experience huge latency spikes.

### Batching TLB Invalidations

The solution: batch invalidations and send one global flush at the end:

``` {.sourceCode .c}
struct tlb_batch {
    vaddr_t addrs[1024];
    int count;
};

void unmap_range_batched(struct mm_struct *mm, vaddr_t start, vaddr_t end) {
    struct tlb_batch batch = {0};
    
    // Step 1: Clear all PTEs (collect addresses)
    for (vaddr_t addr = start; addr < end; addr += PAGE_SIZE) {
        pte_t *pte = lookup_pte(mm, addr);
        pte_clear(pte);
        
        batch.addrs[batch.count++] = addr;
        
        if (batch.count == 1024) {
            flush_batch(&batch);
            batch.count = 0;
        }
    }
    
    // Step 2: Flush remaining
    if (batch.count > 0) {
        flush_batch(&batch);
    }
}

void flush_batch(struct tlb_batch *batch) {
    // Flush all CPUs (single IPI broadcast)
    flush_tlb_range_all_cpus(batch->addrs, batch->count);
    
    // Flush all GPUs (single invalidate covering range)
    for_each_gpu(gpu) {
        gpu_tlb_invalidate_range(gpu, batch->addrs[0], 
                                 batch->addrs[batch->count-1]);
    }
    
    // Flush all NICs (single ATS invalidate for range)
    for_each_nic(nic) {
        nic_send_ats_invalidate_range(nic, batch->addrs[0],
                                       batch->addrs[batch->count-1]);
    }
    
    // Flush IOMMU
    iommu_iotlb_flush_range(iommu, batch->addrs[0], 
                            batch->addrs[batch->count-1]);
}
```

**Performance with Batching:**

    Unmap 10,000 pages:
      Clear PTEs: 10,000 × 50 ns = 500 µs
      TLB flush: 24 µs (once for entire range)
      Total: 524 µs
      
    Speedup: 240 ms / 0.524 ms = 458×

The batching is so effective because modern hardware supports
range-based invalidation (flush address range X-Y with one command).

### Cross-Device Ordering

Another challenge: ensuring operations complete in the correct order
across devices.

**Problem Scenario:**

    CPU updates shared data structure:
      T0: CPU writes: data[X] = new_value
      T1: CPU invalidates TLB for data[X]
      T2: GPU reads data[X]
      
    Expected: GPU sees new_value

    Actual (with reordering):
      T0: CPU writes to cache
      T1: CPU sends TLB invalidate to GPU
      T2: GPU receives invalidate, flushes entry
      T3: CPU's write reaches memory (delayed)
      T4: GPU reads data[X] from memory
      Result: GPU sees OLD value (write arrived late!)

**Solution: Memory Barriers**

``` {.sourceCode .c}
void update_shared_data_safe(int X, int new_value) {
    // Write data
    data[X] = new_value;
    
    // Ensure write is visible
    wmb();  // Write memory barrier (flush CPU store buffer)
    
    // Invalidate TLBs
    flush_tlb_all_devices(data + X);
    
    // Ensure invalidate completed before proceeding
    wait_for_all_device_acks();
}
```

The wmb() forces the CPU to flush its store buffer to cache/memory
before proceeding, ensuring the write is visible before the TLB
invalidation propagates.

### Deadlock Avoidance

With multiple devices and locks, deadlock becomes a risk:

**Deadlock Scenario:**

    Thread A (CPU 0):
      1. Locks page table lock for address 0x1000
      2. Sends TLB invalidate to GPU
      3. Waits for GPU ack
      
    GPU (handling another request):
      1. Page fault on address 0x2000
      2. Sends Page Request to CPU
      3. CPU fault handler needs page table lock for 0x2000
      
    Result: Deadlock!
      Thread A holds lock, waits for GPU
      GPU waits for CPU fault handler
      CPU fault handler waits for Thread A's lock

**Solution: Hierarchical Locking with Timeout**

``` {.sourceCode .c}
// Never hold locks while waiting for device responses

void unmap_page_safe(vaddr_t addr) {
    // Acquire lock
    spin_lock(&page_table_lock);
    
    // Update page tables
    pte_clear(lookup_pte(addr));
    
    // Release lock BEFORE device operations
    spin_unlock(&page_table_lock);
    
    // Now safe to wait for devices
    flush_tlb_all_devices(addr);
    wait_for_all_acks_with_timeout(100ms);
    
    if (timeout) {
        // Device didn't respond - reset it
        reset_misbehaving_device();
    }
}
```

The key principle: never hold spinlocks while waiting for external
devices (which might take arbitrarily long).

\[Continuing with sections 10.9 and 10.10 in next file...\] \## 10.9
Case Study: Multi-Device Video Processing Pipeline

To synthesize the concepts from this chapter, let\'s examine a
real-world system that coordinates multiple device types: a live video
transcoding pipeline for a streaming service.

### System Architecture

**Hardware:**

    Server: Dual Intel Xeon Gold 6348 (28 cores/socket, 56 total)
    RAM: 512 GB DDR4
    GPU: NVIDIA A10 (24 GB VRAM)
    NIC: Mellanox ConnectX-6 (100 Gbps, RDMA capable)
    Video Encoder: Intel QuickSync (on CPU)
    Storage: 4× NVMe SSDs (local cache)

**Pipeline Flow:**

    1. Ingest: NIC receives 4K video stream via RDMA (40 Gbps)
    2. Decode: CPU QuickSync decodes 4K H.264 → raw frames
    3. Process: GPU applies filters (color correction, scaling)
    4. Encode: QuickSync encodes to multiple bitrates (4K, 1080p, 720p)
    5. Distribute: NIC sends encoded streams via RDMA to CDN

The critical challenge: all devices must share frame buffers with
minimal copying.

### Memory Layout and Sharing

**Naive Approach (with copies):**

``` {.sourceCode .c}
// Receive buffer (NIC DMA target)
void *rx_buffer = malloc(100MB);
ibv_reg_mr(pd, rx_buffer, 100MB, IBV_ACCESS_LOCAL_WRITE);

// Decode buffer (QuickSync output)
void *decode_buffer = malloc(300MB);  // Raw 4K frame

// GPU buffer (processing input/output)
void *gpu_buffer;
cudaMalloc(&gpu_buffer, 300MB);

// Encode buffer (QuickSync input)
void *encode_buffer = malloc(150MB);  // Multiple outputs

// Timeline with copies:
//   T0: NIC DMAs to rx_buffer (2 ms)
//   T1: memcpy(decode_buffer, rx_buffer) (5 ms)
//   T2: QuickSync decodes (16 ms)
//   T3: cudaMemcpy to gpu_buffer (12 ms)
//   T4: GPU processes (8 ms)
//   T5: cudaMemcpy from gpu_buffer (12 ms)
//   T6: QuickSync encodes (25 ms)
//   T7: memcpy to NIC tx_buffer (3 ms)
//   T8: NIC transmits (2 ms)
//
// Total: 85 ms (32 ms of copying!)
```

**Optimized Approach (zero-copy via IOMMU):**

``` {.sourceCode .c}
// Single shared buffer pool (in host memory)
void *frame_pool = mmap(NULL, 2GB, PROT_READ | PROT_WRITE,
                       MAP_PRIVATE | MAP_ANONYMOUS | MAP_HUGETLB,
                       -1, 0);

// Register with all devices:

// 1. NIC (RDMA)
struct ibv_mr *nic_mr = ibv_reg_mr(pd, frame_pool, 2GB,
                                   IBV_ACCESS_LOCAL_WRITE |
                                   IBV_ACCESS_REMOTE_WRITE |
                                   IBV_ACCESS_ON_DEMAND);

// 2. GPU (CUDA)
cudaHostRegister(frame_pool, 2GB, cudaHostRegisterMapped);
void *gpu_ptr = cuda_get_device_pointer(frame_pool);

// 3. QuickSync (Intel VPP API)
mfxFrameAllocator allocator = {
    .Alloc = custom_alloc_from_pool,
    .Lock = custom_lock,
    .Unlock = custom_unlock,
    .Free = custom_free,
};
MFXVideoDECODE_SetFrameAllocator(decode, &allocator);
MFXVideoENCODE_SetFrameAllocator(encode, &allocator);

// Now all devices share the same buffers!
```

**Zero-Copy Timeline:**

``` {.sourceCode .c}
void process_frame_zero_copy() {
    // Allocate frame from shared pool
    frame_t *frame = pool_allocate(frame_pool);
    
    // 1. NIC receives directly into shared buffer
    ibv_post_recv(qp, frame->data, frame->size);
    wait_for_completion();  // 2 ms
    
    // 2. QuickSync decodes in-place
    //    Input: frame->data (compressed)
    //    Output: frame->data (overwrite with raw)
    quicksync_decode(frame->data);  // 16 ms
    
    // 3. GPU processes from/to shared buffer
    //    GPU accesses frame->data via PCIe
    cuda_kernel<<<>>>(gpu_ptr + frame->offset);  // 8 ms
    
    // 4. QuickSync encodes from shared buffer
    //    Input: frame->data (processed)
    //    Output: frame->encoded[] (multiple bitrates)
    quicksync_encode(frame->data, frame->encoded);  // 25 ms
    
    // 5. NIC transmits directly from shared buffer
    ibv_post_send(qp, frame->encoded, size);  // 2 ms
    
    // Total: 53 ms (zero copies!)
    pool_free(frame);
}
```

The zero-copy approach saves 32 ms per frame---38% speedup.

### IOMMU Configuration

With all devices accessing shared memory, IOMMU configuration is
critical:

**Option 1: IOMMU Disabled (Passthrough)**

``` {.sourceCode .bash}
# Boot with iommu=pt
intel_iommu=on iommu=pt

# Results:
#   Performance: Best (no translation overhead)
#   Security: Worst (devices can access any physical memory)
#   Suitable for: Single-tenant, trusted environment
```

**Option 2: IOMMU Enabled with 4KB Pages**

``` {.sourceCode .bash}
intel_iommu=on

# Results:
#   Performance: Poor
#   NIC IOTLB miss rate: 92%
#   GPU page fault rate: High
#   QuickSync reference frame misses: 95%
#   Total latency: 53ms → 78ms (+47%)
```

**Option 3: IOMMU Enabled with 2MB Huge Pages** (chosen)

``` {.sourceCode .bash}
intel_iommu=on
echo always > /sys/kernel/mm/transparent_hugepage/enabled
# Use MAP_HUGETLB for frame pool allocation

# Results:
#   Performance: Excellent
#   NIC IOTLB miss rate: 8%
#   GPU page fault rate: Low
#   QuickSync reference frame coverage: 100%
#   Total latency: 53ms → 56ms (+6%)
```

The 6% overhead is acceptable for the security benefit.

### Device Synchronization

The pipeline must synchronize operations across devices:

``` {.sourceCode .c}
struct frame_sync {
    atomic_t refcount;      // How many devices using this frame
    sem_t nic_complete;     // NIC finished receiving
    sem_t decode_complete;  // Decode finished
    sem_t gpu_complete;     // GPU finished processing
    sem_t encode_complete;  // Encode finished
};

void pipeline_process_frame() {
    frame_t *frame = pool_allocate();
    frame->sync.refcount = 4;  // 4 devices will use it
    
    // Stage 1: NIC Receive
    ibv_post_recv(qp, frame->data, size);
    wait_completion();
    sem_post(&frame->sync.nic_complete);
    
    // Stage 2: Decode (wait for NIC)
    sem_wait(&frame->sync.nic_complete);
    quicksync_decode_async(frame);
    // Decode happens asynchronously
    
    // Callback when decode completes:
    on_decode_complete(frame) {
        sem_post(&frame->sync.decode_complete);
    }
    
    // Stage 3: GPU (wait for decode)
    sem_wait(&frame->sync.decode_complete);
    cuda_kernel_async<<<>>>(frame->data);
    cudaStreamAddCallback(stream, gpu_callback, frame);
    
    gpu_callback(frame) {
        sem_post(&frame->sync.gpu_complete);
    }
    
    // Stage 4: Encode (wait for GPU)
    sem_wait(&frame->sync.gpu_complete);
    quicksync_encode_async(frame);
    
    on_encode_complete(frame) {
        sem_post(&frame->sync.encode_complete);
    }
    
    // Stage 5: Transmit (wait for encode)
    sem_wait(&frame->sync.encode_complete);
    ibv_post_send(qp, frame->encoded, size);
    wait_completion();
    
    // Done - release frame
    if (atomic_dec_and_test(&frame->sync.refcount)) {
        pool_free(frame);
    }
}
```

### TLB Coherency Across Devices

The frame pool uses on-demand paging (ODP) for flexibility. When a frame
is allocated, different devices might fault on it:

    Frame 47 allocated at 0x7f00_0000_0000 (virtual address):

    NIC first access:
      1. NIC DMAs to 0x7f00_0000_0000
      2. IOMMU translates, PTE not present
      3. Page fault to CPU
      4. CPU allocates physical page: 0x12_3456_0000
      5. CPU updates PTE, invalidates IOTLB
      6. NIC retries, succeeds
      7. NIC caches in ATC: 0x7f00_0000_0000 → 0x12_3456_0000
      
    GPU access (shortly after):
      1. GPU accesses 0x7f00_0000_0000
      2. GPU TLB miss
      3. GPU walks page tables (via IOMMU)
      4. PTE present (allocated by NIC fault)
      5. GPU caches: 0x7f00_0000_0000 → 0x12_3456_0000
      
    QuickSync access:
      1. QuickSync DMAs to 0x7f00_0000_0000
      2. IOTLB miss
      3. IOMMU walks page tables
      4. PTE present, translation succeeds
      5. IOTLB caches entry

All devices converge on the same physical address, thanks to shared page
tables.

### Performance Results

**Production Deployment:**

    Streaming service: 500 transcoding servers
    Workload: 100 concurrent 4K→multi-bitrate transcodes per server

    Before optimization (with copies):
      Latency per frame: 85 ms
      Throughput: 11.7 fps per stream
      CPU usage: 78%
      Streams per server: 85 (CPU-limited)
      
    After optimization (zero-copy):
      Latency per frame: 56 ms
      Throughput: 17.8 fps per stream
      CPU usage: 52%
      Streams per server: 125 (still CPU-limited, but less so)
      
    Improvement:
      +47% more streams per server
      +52% higher throughput per stream
      -33% CPU usage per stream

**Economic Impact:**

    Before: 500 servers × 85 streams = 42,500 streams
    After: 500 servers × 125 streams = 62,500 streams

    Additional capacity: 20,000 streams (47% increase)
    Without buying new hardware!

    Deferred capital expense: 235 servers @ $15k = $3.5M
    Operational savings: $700k/year (power, cooling, space)

The deployment succeeded because: 1. Zero-copy eliminated memory
bandwidth bottleneck 2. IOMMU with huge pages added minimal overhead
(6%) 3. Device synchronization was well-designed (no deadlocks) 4. All
devices supported required features (ATS, ODP, etc.)

------------------------------------------------------------------------

## 10.10 Summary and Best Practices

This chapter explored how non-CPU devices access virtual memory through
the IOMMU and related protocols. The landscape is complex, with multiple
trade-offs between performance, security, and flexibility. Modern
systems must balance these competing demands while maintaining
acceptable performance and security posture.

### Key Techniques Recap

**IOMMU** provides per-device page tables and memory isolation, serving
as the foundational security mechanism for device memory access. It\'s
essential for multi-tenant environments but adds overhead that must be
carefully managed. The core insight is that IOMMUs perform the same
translation function as CPU MMUs, but with fundamentally different
performance characteristics due to their position in the system topology
and their need to serve many devices simultaneously.

IOTLB misses cost 500-2000 cycles compared to 100-300 cycles for CPU TLB
misses because the IOMMU must access page tables through main memory
rather than through CPU caches. The shared IOTLB (256-512 entries across
all devices) creates contention that doesn\'t exist in per-core CPU
TLBs. This explains why huge pages transform from optional optimization
to absolute necessity---1 GB pages can achieve 100% IOTLB hit rates
where 4 KB pages miss 99% of the time.

**PCIe ATS** moves translation caching from the centralized IOMMU to
distributed device ATCs, fundamentally changing the performance model.
Instead of every device access requiring an IOMMU round-trip, devices
cache translations locally and only communicate with the IOMMU on
misses. This eliminates a critical bottleneck, reducing ATC hits to
10-50 cycles versus IOTLB misses at 500+ cycles.

PASID extends ATS to enable multi-process device sharing with isolation.
A single physical device can safely access multiple independent address
spaces simultaneously, each protected by separate page tables. This
capability is essential for SR-IOV devices serving multiple VMs or
containers without requiring multiple physical devices.

PRI allows devices to page fault, enabling true on-demand paging that
eliminates the need to pin memory. This represents a fundamental shift
from static memory allocation to dynamic allocation, but it introduces
complexity in device firmware (state machines, timeouts, retry logic)
and new failure modes that must be handled gracefully.

**RDMA Memory Registration** traditionally pins memory to provide stable
physical addresses, creating tension between performance (fast access)
and flexibility (swappable memory). Modern systems resolve this tension
through three approaches that serve different use cases:

Registration cache achieves 85-95% hit rates for workloads with
locality, amortizing the 50-200 ms registration cost across many
operations. This works well for workloads that repeatedly access the
same buffers (database buffer pools, web server response caches) but
poorly for workloads with high churn (key-value stores with uniform
random access).

On-demand paging (ODP) eliminates pinning entirely, allowing the kernel
to swap device-accessible pages. The first access costs 50-100 µs for
page fault handling, but subsequent accesses proceed at normal speed.
This flexibility enables memory overcommit and efficient use of physical
RAM, but the latency spikes are unacceptable for latency-sensitive
applications.

Hybrid approaches pre-register critical hot paths while using ODP for
everything else, providing predictable performance where it matters
while maintaining flexibility elsewhere. This pragmatic solution
reflects the reality that different parts of a system have different
requirements.

**Smart NICs and DPUs** offload network processing to embedded ARM
processors, freeing host CPU cycles for revenue-generating workloads.
The challenge is that accessing host memory via PCIe takes 1-3 µs
instead of 100 ns, requiring careful design to minimize PCIe crossings.

Successful DPU deployments keep hot data (flow tables, connection state)
in DPU memory for fast access, while cold data (configuration,
infrequent metadata) resides in host memory. This two-tier approach
balances performance (fast local access) and capacity (larger host
memory). The economics justify DPUs when CPU cycles are the
bottleneck---offloading OVS to free 30-40% of host CPU enables 32% more
VMs per server, generating far more revenue than the DPU costs.

**FPGA Coherent Access** via CCI-P/CCIX eliminates DMA overhead by
participating in CPU cache coherency, enabling 200-300 ns access when
data is in cache versus 5-20 ms for traditional DMA. This transforms
programming models (no explicit copies, just pass pointers) and works
best for random access patterns where coherency\'s overhead is offset by
eliminating transfers. For sequential scans, uncached DMA is faster
because coherency checking overhead exceeds the benefit of occasional
cache hits.

**Multi-Device Coherency** requires coordinating TLB invalidations
across potentially 100+ devices (64+ CPU cores, multiple GPUs, NICs,
FPGAs, etc.). A naive implementation that invalidates devices
sequentially can take 10-100 µs per page, making large unmaps (10,000+
pages) take hundreds of milliseconds. Batching reduces this to
microseconds by invalidating ranges rather than individual pages and
broadcasting to all devices simultaneously.

Memory barriers prevent reordering bugs where a device reads stale data
because a CPU write hasn\'t yet propagated from cache to memory.
Hierarchical locking with timeouts prevents deadlocks that arise when
devices hold implicit locks (queue full) while waiting for CPU
operations (page faults) that need locks the CPU holds (page table
lock).

### Common Pitfalls to Avoid: Detailed Analysis

Real-world deployments frequently encounter the same failure patterns.
Understanding these pitfalls in detail, including their root causes and
proper solutions, prevents months of debugging and costly production
incidents.

#### Pitfall 1: Forgetting Huge Pages with IOMMU Enabled

**The Problem:** Enabling IOMMU with default 4 KB pages can reduce
device performance by 30-50%, sometimes more. Engineers enable IOMMU for
security, run benchmarks, see catastrophic performance degradation, and
conclude that IOMMU is \"too slow\" for their workload. The real issue
isn\'t the IOMMU itself but the page size mismatch.

**Root Cause Analysis:** Consider a 100 Gbps NIC processing packets
spread across a 1 GB working set. With 4 KB pages, this is 262,144
distinct pages that need translations. The IOTLB might have 512 total
entries shared across all devices on the IOMMU. If the NIC gets 25% of
IOTLB capacity (generous assumption), it has 128 entries. This covers
128 × 4 KB = 512 KB of the 1 GB working set, yielding a 0.05% hit rate.
The remaining 99.95% of accesses miss the IOTLB and require 600 ns page
table walks.

At 100 Gbps with 64-byte packets (worst case for packet processing), the
NIC processes \~194 million packets per second. If each packet touches
10 different pages on average (headers, payload, descriptors), that\'s
1.94 billion page translations per second. With a 99.95% miss rate,
that\'s 1.94 billion × 600 ns = 1,164 seconds of translation overhead
per second---obviously impossible, resulting in the NIC stalling
constantly while waiting for translations.

With 2 MB pages, the same 1 GB working set becomes 512 pages. The NIC\'s
128 IOTLB entries now cover 128 × 2 MB = 256 MB, yielding a 25.6% hit
rate---still not great but 500× better. More importantly, the NIC can
now operate without constant stalls. With 1 GB pages, the entire 1 GB
working set becomes a single page, and a single IOTLB entry covers
everything---100% hit rate, effectively zero translation overhead.

**How to Avoid:**

First, configure the kernel to use huge pages for device buffers:

``` {.sourceCode .bash}
# Enable transparent huge pages
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# For explicit huge pages, allocate them
echo 1024 > /proc/sys/vm/nr_hugepages  # 2 GB worth of 2MB pages
```

Second, ensure application allocations request huge pages:

``` {.sourceCode .c}
// C code for explicit huge pages
void *buffer = mmap(NULL, 1GB, PROT_READ | PROT_WRITE,
                   MAP_PRIVATE | MAP_ANONYMOUS | MAP_HUGETLB | MAP_HUGE_2MB,
                   -1, 0);

// Or rely on THP for regular allocations
void *buffer = malloc(1GB);  // THP may promote to huge pages
madvise(buffer, 1GB, MADV_HUGEPAGE);  // Encourage THP
```

**Detection and Monitoring:**

Monitor IOTLB miss rates to detect this issue:

``` {.sourceCode .bash}
# Use perf to measure IOMMU TLB misses (if exposed)
perf stat -e iommu_tlb_misses,iommu_page_walks ./workload

# Check for IOMMU-related stalls in device statistics
cat /sys/class/net/eth0/device/statistics/iommu_translation_stalls
```

If miss rates exceed 50%, huge pages are likely needed. If miss rates
exceed 90%, performance degradation is likely severe.

**Real-World Impact:** A financial services company enabled IOMMU across
their trading infrastructure for security compliance. NVMe SSD latency
increased from 50 µs to 150 µs, and IOPS dropped from 1.4M to 600K. The
culprit: 4 KB pages with 92% IOTLB miss rate. Switching to 2 MB pages
restored performance to within 5% of baseline, satisfying both security
and performance requirements.

#### Pitfall 2: Pinning Too Much Memory with RDMA

**The Problem:** Engineers pre-register large memory regions with RDMA
NICs to avoid registration overhead on every operation. But pinning 100+
GB per application on a 512 GB server means 20%+ of system RAM is locked
and unusable for other purposes. This wastes resources and limits
deployment flexibility.

**Root Cause Analysis:** RDMA registration pins memory to prevent the
kernel from moving pages (for compaction) or swapping them to disk. The
NIC stores physical addresses in its memory translation table, and those
addresses must remain valid for the duration of the registration. If the
kernel moved a page, the NIC would DMA to the wrong physical location,
corrupting memory.

Pre-registration is attractive because registration is expensive (50-200
ms for gigabytes due to page pinning, DMA table setup, and NIC
programming). Doing this once at startup amortizes the cost across
millions of operations. But the trade-off is memory efficiency.

Consider a key-value store handling 1 million concurrent connections,
each with a 1 MB buffer. Pre-registering all buffers requires 1 TB of
pinned memory. On a system with 512 GB RAM, this is impossible. Even
pre-registering a subset (say, 100 GB for the hottest connections)
wastes memory because the \"hot set\" changes over time. Connections
that were busy an hour ago may be idle now, but their buffers remain
pinned.

**How to Avoid:**

Use on-demand paging (ODP) for applications where: - Memory size is
large (100+ GB) - Access patterns are sparse (not all memory accessed
frequently) - Latency tolerance allows for occasional page faults
(50-100 µs acceptable)

``` {.sourceCode .c}
// Register with ODP flag
struct ibv_mr *mr = ibv_reg_mr(pd, buffer, size,
                               IBV_ACCESS_LOCAL_WRITE |
                               IBV_ACCESS_ON_DEMAND);  // No pinning!
```

For latency-sensitive applications, use hybrid approach: - Pre-register
critical hot path buffers (small, frequently accessed) - ODP for
everything else (large, infrequently accessed)

``` {.sourceCode .c}
// Hot path: pre-registered pool
void *hot_pool = malloc(10GB);
struct ibv_mr *hot_mr = ibv_reg_mr(pd, hot_pool, 10GB,
                                   IBV_ACCESS_LOCAL_WRITE);  // Pinned

// Cold path: ODP
struct ibv_mr *cold_mr = ibv_reg_mr(pd, NULL, 1TB,  // Virtual range
                                    IBV_ACCESS_ON_DEMAND);  // Not pinned
```

**Detection and Monitoring:**

Check pinned memory usage:

``` {.sourceCode .bash}
# Total pinned memory across all processes
grep "^VmLck:" /proc/*/status | awk '{sum+=$2} END {print sum/1024/1024 " GB"}'

# Per-application pinned memory
grep VmLck /proc/<pid>/status
```

Alert when pinned memory exceeds 20% of total RAM, indicating potential
waste.

**Real-World Impact:** A distributed database pinned 180 GB per node
(35% of 512 GB) for RDMA communication. When the company attempted to
deploy additional services on these nodes, memory pressure caused OOM
kills. Switching to ODP reduced pinned memory to 40 GB (8%) while
increasing p99.9 latency by only 80 µs (within SLA). This freed 140 GB ×
1,000 nodes = 140 TB of memory capacity without buying new hardware.

#### Pitfall 3: Ignoring Device Page Fault Latency

**The Problem:** On-demand paging (ODP) seems perfect in theory---no
pinning, flexible memory usage, kernel can swap pages. But in practice,
the first access to each page incurs a 50-100 µs page fault that can
violate latency SLAs for high-frequency workloads.

**Root Cause Analysis:** Device page faults are fundamentally slower
than CPU page faults. A CPU page fault on an unmapped page might take
1-2 µs (allocate page, update PTE, invalidate TLB). A device page fault
requires:

1.  Device detects unmapped page (ATC miss, translation request fails)
2.  Device sends Page Request message via PCIe (1-2 µs)
3.  IOMMU routes to CPU interrupt handler
4.  CPU page fault handler allocates page (0.5-1 µs)
5.  CPU updates page table entry
6.  CPU sends Page Response via IOMMU (1-2 µs)
7.  IOMMU forwards to device
8.  Device retries translation request
9.  Device caches translation in ATC
10. Device finally completes original operation

The PCIe round-trips (steps 2 and 6) add 2-4 µs. The interrupt handling
and message routing add another 1-2 µs. Total: 50-100 µs for the first
access to a page.

For a high-frequency trading system where 10 µs is already pushing
latency budgets, an additional 50-100 µs is catastrophic. For a
key-value store handling 1M operations/sec, if 10% trigger page faults,
that\'s 100K × 50 µs = 5 seconds of page fault overhead per
second---impossible to sustain.

**How to Avoid:**

For latency-critical paths, pre-fault pages to avoid runtime faults:

``` {.sourceCode .c}
// Allocate buffer
void *buffer = malloc(size);

// Pre-fault by touching every page
for (size_t i = 0; i < size; i += PAGE_SIZE) {
    ((char *)buffer)[i] = 0;  // Write to force allocation
}

// Now register with ODP - pages already allocated
struct ibv_mr *mr = ibv_reg_mr(pd, buffer, size, IBV_ACCESS_ON_DEMAND);
```

Alternatively, use mlock() to pre-allocate without pinning for RDMA:

``` {.sourceCode .c}
// Allocate and ensure pages are present
void *buffer = malloc(size);
mlock(buffer, size);  // Forces allocation
munlock(buffer, size);  // Allow swapping later

// Pages now allocated, ODP first access won't fault
struct ibv_mr *mr = ibv_reg_mr(pd, buffer, size, IBV_ACCESS_ON_DEMAND);
```

**Detection and Monitoring:**

Monitor device page fault rates:

``` {.sourceCode .bash}
# Check device page fault statistics (device-specific)
cat /sys/kernel/debug/mlx5/0000:03:00.0/page_fault_stats

# Example output:
#   total_faults: 12,456
#   faults_per_sec: 230
#   avg_fault_latency_us: 87
```

Alert when page faults exceed 100/sec or average latency exceeds 50 µs,
indicating the workload may not be suitable for ODP.

**Real-World Impact:** A machine learning training framework switched to
ODP to eliminate the 200 ms registration overhead when loading training
batches. But training throughput actually decreased by 15% because each
batch triggered hundreds of page faults as it accessed different pages.
The solution: pre-fault pages during batch loading (in parallel with
previous batch\'s computation) so that when the batch was ready, pages
were already allocated. This eliminated both registration overhead and
runtime page faults.

#### Pitfall 4: Not Batching TLB Invalidations

**The Problem:** Unmapping memory page-by-page sends individual TLB
invalidation messages to all devices for every page. On systems with 64
CPU cores + 10 devices, this means 74 invalidations per page. For a
10,000-page region, that\'s 740,000 invalidation operations taking
hundreds of milliseconds.

**Root Cause Analysis:** Each TLB invalidation has fixed overhead: - CPU
cores: Send IPI (\~100 ns per core), wait for acks (\~2 µs total) -
GPUs: PCIe transaction to device (\~1 µs), wait for GPU TLB flush (\~3
µs) - NICs: ATS Invalidation message (\~2 µs), wait for completion (\~1
µs) - IOMMU: Register write (\~0.5 µs), invalidation processing (\~1 µs)

Total per page: \~8 µs when done serially, or \~20 µs when done in
parallel (waiting for slowest device).

For 10,000 pages done individually: 10,000 × 20 µs = 200 ms. This blocks
the unmapping thread for 200 ms during which the application cannot
proceed. If this happens in a request processing path, it adds 200 ms to
request latency---completely unacceptable.

Modern hardware supports range-based invalidation (invalidate all pages
in address range X to Y with one command), but software must use it
explicitly.

**How to Avoid:**

Use range-based unmapping APIs:

``` {.sourceCode .c}
// BAD: Individual page unmaps
for (i = 0; i < 10000; i++) {
    munmap(addr + i * PAGE_SIZE, PAGE_SIZE);  // 10,000 separate invalidations!
}

// GOOD: Single range unmap
munmap(addr, 10000 * PAGE_SIZE);  // One batched invalidation
```

For device-specific operations, use range-based invalidation:

``` {.sourceCode .c}
// BAD: Individual IOTLB invalidations
for (i = 0; i < 10000; i++) {
    iommu_invalidate_page(addr + i * PAGE_SIZE);
}

// GOOD: Range invalidation
iommu_invalidate_range(addr, addr + 10000 * PAGE_SIZE);
```

**Detection and Monitoring:**

Check if applications are doing many small unmaps:

``` {.sourceCode .bash}
# Trace munmap calls
strace -e munmap -c ./application

# If you see thousands of small munmap calls, batching is needed
```

Use perf to measure TLB invalidation overhead:

``` {.sourceCode .bash}
perf stat -e tlb_invalidations,ipi_sent ./workload

# High tlb_invalidations (millions) indicates potential batching issue
```

**Real-World Impact:** A memory allocator used by a web server unmapped
freed memory in 4 KB increments to return it to the OS. Under heavy load
(1M requests/sec freeing memory), this generated 250,000 unmaps/sec. On
a system with 64 cores + IOMMU, each unmap took 20 µs = 5 seconds of TLB
invalidation overhead per second. The application was CPU-bound on TLB
invalidations! The fix: batch free operations and unmap 2 MB regions at
a time, reducing overhead by 512×.

#### Pitfall 5: Assuming Cache Coherency Exists

**The Problem:** Engineers assume that because CPU caches are coherent,
device accesses will automatically see CPU writes. But devices accessing
memory via PCIe don\'t participate in CPU cache coherency unless
explicitly designed to (like CCI-P/CCIX). This leads to subtle
corruption where devices read stale data.

**Root Cause Analysis:** CPU cache coherency operates within the CPU
complex (cores, cache controllers, interconnect). When CPU0 writes data,
the coherency protocol ensures CPU1 sees the new value by invalidating
or updating CPU1\'s cache line. But PCIe devices sit outside this
coherency domain.

When a CPU writes data that remains in cache (not yet written back to
DRAM), a device performing a PCIe read to that address reads from DRAM
and gets the old value. The device doesn\'t know there\'s a newer value
in CPU cache because it can\'t participate in the coherency snooping
protocol.

Consider this sequence: 1. CPU writes shared_data\[X\] = new_value
(value in CPU cache) 2. CPU signals device to process shared_data 3.
Device DMAs from shared_data\[X\] 4. Device reads old_value from DRAM
(cache not visible) 5. Device processes wrong data, produces incorrect
results

This is deterministic corruption that may not surface during testing (if
testing doesn\'t trigger the race) but causes mysterious failures in
production.

**How to Avoid:**

For shared data structures accessed by both CPU and devices:

Option 1: Explicit cache flush (x86-specific):

``` {.sourceCode .c}
// CPU writes data
shared_data[X] = new_value;

// Flush cache line to DRAM
clflushopt(&shared_data[X]);  // Optimized flush
_mm_sfence();  // Ensure flush completes

// Now device read will see new value
signal_device_to_process(X);
```

Option 2: Uncached memory mapping:

``` {.sourceCode .c}
// Allocate memory as uncached
void *shared = mmap(NULL, size, PROT_READ | PROT_WRITE,
                   MAP_SHARED | MAP_ANONYMOUS, -1, 0);

// Set memory type to uncached
set_memory_uc(shared, size);

// CPU writes bypass cache, device always sees current value
// Trade-off: Slower CPU access (100 ns vs 5 ns)
```

Option 3: Message passing (avoid sharing):

``` {.sourceCode .c}
// Don't share memory - use explicit messages

// CPU sends update to device
send_message_to_device(UPDATE_CMD, new_value);

// Device updates its own copy
device_receive_message();  // In device code
device_local_data = new_value;
```

**Detection and Monitoring:**

Coherency bugs are notoriously difficult to detect because they\'re race
conditions. Symptoms include: - Intermittent data corruption - Wrong
results that disappear when debugging (debugger adds delays) - Higher
failure rates on systems with larger caches - Failures that correlate
with CPU load (more cache retention)

Add assertions in device code:

``` {.sourceCode .c}
// Device code reads shared metadata
uint64_t version = shared_data->version;
uint64_t checksum = shared_data->checksum;

// Verify checksum matches
if (compute_checksum(shared_data) != checksum) {
    // Likely coherency issue - data doesn't match checksum
    report_coherency_error();
}
```

**Real-World Impact:** A Smart NIC implementation cached network flow
tables in host memory for CPU/NIC sharing. The CPU updated flow entries,
and the NIC read them for packet forwarding. Intermittent packet drops
occurred when the NIC read stale flow entries from DRAM while updated
entries sat in CPU cache. The NIC forwarded packets to wrong
destinations (\~0.001% of packets, but still thousands per second at 100
Gbps). The fix: Mark flow table memory as uncached, eliminating
coherency issues at the cost of slightly slower CPU updates (acceptable
since updates were infrequent).

#### Pitfall 6: Holding Locks While Waiting for Devices

**The Problem:** Code that acquires a lock, initiates a device
operation, waits for completion, then releases the lock creates deadlock
potential when devices can page fault or need to communicate with the
CPU.

**Root Cause Analysis:** Consider this scenario:

``` {.sourceCode .c}
// Thread A
spin_lock(&page_table_lock);
update_page_table(addr, new_pte);
invalidate_device_tlb(addr);  // Sends message to device
wait_for_device_ack();  // Waiting while holding lock!
spin_unlock(&page_table_lock);

// Device (handling request)
on_device_request() {
    page_fault_to_cpu(addr);  // Needs page allocated
    wait_for_page_fault_response();
}

// Page fault handler (different CPU)
on_device_page_fault() {
    spin_lock(&page_table_lock);  // DEADLOCK! Thread A holds this
    allocate_page(addr);
    // ...
}
```

Thread A holds page_table_lock and waits for device. Device triggers
page fault that needs Thread B to acquire page_table_lock. Thread B
waits for Thread A to release lock. Thread A waits for device. Device
waits for Thread B. Circular dependency = deadlock.

This is subtle because the lock (page_table_lock) and the device
operation seem unrelated. The deadlock manifests only when the device
happens to page fault at the wrong time.

**How to Avoid:**

Never hold locks while waiting for device responses:

``` {.sourceCode .c}
// CORRECT version
spin_lock(&page_table_lock);
update_page_table(addr, new_pte);
spin_unlock(&page_table_lock);  // Release BEFORE device operation

// Now safe to wait for device
invalidate_device_tlb(addr);
wait_for_device_ack();
```

Add timeouts to device waits to detect hung devices:

``` {.sourceCode .c}
if (!wait_for_device_ack_timeout(100ms)) {
    // Device didn't respond - don't deadlock forever
    log_error("Device timeout - possible deadlock or device failure");
    reset_device();  // Reset as recovery
    return -EIO;
}
```

**Detection and Monitoring:**

Deadlocks typically manifest as complete hangs: - Process stuck in D
state (uninterruptible sleep) - Watchdog timeouts - No progress on
operations

Use kernel lock debugging:

``` {.sourceCode .bash}
# Enable lock debugging
echo 1 > /proc/sys/kernel/lock_stat

# Check for lock contention
cat /proc/lock_stat | grep page_table_lock

# Long hold times (milliseconds) indicate potential issues
```

**Real-World Impact:** A GPU driver held a memory management lock while
invalidating GPU TLBs. When the GPU page faulted during invalidation
processing, the page fault handler tried to acquire the same lock,
deadlocking the system. The system would hard-hang randomly, requiring a
reboot. The issue took weeks to debug because it only happened when the
GPU page faulted during a specific window (microseconds) while
invalidations were in flight. The fix: Release the lock before sending
GPU invalidations, eliminating the deadlock possibility.

### Decision Framework

Choose IOMMU Configuration Based on Requirements:

**Security-Critical (Multi-Tenant Cloud):** - IOMMU: Enabled and
mandatory - Pages: 2 MB minimum, 1 GB for high-bandwidth devices -
Passthrough: Never allow (security violation) - Overhead: 5-15%
acceptable trade-off for isolation - Monitoring: Alert on passthrough
attempts, IOTLB miss rates \>50%

The security benefit outweighs performance cost because a single
VM-to-VM attack could compromise hundreds of customer VMs and destroy
business reputation.

**Performance-Critical (Single-Tenant HPC):** - IOMMU: Disabled or
passthrough mode - Security: Rely on physical isolation (no
multi-tenancy) - Overhead: 0% - Monitoring: Ensure firmware settings
match expectations

HPC environments control physical access and don\'t mix untrusted
workloads, making IOMMU overhead unnecessary.

**Balanced (Enterprise Data Centers):** - IOMMU: Enabled with selective
passthrough - Critical devices: Passthrough (storage, internal NICs) -
Untrusted devices: IOMMU with huge pages (external NICs, GPUs) -
Overhead: 3-8% acceptable for mixed environment - Monitoring: Track both
security and performance metrics

Most enterprise environments fall here, balancing security and
performance based on threat model.

Choose Memory Registration Strategy:

**Static Workload (Known Buffers at Startup):** - Use: Pre-registration
of fixed buffer pool - Example: Database buffer cache, video frame
buffers - Trade-off: Memory pinned but zero runtime cost - Size:
Pre-register 50-80% of expected working set

Pre-registration works when workload characteristics are predictable and
memory requirements are stable.

**Dynamic Workload (Unknown Buffers):** - Use: On-demand paging (ODP) -
Example: Key-value store with variable-size values, microservices with
dynamic memory - Trade-off: Flexible memory use, 50-100 µs first-access
latency - Mitigation: Pre-fault for latency-critical paths

ODP enables workloads that can\'t predict memory requirements in
advance.

**Mixed Workload:** - Use: Hybrid (pre-register hot paths + ODP for
cold) - Example: Web server (templates pre-registered, user data ODP) -
Trade-off: Complexity in deciding what to pre-register - Monitoring:
Track cache hit rates to optimize split

Most real systems benefit from hybrid approaches that match strategy to
access patterns.

### Looking Forward

The boundary between CPU and device memory management continues to blur,
driven by several technology trends:

**Unified Virtual Addressing (UVA)** becoming standard across devices.
NVIDIA\'s Unified Memory already provides single address space across
CPU and GPU with automatic migration. Intel\'s oneAPI Level Zero extends
this to FPGAs and AI accelerators. The goal: same virtual address works
everywhere, with hardware transparently moving data where needed.

**CXL (Compute Express Link)** promises cache-coherent device memory at
memory interface speeds. Unlike PCIe which operates at I/O speeds
(microseconds), CXL operates at memory speeds (100s of nanoseconds).
Devices become cache-coherent by default, eliminating explicit cache
flush requirements.

**Device-Side Page Tables** becoming more sophisticated. Current devices
have simple TLB structures (flat tables with limited associativity).
Future devices will have hierarchical TLBs matching CPU complexity,
prefetchers that anticipate access patterns, and speculative translation
that begins walks before knowing if they\'re needed.

**Zero-Copy Everything** as the architectural default. The performance
cost of copying data (10-50 µs for megabytes) is becoming unacceptable
as device speeds increase. 100 Gbps NICs become 400 Gbps, then 1.6 Tbps.
The time to copy even a few megabytes exceeds network transmission time.
Future systems will default to shared memory everywhere, with explicit
copies only when demonstrably necessary.

### References

**PCIe and Device Specifications:**

PCI-SIG. (2019). *PCI Express Base Specification Revision 5.0*. PCI
Special Interest Group. Defines the PCIe protocol including ATS (Address
Translation Services), PRI (Page Request Interface), and PASID (Process
Address Space ID) extensions that enable device-side caching and page
fault handling.

PCI-SIG. (2020). *Address Translation Services Revision 1.1*. PCI
Special Interest Group. Specification for device-side translation
caching, including ATC structure, invalidation protocol, and PASID
support.

**Intel VT-d (IOMMU) Documentation:**

Intel Corporation. (2023). *Intel Virtualization Technology for Directed
I/O (VT-d): Architecture Specification, Revision 4.1*. Document Number:
D51397-017. Comprehensive specification covering root/context table
structures, IOTLB organization, page table formats, and interrupt
remapping. Available at:
https://software.intel.com/content/www/us/en/develop/articles/intel-virtualization-technology-for-directed-io-vt-d-spec.html

Intel Corporation. (2023). *Intel 64 and IA-32 Architectures Software
Developer\'s Manual, Volume 3D: System Programming Guide, Part 4*.
Document Number: 332831-076US. Chapter on VT-d programming interface,
register definitions, and performance optimization.

**AMD IOMMU (AMD-Vi) Documentation:**

AMD Corporation. (2022). *AMD I/O Virtualization Technology (IOMMU)
Specification, Revision 3.07-PUB*. Publication Number: 48882. AMD\'s
IOMMU architecture covering device table structure, per-device IOTLBs,
and differences from Intel VT-d. Available at:
https://www.amd.com/content/dam/amd/en/documents/processor-tech-docs/specifications/48882_IOMMU.pdf

**ARM SMMU Documentation:**

ARM Limited. (2020). *ARM System Memory Management Unit Architecture
Specification, SMMUv3*. Document Number: ARM IHI 0070E. Specification
for ARM\'s IOMMU covering stream tables, two-stage translation for
virtualization, and TLB hierarchy.

**RDMA and Networking:**

Mellanox Technologies. (2020). *ConnectX-6 Ethernet Adapter Card User
Manual, Rev 1.0*. Document Number: 1365560. Covers ATS support,
on-demand paging implementation, and memory registration optimization in
modern RDMA NICs.

Mittal, R., Shpiner, A., Panda, A., Zahavi, E., Krishnamurthy, A.,
Ratnasamy, S., & Shenker, S. (2018). *Revisiting Network Support for
RDMA*. Proceedings of ACM SIGCOMM 2018, pp. 313-326.
doi:10.1145/3230543.3230557. Analysis of RDMA performance
characteristics including memory registration overhead and on-demand
paging trade-offs.

**FPGA Coherent Interconnect:**

Intel Corporation. (2019). *Intel Accelerator Functional Unit (AFU)
Developer\'s Guide for Intel FPGA Programmable Acceleration Card*.
Document Number: 683129. Covers CCI-P (Core Cache Interface) protocol
for cache-coherent FPGA-CPU communication.

CCIX Consortium. (2018). *CCIX Base Specification, Revision 1.0*. Cache
Coherent Interconnect for Accelerators specification defining coherency
protocol over PCIe physical layer.

**Smart NICs and DPUs:**

NVIDIA Corporation. (2021). *NVIDIA BlueField-2 DPU Data Sheet*.
Document Number: DS-09625-001_v1.0. Hardware specifications and
architectural overview of DPU with embedded ARM cores, including host
memory access mechanisms.

Kaufmann, A., Peter, S., Anderson, T., & Krishnamurthy, A. (2015).
*FlexNIC: Rethinking Network DMA*. Proceedings of ACM HotOS XV. Explores
Smart NIC architectures and host memory access patterns.

**Academic Research:**

Basu, A., Gandhi, J., Chang, J., Hill, M. D., & Swift, M. M. (2013).
*Efficient Virtual Memory for Big Memory Servers*. Proceedings of ISCA
2013, pp. 237-248. doi:10.1145/2485922.2485943. Analysis of page table
overhead in systems with large memory, motivating huge pages and reduced
page table structures.

Amit, N., Ben-Yehuda, M., & Yassour, B. (2011). *IOMMU: Strategies for
Mitigating the IOTLB Bottleneck*. Workshop on I/O Virtualization (WIOV
\'11). Analysis of IOTLB performance characteristics and optimization
strategies.

Markuze, A., Smolyar, I., Morrison, A., & Tsafrir, D. (2016). *True
IOMMU Protection from DMA Attacks: When Copy is Faster than Zero Copy*.
Proceedings of ASPLOS 2016, pp. 249-262. doi:10.1145/2872362.2872379.
Demonstrates scenarios where copying data is faster than zero-copy with
IOMMU due to translation overhead.

Willmann, P., Rixner, S., & Cox, A. L. (2006). *An Evaluation of Network
Stack Parallelization Strategies in Modern Operating Systems*.
Proceedings of USENIX ATC 2006. Early analysis of device DMA patterns
and their impact on memory management.

**Industry Technical Blogs and Whitepapers:**

Tsirkin, M. S. (2015). \"vhost-net and virtio-net: Bypassing the
IOMMU.\" *KVM Forum 2015*. Discusses IOMMU bypass techniques in
virtualization.

Bjørling, M., González, J., & Bonnet, P. (2017). \"LightNVM: The Linux
Open-Channel SSD Subsystem.\" *FAST 2017*, pp. 359-374. Case study of
NVMe SSD performance with and without IOMMU.

NVIDIA Developer Blog. (2019). \"CUDA Unified Memory and Page Migration
Engine.\" Covers GPU page fault handling and automatic memory migration
between CPU and GPU.

**Performance Analysis Tools:**

Gregg, B. (2019). *BPF Performance Tools: Linux System and Application
Observability*. Addison-Wesley. ISBN: 978-0136554820. Covers tools for
measuring IOMMU overhead, TLB shootdowns, and device DMA patterns.

Intel Corporation. (2023). \"Intel Performance Counter Monitor (PCM).\"
Open-source tool for measuring PCIe bandwidth, IOMMU activity, and
memory controller traffic. Available at: https://github.com/opcm/pcm

**Standards Organizations:**

JEDEC Solid State Technology Association. (2020). *High Bandwidth Memory
(HBM) DRAM Standard, JESD235C*. Memory standard relevant to device
memory architectures discussed in Chapter 11.

IEEE Computer Society. (2019). *IEEE Std 1003.1-2017: POSIX.1-2017*.
System interfaces including mlock(), mmap(), and memory management APIs
used for device memory registration.

------------------------------------------------------------------------

**End of Chapter 10**

This chapter examined how devices access the memory management unit to
participate in virtual memory. We explored the IOMMU\'s role in
providing per-device isolation, saw how ATS enables device-side caching,
understood the tension between RDMA\'s need for stable addresses and
virtual memory\'s flexibility, examined how Smart NICs and FPGAs access
host memory with different performance characteristics, and learned to
coordinate memory operations across dozens of devices safely.

Chapter 11 extends these concepts to AI/ML accelerators where memory
bandwidth reaches 3-5 TB/s and capacity extends to 192 GB per device.
The challenges intensify---the Google TPU\'s systolic arrays demand
predictable memory access patterns, NVIDIA\'s Unified Memory must decide
whether to migrate pages between CPU and GPU, Intel Habana\'s RDMA
integration must coordinate with external devices, and Apple\'s unified
memory must balance competing demands from CPU, GPU, and Neural Engine.

The techniques from this chapter provide the foundation for
understanding these specialized accelerators. The IOMMU mechanisms
enable GPU compute via PCIe. The coherency protocols we examined extend
to GPU caches. The TLB invalidation coordination becomes even more
critical when training deep learning models across 1,000+ GPUs. Let\'s
turn to these extreme memory systems and understand how they push the
boundaries of what\'s possible.
