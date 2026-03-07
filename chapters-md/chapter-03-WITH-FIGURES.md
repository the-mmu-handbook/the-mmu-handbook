# Chapter 3: Page Table Structures and Implementation

- [Chapter 3: Page Table Structures and
  Implementation](#chapter-3-page-table-structures-and-implementation){#toc-chapter-3-page-table-structures-and-implementation}
  - [3.1 Introduction](#3.1-introduction){#toc-3.1-introduction}
    - [Why Page Table Design
      Matters](#why-page-table-design-matters){#toc-why-page-table-design-matters}
    - [The Evolution: From Simple to
      Sophisticated](#the-evolution-from-simple-to-sophisticated){#toc-the-evolution-from-simple-to-sophisticated}
    - [What This Chapter
      Covers](#what-this-chapter-covers){#toc-what-this-chapter-covers}
    - [A Note on Architecture
      Coverage](#a-note-on-architecture-coverage){#toc-a-note-on-architecture-coverage}
    - [Roadmap for Part 2](#roadmap-for-part-2){#toc-roadmap-for-part-2}
  - [3.2 Single-Level Page Tables: The Simplest
    Approach](#3.2-single-level-page-tables-the-simplest-approach){#toc-3.2-single-level-page-tables-the-simplest-approach}
    - [3.2.1 Structure and
      Mechanics](#3.2.1-structure-and-mechanics){#toc-3.2.1-structure-and-mechanics}
    - [3.2.2 Size Calculations and Memory
      Overhead](#3.2.2-size-calculations-and-memory-overhead){#toc-3.2.2-size-calculations-and-memory-overhead}
    - [3.2.3 Advantages and When Single-Level Tables Make
      Sense](#3.2.3-advantages-and-when-single-level-tables-make-sense){#toc-3.2.3-advantages-and-when-single-level-tables-make-sense}
    - [3.2.4 Fundamental
      Limitations](#3.2.4-fundamental-limitations){#toc-3.2.4-fundamental-limitations}
  - [3.3 Two-Level Page
    Tables](#3.3-two-level-page-tables){#toc-3.3-two-level-page-tables}
    - [3.3.1 The Hierarchical
      Structure](#3.3.1-the-hierarchical-structure){#toc-3.3.1-the-hierarchical-structure}
    - [3.3.2 x86 32-bit Example: The Classic
      Implementation](#3.3.2-x86-32-bit-example-the-classic-implementation){#toc-3.3.2-x86-32-bit-example-the-classic-implementation}
    - [3.3.3 Translation Walkthrough with Concrete
      Example](#3.3.3-translation-walkthrough-with-concrete-example){#toc-3.3.3-translation-walkthrough-with-concrete-example}
    - [3.3.4 Memory Savings
      Analysis](#3.3.4-memory-savings-analysis){#toc-3.3.4-memory-savings-analysis}
    - [3.3.5 The Cost: Translation
      Complexity](#3.3.5-the-cost-translation-complexity){#toc-3.3.5-the-cost-translation-complexity}
    - [3.3.6 Transition to More
      Levels](#3.3.6-transition-to-more-levels){#toc-3.3.6-transition-to-more-levels}
  - [3.4 Multi-Level Page Tables (3+
    Levels)](#3.4-multi-level-page-tables-3-levels){#toc-3.4-multi-level-page-tables-3-levels}
    - [3.4.1 x86-64 Four-Level Paging: The Current
      Standard](#3.4.1-x86-64-four-level-paging-the-current-standard){#toc-3.4.1-x86-64-four-level-paging-the-current-standard}
    - [3.4.2 x86-64 Five-Level Paging: Expanding to 128
      PB](#3.4.2-x86-64-five-level-paging-expanding-to-128-pb){#toc-3.4.2-x86-64-five-level-paging-expanding-to-128-pb}
    - [3.4.3 ARM64 Page Table
      Structures](#3.4.3-arm64-page-table-structures){#toc-3.4.3-arm64-page-table-structures}
    - [3.4.4 RISC-V Page Table
      Structures](#3.4.4-risc-v-page-table-structures){#toc-3.4.4-risc-v-page-table-structures}
    - [3.4.5 Translation Process
      Summary](#3.4.5-translation-process-summary){#toc-3.4.5-translation-process-summary}
  - [3.6 Virtualization: Two-Stage Address
    Translation](#3.6-virtualization-two-stage-address-translation){#toc-3.6-virtualization-two-stage-address-translation}
    - [3.6.2 Intel EPT (Extended Page
      Tables)](#3.6.2-intel-ept-extended-page-tables){#toc-3.6.2-intel-ept-extended-page-tables}
    - [3.6.3 AMD NPT (Nested Page
      Tables)](#3.6.3-amd-npt-nested-page-tables){#toc-3.6.3-amd-npt-nested-page-tables}
    - [3.6.4 ARM Stage 2
      Translation](#3.6.4-arm-stage-2-translation){#toc-3.6.4-arm-stage-2-translation}
    - [3.6.5 RISC-V Hypervisor
      Extension](#3.6.5-risc-v-hypervisor-extension){#toc-3.6.5-risc-v-hypervisor-extension}
    - [3.6.6 Performance Impact and
      Mitigations](#3.6.6-performance-impact-and-mitigations){#toc-3.6.6-performance-impact-and-mitigations}
    - [3.6.7 Why Two Stages
      Matter](#3.6.7-why-two-stages-matter){#toc-3.6.7-why-two-stages-matter}
  - [3.7 What Gets Cached: TLB and Page Walk
    Caches](#3.7-what-gets-cached-tlb-and-page-walk-caches){#toc-3.7-what-gets-cached-tlb-and-page-walk-caches}
    - [3.7.1 Translation Lookaside Buffer (TLB): Final Translation
      Cache](#3.7.1-translation-lookaside-buffer-tlb-final-translation-cache){#toc-3.7.1-translation-lookaside-buffer-tlb-final-translation-cache}
    - [3.7.2 Page Walk Caches: The Hidden
      Optimization](#3.7.2-page-walk-caches-the-hidden-optimization){#toc-3.7.2-page-walk-caches-the-hidden-optimization}
    - [3.7.3 Caching in Virtualization: Combined
      TLB](#3.7.3-caching-in-virtualization-combined-tlb){#toc-3.7.3-caching-in-virtualization-combined-tlb}
    - [3.7.4 What Is NOT Cached: Important
      Clarifications](#3.7.4-what-is-not-cached-important-clarifications){#toc-3.7.4-what-is-not-cached-important-clarifications}
    - [3.7.5 Caching Hierarchy Summary
      Table](#3.7.5-caching-hierarchy-summary-table){#toc-3.7.5-caching-hierarchy-summary-table}
    - [3.7.6 Performance
      Implications](#3.7.6-performance-implications){#toc-3.7.6-performance-implications}
  - [3.8 Hardware Page Table
    Walker](#3.8-hardware-page-table-walker){#toc-3.8-hardware-page-table-walker}
    - [3.8.1 The Page Walk State
      Machine](#3.8.1-the-page-walk-state-machine){#toc-3.8.1-the-page-walk-state-machine}
    - [3.8.2 Hardware-Managed vs Software-Managed
      Bits](#3.8.2-hardware-managed-vs-software-managed-bits){#toc-3.8.2-hardware-managed-vs-software-managed-bits}
    - [3.8.3 Performance
      Characteristics](#3.8.3-performance-characteristics){#toc-3.8.3-performance-characteristics}
  - [3.9 Page Table Management from the OS
    Perspective](#3.9-page-table-management-from-the-os-perspective){#toc-3.9-page-table-management-from-the-os-perspective}
    - [3.9.1 Process Creation and Page Table
      Allocation](#3.9.1-process-creation-and-page-table-allocation){#toc-3.9.1-process-creation-and-page-table-allocation}
    - [3.9.2 Copy-on-Write (COW) and
      Fork](#3.9.2-copy-on-write-cow-and-fork){#toc-3.9.2-copy-on-write-cow-and-fork}
    - [3.9.3 Transparent Huge Pages
      (THP)](#3.9.3-transparent-huge-pages-thp){#toc-3.9.3-transparent-huge-pages-thp}
    - [3.9.4 Page Table
      Reclamation](#3.9.4-page-table-reclamation){#toc-3.9.4-page-table-reclamation}
  - [3.10 Design
    Trade-offs](#3.10-design-trade-offs){#toc-3.10-design-trade-offs}
    - [3.10.1 Memory Overhead vs Translation
      Speed](#3.10.1-memory-overhead-vs-translation-speed){#toc-3.10.1-memory-overhead-vs-translation-speed}
    - [3.10.2 Page Size
      Selection](#3.10.2-page-size-selection){#toc-3.10.2-page-size-selection}
    - [3.10.3 Hardware vs Software
      Complexity](#3.10.3-hardware-vs-software-complexity){#toc-3.10.3-hardware-vs-software-complexity}
    - [3.10.4 Virtualization
      Overhead](#3.10.4-virtualization-overhead){#toc-3.10.4-virtualization-overhead}
  - [3.11 Chapter
    Summary](#3.11-chapter-summary){#toc-3.11-chapter-summary}

## 3.1 Introduction {#3.1-introduction}

In the first two chapters, we established the fundamental concepts of
memory management and virtual memory. We explored how the Memory
Management Unit (MMU) provides the crucial abstraction layer between
virtual addresses---what programs see---and physical addresses---where
data actually resides in RAM. We introduced page tables as the data
structures that store these virtual-to-physical mappings, and we touched
on important optimization structures like the Translation Lookaside
Buffer (TLB) and multi-level page tables.

Now, in Part 2 of this book, we dive deep into the heart of virtual
memory systems: the page tables themselves. These deceptively simple
data structures represent one of the most critical design decisions in
computer architecture, influencing everything from memory overhead and
translation speed to security guarantees and virtualization
capabilities.

### Why Page Table Design Matters

The design of page table structures has far-reaching implications across
multiple dimensions:

**Performance**: Every memory access by a running program potentially
requires consulting the page tables. With modern processors executing
billions of instructions per second, even small inefficiencies in
address translation can significantly impact overall system performance.
The difference between a well-designed page table structure and a poor
one can mean the difference between 5% and 50% overhead in
memory-intensive applications. **Memory Overhead**: Page tables
themselves consume memory---sometimes substantial amounts. A naive
single-level page table for a 64-bit address space would require tens of
petabytes of memory just to store the mapping information! Practical
page table designs must balance the memory overhead of the tables
themselves against the efficiency of the translation process.
**Security**: Page tables are the primary mechanism for memory
protection in modern systems. They enforce process isolation, preventing
programs from reading or modifying each other\'s memory. They enable key
security features like the NX (No Execute) bit that prevents code
execution from data pages, mitigating entire classes of exploits. The
robustness of these protections depends critically on page table design
and implementation. **Virtualization**: Modern cloud computing relies on
virtualization, where multiple guest operating systems run
simultaneously on shared hardware. This introduces a new layer of
complexity: guest operating systems manage their own page tables
(translating guest virtual addresses to what they perceive as physical
addresses), while the hypervisor must translate these \"guest physical
addresses\" to actual physical addresses. This two-stage translation
process doubles the complexity of address translation and places new
demands on page table structures.

### The Evolution: From Simple to Sophisticated

Page table design has evolved dramatically over the past five decades:

**The 1960s-1970s**: Early virtual memory systems like the Atlas
computer and later the VAX-11 used simple, single-level page tables.
With 32-bit or smaller address spaces, this straightforward approach was
practical---a 32-bit address space with 4KB pages requires only 2\^20
(about 1 million) page table entries. **The 1980s-1990s**: As address
spaces grew and memory became cheaper but still finite, multi-level page
tables became standard. The 32-bit x86 architecture introduced two-level
tables, and this hierarchical approach allowed systems to allocate page
table memory only for regions of the address space actually in use.
**The 2000s**: The transition to 64-bit computing posed new challenges.
A naive single-level page table for a 64-bit address space would be
impossibly large. Modern x86-64 processors use four-level page tables,
and recent models support five levels. The introduction of hardware
virtualization support (Intel EPT and AMD NPT) added the complexity of
two-stage address translation. **The 2010s-Present**: Contemporary
systems face new pressures from big data workloads, virtualized cloud
environments, and security threats. Innovations like huge pages (2MB and
1GB mappings), transparent huge page support, and increasingly
sophisticated TLB designs reflect the ongoing optimization of page table
structures for modern workloads.

### What This Chapter Covers

In this chapter, we will systematically explore page table structures
from simple to complex, always grounding our discussion in real-world
implementations:

**Single-Level Page Tables (Section 3.2)**: We begin with the simplest
approach, examining why it works for small address spaces and
understanding its fundamental limitations. We\'ll look at historical
systems like the VAX-11 and modern embedded systems that still use this
approach. **Two-Level Page Tables (Section 3.3)**: We\'ll examine how a
second level of indirection dramatically reduces memory overhead, using
the 32-bit x86 architecture as our primary example. This section
includes detailed address translation examples with concrete numbers.
**Multi-Level Page Tables (Section 3.4)**: This is where we get into the
details of modern architectures. We\'ll cover:

- x86-64\'s four-level paging (the current standard) and five-level
  paging (Intel Ice Lake and later)
- ARM64\'s flexible page table configurations
- RISC-V\'s Sv39, Sv48, and Sv57 schemes

For each architecture, we\'ll examine the exact address format, register
usage, and translation process.

**Page Table Entry Deep Dive (Section 3.5)**: We\'ll dissect the
bit-level structure of page table entries across x86, ARM, and RISC-V
architectures, understanding how each bit affects memory access,
permissions, and system behavior. We\'ll explain the difference between
hardware-managed and software-managed bits, and how operating systems
leverage this structure. **Virtualization and Two-Stage Translation
(Section 3.6)**: One of the most important sections in this chapter,
here we tackle the complexities of running virtual machines. We\'ll
examine:

- How virtualization necessitates VA → IPA → PA translation
- Intel EPT (Extended Page Tables) implementation
- AMD NPT (Nested Page Tables)
- ARM Stage 2 translation
- RISC-V Hypervisor extension
- The performance implications of two-stage translation

**Caching and Performance (Section 3.7)**: Understanding what gets
cached is crucial for performance. We\'ll clarify:

- What the TLB caches (final translations) and what it doesn\'t
  (intermediate entries)
- Page Walk Caches (PWC) that cache intermediate page table entries
- Real TLB sizes from modern processors (Intel Skylake, AMD Zen 3, ARM
  Cortex-A77)
- How virtualization affects caching with VPID/ASID mechanisms

**Hardware Page Table Walker (Section 3.8)**: We\'ll examine the
hardware state machine that walks page tables on a TLB miss,
understanding the algorithm and its performance characteristics. **Page
Table Management (Section 3.9)**: From the OS perspective, we\'ll look
at how operating systems allocate, manage, and optimize page tables,
including techniques like copy-on-write and transparent huge pages.
**Design Trade-offs (Section 3.10)**: Finally, we\'ll step back and
analyze the fundamental trade-offs in page table design: memory overhead
versus translation speed, number of levels versus complexity, and page
size selection.

### A Note on Architecture Coverage

Throughout this chapter, we will focus on three major architecture
families that together represent the vast majority of computing devices
in use today:

**x86-64 (Intel and AMD)**: Dominates servers, desktops, and laptops.
We\'ll draw heavily from the Intel 64 and IA-32 Architectures Software
Developer\'s Manual and AMD\'s equivalent documentation. **ARM64
(ARMv8-A)**: Powers billions of smartphones, tablets, and increasingly,
servers (AWS Graviton, Apple M-series). We\'ll reference the ARM
Architecture Reference Manual. **RISC-V**: An emerging open-source
architecture with clean design and growing adoption. We\'ll use the
RISC-V Privileged Architecture Specification.

Each architecture offers unique insights into page table design, and by
comparing them, we\'ll develop a comprehensive understanding of the
design space and trade-offs involved.

### Roadmap for Part 2

This chapter is the first of several that will explore page tables in
depth:

- **Chapter 3** (this chapter): Page table structures and basic
  implementation
- **Chapter 4** (upcoming): Advanced page table optimizations and huge
  pages
- **Chapter 5** (upcoming): Page table performance and benchmarking

By the end of this chapter, you will have a thorough understanding of
how modern processors implement address translation, why they make the
design choices they do, and how these choices affect system performance,
security, and capability. You\'ll be able to read architecture manuals
with confidence, understand performance profiles of memory-intensive
applications, and make informed decisions about page size and memory
configuration in production systems.

Let\'s begin our detailed exploration of page table structures.

## 3.2 Single-Level Page Tables: The Simplest Approach {#3.2-single-level-page-tables-the-simplest-approach}

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="950" height="550" viewBox="0 0 950 550" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="475" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    Virtualization TLB with VPID/VMID Tagging
  </text>
  
  <!-- Traditional TLB (left side) -->
  <rect x="50" y="70" width="380" height="200" style="fill:#F5F5F5; stroke:#bdc3c7; stroke-width:2" />
  <text x="240" y="95" font-family="Arial, sans-serif" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">
    Traditional TLB (No Virtualization)
  </text>
  
  <rect x="70" y="120" width="340" height="130" style="fill:#ffffff; stroke:#95a5a6; stroke-width:1" />
  
  <!-- TLB Entry Structure -->
  <text x="80" y="145" font-family="Arial, sans-serif" style="fill:#1565C0; font-size:11; font-weight:bold">
    TLB Entry:
  </text>
  <rect x="90" y="155" width="120" height="30" style="fill:#1565C0; stroke:#2980b9; stroke-width:1" />
  <text x="150" y="175" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    VPN (Tag)
  </text>
  
  <rect x="220" y="155" width="40" height="30" style="fill:#9b59b6; stroke:#8e44ad; stroke-width:1" />
  <text x="240" y="175" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    ASID
  </text>
  
  <rect x="270" y="155" width="120" height="30" style="fill:#00796B; stroke:#229954; stroke-width:1" />
  <text x="330" y="175" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    PFN (Data)
  </text>
  
  <!-- Problem -->
  <text x="80" y="210" font-family="Arial, sans-serif" style="fill:#E65100; font-size:10; font-weight:bold">
    Problem with VMs:
  </text>
  <text x="90" y="228" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Different VMs may have same VPN
  </text>
  <text x="90" y="243" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • TLB flush needed on VM switch
  </text>
  
  <!-- Virtualization TLB (right side) -->
  <rect x="520" y="70" width="400" height="280" style="fill:#e8f8f5; stroke:#16a085; stroke-width:3" />
  <text x="720" y="95" font-family="Arial, sans-serif" style="fill:#16a085; font-size:14; font-weight:bold; text-anchor:middle">
    Virtualization TLB (With Tagging)
  </text>
  
  <rect x="540" y="120" width="360" height="210" style="fill:#ffffff; stroke:#16a085; stroke-width:1" />
  
  <!-- Extended TLB Entry -->
  <text x="550" y="145" font-family="Arial, sans-serif" style="fill:#16a085; font-size:11; font-weight:bold">
    TLB Entry with VPID/VMID:
  </text>
  
  <rect x="560" y="155" width="90" height="30" style="fill:#E65100; stroke:#c0392b; stroke-width:1" />
  <text x="605" y="175" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    VPID/VMID
  </text>
  
  <rect x="660" y="155" width="110" height="30" style="fill:#1565C0; stroke:#2980b9; stroke-width:1" />
  <text x="715" y="175" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    VPN (Tag)
  </text>
  
  <rect x="780" y="155" width="40" height="30" style="fill:#9b59b6; stroke:#8e44ad; stroke-width:1" />
  <text x="800" y="175" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    ASID
  </text>
  
  <rect x="830" y="155" width="50" height="30" style="fill:#00796B; stroke:#229954; stroke-width:1" />
  <text x="855" y="175" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    PFN
  </text>
  
  <!-- Example entries -->
  <text x="550" y="210" font-family="Arial, sans-serif" style="fill:#212121; font-size:10; font-weight:bold">
    Example Entries:
  </text>
  
  <!-- VM 1 entry -->
  <rect x="560" y="220" width="90" height="22" style="fill:#ffeaa7; stroke:#E65100; stroke-width:1" />
  <text x="605" y="235" font-family="Arial, sans-serif" style="fill:#212121; font-size:9; text-anchor:middle">
    VPID: 1
  </text>
  <rect x="660" y="220" width="110" height="22" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="715" y="235" font-family="Arial, sans-serif" style="fill:#212121; font-size:8; text-anchor:middle">
    VPN: 0x1000
  </text>
  <rect x="780" y="220" width="40" height="22" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="800" y="235" font-family="Arial, sans-serif" style="fill:#212121; font-size:8; text-anchor:middle">
    10
  </text>
  <rect x="830" y="220" width="50" height="22" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="855" y="235" font-family="Arial, sans-serif" style="fill:#212121; font-size:8; text-anchor:middle">
    0xA00
  </text>
  
  <!-- VM 2 entry (same VPN!) -->
  <rect x="560" y="250" width="90" height="22" style="fill:#1565C0; stroke:#1565C0; stroke-width:1" />
  <text x="605" y="265" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    VPID: 2
  </text>
  <rect x="660" y="250" width="110" height="22" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="715" y="265" font-family="Arial, sans-serif" style="fill:#212121; font-size:8; text-anchor:middle">
    VPN: 0x1000
  </text>
  <rect x="780" y="250" width="40" height="22" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="800" y="265" font-family="Arial, sans-serif" style="fill:#212121; font-size:8; text-anchor:middle">
    5
  </text>
  <rect x="830" y="250" width="50" height="22" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="855" y="265" font-family="Arial, sans-serif" style="fill:#212121; font-size:8; text-anchor:middle">
    0xB00
  </text>
  
  <!-- VM 1 different process -->
  <rect x="560" y="280" width="90" height="22" style="fill:#ffeaa7; stroke:#E65100; stroke-width:1" />
  <text x="605" y="295" font-family="Arial, sans-serif" style="fill:#212121; font-size:9; text-anchor:middle">
    VPID: 1
  </text>
  <rect x="660" y="280" width="110" height="22" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="715" y="295" font-family="Arial, sans-serif" style="fill:#212121; font-size:8; text-anchor:middle">
    VPN: 0x2000
  </text>
  <rect x="780" y="280" width="40" height="22" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="800" y="295" font-family="Arial, sans-serif" style="fill:#212121; font-size:8; text-anchor:middle">
    20
  </text>
  <rect x="830" y="280" width="50" height="22" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="855" y="295" font-family="Arial, sans-serif" style="fill:#212121; font-size:8; text-anchor:middle">
    0xC00
  </text>
  
  <text x="550" y="320" font-family="Arial, sans-serif" style="fill:#16a085; font-size:9; font-weight:bold">
    ✓ Same VPN, different VMs coexist!
  </text>
  
  <!-- Platform Support -->
  <rect x="50" y="300" width="860" height="220" style="fill:#ffffff; stroke:#1565C0; stroke-width:2" />
  <text x="480" y="330" font-family="Arial, sans-serif" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">
    Platform Support
  </text>
  
  <!-- Intel -->
  <rect x="70" y="350" width="250" height="150" style="fill:#e8f4fd; stroke:#1565C0; stroke-width:1" />
  <text x="195" y="375" font-family="Arial, sans-serif" style="fill:#1565C0; font-size:12; font-weight:bold; text-anchor:middle">
    Intel VT-x (VPID)
  </text>
  <text x="80" y="400" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • VPID: 16-bit identifier
  </text>
  <text x="80" y="420" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Stored in VMCS
  </text>
  <text x="80" y="440" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • TLB tagged: {VPID, ASID, VPN}
  </text>
  <text x="80" y="460" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Avoids flush on VM switch
  </text>
  <text x="80" y="480" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:9">
    → 10-15% hit rate improvement
  </text>
  
  <!-- ARM -->
  <rect x="350" y="350" width="250" height="150" style="fill:#f4e8fd; stroke:#9b59b6; stroke-width:1" />
  <text x="475" y="375" font-family="Arial, sans-serif" style="fill:#9b59b6; font-size:12; font-weight:bold; text-anchor:middle">
    ARM (VMID + ASID)
  </text>
  <text x="360" y="400" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • VMID: 8 or 16-bit
  </text>
  <text x="360" y="420" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • ASID: 8 or 16-bit
  </text>
  <text x="360" y="440" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • TLB: {VMID, ASID, VA} → PA
  </text>
  <text x="360" y="460" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Dual-level tagging
  </text>
  <text x="360" y="480" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:9">
    → Clean separation
  </text>
  
  <!-- RISC-V -->
  <rect x="630" y="350" width="260" height="150" style="fill:#e8fdf4; stroke:#00796B; stroke-width:1" />
  <text x="760" y="375" font-family="Arial, sans-serif" style="fill:#00796B; font-size:12; font-weight:bold; text-anchor:middle">
    RISC-V (VMID in hgatp)
  </text>
  <text x="640" y="400" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • VMID: 14-bit in hgatp
  </text>
  <text x="640" y="420" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • ASID: 16-bit in satp
  </text>
  <text x="640" y="440" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Combined tagging
  </text>
  <text x="640" y="460" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Supports nested virt
  </text>
  <text x="640" y="480" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:9">
    → Clean design
  </text>
  
  <!-- Benefit Note -->
  <text x="475" y="25" font-family="Arial, sans-serif" font-style="fill:#16a085; font-size:10">
    Key benefit: TLB entries from multiple VMs coexist → No flush on VM switch!
  </text>
</svg>
</div>
<figcaption><strong>Figure 3.intro:</strong> TLB with VPID/VMID tagging
for virtualization: each TLB entry carries a VM identifier, allowing
guest and host translations to coexist without full flushes on
VM-exit.</figcaption>
</figure>

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="750" viewBox="0 0 900 750" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="450" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    Page Walk Flowchart with Caching
  </text>
  
  <!-- Start: Memory Access -->
  <rect x="350" y="70" width="200" height="50" rx="25" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="450" y="100" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
    Memory Access (VA)
  </text>
  
  <!-- TLB Lookup -->
  <path d="M 450 120 L 450 160" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <polygon points="450,160 550,220 450,280 350,220" style="fill:#f39c12; stroke:#E65100; stroke-width:2"></polygon>
  <text x="450" y="215" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    TLB Hit?
  </text>
  <text x="450" y="235" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    (95-99%)
  </text>
  
  <!-- TLB Hit Path -->
  <path d="M 550 220 L 700 220" marker-end="url(#arrowhead)" style="fill:none; stroke:#00796B; stroke-width:3" />
  <text x="620" y="210" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold">
    YES
  </text>
  
  <rect x="700" y="195" width="180" height="50" rx="5" style="fill:#00796B; stroke:#229954; stroke-width:2" />
  <text x="790" y="220" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Access Physical
  </text>
  <text x="790" y="235" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    Memory (Done!)
  </text>
  
  <!-- TLB Miss Path -->
  <path d="M 450 280 L 450 320" marker-end="url(#arrowhead)" style="fill:none; stroke:#E65100; stroke-width:3" />
  <text x="460" y="305" font-family="Arial, sans-serif" style="fill:#E65100; font-size:11; font-weight:bold">
    NO (Miss)
  </text>
  
  <!-- PWC Level Check -->
  <rect x="320" y="320" width="260" height="60" style="fill:#9b59b6; stroke:#8e44ad; stroke-width:2" />
  <text x="450" y="345" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Check Page Walk Cache
  </text>
  <text x="450" y="365" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    PML4E / PDPTE / PDE cached?
  </text>
  
  <path d="M 450 380 L 450 420" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <!-- PWC Decision -->
  <polygon points="450,420 550,480 450,540 350,480" style="fill:#f39c12; stroke:#E65100; stroke-width:2"></polygon>
  <text x="450" y="475" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    PWC Hit?
  </text>
  <text x="450" y="495" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    (upper levels)
  </text>
  
  <!-- PWC Hit -->
  <path d="M 350 480 L 180 480" marker-end="url(#arrowhead)" style="fill:none; stroke:#00796B; stroke-width:2" />
  <text x="270" y="470" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold">
    YES
  </text>
  
  <rect x="20" y="455" width="160" height="50" rx="5" style="fill:#16a085; stroke:#138d75; stroke-width:2" />
  <text x="100" y="475" font-family="Arial, sans-serif" style="fill:white; font-size:11; font-weight:bold; text-anchor:middle">
    Skip to Cached
  </text>
  <text x="100" y="492" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    Level (Faster!)
  </text>
  
  <path d="M 100 505 L 100 600 L 450 600" marker-end="url(#arrowhead)" style="fill:none; stroke:#16a085; stroke-width:2" />
  
  <!-- PWC Miss -->
  <path d="M 450 540 L 450 580" marker-end="url(#arrowhead)" style="fill:none; stroke:#E65100; stroke-width:2" />
  <text x="460" y="565" font-family="Arial, sans-serif" style="fill:#E65100; font-size:11; font-weight:bold">
    NO
  </text>
  
  <!-- Full Walk -->
  <rect x="300" y="580" width="300" height="100" style="fill:#E65100; stroke:#c0392b; stroke-width:2" />
  <text x="450" y="605" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Full Page Table Walk
  </text>
  <text x="450" y="625" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    1. Read CR3 → PML4 base
  </text>
  <text x="450" y="643" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    2. Read PML4E → PDPT base
  </text>
  <text x="450" y="661" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    3. Read PDPTE → PD base
  </text>
  <text x="450" y="679" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    4. Read PDE → PT base
  </text>
  
  <!-- Read Final PTE -->
  <path d="M 450 680 L 450 710" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <rect x="640" y="585" width="240" height="80" style="fill:#95a5a6; stroke:#7f8c8d; stroke-width:2" />
  <text x="760" y="610" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Read Final PTE
  </text>
  <text x="760" y="630" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    Extract PFN
  </text>
  <text x="760" y="648" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    Check permissions
  </text>
  <text x="760" y="665" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    Set A/D bits
  </text>
  
  <path d="M 600 630 L 640 630" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <!-- Install in TLB -->
  <path d="M 760 665 L 760 695" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <rect x="660" y="695" width="200" height="40" rx="5" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="760" y="720" font-family="Arial, sans-serif" style="fill:white; font-size:11; font-weight:bold; text-anchor:middle">
    Install in TLB &amp; PWC
  </text>
  
  <!-- Final Access -->
  <path d="M 760 735 L 760 765 L 790 765 L 790 245" marker-end="url(#arrowhead)" style="fill:none; stroke:#00796B; stroke-width:2" />
  
  <!-- Performance Notes -->
  <rect x="20" y="70" width="280" height="100" style="fill:#fff9e6; stroke:#f39c12; stroke-width:2" />
  <text x="160" y="95" font-family="Arial, sans-serif" style="fill:#d68910; font-size:12; font-weight:bold; text-anchor:middle">
    Performance Impact
  </text>
  <text x="35" y="115" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • TLB hit: 0-1 cycles ⚡
  </text>
  <text x="35" y="133" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • PWC hit: 10-20 cycles
  </text>
  <text x="35" y="151" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Full walk: 100-250 cycles 🐌
  </text>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" style="fill:#34495e"></polygon>
    </marker>
  </defs>
</svg>
</div>
<figcaption><strong>Figure 3.walk:</strong> Page table walk flowchart
with TLB and page walk cache: a TLB hit returns the physical address
immediately; a miss triggers a hardware walk through up to four levels,
with intermediate levels cached in the page walk cache.</figcaption>
</figure>

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="400" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    Single-Level Page Table Structure
  </text>
  
  <!-- Virtual Address -->
  <g id="virtual-address">
    <rect x="50" y="70" width="300" height="60" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
    <text x="200" y="95" font-family="Arial, sans-serif" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">
      Virtual Address
    </text>
    
    <!-- Page Number section -->
    <rect x="50" y="70" width="200" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="150" y="115" font-family="Arial, sans-serif" style="fill:white; font-size:12; text-anchor:middle">
      Page Number
    </text>
    <text x="150" y="130" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
      (20 bits)
    </text>
    
    <!-- Offset section -->
    <rect x="250" y="70" width="100" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="300" y="115" font-family="Arial, sans-serif" style="fill:white; font-size:12; text-anchor:middle">
      Offset
    </text>
    <text x="300" y="130" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
      (12 bits)
    </text>
  </g>
  
  <!-- Arrow from Page Number to Page Table -->
  <path d="M 150 130 L 150 190" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <text x="160" y="165" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11">Index</text>
  
  <!-- PTBR Register -->
  <g id="ptbr">
    <rect x="450" y="70" width="300" height="40" style="fill:#E65100; stroke:#c0392b; stroke-width:2" />
    <text x="600" y="95" font-family="Arial, sans-serif" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">
      PTBR (CR3 / TTBR0 / satp)
    </text>
  </g>
  
  <!-- Arrow from PTBR to Page Table -->
  <path d="M 600 110 L 600 190" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <text x="610" y="155" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11">Points to base</text>
  
  <!-- Page Table -->
  <g id="page-table">
    <rect x="400" y="200" width="300" height="150" style="fill:#95a5a6; stroke:#7f8c8d; stroke-width:2" />
    <text x="550" y="225" font-family="Arial, sans-serif" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">
      Page Table
    </text>
    
    <!-- Page table entries -->
    <line x1="400" y1="240" x2="700" y2="240" style="stroke:white; stroke-width:1"></line>
    <text x="420" y="260" font-family="Arial, sans-serif" style="fill:white; font-size:11">Entry 0</text>
    <text x="630" y="260" font-family="Arial, sans-serif" style="fill:white; font-size:10">PFN: 0x1234</text>
    
    <line x1="400" y1="270" x2="700" y2="270" style="stroke:white; stroke-width:1"></line>
    <text x="420" y="290" font-family="Arial, sans-serif" style="fill:white; font-size:11">Entry 1</text>
    <text x="630" y="290" font-family="Arial, sans-serif" style="fill:white; font-size:10">PFN: 0x5678</text>
    
    <line x1="400" y1="300" x2="700" y2="300" style="stroke:white; stroke-width:1"></line>
    <text x="420" y="320" font-family="Arial, sans-serif" style="fill:white; font-size:11">...</text>
    
    <text x="550" y="340" font-family="Arial, sans-serif" style="fill:white; font-size:10">
      (2^20 = 1,048,576 entries)
    </text>
  </g>
  
  <!-- Arrow from Page Table to Physical Page -->
  <path d="M 500 350 L 220 365" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <text x="350" y="360" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11">PFN</text>
  
  <!-- Physical Memory -->
  <g id="physical-memory">
    <rect x="50" y="270" width="150" height="120" style="fill:#00796B; stroke:#229954; stroke-width:2" />
    <text x="125" y="290" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
      Physical Memory
    </text>
    <line x1="50" y1="300" x2="200" y2="300" style="stroke:white; stroke-width:1"></line>
    <text x="125" y="320" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">Page Frame 0</text>
    <line x1="50" y1="330" x2="200" y2="330" style="stroke:white; stroke-width:1"></line>
    <text x="125" y="350" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">Page Frame 1</text>
    <line x1="50" y1="360" x2="200" y2="360" style="stroke:white; stroke-width:1"></line>
    <text x="125" y="380" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">...</text>
  </g>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" style="fill:#34495e"></polygon>
    </marker>
  </defs>
</svg>
</div>
<figcaption><strong>Figure 3.1:</strong> Single-level page table: the
virtual page number (VPN) indexes directly into a flat array of PTEs.
Simple but impractical for 64-bit spaces — a 4 KB page size with 48-bit
VAs requires a 256 TB table.</figcaption>
</figure>

The single-level page table represents the most straightforward approach
to address translation. Conceptually, it\'s nothing more than a large
array where each entry maps one virtual page to one physical page.
Despite its simplicity---or perhaps because of it---understanding
single-level page tables provides the foundation for comprehending more
sophisticated designs.

### 3.2.1 Structure and Mechanics {#3.2.1-structure-and-mechanics}

In a single-level page table system, the virtual address is divided into
two parts:

1\. **Page number**: Used as an index into the page table

2\. **Page offset**: Identifies the byte within the page

For a system with 4KB (4096-byte) pages, the offset requires 12 bits
(since 2\^12 = 4096). The remaining high-order bits form the page
number. For a 32-bit address space, this gives us:

- Bits 31-12: Page number (20 bits)
- Bits 11-0: Page offset (12 bits)

The page number component provides 2\^20 = 1,048,576 possible pages,
meaning our page table needs exactly this many entries.

**The Page Table Base Register (PTBR)**

Every architecture that implements virtual memory includes a special
register that points to the base address of the current page table. When
the processor needs to translate a virtual address, it starts with this
register. The specific register varies by architecture:

**x86 Architecture**: Uses the CR3 register (Control Register 3), also
called the \"page table base register\" or PTBR in generic architectural
discussions. CR3 holds the physical address of the top-level page
directory. When the operating system switches processes (context
switch), it loads CR3 with the physical address of the new process\'s
page table structure. *Reference: Intel 64 and IA-32 Architectures
Software Developer\'s Manual, Volume 3A: System Programming Guide, Part
1, Section 4.2: \"Hierarchical Paging Structures: An Overview\"
describes CR3\'s role in address translation. Intel Corporation, 2024.*
**ARM Architecture**: Uses two translation table base registers for
flexibility:

- **TTBR0_EL1** (Translation Table Base Register 0, Exception Level 1):
  Typically used for user-space (application) virtual addresses
- **TTBR1_EL1** (Translation Table Base Register 1, Exception Level 1):
  Typically used for kernel-space virtual addresses

This dual-register approach allows ARM systems to maintain separate page
tables for user and kernel space, with independent switching. User
processes can switch (updating TTBR0) without touching kernel mappings
(TTBR1).

*Reference: ARM Architecture Reference Manual for ARMv8-A, Document DDI
0487J.a, Chapter D5: \"The AArch64 Virtual Memory System Architecture.\"
ARM Limited, 2024.* **RISC-V Architecture**: Uses the satp register
(Supervisor Address Translation and Protection). The satp register not
only contains the base address of the page table but also encodes the
paging mode (Sv39, Sv48, or Sv57) and an Address Space Identifier (ASID)
for TLB tagging.

Specifically, for RV64 (64-bit RISC-V):

- Bits 63-60: MODE (paging mode)
- Bits 59-44: ASID (Address Space Identifier)
- Bits 43-0: PPN (Physical Page Number of root page table)

*Reference: The RISC-V Instruction Set Manual, Volume II: Privileged
Architecture, Version 1.12, Section 4.1.11: \"Supervisor Address
Translation and Protection Register (satp).\" RISC-V International,
2021.* **Translation Process**

When the CPU needs to translate a virtual address using a single-level
page table, the process is straightforward:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
1\. Extract page number from virtual address (VA bits 31-12 for 32-bit,
4KB pages)

2\. Read base address from PTBR (CR3 on x86, TTBR0_EL1 on ARM, satp on
RISC-V)

3\. Calculate PTE address: PTE_address = PTBR + (page_number ×
entry_size)

4\. Read PTE from memory at PTE_address

5\. Extract physical page number from PTE

6\. Combine with page offset: PA = (physical_page_number \<\< 12) \|
page_offset

7\. Access physical memory at PA
:::

This process requires **one memory access** to read the page table entry
(assuming the PTBR is in a CPU register, which it is). If the
translation is not cached in the TLB, every memory access requires this
additional lookup, effectively doubling the number of memory accesses.

### 3.2.2 Size Calculations and Memory Overhead {#3.2.2-size-calculations-and-memory-overhead}

The memory overhead of single-level page tables is easy to calculate but
reveals the approach\'s fundamental limitation.

**32-bit Address Space Example**

Consider a classic 32-bit system with 4KB pages:

- Virtual address space: 2\^32 bytes = 4GB
- Page size: 4KB = 2\^12 bytes
- Number of pages: 4GB / 4KB = 2\^20 = 1,048,576 pages
- Page table entry size: Typically 4 bytes (32 bits) on 32-bit systems
- **Total page table size: 1,048,576 entries × 4 bytes = 4,194,304 bytes
  = 4MB**

This means every single process requires 4MB just for its page table,
regardless of how much memory the process actually uses. A process using
only 4KB of memory still needs a 4MB page table---a 1000:1 overhead
ratio!

**The VAX-11/780: A Historical Example**

The VAX-11/780, introduced by Digital Equipment Corporation in 1978,
provides an excellent historical example of single-level page tables in
practice. The VAX-11 architecture used:

- 32-bit virtual addresses
- 512-byte pages (much smaller than modern systems)
- Single-level page tables

With 512-byte pages, a 32-bit address space requires:

- Page number: 23 bits (bits 31-9)
- Page offset: 9 bits (bits 8-0)
- Number of PTEs: 2\^23 = 8,388,608 entries

At 4 bytes per entry, this would be 32MB per process---an enormous
amount in an era when the VAX-11/780 shipped with only 2MB to 8MB of
physical memory! In practice, the VAX used a clever optimization: the
virtual address space was divided into four regions (P0, P1, S0, S1),
each with its own page table. User processes used P0 and P1, which could
be much smaller than the full address space, making the overhead
manageable.

*Reference: Levy, H. M., & Lipman, P. H. (1982). \"Virtual memory
management in the VAX/VMS operating system.\" Computer, 15(3), 35-41.
This paper provides detailed insights into how the VAX/VMS operating
system managed page tables and optimized memory usage in a single-level
page table system.* **64-bit Address Space: The Impossibility**

To understand why single-level page tables don\'t scale to 64-bit
address spaces, let\'s do the arithmetic:

- Virtual address space: 2\^64 bytes = 16 exabytes
- Page size: 4KB = 2\^12 bytes
- Number of pages: 2\^64 / 2\^12 = 2\^52 = 4,503,599,627,370,496 pages
- Page table entry size: 8 bytes (64 bits) on 64-bit systems
- **Total page table size: 2\^52 entries × 8 bytes = 2\^55 bytes = 32
  petabytes**

To put this in perspective, 32 petabytes is:

- More than 1,000 times the total RAM in a well-equipped server (32GB
  typical)
- More than the total storage capacity of most data centers
- Clearly impossible!

Even if we used larger 2MB pages (21 bits for offset):

- Number of pages: 2\^64 / 2\^21 = 2\^43 pages
- Page table size: 2\^43 × 8 bytes = 64 terabytes

Still impossibly large. This calculation alone demonstrates why
multi-level page tables are absolutely necessary for 64-bit computing.

### 3.2.3 Advantages and When Single-Level Tables Make Sense {#3.2.3-advantages-and-when-single-level-tables-make-sense}

Despite their limitations, single-level page tables have some
advantages:

**Simplicity**: The translation algorithm is trivial. There\'s only one
memory access (to fetch the PTE), and no complex tree traversal.
**Predictable Performance**: Every translation takes exactly the same
time---one memory access. There are no worst-case scenarios where deeply
nested page tables create variable latency. **Fast Context Switching**:
Switching page tables only requires updating a single register
(PTBR/CR3/TTBR/satp). No complex page table structures need to be
manipulated. **Cache Friendly**: Since the entire page table is
contiguous in memory, it benefits from spatial locality. Sequential
address translations access nearby PTEs, which may be cached together.
**When They\'re Still Used Today**

Single-level page tables remain practical in specific scenarios:

**Small Address Spaces**: Embedded systems with limited address spaces
(e.g., 16-bit or small 32-bit systems) where the page table fits
comfortably in available memory. **Real-Time Systems**: Where
predictable, constant-time translation latency is more important than
memory efficiency. Some safety-critical embedded systems prefer
single-level tables because their behavior is completely predictable.
**Hardware Accelerators**: Some specialized processors (GPUs, DSPs) with
limited memory management capabilities use simplified single-level
schemes. **Educational Systems**: Teaching operating systems often
implement single-level tables first because they\'re easiest to
understand and implement.

### 3.2.4 Fundamental Limitations {#3.2.4-fundamental-limitations}

The fatal flaw of single-level page tables is the **complete page table
problem**: the page table must be fully allocated even if only a tiny
fraction of the virtual address space is actually used.

**Sparse Address Space Inefficiency**

Modern programs have sparse memory usage patterns. A typical application
might use:

- A few hundred KB for code (text segment)
- A few MB for static data (data and BSS segments)
- Several KB for the stack
- Variable amounts for the heap (dynamic allocation)

These regions are typically scattered across a 4GB (32-bit) or larger
address space, with vast empty regions between them. Yet a single-level
page table allocates entries for every possible page in the address
space, including all the unused regions.

**Example: Small Program on 32-bit System**

Consider a minimal \"Hello, World\" program:

- Code: 4KB (1 page)
- Data: 4KB (1 page)
- Stack: 8KB (2 pages)
- Heap: 0 KB (program doesn\'t allocate)
- **Total memory used: 16KB (4 pages)**

With single-level page tables:

- **Page table size: 4MB** (for all 2\^20 possible pages)
- **Overhead ratio: 4MB / 16KB = 256:1**

The page table is 256 times larger than the program\'s actual memory
usage! This is clearly unsustainable as systems scale.

**Transition to Multi-Level Tables**

This limitation drove the development of hierarchical page table
structures, which we\'ll examine in the next section. The key insight:
if we can avoid allocating page table entries for unused regions of the
address space, we can dramatically reduce memory overhead while
maintaining the virtual memory abstraction.

The single-level page table, despite its limitations, teaches us the
fundamental mechanics of address translation. Every more sophisticated
page table structure builds on these basics, adding levels of
indirection to solve the memory overhead problem while preserving the
elegance of the virtual-to-physical mapping concept.

## 3.3 Two-Level Page Tables {#3.3-two-level-page-tables}

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="500" viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="450" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    Two-Level Page Table Structure (x86 32-bit)
  </text>
  
  <!-- Virtual Address -->
  <g id="virtual-address">
    <rect x="50" y="70" width="400" height="60" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
    <text x="250" y="95" font-family="Arial, sans-serif" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">
      Virtual Address (32 bits)
    </text>
    
    <!-- PD Index -->
    <rect x="50" y="70" width="150" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="125" y="110" font-family="Arial, sans-serif" style="fill:white; font-size:11; text-anchor:middle">
      PD Index
    </text>
    <text x="125" y="125" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
      (10 bits)
    </text>
    
    <!-- PT Index -->
    <rect x="200" y="70" width="150" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="275" y="110" font-family="Arial, sans-serif" style="fill:white; font-size:11; text-anchor:middle">
      PT Index
    </text>
    <text x="275" y="125" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
      (10 bits)
    </text>
    
    <!-- Offset -->
    <rect x="350" y="70" width="100" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="400" y="110" font-family="Arial, sans-serif" style="fill:white; font-size:11; text-anchor:middle">
      Offset
    </text>
    <text x="400" y="125" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
      (12 bits)
    </text>
  </g>
  
  <!-- CR3 Register -->
  <g id="cr3">
    <rect x="550" y="70" width="200" height="40" style="fill:#E65100; stroke:#c0392b; stroke-width:2" />
    <text x="650" y="95" font-family="Arial, sans-serif" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">
      CR3 Register
    </text>
  </g>
  
  <!-- Arrow from CR3 to Page Directory -->
  <path d="M 650 110 L 650 170" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <!-- Arrow from PD Index to Page Directory -->
  <path d="M 125 130 L 125 170" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <text x="135" y="155" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">Index</text>
  
  <!-- Page Directory -->
  <g id="page-directory">
    <rect x="500" y="180" width="300" height="140" style="fill:#9b59b6; stroke:#8e44ad; stroke-width:2" />
    <text x="650" y="205" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
      Page Directory
    </text>
    
    <line x1="500" y1="220" x2="800" y2="220" style="stroke:white; stroke-width:1"></line>
    <text x="520" y="240" font-family="Arial, sans-serif" style="fill:white; font-size:10">PDE 0</text>
    <text x="700" y="240" font-family="Arial, sans-serif" style="fill:white; font-size:9">→ PT address</text>
    
    <line x1="500" y1="250" x2="800" y2="250" style="stroke:white; stroke-width:1"></line>
    <text x="520" y="270" font-family="Arial, sans-serif" style="fill:white; font-size:10">PDE 1</text>
    <text x="700" y="270" font-family="Arial, sans-serif" style="fill:white; font-size:9">→ PT address</text>
    
    <line x1="500" y1="280" x2="800" y2="280" style="stroke:white; stroke-width:1"></line>
    <text x="650" y="300" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
      ... (1024 entries total)
    </text>
  </g>
  
  <!-- Arrow from Page Directory to Page Table -->
  <path d="M 580 320 L 350 360" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <text x="470" y="340" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">Points to PT</text>
  
  <!-- Arrow from PT Index to Page Table -->
  <path d="M 275 130 L 275 360" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <text x="285" y="250" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">Index</text>
  
  <!-- Page Table -->
  <g id="page-table">
    <rect x="100" y="370" width="300" height="120" style="fill:#95a5a6; stroke:#7f8c8d; stroke-width:2" />
    <text x="250" y="395" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
      Page Table
    </text>
    
    <line x1="100" y1="405" x2="400" y2="405" style="stroke:white; stroke-width:1"></line>
    <text x="120" y="425" font-family="Arial, sans-serif" style="fill:white; font-size:10">PTE 0</text>
    <text x="300" y="425" font-family="Arial, sans-serif" style="fill:white; font-size:9">PFN: 0x1234</text>
    
    <line x1="100" y1="435" x2="400" y2="435" style="stroke:white; stroke-width:1"></line>
    <text x="120" y="455" font-family="Arial, sans-serif" style="fill:white; font-size:10">PTE 1</text>
    <text x="300" y="455" font-family="Arial, sans-serif" style="fill:white; font-size:9">PFN: 0x5678</text>
    
    <line x1="100" y1="465" x2="400" y2="465" style="stroke:white; stroke-width:1"></line>
    <text x="250" y="485" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
      ... (1024 entries)
    </text>
  </g>
  
  <!-- Physical Page -->
  <rect x="550" y="390" width="200" height="80" style="fill:#00796B; stroke:#229954; stroke-width:2" />
  <text x="650" y="415" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Physical Page
  </text>
  <text x="650" y="440" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    4KB Page Frame
  </text>
  <text x="650" y="460" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    (PFN from PTE)
  </text>
  
  <!-- Arrow from Page Table to Physical Page -->
  <path d="M 400 430 L 550 430" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <!-- Memory savings note -->
  <text x="50" y="30" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:11">
    Each 4MB region needs only one PDE + one 4KB PT (if mapped)
  </text>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" style="fill:#34495e"></polygon>
    </marker>
  </defs>
</svg>
</div>
<figcaption><strong>Figure 3.2:</strong> Two-level page table (x86
32-bit): the 20-bit VPN splits into a 10-bit directory index and a
10-bit table index. Only populated second-level tables need physical
frames, dramatically reducing memory overhead.</figcaption>
</figure>

The two-level page table represents a breakthrough in virtual memory
design. By introducing one level of indirection---a page table that
points to page tables---we can eliminate the requirement that the entire
page table be allocated at once. This simple change reduces memory
overhead by orders of magnitude while adding only modest complexity to
the translation process.

### 3.3.1 The Hierarchical Structure {#3.3.1-the-hierarchical-structure}

A two-level page table divides the virtual address into three parts
instead of two:

1\. **Page directory index**: Selects an entry in the page directory
(the first level)

2\. **Page table index**: Selects an entry in a page table (the second
level)

3\. **Page offset**: Identifies the byte within the physical page

The page directory is always present---it\'s the single top-level
structure pointed to by the PTBR register. However, the second-level
page tables are allocated on demand. If a region of the virtual address
space is not in use, the corresponding page directory entry is marked
invalid, and no page table is allocated for that region.

This is the key insight: **we only allocate page tables for regions of
virtual address space that are actually mapped to physical memory**.

**Directory → Table → Page Hierarchy**

The translation process now involves two table lookups:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Virtual Address

↓

Page Directory Index → \[Page Directory\] → Page Directory Entry

↓

(contains physical address of page table)

↓

Page Table Index → \[Page Table\] → Page Table Entry

↓

(contains physical page number)

↓

Physical Page + Offset → Physical Address
:::

Compare this to single-level:

- Single-level: PTBR → Page Table → Physical Page
- Two-level: PTBR → Page Directory → Page Table → Physical Page

We\'ve traded one additional memory access for the ability to leave
second-level page tables unallocated.

### 3.3.2 x86 32-bit Example: The Classic Implementation {#3.3.2-x86-32-bit-example-the-classic-implementation}

The Intel IA-32 architecture (32-bit x86) provides the canonical example
of two-level paging. Introduced with the Intel 80386 in 1985, this
design influenced countless subsequent architectures.

**Address Format**

For 32-bit x86 with 4KB pages:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 31-22: Page Directory Index (10 bits) = 1024 entries

Bits 21-12: Page Table Index (10 bits) = 1024 entries

Bits 11-0: Page Offset (12 bits) = 4096 bytes
:::

Why 10 bits for each index? Because each table (both directory and page
tables) is designed to fit exactly in one 4KB page:

- 1024 entries per table
- 4 bytes per entry (32-bit pointers)
- 1024 × 4 bytes = 4096 bytes = 4KB = exactly one page

This self-referential elegance means page tables can be paged---the page
tables themselves are just pages that can be swapped out if memory is
tight!

**Page Directory Entry (PDE) Structure**

Each 32-bit PDE contains:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 31-12: Physical address of page table (20 bits)

Bit 11: Reserved

Bit 10: Reserved

Bit 9: Available for system use

Bit 8: Global (G)

Bit 7: Page Size (PS) - if 1, this PDE maps a 4MB page directly

Bit 6: Reserved (0)

Bit 5: Accessed (A)

Bit 4: Cache Disable (PCD)

Bit 3: Write-Through (PWT)

Bit 2: User/Supervisor (U/S)

Bit 1: Read/Write (R/W)

Bit 0: Present (P)
:::

The **Present bit (P)** is crucial: if P=0, this page directory entry is
invalid, and no page table exists for this 4MB region of virtual address
space. The CPU doesn\'t access this memory at all.

**Page Table Entry (PTE) Structure**

Each 32-bit PTE contains:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 31-12: Physical page frame number (20 bits)

Bit 11: Reserved

Bit 10: Reserved

Bit 9: Available for system use

Bit 8: Global (G)

Bit 7: Page Attribute Table (PAT)

Bit 6: Dirty (D)

Bit 5: Accessed (A)

Bit 4: Cache Disable (PCD)

Bit 3: Write-Through (PWT)

Bit 2: User/Supervisor (U/S)

Bit 1: Read/Write (R/W)

Bit 0: Present (P)
:::

Again, if P=0, this virtual page is not mapped to physical memory, and
accessing it triggers a page fault.

*Reference: Intel 64 and IA-32 Architectures Software Developer\'s
Manual, Volume 3A: System Programming Guide, Part 1, Section 4.3:
\"32-Bit Paging\" provides complete details on the two-level paging
structure used in legacy 32-bit x86 systems. Intel Corporation, 2024.*
**CR3 Register and Translation**

The CR3 register (Control Register 3) points to the physical address of
the page directory:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 31-12: Physical address of page directory (20 bits)

Bits 11-0: Flags and reserved bits
:::

When the MMU translates an address:

1\. **Extract indices**: Split virtual address into directory index
(bits 31-22), table index (bits 21-12), and offset (bits 11-0)

2\. **Read PDE**:

\- Calculate PDE address: CR3\[31:12\] + (directory_index × 4)

\- Read 32-bit PDE from this address

\- Check Present bit: if P=0, generate page fault

3\. **Read PTE**:

\- Extract page table base from PDE\[31:12\]

\- Calculate PTE address: PDE\[31:12\] + (table_index × 4)

\- Read 32-bit PTE from this address

\- Check Present bit: if P=0, generate page fault

4\. **Form physical address**:

\- Extract physical page number from PTE\[31:12\]

\- Combine with offset: PA = (PTE\[31:12\] \<\< 12) \| offset

5\. **Access memory**: Read from or write to the physical address

### 3.3.3 Translation Walkthrough with Concrete Example {#3.3.3-translation-walkthrough-with-concrete-example}

Let\'s translate a specific virtual address step by step to make this
concrete.

**Given**:

- Virtual address: 0x0040_5678
- CR3 = 0x0010_0000 (physical address of page directory)
- We\'ll discover page table and page frame addresses through the walk

**Step 1: Break down the virtual address**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Virtual Address: 0x0040_5678 = 0000 0000 0100 0000 0101 0110 0111 1000

Bits 31-22 (PD Index): 0000 0000 01 = 0x001 = 1

Bits 21-12 (PT Index): 00 0000 0101 = 0x005 = 5

Bits 11-0 (Offset): 0110 0111 1000 = 0x678 = 1656
:::

So we need:

- Page Directory Entry #1
- Page Table Entry #5 (within the table pointed to by PDE#1)
- Offset 1656 within the resulting physical page

**Step 2: Read Page Directory Entry**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
PDE Address = CR3 + (PD_index × 4)

= 0x0010_0000 + (1 × 4)

= 0x0010_0000 + 0x4

= 0x0010_0004
:::

Read 32-bit value at physical address 0x0010_0004. Let\'s say we find:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
PDE = 0x0020_0007
:::

Interpret this PDE:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 31-12: 0x0020_0 = physical address of page table (0x0020_0000)

Bits 11-0: 0x007 = flags

Bit 0 (P): 1 = Present ✓

Bit 1 (R/W): 1 = Read/Write allowed

Bit 2 (U/S): 1 = User accessible

Other bits: 0 = disabled/not used
:::

The page table is at physical address 0x0020_0000.

**Step 3: Read Page Table Entry**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
PTE Address = Page_Table_Base + (PT_index × 4)

= 0x0020_0000 + (5 × 4)

= 0x0020_0000 + 0x14

= 0x0020_0014
:::

Read 32-bit value at physical address 0x0020_0014. Let\'s say we find:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
PTE = 0x0030_5027
:::

Interpret this PTE:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 31-12: 0x0030_5 = physical page frame number (0x0030_5000)

Bits 11-0: 0x027 = flags

Bit 0 (P): 1 = Present ✓

Bit 1 (R/W): 1 = Read/Write allowed

Bit 2 (U/S): 1 = User accessible

Bit 5 (A): 1 = Accessed (hardware set this on previous access)

Other bits: 0 = disabled/not used
:::

The physical page is at 0x0030_5000.

**Step 4: Form final physical address**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Physical Address = Physical_Page_Base + Offset

= 0x0030_5000 + 0x678

= 0x0030_5678
:::

**Summary**:

- Virtual Address: 0x0040_5678
- Physical Address: 0x0030_5678
- Memory accesses required: 2 (PDE read + PTE read) + 1 (final data
  read) = 3 total

Without a TLB cache hit, this translation requires two additional memory
accesses beyond the actual data access. This is why the TLB is so
critical for performance!

### 3.3.4 Memory Savings Analysis {#3.3.4-memory-savings-analysis}

Now let\'s quantify the memory savings that two-level page tables
provide.

**Scenario: Process Using 16MB of Memory**

Consider a process that uses 16MB of memory scattered across its address
space:

- Code segment: 4MB at virtual address 0x0000_0000 - 0x003F_FFFF
- Heap: 8MB at virtual address 0x4000_0000 - 0x47FF_FFFF
- Stack: 4MB at virtual address 0xBFC0_0000 - 0xBFFF_FFFF

**Single-Level Page Table**:

- Must allocate full table: 1,048,576 entries × 4 bytes = 4,194,304
  bytes = 4MB
- Entries used: 16MB / 4KB = 4,096 pages = 4,096 entries
- Entries wasted: 1,048,576 - 4,096 = 1,044,480 entries (99.6% waste!)

**Two-Level Page Table**:

- Page directory: Always allocated = 1024 entries × 4 bytes = 4KB
- Page tables: Only for used regions

Let\'s calculate which page directory entries need page tables:

**Code segment** (0x0000_0000 - 0x003F_FFFF):

- Covers PD indices 0 through 3 (4MB per PDE, 4MB / 4MB = 1 PDE\...
  wait, let me recalculate)
- Each PDE covers 1024 pages × 4KB = 4MB of address space
- 4MB code / 4MB per PDE = 1 PDE (PD index 0)
- Needs: 1 page table = 4KB

**Heap** (0x4000_0000 - 0x47FF_FFFF):

- Start: 0x4000_0000 → PD index = 0x100 = 256
- End: 0x47FF_FFFF → PD index = 0x11F = 287
- 8MB / 4MB per PDE = 2 PDEs (indices 256-257)
- Needs: 2 page tables = 8KB

**Stack** (0xBFC0_0000 - 0xBFFF_FFFF):

- Start: 0xBFC0_0000 → PD index = 0x2FF = 767
- 4MB / 4MB per PDE = 1 PDE (index 767)
- Needs: 1 page table = 4KB

**Total memory for two-level page tables**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Page directory: 4KB

Page tables (4): 16KB

Total: 20KB
:::

**Savings**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Single-level: 4,096KB (4MB)

Two-level: 20KB

Savings: 4,076KB (99.5% reduction!)
:::

We\'ve reduced page table memory overhead by 99.5%! Instead of 4MB for
every process regardless of memory usage, we now use only 20KB for this
16MB process---and that overhead grows proportionally with actual memory
usage rather than address space size.

**Worst-Case Scenario**

What if the process used memory maximally scattered across the entire
4GB address space? For instance, one page in each 4MB region:

- Page directory: 4KB (always present)
- Page tables: 1024 tables × 4KB = 4MB
- Total: 4MB + 4KB ≈ 4MB

In the absolute worst case, two-level page tables use approximately the
same memory as single-level tables. But this worst case is extremely
rare. Real programs exhibit locality---code, data, heap, and stack
cluster together rather than spreading uniformly across the entire
address space.

**Typical Case: Much Better**

Most processes use tens to hundreds of megabytes of memory in contiguous
or semi-contiguous regions:

- Small process (1-10MB): \~16-40KB page table overhead
- Medium process (100MB): \~200-400KB page table overhead
- Large process (1GB): \~2-4MB page table overhead

Compare to 4MB overhead for every process with single-level tables, and
the savings are dramatic for the common case.

### 3.3.5 The Cost: Translation Complexity {#3.3.5-the-cost-translation-complexity}

Two-level page tables reduce memory overhead but at a cost: translation
now requires two memory accesses instead of one (when the TLB doesn\'t
have the translation cached).

**Performance Impact Without TLB**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Single-level: 1 memory access (page table lookup)

Two-level: 2 memory accesses (directory lookup + table lookup)
:::

If every memory instruction required these lookups, two-level tables
would cut memory bandwidth in half! This is why the TLB is essential:

**Performance Impact With TLB**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
TLB hit rate: 95-99% (typical)

Effective cost: \~1.0-1.1 memory accesses per instruction
:::

With a 95% TLB hit rate:

- 95% of accesses: 0 additional lookups (TLB hit)
- 5% of accesses: 2 additional lookups (TLB miss)
- Average: 0.95×0 + 0.05×2 = 0.10 extra lookups per access

The TLB amortizes the translation cost so effectively that the
performance penalty of two-level tables is typically negligible---a few
percent at most---while the memory savings are dramatic.

### 3.3.6 Transition to More Levels {#3.3.6-transition-to-more-levels}

Two-level page tables solved the memory overhead problem for 32-bit
address spaces, but they still have limitations:

**32-bit Limitation**: Even in the worst case, the overhead is bounded
at \~4MB, which is acceptable for systems with gigabytes of RAM.
**64-bit Impossibility**: For 64-bit address spaces, even two-level
tables don\'t suffice. With 4KB pages and 8-byte entries:

- First-level table covers: 512 entries × 2MB = 1GB per entry
- Would need: 2\^64 / 1GB = 16 million first-level entries
- First-level table size: 16 million × 8 bytes = 128MB per process

Still too large! This is why modern 64-bit systems use three, four, or
even five levels of page tables, which we\'ll explore in the next
section.

The two-level page table represents a sweet spot for 32-bit systems: it
provides dramatic memory savings over single-level tables while adding
minimal complexity and only modest (TLB-mitigated) performance overhead.
Its success in the x86 architecture influenced the design of virtually
all subsequent page table implementations.

## 3.4 Multi-Level Page Tables (3+ Levels) {#3.4-multi-level-page-tables-3-levels}

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="950" height="700" viewBox="0 0 950 700" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="475" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    Page Table Memory Overhead Comparison
  </text>
  
  <!-- Scenario Description -->
  <rect x="50" y="60" width="850" height="60" style="fill:#e8f8f5; stroke:#16a085; stroke-width:2" />
  <text x="475" y="85" font-family="Arial, sans-serif" style="fill:#16a085; font-size:13; font-weight:bold; text-anchor:middle">
    Scenario: Process using 16MB of memory (scattered across address space)
  </text>
  <text x="475" y="107" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11; text-anchor:middle">
    Code: 4MB | Heap: 8MB | Stack: 4MB | Total: 4,096 pages (4KB each)
  </text>
  
  <!-- Comparison Table -->
  <rect x="50" y="150" width="850" height="520" style="fill:#ffffff; stroke:#bdc3c7; stroke-width:2" />
  
  <!-- Header Row -->
  <rect x="50" y="150" width="850" height="50" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="150" y="180" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Scheme
  </text>
  <text x="350" y="180" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Levels
  </text>
  <text x="500" y="180" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Page Table Size
  </text>
  <text x="700" y="180" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Overhead
  </text>
  <text x="830" y="180" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    Savings
  </text>
  
  <!-- Single-Level (32-bit) -->
  <rect x="50" y="200" width="850" height="80" style="fill:#fee; stroke:#E65100; stroke-width:1" />
  <text x="150" y="235" font-family="Arial, sans-serif" style="fill:#E65100; font-size:11; font-weight:bold; text-anchor:middle">
    Single-Level
  </text>
  <text x="150" y="252" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    (32-bit)
  </text>
  
  <text x="350" y="245" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11; text-anchor:middle">
    1
  </text>
  
  <text x="500" y="235" font-family="Arial, sans-serif" style="fill:#E65100; font-size:11; font-weight:bold; text-anchor:middle">
    4 MB
  </text>
  <text x="500" y="252" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    (2²⁰ entries × 4 bytes)
  </text>
  <text x="500" y="268" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8; text-anchor:middle">
    All 1,048,576 entries allocated
  </text>
  
  <text x="700" y="245" font-family="Arial, sans-serif" style="fill:#E65100; font-size:11; font-weight:bold; text-anchor:middle">
    256:1
  </text>
  
  <text x="830" y="245" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:11; text-anchor:middle">
    —
  </text>
  
  <!-- Two-Level (32-bit) -->
  <rect x="50" y="280" width="850" height="80" style="fill:#ffeaa7; stroke:#f39c12; stroke-width:1" />
  <text x="150" y="315" font-family="Arial, sans-serif" style="fill:#d68910; font-size:11; font-weight:bold; text-anchor:middle">
    Two-Level
  </text>
  <text x="150" y="332" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    (x86 32-bit)
  </text>
  
  <text x="350" y="325" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11; text-anchor:middle">
    2
  </text>
  
  <text x="500" y="315" font-family="Arial, sans-serif" style="fill:#d68910; font-size:11; font-weight:bold; text-anchor:middle">
    20 KB
  </text>
  <text x="500" y="332" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    Directory: 4KB
  </text>
  <text x="500" y="348" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    4 Page Tables: 16KB
  </text>
  
  <text x="700" y="325" font-family="Arial, sans-serif" style="fill:#d68910; font-size:11; font-weight:bold; text-anchor:middle">
    1.25:1
  </text>
  
  <text x="830" y="325" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold; text-anchor:middle">
    99.5%
  </text>
  
  <!-- Three-Level (RISC-V Sv39) -->
  <rect x="50" y="360" width="850" height="80" style="fill:#d5f4e6; stroke:#00796B; stroke-width:1" />
  <text x="150" y="395" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold; text-anchor:middle">
    Three-Level
  </text>
  <text x="150" y="412" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    (RISC-V Sv39)
  </text>
  
  <text x="350" y="405" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11; text-anchor:middle">
    3
  </text>
  
  <text x="500" y="395" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold; text-anchor:middle">
    ~24 KB
  </text>
  <text x="500" y="412" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    L2 root: 4KB
  </text>
  <text x="500" y="428" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    L1 + L0 tables: ~20KB
  </text>
  
  <text x="700" y="405" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold; text-anchor:middle">
    1.5:1
  </text>
  
  <text x="830" y="405" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold; text-anchor:middle">
    99.4%
  </text>
  
  <!-- Four-Level (x86-64) -->
  <rect x="50" y="440" width="850" height="80" style="fill:#F5F5F5; stroke:#1565C0; stroke-width:1" />
  <text x="150" y="475" font-family="Arial, sans-serif" style="fill:#1565C0; font-size:11; font-weight:bold; text-anchor:middle">
    Four-Level
  </text>
  <text x="150" y="492" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    (x86-64, ARM64)
  </text>
  
  <text x="350" y="485" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11; text-anchor:middle">
    4
  </text>
  
  <text x="500" y="475" font-family="Arial, sans-serif" style="fill:#1565C0; font-size:11; font-weight:bold; text-anchor:middle">
    ~32 KB
  </text>
  <text x="500" y="492" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    PML4: 4KB | PDPT: 4KB
  </text>
  <text x="500" y="508" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    PD + PT tables: ~24KB
  </text>
  
  <text x="700" y="485" font-family="Arial, sans-serif" style="fill:#1565C0; font-size:11; font-weight:bold; text-anchor:middle">
    2:1
  </text>
  
  <text x="830" y="485" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold; text-anchor:middle">
    99.2%
  </text>
  
  <!-- Five-Level (x86-64 LA57) -->
  <rect x="50" y="520" width="850" height="80" style="fill:#e8daef; stroke:#9b59b6; stroke-width:1" />
  <text x="150" y="555" font-family="Arial, sans-serif" style="fill:#9b59b6; font-size:11; font-weight:bold; text-anchor:middle">
    Five-Level
  </text>
  <text x="150" y="572" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    (x86-64 LA57)
  </text>
  
  <text x="350" y="565" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11; text-anchor:middle">
    5
  </text>
  
  <text x="500" y="555" font-family="Arial, sans-serif" style="fill:#9b59b6; font-size:11; font-weight:bold; text-anchor:middle">
    ~40 KB
  </text>
  <text x="500" y="572" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    PML5: 4KB | PML4-PT: ~36KB
  </text>
  <text x="500" y="588" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    Extra level adds ~8KB
  </text>
  
  <text x="700" y="565" font-family="Arial, sans-serif" style="fill:#9b59b6; font-size:11; font-weight:bold; text-anchor:middle">
    2.5:1
  </text>
  
  <text x="830" y="565" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold; text-anchor:middle">
    99.0%
  </text>
  
  <!-- Separator lines -->
  <line x1="250" y1="150" x2="250" y2="670" style="stroke:#bdc3c7; stroke-width:1"></line>
  <line x1="430" y1="150" x2="430" y2="670" style="stroke:#bdc3c7; stroke-width:1"></line>
  <line x1="600" y1="150" x2="600" y2="670" style="stroke:#bdc3c7; stroke-width:1"></line>
  <line x1="770" y1="150" x2="770" y2="670" style="stroke:#bdc3c7; stroke-width:1"></line>
  
  <!-- Row dividers -->
  <line x1="50" y1="200" x2="900" y2="200" style="stroke:#bdc3c7; stroke-width:1"></line>
  <line x1="50" y1="280" x2="900" y2="280" style="stroke:#bdc3c7; stroke-width:1"></line>
  <line x1="50" y1="360" x2="900" y2="360" style="stroke:#bdc3c7; stroke-width:1"></line>
  <line x1="50" y1="440" x2="900" y2="440" style="stroke:#bdc3c7; stroke-width:1"></line>
  <line x1="50" y1="520" x2="900" y2="520" style="stroke:#bdc3c7; stroke-width:1"></line>
  <line x1="50" y1="600" x2="900" y2="600" style="stroke:#bdc3c7; stroke-width:1"></line>
  
  <!-- Key Insight -->
  <rect x="50" y="620" width="850" height="50" style="fill:#fff9e6; stroke:#f39c12; stroke-width:2" />
  <text x="475" y="645" font-family="Arial, sans-serif" style="fill:#d68910; font-size:12; font-weight:bold; text-anchor:middle">
    âš¡ Key Insight: Multi-level tables reduce overhead by 99%+ for sparse address spaces!
  </text>
  <text x="475" y="662" font-family="Arial, sans-serif" style="fill:#856404; font-size:10; text-anchor:middle">
    Only allocate tables for used regions → Overhead grows with actual usage, not address space size
  </text>
</svg>
</div>
<figcaption><strong>Figure 3.overhead:</strong> Page table memory
overhead across architectures: single-level tables require contiguous
allocation; multi-level designs allocate only second-level tables for
mapped regions, achieving near-zero overhead for sparse address
spaces.</figcaption>
</figure>

The transition from 32-bit to 64-bit computing created an entirely new
scale of challenge for page table design. A 64-bit address space is not
merely twice as large as 32-bit---it\'s 2\^32 times larger. Even with
two-level page tables, the overhead would be unmanageable. The solution:
add more levels to the hierarchy.

Modern architectures typically use three, four, or even five levels of
page tables. Each additional level multiplies the sparseness advantage:
we only allocate page table structures for the portions of the vast
64-bit address space that are actually in use. In this section, we\'ll
examine the specific implementations used by the three dominant
architecture families: x86-64 (Intel and AMD), ARM64, and RISC-V.

### 3.4.1 x86-64 Four-Level Paging: The Current Standard {#3.4.1-x86-64-four-level-paging-the-current-standard}

When AMD introduced the x86-64 architecture (also called AMD64 or
x86_64) in 2003, it faced a critical design decision: how to handle the
exponentially larger 64-bit address space? The solution was four-level
paging, which Intel adopted when it began producing 64-bit processors
with EM64T (later rebranded Intel 64).

**The 48-Bit Compromise**

An important detail: despite being called \"64-bit,\" x86-64 processors
don\'t actually use all 64 bits for virtual addresses. Early
implementations use only 48 bits, supporting a 256TB virtual address
space. This was a pragmatic decision:

- 256TB is vastly more than any application or operating system needed
  in 2003
- Using fewer bits simplifies hardware and reduces power consumption
- The remaining 16 bits (bits 63-48) must be copies of bit 47 (sign
  extension), creating \"canonical\" addresses

This design allows future expansion if 256TB ever becomes limiting
(which it has, as we\'ll see with five-level paging).

**Four-Level Structure**

The x86-64 four-level page table hierarchy uses these names:

1\. **PML4** (Page Map Level 4): The top level

2\. **PDPT** (Page Directory Pointer Table): Third level

3\. **PD** (Page Directory): Second level

4\. **PT** (Page Table): Lowest level, contains PTEs that point to
actual pages

Each level contains 512 entries (not 1024 like in 32-bit x86), and each
entry is 8 bytes (64 bits). This gives each table a size of:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
512 entries × 8 bytes = 4,096 bytes = 4KB = one page
:::

Once again, the page table structures themselves fit in single pages!

**Virtual Address Format**

A canonical 48-bit x86-64 virtual address is divided:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-48: Sign extension (16 bits) - must equal bit 47

Bits 47-39: PML4 index (9 bits) = 512 entries, each covers 512GB

Bits 38-30: PDPT index (9 bits) = 512 entries, each covers 1GB

Bits 29-21: PD index (9 bits) = 512 entries, each covers 2MB

Bits 20-12: PT index (9 bits) = 512 entries, each covers 4KB

Bits 11-0: Page offset (12 bits) = 4096 bytes
:::

Let\'s understand what each level covers:

- **PML4 entry**: Points to a PDPT, covers 512GB of address space

\- Calculation: 512 (PDPT entries) × 1GB = 512GB

- **PDPT entry**: Points to a PD, covers 1GB of address space

\- Calculation: 512 (PD entries) × 2MB = 1GB

- **PD entry**: Points to a PT, covers 2MB of address space

\- Calculation: 512 (PT entries) × 4KB = 2MB

- **PT entry**: Points to a physical page, covers 4KB

**CR3 Register in 64-bit Mode**

In 64-bit mode, CR3 still points to the top-level page structure, but
now that\'s the PML4:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-52: Reserved (0)

Bits 51-12: Physical address of PML4 (40 bits)

Bits 11-5: Reserved (0)

Bits 4-3: PWT, PCD flags (page-level cache control)

Bit 2-0: Reserved (0)
:::

The 40-bit physical address allows addressing up to 1TB (2\^40 bytes) of
physical RAM, though actual CPU models support varying amounts.

**Entry Format**

All four levels (PML4E, PDPTE, PDE, PTE) share a similar 64-bit format,
though some bits have level-specific meanings:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bit 63: XD (Execute Disable) / NX (No Execute)

Bits 62-52: Available for OS use (11 bits)

Bits 51-12: Physical address of next level / page frame (40 bits)

Bits 11-9: Available for OS use (3 bits)

Bit 8: Global (G) - only in lowest-level PTE

Bit 7: PS (Page Size) - in PDPTE/PDE, indicates huge page

Bit 6: Dirty (D) - only in lowest-level PTE

Bit 5: Accessed (A)

Bit 4: PCD (Page-level Cache Disable)

Bit 3: PWT (Page-level Write-Through)

Bit 2: U/S (User/Supervisor)

Bit 1: R/W (Read/Write)

Bit 0: P (Present)
:::

Key points:

- **XD/NX bit** (bit 63): Prevents instruction execution from this page,
  a crucial security feature
- **Present bit** (bit 0): If 0, this entry is invalid---no lower-level
  structure exists
- **PS bit** (bit 7): In PDPTE or PDE, indicates this entry points
  directly to a 1GB or 2MB page (huge pages)
- **Accessed/Dirty bits**: Hardware-managed status bits

*Reference: Intel 64 and IA-32 Architectures Software Developer\'s
Manual, Volume 3A: System Programming Guide, Part 1, Section 4.5:
\"4-Level Paging and 5-Level Paging\" provides comprehensive coverage of
the page table entry formats and translation process. Intel Corporation,
2024.* **Translation Process**

The hardware page walker performs these steps on a TLB miss:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
1\. Read CR3 → get PML4 physical address

2\. Extract PML4 index from VA\[47:39\]

3\. Read PML4\[index\] (PML4E)

4\. Check PML4E.P bit; if 0, page fault

5\. Extract PDPT physical address from PML4E\[51:12\]

6\. Extract PDPT index from VA\[38:30\]

7\. Read PDPT\[index\] (PDPTE)

8\. Check PDPTE.P bit; if 0, page fault

9\. If PDPTE.PS = 1, this is a 1GB huge page → skip to step 15

10\. Extract PD physical address from PDPTE\[51:12\]

11\. Extract PD index from VA\[29:21\]

12\. Read PD\[index\] (PDE)

13\. Check PDE.P bit; if 0, page fault

14\. If PDE.PS = 1, this is a 2MB huge page → skip to step 18

15\. Extract PT physical address from PDE\[51:12\]

16\. Extract PT index from VA\[20:12\]

17\. Read PT\[index\] (PTE)

18\. Check PTE.P bit; if 0, page fault

19\. Check permissions (XD, U/S, R/W); if violation, page fault

20\. Extract physical page frame from PTE\[51:12\]

21\. Set PTE.A bit (hardware); if write, set PTE.D bit

22\. Combine page frame with offset: PA = (PTE\[51:12\] \<\< 12) \|
VA\[11:0\]

23\. Insert translation into TLB

24\. Complete memory access
:::

Without TLB caching, this requires **four memory reads** before the
actual data access---five memory accesses total. This is why page walk
caches and large TLBs are critical for modern processor performance.

**Example: Translating a Concrete Address**

Let\'s translate virtual address 0x0000_7F8A_4050_1678:

First, verify it\'s canonical:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Binary: 0000 0000 0000 0000 0111 1111 1000 1010 0100 0000 0101 0000 0001
0110 0111 1000

Bit 47: 0

Bits 63-48: all 0 (match bit 47) ✓ Canonical
:::

Extract indices:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 47-39 (PML4): 000 0000 00 = 0x000 = 0

Bits 38-30 (PDPT): 00 1111 111 = 0x07F = 127

Bits 29-21 (PD): 000 1010 01 = 0x029 = 41

Bits 20-12 (PT): 00 0000 010 = 0x002 = 2

Bits 11-0 (Offset): 1000 0001 0110 0111 1000 = 0x678 = 1656
:::

Assume CR3 = 0x0010_0000. The walk proceeds:

**Step 1: PML4 lookup**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
PML4E address = 0x0010_0000 + (0 × 8) = 0x0010_0000

Read PML4E = assume 0x0020_0000_0000_0003

Present: 1 ✓

R/W: 1 ✓

PDPT at 0x0020_0000_0000
:::

**Step 2: PDPT lookup**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
PDPTE address = 0x0020_0000_0000 + (127 × 8) = 0x0020_0000_03F8

Read PDPTE = assume 0x0030_0000_0000_0003

Present: 1 ✓

PS: 0 (not 1GB page)

PD at 0x0030_0000_0000
:::

**Step 3: PD lookup**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
PDE address = 0x0030_0000_0000 + (41 × 8) = 0x0030_0000_0148

Read PDE = assume 0x0040_0000_0000_0003

Present: 1 ✓

PS: 0 (not 2MB page)

PT at 0x0040_0000_0000
:::

**Step 4: PT lookup**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
PTE address = 0x0040_0000_0000 + (2 × 8) = 0x0040_0000_0010

Read PTE = assume 0x0050_5000_0000_0027

Present: 1 ✓

R/W: 1 ✓

Accessed: 1 (previously accessed)

Page at 0x0050_5000_0000
:::

**Step 5: Form physical address**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
PA = 0x0050_5000_0000 + 0x678 = 0x0050_5000_0678
:::

**Summary**:

- Virtual: 0x0000_7F8A_4050_1678
- Physical: 0x0050_5000_0678
- Memory accesses: 4 (page table walks) + 1 (data) = 5 total

This is why workload performance can degrade significantly if TLB misses
are frequent!

### 3.4.2 x86-64 Five-Level Paging: Expanding to 128 PB {#3.4.2-x86-64-five-level-paging-expanding-to-128-pb}

In 2019, Intel introduced five-level paging with the Ice Lake processor
architecture. This wasn\'t merely an incremental improvement---it
represented a massive expansion of the virtual address space from 256TB
(48-bit) to 128PB (57-bit), a 512× increase.

**Why Five Levels?**

The motivation for five-level paging comes from large-scale systems:

- **Database servers** managing hundreds of terabytes of data in memory
- **Machine learning workloads** requiring vast memory for training data
- **In-memory analytics** systems processing petabyte-scale datasets
- **Future-proofing** for workloads that don\'t exist yet

While 256TB seemed enormous in 2003, modern high-end servers can have
multiple terabytes of RAM, and applications using memory-mapped files
can easily exceed 256TB of virtual address space usage when working with
very large datasets.

**The LA57 Extension**

Five-level paging is enabled by setting the LA57 bit (bit 12) in the CR4
control register. When CR4.LA57 = 1, the processor uses 57-bit virtual
addresses; when CR4.LA57 = 0, it uses traditional 48-bit addresses with
four-level paging.

This opt-in design allows:

- **Backward compatibility**: Existing software continues using
  four-level paging
- **Performance**: Four-level paging has one fewer memory access;
  systems not needing 128PB can avoid the overhead
- **Gradual adoption**: Operating systems can enable five-level paging
  only when beneficial

**Five-Level Structure**

The hierarchy adds one more level at the top:

1\. **PML5** (Page Map Level 5): New top level

2\. **PML4** (Page Map Level 4): Second level (same as before)

3\. **PDPT** (Page Directory Pointer Table): Third level

4\. **PD** (Page Directory): Fourth level

5\. **PT** (Page Table): Lowest level

**Virtual Address Format (57-bit)**

A canonical 57-bit virtual address:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-57: Sign extension (7 bits) - must equal bit 56

Bits 56-48: PML5 index (9 bits) = 512 entries, each covers 256TB

Bits 47-39: PML4 index (9 bits) = 512 entries, each covers 512GB

Bits 38-30: PDPT index (9 bits) = 512 entries, each covers 1GB

Bits 29-21: PD index (9 bits) = 512 entries, each covers 2MB

Bits 20-12: PT index (9 bits) = 512 entries, each covers 4KB

Bits 11-0: Page offset (12 bits) = 4096 bytes
:::

Coverage per level:

- **PML5 entry**: Covers 256TB = 512 (PML4 entries) × 512GB
- **PML4 entry**: Covers 512GB (unchanged from four-level)
- **PDPT entry**: Covers 1GB (unchanged)
- **PD entry**: Covers 2MB (unchanged)
- **PT entry**: Covers 4KB (unchanged)

Total address space: 512 (PML5) × 256TB = 128PB

**CR3 in Five-Level Mode**

When CR4.LA57 = 1, CR3 points to PML5 instead of PML4:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-52: Reserved (0)

Bits 51-12: Physical address of PML5 (40 bits)

Bits 11-0: Flags and reserved
:::

**Translation Process**

The page walk now requires up to **five memory accesses**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
1\. Read CR3 → get PML5 physical address

2\. Extract PML5 index from VA\[56:48\]

3\. Read PML5\[index\] (PML5E)

4\. Check PML5E.P bit; if 0, page fault

5\. Extract PML4 physical address from PML5E\[51:12\]

\[Then continue with four-level process from PML4 onward\...\]

6-9: PML4 lookup

10-14: PDPT lookup (check for 1GB huge page)

15-19: PD lookup (check for 2MB huge page)

20-24: PT lookup

25: Combine to form physical address
:::

Without TLB or page walk cache hits, this means **five memory reads**
plus the actual data access---six memory accesses total for a single
load or store instruction!

**Performance Considerations**

The additional level has performance implications:

- **Extra memory access**: One more lookup on TLB miss
- **Larger page table structures**: More memory overhead for full
  coverage
- **Page walk cache pressure**: More levels to cache

However, Intel\'s implementation mitigates these issues:

- **Page walk caches** can cache PML5/PML4 entries
- **Huge pages** (1GB, 2MB) skip lower levels
- **Most workloads** don\'t use enough virtual address space to need
  PML5

**Linux Support**

Linux kernel added five-level paging support in version 4.14 (November
2017), predating the actual hardware release:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
c

// Linux kernel configuration

CONFIG_X86_5LEVEL=y // Enable five-level paging support
:::

The kernel detects CPU support and can boot in either four-level or
five-level mode. Most distributions enable the config option but don\'t
activate five-level paging unless needed (very large memory
configurations or specific workload requirements).

*Reference: Shutemov, K. A. (2017). \"x86: 5-level paging enabling for
v4.14\". Linux Kernel Mailing List. This patch series introduced
five-level paging support to the Linux kernel, providing detailed
implementation notes.* *Reference: Intel 64 and IA-32 Architectures
Software Developer\'s Manual, Volume 3A, Section 4.5.4: \"5-Level
Paging\" describes the extended paging structure and translation
process. Intel Corporation, 2024.* **When to Use Five-Level Paging**

Five-level paging makes sense for:

- Systems with \>256TB of virtual address space needs
- Memory-mapped database workloads with petabyte-scale files
- Large-scale in-memory analytics
- Future-proofing for applications not yet conceived

Most desktop, laptop, and even server workloads don\'t benefit from
five-level paging and incur a small performance penalty from the extra
translation level. As of 2024, five-level paging remains a specialized
feature for high-end systems.

### 3.4.3 ARM64 Page Table Structures {#3.4.3-arm64-page-table-structures}

The ARM architecture takes a different approach to page table design
than x86. Rather than specifying a single fixed structure, ARMv8-A
provides multiple configuration options, allowing system designers to
choose the best trade-off for their specific use case. This flexibility
is one reason ARM dominates embedded systems and mobile devices---the
same architecture scales from tiny microcontrollers to high-performance
servers.

**Three Configuration Dimensions**

ARM64 systems can independently choose:

1\. **Page size**: 4KB, 16KB, or 64KB

2\. **Virtual address size**: 39-bit (512GB), 48-bit (256TB), or 52-bit
(4PB)

3\. **Physical address size**: Up to 52 bits (4PB of physical RAM)

This creates dozens of possible combinations. We\'ll focus on the most
common configuration: 4KB pages with 48-bit virtual addresses, which
uses a four-level page table similar to x86-64.

**Translation Table Base Registers**

ARM uses separate registers for user and kernel address spaces:

- **TTBR0_EL1**: Translation Table Base Register 0, Exception Level 1
  (user space)
- **TTBR1_EL1**: Translation Table Base Register 1, Exception Level 1
  (kernel space)

The address space is split:

- Lower half (bit 63 = 0): Uses TTBR0_EL1, typically for user processes
- Upper half (bit 63 = 1): Uses TTBR1_EL1, typically for kernel

This allows kernel mappings to remain unchanged when switching between
processes---only TTBR0_EL1 needs updating.

**Four-Level Structure with 4KB Pages (Most Common)**

The ARM names for the four levels:

1\. **Level 0**: Top level (512GB per entry)

2\. **Level 1**: Third level (1GB per entry)

3\. **Level 2**: Second level (2MB per entry)

4\. **Level 3**: Lowest level (4KB per entry)

Note that ARM counts from 0, and in the opposite direction from x86!

**Virtual Address Format (48-bit, 4KB pages)**

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63: Region select (0 = TTBR0, 1 = TTBR1)

Bits 62-48: Must match bit 63 (canonical form)

Bits 47-39: Level 0 index (9 bits) = 512 entries, each covers 512GB

Bits 38-30: Level 1 index (9 bits) = 512 entries, each covers 1GB

Bits 29-21: Level 2 index (9 bits) = 512 entries, each covers 2MB

Bits 20-12: Level 3 index (9 bits) = 512 entries, each covers 4KB

Bits 11-0: Page offset (12 bits) = 4096 bytes
:::

This is very similar to x86-64\'s four-level structure, reflecting
convergent evolution toward the same solution.

**Descriptor Format (64-bit)**

ARM uses the term \"descriptor\" instead of \"page table entry.\" Each
64-bit descriptor contains:

**For Upper-Level Descriptors (Levels 0-2)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63: Ignored

Bits 62-52: Ignored (software can use)

Bits 51-12: Next-level table address (40 bits, 4KB aligned)

Bits 11-2: Ignored

Bit 1: Descriptor type (0 = block, 1 = table)

Bit 0: Valid bit
:::

**For Level 3 Page Descriptors**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-59: Ignored

Bit 58-55: Reserved

Bit 54: XN (Execute Never) for privileged

Bit 53: PXN (Privileged Execute Never)

Bit 52: Contiguous hint (for TLB caching)

Bits 51-12: Output address (physical address, 40 bits)

Bit 11: nG (not Global) - if 1, tagged with ASID

Bit 10: AF (Access Flag) - must be 1 for valid translation

Bits 9-8: SH (Shareability) - for multi-core coherency

Bits 7-6: AP (Access Permissions) - read/write control

Bit 5: NS (Non-Secure bit) - for TrustZone

Bits 4-2: AttrIndx - index into MAIR_ELx (memory attributes)

Bit 1: Descriptor type (always 1 for pages)

Bit 0: Valid bit
:::

Key ARM-specific features:

**Access Flag (AF)**: Unlike x86 where the Accessed bit starts at 0 and
hardware sets it to 1, ARM requires software to set AF=1 before the page
is accessible. If AF=0, the MMU raises an Access Flag fault, allowing
the OS to track page accesses. **Shareability (SH)**: Controls cache
coherency in multi-core systems:

- Non-shareable: Used by only one core
- Inner shareable: Shared within a cluster
- Outer shareable: Shared across all cores

**ASID (Address Space Identifier)**: The nG (not Global) bit works with
ASIDs to allow TLB entries from different processes to coexist without
flushing on context switch. **Memory Attributes (AttrIndx)**: Instead of
PCD/PWT bits, ARM uses an index into the MAIR_ELx register, which
contains memory type information (device, normal memory, write-through,
write-back, etc.). *Reference: ARM Architecture Reference Manual for
ARMv8-A, ARM DDI 0487J.a, Section D5: \"The AArch64 Virtual Memory
System Architecture\", specifically Section D5.2: \"The VMSAv8-64
address translation system\" and Section D5.3.3: \"Descriptor formats\".
ARM Limited, 2024.* **Real-World ARM Implementations** **Apple M-series
(M1, M2, M3, M4)**:

- Uses 4KB pages, 48-bit addresses (consumer devices)
- Four-level page tables
- Extremely large TLBs (details not publicly disclosed, but measured to
  be very effective)
- Custom page table implementation with optimizations

**AWS Graviton (Graviton2, Graviton3)**:

- ARM Neoverse N1/V1 cores
- 4KB pages, 48-bit virtual addressing
- Optimized for server workloads with large memory

**Qualcomm Snapdragon**:

- Kryo cores (ARM Cortex-based)
- Mobile-optimized with power-efficient page walks
- 4KB pages standard

**Alternative Configurations** **64KB Pages (Three Levels)**:

Used in some server deployments for better TLB coverage:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 47-42: Level 1 index (6 bits) = 64 entries, each covers 512GB

Bits 41-29: Level 2 index (13 bits) = 8192 entries, each covers 64MB

Bits 28-16: Level 3 index (13 bits) = 8192 entries, each covers 64KB

Bits 15-0: Page offset (16 bits) = 65536 bytes
:::

Fewer levels mean faster translation, and larger pages mean better TLB
hit rates. The trade-off: internal fragmentation (wasted space within
pages).

**16KB Pages (Four Levels)**:

A middle ground, less commonly used:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 47-42: Level 0 index (6 bits)

Bits 41-36: Level 1 index (6 bits)

Bits 35-25: Level 2 index (11 bits)

Bits 24-14: Level 3 index (11 bits)

Bits 13-0: Page offset (14 bits) = 16384 bytes
:::

### 3.4.4 RISC-V Page Table Structures {#3.4.4-risc-v-page-table-structures}

RISC-V, being a newer architecture (first specification released 2011,
ratified 2019), learned from decades of x86 and ARM experience. The
designers made deliberate choices to simplify page table handling while
maintaining flexibility and performance.

**The Satp Register**

RISC-V uses a single register for all address translation configuration:
satp (Supervisor Address Translation and Protection). For RV64 (64-bit
RISC-V), satp is divided:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-60: MODE (4 bits) - selects paging scheme

0000 = Bare (no translation)

1000 = Sv39 (39-bit virtual address, 3 levels)

1001 = Sv48 (48-bit virtual address, 4 levels)

1010 = Sv57 (57-bit virtual address, 5 levels)

Others = Reserved

Bits 59-44: ASID (16 bits) - Address Space Identifier for TLB tagging

Bits 43-0: PPN (44 bits) - Physical Page Number of root page table
:::

This single register encodes:

- Whether paging is enabled
- Which paging mode to use
- The ASID for TLB management
- The base address of the page table

**Sv39: Three-Level Paging (Most Common)**

Sv39 uses a 39-bit virtual address space (512GB) with three levels of
page tables. This is the most common scheme in current RISC-V
implementations because it balances capability with simplicity.

**Virtual Address Format (Sv39)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-39: Must be copies of bit 38 (canonical form, 25 bits)

Bits 38-30: VPN\[2\] (Virtual Page Number level 2, 9 bits) = 512 entries

Bits 29-21: VPN\[1\] (Virtual Page Number level 1, 9 bits) = 512 entries

Bits 20-12: VPN\[0\] (Virtual Page Number level 0, 9 bits) = 512 entries

Bits 11-0: Page offset (12 bits) = 4096 bytes
:::

Note: RISC-V numbers levels from 0 (lowest) to 2 (highest), opposite of
ARM\'s convention!

**Page Table Entry Format (64-bit)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-54: Reserved (must be zero)

Bits 53-28: PPN\[2\] (Physical Page Number bits 26:0)

Bits 27-19: PPN\[1\] (Physical Page Number bits 18:9)

Bits 18-10: PPN\[0\] (Physical Page Number bits 8:0)

Bits 9-8: RSW (Reserved for Supervisor Software)

Bit 7: D (Dirty)

Bit 6: A (Accessed)

Bit 5: G (Global)

Bit 4: U (User accessible)

Bit 3: X (Execute permission)

Bit 2: W (Write permission)

Bit 1: R (Read permission)

Bit 0: V (Valid)
:::

**Key RISC-V Innovations**: **Explicit R/W/X Bits**: Unlike x86 (which
only has R/W) or ARM (which uses encoded AP bits), RISC-V provides three
separate permission bits. This makes permissions more flexible and
easier to understand. **Leaf Page Detection**: A PTE is a leaf (points
to a page) if any of R/W/X bits are set. If all three are zero, it\'s a
pointer to the next level. This is more elegant than x86\'s Page Size
bit. **Megapages and Gigapages**: At any level, if R/W/X bits are set,
that PTE becomes a leaf:

- Level 0 PTE with R/W/X set: Normal 4KB page
- Level 1 PTE with R/W/X set: 2MB megapage (superpage)
- Level 2 PTE with R/W/X set: 1GB gigapage

This allows flexible huge page support without special flags.

**Translation Process (Sv39)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
1\. Read satp.PPN → get root page table (Level 2)

2\. Extract VPN\[2\] from VA\[38:30\]

3\. Read PTE = root_table\[VPN\[2\]\]

4\. Check PTE.V; if 0, page fault

5\. If PTE.R\|W\|X != 0, this is a gigapage → skip to step 12

6\. Extract next table address from PTE.PPN

7\. Extract VPN\[1\] from VA\[29:21\]

8\. Read PTE = level1_table\[VPN\[1\]\]

9\. Check PTE.V; if 0, page fault

10\. If PTE.R\|W\|X != 0, this is a megapage → skip to step 12

11\. Extract next table address from PTE.PPN

12\. Extract VPN\[0\] from VA\[20:12\]

13\. Read PTE = level0_table\[VPN\[0\]\]

14\. Check PTE.V; if 0, page fault

15\. Check permissions (R/W/X/U); if violation, page fault

16\. Set PTE.A; if write, set PTE.D

17\. Form PA = (PTE.PPN \<\< 12) \| VA\[11:0\]

18\. Complete memory access
:::

**Sv48 and Sv57**

RISC-V also defines four-level (Sv48, 48-bit addresses) and five-level
(Sv57, 57-bit addresses) schemes for larger address spaces, similar to
x86-64:

**Sv48** (256TB virtual space):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 47-39: VPN\[3\] (9 bits) - Fourth level

Bits 38-30: VPN\[2\] (9 bits) - Third level

Bits 29-21: VPN\[1\] (9 bits) - Second level

Bits 20-12: VPN\[0\] (9 bits) - First level

Bits 11-0: Offset (12 bits)
:::

**Sv57** (128PB virtual space):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 56-48: VPN\[4\] (9 bits) - Fifth level

Bits 47-39: VPN\[3\] (9 bits) - Fourth level

\[\... continues similarly \...\]
:::

*Reference: The RISC-V Instruction Set Manual, Volume II: Privileged
Architecture, Version 1.12, Chapter 4: \"Supervisor-Level ISA\",
specifically Section 4.3: \"Sv39: Page-Based 39-bit Virtual-Memory
System\", Section 4.4: \"Sv48: Page-Based 48-bit Virtual-Memory
System\", and Section 4.5: \"Sv57: Page-Based 57-bit Virtual-Memory
System\". RISC-V International, 2021.* **Real-World RISC-V
Implementations** **SiFive U74** (Used in HiFive Unmatched board):

- Sv39 mode only
- 4-core CPU for embedded and edge computing
- Efficient implementation suitable for Linux

**StarFive JH7110** (VisionFive 2 board):

- Sv39 mode
- 4-core SiFive U74 cores
- Popular development platform for RISC-V

**Alibaba Xuantie C910**:

- Supports Sv39 and Sv48
- High-performance core used in servers
- Demonstrates scalability to larger address spaces

As of 2024, most RISC-V implementations use Sv39 because:

- 512GB is sufficient for current applications
- Three levels are simpler and faster than four or five
- Hardware is less complex and lower power

Sv48 and Sv57 provide headroom for future growth as RISC-V moves into
high-end server markets.

**Comparison Across Architectures**

Now that we\'ve examined x86-64, ARM64, and RISC-V in detail, we can
compare their approaches:

\| Feature \| x86-64 \| ARM64 \| RISC-V \|

\|\-\-\-\-\-\-\-\--\|\-\-\-\-\-\-\--\|\-\-\-\-\-\--\|\-\-\-\-\-\-\--\|

\| **Common config** \| 4-level, 48-bit \| 4-level, 48-bit \| 3-level,
39-bit \|

\| **Max levels** \| 5 \| 4 \| 5 \|

\| **Max VA size** \| 57-bit (128PB) \| 52-bit (4PB) \| 57-bit (128PB)
\|

\| **Page sizes** \| 4KB, 2MB, 1GB \| 4KB, 16KB, 64KB + huge \| 4KB,
2MB, 1GB \|

\| **Entry size** \| 8 bytes \| 8 bytes \| 8 bytes \|

\| **Entries/table** \| 512 \| 512 or varies \| 512 \|

\| **Permission model** \| R/W, XD separate \| AP bits + XN/PXN \|
Explicit R/W/X \|

\| **ASID support** \| PCID (optional) \| Built-in (16-bit) \| Built-in
(16-bit) \|

\| **Huge page method** \| PS bit in PDE/PDPTE \| Block descriptors \|
R/W/X in upper level \|

All three architectures converged on similar solutions (4-5 levels, 512
entries per table, 8-byte entries) despite different design
philosophies, suggesting these are close to optimal trade-offs for
modern systems.

### 3.4.5 Translation Process Summary {#3.4.5-translation-process-summary}

Before moving on to virtualization, let\'s summarize the page table walk
process across architectures:

**Memory Accesses Required (without caching)**:

- **Single-level**: 1 access
- **Two-level (x86 32-bit)**: 2 accesses
- **Three-level (RISC-V Sv39)**: 3 accesses
- **Four-level (x86-64, ARM64)**: 4 accesses
- **Five-level (x86-64 LA57)**: 5 accesses

Each access requires reading from DRAM (or cache), which takes 50-200
CPU cycles depending on cache hits. This is why TLB hit rates of 95-99%
are crucial---they eliminate most of these accesses.

**Address Space Coverage**:

- **Three-level, 4KB pages**: 512GB (RISC-V Sv39)
- **Four-level, 4KB pages**: 256TB (x86-64, ARM64)
- **Five-level, 4KB pages**: 128PB (x86-64 LA57)

The progression shows a clear pattern: each additional level multiplies
the address space by 512 (the number of entries per table).

## 3.6 Virtualization: Two-Stage Address Translation {#3.6-virtualization-two-stage-address-translation}

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="1000" height="600" viewBox="0 0 1000 600" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="500" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    Page Table Entry (PTE) Bit Layout Comparison
  </text>
  
  <!-- x86-64 PTE -->
  <text x="50" y="70" font-family="Arial, sans-serif" style="fill:#1565C0; font-size:14; font-weight:bold">
    x86-64 PTE (64-bit)
  </text>
  
  <rect x="50" y="80" width="900" height="70" style="fill:#F5F5F5; stroke:#bdc3c7; stroke-width:2" />
  
  <!-- Bit numbers -->
  <text x="55" y="100" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">63</text>
  <text x="460" y="100" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">52</text>
  <text x="480" y="100" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">51</text>
  <text x="730" y="100" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">12</text>
  <text x="750" y="100" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">11</text>
  <text x="930" y="100" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">0</text>
  
  <rect x="50" y="105" width="35" height="40" style="fill:#E65100; stroke:white" />
  <text x="67" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">XD</text>
  
  <rect x="85" y="105" width="380" height="40" style="fill:#95a5a6; stroke:white" />
  <text x="275" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">Available (62-52)</text>
  
  <rect x="465" y="105" width="270" height="40" style="fill:#1565C0; stroke:white" />
  <text x="600" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">Physical Page Number (51-12)</text>
  
  <rect x="735" y="105" width="180" height="40" style="fill:#2ecc71; stroke:white" />
  <text x="825" y="120" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">G|PS|D|A|PCD|PWT</text>
  <text x="825" y="132" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">U/S|R/W</text>
  
  <rect x="915" y="105" width="35" height="40" style="fill:#E65100; stroke:white" />
  <text x="932" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">P</text>
  
  <!-- ARM64 Descriptor -->
  <text x="50" y="190" font-family="Arial, sans-serif" style="fill:#9b59b6; font-size:14; font-weight:bold">
    ARM64 Descriptor (64-bit, Stage 1)
  </text>
  
  <rect x="50" y="200" width="900" height="70" style="fill:#F5F5F5; stroke:#bdc3c7; stroke-width:2" />
  
  <!-- Bit numbers -->
  <text x="55" y="220" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">63</text>
  <text x="200" y="220" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">54</text>
  <text x="480" y="220" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">51</text>
  <text x="730" y="220" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">12</text>
  <text x="810" y="220" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">11</text>
  <text x="930" y="220" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">0</text>
  
  <rect x="50" y="225" width="170" height="40" style="fill:#95a5a6; stroke:white" />
  <text x="135" y="248" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">Ignored (63-54)</text>
  
  <rect x="220" y="225" width="80" height="40" style="fill:#E65100; stroke:white" />
  <text x="260" y="238" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">XN|PXN</text>
  <text x="260" y="250" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">Contig</text>
  
  <rect x="300" y="225" width="190" height="40" style="fill:#95a5a6; stroke:white" />
  <text x="395" y="245" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">Reserved (53-52)</text>
  
  <rect x="490" y="225" width="250" height="40" style="fill:#1565C0; stroke:white" />
  <text x="615" y="248" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">Output Address (51-12)</text>
  
  <rect x="740" y="225" width="180" height="40" style="fill:#2ecc71; stroke:white" />
  <text x="830" y="238" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">nG|AF|SH|AP</text>
  <text x="830" y="250" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">NS|AttrIdx</text>
  
  <rect x="920" y="225" width="30" height="40" style="fill:#E65100; stroke:white" />
  <text x="935" y="240" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">Type</text>
  <text x="935" y="252" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">Valid</text>
  
  <!-- RISC-V PTE -->
  <text x="50" y="310" font-family="Arial, sans-serif" style="fill:#00796B; font-size:14; font-weight:bold">
    RISC-V PTE (64-bit, Sv39)
  </text>
  
  <rect x="50" y="320" width="900" height="70" style="fill:#F5F5F5; stroke:#bdc3c7; stroke-width:2" />
  
  <!-- Bit numbers -->
  <text x="55" y="340" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">63</text>
  <text x="120" y="340" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">54</text>
  <text x="140" y="340" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">53</text>
  <text x="680" y="340" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">10</text>
  <text x="710" y="340" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">9</text>
  <text x="800" y="340" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">8</text>
  <text x="930" y="340" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:8">0</text>
  
  <rect x="50" y="345" width="80" height="40" style="fill:#95a5a6; stroke:white" />
  <text x="90" y="368" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">Reserved</text>
  
  <rect x="130" y="345" width="560" height="40" style="fill:#1565C0; stroke:white" />
  <text x="410" y="368" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">PPN[2:0] - Physical Page Number (53-10)</text>
  
  <rect x="690" y="345" width="120" height="40" style="fill:#95a5a6; stroke:white" />
  <text x="750" y="368" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">RSW</text>
  
  <rect x="810" y="345" width="140" height="40" style="fill:#2ecc71; stroke:white" />
  <text x="880" y="358" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">D|A|G|U</text>
  <text x="880" y="372" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">X|W|R</text>
  
  <rect x="950" y="345" width="0" height="40" style="fill:none" />
  
  <!-- Bit marker at end -->
  <rect x="920" y="345" width="30" height="40" style="fill:#E65100; stroke:white" />
  <text x="935" y="368" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">V</text>
  
  <!-- Key Features Comparison -->
  <text x="50" y="430" font-family="Arial, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">
    Key Differences
  </text>
  
  <rect x="50" y="440" width="900" height="130" style="fill:#ffffff; stroke:#bdc3c7; stroke-width:2" />
  
  <text x="70" y="465" font-family="Arial, sans-serif" style="fill:#1565C0; font-size:11; font-weight:bold">x86-64:</text>
  <text x="150" y="465" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • R/W bit (no separate read). XD for execute disable. Hardware A/D bits
  </text>
  
  <text x="70" y="495" font-family="Arial, sans-serif" style="fill:#9b59b6; font-size:11; font-weight:bold">ARM64:</text>
  <text x="150" y="495" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • AP bits for permissions. XN/PXN for execute. AF must be set by software before access
  </text>
  <text x="150" y="512" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • AttrIndx points to MAIR_ELx for memory type. Shareability bits for multi-core
  </text>
  
  <text x="70" y="540" font-family="Arial, sans-serif" style="fill:#00796B; font-size:11; font-weight:bold">RISC-V:</text>
  <text x="150" y="540" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Explicit R/W/X bits (most flexible). Hardware A/D bits. RSW for OS use
  </text>
  <text x="150" y="557" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Leaf detection: R|W|X != 0. Cleanest permission model
  </text>
</svg>
</div>
<figcaption><strong>Figure 3.pte:</strong> PTE bit-field layout
comparison across x86-64, ARM64, and RISC-V Sv39: all share
Present/Valid, R/W, User, Dirty, and Accessed bits; x86-64 adds NX;
ARM64 uses AP fields; RISC-V consolidates R/W/X as separate
bits.</figcaption>
</figure>

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="850" height="500" viewBox="0 0 850 500" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="425" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    RISC-V Sv39 Page Table Structure
  </text>
  
  <!-- Virtual Address -->
  <rect x="50" y="70" width="550" height="60" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="325" y="92" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
    Virtual Address (39-bit)
  </text>
  
  <!-- Canonical Extension -->
  <rect x="50" y="70" width="150" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="125" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    Canonical
  </text>
  <text x="125" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (25 bits)
  </text>
  <text x="125" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    63:39 = 38
  </text>
  
  <!-- VPN[2] -->
  <rect x="200" y="70" width="120" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="260" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    VPN[2]
  </text>
  <text x="260" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="260" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    38:30
  </text>
  
  <!-- VPN[1] -->
  <rect x="320" y="70" width="120" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="380" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    VPN[1]
  </text>
  <text x="380" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="380" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    29:21
  </text>
  
  <!-- VPN[0] -->
  <rect x="440" y="70" width="120" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="500" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    VPN[0]
  </text>
  <text x="500" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="500" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    20:12
  </text>
  
  <!-- Offset -->
  <rect x="560" y="70" width="40" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="580" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    Offset
  </text>
  <text x="580" y="120" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    11:0
  </text>
  
  <!-- satp Register -->
  <rect x="650" y="70" width="180" height="90" style="fill:#E65100; stroke:#c0392b; stroke-width:2" />
  <text x="740" y="95" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    satp Register
  </text>
  <text x="740" y="115" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    MODE: Sv39 (1000)
  </text>
  <text x="740" y="132" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    ASID: 16 bits
  </text>
  <text x="740" y="149" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    PPN: Root table
  </text>
  
  <!-- Level 2 (Root) -->
  <rect x="650" y="200" width="170" height="70" style="fill:#9b59b6; stroke:#8e44ad; stroke-width:2" />
  <text x="735" y="225" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Level 2 (Root)
  </text>
  <text x="735" y="245" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 PTEs
  </text>
  <text x="735" y="260" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 1GB region
  </text>
  
  <!-- Level 1 -->
  <rect x="450" y="300" width="160" height="70" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="530" y="325" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Level 1
  </text>
  <text x="530" y="345" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 PTEs
  </text>
  <text x="530" y="360" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 2MB region
  </text>
  
  <!-- Level 0 (Leaf) -->
  <rect x="250" y="400" width="160" height="70" style="fill:#95a5a6; stroke:#7f8c8d; stroke-width:2" />
  <text x="330" y="425" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Level 0 (Leaf)
  </text>
  <text x="330" y="445" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 PTEs
  </text>
  <text x="330" y="460" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 4KB page
  </text>
  
  <!-- Physical Page -->
  <rect x="450" y="415" width="120" height="45" style="fill:#00796B; stroke:#229954; stroke-width:2" />
  <text x="510" y="438" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Physical
  </text>
  <text x="510" y="452" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    4KB Page
  </text>
  
  <!-- Arrows -->
  <path d="M 740 160 L 740 200" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 650 245 L 570 300" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 450 345 L 380 400" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 410 435 L 450 435" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <!-- RISC-V Features Box -->
  <rect x="50" y="180" width="340" height="160" style="fill:#F5F5F5; stroke:#bdc3c7; stroke-width:2" />
  <text x="220" y="205" font-family="Arial, sans-serif" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">
    RISC-V Key Features
  </text>
  
  <text x="60" y="230" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Explicit R/W/X permission bits
  </text>
  <text x="60" y="250" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Leaf detection: Any R/W/X set → leaf PTE
  </text>
  <text x="60" y="270" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Megapages: Leaf at L1 = 2MB
  </text>
  <text x="60" y="290" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Gigapages: Leaf at L2 = 1GB
  </text>
  <text x="60" y="310" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Hardware A/D bit management
  </text>
  <text x="60" y="330" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Sv48 (4-level) and Sv57 (5-level) also supported
  </text>
  
  <!-- Address Space Note -->
  <text x="50" y="25" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:10">
    Address Space: 512GB (39-bit) | Used by: SiFive U74, StarFive JH7110
  </text>
  
  <!-- Simple Note -->
  <text x="50" y="485" font-family="Arial, sans-serif" style="fill:#16a085; font-size:10; font-weight:bold">
    Cleanest design: Numbering from 0 (leaf) up
  </text>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" style="fill:#34495e"></polygon>
    </marker>
  </defs>
</svg>
</div>
<figcaption><strong>Figure 3.riscv:</strong> RISC-V Sv39 three-level
page table: 39-bit virtual addresses split into three 9-bit VPN fields
indexing 512-entry page tables. Sv48 and Sv57 add fourth and fifth
levels for larger address spaces.</figcaption>
</figure>

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="550" viewBox="0 0 900 550" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="450" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    ARM64 Page Table Structure (4KB pages, 48-bit VA)
  </text>
  
  <!-- Virtual Address -->
  <rect x="50" y="70" width="650" height="60" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="375" y="92" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
    Virtual Address (48-bit)
  </text>
  
  <!-- Region Select -->
  <rect x="50" y="70" width="70" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="85" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    Region
  </text>
  <text x="85" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    bit 63
  </text>
  <text x="85" y="127" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    0=TTBR0
  </text>
  
  <!-- Sign Extension -->
  <rect x="120" y="70" width="90" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="165" y="110" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    Sign Ext
  </text>
  <text x="165" y="123" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    62:48
  </text>
  
  <!-- L0 Index -->
  <rect x="210" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="265" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    L0
  </text>
  <text x="265" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="265" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    47:39
  </text>
  
  <!-- L1 Index -->
  <rect x="320" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="375" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    L1
  </text>
  <text x="375" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="375" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    38:30
  </text>
  
  <!-- L2 Index -->
  <rect x="430" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="485" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    L2
  </text>
  <text x="485" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="485" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    29:21
  </text>
  
  <!-- L3 Index -->
  <rect x="540" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="595" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    L3
  </text>
  <text x="595" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="595" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    20:12
  </text>
  
  <!-- Offset -->
  <rect x="650" y="70" width="50" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="675" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    Off
  </text>
  <text x="675" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    11:0
  </text>
  
  <!-- TTBR0_EL1 and TTBR1_EL1 -->
  <rect x="750" y="60" width="130" height="35" style="fill:#E65100; stroke:#c0392b; stroke-width:2" />
  <text x="815" y="82" font-family="Arial, sans-serif" style="fill:white; font-size:11; font-weight:bold; text-anchor:middle">
    TTBR0_EL1
  </text>
  
  <rect x="750" y="100" width="130" height="35" style="fill:#c0392b; stroke:#a93226; stroke-width:2" />
  <text x="815" y="122" font-family="Arial, sans-serif" style="fill:white; font-size:11; font-weight:bold; text-anchor:middle">
    TTBR1_EL1
  </text>
  
  <!-- Level 0 Table -->
  <rect x="700" y="170" width="170" height="70" style="fill:#9b59b6; stroke:#8e44ad; stroke-width:2" />
  <text x="785" y="195" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Level 0 Table
  </text>
  <text x="785" y="215" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 entries
  </text>
  <text x="785" y="230" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 512GB
  </text>
  
  <!-- Level 1 Table -->
  <rect x="520" y="270" width="160" height="70" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="600" y="295" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Level 1 Table
  </text>
  <text x="600" y="315" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 entries
  </text>
  <text x="600" y="330" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 1GB
  </text>
  
  <!-- Level 2 Table -->
  <rect x="340" y="370" width="160" height="70" style="fill:#00796B; stroke:#16a085; stroke-width:2" />
  <text x="420" y="395" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Level 2 Table
  </text>
  <text x="420" y="415" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 entries
  </text>
  <text x="420" y="430" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 2MB
  </text>
  
  <!-- Level 3 Table -->
  <rect x="160" y="470" width="160" height="70" style="fill:#95a5a6; stroke:#7f8c8d; stroke-width:2" />
  <text x="240" y="495" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Level 3 Table
  </text>
  <text x="240" y="515" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 entries
  </text>
  <text x="240" y="530" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 4KB
  </text>
  
  <!-- Physical Page -->
  <rect x="370" y="485" width="120" height="45" style="fill:#00796B; stroke:#229954; stroke-width:2" />
  <text x="430" y="508" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Physical
  </text>
  <text x="430" y="522" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    4KB Page
  </text>
  
  <!-- Arrows -->
  <path d="M 815 95 L 800 170" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 700 215 L 640 270" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 520 315 L 460 370" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 340 415 L 295 470" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 320 505 L 370 505" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <!-- Key Features Box -->
  <rect x="50" y="170" width="280" height="130" style="fill:#F5F5F5; stroke:#bdc3c7; stroke-width:2" />
  <text x="190" y="195" font-family="Arial, sans-serif" style="fill:#212121; font-size:12; font-weight:bold; text-anchor:middle">
    ARM64 Features
  </text>
  <text x="60" y="220" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Dual TTBR (user/kernel split)
  </text>
  <text x="60" y="240" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • ASID tagging (16-bit)
  </text>
  <text x="60" y="260" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Stage 2 for virtualization
  </text>
  <text x="60" y="280" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    • Flexible page sizes (4/16/64KB)
  </text>
  
  <!-- Note -->
  <text x="50" y="25" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:10">
    Used by: Apple M-series, AWS Graviton, Snapdragon
  </text>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" style="fill:#34495e"></polygon>
    </marker>
  </defs>
</svg>
</div>
<figcaption><strong>Figure 3.arm64:</strong> ARM64 four-level page table
with 4 KB pages and 48-bit virtual addresses: L0–L3 tables each hold 512
entries. TTBR0_EL1 points to user-space tables; TTBR1_EL1 to kernel
tables, split at the canonical address hole.</figcaption>
</figure>

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="1000" height="650" viewBox="0 0 1000 650" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="500" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    Five-Level Page Table Structure (x86-64 LA57)
  </text>
  
  <!-- Virtual Address -->
  <rect x="30" y="70" width="800" height="60" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="430" y="92" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
    Virtual Address (57-bit canonical)
  </text>
  
  <!-- Sign Extension -->
  <rect x="30" y="70" width="90" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="75" y="110" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    Sign Ext
  </text>
  <text x="75" y="123" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    (7 bits)
  </text>
  
  <!-- PML5 Index -->
  <rect x="120" y="70" width="120" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="180" y="102" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    PML5
  </text>
  <text x="180" y="115" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="180" y="125" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    56:48
  </text>
  
  <!-- PML4 Index -->
  <rect x="240" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="295" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    PML4
  </text>
  <text x="295" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="295" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    47:39
  </text>
  
  <!-- PDPT Index -->
  <rect x="350" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="405" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    PDPT
  </text>
  <text x="405" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="405" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    38:30
  </text>
  
  <!-- PD Index -->
  <rect x="460" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="515" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    PD
  </text>
  <text x="515" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="515" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    29:21
  </text>
  
  <!-- PT Index -->
  <rect x="570" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="625" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    PT
  </text>
  <text x="625" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (9 bits)
  </text>
  <text x="625" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    20:12
  </text>
  
  <!-- Offset -->
  <rect x="680" y="70" width="150" height="60" style="fill:none; stroke:white; stroke-width:2" />
  <text x="755" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    Offset
  </text>
  <text x="755" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    (12 bits)
  </text>
  <text x="755" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    11:0
  </text>
  
  <!-- CR3 Register with LA57 indicator -->
  <rect x="880" y="70" width="100" height="40" style="fill:#E65100; stroke:#c0392b; stroke-width:2" />
  <text x="930" y="95" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    CR3
  </text>
  <text x="930" y="155" font-family="Arial, sans-serif" style="fill:#E65100; font-size:9; font-weight:bold">
    CR4.LA57=1
  </text>
  
  <!-- Level labels -->
  <text x="10" y="205" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:10; font-weight:bold">L5</text>
  <text x="10" y="295" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:10; font-weight:bold">L4</text>
  <text x="10" y="385" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:10; font-weight:bold">L3</text>
  <text x="10" y="475" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:10; font-weight:bold">L2</text>
  <text x="10" y="565" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:10; font-weight:bold">L1</text>
  
  <!-- PML5 -->
  <rect x="800" y="170" width="170" height="70" style="fill:#E65100; stroke:#d35400; stroke-width:2" />
  <text x="885" y="195" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    PML5
  </text>
  <text x="885" y="215" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 entries
  </text>
  <text x="885" y="230" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 256TB
  </text>
  
  <!-- PML4 -->
  <rect x="640" y="260" width="160" height="70" style="fill:#9b59b6; stroke:#8e44ad; stroke-width:2" />
  <text x="720" y="285" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    PML4
  </text>
  <text x="720" y="305" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 entries
  </text>
  <text x="720" y="320" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 512GB
  </text>
  
  <!-- PDPT -->
  <rect x="480" y="350" width="160" height="70" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="560" y="375" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    PDPT
  </text>
  <text x="560" y="395" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 entries
  </text>
  <text x="560" y="410" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 1GB
  </text>
  
  <!-- PD -->
  <rect x="320" y="440" width="160" height="70" style="fill:#00796B; stroke:#16a085; stroke-width:2" />
  <text x="400" y="465" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    PD
  </text>
  <text x="400" y="485" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 entries
  </text>
  <text x="400" y="500" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 2MB
  </text>
  
  <!-- PT -->
  <rect x="160" y="530" width="160" height="70" style="fill:#95a5a6; stroke:#7f8c8d; stroke-width:2" />
  <text x="240" y="555" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    PT
  </text>
  <text x="240" y="575" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    512 entries
  </text>
  <text x="240" y="590" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
    Each: 4KB
  </text>
  
  <!-- Physical Page -->
  <rect x="370" y="540" width="130" height="50" style="fill:#00796B; stroke:#229954; stroke-width:2" />
  <text x="435" y="565" font-family="Arial, sans-serif" style="fill:white; font-size:10; font-weight:bold; text-anchor:middle">
    Physical
  </text>
  <text x="435" y="580" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    4KB Frame
  </text>
  
  <!-- Arrows -->
  <path d="M 930 110 L 895 170" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 800 215 L 735 260" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 640 305 L 575 350" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 480 395 L 415 440" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 320 485 L 285 530" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 320 565 L 370 565" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <!-- Note -->
  <text x="50" y="630" font-family="Arial, sans-serif" style="fill:#E65100; font-size:11; font-weight:bold">
    Total Address Space: 128 PB (57-bit)
  </text>
  <text x="600" y="630" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:9">
    5 memory accesses on TLB miss (vs 4 for four-level)
  </text>
  
  <text x="50" y="25" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:10">
    Introduced: Intel Ice Lake (2019) | Linux: Kernel 4.14+
  </text>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" style="fill:#34495e"></polygon>
    </marker>
  </defs>
</svg>
</div>
<figcaption><strong>Figure 3.5level:</strong> x86-64 five-level page
table (LA57): adds a fifth PGD level, extending virtual address space to
57 bits (128 PB). Linux enables LA57 at boot when the CPU supports it;
the extra walk adds ~1 cycle of TLB-miss latency.</figcaption>
</figure>

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="1000" height="600" viewBox="0 0 1000 600" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="500" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    Four-Level Page Table Structure (x86-64)
  </text>
  
  <!-- Virtual Address -->
  <g id="virtual-address">
    <rect x="50" y="70" width="700" height="60" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
    <text x="400" y="92" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
      Virtual Address (48-bit canonical)
    </text>
    
    <!-- Sign Extension -->
    <rect x="50" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="105" y="110" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
      Sign Ext
    </text>
    <text x="105" y="123" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
      (16 bits)
    </text>
    
    <!-- PML4 Index -->
    <rect x="160" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="215" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
      PML4
    </text>
    <text x="215" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
      (9 bits)
    </text>
    <text x="215" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
      47:39
    </text>
    
    <!-- PDPT Index -->
    <rect x="270" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="325" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
      PDPT
    </text>
    <text x="325" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
      (9 bits)
    </text>
    <text x="325" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
      38:30
    </text>
    
    <!-- PD Index -->
    <rect x="380" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="435" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
      PD
    </text>
    <text x="435" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
      (9 bits)
    </text>
    <text x="435" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
      29:21
    </text>
    
    <!-- PT Index -->
    <rect x="490" y="70" width="110" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="545" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
      PT
    </text>
    <text x="545" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
      (9 bits)
    </text>
    <text x="545" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
      20:12
    </text>
    
    <!-- Offset -->
    <rect x="600" y="70" width="150" height="60" style="fill:none; stroke:white; stroke-width:2" />
    <text x="675" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
      Offset
    </text>
    <text x="675" y="118" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
      (12 bits)
    </text>
    <text x="675" y="128" font-family="Arial, sans-serif" style="fill:white; font-size:7; text-anchor:middle">
      11:0
    </text>
  </g>
  
  <!-- CR3 Register -->
  <rect x="820" y="70" width="130" height="40" style="fill:#E65100; stroke:#c0392b; stroke-width:2" />
  <text x="885" y="95" font-family="Arial, sans-serif" style="fill:white; font-size:12; font-weight:bold; text-anchor:middle">
    CR3
  </text>
  
  <!-- Level labels -->
  <text x="20" y="210" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:11; font-weight:bold">Level 4</text>
  <text x="20" y="320" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:11; font-weight:bold">Level 3</text>
  <text x="20" y="430" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:11; font-weight:bold">Level 2</text>
  <text x="20" y="540" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:11; font-weight:bold">Level 1</text>
  
  <!-- PML4 -->
  <rect x="780" y="170" width="180" height="80" style="fill:#9b59b6; stroke:#8e44ad; stroke-width:2" />
  <text x="870" y="195" font-family="Arial, sans-serif" style="fill:white; font-size:11; font-weight:bold; text-anchor:middle">
    PML4
  </text>
  <line x1="780" y1="205" x2="960" y2="205" style="stroke:white; stroke-width:1"></line>
  <text x="870" y="225" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    512 entries
  </text>
  <text x="870" y="240" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    Each covers 512GB
  </text>
  
  <!-- PDPT -->
  <rect x="570" y="280" width="180" height="80" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="660" y="305" font-family="Arial, sans-serif" style="fill:white; font-size:11; font-weight:bold; text-anchor:middle">
    PDPT
  </text>
  <line x1="570" y1="315" x2="750" y2="315" style="stroke:white; stroke-width:1"></line>
  <text x="660" y="335" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    512 entries
  </text>
  <text x="660" y="350" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    Each covers 1GB
  </text>
  
  <!-- PD -->
  <rect x="360" y="390" width="180" height="80" style="fill:#00796B; stroke:#16a085; stroke-width:2" />
  <text x="450" y="415" font-family="Arial, sans-serif" style="fill:white; font-size:11; font-weight:bold; text-anchor:middle">
    PD
  </text>
  <line x1="360" y1="425" x2="540" y2="425" style="stroke:white; stroke-width:1"></line>
  <text x="450" y="445" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    512 entries
  </text>
  <text x="450" y="460" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    Each covers 2MB
  </text>
  
  <!-- PT -->
  <rect x="150" y="500" width="180" height="80" style="fill:#95a5a6; stroke:#7f8c8d; stroke-width:2" />
  <text x="240" y="525" font-family="Arial, sans-serif" style="fill:white; font-size:11; font-weight:bold; text-anchor:middle">
    PT
  </text>
  <line x1="150" y1="535" x2="330" y2="535" style="stroke:white; stroke-width:1"></line>
  <text x="240" y="555" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    512 entries
  </text>
  <text x="240" y="570" font-family="Arial, sans-serif" style="fill:white; font-size:8; text-anchor:middle">
    Each covers 4KB
  </text>
  
  <!-- Physical Page -->
  <rect x="410" y="510" width="140" height="60" style="fill:#00796B; stroke:#229954; stroke-width:2" />
  <text x="480" y="535" font-family="Arial, sans-serif" style="fill:white; font-size:11; font-weight:bold; text-anchor:middle">
    Physical Page
  </text>
  <text x="480" y="555" font-family="Arial, sans-serif" style="fill:white; font-size:9; text-anchor:middle">
    4KB Frame
  </text>
  
  <!-- Arrows -->
  <path d="M 885 110 L 885 170" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 215 130 L 840 170" marker-end="url(#arrowhead)" style="fill:none; stroke:#E65100; stroke-width:2; stroke-dasharray:5,5" />
  
  <path d="M 780 220 L 700 280" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 325 130 L 630 280" marker-end="url(#arrowhead)" style="fill:none; stroke:#E65100; stroke-width:2; stroke-dasharray:5,5" />
  
  <path d="M 570 330 L 490 390" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 435 130 L 420 390" marker-end="url(#arrowhead)" style="fill:none; stroke:#E65100; stroke-width:2; stroke-dasharray:5,5" />
  
  <path d="M 360 440 L 310 500" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 545 130 L 270 500" marker-end="url(#arrowhead)" style="fill:none; stroke:#E65100; stroke-width:2; stroke-dasharray:5,5" />
  
  <path d="M 330 540 L 410 540" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <!-- Legend -->
  <text x="820" y="500" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    — Walk path
  </text>
  <line x1="820" y1="510" x2="870" y2="510" style="stroke:#E65100; stroke-width:2; stroke-dasharray:5,5"></line>
  <text x="880" y="515" font-family="Arial, sans-serif" style="fill:#E65100; font-size:10">
    Index path
  </text>
  
  <!-- Note -->
  <text x="600" y="25" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:10">
    Address space: 256TB (48-bit canonical)
  </text>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" style="fill:#34495e"></polygon>
    </marker>
  </defs>
</svg>
</div>
<figcaption><strong>Figure 3.4level:</strong> x86-64 four-level page
table: 48-bit virtual addresses split into PGD (9b) → PUD (9b) → PMD
(9b) → PTE (9b) → page offset (12b). Each level maps 512 GB, 1 GB, 2 MB,
and 4 KB regions respectively.</figcaption>
</figure>

Modern cloud computing depends critically on virtualization: running
multiple guest operating systems simultaneously on shared physical
hardware. Each guest OS believes it has exclusive access to physical
memory, when in reality it\'s sharing the machine with other guests.
Making this illusion work efficiently requires extending our page table
mechanisms to support **two-stage address translation**.

\###

3.6.1 The Virtualization Problem

In traditional (non-virtualized) systems, we have one translation:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Virtual Address (VA) → Physical Address (PA)
:::

The operating system manages page tables, and the MMU translates
addresses using these tables.

With virtualization, we have multiple operating systems running as
\"guests,\" each managing its own page tables. But these page tables
translate to what the guest *thinks* are physical addresses---which the
hypervisor must then translate to actual physical addresses. This
creates a two-level translation problem:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Guest Virtual Address (GVA) → Guest Physical Address (GPA) → Host
Physical Address (HPA)
:::

Or using more standard terminology:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
VA → IPA → PA

(Virtual Address → Intermediate Physical Address → Physical Address)
:::

**Why Not Shadow Page Tables?**

Before hardware virtualization support, VMMs (Virtual Machine Monitors)
like VMware used **shadow page tables**: the hypervisor intercepted
every guest OS page table modification and maintained duplicate
\"shadow\" page tables that directly mapped GVA → HPA. This approach:

- Required trapping every page table update (expensive)
- Complicated synchronization between guest and shadow tables
- Added significant CPU overhead (10-30% in memory-intensive workloads)

Hardware-assisted two-stage translation solves this by letting the guest
manage its own page tables normally while the hypervisor provides a
second translation layer.

### 3.6.2 Intel EPT (Extended Page Tables) {#3.6.2-intel-ept-extended-page-tables}

Intel introduced EPT with the Nehalem microarchitecture in 2008 as part
of Intel VT-x (Virtualization Technology). EPT provides hardware support
for the second stage of translation.

**VMCS and Control**

The **VMCS** (Virtual Machine Control Structure) is a data structure in
memory that stores the complete state of a virtual machine. Among many
other things, it contains:

- **Guest CR3**: Points to the guest\'s page tables (Stage 1: VA → IPA)
- **EPT Pointer (EPTP)**: Points to the EPT structures (Stage 2: IPA →
  PA)

When a guest is running, the CPU uses both:

1\. Guest CR3 for the first translation (VA → IPA)

2\. EPT for the second translation (IPA → PA)

**Stage 1: Guest Page Tables (VA → IPA)**

The guest OS manages these tables exactly as if it were running on bare
metal. If the guest is running 64-bit Linux:

- Uses standard four-level or five-level x86-64 page tables
- Guest CR3 points to the guest\'s PML4
- Translation produces what the guest believes is a physical address
  (actually an IPA)

From the guest\'s perspective, nothing is different---it\'s completely
unaware of the second translation stage.

**Stage 2: EPT (IPA → PA)**

The hypervisor manages EPT structures. EPT uses its own four-level (or
five-level with LA57) page table hierarchy, structurally similar to
regular x86-64 page tables but with different entry formats.

**EPT Page Table Hierarchy**:

1\. **EPT PML4** (or EPT PML5): Top level

2\. **EPT PDPT**: Third level

3\. **EPT PD**: Second level

4\. **EPT PT**: Lowest level

**EPT Page Table Entry Format** (64-bit):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-52: Ignored

Bits 51-12: Physical address of next level or page frame (40 bits)

Bits 11-8: Ignored

Bit 7: Ignored (in EPT PML4E, PDPTE, PDE)

OR Page size for 1GB/2MB pages

Bits 6-3: Ignored / Memory type bits

Bit 2: Execute permission for user-mode linear addresses

Bit 1: Write permission

Bit 0: Read permission
:::

Unlike normal page tables which use Present/Accessed/Dirty bits, EPT
entries have explicit Read/Write/Execute permissions. This gives the
hypervisor fine-grained control over guest memory access.

**Memory Type Bits** (bits 6-3 in leaf entries):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 6-3: IPAT, Type encoding

000: Uncacheable (UC)

001: Write Combining (WC)

100: Write-Through (WT)

101: Write-Protected (WP)

110: Write-Back (WB)
:::

The hypervisor can control caching behavior for guest physical memory,
important for device memory regions.

**Combined Translation Process**

When a guest accesses a virtual address, the hardware performs a complex
combined walk:

1\. **Start with guest VA**

2\. **Walk guest page tables** to get IPA:

\- Read guest CR3 (this is an IPA, so we need to translate it via EPT!)

\- For each level of guest page table:

\- The page table entry address is an IPA

\- Translate IPA to PA using EPT walk

\- Read the page table entry from PA

3\. **Result**: IPA from guest page tables

4\. **Walk EPT** to translate IPA → PA

5\. **Access final PA**

This is where it gets complex: **each access to a guest page table
itself requires an EPT walk**! Let\'s count the memory accesses:

**Worst case (no caching, 4-level guest tables, 4-level EPT)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Guest CR3 lookup: 4 EPT accesses to get CR3 PA

Guest PML4 lookup: 4 EPT accesses to get PML4E

Guest PDPT lookup: 4 EPT accesses to get PDPTE

Guest PD lookup: 4 EPT accesses to get PDE

Guest PT lookup: 4 EPT accesses to get PTE

Final IPA→PA: 4 EPT accesses to get data PA

Data access: 1 access

Total: 25 memory accesses!
:::

This is why EPT seemed impossible when first proposed---25 memory
accesses per instruction would be catastrophic! But in practice, caching
makes it work.

*Reference: Intel 64 and IA-32 Architectures Software Developer\'s
Manual, Volume 3C: System Programming Guide, Part 3, Section 28.2: \"The
Extended Page Table Mechanism (EPT)\" provides complete details on EPT
structure and translation. Intel Corporation, 2024.* **EPT Violations**

When EPT translation fails (missing page, permission violation), the CPU
generates an **EPT violation** VM exit. The hypervisor handles this
similarly to how an OS handles page faults:

- Allocate physical page
- Update EPT entry
- Resume guest

The guest is completely unaware this happened---from its perspective,
memory just worked.

### 3.6.3 AMD NPT (Nested Page Tables) {#3.6.3-amd-npt-nested-page-tables}

AMD introduced NPT (also called AMD-Vi for I/O virtualization) with the
Barcelona microarchitecture in 2007, actually predating Intel\'s EPT by
about a year. The concepts are very similar to EPT, with some
differences in terminology and minor implementation details.

**Nested vs Extended**

AMD uses the term \"nested\" to emphasize that guest page tables are
nested inside hypervisor page tables. The principle is the same as
Intel\'s \"extended\" page tables.

**nCR3 Register**

AMD uses **nCR3** (nested CR3) register, stored in the VMCB (Virtual
Machine Control Block, AMD\'s equivalent of Intel\'s VMCS). This points
to the base of the nested page tables.

**NPT Structure**

NPT uses the same four-level (or five-level) hierarchy as AMD64 normal
paging:

- nPML4 → nPDPT → nPD → nPT

**NPT Entry Format** is similar to Intel EPT, with Read/Write/Execute
permissions:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-52: Available

Bits 51-12: Physical address (40 bits)

Bits 11-9: Available

Bits 8-7: Reserved (0)

Bits 6-5: Ignored

Bit 4-3: Ignored / Memory type

Bit 2: User/Supervisor (U/S)

Bit 1: Read/Write (R/W)

Bit 0: Present (P)
:::

**Translation Process**

AMD NPT works essentially identically to Intel EPT:

1\. Guest manages normal page tables (gCR3 → GVA → GPA)

2\. Hypervisor manages NPT (nCR3 → GPA → HPA)

3\. Combined walk performs both translations

The same explosion of memory accesses occurs without caching, and the
same caching mechanisms mitigate it.

*Reference: AMD64 Architecture Programmer\'s Manual, Volume 2: System
Programming, Section 15.25: \"Nested Paging\" describes AMD\'s nested
page table implementation. AMD, 2023.* **Historical Note**

AMD shipping NPT first gave AMD processors a virtualization performance
advantage in 2007-2008. When Intel shipped EPT in 2008, virtualization
performance on x86 became comparable between the two vendors.

### 3.6.4 ARM Stage 2 Translation {#3.6.4-arm-stage-2-translation}

ARM\'s approach to virtualization emerged with the ARMv7 Virtualization
Extensions and matured in ARMv8-A (64-bit ARM). ARM explicitly models
two translation stages, with clean separation between guest-managed and
hypervisor-managed translations.

**Translation Stages**

ARM terminology:

- **Stage 1**: VA → IPA (managed by guest OS running at EL1)
- **Stage 2**: IPA → PA (managed by hypervisor running at EL2)

**Control Registers** **Stage 1 (Guest)**:

- **TTBR0_EL1**, **TTBR1_EL1**: Guest page table bases
- **TCR_EL1**: Translation Control Register (configures Stage 1)

**Stage 2 (Hypervisor)**:

- **VTTBR_EL2**: Virtual Translation Table Base Register (Stage 2 base)
- **VTCR_EL2**: Virtualization Translation Control Register (configures
  Stage 2)

**Stage 2 Page Table Structure**

Stage 2 uses separate page table structures from Stage 1, with different
descriptor formats. For 4KB pages with IPA size up to 48 bits:

**Stage 2 Table Structure**:

- Can be 2, 3, or 4 levels depending on IPA size
- Each table: 512 or more entries
- Concatenated tables at Level 0 for some configurations

**Stage 2 Descriptor Format** (different from Stage 1!):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-59: Ignored

Bits 58-55: Reserved

Bit 54: XN (Execute Never) for Stage 1 EL0 translations

Bit 53: PXN (Privileged Execute Never)

Bit 52: Contiguous hint

Bits 51-12: Output address (PA) or next level table address

Bits 11-10: Reserved

Bits 9-8: SH (Shareability)

Bits 7-6: S2AP (Stage 2 Access Permissions)

00: No access

01: Read-only

10: Write-only

11: Read/Write

Bits 5-4: MemAttr (Memory attributes)

Bit 3-2: Ignored

Bit 1: Descriptor type (0 = block, 1 = table/page)

Bit 0: Valid
:::

Key differences from Stage 1:

- **S2AP** instead of AP: Simpler permission model
- **MemAttr** instead of AttrIndx: Direct memory type encoding
- **Separate XN/PXN**: Control execution at different privilege levels

**Combined Translation**

When a guest running at EL1 accesses memory:

1\. **Stage 1 translation**: VA → IPA using TTBR0_EL1/TTBR1_EL1

\- Guest OS manages these tables

\- Four-level walk (typically)

2\. **Stage 2 translation**: IPA → PA using VTTBR_EL2

\- Hypervisor manages these tables

\- Up to four-level walk

Similar to x86, each access to Stage 1 page tables requires a Stage 2
translation of the table address. Maximum memory accesses:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
4 (Stage 1 levels) × 4 (Stage 2 per access) + 4 (final IPA→PA) = 20
memory accesses
:::

(Slightly better than x86\'s 25 because ARM\'s Stage 1 and Stage 2 are
more independent in implementation.)

**Real-World ARM Hypervisors** **KVM/ARM**: Linux\'s built-in hypervisor

- Uses Stage 2 extensively
- Efficient implementation on Cortex-A series and Neoverse

**Xen on ARM**: Server virtualization

- Stage 2 for guest isolation
- Used in embedded and automotive (safety-critical virtualization)

**Apple Virtualization Framework**: macOS/iOS hypervisor

- Powers Linux VMs on M-series Macs
- Highly optimized Stage 2 implementation

*Reference: ARM Architecture Reference Manual for ARMv8-A, ARM DDI
0487J.a, Section D5.2: \"The VMSAv8-64 translation system\",
specifically Section D5.2.5: \"Translation table walks for the stage 2
translations\" and Section D5.3: \"VMSAv8-64 translation table format\".
ARM Limited, 2024.*

### 3.6.5 RISC-V Hypervisor Extension {#3.6.5-risc-v-hypervisor-extension}

RISC-V added hypervisor support relatively recently---the Hypervisor
Extension was frozen in 2019 and ratified as v1.0 in 2021. Being newer,
it learned from x86 and ARM\'s experiences and features a clean,
orthogonal design.

**Two-Stage Translation in RISC-V**

RISC-V terminology:

- **VS-stage** (Virtual Supervisor stage): VA → GPA (Guest Physical
  Address)
- **G-stage** (Hypervisor/Guest stage): GPA → SPA (Supervisor Physical
  Address)

This is conceptually identical to x86 EPT and ARM Stage 2, just with
different names.

**Control Registers** **VS-stage (Guest)**:

- **vsatp**: Virtual Supervisor Address Translation and Protection

\- Same format as regular satp

\- Guest manages this

**G-stage (Hypervisor)**:

- **hgatp**: Hypervisor Guest Address Translation and Protection

\- Format similar to satp

\- Hypervisor manages this

**hgatp Register Format** (RV64):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-60: MODE

0000 = Bare (no translation)

1000 = Sv39x4 (39-bit GPA, 3 levels)

1001 = Sv48x4 (48-bit GPA, 4 levels)

1010 = Sv57x4 (57-bit GPA, 5 levels)

Bits 59-44: VMID (Virtual Machine ID, 14 bits)

Bits 43-0: PPN of root G-stage page table
:::

**G-Stage Page Table Format**

G-stage page tables use the same structure as regular RISC-V page
tables, with 64-bit PTEs:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Bits 63-54: Reserved (0)

Bits 53-10: PPN (Physical Page Number)

Bits 9-8: RSW (Reserved for software)

Bit 7: D (Dirty)

Bit 6: A (Accessed)

Bit 5: G (Global)

Bit 4: U (User)

Bit 3: X (Execute)

Bit 2: W (Write)

Bit 1: R (Read)

Bit 0: V (Valid)
:::

The beauty of RISC-V: G-stage tables are structurally identical to
VS-stage tables, just managed by different software layers!

**Combined Translation**

For a guest with Sv39 VS-stage and Sv39x4 G-stage:

1\. **VS-stage walk** (3 levels):

\- Each level lookup requires G-stage translation

\- 3 levels × 3 G-stage walks = 9 memory accesses

2\. **Final GPA → SPA**:

\- G-stage walk: 3 memory accesses

3\. **Data access**: 1 access

**Total: 13 memory accesses** (better than x86\'s 25 or ARM\'s 20!)

This is because RISC-V defaulted to 3-level VS-stage tables instead of
4, reducing the worst case.

*Reference: The RISC-V Instruction Set Manual, Volume II: Privileged
Architecture, Version 1.12, Chapter 8: \"Hypervisor Extension\"
describes the complete hypervisor implementation including two-stage
address translation. RISC-V International, 2021.*

### 3.6.6 Performance Impact and Mitigations {#3.6.6-performance-impact-and-mitigations}

The explosion of memory accesses for two-stage translation would be
disastrous without hardware mitigations. Multiple techniques work
together to make virtualization practical:

**1. Combined TLB (VA → PA Direct)**

Modern CPUs cache the **final translation** (VA → PA) directly in the
TLB, skipping both guest and hypervisor page table walks on a hit. The
TLB entry is tagged with:

- **VPID/ASID**: Identifies the virtual machine
- **Process ASID**: Identifies the process within the VM

This allows TLB entries from multiple VMs and multiple processes to
coexist.

**Intel VPID** (Virtual Processor ID):

- 16-bit tag in TLB entries
- Enabled via VMCS
- Avoids TLB flush on VM entry/exit

**AMD ASID** (Address Space ID):

- Similar concept to VPID
- Also 16-bit
- Stored in VMCB

**ARM ASID and VMID**:

- **ASID**: 8-bit or 16-bit, identifies process
- **VMID**: Identifies VM
- TLB entries tagged with both

**RISC-V VMID**:

- 14-bit tag in hgatp
- TLB entries tagged with VMID + ASID

With a combined TLB hit (95-99% for typical workloads), two-stage
translation has **zero overhead** for that access!

**2. Page Walk Caches for Both Stages**

Modern CPUs cache intermediate page table entries for both stages:

- Guest page table entries (PML4E, PDPTE, PDE)
- EPT/NPT/Stage 2 page table entries

If the PWC contains cached entries, many of the potential 20-25 memory
accesses are eliminated.

**3. Huge Pages**

Using 2MB or 1GB pages in either stage dramatically reduces translation
overhead:

- Fewer page table levels to walk
- Better TLB coverage (one TLB entry covers more memory)

Many hypervisors aggressively use huge pages when possible.

**Real-World Performance Measurements**

Multiple academic studies have measured two-stage translation overhead:

**Adams & Agesen (2006), VMware**:

- Compared software (shadow) vs hardware (EPT) virtualization
- Hardware two-stage translation: 2-7% overhead
- Shadow paging: 15-30% overhead
- **Conclusion**: Hardware support critical for acceptable performance

*Reference: Adams, K., & Agesen, O. (2006). \"A comparison of software
and hardware techniques for x86 virtualization\". ACM SIGPLAN Notices,
41(11), 2-13. This landmark paper from VMware researchers demonstrated
the performance advantages of hardware-assisted virtualization.* **Barr
et al. (2010), VMware Mobile**:

- Nested page tables on mobile ARM processors
- Overhead: 3-5% for typical mobile workloads
- Higher overhead (10-15%) for memory-intensive tasks
- **Conclusion**: Acceptable for mobile virtualization

*Reference: Barr, K., et al. (2010). \"The VMware mobile virtualization
platform: is that a hypervisor in your pocket?\". ACM SIGOPS Operating
Systems Review, 44(4), 124-135.* **Performance Summary**

Typical virtualization overhead with modern hardware support:

- **Best case** (TLB-friendly workload): \<2% overhead
- **Typical case** (mixed workload): 2-7% overhead
- **Worst case** (TLB-thrashing workload): 10-20% overhead

Compare to 50-80% overhead with pure software virtualization, and
hardware support clearly justifies its complexity!

### 3.6.7 Why Two Stages Matter {#3.6.7-why-two-stages-matter}

Two-stage translation enables modern cloud computing. Without it:

- **AWS, Azure, Google Cloud** wouldn\'t be feasible at current scale
- **Container** runtimes still benefit (nested virtualization scenarios)
- **Mobile virtualization** (running multiple OS environments) wouldn\'t
  work
- **Security** features like Intel TDX and AMD SEV depend on it

The complexity of 20+ potential memory accesses is completely hidden
from both guest operating systems and applications by sophisticated
caching. This is a triumph of hardware/software co-design: software
(hypervisors) provides the management interfaces, hardware provides
transparent acceleration.

## 3.7 What Gets Cached: TLB and Page Walk Caches {#3.7-what-gets-cached-tlb-and-page-walk-caches}

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="950" height="650" viewBox="0 0 950 650" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="475" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    Two-Stage Address Translation (Virtualization)
  </text>
  
  <!-- Guest VA -->
  <rect x="50" y="80" width="200" height="50" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="150" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
    Guest Virtual
  </text>
  <text x="150" y="122" font-family="Arial, sans-serif" style="fill:white; font-size:12; text-anchor:middle">
    Address (VA)
  </text>
  
  <!-- Stage 1: Guest Page Tables -->
  <rect x="300" y="60" width="250" height="100" style="fill:#9b59b6; stroke:#8e44ad; stroke-width:3" />
  <text x="425" y="85" font-family="Arial, sans-serif" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">
    Stage 1: Guest Tables
  </text>
  <text x="425" y="105" font-family="Arial, sans-serif" style="fill:white; font-size:11; text-anchor:middle">
    (Managed by Guest OS)
  </text>
  <text x="425" y="125" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    Guest CR3/TTBR/satp
  </text>
  <text x="425" y="145" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    PML4→PDPT→PD→PT
  </text>
  
  <!-- Arrow from VA to Stage 1 -->
  <path d="M 250 105 L 300 105" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:3" />
  
  <!-- IPA -->
  <rect x="600" y="80" width="220" height="50" style="fill:#E65100; stroke:#d35400; stroke-width:2" />
  <text x="710" y="100" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
    Intermediate Physical
  </text>
  <text x="710" y="117" font-family="Arial, sans-serif" style="fill:white; font-size:12; text-anchor:middle">
    Address (IPA / GPA)
  </text>
  
  <!-- Arrow from Stage 1 to IPA -->
  <path d="M 550 105 L 600 105" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:3" />
  
  <!-- Stage 2: EPT/NPT -->
  <rect x="300" y="250" width="250" height="100" style="fill:#00796B; stroke:#16a085; stroke-width:3" />
  <text x="425" y="275" font-family="Arial, sans-serif" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">
    Stage 2: EPT/NPT/G-stage
  </text>
  <text x="425" y="295" font-family="Arial, sans-serif" style="fill:white; font-size:11; text-anchor:middle">
    (Managed by Hypervisor)
  </text>
  <text x="425" y="315" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    Intel: EPTP (EPT pointer)
  </text>
  <text x="425" y="335" font-family="Arial, sans-serif" style="fill:white; font-size:10; text-anchor:middle">
    AMD: nCR3 | ARM: VTTBR_EL2
  </text>
  
  <!-- Arrow from IPA to Stage 2 -->
  <path d="M 710 130 L 710 190 L 425 190 L 425 250" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:3" />
  <text x="720" y="165" font-family="Arial, sans-serif" style="fill:#34495e; font-size:11; font-weight:bold">
    Translate IPA
  </text>
  
  <!-- Host PA -->
  <rect x="600" y="275" width="220" height="50" style="fill:#00796B; stroke:#229954; stroke-width:2" />
  <text x="710" y="295" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
    Host Physical
  </text>
  <text x="710" y="312" font-family="Arial, sans-serif" style="fill:white; font-size:12; text-anchor:middle">
    Address (PA / HPA)
  </text>
  
  <!-- Arrow from Stage 2 to PA -->
  <path d="M 550 300 L 600 300" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:3" />
  
  <!-- Memory Access Counter -->
  <rect x="50" y="400" width="850" height="220" style="fill:#F5F5F5; stroke:#bdc3c7; stroke-width:2" />
  <text x="475" y="425" font-family="Arial, sans-serif" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">
    Worst-Case Memory Accesses (No Caching)
  </text>
  
  <!-- x86-64 with EPT -->
  <text x="70" y="455" font-family="Arial, sans-serif" style="fill:#1565C0; font-size:12; font-weight:bold">
    x86-64 with EPT (4-level + 4-level):
  </text>
  <text x="90" y="475" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Guest CR3 access: 4 EPT walks = 4 accesses
  </text>
  <text x="90" y="495" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Guest PML4 read: 4 EPT walks = 4 accesses
  </text>
  <text x="90" y="515" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Guest PDPT read: 4 EPT walks = 4 accesses
  </text>
  <text x="90" y="535" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Guest PD read: 4 EPT walks = 4 accesses
  </text>
  <text x="90" y="555" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Guest PT read: 4 EPT walks = 4 accesses
  </text>
  <text x="90" y="575" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    • Final IPA→PA: 4 EPT walks = 4 accesses
  </text>
  <text x="90" y="600" font-family="Arial, sans-serif" style="fill:#E65100; font-size:11; font-weight:bold">
    TOTAL: 24 memory accesses + 1 data = 25 accesses!
  </text>
  
  <!-- Mitigations -->
  <rect x="520" y="450" width="370" height="155" style="fill:#ffffff; stroke:#1565C0; stroke-width:2" />
  <text x="705" y="475" font-family="Arial, sans-serif" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">
    Performance Mitigations
  </text>
  <text x="540" y="500" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10; font-weight:bold">
    ✓ Combined TLB
  </text>
  <text x="555" y="518" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    Cache VA→PA directly (skip both stages)
  </text>
  
  <text x="540" y="543" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10; font-weight:bold">
    ✓ VPID/VMID Tagging
  </text>
  <text x="555" y="561" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    Multiple VMs share TLB without flushing
  </text>
  
  <text x="540" y="586" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10; font-weight:bold">
    ✓ Page Walk Caches (Both Stages)
  </text>
  <text x="555" y="604" font-family="Arial, sans-serif" style="fill:#34495e; font-size:9">
    Cache intermediate entries from both tables
  </text>
  
  <!-- Reality Note -->
  <rect x="50" y="210" width="850" height="30" style="fill:#fff9e6; stroke:#f39c12; stroke-width:2" />
  <text x="475" y="230" font-family="Arial, sans-serif" style="fill:#E65100; font-size:11; font-weight:bold; text-anchor:middle">
    ⚡ With caching: Typical overhead is only 2-7% | TLB hit rate: 95-99% → Most accesses cost 0!
  </text>
  
  <!-- Platform Labels -->
  <text x="50" y="25" font-family="Arial, sans-serif" font-style="fill:#7f8c8d; font-size:10">
    Intel: EPT | AMD: NPT | ARM: Stage 2 | RISC-V: G-stage
  </text>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" style="fill:#34495e"></polygon>
    </marker>
  </defs>
</svg>
</div>
<figcaption><strong>Figure 3.2stage:</strong> Two-stage address
translation for virtualization: Stage 1 (guest OS) maps guest virtual →
guest physical; Stage 2 (hypervisor) maps guest physical → host
physical. Intel EPT and ARM stage-2 tables implement this in
hardware.</figcaption>
</figure>

We\'ve seen that page table walks can require anywhere from 1 to 25
memory accesses depending on the number of levels and whether
virtualization is active. These accesses would devastate performance if
they occurred on every memory instruction. Modern processors employ
multiple levels of caching to mitigate this overhead. Understanding what
gets cached---and critically, what doesn\'t---is essential for
performance tuning and system design.

### 3.7.1 Translation Lookaside Buffer (TLB): Final Translation Cache {#3.7.1-translation-lookaside-buffer-tlb-final-translation-cache}

The TLB is the primary cache for address translation, and most
developers are familiar with its basic purpose. However, understanding
precisely what it caches and its limitations helps explain many
performance behaviors.

**What the TLB Caches**

The TLB caches **complete translations**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
VA → PA (complete final mapping)
:::

Each TLB entry stores:

- **Virtual page number** (VPN): The tag
- **Physical page frame number** (PFN): The result
- **Permission bits**: R/W/X permissions
- **Additional flags**: Dirty, Accessed, Global, etc.
- **ASID/PCID**: Process identifier for multi-process caching
- **Page size**: 4KB, 2MB, or 1GB

**What the TLB Does NOT Cache**

Critically, the TLB does **not** cache:

- Intermediate page table entries (PML4E, PDPTE, PDE)
- Page table pointers
- The address of page tables themselves
- Partial translations (e.g., just VA → IPA in virtualization)

When we have a TLB miss, the hardware page walker must still perform the
complete page table walk, reading every level from memory (or cache).

**TLB Organization**

Modern processors have multiple TLB levels with different
characteristics:

**L1 TLB**: Split into instruction and data

- **L1 ITLB** (Instruction TLB): Caches translations for code
- **L1 DTLB** (Data TLB): Caches translations for data

**L2 TLB** (or STLB - Shared TLB): Unified, larger, slightly slower

- Shared between instructions and data
- Significantly more entries than L1
- Backing store for L1 TLBs

**Real-World TLB Sizes**

Let\'s examine actual TLB configurations from modern processors:

**Intel Skylake (2015-2019)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
L1 DTLB:

\- 64 entries for 4KB pages

\- 32 entries for 2MB/4MB pages

\- 4 entries for 1GB pages

L1 ITLB:

\- 128 entries for 4KB pages

\- 8 entries for 2MB/4MB pages

L2 STLB (shared):

\- 1536 entries for 4KB or 2MB pages (shared pool)

\- 16 entries for 1GB pages
:::

*Reference: Intel 64 and IA-32 Architectures Optimization Reference
Manual, Section 2.5: \"Translation Lookaside Buffers (TLB)\". Intel
Corporation, 2024.* **AMD Zen 3 (2020)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
L1 DTLB:

\- 72 entries for 4KB pages

\- 72 entries for 2MB/1GB pages (separate pool)

L1 ITLB:

\- 64 entries for 4KB pages

\- 64 entries for 2MB pages

L2 TLB (unified):

\- 2048 entries for 4KB/2MB pages

\- 1024 entries for 1GB pages
:::

AMD Zen 3\'s L2 TLB is notably larger than Intel Skylake\'s, reflecting
AMD\'s emphasis on reducing TLB misses.

*Reference: AMD, \"Software Optimization Guide for AMD Family 19h
Processors\" (Zen 3), Publication #56665, Revision 3.01, Section 2.10:
\"Translation Lookaside Buffer\". AMD, 2020.* **ARM Cortex-A77 (2019)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
L1 DTLB:

\- 48 fully-associative entries for 4KB pages

\- 32 fully-associative entries for larger pages

L1 ITLB:

\- 48 fully-associative entries for 4KB pages

\- 32 fully-associative entries for larger pages

L2 TLB (unified):

\- 1280 entries, 4-way set-associative

\- Supports 4KB, 16KB, 64KB, 2MB, 32MB, 512MB, 1GB pages
:::

*Reference: ARM Cortex-A77 Core Technical Reference Manual, Section 5.2:
\"TLB organization\". ARM Limited, 2019.* **Coverage Analysis**

Let\'s calculate how much memory a TLB can cover:

**Intel Skylake L2 STLB (worst case - all 4KB pages)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
1536 entries × 4KB = 6,144 KB = 6 MB
:::

**Intel Skylake L2 STLB (best case - all 1GB pages)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
16 entries × 1GB = 16 GB
:::

**AMD Zen 3 L2 TLB (4KB pages)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
2048 entries × 4KB = 8,192 KB = 8 MB
:::

**AMD Zen 3 L2 TLB (2MB pages)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
2048 entries × 2MB = 4,096 MB = 4 GB
:::

**ARM Cortex-A77 L2 TLB (4KB pages)**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
1280 entries × 4KB = 5,120 KB = 5 MB
:::

These numbers reveal a critical insight: if your working set exceeds 5-8
MB with 4KB pages, you\'ll experience TLB thrashing. Using huge pages
(2MB) extends coverage to multiple gigabytes.

### 3.7.2 Page Walk Caches: The Hidden Optimization {#3.7.2-page-walk-caches-the-hidden-optimization}

While TLBs are well-known, page walk caches (PWCs) are less documented
but equally important for modern processor performance. PWCs cache
**intermediate page table entries**, reducing the number of memory
accesses needed on a TLB miss.

**What Page Walk Caches Do**

PWCs cache upper-level page table entries:

- PML4 entries
- PDPT entries
- PD entries

These caches sit between the TLB and main memory. On a TLB miss, the
hardware page walker checks the PWC before accessing memory.

**Why PWCs Matter**

Without PWC, a TLB miss on x86-64 requires 4 memory accesses:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
CR3 → PML4E → PDPTE → PDE → PTE → PA

read read read read
:::

With PWC hits on upper levels:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
CR3 → PML4E → PDPTE → PDE → PTE → PA

(PWC) (PWC) (PWC) read
:::

Only 1 memory access needed instead of 4!

**Intel\'s Page Walk Cache (Undocumented)**

Intel doesn\'t officially document PWC details in their optimization
manuals, but researchers have measured its existence and
characteristics:

**Barr et al. (2011)** measured Intel processors and found:

- PWC caches PML4, PDPT, and PD entries
- Estimated size: \~32 entries per level
- Dramatically reduces page walk latency
- Works transparently---software can\'t control it

*Reference: Barr, T. W., Cox, A. L., & Rixner, S. (2011). \"Translation
caching: skip, don\'t walk (the page table)\". ACM SIGARCH Computer
Architecture News, 39(3), 48-59. This paper characterized Intel\'s page
walk cache through experimental measurement.* **Bhattacharjee et al.
(2011)** further analyzed PWC:

- Called it \"intermediate TLB\" or \"TLB for page tables\"
- Showed 50-80% reduction in page walk memory accesses
- Proposed shared last-level TLBs to further improve hit rates

*Reference: Bhattacharjee, A., Lustig, D., & Martonosi, M. (2011).
\"Shared last-level TLBs for chip multiprocessors\". Proceedings of the
17th IEEE Symposium on High Performance Computer Architecture (HPCA),
62-73.* **AMD\'s Page Map Cache (PMC)**

AMD is slightly more transparent about caching intermediate entries:

- Caches PML4E, PDPTE, PDE entries
- Works in conjunction with L2 TLB
- Size not officially specified (estimated \~32-64 entries)

*Reference: AMD Software Optimization Guide mentions the Page Map Cache
but provides limited implementation details. AMD, 2023.*

### 3.7.3 Caching in Virtualization: Combined TLB {#3.7.3-caching-in-virtualization-combined-tlb}

Two-stage translation introduces new caching challenges. We could cache:

1\. VA → IPA (guest translation only)

2\. IPA → PA (hypervisor translation only)

3\. VA → PA (complete combined translation)

Modern processors use option 3: **cache the final VA → PA mapping
directly**, skipping both intermediate stages!

**VPID/ASID Tagging**

To allow multiple VMs to share the TLB without conflicts, entries are
tagged with identifiers:

**Intel VPID (Virtual Processor ID)**:

- 16-bit identifier
- Each VM gets a unique VPID
- Stored in VMCS
- TLB entries tagged: {VPID, ASID, VPN} → {PFN, permissions}
- Avoids TLB flush on VM entry/exit

When the hypervisor switches VMs:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Old behavior (no VPID): Flush entire TLB

New behavior (with VPID): Keep all entries, use VPID to distinguish
:::

*Reference: Intel 64 and IA-32 Architectures Software Developer\'s
Manual, Volume 3C, Section 28.3.3.1: \"Virtual-Processor Identifiers
(VPIDs)\" describes VPID implementation. Intel Corporation, 2024.* **AMD
ASID**:

- Similar concept to VPID
- 32-bit ASID space (though typically only lower bits used)
- Stored in VMCB

**ARM VMID and ASID**:

- **VMID** (Virtual Machine ID): 8 or 16 bits, identifies VM
- **ASID** (Address Space ID): 8 or 16 bits, identifies process within
  VM
- TLB entries tagged with both: {VMID, ASID, VA} → {PA, permissions}

This allows:

- Multiple VMs active simultaneously (different VMIDs)
- Multiple processes per VM (different ASIDs)
- No flush needed when switching contexts

*Reference: ARM Architecture Reference Manual for ARMv8-A, ARM DDI
0487J.a, Section D5.10.3: \"TLB maintenance requirements\" describes
VMID and ASID usage. ARM Limited, 2024.* **RISC-V VMID**:

- 14-bit VMID in hgatp register
- Works with ASID from satp
- Combined tagging for virtualization TLB

**Measured Impact** **Bhattacharjee & Martonosi (2009)** measured TLB
behavior with virtualization:

- TLB hit rate: 85-95% for typical virtualized workloads
- VPID/ASID support improved hit rate by 10-15 percentage points
- Without tagging, VM switches caused severe TLB thrashing

*Reference: Bhattacharjee, A., & Martonosi, M. (2009). \"Characterizing
the TLB behavior of emerging parallel workloads on chip
multiprocessors\". Proceedings of the 18th International Conference on
Parallel Architectures and Compilation Techniques (PACT), 29-40.*

### 3.7.4 What Is NOT Cached: Important Clarifications {#3.7.4-what-is-not-cached-important-clarifications}

Understanding what caching structures **don\'t** do is as important as
understanding what they do:

**TLB Does NOT Cache**:

- Page table entries for non-present pages (Present bit = 0)
- Intermediate page table entries (PML4E, PDPTE, PDE)
- Permission bits separately (only combined with translation)
- Failed translations (page faults)

**Page Walk Cache Does NOT Cache**:

- Final page translations (that\'s the TLB\'s job)
- Complete paths (only individual level entries)
- Cross-process entries (flushed on context switch unless Global)

**Neither TLB nor PWC Caches**:

- Page table structures themselves (those may be in L1/L2/L3 cache)
- Multiple translations for the same VA (only most recent)
- Speculative translations (except in research proposals)

**No Persistence Across**:

- Context switches (unless marked Global/nG=0)

- TLB flush instructions (INVLPG, INVPCID on x86)

- CR3/TTBR/satp writes (unless PCID/ASID preserves entries)

- VM exits (unless VPID preserves entries)

  ### 3.7.5 Caching Hierarchy Summary Table {#3.7.5-caching-hierarchy-summary-table}

Here\'s a comprehensive view of what gets cached where:

\| Structure \| What It Caches \| What It Doesn\'t Cache \| Typical Size
\| Access Time \|

\|\-\-\-\-\-\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\--\|

\| **L1 TLB** \| VA→PA (final) \| Intermediate PTEs \| 64-128 entries \|
0-1 cycles \|

\| **L2 TLB** \| VA→PA (final) \| Intermediate PTEs \| 1280-2048 entries
\| 5-10 cycles \|

\| **PWC** \| PML4E, PDPTE, PDE \| Final PTEs, VA→PA \| \~32-64
entries/level \| 10-20 cycles \|

\| **L1 Cache** \| Page table data \| Nothing special \| 32-64 KB \| 3-5
cycles \|

\| **L2 Cache** \| Page table data \| Nothing special \| 256-512 KB \|
10-15 cycles \|

\| **L3 Cache** \| Page table data \| Nothing special \| 8-32 MB \|
40-60 cycles \|

\| **RAM** \| Everything \| - \| GBs \| 100-200 cycles \|

This hierarchy explains why TLB hit rate is so critical:

- **TLB hit**: 0-1 cycles for translation
- **TLB miss, PWC hit**: 10-20 cycles
- **TLB miss, PWC miss, L3 hit**: 50-80 cycles
- **TLB miss, PWC miss, DRAM**: 150-250 cycles

The difference between a TLB hit and a complete miss can be 200× in
latency!

### 3.7.6 Performance Implications {#3.7.6-performance-implications}

**Application-Level Impact**:

Programs with good **spatial locality** (accessing nearby addresses)
benefit from:

- Fewer unique pages accessed → better TLB hit rate
- Sequential page table entries → better PWC hit rate
- Page tables stay cache-hot → faster walks

Programs with poor **spatial locality** (random access patterns) suffer:

- Many unique pages → TLB thrashing
- Scattered page table access → PWC misses
- Cold page tables → DRAM latency

**Huge Pages as TLB Optimization**:

Using 2MB pages instead of 4KB pages:

- Reduces page count by 512× for same memory
- Each TLB entry covers 512× more memory
- Dramatically improves TLB hit rate

Example: 1GB working set

- With 4KB pages: 262,144 pages (can\'t fit in TLB)
- With 2MB pages: 512 pages (fits in L2 TLB!)

This is why databases, HPC applications, and VMs aggressively use huge
pages.

Understanding caching behavior is crucial for:

- **System tuning**: Page size selection, huge page usage

- **Performance debugging**: Identifying TLB thrashing

- **Architecture design**: Balancing TLB size vs complexity

  ## 3.8 Hardware Page Table Walker {#3.8-hardware-page-table-walker}

  <figure
  style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
  <div
  style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
  <svg width="1000" height="700" viewBox="0 0 1000 700" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <!-- Title -->
  <text x="500" y="30" font-family="Arial, sans-serif" style="fill:#212121; font-size:18; font-weight:bold; text-anchor:middle">
    TLB vs Page Walk Cache: What Gets Cached
  </text>
  
  <!-- Virtual Address -->
  <rect x="50" y="70" width="200" height="50" style="fill:#1565C0; stroke:#2980b9; stroke-width:2" />
  <text x="150" y="100" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
    Virtual Address
  </text>
  
  <!-- Page Table Walk -->
  <rect x="300" y="50" width="400" height="90" style="fill:#F5F5F5; stroke:#bdc3c7; stroke-width:2" />
  <text x="500" y="75" font-family="Arial, sans-serif" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">
    Page Table Walk (4-level x86-64)
  </text>
  <text x="500" y="100" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10; text-anchor:middle">
    CR3 → PML4E → PDPTE → PDE → PTE
  </text>
  <text x="500" y="125" font-family="Arial, sans-serif" style="fill:#7f8c8d; font-size:9; text-anchor:middle">
    (4 memory accesses without caching)
  </text>
  
  <!-- Physical Address -->
  <rect x="750" y="70" width="200" height="50" style="fill:#00796B; stroke:#229954; stroke-width:2" />
  <text x="850" y="100" font-family="Arial, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">
    Physical Address
  </text>
  
  <!-- Arrows -->
  <path d="M 250 95 L 300 95" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  <path d="M 700 95 L 750 95" marker-end="url(#arrowhead)" style="fill:none; stroke:#34495e; stroke-width:2" />
  
  <!-- TLB Section -->
  <rect x="50" y="200" width="400" height="220" style="fill:#fff9e6; stroke:#f39c12; stroke-width:3" />
  <text x="250" y="230" font-family="Arial, sans-serif" style="fill:#E65100; font-size:15; font-weight:bold; text-anchor:middle">
    TLB (Translation Lookaside Buffer)
  </text>
  
  <text x="70" y="260" font-family="Arial, sans-serif" style="fill:#212121; font-size:12; font-weight:bold">
    What TLB Caches:
  </text>
  <text x="80" y="285" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10">
    ✓ Complete VA → PA translation (final result)
  </text>
  <text x="80" y="305" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10">
    ✓ Permission bits (R/W/X, U/S)
  </text>
  <text x="80" y="325" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10">
    ✓ Page size (4KB / 2MB / 1GB)
  </text>
  <text x="80" y="345" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10">
    ✓ ASID/PCID tag (process ID)
  </text>
  
  <text x="70" y="375" font-family="Arial, sans-serif" style="fill:#212121; font-size:12; font-weight:bold">
    What TLB Does NOT Cache:
  </text>
  <text x="80" y="395" font-family="Arial, sans-serif" style="fill:#E65100; font-size:10">
    ✗ Intermediate PTEs (PML4E, PDPTE, PDE)
  </text>
  <text x="80" y="413" font-family="Arial, sans-serif" style="fill:#E65100; font-size:10">
    ✗ Page table pointers
  </text>
  
  <!-- PWC Section -->
  <rect x="550" y="200" width="400" height="220" style="fill:#e8f8f5; stroke:#16a085; stroke-width:3" />
  <text x="750" y="230" font-family="Arial, sans-serif" style="fill:#16a085; font-size:15; font-weight:bold; text-anchor:middle">
    PWC (Page Walk Cache)
  </text>
  
  <text x="570" y="260" font-family="Arial, sans-serif" style="fill:#212121; font-size:12; font-weight:bold">
    What PWC Caches:
  </text>
  <text x="580" y="285" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10">
    ✓ Intermediate PTEs (PML4E, PDPTE, PDE)
  </text>
  <text x="580" y="305" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10">
    ✓ Pointers to next-level tables
  </text>
  <text x="580" y="325" font-family="Arial, sans-serif" style="fill:#00796B; font-size:10">
    ✓ Partial translation paths
  </text>
  
  <text x="570" y="355" font-family="Arial, sans-serif" style="fill:#212121; font-size:12; font-weight:bold">
    What PWC Does NOT Cache:
  </text>
  <text x="580" y="375" font-family="Arial, sans-serif" style="fill:#E65100; font-size:10">
    ✗ Final VA → PA translations (TLB&#39;s job)
  </text>
  <text x="580" y="393" font-family="Arial, sans-serif" style="fill:#E65100; font-size:10">
    ✗ Cross-process entries (flushed on switch)
  </text>
  <text x="580" y="411" font-family="Arial, sans-serif" style="fill:#E65100; font-size:10">
    ✗ Speculative translations
  </text>
  
  <!-- Real-World Sizes -->
  <rect x="50" y="450" width="900" height="220" style="fill:#ffffff; stroke:#1565C0; stroke-width:2" />
  <text x="500" y="480" font-family="Arial, sans-serif" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">
    Real-World Cache Sizes (Modern Processors)
  </text>
  
  <!-- Intel Skylake -->
  <text x="70" y="510" font-family="Arial, sans-serif" style="fill:#1565C0; font-size:12; font-weight:bold">
    Intel Skylake (2015):
  </text>
  <text x="90" y="530" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    L1 DTLB: 64 entries (4KB), 32 entries (2MB)
  </text>
  <text x="90" y="548" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    L2 STLB: 1536 entries → Coverage: 6 MB (4KB) or 3 GB (2MB)
  </text>
  <text x="90" y="566" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    PWC: ~32 entries per level (estimated, undocumented)
  </text>
  
  <!-- AMD Zen 3 -->
  <text x="520" y="510" font-family="Arial, sans-serif" style="fill:#9b59b6; font-size:12; font-weight:bold">
    AMD Zen 3 (2020):
  </text>
  <text x="540" y="530" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    L1 DTLB: 72 entries (4KB/2MB)
  </text>
  <text x="540" y="548" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    L2 TLB: 2048 entries → Coverage: 8 MB (4KB) or 4 GB (2MB)
  </text>
  <text x="540" y="566" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    PMC (Page Map Cache): ~32-64 entries (estimated)
  </text>
  
  <!-- ARM Cortex-A77 -->
  <text x="70" y="600" font-family="Arial, sans-serif" style="fill:#00796B; font-size:12; font-weight:bold">
    ARM Cortex-A77 (2019):
  </text>
  <text x="90" y="620" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    L1 DTLB: 48 entries (4KB), 32 entries (large)
  </text>
  <text x="90" y="638" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    L2 TLB: 1280 entries → Coverage: 5 MB (4KB)
  </text>
  <text x="90" y="656" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    Page walk cache: Integrated (details not disclosed)
  </text>
  
  <!-- Performance Impact -->
  <rect x="520" y="590" width="420" height="70" style="fill:#fff3cd; stroke:#ffc107; stroke-width:2" />
  <text x="730" y="612" font-family="Arial, sans-serif" style="fill:#856404; font-size:11; font-weight:bold; text-anchor:middle">
    Performance Impact
  </text>
  <text x="540" y="632" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    TLB hit: 0-1 cycles | TLB miss + PWC hit: 10-20 cycles
  </text>
  <text x="540" y="650" font-family="Arial, sans-serif" style="fill:#34495e; font-size:10">
    TLB miss + PWC miss: 100-250 cycles (DRAM access)
  </text>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" style="fill:#34495e"></polygon>
    </marker>
  </defs>
</svg>
  </div>
  <figcaption><strong>Figure 3.cache:</strong> TLB vs. page walk cache:
  the TLB caches complete virtual→physical translations; the page walk
  cache stores intermediate page-directory entries, short-circuiting
  multi-level walks to one or two memory accesses on a TLB
  miss.</figcaption>
  </figure>

We\'ve discussed page table walks throughout this chapter, but let\'s
consolidate our understanding of how the hardware actually implements
the translation process.

### 3.8.1 The Page Walk State Machine {#3.8.1-the-page-walk-state-machine}

The hardware page walker is a dedicated state machine in the MMU that
activates on a TLB miss. It operates concurrently with other CPU
execution units, allowing out-of-order processors to continue executing
independent instructions during the walk.

**Walk Initiation**:

1\. Instruction tries to access memory at virtual address VA

2\. TLB lookup: miss

3\. PWC lookup for upper levels: partial hits possible

4\. Hardware walker activates for remaining levels

5\. Other instructions continue (if independent of this load)

**x86-64 Four-Level Walk Algorithm**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
Input: VA (virtual address)

Output: PA (physical address) or Page Fault

1\. base = CR3\[51:12\] \<\< 12 // PML4 base address

2\. index = VA\[47:39\] // PML4 index

3\. pml4e = read(base + index × 8)

4\. if pml4e.P == 0: raise PAGE_FAULT

5\. base = pml4e\[51:12\] \<\< 12 // PDPT base

6\. index = VA\[38:30\] // PDPT index

7\. pdpte = read(base + index × 8)

8\. if pdpte.P == 0: raise PAGE_FAULT

9\. if pdpte.PS == 1: goto HUGE_1GB

10\. base = pdpte\[51:12\] \<\< 12

11\. index = VA\[29:21\]

12\. pde = read(base + index × 8)

13\. if pde.P == 0: raise PAGE_FAULT

14\. if pde.PS == 1: goto HUGE_2MB

15\. base = pde\[51:12\] \<\< 12

16\. index = VA\[20:12\]

17\. pte = read(base + index × 8)

18\. if pte.P == 0: raise PAGE_FAULT

19\. check permissions (pte.XD, pte.U/S, pte.R/W)

20\. if violation: raise PAGE_FAULT

21\. pte.A = 1 (mark accessed)

22\. if write: pte.D = 1 (mark dirty)

23\. PA = (pte\[51:12\] \<\< 12) \| VA\[11:0\]

24\. install in TLB

25\. return PA

HUGE_2MB:

PA = (pde\[51:21\] \<\< 21) \| VA\[20:0\]

goto step 24

HUGE_1GB:

PA = (pdpte\[51:30\] \<\< 30) \| VA\[29:0\]

goto step 24
:::

**Key Implementation Details**: **Speculative Execution**: Modern CPUs
may speculatively start page walks before knowing if the load/store will
actually execute (e.g., after a branch prediction). **Parallel Walks**:
Some processors can handle multiple concurrent page walks for different
addresses. **Abort Handling**: If a page fault occurs mid-walk, the CPU
must cleanly abort, save fault information (faulting address, error
code), and vector to the page fault handler. *Reference: Intel 64 and
IA-32 Architectures Software Developer\'s Manual, Volume 3A, Section
4.7: \"Page-Fault Exceptions\" describes the complete page fault
handling mechanism. Intel Corporation, 2024.*

### 3.8.2 Hardware-Managed vs Software-Managed Bits {#3.8.2-hardware-managed-vs-software-managed-bits}

Different architectures divide responsibility between hardware and
software for page table management:

**x86: Mostly Hardware-Managed**:

- Hardware sets **Accessed (A)** bit on any access
- Hardware sets **Dirty (D)** bit on writes
- Software can clear these bits but cannot prevent hardware from setting
  them

**ARM: Hybrid Approach**:

- Hardware can set **Access Flag (AF)** if configured, or generate fault
- Software typically pre-sets AF=1 to avoid faults
- Dirty tracking through software using read-only pages + COW

**RISC-V: Fully Hardware-Managed**:

- Hardware always sets **Accessed (A)** bit on access
- Hardware always sets **Dirty (D)** bit on writes
- Software can clear but not prevent setting

The hardware-managed approach simplifies OS implementation but reduces
flexibility. Some OS algorithms prefer software-managed tracking for
more precise control.

### 3.8.3 Performance Characteristics {#3.8.3-performance-characteristics}

Page walk latency depends on cache hits:

**Best case** (all levels in L1 cache):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
4 cache accesses × 4 cycles = 16 cycles

\+ TLB install: \~5 cycles

Total: \~20 cycles
:::

**Typical case** (mix of L1/L2/L3 cache):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
\~50-100 cycles
:::

**Worst case** (DRAM accesses):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
4 DRAM accesses × 100-200 cycles = 400-800 cycles
:::

This is why TLB hit rate matters so much: a 95% hit rate means only 5%
of memory accesses pay this penalty, but with random access patterns
causing frequent TLB misses, performance can degrade dramatically.

## 3.9 Page Table Management from the OS Perspective {#3.9-page-table-management-from-the-os-perspective}

While hardware handles the mechanics of translation, the operating
system is responsible for allocating, initializing, and managing page
tables. Let\'s examine key OS-level page table operations.

### 3.9.1 Process Creation and Page Table Allocation {#3.9.1-process-creation-and-page-table-allocation}

When creating a new process (e.g., `fork()` on UNIX systems):

**1. Allocate top-level table**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
c

// Allocate page directory (x86) or PML4 (x86-64)

struct page \*pgd = alloc_page(GFP_KERNEL);

pml4_t \*pml4 = page_address(pgd);

memset(pml4, 0, PAGE_SIZE); // Zero-initialize
:::

**2. Set up kernel mappings** (upper half on many systems):

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
c

// Copy kernel page table entries

// This way kernel is mapped in all processes

for (i = 256; i \< 512; i++) { // Upper half

pml4\[i\] = kernel_pml4\[i\];

}
:::

**3. Allocate user mappings on-demand**:

- Don\'t allocate page tables for entire address space

- Allocate as pages are actually mapped

- Lazy allocation saves memory

  ### 3.9.2 Copy-on-Write (COW) and Fork {#3.9.2-copy-on-write-cow-and-fork}

Traditional `fork()` would copy all memory from parent to
child---extremely expensive for large processes. COW optimizes this:

**1. Share page tables, mark pages read-only**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
c

fork() {

child-\>pml4 = alloc_page_table();

for each mapped page in parent:

// Copy PTE to child

child_pte = parent_pte;

// Mark both parent and child read-only

parent_pte.R/W = 0;

child_pte.R/W = 0;

// Increment page reference count

page_refcount++;

}
:::

**2. On write attempt, copy page**:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
c

page_fault_handler(address, error_code) {

if (error_code == WRITE_TO_READONLY) {

if (page_refcount == 1) {

// Only reference, just make writable

pte.R/W = 1;

} else {

// Multiple references, copy the page

new_page = alloc_page();

memcpy(new_page, old_page, PAGE_SIZE);

pte.pfn = new_page_number;

pte.R/W = 1;

page_refcount\--;

}

}

}
:::

COW means `fork()` is nearly instant regardless of process size!

*Reference: Appel, A. W., & Li, K. (1991). \"Virtual memory primitives
for user programs\". ACM SIGPLAN Notices, 26(4), 96-107. This paper
describes COW and other VM primitives from a programmer\'s perspective.*

### 3.9.3 Transparent Huge Pages (THP) {#3.9.3-transparent-huge-pages-thp}

Linux\'s Transparent Huge Page support automatically promotes regions of
memory to 2MB huge pages when beneficial.

**khugepaged kernel thread**:

- Scans memory regions
- Looks for contiguous 4KB pages that could be combined
- Promotes to 2MB page if:

\* 512 contiguous pages allocated

\* Memory is physically contiguous

\* No special mappings (device memory, etc.)

**Benefit**: Applications get huge page performance without explicit
huge page requests. **Trade-off**: Potential memory waste if process
doesn\'t use all 2MB. *Reference: Arcangeli, A., Eidus, I., & Wright, C.
(2011). \"Increasing memory density by using KSM\". Proceedings of the
Linux Symposium, 19-28. (Discusses THP as part of Linux memory
optimization.)*

### 3.9.4 Page Table Reclamation {#3.9.4-page-table-reclamation}

On memory pressure, the OS can reclaim page table memory for unused
regions:

::: {.technical-note style="background:#f8f9fa;border-left:3px solid #9E9E9E;padding:0.6em 1em;margin:0.8em 0;font-size:0.92em;font-family:monospace;"}
c

unmap_page_range(start, end) {

for each page table covering \[start, end\]:

if all PTEs in table are invalid:

free_page_table(pt);

mark_pde_invalid();

}
:::

This is the inverse of lazy allocation: lazily free page tables when no
longer needed.

## 3.10 Design Trade-offs {#3.10-design-trade-offs}

Having explored page table structures in depth, let\'s step back and
analyze the fundamental trade-offs that architects face.

### 3.10.1 Memory Overhead vs Translation Speed {#3.10.1-memory-overhead-vs-translation-speed}

**More levels** → Less memory overhead, slower translation:

- Each additional level multiplies address space by entries-per-table
- But adds one memory access to every TLB miss

**Fewer levels** → More memory overhead, faster translation:

- Reduces TLB miss penalty
- But wastes memory for sparse address spaces

**Quantitative Example** (4KB pages, 512 entries/table):

\| Levels \| Max Address Space \| Worst-case Overhead \| TLB Miss Cost
\|

\|\-\-\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\-\-\--\|

\| 1 \| 2GB \| 4MB per process \| 1 memory access \|

\| 2 \| 1TB \| \~4MB (sparse) \| 2 memory accesses \|

\| 3 \| 512GB \| \~16KB (sparse) \| 3 memory accesses \|

\| 4 \| 256TB \| \~32KB (sparse) \| 4 memory accesses \|

\| 5 \| 128PB \| \~40KB (sparse) \| 5 memory accesses \|

The \"sweet spot\" for most systems is 3-4 levels, balancing reasonable
overhead with manageable translation cost.

### 3.10.2 Page Size Selection {#3.10.2-page-size-selection}

**Small pages (4KB)**:

- ✅ Fine-grained protection
- ✅ Less internal fragmentation
- ❌ More TLB entries needed
- ❌ Larger page tables

**Large pages (2MB, 1GB)**:

- ✅ Better TLB coverage
- ✅ Smaller page tables
- ❌ Internal fragmentation
- ❌ Coarse-grained protection

**Real-world solution**: Support multiple page sizes, let OS/apps
choose.

### 3.10.3 Hardware vs Software Complexity {#3.10.3-hardware-vs-software-complexity}

**Hardware page walker** (x86, ARM, RISC-V):

- ✅ Fast, consistent performance
- ✅ OS doesn\'t handle TLB misses
- ❌ Fixed format, less flexible
- ❌ More complex hardware

**Software-managed TLB** (MIPS, some RISC processors):

- ✅ Flexible page table formats
- ✅ OS can optimize for workload
- ❌ TLB miss handler overhead
- ❌ Slower worst-case performance

*Reference: Rosenblum, M., et al. (1995). \"Complete computer system
simulation: The SimOS approach\". IEEE Parallel & Distributed
Technology, 3(4), 34-43. Discusses trade-offs in MMU design through
simulation.*

Modern trend: Hardware walkers win for general-purpose computing due to
better average-case performance.

### 3.10.4 Virtualization Overhead {#3.10.4-virtualization-overhead}

Two-stage translation adds:

- Potential 20-25× memory accesses (without caching)
- More page walk cache pressure
- Larger TLB to cache both stages

**Mitigations**:

- Combined TLB (cache VA → PA directly)
- Page walk caches for both stages
- Huge pages at both stages
- VPID/VMID tagging

Result: 2-7% typical overhead---acceptable for cloud computing.

## 3.11 Chapter Summary {#3.11-chapter-summary}

In this chapter, we\'ve explored page table structures from simple to
complex, always grounding our discussion in real-world implementations:

**Key Concepts**:

1\. **Single-level page tables** work for small address spaces but
don\'t scale to 64-bit systems (would require petabytes of table
memory).

2\. **Two-level page tables** solved the overhead problem for 32-bit
systems by allocating page tables only for used regions.

3\. **Multi-level page tables** (3-5 levels) are necessary for modern
64-bit systems:

\- x86-64: Four levels (48-bit) or five levels (57-bit)

\- ARM64: Flexible configurations, typically four levels

\- RISC-V: Three levels (Sv39) most common, up to five supported

4\. **Virtualization** requires two-stage translation (VA → IPA → PA):

\- Intel EPT, AMD NPT, ARM Stage 2, RISC-V G-stage

\- Could require 20+ memory accesses without caching

\- Modern hardware makes this practical through sophisticated caching

5\. **Caching is critical** for performance:

\- TLB caches final translations (VA → PA)

\- Page walk caches (PWC) cache intermediate entries

\- Combined with VPID/ASID tagging for virtualization

\- 95-99% TLB hit rates make even 5-level paging practical

6\. **Operating systems** manage page tables:

\- Lazy allocation saves memory

\- Copy-on-write optimizes fork()

\- Transparent huge pages improve performance automatically

**Design Insights**:

The convergence of x86-64, ARM64, and RISC-V on similar solutions (4-5
levels, 512 entries per table, 8-byte entries) despite different design
philosophies suggests these represent near-optimal trade-offs for modern
systems.

**Performance Implications**:

- Translation overhead: 0-200 CPU cycles depending on cache hits
- TLB hit rate is critical: 95% vs 85% can mean 2× performance
  difference
- Huge pages dramatically improve TLB coverage
- Virtualization adds 2-7% overhead with modern hardware support

**Looking Ahead**:

In the next chapters, we\'ll build on this foundation to explore:

- Advanced page table optimizations
- Huge page management and trade-offs
- Performance analysis and tuning
- Security implications of page table design

Page tables are the foundation of modern virtual memory systems.
Understanding their structure, implementation, and performance
characteristics is essential for systems programmers, architects, and
anyone working with high-performance computing or cloud infrastructure.
