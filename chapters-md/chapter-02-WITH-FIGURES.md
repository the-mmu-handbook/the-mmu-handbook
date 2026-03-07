::: {#title-block-header}
# Chapter 2: Virtual Memory Concepts {#chapter-2-virtual-memory-concepts .title}
:::

- [Chapter 2: Virtual Memory
  Concepts](#chapter-2-virtual-memory-concepts){#toc-chapter-2-virtual-memory-concepts}
  - [2.1 Introduction: The Illusion of Unlimited
    Memory](#introduction-the-illusion-of-unlimited-memory){#toc-introduction-the-illusion-of-unlimited-memory}
    - [The Core Insight](#the-core-insight){#toc-the-core-insight}
    - [What This Chapter
      Covers](#what-this-chapter-covers){#toc-what-this-chapter-covers}
  - [2.2 Demand Paging: Loading Pages on
    Demand](#demand-paging-loading-pages-on-demand){#toc-demand-paging-loading-pages-on-demand}
    - [2.2.1 The Basic
      Concept](#the-basic-concept){#toc-the-basic-concept}
    - [2.2.2 How Demand Paging
      Works](#how-demand-paging-works){#toc-how-demand-paging-works}
    - [2.2.3 Page Table Entries
      Revisited](#page-table-entries-revisited){#toc-page-table-entries-revisited}
    - [2.2.4 Types of Pages](#types-of-pages){#toc-types-of-pages}
    - [2.2.5 The Cost of Page
      Faults](#the-cost-of-page-faults){#toc-the-cost-of-page-faults}
    - [2.2.6 Optimizing Demand Paging:
      Prefetching](#optimizing-demand-paging-prefetching){#toc-optimizing-demand-paging-prefetching}
  - [2.3 Page Replacement
    Algorithms](#page-replacement-algorithms){#toc-page-replacement-algorithms}
    - [2.3.1 The Optimal Algorithm
      (Theoretical)](#the-optimal-algorithm-theoretical){#toc-the-optimal-algorithm-theoretical}
    - [2.3.2 First-In-First-Out
      (FIFO)](#first-in-first-out-fifo){#toc-first-in-first-out-fifo}
    - [2.3.3 Least Recently Used
      (LRU)](#least-recently-used-lru){#toc-least-recently-used-lru}
    - [2.3.4 Clock Algorithm (Second Chance / Not Recently
      Used)](#clock-algorithm-second-chance-not-recently-used){#toc-clock-algorithm-second-chance-not-recently-used}
    - [2.3.5 Comparison of
      Algorithms](#comparison-of-algorithms){#toc-comparison-of-algorithms}
  - [2.4 Thrashing and the Working Set
    Model](#thrashing-and-the-working-set-model){#toc-thrashing-and-the-working-set-model}
    - [2.4.1 What is
      Thrashing?](#what-is-thrashing){#toc-what-is-thrashing}
    - [2.4.2 Why Thrashing
      Occurs](#why-thrashing-occurs){#toc-why-thrashing-occurs}
    - [2.4.3 The Working Set
      Model](#the-working-set-model){#toc-the-working-set-model}
    - [2.4.4 Preventing
      Thrashing](#preventing-thrashing){#toc-preventing-thrashing}
    - [2.4.5 Detecting
      Thrashing](#detecting-thrashing){#toc-detecting-thrashing}
  - [2.5 Copy-on-Write
    (COW)](#copy-on-write-cow){#toc-copy-on-write-cow}
    - [2.5.1 The Problem COW
      Solves](#the-problem-cow-solves){#toc-the-problem-cow-solves}
    - [2.5.2 How Copy-on-Write
      Works](#how-copy-on-write-works){#toc-how-copy-on-write-works}
    - [2.5.3 Benefits of COW](#benefits-of-cow){#toc-benefits-of-cow}
    - [2.5.4 COW in Other
      Contexts](#cow-in-other-contexts){#toc-cow-in-other-contexts}
  - [2.6 Memory-Mapped
    Files](#memory-mapped-files){#toc-memory-mapped-files}
    - [2.6.1 Traditional File I/O vs. Memory
      Mapping](#traditional-file-io-vs.-memory-mapping){#toc-traditional-file-io-vs.-memory-mapping}
    - [2.6.2 How Memory Mapping
      Works](#how-memory-mapping-works){#toc-how-memory-mapping-works}
    - [2.6.3 Advantages of Memory
      Mapping](#advantages-of-memory-mapping){#toc-advantages-of-memory-mapping}
    - [2.6.4 Use Cases](#use-cases){#toc-use-cases}
  - [2.7 Advanced Topics](#advanced-topics){#toc-advanced-topics}
    - [2.7.1 Huge Pages / Large
      Pages](#huge-pages-large-pages){#toc-huge-pages-large-pages}
    - [2.7.2 Memory
      Overcommitment](#memory-overcommitment){#toc-memory-overcommitment}
    - [2.7.3 NUMA (Non-Uniform Memory
      Access)](#numa-non-uniform-memory-access){#toc-numa-non-uniform-memory-access}
  - [2.8 Performance Optimization
    Strategies](#performance-optimization-strategies){#toc-performance-optimization-strategies}
    - [2.8.1 Reduce Page
      Faults](#reduce-page-faults){#toc-reduce-page-faults}
    - [2.8.2 Monitor
      Performance](#monitor-performance){#toc-monitor-performance}
  - [2.9 Chapter Summary](#chapter-summary){#toc-chapter-summary}
  - [2.10 Looking Ahead](#looking-ahead){#toc-looking-ahead}
  - [References](#references){#toc-references}

# Chapter 2: Virtual Memory Concepts {#chapter-2-virtual-memory-concepts}

> *"Virtual memory is a powerful illusion---programs believe they have
> unlimited, contiguous memory, when in reality they're sharing limited
> physical RAM with dozens of other processes."*

## 2.1 Introduction: The Illusion of Unlimited Memory

In Chapter 1, we learned that virtual memory gives each process its own
private address space, with the MMU translating virtual addresses to
physical addresses. But we left an important question unanswered: **What
happens when a program's virtual address space is larger than the
available physical RAM?**

Consider a realistic scenario: - Your laptop has **16 GB of physical
RAM** - You're running: Chrome (50 tabs using 8 GB), IDE (3 GB),
database (4 GB), video editor (6 GB) - **Total virtual memory needed: 21
GB** - Physical RAM available: **16 GB**

How does this work? The answer is **virtual memory** in its fullest
sense---not just address translation, but the ability to transparently
use disk storage as an extension of physical RAM.

### The Core Insight

Not all of a program's virtual memory needs to be in physical RAM
simultaneously. Most programs exhibit **locality of reference**: - They
access a small subset of their code repeatedly (loops, frequently called
functions) - They work with a limited working set of data at any given
time - Large data structures are often accessed sequentially or in
predictable patterns

Virtual memory exploits this behavior through **demand
paging**---loading pages into physical RAM only when they're actually
accessed, and evicting unused pages to disk when memory is scarce.

### What This Chapter Covers

This chapter explores how operating systems implement virtual memory to
create the illusion of abundant memory:

1.  **Demand Paging:** How pages are loaded on-demand from disk
2.  **Page Replacement:** Which pages to evict when memory is full
3.  **Thrashing:** When the system spends more time paging than
    executing
4.  **Advanced Techniques:** Copy-on-Write, memory-mapped files, shared
    memory
5.  **Performance Optimization:** Reducing page faults and improving
    locality

By the end, you'll understand how your computer runs dozens of programs
simultaneously, each thinking it has gigabytes of memory, on hardware
with limited physical RAM.

------------------------------------------------------------------------

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="580" viewBox="0 0 900 580" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#212121"></polygon></marker>
    <marker id="arr-b" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="arr-t" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker>
    <marker id="arr-o" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-color="rgba(0,0,0,0.18)"></fedropshadow></filter>
  </defs>
  <rect width="900" height="580" style="fill:#fff" />

  <!-- Title -->
  <text x="30" y="36" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold">Figure 2.4 — The Virtual Memory Illusion: More Virtual Space Than Physical RAM</text>

  <!-- ===== LEFT: VIRTUAL ADDRESS SPACES ===== -->
  <rect x="30" y="52" width="490" height="490" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="30" y="52" width="490" height="34" rx="8" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="275" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Virtual Address Spaces (Each Process: up to 128 TB on x86-64)</text>

  <!-- Process A -->
  <g filter="url(#sh)">
    <rect x="55" y="100" width="130" height="200" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  </g>
  <text x="120" y="120" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Chrome</text>
  <text x="120" y="137" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">(50 tabs)</text>
  <!-- segments inside process A -->
  <rect x="62" y="148" width="116" height="22" rx="3" style="fill:#0D47A1" />
  <text x="120" y="163" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Stack</text>
  <rect x="62" y="175" width="116" height="22" rx="3" style="fill:#1976D2" />
  <text x="120" y="190" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Heap</text>
  <rect x="62" y="202" width="116" height="22" rx="3" style="fill:#42A5F5" />
  <text x="120" y="217" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Mapped Files</text>
  <rect x="62" y="229" width="116" height="22" rx="3" style="fill:#90CAF9" />
  <text x="120" y="244" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; text-anchor:middle">Code + Libs</text>
  <text x="120" y="272" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:14; font-weight:bold; text-anchor:middle">8 GB virtual</text>
  <text x="120" y="290" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">needed</text>

  <!-- Process B -->
  <g filter="url(#sh)">
    <rect x="210" y="100" width="130" height="130" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  </g>
  <text x="275" y="120" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">IDE</text>
  <rect x="217" y="132" width="116" height="22" rx="3" style="fill:#0D47A1" />
  <text x="275" y="147" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Stack</text>
  <rect x="217" y="159" width="116" height="22" rx="3" style="fill:#1976D2" />
  <text x="275" y="174" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Heap</text>
  <rect x="217" y="186" width="116" height="22" rx="3" style="fill:#42A5F5" />
  <text x="275" y="201" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Code + Libs</text>
  <text x="275" y="222" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:14; font-weight:bold; text-anchor:middle">3 GB virtual</text>

  <!-- Process C -->
  <g filter="url(#sh)">
    <rect x="365" y="100" width="130" height="160" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  </g>
  <text x="430" y="120" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Database</text>
  <rect x="372" y="132" width="116" height="22" rx="3" style="fill:#0D47A1" />
  <text x="430" y="147" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Stack</text>
  <rect x="372" y="159" width="116" height="22" rx="3" style="fill:#1976D2" />
  <text x="430" y="174" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Heap (Buffer Pool)</text>
  <rect x="372" y="186" width="116" height="22" rx="3" style="fill:#42A5F5" />
  <text x="430" y="201" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Shared Mem</text>
  <rect x="372" y="213" width="116" height="22" rx="3" style="fill:#90CAF9" />
  <text x="430" y="228" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; text-anchor:middle">Code</text>
  <text x="430" y="250" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:14; font-weight:bold; text-anchor:middle">4 GB virtual</text>

  <!-- Total virtual annotation -->
  <line x1="55" y1="315" x2="495" y2="315" style="stroke:#E65100; stroke-width:1.5; stroke-dasharray:6,3"></line>
  <text x="275" y="335" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:15; font-weight:bold; text-anchor:middle">Total virtual memory requested: ~21 GB</text>
  <text x="275" y="355" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:13; text-anchor:middle">(Each process believes it has exclusive ownership of its full address space)</text>

  <!-- Locality of reference diagram -->
  <rect x="55" y="375" width="450" height="148" rx="6" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="280" y="397" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Locality of Reference — Why This Works</text>
  <!-- Two zones: active working set and inactive -->
  <rect x="70" y="410" width="160" height="96" rx="5" style="fill:#1565C0" />
  <text x="150" y="432" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Active Working Set</text>
  <text x="150" y="452" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">~10–20% of pages</text>
  <text x="150" y="472" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">→ stays in RAM</text>
  <text x="150" y="492" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:12; text-anchor:middle">accesses: 99%+ of time</text>
  <rect x="260" y="410" width="230" height="96" rx="5" style="fill:#EEEEEE; stroke:#9E9E9E; stroke-width:1" />
  <text x="375" y="432" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:13; font-weight:bold; text-anchor:middle">Inactive / Cold Pages</text>
  <text x="375" y="452" font-family="Arial,Helvetica,sans-serif" style="fill:#9E9E9E; font-size:12; text-anchor:middle">~80–90% of virtual space</text>
  <text x="375" y="472" font-family="Arial,Helvetica,sans-serif" style="fill:#9E9E9E; font-size:12; text-anchor:middle">→ can reside on disk</text>
  <text x="375" y="492" font-family="Arial,Helvetica,sans-serif" style="fill:#9E9E9E; font-size:12; text-anchor:middle">accesses: &lt;1% of time</text>

  <!-- ===== RIGHT: PHYSICAL RAM ===== -->
  <rect x="545" y="52" width="325" height="490" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="545" y="52" width="325" height="34" rx="8" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
  <text x="707" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Physical RAM — 16 GB Available</text>

  <!-- Physical frames — only active pages fit -->
  <text x="707" y="108" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:13; font-weight:bold; text-anchor:middle">Resident Pages (hot/active only):</text>

  <!-- Chrome active pages -->
  <rect x="565" y="116" width="285" height="28" rx="4" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="707" y="134" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Chrome — active tabs (~3.2 GB in RAM)</text>
  <!-- sub frames -->
  <rect x="565" y="148" width="95" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
  <text x="612" y="163" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; text-anchor:middle">Tab renderer</text>
  <rect x="665" y="148" width="95" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
  <text x="712" y="163" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; text-anchor:middle">JS engine</text>
  <rect x="765" y="148" width="85" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
  <text x="807" y="163" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; text-anchor:middle">libc, etc.</text>

  <!-- IDE active pages -->
  <rect x="565" y="180" width="285" height="28" rx="4" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="707" y="198" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">IDE — active workspace (~1.5 GB in RAM)</text>
  <rect x="565" y="212" width="135" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
  <text x="632" y="227" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; text-anchor:middle">Open files/AST</text>
  <rect x="705" y="212" width="145" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
  <text x="777" y="227" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; text-anchor:middle">Code index cache</text>

  <!-- DB active pages -->
  <rect x="565" y="244" width="285" height="28" rx="4" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="707" y="262" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Database — hot buffer pool (~2 GB in RAM)</text>
  <rect x="565" y="276" width="285" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
  <text x="707" y="291" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; text-anchor:middle">Hot rows / indexes / shared memory segments</text>

  <!-- Free/OS/Kernel -->
  <rect x="565" y="308" width="285" height="28" rx="4" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
  <text x="707" y="326" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">OS Kernel + Page Cache (~2 GB)</text>

  <!-- Swap / disk region -->
  <rect x="565" y="346" width="285" height="180" rx="4" style="fill:#EEEEEE; stroke:#9E9E9E; stroke-width:1.5; stroke-dasharray:6,3" />
  <text x="707" y="368" font-family="Arial,Helvetica,sans-serif" style="fill:#9E9E9E; font-size:14; font-weight:bold; text-anchor:middle">Swap / Disk</text>
  <text x="707" y="390" font-family="Arial,Helvetica,sans-serif" style="fill:#9E9E9E; font-size:13; text-anchor:middle">(Cold / inactive pages evicted here)</text>
  <rect x="580" y="400" width="255" height="22" rx="3" style="fill:#F5F5F5; stroke:#BDBDBD; stroke-width:1" />
  <text x="707" y="415" font-family="Arial,Helvetica,sans-serif" style="fill:#9E9E9E; font-size:12; text-anchor:middle">Chrome: 4.8 GB cold tab data</text>
  <rect x="580" y="428" width="255" height="22" rx="3" style="fill:#F5F5F5; stroke:#BDBDBD; stroke-width:1" />
  <text x="707" y="443" font-family="Arial,Helvetica,sans-serif" style="fill:#9E9E9E; font-size:12; text-anchor:middle">IDE: 1.5 GB project index (cold)</text>
  <rect x="580" y="456" width="255" height="22" rx="3" style="fill:#F5F5F5; stroke:#BDBDBD; stroke-width:1" />
  <text x="707" y="471" font-family="Arial,Helvetica,sans-serif" style="fill:#9E9E9E; font-size:12; text-anchor:middle">DB: 2 GB cold data pages</text>
  <text x="707" y="510" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">~5 GB swapped out</text>

  <!-- Summary bar -->
  <rect x="30" y="552" width="840" height="24" rx="5" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="450" y="569" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">
    Virtual illusion: 21 GB demanded  |  16 GB physical  |  ~5 GB on swap  |  Transparent to all processes via MMU + OS
  </text>
</svg>
</div>
<figcaption><strong>Figure 2.4:</strong> The virtual memory illusion:
each process sees a private, contiguous 64-bit address space far larger
than physical RAM. The OS and MMU transparently map virtual pages to
physical frames, with inactive pages spilled to disk.</figcaption>
</figure>

## 2.2 Demand Paging: Loading Pages on Demand

### 2.2.1 The Basic Concept

**Demand paging** is the technique of loading pages into physical memory
only when they're accessed, not when the program starts \[Denning,
1970\].

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="650" viewBox="0 0 900 650" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arrow-dark" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" style="fill:#212121"></polygon>
    </marker>
    <marker id="arrow-blue" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" style="fill:#1565C0"></polygon>
    </marker>
    <marker id="arrow-orange" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" style="fill:#E65100"></polygon>
    </marker>
    <marker id="arrow-teal" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" style="fill:#00796B"></polygon>
    </marker>
    <filter id="shadow">
      <fedropshadow dx="2" dy="3" stddeviation="3" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="900" height="650" style="fill:#FFFFFF" />

  <!-- Title -->
  <text x="30" y="38" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:20; font-weight:bold">Figure 2.1 — Demand Paging: Page Fault Handling Flow</text>

  <!-- Step 1: CPU Memory Access -->
  <g id="step1" filter="url(#shadow)">
    <rect x="330" y="65" width="240" height="52" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
    <text x="450" y="87" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:16; font-weight:bold; text-anchor:middle">CPU Issues</text>
    <text x="450" y="107" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:16; text-anchor:middle">Virtual Memory Access</text>
  </g>

  <!-- Arrow down -->
  <line x1="450" y1="117" x2="450" y2="145" marker-end="url(#arrow-dark)" style="stroke:#212121; stroke-width:2"></line>

  <!-- Step 2: TLB Lookup Diamond -->
  <g id="step2">
    <polygon points="450,148 560,188 450,228 340,188" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2"></polygon>
    <text x="450" y="183" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:15; font-weight:bold; text-anchor:middle">TLB Lookup</text>
    <text x="450" y="201" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:14; text-anchor:middle">Translation cached?</text>
  </g>

  <!-- TLB Hit branch — right -->
  <line x1="560" y1="188" x2="650" y2="188" marker-end="url(#arrow-teal)" style="stroke:#00796B; stroke-width:2"></line>
  <text x="600" y="180" font-family="Arial, Helvetica, sans-serif" style="fill:#00796B; font-size:14; font-weight:bold; text-anchor:middle">HIT</text>

  <!-- TLB Hit result box -->
  <g filter="url(#shadow)">
    <rect x="650" y="162" width="200" height="52" rx="6" style="fill:#00796B; stroke:#004D40; stroke-width:2" />
    <text x="750" y="184" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">Physical Address</text>
    <text x="750" y="204" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:14; text-anchor:middle">→ Memory Access ✓</text>
  </g>
  <text x="760" y="230" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13; text-anchor:middle">~1–5 cycles</text>

  <!-- TLB Miss branch — down -->
  <line x1="450" y1="228" x2="450" y2="256" marker-end="url(#arrow-orange)" style="stroke:#E65100; stroke-width:2"></line>
  <text x="465" y="248" font-family="Arial, Helvetica, sans-serif" style="fill:#E65100; font-size:14; font-weight:bold">MISS</text>

  <!-- Step 3: Page Table Walk -->
  <g id="step3" filter="url(#shadow)">
    <rect x="330" y="258" width="240" height="52" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
    <text x="450" y="280" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:16; font-weight:bold; text-anchor:middle">Page Table Walk</text>
    <text x="450" y="300" font-family="Arial, Helvetica, sans-serif" style="fill:#BDBDBD; font-size:14; text-anchor:middle">(MMU walks PT levels)</text>
  </g>

  <!-- Arrow down -->
  <line x1="450" y1="310" x2="450" y2="338" marker-end="url(#arrow-dark)" style="stroke:#212121; stroke-width:2"></line>

  <!-- Step 4: Page Present Diamond -->
  <g id="step4">
    <polygon points="450,341 560,381 450,421 340,381" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2"></polygon>
    <text x="450" y="376" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:15; font-weight:bold; text-anchor:middle">Page Present</text>
    <text x="450" y="394" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:14; text-anchor:middle">in Physical RAM?</text>
  </g>

  <!-- Present YES — right -->
  <line x1="560" y1="381" x2="650" y2="381" marker-end="url(#arrow-teal)" style="stroke:#00796B; stroke-width:2"></line>
  <text x="602" y="373" font-family="Arial, Helvetica, sans-serif" style="fill:#00796B; font-size:14; font-weight:bold">YES</text>
  <g filter="url(#shadow)">
    <rect x="650" y="355" width="200" height="52" rx="6" style="fill:#00796B; stroke:#004D40; stroke-width:2" />
    <text x="750" y="377" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">Update TLB</text>
    <text x="750" y="397" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:14; text-anchor:middle">→ Retry Access ✓</text>
  </g>
  <text x="755" y="422" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13; text-anchor:middle">~100–300 cycles</text>

  <!-- Present NO — down (PAGE FAULT) -->
  <line x1="450" y1="421" x2="450" y2="449" marker-end="url(#arrow-orange)" style="stroke:#E65100; stroke-width:2"></line>
  <text x="468" y="440" font-family="Arial, Helvetica, sans-serif" style="fill:#E65100; font-size:14; font-weight:bold">NO — PAGE FAULT</text>

  <!-- PAGE FAULT REGION background -->
  <rect x="50" y="452" width="800" height="170" rx="8" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5; stroke-dasharray:6,3" />
  <text x="70" y="475" font-family="Arial, Helvetica, sans-serif" style="fill:#E65100; font-size:14; font-weight:bold">OS Page Fault Handler</text>

  <!-- Step 5: Save context -->
  <g filter="url(#shadow)">
    <rect x="70" y="482" width="160" height="52" rx="6" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
    <text x="150" y="504" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">① Save CPU</text>
    <text x="150" y="522" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:14; text-anchor:middle">Context / Registers</text>
  </g>

  <line x1="230" y1="508" x2="258" y2="508" marker-end="url(#arrow-dark)" style="stroke:#212121; stroke-width:2"></line>

  <!-- Step 6: Select victim page -->
  <g filter="url(#shadow)">
    <rect x="260" y="482" width="160" height="52" rx="6" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
    <text x="340" y="504" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">② Select Victim</text>
    <text x="340" y="522" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:14; text-anchor:middle">Page (if mem full)</text>
  </g>

  <line x1="420" y1="508" x2="448" y2="508" marker-end="url(#arrow-dark)" style="stroke:#212121; stroke-width:2"></line>

  <!-- Step 7: Load page from disk -->
  <g filter="url(#shadow)">
    <rect x="450" y="482" width="160" height="52" rx="6" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
    <text x="530" y="504" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">③ Load Page</text>
    <text x="530" y="522" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:14; text-anchor:middle">from Disk/Swap</text>
  </g>

  <line x1="610" y1="508" x2="638" y2="508" marker-end="url(#arrow-dark)" style="stroke:#212121; stroke-width:2"></line>

  <!-- Step 8: Update PT and resume -->
  <g filter="url(#shadow)">
    <rect x="640" y="482" width="175" height="52" rx="6" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
    <text x="727" y="504" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">④ Update PT &amp; TLB</text>
    <text x="727" y="522" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:14; text-anchor:middle">→ Resume Process</text>
  </g>

  <!-- Disk I/O cost callout -->
  <text x="450" y="565" font-family="Arial, Helvetica, sans-serif" style="fill:#BF360C; font-size:14; font-weight:bold; text-anchor:middle">Disk I/O: ~5–10 million cycles  |  SSD: ~100K–1M cycles</text>

  <!-- Legend -->
  <rect x="50" y="610" width="14" height="14" rx="2" style="fill:#1565C0" />
  <text x="70" y="622" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:13">CPU / MMU Hardware</text>
  <rect x="240" y="610" width="14" height="14" rx="2" style="fill:#00796B" />
  <text x="260" y="622" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:13">Fast Path (TLB Hit / PT Hit)</text>
  <rect x="460" y="610" width="14" height="14" rx="2" style="fill:#E65100" />
  <text x="480" y="622" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:13">OS Handler — Slow Path (Page Fault)</text>
</svg>
</div>
<figcaption><strong>Figure 2.1:</strong> Demand paging page fault
handling flow: TLB hit returns physical address in 1–5 cycles; TLB miss
triggers a page table walk; if the page is absent, the OS page fault
handler loads it from disk/swap, costing millions of
cycles.</figcaption>
</figure>

### 2.2.2 How Demand Paging Works

**Step-by-Step Process:**

1.  **Program Starts**

    - OS creates page table entries for the entire virtual address space
    - All pages marked as "not present" (Present bit = 0)
    - No physical memory allocated yet

2.  **First Instruction Fetch**

    - CPU tries to fetch instruction from virtual address 0x1000
    - MMU looks up page table entry
    - Present bit = 0 â†' **Page Fault Exception**

3.  **Page Fault Handler (OS)**

        1. Save CPU state (registers, program counter)
        2. Check if address is valid (within process's virtual address space)
        3. If invalid â†’ Segmentation fault (kill process)
        4. If valid:
           a. Find a free physical frame (or evict a page)
           b. Load page from disk into that frame
           c. Update page table: frame number, Present=1
        5. Restore CPU state
        6. Return from exception
        7. CPU retries the instruction (now succeeds)

4.  **Execution Continues**

    - Instruction executes successfully
    - Program continues until accessing another non-present page
    - Process repeats

### 2.2.3 Page Table Entries Revisited

Page table entries must distinguish between three states:

**State 1: Present in Memory**

    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚  Frame  â”‚ P â”‚ D â”‚ A â”‚ R â”‚ W â”‚ X â”‚ U â”‚    (unused)       â”‚
    â”‚ Number  â”‚ 1 â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â”‚                   â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
    P=1: Page is in physical memory at specified frame

**State 2: Swapped to Disk**

    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚    Disk Block Number        â”‚ P â”‚     (disk metadata)      â”‚
    â”‚   (where page is stored)    â”‚ 0 â”‚                          â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
    P=0: Page is on disk, not in memory

**State 3: Never Allocated**

    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚                    All zeros                             â”‚
    â”‚             (or special bit pattern)                     â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
    Valid=0 in some architectures: Page has never been used

### 2.2.4 Types of Pages

Different types of memory pages behave differently with demand paging:

**Code Pages (Text Segment):** - Loaded from executable file on disk -
Read-only, never modified - Can be discarded (not swapped) since
original is on disk - Shared between multiple instances of same program

**Data Pages (Initialized Data):** - Loaded from executable file - Can
be modified (writable) - If modified, must be swapped to disk when
evicted - Private to each process

**BSS Pages (Uninitialized Data):** - Not stored in executable file -
Allocated on first access - Filled with zeros (zero page) - No disk I/O
needed initially

**Stack Pages:** - Allocated on demand as stack grows - Filled with
zeros - Can be swapped when inactive

**Heap Pages:** - Allocated by malloc() / mmap() - Initially filled with
zeros (for security) - Can be swapped when inactive

**Anonymous Pages:** - Not backed by any file - Created by
mmap(MAP_ANONYMOUS) - Must be swapped to disk if evicted

### 2.2.5 The Cost of Page Faults

Page faults are expensive. Let's quantify the cost:

    Operation                          Latency
    â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    L1 Cache hit                       ~1 ns
    DRAM access                        ~70 ns
    Page fault (page in memory cache)  ~1 Î¼s
    Page fault (from SSD)              ~100 Î¼s
    Page fault (from HDD)              ~10,000 Î¼s (10 ms)
    â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

**Example: Processing 1 million array elements**

``` {.sourceCode .c}
// Array: 4 MB (1 million Ã— 4 bytes)
// Page size: 4 KB
// Pages needed: 1,000

int sum = 0;
for (int i = 0; i < 1000000; i++) {
    sum += array[i];
}
```

**Scenario 1: All pages in memory (no page faults)** - Memory accesses:
1,000,000 - Time: 1,000,000 Ã--- 70 ns = 70 ms

**Scenario 2: All pages on SSD (1,000 page faults)** - Page faults:
1,000 Ã--- 100 Î¼s = 100 ms - Memory accesses: 1,000,000 Ã--- 70 ns = 70
ms - **Total: 170 ms (2.4Ã--- slower)**

**Scenario 3: All pages on HDD (1,000 page faults)** - Page faults:
1,000 Ã--- 10 ms = **10,000 ms (10 seconds!)** - Memory accesses: 70
ms - **Total: \~10 seconds (140Ã--- slower)**

**Lesson:** Page faults to disk are catastrophically expensive.
Minimizing page faults is critical for performance.

### 2.2.6 Optimizing Demand Paging: Prefetching

Operating systems use **prefetching** to reduce page faults by
predicting which pages will be needed:

**Sequential Prefetching:**

    Process accesses page N
      â†“
    OS predicts pages N+1, N+2, N+3 will be needed soon
      â†“
    Load N+1, N+2, N+3 in background (before they're accessed)
      â†“
    When process accesses N+1 â†’ Already in memory (no fault)

**Effectiveness:** - Works great for sequential access patterns (file
reading, array traversal) - Wasted effort for random access patterns -
Modern OSes detect access patterns and adapt

**Linux readahead:**

``` {.sourceCode .bash}
# Check current readahead setting (in KB)
blockdev --getra /dev/sda
# Output: 256 (means 256 KB prefetched)

# Increase readahead for better sequential performance
blockdev --setra 512 /dev/sda
```

------------------------------------------------------------------------

## 2.3 Page Replacement Algorithms

When physical memory is full and a page fault occurs, the OS must choose
which page to **evict** (remove from memory) to make room for the new
page. This is the **page replacement problem** \[Belady, 1966\].

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="650" viewBox="0 0 900 650" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arrow-dark" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" style="fill:#212121"></polygon>
    </marker>
    <filter id="shadow">
      <fedropshadow dx="2" dy="3" stddeviation="3" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
  </defs>

  <rect width="900" height="650" style="fill:#FFFFFF" />

  <!-- Title -->
  <text x="30" y="38" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:20; font-weight:bold">Figure 2.2 — Page Replacement Algorithms: FIFO, LRU, and Clock (Second Chance)</text>
  <text x="30" y="60" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:14">Reference string: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5   |   3 page frames available</text>

  <!-- Reference String Header Row -->
  <text x="30" y="100" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Access:</text>
  <!-- Cells for reference string -->
  <!-- x positions: 120, 185, 250, 315, 380, 445, 510, 575, 640, 705, 770, 835 -->
  <!-- Values: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 -->
  <g font-family="Arial, Helvetica, sans-serif" style="font-size:15; font-weight:bold; text-anchor:middle">
    <rect x="107" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="132" y="101" style="fill:#212121">1</text>
    <rect x="172" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="197" y="101" style="fill:#212121">2</text>
    <rect x="237" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="262" y="101" style="fill:#212121">3</text>
    <rect x="302" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="327" y="101" style="fill:#212121">4</text>
    <rect x="367" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="392" y="101" style="fill:#212121">1</text>
    <rect x="432" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="457" y="101" style="fill:#212121">2</text>
    <rect x="497" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="522" y="101" style="fill:#212121">5</text>
    <rect x="562" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="587" y="101" style="fill:#212121">1</text>
    <rect x="627" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="652" y="101" style="fill:#212121">2</text>
    <rect x="692" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="717" y="101" style="fill:#212121">3</text>
    <rect x="757" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="782" y="101" style="fill:#212121">4</text>
    <rect x="822" y="82" width="50" height="28" rx="4" style="fill:#E3F2FD; stroke:#9E9E9E; stroke-width:1" />
    <text x="847" y="101" style="fill:#212121">5</text>
  </g>

  <!-- ===== FIFO SECTION ===== -->
  <rect x="50" y="118" width="830" height="155" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="70" y="140" font-family="Arial, Helvetica, sans-serif" style="fill:#1565C0; font-size:16; font-weight:bold">FIFO (First-In First-Out)  — 9 page faults</text>
  <!-- FIFO explanation -->
  <text x="70" y="158" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13">Evicts the oldest loaded page. Simple but ignores recency of use.</text>

  <!-- FIFO Frame rows -->
  <!-- Frame row labels -->
  <text x="70" y="185" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Frame 0:</text>
  <text x="70" y="210" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Frame 1:</text>
  <text x="70" y="235" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Frame 2:</text>
  <text x="70" y="260" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Fault?</text>

  <!-- FIFO data: ref: 1,2,3,4,1,2,5,1,2,3,4,5 — frames: 3 -->
  <!-- Step 1: ref=1 → [1,-,-] FAULT -->
  <!-- Step 2: ref=2 → [1,2,-] FAULT -->
  <!-- Step 3: ref=3 → [1,2,3] FAULT -->
  <!-- Step 4: ref=4 → [4,2,3] FAULT (evict 1, oldest) -->
  <!-- Step 5: ref=1 → [4,1,3] FAULT (evict 2) -->
  <!-- Step 6: ref=2 → [4,1,2] FAULT (evict 3) -->
  <!-- Step 7: ref=5 → [5,1,2] FAULT (evict 4) -->
  <!-- Step 8: ref=1 → [5,1,2] HIT -->
  <!-- Step 9: ref=2 → [5,1,2] HIT -->
  <!-- Step 10: ref=3 → [5,3,2] FAULT (evict 1) -->
  <!-- Step 11: ref=4 → [5,3,4] FAULT (evict 2) -->
  <!-- Step 12: ref=5 → [5,3,4] HIT -->

  <!-- FIFO grid cells -->
  <g font-family="Arial, Helvetica, sans-serif" style="font-size:14; text-anchor:middle">
    <!-- Access 1: fault, 1 loaded into frame0 -->
    <rect x="107" y="170" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="132" y="186" style="fill:#212121">1</text>
    <rect x="107" y="196" width="50" height="22" rx="3" style="fill:#EEEEEE; stroke:#9E9E9E; stroke-width:1" />
    <text x="132" y="212" style="fill:#9E9E9E">-</text>
    <rect x="107" y="222" width="50" height="22" rx="3" style="fill:#EEEEEE; stroke:#9E9E9E; stroke-width:1" />
    <text x="132" y="238" style="fill:#9E9E9E">-</text>
    <text x="132" y="260" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- Access 2: fault, 2 into frame1 -->
    <rect x="172" y="170" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="197" y="186" style="fill:#212121">1</text>
    <rect x="172" y="196" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="197" y="212" style="fill:#212121">2</text>
    <rect x="172" y="222" width="50" height="22" rx="3" style="fill:#EEEEEE; stroke:#9E9E9E; stroke-width:1" />
    <text x="197" y="238" style="fill:#9E9E9E">-</text>
    <text x="197" y="260" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- Access 3: fault, 3 into frame2 -->
    <rect x="237" y="170" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="262" y="186" style="fill:#212121">1</text>
    <rect x="237" y="196" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="262" y="212" style="fill:#212121">2</text>
    <rect x="237" y="222" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="262" y="238" style="fill:#212121">3</text>
    <text x="262" y="260" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- Access 4: fault, evict 1 (oldest), load 4 into frame0 -->
    <rect x="302" y="170" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="327" y="186" style="fill:#212121">4</text>
    <rect x="302" y="196" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="327" y="212" style="fill:#212121">2</text>
    <rect x="302" y="222" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="327" y="238" style="fill:#212121">3</text>
    <text x="327" y="260" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- Access 5: ref=1, fault, evict 2, load 1 into frame1 -->
    <rect x="367" y="170" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="392" y="186" style="fill:#212121">4</text>
    <rect x="367" y="196" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="392" y="212" style="fill:#212121">1</text>
    <rect x="367" y="222" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="392" y="238" style="fill:#212121">3</text>
    <text x="392" y="260" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- Access 6: ref=2, fault, evict 3, load 2 into frame2 -->
    <rect x="432" y="170" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="457" y="186" style="fill:#212121">4</text>
    <rect x="432" y="196" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="457" y="212" style="fill:#212121">1</text>
    <rect x="432" y="222" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="457" y="238" style="fill:#212121">2</text>
    <text x="457" y="260" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- Access 7: ref=5, fault, evict 4, load 5 into frame0 -->
    <rect x="497" y="170" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="522" y="186" style="fill:#212121">5</text>
    <rect x="497" y="196" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="522" y="212" style="fill:#212121">1</text>
    <rect x="497" y="222" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="522" y="238" style="fill:#212121">2</text>
    <text x="522" y="260" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- Access 8: ref=1, HIT -->
    <rect x="562" y="170" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="587" y="186" style="fill:#212121">5</text>
    <rect x="562" y="196" width="50" height="22" rx="3" style="fill:#C8E6C9; stroke:#00796B; stroke-width:2" />
    <text x="587" y="212" style="fill:#212121">1</text>
    <rect x="562" y="222" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="587" y="238" style="fill:#212121">2</text>
    <text x="587" y="260" style="fill:#00796B; font-weight:bold">✓</text>

    <!-- Access 9: ref=2, HIT -->
    <rect x="627" y="170" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="652" y="186" style="fill:#212121">5</text>
    <rect x="627" y="196" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="652" y="212" style="fill:#212121">1</text>
    <rect x="627" y="222" width="50" height="22" rx="3" style="fill:#C8E6C9; stroke:#00796B; stroke-width:2" />
    <text x="652" y="238" style="fill:#212121">2</text>
    <text x="652" y="260" style="fill:#00796B; font-weight:bold">✓</text>

    <!-- Access 10: ref=3, fault, evict 5, load 3 -->
    <rect x="692" y="170" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="717" y="186" style="fill:#212121">3</text>
    <rect x="692" y="196" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="717" y="212" style="fill:#212121">1</text>
    <rect x="692" y="222" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="717" y="238" style="fill:#212121">2</text>
    <text x="717" y="260" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- Access 11: ref=4, fault, evict 1, load 4 -->
    <rect x="757" y="170" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="782" y="186" style="fill:#212121">3</text>
    <rect x="757" y="196" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="782" y="212" style="fill:#212121">4</text>
    <rect x="757" y="222" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="782" y="238" style="fill:#212121">2</text>
    <text x="782" y="260" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- Access 12: ref=5, fault, evict 2, load 5 -->
    <rect x="822" y="170" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="847" y="186" style="fill:#212121">3</text>
    <rect x="822" y="196" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="847" y="212" style="fill:#212121">4</text>
    <rect x="822" y="222" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="847" y="238" style="fill:#212121">5</text>
    <text x="847" y="260" style="fill:#E65100; font-weight:bold">✕</text>
  </g>

  <!-- ===== LRU SECTION ===== -->
  <rect x="50" y="282" width="830" height="155" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="70" y="304" font-family="Arial, Helvetica, sans-serif" style="fill:#1565C0; font-size:16; font-weight:bold">LRU (Least Recently Used)  — 8 page faults</text>
  <text x="70" y="322" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13">Evicts the page not used for the longest time. Near-optimal but costly to implement precisely.</text>

  <text x="70" y="349" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Frame 0:</text>
  <text x="70" y="374" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Frame 1:</text>
  <text x="70" y="399" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Frame 2:</text>
  <text x="70" y="424" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Fault?</text>

  <!-- LRU: 1→F, 2→F, 3→F, 4→F(evict1), 1→F(evict2), 2→F(evict3), 5→F(evict4), 1→H, 2→H, 3→F(evict5), 4→F(evict1), 5→F(evict2) = 8 faults -->
  <g font-family="Arial, Helvetica, sans-serif" style="font-size:14; text-anchor:middle">
    <!-- 1: fault [1,-,-] -->
    <rect x="107" y="334" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="132" y="350" style="fill:#212121">1</text>
    <rect x="107" y="358" width="50" height="22" rx="3" style="fill:#EEEEEE; stroke:#9E9E9E; stroke-width:1" />
    <text x="132" y="374" style="fill:#9E9E9E">-</text>
    <rect x="107" y="382" width="50" height="22" rx="3" style="fill:#EEEEEE; stroke:#9E9E9E; stroke-width:1" />
    <text x="132" y="398" style="fill:#9E9E9E">-</text>
    <text x="132" y="424" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- 2: fault [1,2,-] -->
    <rect x="172" y="334" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="197" y="350" style="fill:#212121">1</text>
    <rect x="172" y="358" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="197" y="374" style="fill:#212121">2</text>
    <rect x="172" y="382" width="50" height="22" rx="3" style="fill:#EEEEEE; stroke:#9E9E9E; stroke-width:1" />
    <text x="197" y="398" style="fill:#9E9E9E">-</text>
    <text x="197" y="424" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- 3: fault [1,2,3] -->
    <rect x="237" y="334" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="262" y="350" style="fill:#212121">1</text>
    <rect x="237" y="358" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="262" y="374" style="fill:#212121">2</text>
    <rect x="237" y="382" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="262" y="398" style="fill:#212121">3</text>
    <text x="262" y="424" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- 4: fault, LRU=1 evicted [4,2,3] -->
    <rect x="302" y="334" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="327" y="350" style="fill:#212121">4</text>
    <rect x="302" y="358" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="327" y="374" style="fill:#212121">2</text>
    <rect x="302" y="382" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="327" y="398" style="fill:#212121">3</text>
    <text x="327" y="424" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- 1: fault, LRU=2 evicted [4,1,3] -->
    <rect x="367" y="334" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="392" y="350" style="fill:#212121">4</text>
    <rect x="367" y="358" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="392" y="374" style="fill:#212121">1</text>
    <rect x="367" y="382" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="392" y="398" style="fill:#212121">3</text>
    <text x="392" y="424" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- 2: fault, LRU=3 evicted [4,1,2] -->
    <rect x="432" y="334" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="457" y="350" style="fill:#212121">4</text>
    <rect x="432" y="358" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="457" y="374" style="fill:#212121">1</text>
    <rect x="432" y="382" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="457" y="398" style="fill:#212121">2</text>
    <text x="457" y="424" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- 5: fault, LRU=4 evicted [5,1,2] -->
    <rect x="497" y="334" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="522" y="350" style="fill:#212121">5</text>
    <rect x="497" y="358" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="522" y="374" style="fill:#212121">1</text>
    <rect x="497" y="382" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="522" y="398" style="fill:#212121">2</text>
    <text x="522" y="424" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- 1: HIT [5,1,2] -->
    <rect x="562" y="334" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="587" y="350" style="fill:#212121">5</text>
    <rect x="562" y="358" width="50" height="22" rx="3" style="fill:#C8E6C9; stroke:#00796B; stroke-width:2" />
    <text x="587" y="374" style="fill:#212121">1</text>
    <rect x="562" y="382" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="587" y="398" style="fill:#212121">2</text>
    <text x="587" y="424" style="fill:#00796B; font-weight:bold">✓</text>

    <!-- 2: HIT [5,1,2] -->
    <rect x="627" y="334" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="652" y="350" style="fill:#212121">5</text>
    <rect x="627" y="358" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="652" y="374" style="fill:#212121">1</text>
    <rect x="627" y="382" width="50" height="22" rx="3" style="fill:#C8E6C9; stroke:#00796B; stroke-width:2" />
    <text x="652" y="398" style="fill:#212121">2</text>
    <text x="652" y="424" style="fill:#00796B; font-weight:bold">✓</text>

    <!-- 3: fault, LRU=5 evicted [3,1,2] -->
    <rect x="692" y="334" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="717" y="350" style="fill:#212121">3</text>
    <rect x="692" y="358" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="717" y="374" style="fill:#212121">1</text>
    <rect x="692" y="382" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="717" y="398" style="fill:#212121">2</text>
    <text x="717" y="424" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- 4: fault, LRU=1 evicted [3,4,2] -->
    <rect x="757" y="334" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="782" y="350" style="fill:#212121">3</text>
    <rect x="757" y="358" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="782" y="374" style="fill:#212121">4</text>
    <rect x="757" y="382" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="782" y="398" style="fill:#212121">2</text>
    <text x="782" y="424" style="fill:#E65100; font-weight:bold">✕</text>

    <!-- 5: fault, LRU=2 evicted [3,4,5] -->
    <rect x="822" y="334" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="847" y="350" style="fill:#212121">3</text>
    <rect x="822" y="358" width="50" height="22" rx="3" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
    <text x="847" y="374" style="fill:#212121">4</text>
    <rect x="822" y="382" width="50" height="22" rx="3" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
    <text x="847" y="398" style="fill:#212121">5</text>
    <text x="847" y="424" style="fill:#E65100; font-weight:bold">✕</text>
  </g>

  <!-- ===== CLOCK ALGORITHM SECTION ===== -->
  <rect x="50" y="448" width="830" height="155" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="70" y="470" font-family="Arial, Helvetica, sans-serif" style="fill:#1565C0; font-size:16; font-weight:bold">Clock / Second-Chance Algorithm  — 8 page faults (practical LRU approximation)</text>
  <text x="70" y="488" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13">Reference bit R set on access. On fault, scan clock: R=1 → clear R, advance; R=0 → evict. O(1) overhead.</text>

  <!-- Clock diagram showing circular structure with 3 frames -->
  <!-- Draw the clock circle conceptually with 3 positions -->
  <g id="clock-diagram" transform="translate(180, 560)">
    <!-- Clock circle background -->
    <circle cx="0" cy="0" r="55" style="fill:none; stroke:#9E9E9E; stroke-width:1.5; stroke-dasharray:4,3"></circle>

    <!-- Frame positions on circle: top(0,-55), bottom-left(-48,28), bottom-right(48,28) -->
    <!-- Frame 0 top -->
    <rect x="-28" y="-67" width="56" height="26" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
    <text x="0" y="-49" font-family="Arial, Helvetica, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">P:1 R=1</text>

    <!-- Frame 1 bottom-left -->
    <rect x="-76" y="16" width="56" height="26" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
    <text x="-48" y="34" font-family="Arial, Helvetica, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">P:2 R=0</text>

    <!-- Frame 2 bottom-right -->
    <rect x="20" y="16" width="56" height="26" rx="5" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
    <text x="48" y="34" font-family="Arial, Helvetica, sans-serif" style="fill:white; font-size:13; font-weight:bold; text-anchor:middle">P:3 R=0</text>

    <!-- Clock hand arrow pointing to frame2 (evict candidate) -->
    <line x1="0" y1="0" x2="40" y2="22" marker-end="url(#arrow-orange)" style="stroke:#E65100; stroke-width:2.5"></line>
    <text x="2" y="4" font-family="Arial, Helvetica, sans-serif" style="fill:#E65100; font-size:12; font-weight:bold">clock</text>
    <text x="2" y="17" font-family="Arial, Helvetica, sans-serif" style="fill:#E65100; font-size:12; font-weight:bold">hand</text>
  </g>

  <!-- Clock explanation text -->
  <text x="330" y="490" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Algorithm on page fault:</text>
  <text x="330" y="512" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14">① Check frame at clock hand</text>
  <text x="330" y="533" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14">② If R=1: clear R bit → advance hand (second chance)</text>
  <text x="330" y="554" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14">③ If R=0: evict this page → load new page here</text>
  <text x="330" y="575" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14">④ Set R=1 on newly loaded page → advance hand</text>
  <text x="330" y="596" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13">Linux uses a variant with active/inactive page lists (clock-pro)</text>

  <!-- Summary bar -->
  <rect x="50" y="614" width="830" height="28" rx="5" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="450" y="633" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">
    Fault comparison (3 frames, 12 accesses):  FIFO = 9 faults  |  LRU = 8 faults  |  Clock ≈ 8 faults  |  Optimal = 6 faults (theoretical minimum)
  </text>
</svg>
</div>
<figcaption><strong>Figure 2.2:</strong> Page replacement algorithms:
FIFO evicts the oldest page (simple but can evict frequently used
pages); LRU evicts the least recently used page (near-optimal, exploits
temporal locality); Clock/Second-Chance approximates LRU using a
reference bit and circular scan.</figcaption>
</figure>

### 2.3.1 The Optimal Algorithm (Theoretical)

**Belady's Optimal Algorithm (OPT):** Evict the page that will be used
furthest in the future.

**Example:**

    Reference string: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5
    Physical frames: 3

    Time:  1  2  3  4  1  2  5  1  2  3  4  5
         â”Œâ”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”
      F1 â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚
         â”œâ”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¤
      F2 â”‚  â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 4â”‚ 4â”‚
         â”œâ”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¤
      F3 â”‚  â”‚  â”‚ 3â”‚ 4â”‚ 4â”‚ 4â”‚ 5â”‚ 5â”‚ 5â”‚ 3â”‚ 3â”‚ 5â”‚
         â””â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”˜
    Faults: F  F  F  F        F           F  F

    Page faults: 7

**Why it's optimal:** At each eviction, it chooses the page that won't
be needed for the longest time, minimizing future faults.

**Why it's impractical:** Requires knowledge of future memory
references---impossible in real systems.

**Value:** Provides a theoretical lower bound for comparison. Any
practical algorithm will have â‰¥ OPT page faults.

### 2.3.2 First-In-First-Out (FIFO)

**Algorithm:** Evict the page that has been in memory the longest.

**Implementation:**

``` {.sourceCode .c}
// Simple queue of page frames
struct page_queue {
    int frames[NUM_FRAMES];
    int front, rear;
};

int fifo_replace(struct page_queue *q) {
    int victim = q->frames[q->front];
    q->front = (q->front + 1) % NUM_FRAMES;
    return victim;
}
```

**Example (same reference string):**

    Reference string: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5
    Physical frames: 3

    Time:  1  2  3  4  1  2  5  1  2  3  4  5
         â”Œâ”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”
      F1 â”‚ 1â”‚ 1â”‚ 1â”‚ 4â”‚ 4â”‚ 4â”‚ 4â”‚ 4â”‚ 4â”‚ 3â”‚ 3â”‚ 3â”‚
         â”œâ”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¤
      F2 â”‚  â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 5â”‚ 5â”‚ 5â”‚ 5â”‚ 4â”‚ 4â”‚
         â”œâ”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¤
      F3 â”‚  â”‚  â”‚ 3â”‚ 3â”‚ 3â”‚ 3â”‚ 3â”‚ 3â”‚ 3â”‚ 3â”‚ 3â”‚ 5â”‚
         â””â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”˜
    Faults: F  F  F  F        F           F  F

    Page faults: 10

**Advantages:** - Simple to implement - Fair (all pages treated
equally) - Low overhead

**Disadvantages:** - Doesn't consider page usage patterns - Can evict
frequently used pages - Suffers from Belady's Anomaly (more frames â†'
more faults in some cases)

**Belady's Anomaly Example:**

    Reference string: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5

    With 3 frames: 9 page faults
    With 4 frames: 10 page faults (!)

    More memory â†’ worse performance (rare but possible with FIFO)

### 2.3.3 Least Recently Used (LRU)

**Algorithm:** Evict the page that hasn't been used for the longest
time.

**Rationale:** If a page hasn't been used recently, it's less likely to
be used soon (temporal locality).

**Example (same reference string):**

    Reference string: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5
    Physical frames: 3

    Time:  1  2  3  4  1  2  5  1  2  3  4  5
         â”Œâ”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”¬â”€â”€â”
      F1 â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 1â”‚ 5â”‚
         â”œâ”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¤
      F2 â”‚  â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 2â”‚ 4â”‚ 4â”‚
         â”œâ”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¼â”€â”€â”¤
      F3 â”‚  â”‚  â”‚ 3â”‚ 4â”‚ 4â”‚ 4â”‚ 5â”‚ 5â”‚ 5â”‚ 3â”‚ 3â”‚ 3â”‚
         â””â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”´â”€â”€â”˜
    Faults: F  F  F  F        F           F  F

    Page faults: 8 (better than FIFO!)

**Perfect LRU Implementation (Impractical):**

``` {.sourceCode .c}
// Timestamp every memory reference
struct page {
    int frame_number;
    timestamp_t last_access;  // Updated on EVERY access
};

int lru_replace() {
    timestamp_t oldest = MAX_TIME;
    int victim = -1;
    
    for (int i = 0; i < num_frames; i++) {
        if (pages[i].last_access < oldest) {
            oldest = pages[i].last_access;
            victim = i;
        }
    }
    return victim;
}
```

**Problem:** Updating timestamps on every memory access is impossibly
expensive (billions of updates per second).

**Hardware Support (x86 Accessed Bit):** - Page table entries have an
"Accessed" (A) bit - MMU sets A=1 automatically when page is accessed -
OS can read and clear the A bit periodically - Provides approximation of
recency without timestamps

**Advantages:** - Excellent performance (close to OPT) - Adapts to
program behavior - No Belady's Anomaly

**Disadvantages:** - Expensive to implement perfectly - Requires
hardware support (Accessed bit)

### 2.3.4 Clock Algorithm (Second Chance / Not Recently Used)

**Algorithm:** Approximation of LRU using the hardware Accessed bit.

**Implementation:**

    1. Organize pages in a circular list (like a clock)
    2. Keep a "hand" pointer pointing to next candidate
    3. When eviction needed:
       a. Check page at hand position
       b. If Accessed bit = 0 â†’ Evict this page
       c. If Accessed bit = 1 â†’ Set to 0, move hand forward
       d. Repeat until finding page with Accessed = 0

**Visual Representation:**

            Page 0
             (A=1)
        â†—            â†–
    Page 7          Page 1
    (A=0)            (A=1)
       â†‘    Hand â†’   â†“
    Page 6          Page 2
    (A=1)            (A=0)
        â†–            â†—
            Page 3
             (A=1)
            
    Clock hand points to Page 0
    Need to evict a page:
      - Page 0: A=1 â†’ Set A=0, advance
      - Page 1: A=1 â†’ Set A=0, advance
      - Page 2: A=0 â†’ EVICT Page 2

**Advantages:** - Simple to implement - Low overhead - Good
approximation of LRU - Used in many real systems (Linux, BSD)

**Disadvantages:** - Not as good as perfect LRU - May scan many pages
before finding victim

**Linux Implementation (Simplified):**

``` {.sourceCode .c}
// Linux uses two lists: active and inactive
struct lru_list {
    struct list_head active_list;
    struct list_head inactive_list;
};

// Pages move between lists based on Accessed bit
void age_pages() {
    for each page in active_list {
        if (page->accessed == 0)
            move_to_inactive_list(page);
        page->accessed = 0;  // Clear for next period
    }
}
```

### 2.3.5 Comparison of Algorithms

**Performance on typical workloads:**

  -------------------------------------------------------------------------
  Algorithm   Page Faults          Implementation          Used in

|  | (relative) | Complexity | Practice? |
| --- | --- | --- | --- |
| Optimal | 1.0Ã--- (best | Impossible (needs | No (theoretical) |
| (OPT) | possible) | future knowledge) |  |
| LRU | \~1.1Ã--- | High (expensive to track) | No (too expensive) |
| Clock (NRU) | \~1.3Ã--- | Low (uses Accessed bit) | Yes (most OSes) |
| FIFO | \~1.8Ã--- | Very low (simple queue) | Rarely (too poor) |


Source: Empirical studies from Aho et al. (1971) and modern OS
textbooks.

**Real-World Choice:** Most operating systems use variants of the Clock
algorithm because it offers the best balance of performance and
implementation cost.

------------------------------------------------------------------------

## 2.4 Thrashing and the Working Set Model

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="620" viewBox="0 0 900 620" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#212121"></polygon></marker>
    <marker id="arr-b" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="arr-o" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-color="rgba(0,0,0,0.18)"></fedropshadow></filter>
  </defs>
  <rect width="900" height="620" style="fill:#fff" />

  <text x="30" y="36" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold">Figure 2.5 — Thrashing and the Working Set Model</text>

  <!-- ===== TOP LEFT: CPU Utilization Curve ===== -->
  <rect x="30" y="52" width="420" height="270" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="240" y="74" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:15; font-weight:bold; text-anchor:middle">CPU Utilization vs. Degree of Multiprogramming</text>

  <!-- Axes -->
  <line x1="70" y1="280" x2="420" y2="280" marker-end="url(#arr)" style="stroke:#212121; stroke-width:2"></line>
  <line x1="70" y1="280" x2="70" y2="90" marker-end="url(#arr)" style="stroke:#212121; stroke-width:2"></line>
  <text x="240" y="300" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">Number of Active Processes →</text>
  <text x="30" y="195" font-family="Arial,Helvetica,sans-serif" transform="rotate(-90,30,195)" style="fill:#212121; font-size:13; text-anchor:middle">CPU Utilization %</text>

  <!-- Y axis labels -->
  <text x="62" y="280" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:end">0%</text>
  <text x="62" y="217" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:end">50%</text>
  <text x="62" y="155" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:end">80%</text>
  <text x="62" y="110" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:end">100%</text>

  <!-- X axis labels -->
  <text x="120" y="292" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">2</text>
  <text x="180" y="292" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">4</text>
  <text x="240" y="292" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">6</text>
  <text x="300" y="292" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">8</text>
  <text x="360" y="292" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">10</text>
  <text x="410" y="292" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">12</text>

  <!-- CPU utilization curve: rises then crashes at thrashing point -->
  <!-- Points: (70,280)→(120,200)→(180,145)→(240,120)→(265,110)→(285,130)→(320,185)→(365,240)→(410,265) -->
  <polyline points="70,280 120,200 180,145 240,120 265,110 285,135 320,190 365,245 410,268" style="fill:none; stroke:#1565C0; stroke-width:3"></polyline>

  <!-- Peak marker and label -->
  <circle cx="265" cy="110" r="5" style="fill:#E65100"></circle>
  <line x1="265" y1="110" x2="265" y2="280" style="stroke:#E65100; stroke-width:1.5; stroke-dasharray:5,3"></line>
  <text x="262" y="106" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:12; text-anchor:middle">Peak</text>

  <!-- Thrashing zone shading -->
  <polygon points="285,280 285,130 410,268 410,280" style="fill:#FFECB3; opacity:0.7"></polygon>
  <text x="355" y="235" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">THRASHING</text>
  <text x="355" y="253" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:12; text-anchor:middle">zone</text>

  <!-- Normal zone annotation -->
  <text x="175" y="170" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:12; text-anchor:middle">Normal</text>
  <text x="175" y="184" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:12; text-anchor:middle">Operation</text>

  <!-- ===== TOP RIGHT: Vicious Cycle ===== -->
  <rect x="470" y="52" width="400" height="270" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="670" y="74" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:15; font-weight:bold; text-anchor:middle">The Thrashing Vicious Cycle</text>

  <!-- Cycle nodes (7 nodes arranged in oval) -->
  <!-- Center ~670, 185  radius ~90 -->
  <!-- Node positions: top=670,100 | top-right=755,130 | right=775,185 | bottom-right=730,250 | bottom=640,265 | left=560,185 | top-left=575,125 -->

  <!-- Node 1: Too many processes -->
  <rect x="595" y="90" width="150" height="32" rx="16" filter="url(#sh)" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
  <text x="670" y="111" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Too many processes</text>

  <!-- Arrow 1→2 -->
  <path d="M 720 116 Q 790 130 780 155" marker-end="url(#arr)" style="fill:none; stroke:#212121; stroke-width:2" />

  <!-- Node 2: Too few frames each -->
  <rect x="738" y="155" width="140" height="32" rx="16" filter="url(#sh)" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
  <text x="808" y="176" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Too few frames each</text>

  <!-- Arrow 2→3 -->
  <path d="M 775 190 Q 790 220 755 235" marker-end="url(#arr)" style="fill:none; stroke:#212121; stroke-width:2" />

  <!-- Node 3: Frequent page faults -->
  <rect x="660" y="233" width="150" height="32" rx="16" filter="url(#sh)" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
  <text x="735" y="254" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Frequent page faults</text>

  <!-- Arrow 3→4 -->
  <path d="M 660 258 Q 625 268 605 255" marker-end="url(#arr)" style="fill:none; stroke:#212121; stroke-width:2" />

  <!-- Node 4: Disk I/O saturated -->
  <rect x="480" y="233" width="128" height="32" rx="16" filter="url(#sh)" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
  <text x="544" y="254" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Disk I/O saturated</text>

  <!-- Arrow 4→5 -->
  <path d="M 484 233 Q 468 205 480 185" marker-end="url(#arr)" style="fill:none; stroke:#212121; stroke-width:2" />

  <!-- Node 5: CPU waits for I/O -->
  <rect x="476" y="155" width="135" height="32" rx="16" filter="url(#sh)" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
  <text x="543" y="176" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">CPU idles waiting I/O</text>

  <!-- Arrow 5→6 -->
  <path d="M 540 155 Q 540 130 575 118" marker-end="url(#arr)" style="fill:none; stroke:#212121; stroke-width:2" />

  <!-- Node 6: OS adds more processes (the bad decision) -->
  <!-- wraps back to node 1 — shown with special label -->
  <rect x="600" y="155" width="135" height="32" rx="16" filter="url(#sh)" style="fill:#BF360C; stroke:#7f0000; stroke-width:2" />
  <text x="667" y="169" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:12; font-weight:bold; text-anchor:middle">OS: low CPU util →</text>
  <text x="667" y="183" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:12; font-weight:bold; text-anchor:middle">add MORE processes!</text>

  <!-- Arrow 6 back to 1 -->
  <path d="M 670 155 Q 670 130 665 122" marker-end="url(#arr-o)" style="fill:none; stroke:#BF360C; stroke-width:2.5; stroke-dasharray:5,3" />

  <!-- OOM/solution callout -->
  <rect x="476" y="290" width="395" height="26" rx="5" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1" />
  <text x="673" y="308" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Solution: working set enforcement → suspend low-priority processes</text>

  <!-- ===== BOTTOM: Working Set Model ===== -->
  <rect x="30" y="340" width="840" height="250" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="30" y="340" width="840" height="34" rx="8" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="450" y="363" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Working Set Model: WS(t, Δ) — Pages Referenced in Window Δ</text>

  <!-- Reference string visualization -->
  <text x="60" y="396" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:14; font-weight:bold">Reference string (t=1→10):</text>
  <!-- boxes for each access -->
  <g font-family="Arial,Helvetica,sans-serif" style="font-size:15; font-weight:bold; text-anchor:middle">
    <!-- t=1: page 1 -->
    <rect x="250" y="380" width="38" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="269" y="399" style="fill:#212121">1</text>
    <text x="269" y="421" style="fill:#616161; font-size:12; font-weight:normal">t=1</text>
    <!-- t=2: page 2 -->
    <rect x="292" y="380" width="38" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="311" y="399" style="fill:#212121">2</text>
    <text x="311" y="421" style="fill:#616161; font-size:12; font-weight:normal">t=2</text>
    <!-- t=3: page 3 -->
    <rect x="334" y="380" width="38" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="353" y="399" style="fill:#212121">3</text>
    <text x="353" y="421" style="fill:#616161; font-size:12; font-weight:normal">t=3</text>
    <!-- t=4: page 4 -->
    <rect x="376" y="380" width="38" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="395" y="399" style="fill:#212121">4</text>
    <text x="395" y="421" style="fill:#616161; font-size:12; font-weight:normal">t=4</text>
    <!-- t=5: page 1 -->
    <rect x="418" y="380" width="38" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="437" y="399" style="fill:#212121">1</text>
    <text x="437" y="421" style="fill:#616161; font-size:12; font-weight:normal">t=5</text>
    <!-- t=6: page 2 -->
    <rect x="460" y="380" width="38" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="479" y="399" style="fill:#212121">2</text>
    <text x="479" y="421" style="fill:#616161; font-size:12; font-weight:normal">t=6</text>
    <!-- t=7: page 5 -->
    <rect x="502" y="380" width="38" height="28" rx="4" style="fill:#FFCCBC; stroke:#E65100; stroke-width:2" />
    <text x="521" y="399" style="fill:#212121">5</text>
    <text x="521" y="421" style="fill:#E65100; font-size:12; font-weight:normal">t=7 ★</text>
    <!-- t=8: page 1 -->
    <rect x="544" y="380" width="38" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="563" y="399" style="fill:#212121">1</text>
    <text x="563" y="421" style="fill:#616161; font-size:12; font-weight:normal">t=8</text>
    <!-- t=9: page 2 -->
    <rect x="586" y="380" width="38" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="605" y="399" style="fill:#212121">2</text>
    <text x="605" y="421" style="fill:#616161; font-size:12; font-weight:normal">t=9</text>
    <!-- t=10: page 3 -->
    <rect x="628" y="380" width="38" height="28" rx="4" style="fill:#C8E6C9; stroke:#00796B; stroke-width:2" />
    <text x="647" y="399" style="fill:#212121">3</text>
    <text x="647" y="421" style="fill:#00796B; font-size:12; font-weight:normal">t=10 ◆</text>
  </g>

  <!-- Window Δ=5 bracket at t=10 -->
  <line x1="502" y1="374" x2="666" y2="374" style="stroke:#E65100; stroke-width:2"></line>
  <line x1="502" y1="370" x2="502" y2="378" style="stroke:#E65100; stroke-width:2"></line>
  <line x1="666" y1="370" x2="666" y2="378" style="stroke:#E65100; stroke-width:2"></line>
  <text x="584" y="370" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Δ = 5 references window</text>

  <!-- Working sets at different t -->
  <!-- WS at t=5 (last 5 refs: 1,2,3,4,1 → {1,2,3,4}) -->
  <rect x="50" y="435" width="260" height="80" rx="6" style="fill:#E8F5E9; stroke:#00796B; stroke-width:1.5" />
  <text x="180" y="453" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">WS(t=5, Δ=5)</text>
  <text x="180" y="473" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">Last 5 refs: 1, 2, 3, 4, 1</text>
  <text x="180" y="493" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:14; font-weight:bold; text-anchor:middle">Working Set = {1, 2, 3, 4}</text>
  <text x="180" y="508" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:13; text-anchor:middle">Size = 4 pages needed in RAM</text>

  <!-- WS at t=10 (last 5: 5,1,2,3 → {1,2,3,5}) -->
  <rect x="330" y="435" width="260" height="80" rx="6" style="fill:#E8F5E9; stroke:#00796B; stroke-width:1.5" />
  <text x="460" y="453" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">WS(t=10, Δ=5)</text>
  <text x="460" y="473" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">Last 5 refs: 5, 1, 2, 3 (t=7→10)</text>
  <text x="460" y="493" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:14; font-weight:bold; text-anchor:middle">Working Set = {1, 2, 3, 5}</text>
  <text x="460" y="508" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:13; text-anchor:middle">Phase change at t=7: page 5 joins</text>

  <!-- Working set size over time mini chart -->
  <rect x="610" y="435" width="245" height="80" rx="6" style="fill:#FFF9C4; stroke:#F9A825; stroke-width:1.5" />
  <text x="732" y="453" font-family="Arial,Helvetica,sans-serif" style="fill:#F57F17; font-size:13; font-weight:bold; text-anchor:middle">Working Set Size Over Time</text>
  <!-- Mini axes -->
  <line x1="630" y1="505" x2="843" y2="505" marker-end="url(#arr)" style="stroke:#9E9E9E; stroke-width:1.5"></line>
  <line x1="630" y1="505" x2="630" y2="460" marker-end="url(#arr)" style="stroke:#9E9E9E; stroke-width:1.5"></line>
  <!-- Phases: init(large), steady(small), phase-change(spike), new-steady(medium) -->
  <polyline points="630,490 660,480 680,468 690,462 720,470 740,475 755,462 770,468 790,475 830,472" style="fill:none; stroke:#E65100; stroke-width:2.5"></polyline>
  <text x="645" y="519" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:11">Init</text>
  <text x="690" y="519" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:11">Steady</text>
  <text x="745" y="519" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:11">Phase↑</text>
  <text x="800" y="519" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:11">Stable</text>

  <!-- Bottom summary -->
  <rect x="30" y="598" width="840" height="22" rx="5" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="450" y="614" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">
    Thrashing prevention: only run processes whose working sets fit in RAM  |  Suspend excess processes until memory frees
  </text>
</svg>
</div>
<figcaption><strong>Figure 2.5:</strong> Thrashing and the working set
model: CPU utilization collapses when total working set sizes exceed
physical RAM. The working set W(t, Δ) defines pages actively used in the
last Δ references; allocating fewer frames than the working set triggers
thrashing.</figcaption>
</figure>

### 2.4.1 What is Thrashing?

**Thrashing** occurs when a system spends more time swapping pages
between memory and disk than executing useful work \[Denning, 1968\].

**Symptoms:** - CPU utilization drops dramatically (from 80% to \<10%) -
Disk I/O spikes to 100% - System becomes unresponsive - Applications
freeze or run extremely slowly

**Visual Representation of System State:**

### 2.4.2 Why Thrashing Occurs

**Scenario:** Too many active processes, insufficient physical memory

    System: 4 GB RAM, 10 processes, each needs 500 MB working set
    Total needed: 5 GB
    Available: 4 GB
    Deficit: 1 GB

    What happens:
    1. Process A runs, faults, loads pages
    2. No free frames â†’ evict pages from Process B
    3. Process B scheduled, faults on recently evicted pages
    4. No free frames â†’ evict pages from Process C
    5. Process C scheduled, faults...
    6. Repeat endlessly (thrashing)

**The Vicious Cycle:**

    Too many processes
       â†“
    Each process gets too few frames
       â†“
    Frequent page faults
       â†“
    High disk I/O
       â†“
    CPU idle waiting for I/O
       â†“
    OS sees low CPU utilization
       â†“
    OS adds MORE processes (!)
       â†“
    Even worse thrashing

### 2.4.3 The Working Set Model

**Working Set (Peter Denning, 1968):** The set of pages a process
actively uses during a time window.

**Definition:**\
WS(t, Î") = Set of pages referenced in time interval \[t - Î", t\]

Where: - t = current time - Î" = working set window (e.g., 10,000 memory
references)

**Example:**

    Process accesses pages: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3

    Working set window (Î”) = last 5 references

    At position 10:
    Last 5 references: 2, 5, 1, 2, 3
    Working set: {1, 2, 3, 5} (4 pages)

**Working Set Size Over Time:**

    Size
     |     â”Œâ”€â”€â”€â”€â”€â”
     |    â•±       â•²     â”Œâ”€â”€â”€â”€â”
     |   â•±         â•²   â•±      â•²
     |  â•±           â•² â•±        â•²
     | â•±             â•²          â•²
     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â†’ Time
       Init   Execute  Compute  I/O

Programs transition between phases: - **Initialization:** Large working
set (loading libraries) - **Steady state:** Small working set (main
loop) - **Phase change:** Working set spike (new functionality)

### 2.4.4 Preventing Thrashing

**Strategy 1: Working Set Algorithm**

    For each process P:
      1. Estimate working set size WS(P)
      2. Allocate at least WS(P) frames to P
      3. If Î£ WS(all processes) > Total RAM:
         â†’ Suspend some processes (don't run them)
      4. Only run processes whose working sets fit

**Strategy 2: Page Fault Frequency (PFF)**

    Monitor page fault rate for each process:

    If fault rate > upper threshold:
      â†’ Allocate more frames to this process
      
    If fault rate < lower threshold:
      â†’ Take away frames from this process
      
    If no frames available:
      â†’ Suspend process (swap out entirely)

**Strategy 3: Linux OOM Killer** When memory is critically low, Linux
uses the Out-Of-Memory (OOM) killer:

``` {.sourceCode .c}
// Simplified OOM scoring
int calculate_oom_score(process P) {
    score = P.memory_usage;           // Higher usage â†’ higher score
    score -= P.runtime * 10;          // Longer running â†’ lower score
    if (P.is_root_process) score = 0; // Don't kill init
    if (P.is_oom_protected) score = 0;// Don't kill critical processes
    return score;
}

// Kill highest scoring process
void oom_kill() {
    process victim = find_highest_score();
    send_signal(victim, SIGKILL);
    log("OOM: Killed process %d (%s)", victim.pid, victim.name);
}
```

**Real-World Example:**

``` {.sourceCode .bash}
# Linux kernel message when OOM killer activates
[1234567.890] Out of memory: Kill process 12345 (chrome) score 925 or sacrifice child
[1234567.891] Killed process 12345 (chrome) total-vm:8388608kB, anon-rss:7340032kB, file-rss:0kB
```

### 2.4.5 Detecting Thrashing

**Metrics to monitor:**

``` {.sourceCode .bash}
# Linux: Check page fault rate
sar -B 1 10
# Output:
# pgfault/s: Page faults per second
# major/s: Major page faults (from disk)
# If major/s > 100, you might be thrashing

# Check swap activity
vmstat 1
# si: Swap in (KB/s)
# so: Swap out (KB/s)
# If si + so > 1000 KB/s sustained, investigate

# Check if processes are waiting for I/O
top
# Look for high %wa (wait for I/O)
# If %wa > 30%, likely I/O bound (possibly thrashing)
```

------------------------------------------------------------------------

## 2.5 Copy-on-Write (COW)

### 2.5.1 The Problem COW Solves

When a process calls `fork()` to create a child process, traditionally
the OS would: 1. Copy all of the parent's memory pages to the child 2.
This could be hundreds of megabytes or gigabytes 3. Very slow and
wasteful if child immediately calls `exec()` to run a new program

**Example:**

``` {.sourceCode .c}
// Parent process using 2 GB of memory
int main() {
    char *big_buffer = malloc(2 * 1024 * 1024 * 1024);  // 2 GB
    // ... fill buffer with data ...
    
    pid_t pid = fork();  // Create child
    
    if (pid == 0) {
        // Child process
        exec("/bin/ls");  // Immediately replace with new program
        // All that copied memory is wasted!
    }
}
```

Traditional approach: Copy 2 GB, then immediately discard it when
`exec()` is called.

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="560" viewBox="0 0 900 560" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arrow-dark" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" style="fill:#212121"></polygon>
    </marker>
    <marker id="arrow-orange" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" style="fill:#E65100"></polygon>
    </marker>
    <marker id="arrow-blue" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" style="fill:#1565C0"></polygon>
    </marker>
    <marker id="arrow-teal" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" style="fill:#00796B"></polygon>
    </marker>
    <filter id="shadow">
      <fedropshadow dx="2" dy="3" stddeviation="3" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
  </defs>

  <rect width="900" height="560" style="fill:#FFFFFF" />

  <!-- Title -->
  <text x="30" y="38" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:20; font-weight:bold">Figure 2.3 — Copy-on-Write (COW): Shared Pages Before and After fork()</text>

  <!-- ===== BEFORE FORK — LEFT PANEL ===== -->
  <rect x="30" y="55" width="390" height="460" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="30" y="55" width="390" height="36" rx="8" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="225" y="79" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:16; font-weight:bold; text-anchor:middle">BEFORE fork() — Single Process</text>

  <!-- Parent Process -->
  <g filter="url(#shadow)">
    <rect x="60" y="105" width="140" height="60" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
    <text x="130" y="131" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">Parent Process</text>
    <text x="130" y="151" font-family="Arial, Helvetica, sans-serif" style="fill:#BDBDBD; font-size:13; text-anchor:middle">Virtual Address Space</text>
  </g>

  <!-- Parent page table entries -->
  <text x="60" y="185" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13; font-weight:bold">Page Table (Parent):</text>
  <g font-family="Arial, Helvetica, sans-serif" style="font-size:14; text-anchor:middle">
    <rect x="60" y="192" width="130" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="125" y="211" style="fill:#212121">VPN 0 → PPN 10</text>
    <rect x="60" y="226" width="130" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="125" y="245" style="fill:#212121">VPN 1 → PPN 15</text>
    <rect x="60" y="260" width="130" height="28" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1.5" />
    <text x="125" y="279" style="fill:#212121">VPN 2 → PPN 22</text>
  </g>

  <!-- Arrows to physical pages -->
  <line x1="190" y1="206" x2="245" y2="222" marker-end="url(#arrow-blue)" style="stroke:#1565C0; stroke-width:1.5"></line>
  <line x1="190" y1="240" x2="245" y2="318" marker-end="url(#arrow-blue)" style="stroke:#1565C0; stroke-width:1.5"></line>
  <line x1="190" y1="274" x2="245" y2="414" marker-end="url(#arrow-blue)" style="stroke:#1565C0; stroke-width:1.5"></line>

  <!-- Physical Memory frames -->
  <text x="248" y="205" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13; font-weight:bold">Physical RAM:</text>
  <g font-family="Arial, Helvetica, sans-serif" style="font-size:14; text-anchor:middle">
    <rect x="248" y="210" width="130" height="30" rx="4" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
    <text x="313" y="230" style="fill:#FFFFFF; font-weight:bold">Frame 10 — Code</text>
    <rect x="248" y="305" width="130" height="30" rx="4" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
    <text x="313" y="325" style="fill:#FFFFFF; font-weight:bold">Frame 15 — Stack</text>
    <rect x="248" y="400" width="130" height="30" rx="4" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
    <text x="313" y="420" style="fill:#FFFFFF; font-weight:bold">Frame 22 — Heap</text>
  </g>

  <text x="225" y="490" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13; text-anchor:middle">All pages writable. One copy in RAM.</text>

  <!-- ===== DIVIDER / FORK EVENT ===== -->
  <g id="fork-event" transform="translate(450,285)">
    <rect x="-30" y="-36" width="60" height="72" rx="30" filter="url(#shadow)" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
    <text x="0" y="-12" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">fork()</text>
    <text x="0" y="8" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:11; text-anchor:middle">shallow</text>
    <text x="0" y="23" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:11; text-anchor:middle">copy →</text>
  </g>
  <line x1="420" y1="285" x2="482" y2="285" style="stroke:#E65100; stroke-width:2.5; stroke-dasharray:5,3"></line>

  <!-- ===== AFTER FORK — RIGHT PANEL ===== -->
  <rect x="480" y="55" width="400" height="460" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="480" y="55" width="400" height="36" rx="8" style="fill:#E65100; stroke:#BF360C; stroke-width:1.5" />
  <text x="680" y="79" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:16; font-weight:bold; text-anchor:middle">AFTER fork() — Child Writes to Heap</text>

  <!-- Parent box -->
  <g filter="url(#shadow)">
    <rect x="495" y="100" width="120" height="50" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
    <text x="555" y="122" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Parent</text>
    <text x="555" y="140" font-family="Arial, Helvetica, sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">read-only map</text>
  </g>

  <!-- Child box -->
  <g filter="url(#shadow)">
    <rect x="755" y="100" width="110" height="50" rx="6" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
    <text x="810" y="122" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Child</text>
    <text x="810" y="140" font-family="Arial, Helvetica, sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">write triggers COW</text>
  </g>

  <!-- Physical memory — shared frames -->
  <text x="655" y="190" font-family="Arial, Helvetica, sans-serif" style="fill:#616161; font-size:13; font-weight:bold; text-anchor:middle">Physical RAM:</text>

  <!-- Frame 10 — Code: SHARED (read-only) -->
  <rect x="610" y="198" width="145" height="30" rx="4" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
  <text x="682" y="218" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Frame 10 — Code</text>
  <rect x="760" y="202" width="60" height="22" rx="4" style="fill:#C8E6C9; stroke:#00796B; stroke-width:1" />
  <text x="790" y="218" font-family="Arial, Helvetica, sans-serif" style="fill:#00796B; font-size:12; font-weight:bold; text-anchor:middle">SHARED</text>

  <!-- Frame 15 — Stack: SHARED -->
  <rect x="610" y="290" width="145" height="30" rx="4" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
  <text x="682" y="310" font-family="Arial, Helvetica, sans-serif" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Frame 15 — Stack</text>
  <rect x="760" y="294" width="60" height="22" rx="4" style="fill:#C8E6C9; stroke:#00796B; stroke-width:1" />
  <text x="790" y="310" font-family="Arial, Helvetica, sans-serif" style="fill:#00796B; font-size:12; font-weight:bold; text-anchor:middle">SHARED</text>

  <!-- Frame 22 — Original Heap: Parent maps here, now read-only -->
  <rect x="610" y="382" width="145" height="30" rx="4" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:2; stroke-dasharray:5,3" />
  <text x="682" y="402" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">Frame 22 — Heap</text>
  <rect x="760" y="386" width="70" height="22" rx="4" style="fill:#FFF9C4; stroke:#F9A825; stroke-width:1" />
  <text x="795" y="402" font-family="Arial, Helvetica, sans-serif" style="fill:#F57F17; font-size:11; font-weight:bold; text-anchor:middle">Parent R/O</text>

  <!-- New Frame 35 — Child's COW copy of Heap -->
  <rect x="610" y="430" width="145" height="30" rx="4" style="fill:#FFCCBC; stroke:#E65100; stroke-width:2" />
  <text x="682" y="450" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">Frame 35 — Heap′ (copy)</text>
  <rect x="760" y="434" width="70" height="22" rx="4" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
  <text x="795" y="450" font-family="Arial, Helvetica, sans-serif" style="fill:#BF360C; font-size:11; font-weight:bold; text-anchor:middle">Child R/W</text>

  <!-- Arrow: Parent → shared frames -->
  <line x1="555" y1="150" x2="610" y2="210" marker-end="url(#arrow-blue)" style="stroke:#1565C0; stroke-width:1.5"></line>
  <line x1="555" y1="150" x2="610" y2="302" marker-end="url(#arrow-blue)" style="stroke:#1565C0; stroke-width:1.5"></line>
  <line x1="555" y1="150" x2="610" y2="394" marker-end="url(#arrow-blue)" style="stroke:#1565C0; stroke-width:1.5"></line>

  <!-- Arrow: Child → shared frames -->
  <line x1="810" y1="150" x2="757" y2="210" marker-end="url(#arrow-teal)" style="stroke:#00796B; stroke-width:1.5"></line>
  <line x1="810" y1="150" x2="757" y2="302" marker-end="url(#arrow-teal)" style="stroke:#00796B; stroke-width:1.5"></line>

  <!-- Arrow: Child → COW copy of heap (orange — write fault triggered) -->
  <line x1="810" y1="150" x2="757" y2="442" marker-end="url(#arrow-orange)" style="stroke:#E65100; stroke-width:2; stroke-dasharray:6,3"></line>
  <text x="845" y="295" font-family="Arial, Helvetica, sans-serif" style="fill:#E65100; font-size:12; font-weight:bold; text-anchor:middle">Write</text>
  <text x="845" y="310" font-family="Arial, Helvetica, sans-serif" style="fill:#E65100; font-size:12; font-weight:bold; text-anchor:middle">fault!</text>
  <text x="845" y="325" font-family="Arial, Helvetica, sans-serif" style="fill:#E65100; font-size:12; font-weight:bold; text-anchor:middle">→ COW</text>
  <text x="845" y="340" font-family="Arial, Helvetica, sans-serif" style="fill:#E65100; font-size:12; font-weight:bold; text-anchor:middle">copy</text>

  <!-- COW Benefits callout -->
  <rect x="490" y="476" width="375" height="28" rx="5" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="677" y="495" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">
    COW saves RAM: shared pages copied <tspan font-style="italic">only</tspan> when written — lazy allocation
  </text>

  <!-- Legend -->
  <rect x="30" y="525" width="14" height="14" rx="2" style="fill:#00796B" />
  <text x="50" y="537" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:13">Shared (read-only COW)</text>
  <rect x="220" y="525" width="14" height="14" rx="2" style="fill:#BBDEFB; stroke:#1565C0; stroke-width:1" />
  <text x="240" y="537" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:13">Original frame (Parent R/O)</text>
  <rect x="450" y="525" width="14" height="14" rx="2" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1" />
  <text x="470" y="537" font-family="Arial, Helvetica, sans-serif" style="fill:#212121; font-size:13">New copy allocated (Child R/W)</text>
</svg>
</div>
<figcaption><strong>Figure 2.3:</strong> Copy-on-Write (COW): after
fork(), parent and child share physical pages marked read-only. On the
first write by either process, the MMU raises a protection fault; the OS
copies only the written page to a new frame, leaving all other pages
shared.</figcaption>
</figure>

### 2.5.2 How Copy-on-Write Works

**Copy-on-Write (COW):** Initially share memory pages between parent and
child, copying only when one writes to a page.

**Implementation:**

    1. Parent calls fork()
    2. Child's page table created
    3. Both parent and child page tables point to SAME physical frames
    4. All pages marked as read-only (even if originally writable)
    5. Parent and child run

    6. Either process tries to WRITE to a shared page
    7. MMU detects write to read-only page â†’ Page Fault
    8. OS page fault handler:
       a. Recognize this is COW fault
       b. Allocate new physical frame
       c. Copy page contents to new frame
       d. Update faulting process's page table to new frame
       e. Mark both pages as writable
    9. Retry the write instruction (now succeeds)

**Visual Example:**

    Before fork():
    Parent Process
      Virtual Page 0 â†’ Physical Frame 100 (R/W)
      Virtual Page 1 â†’ Physical Frame 101 (R/W)

    After fork() (COW):
    Parent Process                Child Process
      VP 0 â†’ PF 100 (R-only)       VP 0 â†’ PF 100 (R-only)  } Shared
      VP 1 â†’ PF 101 (R-only)       VP 1 â†’ PF 101 (R-only)  } Shared

    Parent writes to VP 0:
      - Page fault (write to read-only)
      - Allocate new frame 200
      - Copy frame 100 â†’ frame 200
      - Update parent's PT: VP 0 â†’ PF 200 (R/W)
      
    After parent's write:
    Parent Process                Child Process
      VP 0 â†’ PF 200 (R/W)          VP 0 â†’ PF 100 (R/W)     } Private
      VP 1 â†’ PF 101 (R-only)       VP 1 â†’ PF 101 (R-only)  } Still shared

### 2.5.3 Benefits of COW

**Performance:**

    Traditional fork() of 1 GB process:
      - Copy 1 GB = 250,000 page copies (at 4 KB/page)
      - Time: ~500 ms (at 2 GB/s memory bandwidth)

    COW fork() of 1 GB process:
      - Copy page tables only = ~250 KB
      - Time: ~1 ms
      
    Speed improvement: 500Ã— faster!

**Memory Efficiency:**

    If child immediately calls exec():
      - Traditional: Wasted 1 GB of copy
      - COW: Wasted 0 bytes (no copies made)

    If parent and child both read (common case):
      - Traditional: Uses 2 GB (duplicate memory)
      - COW: Uses 1 GB (shared)

**Real-World Impact:** Modern systems heavily use `fork()` + `exec()`: -
Shell executing commands - Web servers spawning workers - Build systems
compiling code

COW makes these operations practical.

### 2.5.4 COW in Other Contexts

**File Systems (ZFS, Btrfs):**

``` {.sourceCode .c}
// Create snapshot of filesystem
zfs snapshot pool/filesystem@snapshot

// Snapshot is instantaneous (COW)
// Original and snapshot share blocks
// Blocks copied only when modified
```

**Containers (Docker):**

``` {.sourceCode .bash}
# Docker image layers use COW
docker run ubuntu  # Shares base image with all containers
# Each container has COW layer for changes
# Saves gigabytes of disk space
```

**Virtual Machines:**

    Base disk image: windows.qcow2 (20 GB)
    VM1 snapshot: vm1.qcow2 (points to windows.qcow2, COW)
    VM2 snapshot: vm2.qcow2 (points to windows.qcow2, COW)

    All VMs share base image, copy blocks only when writing

------------------------------------------------------------------------

## 2.6 Memory-Mapped Files

### 2.6.1 Traditional File I/O vs. Memory Mapping

**Traditional File I/O:**

``` {.sourceCode .c}
int fd = open("data.txt", O_RDONLY);
char buffer[4096];
read(fd, buffer, 4096);  // Copy from kernel buffer to user buffer
// Work with buffer
close(fd);
```

Data path: Disk â†' Kernel buffer â†' User buffer (two copies)

**Memory-Mapped I/O:**

``` {.sourceCode .c}
int fd = open("data.txt", O_RDONLY);
char *ptr = mmap(NULL, file_size, PROT_READ, MAP_SHARED, fd, 0);
// ptr[x] directly accesses file contents
// No explicit read() call needed
munmap(ptr, file_size);
close(fd);
```

Data path: Disk â†' Kernel buffer â†' Mapped into user address space
(zero copy)

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="560" viewBox="0 0 900 560" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#212121"></polygon></marker>
    <marker id="arr-b" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="arr-t" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-color="rgba(0,0,0,0.18)"></fedropshadow></filter>
  </defs>
  <rect width="900" height="560" style="fill:#fff" />

  <text x="30" y="36" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold">Figure 2.6 — Memory-Mapped Files vs. Traditional File I/O</text>

  <!-- ===== LEFT: TRADITIONAL I/O ===== -->
  <rect x="30" y="52" width="400" height="390" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="30" y="52" width="400" height="34" rx="8" style="fill:#9E9E9E; stroke:#757575; stroke-width:1.5" />
  <text x="230" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Traditional File I/O — Two-Copy Path</text>

  <!-- Layers: App Buffer → Kernel Buffer → Disk -->
  <!-- Disk -->
  <g filter="url(#sh)">
    <rect x="135" y="95" width="190" height="50" rx="6" style="fill:#616161; stroke:#424242; stroke-width:2" />
  </g>
  <text x="230" y="116" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">💾  Disk / Storage</text>
  <text x="230" y="135" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:13; text-anchor:middle">file data at rest</text>

  <!-- Arrow: disk → kernel -->
  <line x1="230" y1="145" x2="230" y2="178" marker-end="url(#arr)" style="stroke:#212121; stroke-width:2.5"></line>
  <text x="275" y="166" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold">① read()</text>
  <text x="275" y="180" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12">DMA transfer</text>

  <!-- Kernel Page Cache / Buffer -->
  <g filter="url(#sh)">
    <rect x="95" y="182" width="270" height="55" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  </g>
  <text x="230" y="205" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Kernel Page Cache</text>
  <text x="230" y="225" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:13; text-anchor:middle">(buffer in kernel address space)</text>

  <!-- Arrow: kernel → user -->
  <line x1="230" y1="237" x2="230" y2="270" marker-end="url(#arr)" style="stroke:#212121; stroke-width:2.5"></line>
  <text x="275" y="257" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold">② copy_to_user()</text>
  <text x="275" y="271" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12">memcpy: kernel→user</text>

  <!-- User buffer -->
  <g filter="url(#sh)">
    <rect x="95" y="274" width="270" height="55" rx="6" style="fill:#00796B; stroke:#004D40; stroke-width:2" />
  </g>
  <text x="230" y="297" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">User Application Buffer</text>
  <text x="230" y="317" font-family="Arial,Helvetica,sans-serif" style="fill:#B2DFDB; font-size:13; text-anchor:middle">char buffer[4096] on stack/heap</text>

  <!-- CPU processes data -->
  <g filter="url(#sh)">
    <rect x="135" y="348" width="190" height="40" rx="6" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
  </g>
  <text x="230" y="369" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">③ CPU processes buffer</text>

  <!-- Cost annotation -->
  <rect x="45" y="400" width="372" height="32" rx="5" style="fill:#FFECB3; stroke:#F9A825; stroke-width:1.5" />
  <text x="231" y="414" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Cost: 2 data copies + 2 context switches per read()</text>
  <text x="231" y="428" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">Disk→Kernel (DMA) + Kernel→User (CPU memcpy)</text>

  <!-- ===== RIGHT: MMAP I/O ===== -->
  <rect x="460" y="52" width="410" height="390" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="460" y="52" width="410" height="34" rx="8" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
  <text x="665" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Memory-Mapped I/O — Zero-Copy Path</text>

  <!-- Disk -->
  <g filter="url(#sh)">
    <rect x="570" y="95" width="190" height="50" rx="6" style="fill:#616161; stroke:#424242; stroke-width:2" />
  </g>
  <text x="665" y="116" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">💾  Disk / Storage</text>
  <text x="665" y="135" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:13; text-anchor:middle">file data at rest</text>

  <!-- Arrow: disk → kernel page cache -->
  <line x1="665" y1="145" x2="665" y2="178" marker-end="url(#arr)" style="stroke:#212121; stroke-width:2.5"></line>
  <text x="710" y="166" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold">① page fault</text>
  <text x="710" y="180" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12">DMA on demand</text>

  <!-- Kernel Page Cache = shared directly -->
  <g filter="url(#sh)">
    <rect x="520" y="182" width="290" height="120" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  </g>
  <text x="665" y="208" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Kernel Page Cache</text>
  <text x="665" y="228" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:13; text-anchor:middle">= also User&#39;s mapped pages</text>
  <!-- PTE inside box -->
  <rect x="534" y="238" width="262" height="30" rx="4" style="fill:#0D47A1; stroke:#BBDEFB; stroke-width:1" />
  <text x="665" y="258" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">PTE: VPN → same physical frames</text>
  <text x="665" y="295" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">② OS maps pages into process VA space</text>

  <!-- Direct access annotation - no arrow down needed -->
  <line x1="665" y1="302" x2="665" y2="330" marker-end="url(#arr-t)" style="stroke:#00796B; stroke-width:2.5; stroke-dasharray:6,3"></line>
  <text x="720" y="320" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:13; font-weight:bold">ZERO COPY</text>

  <!-- User access -->
  <g filter="url(#sh)">
    <rect x="520" y="333" width="290" height="45" rx="6" style="fill:#00796B; stroke:#004D40; stroke-width:2" />
  </g>
  <text x="665" y="352" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">③ ptr[offset] — direct access</text>
  <text x="665" y="370" font-family="Arial,Helvetica,sans-serif" style="fill:#B2DFDB; font-size:13; text-anchor:middle">no read() call, no copy, no syscall</text>

  <!-- Cost annotation -->
  <rect x="475" y="393" width="380" height="42" rx="5" style="fill:#E8F5E9; stroke:#00796B; stroke-width:1.5" />
  <text x="665" y="408" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Cost: 1 data copy (DMA only). No kernel→user memcpy.</text>
  <text x="665" y="425" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">Dirty pages written back to file on eviction (D=1 → writeback)</text>

  <!-- ===== BOTTOM: Shared Memory via mmap ===== -->
  <rect x="30" y="455" width="840" height="90" rx="8" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="450" y="476" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:15; font-weight:bold; text-anchor:middle">Bonus: Inter-Process Shared Memory via mmap(MAP_SHARED)</text>

  <!-- Process A -->
  <rect x="55" y="486" width="120" height="48" rx="6" filter="url(#sh)" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  <text x="115" y="505" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Process A</text>
  <text x="115" y="522" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">ptr_a[0] = 42</text>

  <!-- Arrow A → shared frames -->
  <line x1="175" y1="510" x2="318" y2="510" marker-end="url(#arr-b)" style="stroke:#1565C0; stroke-width:2"></line>

  <!-- Shared physical frames -->
  <rect x="320" y="486" width="220" height="48" rx="6" filter="url(#sh)" style="fill:#00796B; stroke:#004D40; stroke-width:2" />
  <text x="430" y="505" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Shared Physical Frames</text>
  <text x="430" y="522" font-family="Arial,Helvetica,sans-serif" style="fill:#B2DFDB; font-size:12; text-anchor:middle">(Kernel Page Cache)</text>

  <!-- Arrow shared frames → B -->
  <line x1="540" y1="510" x2="718" y2="510" marker-end="url(#arr-b)" style="stroke:#1565C0; stroke-width:2"></line>

  <!-- Process B -->
  <rect x="720" y="486" width="130" height="48" rx="6" filter="url(#sh)" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  <text x="785" y="505" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Process B</text>
  <text x="785" y="522" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">ptr_b[0] → 42 ✓</text>
</svg>
</div>
<figcaption><strong>Figure 2.6:</strong> Memory-mapped files vs.
traditional file I/O: traditional I/O copies data through kernel buffers
(two copies per read); mmap() maps file pages directly into the process
address space, allowing zero-copy access and sharing the page cache
across processes.</figcaption>
</figure>

### 2.6.2 How Memory Mapping Works

**Step-by-Step:**

    1. Application calls mmap(file, size, ...)
    2. OS creates VMA (Virtual Memory Area) in process address space
    3. VMA marked as "file-backed" (points to file)
    4. No pages loaded yet (demand paging)
    5. Application accesses ptr[offset]
    6. Page fault (page not present)
    7. OS reads page from file into memory
    8. Maps page into process address space
    9. Access succeeds

**Page Table Entry for Memory-Mapped File:**

    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚ Frame Number â”‚ P â”‚ D â”‚ A â”‚  File: data.txt        â”‚
    â”‚              â”‚   â”‚   â”‚   â”‚  Offset: 12288         â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

    If evicted: Don't swap to swap file, just drop
    If dirty (D=1): Write back to original file

### 2.6.3 Advantages of Memory Mapping

**1. Simplified Programming:**

``` {.sourceCode .c}
// Traditional I/O (complex)
while (offset < file_size) {
    bytes_read = read(fd, buffer, BUFFER_SIZE);
    if (bytes_read <= 0) break;
    process_data(buffer, bytes_read);
    offset += bytes_read;
}

// Memory mapping (simple)
for (int i = 0; i < file_size; i++) {
    process_byte(file_ptr[i]);  // Just like an array!
}
```

**2. Zero-Copy I/O:** No copying between kernel and user space---direct
access to kernel's page cache.

**3. Sharing Between Processes:**

``` {.sourceCode .c}
// Process A
int fd = open("shared.dat", O_RDWR);
void *ptr = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);

// Process B (different process)
int fd = open("shared.dat", O_RDWR);
void *ptr = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);

// Both processes see the same physical pages
// Changes by Process A are visible to Process B
```

**4. Lazy Loading:** Large files can be mapped without loading entire
file into memory. Pages loaded on-demand.

### 2.6.4 Use Cases

**Databases:**

``` {.sourceCode .c}
// SQLite, LMDB, and many others use mmap
void *db_file = mmap(NULL, db_size, PROT_READ|PROT_WRITE, 
                     MAP_SHARED, db_fd, 0);
// Treat file as in-memory database
// OS handles caching automatically
```

**Shared Libraries:**

``` {.sourceCode .bash}
# All processes using libc.so share the same physical pages
$ cat /proc/1234/maps | grep libc
7f1234567000-7f1234700000 r-xp 00000000 08:01 12345  /lib/x86_64-linux-gnu/libc.so.6

# Code pages shared, data pages COW
```

**Inter-Process Communication (Shared Memory):**

``` {.sourceCode .c}
// Modern POSIX shared memory
int shm_fd = shm_open("/my_shm", O_CREAT|O_RDWR, 0666);
ftruncate(shm_fd, 4096);
void *ptr = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_SHARED, shm_fd, 0);
// Fastest IPC mechanism (no copies, just shared pages)
```

------------------------------------------------------------------------

## 2.7 Advanced Topics

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 900 600" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#212121"></polygon></marker>
    <marker id="arr-b" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="arr-t" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker>
    <marker id="arr-o" markerwidth="10" markerheight="7" refx="10" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-color="rgba(0,0,0,0.18)"></fedropshadow></filter>
  </defs>
  <rect width="900" height="600" style="fill:#fff" />

  <text x="30" y="36" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold">Figure 2.7 — Huge Pages and NUMA Architecture</text>

  <!-- ===== TOP LEFT: 4KB pages TLB problem ===== -->
  <rect x="30" y="52" width="405" height="270" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="30" y="52" width="405" height="34" rx="8" style="fill:#9E9E9E; stroke:#757575; stroke-width:1.5" />
  <text x="232" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Standard 4 KB Pages — 1 GB Region</text>

  <!-- TLB box — small, overflowing -->
  <g filter="url(#sh)">
    <rect x="55" y="96" width="160" height="200" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  </g>
  <text x="135" y="116" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">TLB</text>
  <text x="135" y="133" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">(1,536 entries typical)</text>
  <!-- TLB entries — a few visible, then "..." -->
  <rect x="65" y="142" width="140" height="18" rx="3" style="fill:#BBDEFB" />
  <text x="135" y="155" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:11; text-anchor:middle">VPN 0 → PPN 400</text>
  <rect x="65" y="163" width="140" height="18" rx="3" style="fill:#BBDEFB" />
  <text x="135" y="176" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:11; text-anchor:middle">VPN 1 → PPN 401</text>
  <rect x="65" y="184" width="140" height="18" rx="3" style="fill:#BBDEFB" />
  <text x="135" y="197" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:11; text-anchor:middle">VPN 2 → PPN 402</text>
  <text x="135" y="220" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:18; text-anchor:middle">⋮</text>
  <text x="135" y="248" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">1,536 / 262,144</text>
  <text x="135" y="265" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">entries fit</text>
  <text x="135" y="282" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:11; text-anchor:middle">OVERFLOW!</text>

  <!-- Stats right side -->
  <text x="255" y="108" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold">1 GB ÷ 4 KB =</text>
  <rect x="250" y="114" width="165" height="28" rx="4" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1.5" />
  <text x="332" y="133" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:15; font-weight:bold; text-anchor:middle">262,144 pages</text>

  <text x="255" y="165" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold">TLB entries needed:</text>
  <rect x="250" y="170" width="165" height="28" rx="4" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1.5" />
  <text x="332" y="189" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:15; font-weight:bold; text-anchor:middle">262,144 ← won&#39;t fit</text>

  <text x="255" y="222" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold">Result:</text>
  <rect x="250" y="228" width="165" height="40" rx="4" style="fill:#FFCCBC; stroke:#E65100; stroke-width:1.5" />
  <text x="332" y="244" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Constant TLB misses</text>
  <text x="332" y="260" font-family="Arial,Helvetica,sans-serif" style="fill:#BF360C; font-size:12; text-anchor:middle">→ page table walks</text>

  <text x="232" y="298" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Performance: baseline (1×)</text>

  <!-- ===== TOP RIGHT: 2MB Huge Pages ===== -->
  <rect x="460" y="52" width="410" height="270" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="460" y="52" width="410" height="34" rx="8" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
  <text x="665" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">2 MB Huge Pages — Same 1 GB Region</text>

  <!-- TLB box — comfortable fit -->
  <g filter="url(#sh)">
    <rect x="480" y="96" width="160" height="185" rx="6" style="fill:#00796B; stroke:#004D40; stroke-width:2" />
  </g>
  <text x="560" y="116" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">TLB (L2)</text>
  <text x="560" y="133" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">(1,536 entries typical)</text>
  <!-- 512 entries visible and fitting -->
  <rect x="490" y="142" width="140" height="18" rx="3" style="fill:#B2DFDB" />
  <text x="560" y="155" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:11; text-anchor:middle">HPN 0 → PPN 0x200</text>
  <rect x="490" y="163" width="140" height="18" rx="3" style="fill:#B2DFDB" />
  <text x="560" y="176" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:11; text-anchor:middle">HPN 1 → PPN 0x400</text>
  <rect x="490" y="184" width="140" height="18" rx="3" style="fill:#B2DFDB" />
  <text x="560" y="197" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:11; text-anchor:middle">HPN 2 → PPN 0x600</text>
  <text x="560" y="225" font-family="Arial,Helvetica,sans-serif" style="fill:#B2DFDB; font-size:16; text-anchor:middle">⋮</text>
  <text x="560" y="256" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:13; text-anchor:middle">512 entries total</text>
  <text x="560" y="272" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:12; text-anchor:middle">ALL FIT ✓</text>

  <!-- Stats -->
  <text x="680" y="108" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold">1 GB ÷ 2 MB =</text>
  <rect x="675" y="114" width="165" height="28" rx="4" style="fill:#C8E6C9; stroke:#00796B; stroke-width:1.5" />
  <text x="757" y="133" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:15; font-weight:bold; text-anchor:middle">512 pages only</text>

  <text x="680" y="165" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold">TLB entries needed:</text>
  <rect x="675" y="170" width="165" height="28" rx="4" style="fill:#C8E6C9; stroke:#00796B; stroke-width:1.5" />
  <text x="757" y="189" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:15; font-weight:bold; text-anchor:middle">512 ← fits easily</text>

  <text x="680" y="222" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold">Result:</text>
  <rect x="675" y="228" width="165" height="40" rx="4" style="fill:#C8E6C9; stroke:#00796B; stroke-width:1.5" />
  <text x="757" y="244" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">TLB misses: rare</text>
  <text x="757" y="260" font-family="Arial,Helvetica,sans-serif" style="fill:#00695C; font-size:12; text-anchor:middle">→ no page walk needed</text>

  <text x="665" y="298" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Performance: 2–4× faster for memory-intensive workloads</text>

  <!-- ===== BOTTOM: NUMA Topology ===== -->
  <rect x="30" y="338" width="840" height="242" rx="8" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="30" y="338" width="840" height="34" rx="8" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="450" y="361" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">NUMA (Non-Uniform Memory Access) — 2-Socket Server Topology</text>

  <!-- NUMA Node 0 -->
  <rect x="55" y="384" width="350" height="175" rx="8" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:2" />
  <text x="230" y="403" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">NUMA Node 0</text>

  <!-- CPU 0 cores -->
  <g filter="url(#sh)">
    <rect x="70" y="412" width="140" height="80" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  </g>
  <text x="140" y="432" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">CPU Socket 0</text>
  <rect x="78" y="443" width="55" height="22" rx="3" style="fill:#42A5F5" />
  <text x="105" y="458" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Core 0–3</text>
  <rect x="137" y="443" width="65" height="22" rx="3" style="fill:#42A5F5" />
  <text x="170" y="458" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Core 4–7</text>
  <text x="140" y="484" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">L3 Cache: 32 MB</text>

  <!-- Local Memory 0 -->
  <g filter="url(#sh)">
    <rect x="230" y="412" width="155" height="80" rx="6" style="fill:#00796B; stroke:#004D40; stroke-width:2" />
  </g>
  <text x="307" y="432" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Local Memory 0</text>
  <text x="307" y="452" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:14; text-anchor:middle">128 GB DDR5</text>
  <rect x="238" y="460" width="139" height="22" rx="4" style="fill:#004D40" />
  <text x="307" y="475" font-family="Arial,Helvetica,sans-serif" style="fill:#4DB6AC; font-size:13; font-weight:bold; text-anchor:middle">Latency: ~70 ns ✓</text>

  <!-- Local access arrow -->
  <line x1="210" y1="452" x2="228" y2="452" marker-end="url(#arr-t)" style="stroke:#00796B; stroke-width:2.5"></line>
  <text x="218" y="446" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:11; text-anchor:middle">fast</text>

  <!-- Interconnect annotation -->
  <rect x="65" y="506" width="325" height="42" rx="5" style="fill:#fff; stroke:#1565C0; stroke-width:1" />
  <text x="227" y="521" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; font-weight:bold; text-anchor:middle">NUMA-aware allocation:</text>
  <text x="227" y="540" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">numa_alloc_local() → always use node-local RAM</text>

  <!-- QPI / UPI Interconnect in center -->
  <rect x="415" y="430" width="70" height="60" rx="6" filter="url(#sh)" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
  <text x="450" y="450" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; font-weight:bold; text-anchor:middle">QPI /</text>
  <text x="450" y="466" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; font-weight:bold; text-anchor:middle">UPI</text>
  <text x="450" y="482" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:11; text-anchor:middle">Link</text>
  <!-- Arrows through interconnect -->
  <line x1="405" y1="460" x2="368" y2="460" marker-end="url(#arr-o)" style="stroke:#E65100; stroke-width:2.5; stroke-dasharray:4,3"></line>
  <line x1="485" y1="460" x2="495" y2="460" marker-end="url(#arr-o)" style="stroke:#E65100; stroke-width:2.5; stroke-dasharray:4,3"></line>

  <!-- Latency label on interconnect -->
  <text x="450" y="510" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">~140 ns</text>
  <text x="450" y="527" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:12; text-anchor:middle">(2× slower!)</text>

  <!-- NUMA Node 1 -->
  <rect x="495" y="384" width="350" height="175" rx="8" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:2" />
  <text x="670" y="403" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">NUMA Node 1</text>

  <!-- CPU 1 cores -->
  <g filter="url(#sh)">
    <rect x="510" y="412" width="140" height="80" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  </g>
  <text x="580" y="432" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">CPU Socket 1</text>
  <rect x="518" y="443" width="55" height="22" rx="3" style="fill:#42A5F5" />
  <text x="545" y="458" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Core 8–11</text>
  <rect x="577" y="443" width="65" height="22" rx="3" style="fill:#42A5F5" />
  <text x="610" y="458" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:12; text-anchor:middle">Core 12–15</text>
  <text x="580" y="484" font-family="Arial,Helvetica,sans-serif" style="fill:#BDBDBD; font-size:12; text-anchor:middle">L3 Cache: 32 MB</text>

  <!-- Local Memory 1 -->
  <g filter="url(#sh)">
    <rect x="665" y="412" width="155" height="80" rx="6" style="fill:#00796B; stroke:#004D40; stroke-width:2" />
  </g>
  <text x="742" y="432" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Local Memory 1</text>
  <text x="742" y="452" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCC80; font-size:14; text-anchor:middle">128 GB DDR5</text>
  <rect x="673" y="460" width="139" height="22" rx="4" style="fill:#004D40" />
  <text x="742" y="475" font-family="Arial,Helvetica,sans-serif" style="fill:#4DB6AC; font-size:13; font-weight:bold; text-anchor:middle">Latency: ~70 ns ✓</text>

  <!-- Local access arrow -->
  <line x1="647" y1="452" x2="663" y2="452" marker-end="url(#arr-t)" style="stroke:#00796B; stroke-width:2.5"></line>
  <text x="655" y="446" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:11; text-anchor:middle">fast</text>

  <!-- Node 1 note -->
  <rect x="505" y="506" width="325" height="42" rx="5" style="fill:#fff; stroke:#1565C0; stroke-width:1" />
  <text x="667" y="521" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:12; font-weight:bold; text-anchor:middle">Remote access penalty:</text>
  <text x="667" y="540" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">CPU 0 accessing Memory 1 → 140 ns (2× latency)</text>

  <!-- Bottom summary -->
  <rect x="30" y="588" width="840" height="22" rx="5" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="450" y="604" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">
    Huge pages: 512× fewer TLB entries for 1 GB  |  NUMA: always allocate from local node to avoid 2× latency penalty
  </text>
</svg>
</div>
<figcaption><strong>Figure 2.7:</strong> Huge pages and NUMA: 2 MB huge
pages reduce TLB pressure by covering 512× more virtual address space
per entry; NUMA architecture places memory banks physically close to
specific CPU sockets, with cross-node accesses incurring 1.5–2× higher
latency.</figcaption>
</figure>

### 2.7.1 Huge Pages / Large Pages

Modern systems support multiple page sizes:

**Standard Pages:** 4 KB (x86-64)\
**Huge Pages:** 2 MB, 1 GB (x86-64)

**Benefits of Huge Pages:**

    Scenario: 1 GB memory region

    With 4 KB pages:
      - Pages needed: 262,144
      - TLB entries needed: 262,144 (won't fit!)
      - TLB misses: Constant

    With 2 MB pages:
      - Pages needed: 512
      - TLB entries needed: 512 (fits in L2 TLB)
      - TLB misses: Rare

    Performance improvement: 2-4Ã— for memory-intensive workloads

**Enabling Huge Pages (Linux):**

``` {.sourceCode .bash}
# Transparent Huge Pages (automatic)
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# Explicit huge pages
echo 1024 > /proc/sys/vm/nr_hugepages  # Allocate 1024 Ã— 2MB = 2GB
```

**Trade-offs:** - âœ" Fewer TLB misses - âœ" Smaller page tables - âœ---
More internal fragmentation - âœ--- Slower allocation (finding
contiguous 2 MB)

### 2.7.2 Memory Overcommitment

Linux allows allocating more virtual memory than physical RAM + swap:

``` {.sourceCode .bash}
# Check overcommit mode
cat /proc/sys/vm/overcommit_memory
# 0: Heuristic (default)
# 1: Always allow
# 2: Never overcommit (strict accounting)

# Example: System with 16 GB RAM, 8 GB swap
# Can allocate 100 GB virtual memory if overcommit=1
# OS assumes not all will be used simultaneously
```

**Risk:** If all processes actually use their allocated memory, OOM
killer activates.

### 2.7.3 NUMA (Non-Uniform Memory Access)

Modern multi-socket servers have NUMA:

    CPU 0 â†fastâ†’ Memory 0
      â†“slow
    CPU 1 â†fastâ†’ Memory 1

    Accessing local memory: 70 ns
    Accessing remote memory: 140 ns (2Ã— slower)

**NUMA-Aware Allocation:**

``` {.sourceCode .c}
// Linux: Allocate memory on local node
void *ptr = numa_alloc_local(size);

// Pin thread to CPU 0 and allocate from Node 0
numa_run_on_node(0);
void *ptr = malloc(size);  // Allocated from Node 0
```

------------------------------------------------------------------------

## 2.8 Performance Optimization Strategies

### 2.8.1 Reduce Page Faults

**Technique 1: Improve Locality**

``` {.sourceCode .c}
// Bad: Column-major access (poor locality)
for (int j = 0; j < N; j++) {
    for (int i = 0; i < N; i++) {
        sum += matrix[i][j];  // Jumps between pages
    }
}

// Good: Row-major access (good locality)
for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
        sum += matrix[i][j];  // Sequential within pages
    }
}
```

**Technique 2: Use mlock() for Critical Pages**

``` {.sourceCode .c}
// Prevent page from being swapped out
void *critical_data = malloc(size);
mlock(critical_data, size);  // Lock in RAM
// Guaranteed to never page fault
```

**Technique 3: Prefetch**

``` {.sourceCode .c}
// GCC built-in
__builtin_prefetch(&data[i + 64], 0, 3);  // Prefetch for reading
```

### 2.8.2 Monitor Performance

**Linux Tools:**

``` {.sourceCode .bash}
# Page fault statistics
ps -o min_flt,maj_flt,cmd -p <pid>
# min_flt: Minor faults (page in cache)
# maj_flt: Major faults (from disk)

# System-wide memory stats
vmstat 1

# Detailed process memory map
pmap -X <pid>

# Memory profiling with perf
perf stat -e page-faults,minor-faults,major-faults ./program
```

------------------------------------------------------------------------

## 2.9 Chapter Summary

**Key Concepts:**

1.  **Demand Paging:** Pages loaded from disk only when accessed,
    enabling programs larger than physical RAM.

2.  **Page Replacement:** When memory is full, OS must choose which page
    to evict. Clock algorithm offers best practical performance.

3.  **Thrashing:** Occurs when system spends more time swapping than
    executing. Prevented by limiting active processes to those whose
    working sets fit in RAM.

4.  **Copy-on-Write:** Efficient fork() implementation that shares pages
    until written, making process creation 500Ã--- faster.

5.  **Memory-Mapped Files:** Map files directly into address space,
    simplifying I/O and enabling zero-copy access.

6.  **Huge Pages:** Reduce TLB misses for memory-intensive workloads
    (2-4Ã--- speedup).

**Performance Principles:**

- Page faults to disk are catastrophically expensive (10,000Ã--- slower
  than DRAM)
- Locality of reference is crucial for performance
- Working set must fit in physical RAM to avoid thrashing
- Modern OSes use sophisticated algorithms (Clock, working set) to
  minimize page faults

**Real-World Impact:**

These virtual memory techniques enable: - Running dozens of programs on
limited RAM - Instant process creation (`fork()`) - Efficient large file
processing - Shared libraries saving gigabytes of memory - Databases
performing well with files larger than RAM

------------------------------------------------------------------------

## 2.10 Looking Ahead

**Chapter 3** will explore how these concepts are implemented in
hardware: - Page table structures (single-level, multi-level,
inverted) - Translation Lookaside Buffer (TLB) architecture - Hardware
page table walkers - Different architectures' approaches (x86, ARM,
RISC-V)

**Chapter 4** will cover OS-specific implementations: - Linux memory
management (`mm_struct`, page allocator, kswapd) - Windows memory
manager - How OSes coordinate with MMU hardware

------------------------------------------------------------------------

## References

1.  **Denning, P. J. (1968)**. "The working set model for program
    behavior". *Communications of the ACM*, 11(5), 323-333.

2.  **Denning, P. J. (1970)**. "Virtual memory". *Computing Surveys*,
    2(3), 153-189.

3.  **Belady, L. A. (1966)**. "A study of replacement algorithms for
    virtual-storage computer". *IBM Systems Journal*, 5(2), 78-101.

4.  **Aho, A. V., Denning, P. J., & Ullman, J. D. (1971)**. "Principles
    of optimal page replacement". *Journal of the ACM*, 18(1), 80-93.

5.  **Bhattacharjee, A., & Lustig, D. (2017)**. *Architectural and
    Operating System Support for Virtual Memory*. Morgan & Claypool.

6.  **Gorman, M. (2004)**. *Understanding the Linux Virtual Memory
    Manager*. Prentice Hall.

7.  **Love, R. (2010)**. *Linux Kernel Development* (3rd ed.).
    Addison-Wesley. Chapter 15: The Page Cache and Page Writeback.

------------------------------------------------------------------------

*Next Chapter: Page Table Structures and TLB Architecture - Hardware
implementation of address translation.*
