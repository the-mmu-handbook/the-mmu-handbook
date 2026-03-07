---
nav_exclude: true
sitemap: false
---

::: {#title-block-header}
# Chapter 1: Memory Management Basics {#chapter-1-memory-management-basics .title}
:::

- [Part I: Introduction and
  Fundamentals](#part-i-introduction-and-fundamentals){#toc-part-i-introduction-and-fundamentals}
- [Chapter 1: Memory Management
  Basics](#chapter-1-memory-management-basics){#toc-chapter-1-memory-management-basics}
  - [1.1 Introduction: Why Virtual Memory
    Exists](#introduction-why-virtual-memory-exists){#toc-introduction-why-virtual-memory-exists}
    - [The Programming Model We Take for
      Granted](#the-programming-model-we-take-for-granted){#toc-the-programming-model-we-take-for-granted}
    - [What Virtual Memory
      Provides](#what-virtual-memory-provides){#toc-what-virtual-memory-provides}
    - [The Core Mechanism: Address
      Translation](#the-core-mechanism-address-translation){#toc-the-core-mechanism-address-translation}
    - [Why Two Address Spaces Solve
      Everything](#why-two-address-spaces-solve-everything){#toc-why-two-address-spaces-solve-everything}
    - [The Memory Management Unit
      (MMU)](#the-memory-management-unit-mmu){#toc-the-memory-management-unit-mmu}
    - [The Three Fundamental
      Challenges](#the-three-fundamental-challenges){#toc-the-three-fundamental-challenges}
    - [What This Chapter
      Covers](#what-this-chapter-covers){#toc-what-this-chapter-covers}
  - [1.2 What is Memory
    Management?](#what-is-memory-management){#toc-what-is-memory-management}
    - [1.2.1 The Four Pillars of Memory
      Management](#the-four-pillars-of-memory-management){#toc-the-four-pillars-of-memory-management}
  - [1.3 The Evolution of Memory
    Management](#the-evolution-of-memory-management){#toc-the-evolution-of-memory-management}
    - [1.3.1 Early Systems: No Memory Management
      (1940s-1950s)](#early-systems-no-memory-management-1940s-1950s){#toc-early-systems-no-memory-management-1940s-1950s}
    - [1.3.2 Base and Bounds Registers
      (1960s)](#base-and-bounds-registers-1960s){#toc-base-and-bounds-registers-1960s}
    - [1.3.3 Segmentation
      (1960s-1970s)](#segmentation-1960s-1970s){#toc-segmentation-1960s-1970s}
    - [1.3.4 Paging: The Modern Solution
      (1960s-Present)](#paging-the-modern-solution-1960s-present){#toc-paging-the-modern-solution-1960s-present}
    - [Understanding Fragmentation: Visual
      Examples](#understanding-fragmentation-visual-examples){#toc-understanding-fragmentation-visual-examples}
  - [1.4 Hierarchical Levels of Memory
    Management](#hierarchical-levels-of-memory-management){#toc-hierarchical-levels-of-memory-management}
    - [1.4.1 Hardware Level: The Memory Management Unit
      (MMU)](#hardware-level-the-memory-management-unit-mmu){#toc-hardware-level-the-memory-management-unit-mmu}
    - [1.4.2 Operating System Level: The Virtual Memory
      Manager](#operating-system-level-the-virtual-memory-manager){#toc-operating-system-level-the-virtual-memory-manager}
    - [1.4.3 Application Level: Memory Allocation
      Libraries](#application-level-memory-allocation-libraries){#toc-application-level-memory-allocation-libraries}
  - [1.5 The Virtual Memory
    Abstraction](#the-virtual-memory-abstraction){#toc-the-virtual-memory-abstraction}
    - [1.5.1 Benefits of Virtual
      Memory](#benefits-of-virtual-memory){#toc-benefits-of-virtual-memory}
    - [1.5.2 The Cost of Virtual
      Memory](#the-cost-of-virtual-memory){#toc-the-cost-of-virtual-memory}
  - [1.6 Key Concepts and
    Terminology](#key-concepts-and-terminology){#toc-key-concepts-and-terminology}
    - [Address Spaces](#address-spaces){#toc-address-spaces}
    - [Pages and Frames](#pages-and-frames){#toc-pages-and-frames}
    - [Page Tables](#page-tables){#toc-page-tables}
    - [Page States](#page-states){#toc-page-states}
    - [Memory Operations](#memory-operations){#toc-memory-operations}
  - [1.7 A Concrete Example: Address
    Translation](#a-concrete-example-address-translation){#toc-a-concrete-example-address-translation}
  - [1.8 The Translation Lookaside Buffer
    (TLB)](#the-translation-lookaside-buffer-tlb){#toc-the-translation-lookaside-buffer-tlb}
  - [1.9 Multi-Level Page
    Tables](#multi-level-page-tables){#toc-multi-level-page-tables}
  - [1.10 Why MMU Matters: Real-World
    Impact](#why-mmu-matters-real-world-impact){#toc-why-mmu-matters-real-world-impact}
    - [Case Study 1: The Cost of TLB
      Misses](#case-study-1-the-cost-of-tlb-misses){#toc-case-study-1-the-cost-of-tlb-misses}
    - [Case Study 2: Spectre and
      Meltdown](#case-study-2-spectre-and-meltdown){#toc-case-study-2-spectre-and-meltdown}
    - [Case Study 3:
      Rowhammer](#case-study-3-rowhammer){#toc-case-study-3-rowhammer}
  - [1.11 Looking Ahead](#looking-ahead){#toc-looking-ahead}
  - [1.12 Chapter Summary](#chapter-summary){#toc-chapter-summary}
  - [References and Further
    Reading](#references-and-further-reading){#toc-references-and-further-reading}

# Part I: Introduction and Fundamentals

# Chapter 1: Memory Management Basics {#chapter-1-memory-management-basics}

> *\"The memory hierarchy is a fundamental structure in computer
> architecture, and virtual memory is one of the greatest ideas in
> computer science.\"*\
> \-- John L. Hennessy & David A. Patterson, Computer Architecture: A
> Quantitative Approach

## 1.1 Introduction: Why Virtual Memory Exists

### The Programming Model We Take for Granted

When you write a program in C, Python, or any modern language, you make
several assumptions about memory:

1.  Your program can use memory addresses starting from 0
2.  Memory appears as one large, contiguous space
3.  Other programs won\'t interfere with your memory
4.  You can use more memory than physically available (within limits)
5.  The program works the same regardless of how much RAM the computer
    has

These assumptions seem natural, but they\'re not inherent to computer
hardware. They\'re provided by **virtual memory**\--one of computer
science\'s most important abstractions \[Bhattacharjee & Lustig, 2017\].

### What Virtual Memory Provides

Virtual memory (VM) is the hardware and software mechanism that gives
each program its own **private view** of the computer\'s memory.
According to Bhattacharjee & Lustig (2017), virtual memory provides
several critical benefits:

**1. Simplified Programming (Abstraction)** - Programs use simple
addresses starting from 0 - No need to know physical memory size or
layout - Memory appears as one large array - Code is portable across
different hardware

**2. Memory Protection and Isolation** - Each program has its own
address space - Programs cannot access each other\'s memory - Operating
system memory is protected from user programs - Security: malicious code
can\'t read passwords from other programs

**3. Memory Overcommitment** - Total virtual memory across all programs
can exceed physical RAM - Programs can use address spaces larger than
physical memory - Inactive data can be stored on disk - Efficient memory
sharing between programs

**4. Flexibility in Memory Allocation** - Programs can be loaded
anywhere in physical memory - Memory doesn\'t need to be contiguous in
physical RAM - Easy to relocate programs - Simplifies dynamic memory
allocation

### The Core Mechanism: Address Translation

Virtual memory works through **address translation**. Let\'s understand
this with a concrete example:

``` {.sourceCode .c}
int main() {
    int x = 42;
    printf("Address of x: %p\n", &x);  
    // Might print: 0x7ffe5c3d4a8c
    return 0;
}
```

When you run this program, it prints an address like `0x7ffe5c3d4a8c`.
This is a **virtual address**\--a number your program uses to refer to a
memory location. But this is not where `x` actually lives in the
physical RAM chips.

**Two Types of Addresses:**

**Virtual Address (VA)** - What your program sees and uses - Example:
`0x7ffe5c3d4a8c` - Every program has its own virtual addresses starting
from 0 - Abstract, not tied to physical hardware

**Physical Address (PA)**\
- Where data actually resides in RAM chips - Example: `0x12A4B000`
(completely different!) - Only one set of physical addresses in the
entire system - Corresponds to actual hardware locations

**The Translation:**

When your program accesses virtual address `0x7ffe5c3d4a8c`, hardware
automatically translates it to the corresponding physical address (say,
`0x12A4B000`) where your data actually lives.

    Program's view:         Virtual Address 0x7ffe5c3d4a8c
                                      ↓
                            [MMU Translation]
                                      ↓
    Reality in hardware:    Physical Address 0x12A4B000

### Why Two Address Spaces Solve Everything

This simple translation mechanism simultaneously solves all the problems
mentioned above:

**Isolation:** Program A\'s virtual address `0x1000` maps to physical
address `0x3A2F1000`. Program B\'s virtual address `0x1000` maps to
physical address `0x91B52000`. Same virtual address, different physical
locations\--they can never conflict.

**Simplification:** Every program uses addresses starting from 0. The
program doesn\'t need to know where it\'s actually loaded in physical
memory.

**Overcommitment:** A program can have virtual addresses from 0 to 4
billion (on 32-bit systems), even if physical RAM is only 2 GB. Not all
virtual addresses need to be in physical memory simultaneously\--some
can be on disk.

**Protection:** The translation mechanism includes permission checks.
The hardware verifies that your program is allowed to access each
physical address it translates to.

### The Memory Management Unit (MMU)

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="980" height="680" viewBox="0 0 980 680" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
    <marker id="aspd" markerwidth="8" markerheight="6" refx="7" refy="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" style="fill:#1565C0"></polygon>
    </marker>
  </defs>
  <rect width="980" height="680" style="fill:#FAFAFA" />
  <text x="120" y="36" style="fill:#212121; font-size:20; font-weight:bold">Memory Hierarchy: Size, Speed, and Latency Trade-offs</text>

  <!-- Column headers -->
  <text x="370" y="68" style="fill:#616161; font-size:14; font-weight:bold; text-anchor:middle">Memory Level</text>
  <text x="680" y="68" style="fill:#616161; font-size:14; font-weight:bold; text-anchor:middle">Typical Size</text>
  <text x="860" y="68" style="fill:#616161; font-size:14; font-weight:bold; text-anchor:middle">Access Latency</text>
  <line x1="620" y1="52" x2="620" y2="585" style="stroke:#9E9E9E; stroke-width:1; stroke-dasharray:4,3"></line>
  <line x1="780" y1="52" x2="780" y2="585" style="stroke:#9E9E9E; stroke-width:1; stroke-dasharray:4,3"></line>

  <!-- Registers -->
  <rect x="290" y="78" width="160" height="50" rx="6" filter="url(#sh)" style="fill:#1565C0" />
  <text x="370" y="107" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">CPU Registers</text>
  <text x="680" y="107" style="fill:#212121; font-size:14; text-anchor:middle">16 – 256 bytes</text>
  <text x="860" y="107" style="fill:#212121; font-size:14; text-anchor:middle">0 cycles (instant)</text>
  <line x1="370" y1="128" x2="370" y2="142" style="stroke:#BDBDBD; stroke-width:2"></line>
  <polygon points="364,140 376,140 370,148" style="fill:#BDBDBD"></polygon>

  <!-- L1 -->
  <rect x="260" y="150" width="220" height="52" rx="6" filter="url(#sh)" style="fill:#1565C0; opacity:0.84" />
  <text x="370" y="178" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">L1 Cache</text>
  <text x="370" y="195" style="fill:#BBDEFB; font-size:12; text-anchor:middle">Per-core, split I$ + D$</text>
  <text x="680" y="181" style="fill:#212121; font-size:14; text-anchor:middle">32 KB – 64 KB</text>
  <text x="860" y="181" style="fill:#212121; font-size:14; text-anchor:middle">4 cycles (~1 ns)</text>
  <line x1="370" y1="202" x2="370" y2="216" style="stroke:#BDBDBD; stroke-width:2"></line>
  <polygon points="364,214 376,214 370,222" style="fill:#BDBDBD"></polygon>

  <!-- L2 -->
  <rect x="222" y="224" width="296" height="52" rx="6" filter="url(#sh)" style="fill:#00796B" />
  <text x="370" y="252" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">L2 Cache</text>
  <text x="370" y="268" style="fill:#B2DFDB; font-size:12; text-anchor:middle">Unified, per-core or shared</text>
  <text x="680" y="255" style="fill:#212121; font-size:14; text-anchor:middle">256 KB – 1 MB</text>
  <text x="860" y="255" style="fill:#212121; font-size:14; text-anchor:middle">12 cycles (~4 ns)</text>
  <line x1="370" y1="276" x2="370" y2="290" style="stroke:#BDBDBD; stroke-width:2"></line>
  <polygon points="364,288 376,288 370,296" style="fill:#BDBDBD"></polygon>

  <!-- L3 -->
  <rect x="178" y="298" width="384" height="52" rx="6" filter="url(#sh)" style="fill:#00796B; opacity:0.78" />
  <text x="370" y="326" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">L3 Cache (LLC)</text>
  <text x="370" y="342" style="fill:#B2DFDB; font-size:12; text-anchor:middle">Shared across all cores</text>
  <text x="680" y="329" style="fill:#212121; font-size:14; text-anchor:middle">8 MB – 64 MB</text>
  <text x="860" y="329" style="fill:#212121; font-size:14; text-anchor:middle">40 cycles (~14 ns)</text>
  <line x1="370" y1="350" x2="370" y2="364" style="stroke:#BDBDBD; stroke-width:2"></line>
  <polygon points="364,362 376,362 370,370" style="fill:#BDBDBD"></polygon>

  <!-- DRAM -->
  <rect x="136" y="372" width="468" height="54" rx="6" filter="url(#sh)" style="fill:#757575" />
  <rect x="136" y="380" width="468" height="8" style="fill:#9E9E9E" />
  <rect x="136" y="396" width="468" height="8" style="fill:#9E9E9E" />
  <rect x="136" y="412" width="468" height="8" style="fill:#9E9E9E" />
  <rect x="136" y="372" width="468" height="54" rx="6" style="fill:none; stroke:#424242; stroke-width:1.5" />
  <text x="370" y="399" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">Main Memory (DRAM)</text>
  <text x="370" y="416" style="fill:#E0E0E0; font-size:12; text-anchor:middle">DDR4 / DDR5 / LPDDR5</text>
  <text x="680" y="402" style="fill:#212121; font-size:14; text-anchor:middle">8 GB – 512 GB</text>
  <text x="860" y="402" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">200 cycles (~70 ns)</text>
  <line x1="370" y1="426" x2="370" y2="440" style="stroke:#BDBDBD; stroke-width:2"></line>
  <polygon points="364,438 376,438 370,446" style="fill:#BDBDBD"></polygon>

  <!-- SSD -->
  <rect x="112" y="448" width="490" height="50" rx="6" filter="url(#sh)" style="fill:#424242" />
  <text x="357" y="475" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">SSD / NVMe (Swap and Files)</text>
  <text x="357" y="491" style="fill:#BDBDBD; font-size:12; text-anchor:middle">Virtual memory backing store</text>
  <text x="680" y="477" style="fill:#212121; font-size:14; text-anchor:middle">256 GB – 8 TB</text>
  <text x="860" y="477" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">25 μs (25,000 cycles)</text>
  <line x1="370" y1="498" x2="370" y2="512" style="stroke:#BDBDBD; stroke-width:2"></line>
  <polygon points="364,510 376,510 370,518" style="fill:#BDBDBD"></polygon>

  <!-- HDD -->
  <rect x="112" y="520" width="490" height="40" rx="6" filter="url(#sh)" style="fill:#212121" />
  <text x="357" y="544" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">Hard Disk Drive (HDD)</text>
  <text x="680" y="544" style="fill:#212121; font-size:14; text-anchor:middle">1 TB – 20 TB</text>
  <text x="860" y="544" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">10 ms (10M cycles)</text>

  <!-- Speed/Size arrow — x=90, giving clear left margin -->
  <line x1="90" y1="565" x2="90" y2="85" marker-end="url(#aspd)" style="stroke:#1565C0; stroke-width:2.5"></line>
  <!-- Rotated label centered vertically along the arrow at x=74 -->
  <text x="74" y="375" transform="rotate(-90,74,375)" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:middle">Faster / Smaller / More Expensive</text>

  <!-- Insight box — properly bounded, clear margins all sides -->
  <rect x="630" y="575" width="330" height="90" rx="6" filter="url(#sh)" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="795" y="598" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">The Memory Wall</text>
  <line x1="645" y1="607" x2="945" y2="607" style="stroke:#E65100; stroke-width:1; stroke-dasharray:3,3"></line>
  <text x="795" y="624" style="fill:#212121; font-size:13; text-anchor:middle">CPU ~0.3 ns/cycle vs DRAM ~70 ns.</text>
  <text x="795" y="644" style="fill:#212121; font-size:13; text-anchor:middle">Every cache miss wastes ~280 CPU cycles.</text>
</svg>
</div>
<figcaption><strong>Figure 1.1:</strong> Memory hierarchy: CPU registers
to persistent storage with typical latencies and capacities at each
level.</figcaption>
</figure>

The **Memory Management Unit (MMU)** is the hardware component inside
your CPU that performs this translation. On every memory
access\--billions of times per second\--the MMU:

1.  Receives a virtual address from the program
2.  Translates it to the corresponding physical address
3.  Checks if the access is allowed (read/write/execute permissions)
4.  Either completes the access or triggers an exception

This happens automatically and transparently. Your program never knows
it\'s using virtual addresses.

### The Three Fundamental Challenges

While virtual memory elegantly solves programming and protection
problems, it introduces new challenges that the MMU must address:

**Challenge 1: Translation Performance** - Modern CPUs execute \~4
billion instructions per second - Many instructions access memory
multiple times - That\'s billions of translations per second - Each
translation must be fast (sub-nanosecond) or the CPU stalls

**Challenge 2: Translation Overhead** - Translation requires looking up
tables in memory - But those table lookups themselves require memory
access - This could create infinite recursion - The translation
mechanism itself consumes memory

**Challenge 3: The Memory Wall** - Memory access takes \~70
nanoseconds - During that time, CPU could execute 280 instructions -
Most CPU time is spent waiting for memory - Virtual memory must not make
this worse

**How These Are Solved:** - **Translation Lookaside Buffer (TLB)**: A
cache that remembers recent translations, making most translations
instant - **Hardware Page Table Walker**: Dedicated logic to quickly
traverse translation tables - **Multi-level page tables**: Hierarchical
structure that reduces memory overhead - **Large pages**: Reducing the
number of translations needed

### What This Chapter Covers

Understanding virtual memory requires understanding the interplay
between hardware and software:

**Hardware (MMU):** - How address translation works (page tables) - How
to make translation fast (TLBs, page table walkers) - Different
architectures\' approaches (x86, ARM, RISC-V)

**Operating System:** - Managing page tables for all processes -
Handling page faults (when data isn\'t in RAM) - Deciding what to keep
in physical memory - Implementing memory protection policies

**Together:** - How hardware and OS cooperate - Performance
implications - Security considerations - Modern challenges and solutions

By the end of this chapter, you\'ll understand how modern computers
provide every program with the illusion of having abundant, fast,
private memory\--even though physical memory is limited, slow, and
shared.

------------------------------------------------------------------------

## 1.2 What is Memory Management?

Given the fundamental challenges outlined above\--the memory wall,
capacity limitations, and security requirements\--memory management is
the collection of hardware and software mechanisms that bridge the gap
between what programmers need (fast, large, secure memory) and what
hardware provides (slow, limited, shared physical RAM).

At its core, memory management must simultaneously solve several
competing challenges:

### 1.2.1 The Four Pillars of Memory Management

#### 1. **Allocation and Deallocation**

Every program requires memory to store instructions and data. When a
process starts, memory must be allocated. When it terminates, that
memory must be reclaimed.

**The Challenge:** How do we allocate memory efficiently when programs
have unpredictable memory needs? How do we avoid fragmentation? What
happens when physical memory is exhausted?

**Example: The malloc() Mystery**

``` {.sourceCode .c}
int* ptr = malloc(1024 * 1024 * 1024);  // Request 1 GB
if (ptr != NULL) {
    printf("Allocation succeeded!\n");
    // But have we actually allocated 1 GB of physical RAM?
}
```

Surprisingly, on most modern systems, `malloc()` will succeed even if
you only have 512 MB of physical RAM available. How is this possible?
The answer lies in *virtual memory* and *demand paging*\--concepts
we\'ll explore in depth.

#### 2. **Address Translation**

Programs operate using *virtual addresses* (also called logical
addresses), but the actual data resides at *physical addresses* in RAM.
The Memory Management Unit (MMU) performs this translation billions of
times per second.

**The Challenge:** How do we translate addresses quickly enough to avoid
becoming a bottleneck? How do we handle the translation table itself,
which might be enormous?

**Concrete Example:**

    Virtual Address:  0x7fff5fbff710  (Program's view)
    Physical Address: 0x3a2f1000      (Actual RAM location)

The MMU must perform this translation for *every single memory access*.
On a modern CPU executing billions of instructions per second, with
multiple memory accesses per instruction, this means billions of
translations per second.

#### 3. **Protection and Isolation**

In a multitasking system, one misbehaving program must not be able to
corrupt another program\'s memory\--or worse, the operating system
kernel\'s memory.

**Historical Perspective:**\
Early microcomputers like the Commodore 64 and Apple II had no memory
protection. A single buggy program could crash the entire system. Modern
systems enforce strict isolation.

**The Challenge:** How do we enforce protection without sacrificing
performance? How do we share memory safely when needed (e.g., shared
libraries)?

**Real-World Impact:** The 2018 Spectre and Meltdown vulnerabilities
demonstrated that even with hardware memory protection, subtle CPU
implementation details could leak protected memory. These
vulnerabilities affected billions of devices and showed that memory
isolation is harder than it appears \[Kocher et al., 2019; Lipp et al.,
2018\].

#### 4. **Optimization**

Memory management must be fast. Every optimization matters: better cache
utilization, reduced TLB misses, efficient page table structures, and
intelligent page replacement algorithms.

**The Challenge:** How do we balance competing goals? Larger pages
reduce translation overhead but increase internal fragmentation. More
complex page tables enable features but consume memory themselves.

**Performance Reality:**

To understand why memory management is critical, consider the real cost
of different memory operations. These numbers come from actual hardware
measurements on a modern Intel Xeon processor:

    Operation                        Latency          CPU Cycles (@4GHz)    Human Scale*
    L1 Cache Hit                     ~0.5 ns          ~2 cycles             1 second
    L2 Cache Hit                     ~3 ns            ~12 cycles            6 seconds
    L3 Cache Hit                     ~12 ns           ~50 cycles            24 seconds
    DRAM Access (TLB hit)            ~70 ns           ~280 cycles           2.3 minutes
    DRAM Access (TLB miss)           ~150 ns          ~600 cycles           5 minutes
    Page Fault (from SSD)            ~25,000 ns       ~100,000 cycles       1.2 days
    Page Fault (from HDD)            ~10,000,000 ns   ~40,000,000 cycles    1.3 years

*Table 1.1: Memory hierarchy latencies. Human scale shows the relative
time if L1 cache = 1 second.*

**Understanding the Scale:**\
If an L1 cache access took 1 second, a page fault from a hard drive
would take over a year. This isn\'t a small performance penalty\--it\'s
the difference between a responsive system and one that appears frozen.

**Why the Memory Wall Matters:**\
The memory wall means that for many applications, performance is
dominated not by CPU speed but by memory access patterns. Programs with
good locality (accessing nearby memory addresses) stay in fast caches.
Programs with poor locality constantly miss caches and TLBs, spending
most of their time waiting for slow DRAM.

Sources: Latency measurements from Hennessy & Patterson (2024), Intel
Xeon performance guides, and empirical testing.

------------------------------------------------------------------------

## 1.3 The Evolution of Memory Management

### 1.3.1 Early Systems: No Memory Management (1940s-1950s)

The earliest computers like ENIAC and EDVAC had no memory management.
Programs had direct access to all physical memory. Only one program
could run at a time.

**Programming Model:**

``` assembly
; PDP-8 example (1965)
; Direct physical addressing - no translation
0200:  7200    CLA      ; Clear accumulator  
0201:  1234    TAD 234  ; Load from absolute address 234
0202:  3456    DCA 456  ; Store to absolute address 456
```

**Limitations:** - No multitasking - No protection - Manual memory
layout by programmer - Physical memory size limited program size

### 1.3.2 Base and Bounds Registers (1960s)

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
    <marker id="ab" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="ao" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
    <marker id="at" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker>
  </defs>
  <rect width="900" height="560" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Base and Bounds Address Translation (1960s Era)</text>

  <!-- CPU -->
  <rect x="30" y="70" width="155" height="90" rx="6" filter="url(#sh)" style="fill:#1565C0" />
  <text x="107" y="100" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">CPU / Program</text>
  <text x="107" y="120" style="fill:#BBDEFB; font-size:13; text-anchor:middle">Logical address:</text>
  <text x="107" y="138" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">0x2000</text>

  <!-- Arrow CPU -> Adder -->
  <line x1="185" y1="115" x2="295" y2="195" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:2.5"></line>
  <text x="218" y="145" style="fill:#1565C0; font-size:13; font-weight:bold">Logical Addr</text>

  <!-- Base Register -->
  <rect x="30" y="240" width="155" height="70" rx="6" filter="url(#sh)" style="fill:#00796B" />
  <text x="107" y="268" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">Base Register</text>
  <text x="107" y="288" style="fill:#B2DFDB; font-size:14; text-anchor:middle">0x10000</text>
  <text x="107" y="304" style="fill:#B2DFDB; font-size:12; text-anchor:middle">program start in RAM</text>

  <!-- Arrow Base -> Adder -->
  <line x1="185" y1="270" x2="295" y2="235" marker-end="url(#at)" style="stroke:#00796B; stroke-width:2.5"></line>
  <text x="198" y="263" style="fill:#00796B; font-size:13">+ Base value</text>

  <!-- Adder -->
  <rect x="298" y="185" width="118" height="80" rx="6" filter="url(#sh)" style="fill:#1565C0" />
  <text x="357" y="218" style="fill:#FFFFFF; font-size:26; font-weight:bold; text-anchor:middle">+</text>
  <text x="357" y="245" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">ADDER</text>
  <text x="357" y="260" style="fill:#BBDEFB; font-size:12; text-anchor:middle">hardware unit</text>

  <!-- Arrow Adder -> Checker -->
  <line x1="416" y1="225" x2="478" y2="225" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:2.5"></line>
  <text x="420" y="218" style="fill:#424242; font-size:12">Phys: 0x12000</text>

  <!-- Bounds Register -->
  <rect x="298" y="360" width="160" height="70" rx="6" filter="url(#sh)" style="fill:#E65100" />
  <text x="378" y="388" style="fill:#FFFFFF; font-size:15; font-weight:bold; text-anchor:middle">Bounds Register</text>
  <text x="378" y="408" style="fill:#FFCCBC; font-size:14; text-anchor:middle">Limit: 0x8000</text>
  <text x="378" y="424" style="fill:#FFCCBC; font-size:12; text-anchor:middle">max program size</text>

  <!-- Arrow Bounds -> Checker -->
  <line x1="378" y1="360" x2="510" y2="300" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2; stroke-dasharray:6,3"></line>
  <text x="400" y="344" style="fill:#E65100; font-size:12">Addr &lt; Limit?</text>

  <!-- Bounds Checker -->
  <rect x="480" y="170" width="158" height="120" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />
  <text x="559" y="198" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Bounds Check</text>
  <line x1="492" y1="208" x2="626" y2="208" style="stroke:#BDBDBD; stroke-width:1"></line>
  <text x="559" y="228" style="fill:#212121; font-size:13; text-anchor:middle">0x2000 &lt; 0x8000?</text>
  <text x="559" y="252" style="fill:#2E7D32; font-size:20; font-weight:bold; text-anchor:middle">YES</text>
  <text x="559" y="275" style="fill:#212121; font-size:13; text-anchor:middle">Access permitted</text>

  <!-- Arrow Checker -> Memory (good) -->
  <line x1="638" y1="225" x2="718" y2="225" marker-end="url(#at)" style="stroke:#00796B; stroke-width:2.5"></line>

  <!-- Physical Memory -->
  <rect x="722" y="155" width="150" height="175" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />
  <rect x="730" y="163" width="134" height="9" style="fill:#E0E0E0" />
  <rect x="730" y="180" width="134" height="9" style="fill:#E0E0E0" />
  <rect x="730" y="197" width="134" height="9" style="fill:#E0E0E0" />
  <text x="797" y="228" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Physical Memory</text>
  <rect x="730" y="238" width="134" height="44" rx="4" style="fill:#00796B" />
  <text x="797" y="261" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">0x12000</text>
  <text x="797" y="276" style="fill:#B2DFDB; font-size:12; text-anchor:middle">Target location</text>
  <rect x="730" y="288" width="134" height="30" rx="4" style="fill:#BDBDBD" />
  <text x="797" y="308" style="fill:#616161; font-size:12; text-anchor:middle">other processes</text>

  <!-- Fault path -->
  <rect x="480" y="400" width="200" height="65" rx="6" filter="url(#sh)" style="fill:#B71C1C" />
  <text x="580" y="426" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Protection Fault!</text>
  <text x="580" y="446" style="fill:#FFCDD2; font-size:13; text-anchor:middle">Addr &gt;= Limit: Trap to OS</text>
  <text x="580" y="462" style="fill:#FFCDD2; font-size:13; text-anchor:middle">Process terminated</text>

  <!-- Arrow checker -> fault -->
  <line x1="559" y1="290" x2="559" y2="400" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2.5; stroke-dasharray:6,3"></line>
  <text x="570" y="355" style="fill:#E65100; font-size:13; font-weight:bold">NO (violation)</text>

  <!-- Annotation box -->
  <rect x="30" y="380" width="252" height="110" rx="6" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="156" y="400" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Example Calculation</text>
  <text x="44" y="420" style="fill:#212121; font-size:13">Base   = 0x10000  (program loaded here)</text>
  <text x="44" y="438" style="fill:#212121; font-size:13">Limit  = 0x8000   (program is 32 KB)</text>
  <text x="44" y="456" style="fill:#212121; font-size:13">Logical= 0x2000   (within program)</text>
  <text x="44" y="478" style="fill:#00796B; font-size:13; font-weight:bold">Physical = 0x10000 + 0x2000 = 0x12000</text>

  <!-- Limitation note -->
  <rect x="698" y="378" width="182" height="100" rx="6" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="789" y="398" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Limitations</text>
  <text x="710" y="418" style="fill:#212121; font-size:12">- No memory sharing</text>
  <text x="710" y="436" style="fill:#212121; font-size:12">- External fragmentation</text>
  <text x="710" y="454" style="fill:#212121; font-size:12">- Program must be contiguous</text>
  <text x="710" y="472" style="fill:#212121; font-size:12">- Replaced by paging (1970s+)</text>
</svg>
</div>
<figcaption><strong>Figure 1.2:</strong> Base-and-bounds translation:
the CPU adds the base register to the logical address; exceeding the
bounds register raises a protection fault.</figcaption>
</figure>

The first hardware memory management used simple *base and bounds*
registers. The base register contained the program\'s starting address,
and all memory accesses were offset from this base. The bounds register
limited the maximum offset.

    Physical Address = Base Register + Program Address

    if (Program Address > Bounds Register):
        TRAP to operating system  # Protection fault

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="500" viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter></defs>
  <rect width="900" height="500" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Base and Bounds: Three Worked Calculation Examples</text>

  <!-- Column headers -->
  <rect x="22" y="55" width="856" height="36" rx="4" style="fill:#1565C0" />
  <text x="130" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Logical Address</text>
  <text x="300" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Base Register</text>
  <text x="470" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Limit Register</text>
  <text x="640" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Check: Addr &lt; Limit?</text>
  <text x="810" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Result</text>

  <!-- Example 1: Valid access -->
  <rect x="22" y="91" width="856" height="80" rx="0" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:1.5" />
  <text x="130" y="115" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">0x2000</text>
  <text x="130" y="135" style="fill:#616161; font-size:12; text-anchor:middle">within program space</text>
  <text x="300" y="115" style="fill:#212121; font-size:14; text-anchor:middle">0x10000</text>
  <text x="300" y="135" style="fill:#616161; font-size:12; text-anchor:middle">program starts here</text>
  <text x="470" y="115" style="fill:#212121; font-size:14; text-anchor:middle">0x8000</text>
  <text x="470" y="135" style="fill:#616161; font-size:12; text-anchor:middle">32 KB program</text>
  <text x="640" y="115" style="fill:#2E7D32; font-size:14; font-weight:bold; text-anchor:middle">0x2000 &lt; 0x8000: YES</text>
  <text x="640" y="135" style="fill:#616161; font-size:12; text-anchor:middle">within bounds</text>
  <text x="810" y="108" style="fill:#2E7D32; font-size:13; font-weight:bold; text-anchor:middle">Physical = 0x12000</text>
  <text x="810" y="128" style="fill:#212121; font-size:13; text-anchor:middle">0x10000 + 0x2000</text>
  <text x="810" y="148" style="fill:#2E7D32; font-size:12; text-anchor:middle">Access ALLOWED</text>

  <!-- Example 2: Boundary edge valid -->
  <rect x="22" y="171" width="856" height="80" rx="0" style="fill:#FFF9C4; stroke:#F9A825; stroke-width:1.5" />
  <text x="130" y="195" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">0x7FFF</text>
  <text x="130" y="215" style="fill:#616161; font-size:12; text-anchor:middle">last valid byte</text>
  <text x="300" y="195" style="fill:#212121; font-size:14; text-anchor:middle">0x10000</text>
  <text x="300" y="215" style="fill:#616161; font-size:12; text-anchor:middle">same program</text>
  <text x="470" y="195" style="fill:#212121; font-size:14; text-anchor:middle">0x8000</text>
  <text x="470" y="215" style="fill:#616161; font-size:12; text-anchor:middle">32 KB program</text>
  <text x="640" y="195" style="fill:#F9A825; font-size:14; font-weight:bold; text-anchor:middle">0x7FFF &lt; 0x8000: YES</text>
  <text x="640" y="215" style="fill:#616161; font-size:12; text-anchor:middle">just barely in bounds</text>
  <text x="810" y="188" style="fill:#F9A825; font-size:13; font-weight:bold; text-anchor:middle">Physical = 0x17FFF</text>
  <text x="810" y="208" style="fill:#212121; font-size:13; text-anchor:middle">0x10000 + 0x7FFF</text>
  <text x="810" y="228" style="fill:#2E7D32; font-size:12; text-anchor:middle">Access ALLOWED</text>

  <!-- Example 3: Out of bounds violation -->
  <rect x="22" y="251" width="856" height="80" rx="0" style="fill:#FFEBEE; stroke:#B71C1C; stroke-width:1.5" />
  <text x="130" y="275" style="fill:#B71C1C; font-size:14; font-weight:bold; text-anchor:middle">0x9000</text>
  <text x="130" y="295" style="fill:#616161; font-size:12; text-anchor:middle">past end of program!</text>
  <text x="300" y="275" style="fill:#212121; font-size:14; text-anchor:middle">0x10000</text>
  <text x="300" y="295" style="fill:#616161; font-size:12; text-anchor:middle">same program</text>
  <text x="470" y="275" style="fill:#212121; font-size:14; text-anchor:middle">0x8000</text>
  <text x="470" y="295" style="fill:#616161; font-size:12; text-anchor:middle">32 KB program</text>
  <text x="640" y="275" style="fill:#B71C1C; font-size:14; font-weight:bold; text-anchor:middle">0x9000 &lt; 0x8000: NO!</text>
  <text x="640" y="295" style="fill:#616161; font-size:12; text-anchor:middle">access violation</text>
  <text x="810" y="268" style="fill:#B71C1C; font-size:14; font-weight:bold; text-anchor:middle">PROTECTION FAULT</text>
  <text x="810" y="288" style="fill:#212121; font-size:13; text-anchor:middle">Trap to OS</text>
  <text x="810" y="308" style="fill:#B71C1C; font-size:12; text-anchor:middle">Process killed</text>

  <!-- Formula -->
  <rect x="22" y="348" width="856" height="60" rx="6" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="438" y="372" style="fill:#1565C0; font-size:15; font-weight:bold; text-anchor:middle">Translation Formula</text>
  <text x="438" y="396" style="fill:#212121; font-size:14; text-anchor:middle">IF (Logical_Address &lt; Limit) THEN Physical_Address = Base + Logical_Address  ELSE raise ProtectionFault()</text>

  <!-- Key distinction vs paging -->
  <rect x="22" y="424" width="856" height="60" rx="6" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="438" y="448" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">Base-and-Bounds vs. Paging</text>
  <text x="438" y="470" style="fill:#212121; font-size:13; text-anchor:middle">Base-and-Bounds: Single contiguous region per process. Simple but causes external fragmentation. Replaced by paging in modern systems.</text>
</svg>
</div>
<figcaption><strong>Figure 1.3:</strong> Concrete base-and-bounds
calculation examples showing address mapping and bounds-violation
detection.</figcaption>
</figure>

**Example: IBM 7094 (1962)**

    Base:   0x100000
    Bounds: 0x010000  (64 KB limit)

    Program accesses: 0x1234
    Physical address: 0x100000 + 0x1234 = 0x101234 ✓ (within bounds)

    Program accesses: 0x20000  
    0x20000 > 0x010000 → PROTECTION FAULT

**Limitations:** - Still required contiguous physical memory -
Relocation required copying entire program in memory - External
fragmentation: gaps between programs - No sharing of code between
processes

### 1.3.3 Segmentation (1960s-1970s)

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="580" viewBox="0 0 900 580" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
    <marker id="ab" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="at" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker>
  </defs>
  <rect width="900" height="580" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Segmentation Architecture: Logical Segments to Physical Memory</text>

  <!-- Virtual Address breakdown -->
  <text x="30" y="72" style="fill:#212121; font-size:15; font-weight:bold">Virtual (Logical) Address Format:</text>
  <rect x="30" y="82" width="180" height="44" rx="4" style="fill:#1565C0" />
  <text x="120" y="100" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Segment ID</text>
  <text x="120" y="118" style="fill:#BBDEFB; font-size:13; text-anchor:middle">e.g., 2 bits = 4 segs</text>
  <rect x="210" y="82" width="300" height="44" rx="4" style="fill:#00796B" />
  <text x="360" y="100" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Offset within Segment</text>
  <text x="360" y="118" style="fill:#B2DFDB; font-size:13; text-anchor:middle">byte position inside the segment</text>
  <text x="120" y="142" style="fill:#616161; font-size:13; text-anchor:middle">bits 15-14</text>
  <text x="360" y="142" style="fill:#616161; font-size:13; text-anchor:middle">bits 13-0</text>

  <!-- Arrow to segment table -->
  <line x1="120" y1="126" x2="120" y2="196" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:2.5"></line>
  <text x="130" y="165" style="fill:#1565C0; font-size:13">Seg ID selects row</text>

  <!-- Segment Descriptor Table -->
  <text x="30" y="196" style="fill:#212121; font-size:15; font-weight:bold">Segment Descriptor Table (in memory, pointed to by LDTR/GDTR):</text>
  <rect x="30" y="205" width="420" height="44" rx="0" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="38" y="228" style="fill:#1565C0; font-size:13; font-weight:bold">Seg</text>
  <text x="100" y="228" style="fill:#1565C0; font-size:13; font-weight:bold">Name</text>
  <text x="200" y="228" style="fill:#1565C0; font-size:13; font-weight:bold">Base Address</text>
  <text x="330" y="228" style="fill:#1565C0; font-size:13; font-weight:bold">Limit</text>
  <text x="395" y="228" style="fill:#1565C0; font-size:13; font-weight:bold">Perms</text>
  <text x="38" y="243" style="fill:#424242; font-size:12">Table header row</text>

  <!-- Segment rows -->
  <rect x="30" y="249" width="420" height="36" rx="0" style="fill:#FFFFFF; stroke:#9E9E9E; stroke-width:1" />
  <text x="38" y="272" style="fill:#212121; font-size:13">0</text>
  <text x="100" y="272" style="fill:#1565C0; font-size:13; font-weight:bold">Code</text>
  <text x="200" y="272" style="fill:#212121; font-size:13">0x08048000</text>
  <text x="330" y="272" style="fill:#212121; font-size:13">64 KB</text>
  <text x="395" y="272" style="fill:#212121; font-size:13">R-X</text>

  <rect x="30" y="285" width="420" height="36" rx="0" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="38" y="308" style="fill:#212121; font-size:13">1</text>
  <text x="100" y="308" style="fill:#00796B; font-size:13; font-weight:bold">Data</text>
  <text x="200" y="308" style="fill:#212121; font-size:13">0x0804C000</text>
  <text x="330" y="308" style="fill:#212121; font-size:13">32 KB</text>
  <text x="395" y="308" style="fill:#212121; font-size:13">RW-</text>

  <rect x="30" y="321" width="420" height="36" rx="0" style="fill:#FFFFFF; stroke:#9E9E9E; stroke-width:1" />
  <text x="38" y="344" style="fill:#212121; font-size:13">2</text>
  <text x="100" y="344" style="fill:#E65100; font-size:13; font-weight:bold">Stack</text>
  <text x="200" y="344" style="fill:#212121; font-size:13">0x7FFFF000</text>
  <text x="330" y="344" style="fill:#212121; font-size:13">8 MB</text>
  <text x="395" y="344" style="fill:#212121; font-size:13">RW-</text>

  <rect x="30" y="357" width="420" height="36" rx="0" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="38" y="380" style="fill:#212121; font-size:13">3</text>
  <text x="100" y="380" style="fill:#9E9E9E; font-size:13; font-weight:bold">Heap</text>
  <text x="200" y="380" style="fill:#212121; font-size:13">0x0900A000</text>
  <text x="330" y="380" style="fill:#212121; font-size:13">16 MB</text>
  <text x="395" y="380" style="fill:#212121; font-size:13">RW-</text>

  <!-- Physical Memory map -->
  <text x="580" y="196" style="fill:#212121; font-size:15; font-weight:bold">Physical Memory:</text>
  <rect x="580" y="205" width="290" height="380" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />

  <!-- OS region -->
  <rect x="588" y="213" width="274" height="40" rx="4" style="fill:#424242" />
  <text x="725" y="238" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">OS Kernel (protected)</text>

  <!-- Code segment -->
  <rect x="588" y="258" width="274" height="50" rx="4" style="fill:#1565C0" />
  <text x="725" y="281" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Code Segment (Seg 0)</text>
  <text x="725" y="298" style="fill:#BBDEFB; font-size:12; text-anchor:middle">0x08048000 – 0x08058000</text>

  <!-- Data segment -->
  <rect x="588" y="313" width="274" height="44" rx="4" style="fill:#00796B" />
  <text x="725" y="336" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Data Segment (Seg 1)</text>
  <text x="725" y="352" style="fill:#B2DFDB; font-size:12; text-anchor:middle">0x0804C000 – 0x08054000</text>

  <!-- Gap (fragmentation) -->
  <rect x="588" y="362" width="274" height="36" rx="4" style="fill:#FFCDD2; stroke:#E65100; stroke-width:1; stroke-dasharray:4,2" />
  <text x="725" y="384" style="fill:#E65100; font-size:13; text-anchor:middle">External Fragmentation Gap</text>

  <!-- Heap -->
  <rect x="588" y="403" width="274" height="50" rx="4" style="fill:#9E9E9E" />
  <text x="725" y="426" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Heap Segment (Seg 3)</text>
  <text x="725" y="443" style="fill:#E0E0E0; font-size:12; text-anchor:middle">0x0900A000 – ...</text>

  <!-- Stack -->
  <rect x="588" y="458" width="274" height="50" rx="4" style="fill:#E65100" />
  <text x="725" y="481" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Stack Segment (Seg 2)</text>
  <text x="725" y="498" style="fill:#FFCCBC; font-size:12; text-anchor:middle">0x7FFFF000 (grows down)</text>

  <!-- Arrows from table to physical memory -->
  <line x1="450" y1="267" x2="580" y2="283" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:2; stroke-dasharray:5,3"></line>
  <line x1="450" y1="303" x2="580" y2="335" marker-end="url(#at)" style="stroke:#00796B; stroke-width:2; stroke-dasharray:5,3"></line>

  <!-- Translation arrow with label -->
  <text x="470" y="260" style="fill:#1565C0; font-size:12">Base+Offset</text>
  <text x="470" y="296" style="fill:#00796B; font-size:12">Base+Offset</text>

  <!-- Offset arrow from address field -->
  <line x1="360" y1="126" x2="360" y2="160" marker-end="url(#at)" style="stroke:#00796B; stroke-width:2"></line>
  <text x="366" y="150" style="fill:#00796B; font-size:12">+ Offset</text>
  <line x1="360" y1="160" x2="440" y2="175" style="stroke:#00796B; stroke-width:1.5; stroke-dasharray:4,2"></line>
  <text x="442" y="170" style="fill:#616161; font-size:12">(added to base)</text>

  <!-- Benefit/limitation callout -->
  <rect x="30" y="460" width="390" height="100" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="225" y="481" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Segmentation vs. Base-and-Bounds</text>
  <text x="44" y="500" style="fill:#2E7D32; font-size:13">+ Multiple segments per process (code/data/stack)</text>
  <text x="44" y="518" style="fill:#2E7D32; font-size:13">+ Per-segment protection (R/W/X permissions)</text>
  <text x="44" y="536" style="fill:#E65100; font-size:13">- External fragmentation between segments</text>
  <text x="44" y="554" style="fill:#E65100; font-size:13">- Segments must still be contiguous in RAM</text>
</svg>
</div>
<figcaption><strong>Figure 1.4:</strong> Segmentation architecture: a
logical address encodes a segment selector and byte offset; the segment
descriptor table maps each selector to a base address and
limit.</figcaption>
</figure>

Segmentation divided a program\'s address space into logical units
(segments) like code, data, stack, and heap. Each segment had its own
base and bounds.

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="468" viewBox="0 0 900 468" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
    <marker id="arr-b" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
  </defs>
  <rect width="900" height="480" style="fill:#FAFAFA" />
  <text x="450" y="36" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Segmented Address Format</text>
  <text x="450" y="56" style="fill:#616161; font-size:13; text-anchor:middle">How a segmented virtual address is split into Segment Selector and Offset</text>

  <!-- ADDRESS BAR (32-bit example) -->
  <text x="450" y="86" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">32-bit Segmented Virtual Address</text>

  <!-- Bit labels top -->
  <text x="160" y="102" style="fill:#616161; font-size:12; text-anchor:middle">bit 31</text>
  <text x="430" y="102" style="fill:#616161; font-size:12; text-anchor:middle">bit 16</text>
  <text x="470" y="102" style="fill:#616161; font-size:12; text-anchor:middle">bit 15</text>
  <text x="760" y="102" style="fill:#616161; font-size:12; text-anchor:middle">bit 0</text>

  <!-- Segment Selector field -->
  <rect x="30" y="108" width="420" height="60" rx="6" filter="url(#sh)" style="fill:#1565C0" />
  <text x="240" y="133" style="fill:#FFFFFF; font-size:16; font-weight:bold; text-anchor:middle">Segment Selector</text>
  <text x="240" y="155" style="fill:#BBDEFB; font-size:14; text-anchor:middle">16 bits (bits 31:16) — identifies segment</text>

  <!-- Offset field -->
  <rect x="456" y="108" width="414" height="60" rx="6" filter="url(#sh)" style="fill:#00796B" />
  <text x="663" y="133" style="fill:#FFFFFF; font-size:16; font-weight:bold; text-anchor:middle">Offset within Segment</text>
  <text x="663" y="155" style="fill:#B2DFDB; font-size:14; text-anchor:middle">16 bits (bits 15:0) — byte within segment</text>

  <!-- Example walkthrough -->
  <rect x="30" y="190" width="840" height="80" rx="6" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="450" y="212" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Translation Example: 0x0002_1A40</text>
  <text x="70" y="236" style="fill:#212121; font-size:13">Segment Selector = 0x0002 (Segment 2)</text>
  <text x="70" y="256" style="fill:#212121; font-size:13">Offset = 0x1A40 (byte 6720 within segment)</text>
  <text x="500" y="236" style="fill:#212121; font-size:13">Segment 2 Base = 0x00C0_0000 (from descriptor table)</text>
  <text x="500" y="256" style="fill:#1565C0; font-size:13; font-weight:bold">Physical Address = 0x00C0_0000 + 0x1A40 = 0x00C0_1A40</text>

  <!-- Selector breakdown -->
  <rect x="30" y="292" width="400" height="152" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="230" y="312" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Selector Field Detail (x86 style)</text>

  <rect x="45" y="322" width="160" height="30" rx="3" style="fill:#1565C0" />
  <text x="125" y="341" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Descriptor Index</text>
  <rect x="209" y="322" width="60" height="30" rx="3" style="fill:#5C6BC0" />
  <text x="239" y="341" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">TI</text>
  <rect x="273" y="322" width="80" height="30" rx="3" style="fill:#E65100" />
  <text x="313" y="341" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">RPL</text>

  <text x="125" y="370" style="fill:#616161; font-size:12; text-anchor:middle">Which segment descriptor</text>
  <text x="239" y="370" style="fill:#616161; font-size:12; text-anchor:middle">GDT/LDT</text>
  <text x="313" y="370" style="fill:#616161; font-size:12; text-anchor:middle">Privilege (0–3)</text>
  <text x="45" y="395" style="fill:#616161; font-size:12">TI: Table Indicator — 0=GDT (Global), 1=LDT (Local)</text>
  <text x="45" y="412" style="fill:#616161; font-size:12">RPL: Requested Privilege Level</text>

  <!-- Offset breakdown -->
  <rect x="460" y="292" width="410" height="152" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="665" y="312" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Offset Constraints</text>
  <text x="475" y="336" style="fill:#212121; font-size:13">• Offset must be ≤ Limit in segment descriptor</text>
  <text x="475" y="356" style="fill:#212121; font-size:13">• If Offset &gt; Limit → General Protection Fault (#GP)</text>
  <text x="475" y="376" style="fill:#212121; font-size:13">• 16-bit offset: max 64 KB segment size</text>
  <text x="475" y="396" style="fill:#212121; font-size:13">• 32-bit offset (protected mode): max 4 GB segment</text>
</svg>
</div>
<figcaption><strong>Figure 1.5:</strong> Segmented address format: the
high bits select the segment descriptor; the low bits specify the byte
offset within that segment.</figcaption>
</figure>

**Segments Matched Logical Structure:**

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter></defs>
  <rect width="900" height="560" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Segment Types and Properties in a Typical Process</text>

  <!-- Table header -->
  <rect x="22" y="55" width="856" height="36" rx="4" style="fill:#1565C0" />
  <text x="60" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Segment</text>
  <text x="200" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Contains</text>
  <text x="380" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Permissions</text>
  <text x="530" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Typical Size</text>
  <text x="680" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Growth Direction</text>
  <text x="820" y="78" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Shared?</text>

  <!-- Text / Code segment -->
  <rect x="22" y="91" width="856" height="66" rx="0" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <rect x="22" y="91" width="76" height="66" style="fill:#1565C0" />
  <text x="60" y="121" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">.text</text>
  <text x="60" y="139" style="fill:#BBDEFB; font-size:12; text-anchor:middle">(Code)</text>
  <text x="200" y="114" style="fill:#212121; font-size:13; text-anchor:middle">Machine instructions</text>
  <text x="200" y="132" style="fill:#212121; font-size:13; text-anchor:middle">compiled program</text>
  <text x="380" y="114" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">R-X</text>
  <text x="380" y="132" style="fill:#2E7D32; font-size:12; text-anchor:middle">Read + Execute only</text>
  <text x="380" y="148" style="fill:#E65100; font-size:12; text-anchor:middle">No Write! (W^X policy)</text>
  <text x="530" y="121" style="fill:#212121; font-size:13; text-anchor:middle">10 KB – 10 MB</text>
  <text x="680" y="121" style="fill:#212121; font-size:13; text-anchor:middle">Fixed at load time</text>
  <text x="820" y="114" style="fill:#2E7D32; font-size:13; font-weight:bold; text-anchor:middle">YES</text>
  <text x="820" y="132" style="fill:#212121; font-size:12; text-anchor:middle">Between processes</text>

  <!-- Data segment -->
  <rect x="22" y="157" width="856" height="66" rx="0" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <rect x="22" y="157" width="76" height="66" style="fill:#00796B" />
  <text x="60" y="187" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">.data</text>
  <text x="60" y="205" style="fill:#B2DFDB; font-size:12; text-anchor:middle">(Init. Data)</text>
  <text x="200" y="180" style="fill:#212121; font-size:13; text-anchor:middle">Global/static variables</text>
  <text x="200" y="198" style="fill:#212121; font-size:13; text-anchor:middle">with initial values</text>
  <text x="380" y="187" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">RW-</text>
  <text x="380" y="205" style="fill:#616161; font-size:12; text-anchor:middle">Read + Write, No Execute</text>
  <text x="530" y="187" style="fill:#212121; font-size:13; text-anchor:middle">1 KB – 100 MB</text>
  <text x="680" y="187" style="fill:#212121; font-size:13; text-anchor:middle">Fixed at load time</text>
  <text x="820" y="187" style="fill:#E65100; font-size:13; text-anchor:middle">NO (private)</text>

  <!-- BSS segment -->
  <rect x="22" y="223" width="856" height="66" rx="0" style="fill:#E8F5E9; stroke:#9E9E9E; stroke-width:1" />
  <rect x="22" y="223" width="76" height="66" style="fill:#00796B; opacity:0.78" />
  <text x="60" y="253" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">.bss</text>
  <text x="60" y="271" style="fill:#B2DFDB; font-size:12; text-anchor:middle">(Uninit. Data)</text>
  <text x="200" y="246" style="fill:#212121; font-size:13; text-anchor:middle">Uninitialized globals</text>
  <text x="200" y="264" style="fill:#212121; font-size:13; text-anchor:middle">zero-filled by OS</text>
  <text x="380" y="253" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">RW-</text>
  <text x="380" y="271" style="fill:#616161; font-size:12; text-anchor:middle">Read + Write, No Execute</text>
  <text x="530" y="253" style="fill:#212121; font-size:13; text-anchor:middle">1 KB – 100 MB</text>
  <text x="680" y="253" style="fill:#212121; font-size:13; text-anchor:middle">Fixed at load time</text>
  <text x="820" y="253" style="fill:#E65100; font-size:13; text-anchor:middle">NO (private)</text>

  <!-- Heap -->
  <rect x="22" y="289" width="856" height="66" rx="0" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <rect x="22" y="289" width="76" height="66" style="fill:#9E9E9E" />
  <text x="60" y="319" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Heap</text>
  <text x="60" y="337" style="fill:#E0E0E0; font-size:12; text-anchor:middle">(Dynamic)</text>
  <text x="200" y="312" style="fill:#212121; font-size:13; text-anchor:middle">malloc/new allocations</text>
  <text x="200" y="330" style="fill:#212121; font-size:13; text-anchor:middle">runtime dynamic data</text>
  <text x="380" y="319" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">RW-</text>
  <text x="380" y="337" style="fill:#616161; font-size:12; text-anchor:middle">Read + Write, No Execute</text>
  <text x="530" y="319" style="fill:#212121; font-size:13; text-anchor:middle">KB to GB (dynamic)</text>
  <text x="680" y="312" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Grows UP</text>
  <text x="680" y="330" style="fill:#212121; font-size:12; text-anchor:middle">via brk() or mmap()</text>
  <text x="820" y="319" style="fill:#E65100; font-size:13; text-anchor:middle">NO (private)</text>

  <!-- Stack -->
  <rect x="22" y="355" width="856" height="66" rx="0" style="fill:#FFEBEE; stroke:#9E9E9E; stroke-width:1" />
  <rect x="22" y="355" width="76" height="66" style="fill:#E65100" />
  <text x="60" y="385" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Stack</text>
  <text x="60" y="403" style="fill:#FFCCBC; font-size:12; text-anchor:middle">(Per-thread)</text>
  <text x="200" y="378" style="fill:#212121; font-size:13; text-anchor:middle">Local variables, return</text>
  <text x="200" y="396" style="fill:#212121; font-size:13; text-anchor:middle">addresses, saved regs</text>
  <text x="380" y="385" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">RW-</text>
  <text x="380" y="403" style="fill:#616161; font-size:12; text-anchor:middle">Read + Write, No Execute</text>
  <text x="530" y="385" style="fill:#212121; font-size:13; text-anchor:middle">8 KB – 8 MB limit</text>
  <text x="680" y="378" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Grows DOWN</text>
  <text x="680" y="396" style="fill:#212121; font-size:12; text-anchor:middle">toward lower addresses</text>
  <text x="820" y="385" style="fill:#E65100; font-size:13; text-anchor:middle">NO (per-thread)</text>

  <!-- Permissions legend -->
  <rect x="22" y="438" width="856" height="104" rx="6" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="438" y="460" style="fill:#1565C0; font-size:15; font-weight:bold; text-anchor:middle">Permission Flags (set per-page in PTE)</text>
  <text x="90" y="484" style="fill:#212121; font-size:14; text-anchor:middle">R = Readable</text>
  <text x="90" y="504" style="fill:#616161; font-size:13; text-anchor:middle">All segments</text>
  <text x="260" y="484" style="fill:#212121; font-size:14; text-anchor:middle">W = Writable</text>
  <text x="260" y="504" style="fill:#616161; font-size:13; text-anchor:middle">Data/BSS/Heap/Stack</text>
  <text x="450" y="484" style="fill:#212121; font-size:14; text-anchor:middle">X = Executable</text>
  <text x="450" y="504" style="fill:#616161; font-size:13; text-anchor:middle">Code only (W^X enforced)</text>
  <text x="650" y="484" style="fill:#212121; font-size:14; text-anchor:middle">NX = No-Execute</text>
  <text x="650" y="504" style="fill:#616161; font-size:13; text-anchor:middle">Set on data pages (PTE bit 63)</text>
  <text x="438" y="532" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">W^X Policy: A page must never be both Writable and Executable simultaneously (prevents code injection attacks)</text>
</svg>
</div>
<figcaption><strong>Figure 1.6:</strong> Common segment types (code,
data, stack, heap) and their access-protection properties.</figcaption>
</figure>

    Segment 0: Code      (executable, read-only)
    Segment 1: Data      (read-write)
    Segment 2: Stack     (read-write, grows down)
    Segment 3: Heap      (read-write, grows up)

**Virtual Address Format (Segmented):**

**Advantages:** - Logical program structure - Easy sharing (share code
segment) - Different protection for different segments - No internal
fragmentation

**Disadvantages:** - **External fragmentation:** Segments of varying
sizes left gaps in physical memory - Required compaction (expensive
memory copying) - Large segments still needed contiguous physical memory

**Historical Example: Intel 8086 (1978)** The 8086 used segmentation to
address 1 MB of memory with 16-bit registers:

    Physical Address = (Segment x 16) + Offset

### 1.3.4 Paging: The Modern Solution (1960s-Present)

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="580" viewBox="0 0 900 580" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
    <marker id="ab" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="at" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker>
  </defs>
  <rect width="900" height="580" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Paging: Virtual Page to Physical Frame Mapping</text>

  <!-- Process A Virtual Space -->
  <text x="60" y="68" style="fill:#1565C0; font-size:15; font-weight:bold; text-anchor:middle">Process A</text>
  <text x="60" y="84" style="fill:#616161; font-size:13; text-anchor:middle">Virtual Space</text>
  <rect x="20" y="92" width="80" height="36" rx="4" style="fill:#1565C0" />
  <text x="60" y="115" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Page 0</text>
  <rect x="20" y="130" width="80" height="36" rx="4" style="fill:#1565C0; opacity:0.8" />
  <text x="60" y="153" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Page 1</text>
  <rect x="20" y="168" width="80" height="36" rx="4" style="fill:#1565C0; opacity:0.6" />
  <text x="60" y="191" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Page 2</text>
  <rect x="20" y="206" width="80" height="36" rx="4" style="fill:#9E9E9E; stroke:#9E9E9E; stroke-dasharray:4,2" />
  <text x="60" y="229" style="fill:#616161; font-size:12; text-anchor:middle">Page 3</text>
  <text x="60" y="250" style="fill:#616161; font-size:12; text-anchor:middle">(unmapped)</text>

  <!-- Process B Virtual Space -->
  <text x="200" y="68" style="fill:#1565C0; font-size:15; font-weight:bold; text-anchor:middle">Process B</text>
  <text x="200" y="84" style="fill:#616161; font-size:13; text-anchor:middle">Virtual Space</text>
  <rect x="160" y="92" width="80" height="36" rx="4" style="fill:#1565C0" />
  <text x="200" y="115" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Page 0</text>
  <rect x="160" y="130" width="80" height="36" rx="4" style="fill:#1565C0; opacity:0.7" />
  <text x="200" y="153" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Page 1</text>
  <rect x="160" y="168" width="80" height="36" rx="4" style="fill:#9E9E9E; stroke:#9E9E9E; stroke-dasharray:4,2" />
  <text x="200" y="191" style="fill:#616161; font-size:12; text-anchor:middle">Page 2</text>
  <text x="200" y="208" style="fill:#616161; font-size:12; text-anchor:middle">(unmapped)</text>

  <!-- Page Table A — wider: 180px, VPN col 60px, PFN col 120px -->
  <text x="390" y="68" style="fill:#212121; font-size:15; font-weight:bold; text-anchor:middle">Page Table A</text>
  <!-- Header -->
  <rect x="300" y="78" width="180" height="36" rx="4" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <line x1="360" y1="78" x2="360" y2="114" style="stroke:#1565C0; stroke-width:1"></line>
  <text x="330" y="99" style="fill:#1565C0; font-size:12; font-weight:bold; text-anchor:middle">VPN</text>
  <text x="420" y="99" style="fill:#1565C0; font-size:12; font-weight:bold; text-anchor:middle">PFN</text>
  <!-- Row 0 -->
  <rect x="300" y="114" width="180" height="30" style="fill:#FFFFFF; stroke:#9E9E9E; stroke-width:1" />
  <line x1="360" y1="114" x2="360" y2="144" style="stroke:#9E9E9E; stroke-width:1"></line>
  <text x="330" y="133" style="fill:#212121; font-size:13; text-anchor:middle">0</text>
  <text x="420" y="133" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">5</text>
  <!-- Row 1 -->
  <rect x="300" y="144" width="180" height="30" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <line x1="360" y1="144" x2="360" y2="174" style="stroke:#9E9E9E; stroke-width:1"></line>
  <text x="330" y="163" style="fill:#212121; font-size:13; text-anchor:middle">1</text>
  <text x="420" y="163" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">2</text>
  <!-- Row 2 -->
  <rect x="300" y="174" width="180" height="30" style="fill:#FFFFFF; stroke:#9E9E9E; stroke-width:1" />
  <line x1="360" y1="174" x2="360" y2="204" style="stroke:#9E9E9E; stroke-width:1"></line>
  <text x="330" y="193" style="fill:#212121; font-size:13; text-anchor:middle">2</text>
  <text x="420" y="193" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">8</text>
  <!-- Row 3 — NOT PRESENT, taller row -->
  <rect x="300" y="204" width="180" height="44" style="fill:#FFF8E1; stroke:#9E9E9E; stroke-width:1" />
  <line x1="360" y1="204" x2="360" y2="248" style="stroke:#9E9E9E; stroke-width:1"></line>
  <text x="330" y="222" style="fill:#212121; font-size:13; text-anchor:middle">3</text>
  <rect x="364" y="213" width="112" height="28" rx="3" style="fill:#FFCC80" />
  <text x="420" y="224" style="fill:#BF360C; font-size:10; font-weight:bold; text-anchor:middle">NOT</text>
  <text x="420" y="237" style="fill:#BF360C; font-size:10; font-weight:bold; text-anchor:middle">PRESENT</text>

  <!-- Page Table B — same wider layout -->
  <text x="390" y="278" style="fill:#212121; font-size:15; font-weight:bold; text-anchor:middle">Page Table B</text>
  <!-- Header -->
  <rect x="300" y="288" width="180" height="36" rx="4" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <line x1="360" y1="288" x2="360" y2="324" style="stroke:#1565C0; stroke-width:1"></line>
  <text x="330" y="309" style="fill:#1565C0; font-size:12; font-weight:bold; text-anchor:middle">VPN</text>
  <text x="420" y="309" style="fill:#1565C0; font-size:12; font-weight:bold; text-anchor:middle">PFN</text>
  <!-- Row 0 -->
  <rect x="300" y="324" width="180" height="30" style="fill:#FFFFFF; stroke:#9E9E9E; stroke-width:1" />
  <line x1="360" y1="324" x2="360" y2="354" style="stroke:#9E9E9E; stroke-width:1"></line>
  <text x="330" y="343" style="fill:#212121; font-size:13; text-anchor:middle">0</text>
  <text x="420" y="343" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">3</text>
  <!-- Row 1 -->
  <rect x="300" y="354" width="180" height="30" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <line x1="360" y1="354" x2="360" y2="384" style="stroke:#9E9E9E; stroke-width:1"></line>
  <text x="330" y="373" style="fill:#212121; font-size:13; text-anchor:middle">1</text>
  <text x="420" y="373" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">7</text>
  <!-- Row 2 — NOT PRESENT, taller row -->
  <rect x="300" y="384" width="180" height="44" style="fill:#FFF8E1; stroke:#9E9E9E; stroke-width:1" />
  <line x1="360" y1="384" x2="360" y2="428" style="stroke:#9E9E9E; stroke-width:1"></line>
  <text x="330" y="402" style="fill:#212121; font-size:13; text-anchor:middle">2</text>
  <rect x="364" y="393" width="112" height="28" rx="3" style="fill:#FFCC80" />
  <text x="420" y="404" style="fill:#BF360C; font-size:10; font-weight:bold; text-anchor:middle">NOT</text>
  <text x="420" y="417" style="fill:#BF360C; font-size:10; font-weight:bold; text-anchor:middle">PRESENT</text>

  <!-- Physical Memory -->
  <text x="750" y="68" style="fill:#212121; font-size:15; font-weight:bold; text-anchor:middle">Physical Memory</text>
  <text x="750" y="84" style="fill:#616161; font-size:13; text-anchor:middle">(shared, one real RAM)</text>
  <rect x="670" y="92" width="160" height="400" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />
  <rect x="678" y="100" width="144" height="36" rx="4" style="fill:#424242" />
  <text x="750" y="122" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Frame 0: OS Kernel</text>
  <rect x="678" y="138" width="144" height="36" rx="4" style="fill:#BDBDBD" />
  <text x="750" y="160" style="fill:#616161; font-size:12; text-anchor:middle">Frame 1: free</text>
  <rect x="678" y="176" width="144" height="36" rx="4" style="fill:#1565C0" />
  <text x="750" y="198" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Frame 2: Proc A Pg 1</text>
  <rect x="678" y="214" width="144" height="36" rx="4" style="fill:#00796B" />
  <text x="750" y="236" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Frame 3: Proc B Pg 0</text>
  <rect x="678" y="252" width="144" height="36" rx="4" style="fill:#BDBDBD" />
  <text x="750" y="274" style="fill:#616161; font-size:12; text-anchor:middle">Frame 4: free</text>
  <rect x="678" y="290" width="144" height="36" rx="4" style="fill:#1565C0; opacity:0.7" />
  <text x="750" y="312" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Frame 5: Proc A Pg 0</text>
  <rect x="678" y="328" width="144" height="36" rx="4" style="fill:#BDBDBD" />
  <text x="750" y="350" style="fill:#616161; font-size:12; text-anchor:middle">Frame 6: free</text>
  <rect x="678" y="366" width="144" height="36" rx="4" style="fill:#00796B; opacity:0.7" />
  <text x="750" y="388" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Frame 7: Proc B Pg 1</text>
  <rect x="678" y="404" width="144" height="36" rx="4" style="fill:#1565C0; opacity:0.5" />
  <text x="750" y="426" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Frame 8: Proc A Pg 2</text>

  <!-- Mapping arrows from Page Table A -->
  <line x1="480" y1="129" x2="668" y2="305" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:1.8; stroke-dasharray:5,3"></line>
  <line x1="480" y1="159" x2="668" y2="195" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:1.8; stroke-dasharray:5,3"></line>
  <line x1="480" y1="189" x2="668" y2="421" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:1.8; stroke-dasharray:5,3"></line>
  <!-- Mapping arrows from Page Table B -->
  <line x1="480" y1="339" x2="668" y2="232" marker-end="url(#at)" style="stroke:#00796B; stroke-width:1.8; stroke-dasharray:5,3"></line>
  <line x1="480" y1="369" x2="668" y2="384" marker-end="url(#at)" style="stroke:#00796B; stroke-width:1.8; stroke-dasharray:5,3"></line>

  <!-- Benefits annotation -->
  <rect x="26" y="460" width="260" height="100" rx="6" style="fill:#E8F5E9; stroke:#00796B; stroke-width:1.5" />
  <text x="156" y="481" style="fill:#00796B; font-size:14; font-weight:bold; text-anchor:middle">Key Benefits of Paging</text>
  <text x="38" y="501" style="fill:#212121; font-size:13">+ Non-contiguous physical allocation</text>
  <text x="38" y="519" style="fill:#212121; font-size:13">+ Complete process isolation</text>
  <text x="38" y="537" style="fill:#212121; font-size:13">+ No external fragmentation</text>
  <text x="38" y="555" style="fill:#212121; font-size:13">+ Simple frame reclamation</text>

  <!-- Isolation annotation -->
  <rect x="300" y="460" width="350" height="100" rx="6" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="475" y="481" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">Isolation in Action</text>
  <text x="312" y="501" style="fill:#212121; font-size:13">Proc A: VA 0x1000 → Frame 5 (PFN=5)</text>
  <text x="312" y="519" style="fill:#212121; font-size:13">Proc B: VA 0x1000 → Frame 3 (PFN=3)</text>
  <text x="312" y="537" style="fill:#212121; font-size:13">Same virtual address, different physical</text>
  <text x="312" y="555" style="fill:#00796B; font-size:14; font-weight:bold">= Perfect isolation guaranteed!</text>
</svg>
</div>
<figcaption><strong>Figure 1.7:</strong> Paging overview: the virtual
address splits into a Virtual Page Number (VPN) and page offset; the
page table maps each VPN to a Physical Frame Number (PFN).</figcaption>
</figure>

The Atlas computer (University of Manchester, 1962) introduced
**paging**\--dividing both virtual and physical memory into fixed-size
blocks called *pages* (virtual) and *frames* (physical) \[Fotheringham,
1961; Kilburn et al., 1962\].

**Key Insight:** With fixed-size pages, any page can map to any frame.
No external fragmentation!

**Typical Page Sizes:** - **4 KB**: Standard on x86/x64, ARM, RISC-V -
**16 KB**: Option on ARM - **64 KB**: Option on ARM, used by some UNIX
variants - **2 MB/1 GB**: \"Huge pages\" for reducing translation
overhead

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter></defs>
  <rect width="900" height="560" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Page Table Entry (PTE) Structure: x86-64 64-bit Format</text>

  <!-- 64-bit PTE bar -->
  <text x="30" y="66" style="fill:#616161; font-size:14; font-weight:bold">64-bit PTE (one entry per virtual page):</text>
  <!-- Bit fields -->
  <!-- NX bit 63 -->
  <rect x="22" y="76" width="38" height="44" rx="3" style="fill:#E65100" />
  <text x="41" y="96" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">NX</text>
  <text x="41" y="112" style="fill:#FFCCBC; font-size:10; text-anchor:middle">bit 63</text>
  <!-- Reserved 62-52 -->
  <rect x="62" y="76" width="82" height="44" rx="3" style="fill:#BDBDBD" />
  <text x="103" y="96" style="fill:#616161; font-size:11; text-anchor:middle">Reserved</text>
  <text x="103" y="112" style="fill:#757575; font-size:10; text-anchor:middle">bits 62-52</text>
  <!-- PFN 51-12 -->
  <rect x="146" y="76" width="480" height="44" rx="3" style="fill:#00796B" />
  <text x="386" y="96" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Physical Frame Number (PFN)</text>
  <text x="386" y="112" style="fill:#B2DFDB; font-size:12; text-anchor:middle">bits 51-12  (40 bits = up to 4 PB of physical memory)</text>
  <!-- Flags 11-9 -->
  <rect x="628" y="76" width="46" height="44" rx="3" style="fill:#9E9E9E" />
  <text x="651" y="96" style="fill:#FFFFFF; font-size:11; text-anchor:middle">Avail</text>
  <text x="651" y="112" style="fill:#E0E0E0; font-size:10; text-anchor:middle">11-9</text>
  <!-- G -->
  <rect x="676" y="76" width="26" height="44" rx="3" style="fill:#1565C0" />
  <text x="689" y="96" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">G</text>
  <text x="689" y="112" style="fill:#BBDEFB; font-size:10; text-anchor:middle">bit8</text>
  <!-- PAT -->
  <rect x="704" y="76" width="26" height="44" rx="3" style="fill:#1565C0" />
  <text x="717" y="96" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">PAT</text>
  <text x="717" y="112" style="fill:#BBDEFB; font-size:10; text-anchor:middle">bit7</text>
  <!-- D -->
  <rect x="732" y="76" width="26" height="44" rx="3" style="fill:#1565C0" />
  <text x="745" y="96" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">D</text>
  <text x="745" y="112" style="fill:#BBDEFB; font-size:10; text-anchor:middle">bit6</text>
  <!-- A -->
  <rect x="760" y="76" width="26" height="44" rx="3" style="fill:#1565C0" />
  <text x="773" y="96" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">A</text>
  <text x="773" y="112" style="fill:#BBDEFB; font-size:10; text-anchor:middle">bit5</text>
  <!-- PCD -->
  <rect x="788" y="76" width="26" height="44" rx="3" style="fill:#9E9E9E" />
  <text x="801" y="96" style="fill:#FFFFFF; font-size:11; text-anchor:middle">PCD</text>
  <text x="801" y="112" style="fill:#E0E0E0; font-size:10; text-anchor:middle">bit4</text>
  <!-- PWT -->
  <rect x="816" y="76" width="26" height="44" rx="3" style="fill:#9E9E9E" />
  <text x="829" y="96" style="fill:#FFFFFF; font-size:11; text-anchor:middle">PWT</text>
  <text x="829" y="112" style="fill:#E0E0E0; font-size:10; text-anchor:middle">bit3</text>
  <!-- U/S -->
  <rect x="844" y="76" width="22" height="44" rx="3" style="fill:#E65100" />
  <text x="855" y="96" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">U/S</text>
  <text x="855" y="112" style="fill:#FFCCBC; font-size:10; text-anchor:middle">bit2</text>
  <!-- R/W -->
  <rect x="868" y="76" width="14" height="44" rx="3" style="fill:#E65100" />
  <text x="875" y="96" style="fill:#FFFFFF; font-size:9; font-weight:bold; text-anchor:middle">R/W</text>
  <text x="875" y="112" style="fill:#FFCCBC; font-size:9; text-anchor:middle">b1</text>
  <!-- P -->
  <rect x="884" y="76" width="12" height="44" rx="3" style="fill:#2E7D32" />
  <text x="890" y="96" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">P</text>
  <text x="890" y="112" style="fill:#A5D6A7; font-size:9; text-anchor:middle">b0</text>

  <!-- Flag explanations -->
  <text x="30" y="152" style="fill:#212121; font-size:15; font-weight:bold">Flag Bit Definitions:</text>

  <rect x="22" y="162" width="420" height="280" rx="6" filter="url(#sh)" style="fill:#FFFFFF; stroke:#9E9E9E; stroke-width:1.5" />
  <rect x="22" y="162" width="420" height="34" rx="6" style="fill:#1565C0" />
  <text x="40" y="183" style="fill:#FFFFFF; font-size:13; font-weight:bold">Bit</text>
  <text x="90" y="183" style="fill:#FFFFFF; font-size:13; font-weight:bold">Name</text>
  <text x="200" y="183" style="fill:#FFFFFF; font-size:13; font-weight:bold">Meaning</text>

  <rect x="22" y="196" width="420" height="28" style="fill:#F5F5F5" />
  <text x="40" y="214" style="fill:#2E7D32; font-size:13; font-weight:bold">0</text>
  <text x="90" y="214" style="fill:#2E7D32; font-size:13; font-weight:bold">P (Present)</text>
  <text x="200" y="214" style="fill:#212121; font-size:13">1 = page in RAM; 0 = page fault</text>

  <rect x="22" y="224" width="420" height="28" style="fill:#FFFFFF" />
  <text x="40" y="242" style="fill:#E65100; font-size:13; font-weight:bold">1</text>
  <text x="90" y="242" style="fill:#E65100; font-size:13; font-weight:bold">R/W</text>
  <text x="200" y="242" style="fill:#212121; font-size:13">1 = writable; 0 = read-only</text>

  <rect x="22" y="252" width="420" height="28" style="fill:#F5F5F5" />
  <text x="40" y="270" style="fill:#E65100; font-size:13; font-weight:bold">2</text>
  <text x="90" y="270" style="fill:#E65100; font-size:13; font-weight:bold">U/S</text>
  <text x="200" y="270" style="fill:#212121; font-size:13">1 = user accessible; 0 = kernel only</text>

  <rect x="22" y="280" width="420" height="28" style="fill:#FFFFFF" />
  <text x="40" y="298" style="fill:#1565C0; font-size:13; font-weight:bold">5</text>
  <text x="90" y="298" style="fill:#1565C0; font-size:13; font-weight:bold">A (Accessed)</text>
  <text x="200" y="298" style="fill:#212121; font-size:13">Set by CPU on any access</text>

  <rect x="22" y="308" width="420" height="28" style="fill:#F5F5F5" />
  <text x="40" y="326" style="fill:#1565C0; font-size:13; font-weight:bold">6</text>
  <text x="90" y="326" style="fill:#1565C0; font-size:13; font-weight:bold">D (Dirty)</text>
  <text x="200" y="326" style="fill:#212121; font-size:13">Set by CPU on write access</text>

  <rect x="22" y="336" width="420" height="28" style="fill:#FFFFFF" />
  <text x="40" y="354" style="fill:#1565C0; font-size:13; font-weight:bold">8</text>
  <text x="90" y="354" style="fill:#1565C0; font-size:13; font-weight:bold">G (Global)</text>
  <text x="200" y="354" style="fill:#212121; font-size:13">Don&#39;t flush TLB on context switch</text>

  <rect x="22" y="364" width="420" height="28" style="fill:#F5F5F5" />
  <text x="40" y="382" style="fill:#E65100; font-size:13; font-weight:bold">63</text>
  <text x="90" y="382" style="fill:#E65100; font-size:13; font-weight:bold">NX (No-Execute)</text>
  <text x="200" y="382" style="fill:#212121; font-size:13">1 = page cannot execute code</text>

  <rect x="22" y="392" width="420" height="50" style="fill:#E3F2FD" />
  <text x="40" y="410" style="fill:#1565C0; font-size:13; font-weight:bold">12-51</text>
  <text x="110" y="410" style="fill:#1565C0; font-size:13; font-weight:bold">PFN (Physical Frame Number)</text>
  <text x="40" y="432" style="fill:#212121; font-size:13">40-bit frame number. Shift left by 12 to get physical address.</text>

  <!-- Three States diagram -->
  <text x="468" y="152" style="fill:#212121; font-size:15; font-weight:bold">PTE State Machine:</text>

  <!-- State 1: Present -->
  <rect x="468" y="162" width="200" height="90" rx="6" filter="url(#sh)" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:2" />
  <text x="568" y="186" style="fill:#2E7D32; font-size:14; font-weight:bold; text-anchor:middle">PRESENT (P=1)</text>
  <text x="568" y="206" style="fill:#212121; font-size:13; text-anchor:middle">Page is in physical RAM</text>
  <text x="568" y="224" style="fill:#212121; font-size:13; text-anchor:middle">PFN field is valid</text>
  <text x="568" y="242" style="fill:#212121; font-size:13; text-anchor:middle">TLB can cache this entry</text>

  <!-- State 2: Swapped -->
  <rect x="468" y="272" width="200" height="90" rx="6" filter="url(#sh)" style="fill:#FFF3E0; stroke:#E65100; stroke-width:2" />
  <text x="568" y="296" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">SWAPPED (P=0)</text>
  <text x="568" y="316" style="fill:#212121; font-size:13; text-anchor:middle">Page is on disk/swap</text>
  <text x="568" y="334" style="fill:#212121; font-size:13; text-anchor:middle">OS uses PFN bits for</text>
  <text x="568" y="352" style="fill:#212121; font-size:13; text-anchor:middle">swap location info</text>

  <!-- State 3: Never allocated -->
  <rect x="468" y="382" width="200" height="90" rx="6" filter="url(#sh)" style="fill:#FFEBEE; stroke:#B71C1C; stroke-width:2" />
  <text x="568" y="406" style="fill:#B71C1C; font-size:14; font-weight:bold; text-anchor:middle">NOT ALLOCATED</text>
  <text x="568" y="426" style="fill:#212121; font-size:13; text-anchor:middle">Virtual page not mapped</text>
  <text x="568" y="444" style="fill:#212121; font-size:13; text-anchor:middle">Access = SIGSEGV</text>
  <text x="568" y="462" style="fill:#212121; font-size:13; text-anchor:middle">(segmentation fault)</text>

  <!-- Arrows between states -->
  <line x1="568" y1="252" x2="568" y2="272" style="stroke:#9E9E9E; stroke-width:2; stroke-dasharray:4,2"></line>
  <line x1="568" y1="362" x2="568" y2="382" style="stroke:#9E9E9E; stroke-width:2; stroke-dasharray:4,2"></line>

  <!-- What happens on access boxes -->
  <rect x="686" y="162" width="192" height="90" rx="6" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="782" y="183" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:middle">On Access:</text>
  <text x="698" y="203" style="fill:#212121; font-size:13">TLB gets Physical Address</text>
  <text x="698" y="221" style="fill:#212121; font-size:13">Memory access proceeds</text>
  <text x="698" y="239" style="fill:#2E7D32; font-size:13; font-weight:bold">Fast path (0-1 cycles)</text>

  <rect x="686" y="272" width="192" height="90" rx="6" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="782" y="293" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">On Access:</text>
  <text x="698" y="313" style="fill:#212121; font-size:13">Page fault exception</text>
  <text x="698" y="331" style="fill:#212121; font-size:13">OS loads page from disk</text>
  <text x="698" y="349" style="fill:#E65100; font-size:13; font-weight:bold">Slow (25 us - 10 ms)</text>

  <rect x="686" y="382" width="192" height="90" rx="6" style="fill:#FFEBEE; stroke:#B71C1C; stroke-width:1.5" />
  <text x="782" y="403" style="fill:#B71C1C; font-size:13; font-weight:bold; text-anchor:middle">On Access:</text>
  <text x="698" y="423" style="fill:#212121; font-size:13">Page fault exception</text>
  <text x="698" y="441" style="fill:#212121; font-size:13">OS sends SIGSEGV</text>
  <text x="698" y="459" style="fill:#B71C1C; font-size:13; font-weight:bold">Process terminated</text>

  <!-- Connector lines -->
  <line x1="668" y1="207" x2="686" y2="207" style="stroke:#1565C0; stroke-width:1.5"></line>
  <line x1="668" y1="317" x2="686" y2="317" style="stroke:#E65100; stroke-width:1.5"></line>
  <line x1="668" y1="427" x2="686" y2="427" style="stroke:#B71C1C; stroke-width:1.5"></line>
</svg>
</div>
<figcaption><strong>Figure 1.8:</strong> Page Table Entry (PTE)
structure: physical frame number plus status bits -- Present (P),
Read/Write (R/W), User/Supervisor (U/S), Dirty (D), and Accessed
(A).</figcaption>
</figure>

**Virtual Address Format (4 KB pages, 32-bit address space):**

**Physical Address Format:**

**Page Table:** The mapping from virtual page numbers to physical frame
numbers is stored in a *page table*.

**Advantages of Paging:** 1. **No external fragmentation** (all blocks
are same size) 2. **Easy allocation** (any free frame works) 3.
**Efficient sharing** (multiple page tables point to same frame) 4.
**Demand paging** (load pages only when accessed) 5. **Virtual memory**
(address space larger than physical RAM)

**Disadvantages:** 1. **Internal fragmentation** (wasted space in
partial pages) 2. **Page table overhead** (memory consumed by page
tables themselves) 3. **Translation overhead** (every memory access
needs translation)

------------------------------------------------------------------------

### Understanding Fragmentation: Visual Examples

Memory fragmentation comes in two forms: **external** and **internal**.
Understanding the difference is crucial for evaluating memory management
schemes.

#### External Fragmentation (The Problem with Variable-Size Segments)

External fragmentation occurs when free memory is scattered in small,
unusable chunks between allocated blocks.

**The Problem:**\
Free memory becomes fragmented into non-contiguous holes. Even when
sufficient total free memory exists, allocation requests may fail if
they require contiguous memory larger than the biggest hole.

**Real-World Example:**\
After a system runs for 24 hours with frequent allocations and
deallocations, 20-40% of memory can become unusable due to
fragmentation. A system might show 4 GB \"free\" but be unable to
allocate even 100 MB contiguously.

**Solutions:** - **Compaction:** Move allocated blocks to consolidate
free space (expensive - requires copying) - **Paging:** Use fixed-size
blocks to eliminate external fragmentation entirely

#### Internal Fragmentation (The Problem with Fixed-Size Pages)

Internal fragmentation occurs when allocated blocks are larger than
needed, wasting space **within** the allocated block.

**The Trade-off:**

| Page Size | Internal Fragmentation | Page Table Size | TLB Coverage |
| --- | --- | --- | --- |
| 1 KB | Low (max 1023 bytes waste) | Large (many entries) | Poor |
| 4 KB | Medium (max 4095 bytes waste) | Medium | Good |
| 2 MB | High (max 2 MB waste) | Small (few entries) | Excellent |


**Real-World Impact:**\
On a system with 16 GB RAM, 4 KB pages, and 100 processes: - Average
internal fragmentation per process: \~500 KB - Total wasted memory: \~50
MB (0.3% of RAM) - This is **predictable and acceptable**

Compare this to external fragmentation which can waste 20-40% of RAM
unpredictably.

#### Side-by-Side Comparison

**Summary Table:**

| Type | Location | Cause | Impact | Predictable? | Solution |
| --- | --- | --- | --- | --- | --- |
| **External** | Between blocks | Variable-size allocation | Can\'t use total free memory | No, gets worse over time | Compaction or paging |
| **Internal** | Within blocks | Fixed-size blocks | Wasted space in blocks | Yes, ≤ (page_size - 1) per allocation | Choose appropriate page size |


**Why Modern Systems Use Paging:**

External fragmentation is a **catastrophic problem**: memory becomes
increasingly unusable over time, and the only solution (compaction) is
expensive and disruptive. A system might show gigabytes of \"free\"
memory but fail to allocate even small contiguous blocks.

Internal fragmentation is a **manageable problem**: the waste is
bounded, predictable, and typically only 0.3-1% of total RAM with 4 KB
pages. The system always knows the maximum waste per allocation
(page_size - 1 bytes).

This is why virtually all modern operating systems use paging for memory
management\--accepting small, predictable waste to completely eliminate
large, unpredictable memory loss.

------------------------------------------------------------------------

## 1.4 Hierarchical Levels of Memory Management

Modern systems implement memory management at multiple levels:

### 1.4.1 Hardware Level: The Memory Management Unit (MMU)

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="620" viewBox="0 0 900 620" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter></defs>
  <rect width="900" height="620" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Virtual Memory Address Space Layout (Linux x86-64)</text>

  <!-- Process A address space -->
  <text x="160" y="68" style="fill:#1565C0; font-size:15; font-weight:bold; text-anchor:middle">Process A: Virtual Address Space</text>
  <text x="160" y="86" style="fill:#616161; font-size:13; text-anchor:middle">128 TB user space (0x0 – 0x7FFF...)</text>

  <rect x="30" y="96" width="260" height="490" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />

  <!-- Address space regions top to bottom (high to low addresses) -->
  <!-- Kernel space -->
  <rect x="38" y="104" width="244" height="44" rx="3" style="fill:#424242" />
  <text x="160" y="124" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Kernel Space</text>
  <text x="160" y="140" style="fill:#BDBDBD; font-size:12; text-anchor:middle">0xFFFF800000000000 – 0xFFFFFFFFFFFFFFFF</text>

  <!-- Dashed boundary -->
  <line x1="38" y1="148" x2="282" y2="148" style="stroke:#E65100; stroke-width:2; stroke-dasharray:6,3"></line>
  <text x="160" y="162" style="fill:#E65100; font-size:12; font-weight:bold; text-anchor:middle">Kernel / User Boundary (enforced by U/S bit)</text>

  <!-- Stack -->
  <rect x="38" y="170" width="244" height="44" rx="3" style="fill:#E65100" />
  <text x="160" y="191" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Stack</text>
  <text x="160" y="207" style="fill:#FFCCBC; font-size:12; text-anchor:middle">grows ↓  (0x7FFFFFFFFFFF...)</text>

  <!-- gap -->
  <rect x="38" y="216" width="244" height="28" rx="3" style="fill:#E8EAF6; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="160" y="234" style="fill:#616161; font-size:12; text-anchor:middle">[ unmapped – stack gap ]</text>

  <!-- Shared libs -->
  <rect x="38" y="246" width="244" height="36" rx="3" style="fill:#9E9E9E" />
  <text x="160" y="266" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Shared Libraries / mmap</text>
  <text x="160" y="280" style="fill:#E0E0E0; font-size:12; text-anchor:middle">libc.so, libpthread.so, etc.</text>

  <!-- gap -->
  <rect x="38" y="284" width="244" height="28" rx="3" style="fill:#E8EAF6; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="160" y="302" style="fill:#616161; font-size:12; text-anchor:middle">[ unmapped – large gap ]</text>

  <!-- Heap -->
  <rect x="38" y="314" width="244" height="40" rx="3" style="fill:#00796B" />
  <text x="160" y="336" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Heap (malloc/new)</text>
  <text x="160" y="352" style="fill:#B2DFDB; font-size:12; text-anchor:middle">grows ↑  (brk/mmap)</text>

  <!-- gap -->
  <rect x="38" y="356" width="244" height="24" rx="3" style="fill:#E8EAF6; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="160" y="372" style="fill:#616161; font-size:12; text-anchor:middle">[ unmapped ]</text>

  <!-- BSS -->
  <rect x="38" y="382" width="244" height="30" rx="3" style="fill:#00796B; opacity:0.78" />
  <text x="160" y="401" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">BSS (uninitialized data)</text>

  <!-- Data -->
  <rect x="38" y="414" width="244" height="30" rx="3" style="fill:#1565C0; opacity:0.7" />
  <text x="160" y="433" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Data (initialized globals)</text>

  <!-- Read-only data -->
  <rect x="38" y="446" width="244" height="30" rx="3" style="fill:#1565C0; opacity:0.8" />
  <text x="160" y="465" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Read-only Data (.rodata)</text>

  <!-- Text -->
  <rect x="38" y="478" width="244" height="40" rx="3" style="fill:#1565C0" />
  <text x="160" y="499" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Text (executable code)</text>
  <text x="160" y="515" style="fill:#BBDEFB; font-size:12; text-anchor:middle">0x400000 (typical start)</text>

  <!-- Null page -->
  <rect x="38" y="520" width="244" height="30" rx="3" style="fill:#B71C1C" />
  <text x="160" y="540" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">NULL Page (unmapped, addr 0)</text>

  <text x="160" y="574" style="fill:#616161; font-size:12; text-anchor:middle">0x0000000000000000</text>

  <!-- Address labels -->
  <text x="286" y="127" style="fill:#424242; font-size:12">0xFFFF...</text>
  <text x="286" y="195" style="fill:#E65100; font-size:12">0x7FFF...</text>
  <text x="286" y="402" style="fill:#212121; font-size:12">~0x601000</text>
  <text x="286" y="500" style="fill:#212121; font-size:12">0x400000</text>
  <text x="286" y="540" style="fill:#B71C1C; font-size:12">0x0</text>

  <!-- Physical Memory -->
  <text x="620" y="68" style="fill:#212121; font-size:15; font-weight:bold; text-anchor:middle">Physical Memory (RAM)</text>
  <text x="620" y="86" style="fill:#616161; font-size:13; text-anchor:middle">Shared across all processes</text>

  <rect x="490" y="96" width="260" height="490" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />

  <!-- Physical frames (scattered) -->
  <rect x="498" y="104" width="244" height="34" rx="3" style="fill:#424242" />
  <text x="620" y="125" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">OS Kernel (always resident)</text>

  <rect x="498" y="140" width="244" height="28" rx="3" style="fill:#9E9E9E" />
  <text x="620" y="158" style="fill:#FFFFFF; font-size:13; text-anchor:middle">Frame: libc.so (shared)</text>

  <rect x="498" y="170" width="244" height="28" rx="3" style="fill:#E65100; opacity:0.7" />
  <text x="620" y="188" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Frame: Proc A Stack</text>

  <rect x="498" y="200" width="244" height="28" rx="3" style="fill:#E0E0E0" />
  <text x="620" y="218" style="fill:#616161; font-size:13; text-anchor:middle">Frame: (free)</text>

  <rect x="498" y="230" width="244" height="28" rx="3" style="fill:#00796B; opacity:0.7" />
  <text x="620" y="248" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Frame: Proc A Heap</text>

  <rect x="498" y="260" width="244" height="28" rx="3" style="fill:#E65100; opacity:0.5" />
  <text x="620" y="278" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Frame: Proc B Stack</text>

  <rect x="498" y="290" width="244" height="28" rx="3" style="fill:#E0E0E0" />
  <text x="620" y="308" style="fill:#616161; font-size:13; text-anchor:middle">Frame: (free)</text>

  <rect x="498" y="320" width="244" height="28" rx="3" style="fill:#1565C0; opacity:0.6" />
  <text x="620" y="338" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Frame: Proc A BSS/Data</text>

  <rect x="498" y="350" width="244" height="28" rx="3" style="fill:#00796B; opacity:0.5" />
  <text x="620" y="368" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Frame: Proc B Heap</text>

  <rect x="498" y="380" width="244" height="28" rx="3" style="fill:#9E9E9E; opacity:0.6" />
  <text x="620" y="398" style="fill:#FFFFFF; font-size:13; text-anchor:middle">Frame: libpthread.so</text>

  <rect x="498" y="410" width="244" height="28" rx="3" style="fill:#1565C0; opacity:0.8" />
  <text x="620" y="428" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Frame: Proc A .text</text>

  <rect x="498" y="440" width="244" height="28" rx="3" style="fill:#E0E0E0" />
  <text x="620" y="458" style="fill:#616161; font-size:13; text-anchor:middle">Frame: (free)</text>

  <rect x="498" y="470" width="244" height="28" rx="3" style="fill:#1565C0; opacity:0.5" />
  <text x="620" y="488" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Frame: Proc B .text</text>

  <rect x="498" y="500" width="244" height="28" rx="3" style="fill:#E0E0E0" />
  <text x="620" y="518" style="fill:#616161; font-size:13; text-anchor:middle">Frame: (free)</text>

  <text x="620" y="560" style="fill:#616161; font-size:12; text-anchor:middle">Physical Address 0x0</text>
  <text x="620" y="578" style="fill:#616161; font-size:12; text-anchor:middle">to 0x(RAM size)</text>

  <!-- Key insight box -->
  <rect x="762" y="96" width="126" height="490" rx="6" filter="url(#sh)" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:1.5" />
  <text x="825" y="120" style="fill:#2E7D32; font-size:13; font-weight:bold; text-anchor:middle">Key Insights</text>
  <text x="772" y="148" style="fill:#212121; font-size:11">Virtual spaces</text>
  <text x="772" y="162" style="fill:#212121; font-size:11">are huge:</text>
  <text x="772" y="176" style="fill:#1565C0; font-size:12; font-weight:bold">128 TB each</text>
  <line x1="772" y1="192" x2="876" y2="192" style="stroke:#BDBDBD; stroke-width:1"></line>
  <text x="772" y="210" style="fill:#212121; font-size:11">Physical RAM</text>
  <text x="772" y="224" style="fill:#212121; font-size:11">is shared +</text>
  <text x="772" y="238" style="fill:#212121; font-size:11">much smaller</text>
  <line x1="772" y1="254" x2="876" y2="254" style="stroke:#BDBDBD; stroke-width:1"></line>
  <text x="772" y="272" style="fill:#212121; font-size:11">Pages can be</text>
  <text x="772" y="286" style="fill:#212121; font-size:11">anywhere in</text>
  <text x="772" y="300" style="fill:#212121; font-size:11">physical RAM</text>
  <line x1="772" y1="316" x2="876" y2="316" style="stroke:#BDBDBD; stroke-width:1"></line>
  <text x="772" y="334" style="fill:#212121; font-size:11">Unmapped</text>
  <text x="772" y="348" style="fill:#212121; font-size:11">regions use</text>
  <text x="772" y="362" style="fill:#212121; font-size:11">NO physical</text>
  <text x="772" y="376" style="fill:#212121; font-size:11">RAM at all!</text>
  <line x1="772" y1="392" x2="876" y2="392" style="stroke:#BDBDBD; stroke-width:1"></line>
  <text x="772" y="410" style="fill:#212121; font-size:11">Kernel space</text>
  <text x="772" y="424" style="fill:#212121; font-size:11">mapped in all</text>
  <text x="772" y="438" style="fill:#212121; font-size:11">processes but</text>
  <text x="772" y="452" style="fill:#212121; font-size:11">U/S bit blocks</text>
  <text x="772" y="466" style="fill:#212121; font-size:11">user access</text>
  <line x1="772" y1="482" x2="876" y2="482" style="stroke:#BDBDBD; stroke-width:1"></line>
  <text x="772" y="500" style="fill:#2E7D32; font-size:11">libc.so pages</text>
  <text x="772" y="514" style="fill:#2E7D32; font-size:11">shared in</text>
  <text x="772" y="528" style="fill:#2E7D32; font-size:11">physical RAM</text>
  <text x="772" y="542" style="fill:#2E7D32; font-size:11">between all</text>
  <text x="772" y="556" style="fill:#2E7D32; font-size:11">processes!</text>
</svg>
</div>
<figcaption><strong>Figure 1.9:</strong> Virtual address space layout:
kernel space at the top; user space holds stack (grows down), heap
(grows up), BSS, data, and code segments.</figcaption>
</figure>

The MMU is a specialized hardware component, integrated into the CPU,
that performs address translation at hardware speed.

**Core MMU Responsibilities:** 1. **Address Translation:** Convert
virtual → physical addresses 2. **TLB Management:** Cache recent
translations 3. **Protection Checking:** Enforce access permissions 4.
**Exception Generation:** Trigger page faults when needed

**MMU Pipeline Integration:**

    Instruction Fetch → Instruction TLB → Instruction Cache → Decode
                                    ↓
                             Physical Address
                             
    Data Access → Data TLB → Data Cache → Load/Store Unit
                       ↓
                Physical Address

The MMU operates in parallel with the CPU pipeline. Any TLB miss stalls
the pipeline while the page table is walked.

**Historical Note:**\
Early CPUs like the Motorola 68020 had optional external MMU chips
(68851). Modern CPUs integrate the MMU on-die for performance.

### 1.4.2 Operating System Level: The Virtual Memory Manager

The OS kernel manages: - **Page table maintenance:** Creating/updating
page tables for processes - **Page fault handling:** Loading pages from
disk when absent - **Page replacement:** Choosing which pages to evict
under memory pressure - **Swapping:** Moving entire processes to/from
disk - **Memory allocation:** Allocating frames to processes

**Key OS Data Structures:**

``` {.sourceCode .c}
// Linux kernel mm_struct (simplified)
struct mm_struct {
    pgd_t *pgd;                    // Page Global Directory (root page table)
    unsigned long start_code;       // Code segment start
    unsigned long end_code;         // Code segment end
    unsigned long start_data;       // Data segment start
    unsigned long end_data;         // Data segment end
    unsigned long start_brk;        // Heap start
    unsigned long brk;              // Heap end (current)
    unsigned long start_stack;      // Stack start
    unsigned long total_vm;         // Total virtual memory pages
    unsigned long locked_vm;        // Locked pages (mlocked)
    unsigned long pinned_vm;        // Pinned pages
    unsigned long data_vm;          // Data pages
    unsigned long exec_vm;          // Executable pages
    unsigned long stack_vm;         // Stack pages
};
```

**Page Fault Handling Flow:**

    1. CPU accesses virtual address
    2. TLB miss → Page table walk
    3. Page not present → Page Fault Exception
    4. CPU switches to kernel mode, saves context
    5. OS page fault handler invoked:
       a. Check if address is valid (in process's VMA)
       b. If invalid → Segmentation Fault (kill process)
       c. If valid but not resident:
          - Allocate physical frame
          - If swapped: Read page from disk
          - If zero-page: Zero the frame
          - If file-backed: Read from file
          - Update page table entry
          - Mark page as present
    6. Return from exception
    7. CPU retries the faulting instruction
    8. Translation succeeds → execution continues

### 1.4.3 Application Level: Memory Allocation Libraries

Applications don\'t usually manage memory at the page level. Instead,
they use allocation libraries:

**C/C++:**

``` {.sourceCode .c}
void* malloc(size_t size);
void free(void* ptr);
void* calloc(size_t nmemb, size_t size);
void* realloc(void* ptr, size_t size);
```

**How malloc() Works (Simplified):**

``` {.sourceCode .c}
// glibc malloc implementation strategy
void* malloc(size_t size) {
    if (size < MMAP_THRESHOLD) {
        // Small allocation: use heap (brk/sbrk)
        return allocate_from_heap(size);
    } else {
        // Large allocation: use mmap()
        return mmap(NULL, size, PROT_READ|PROT_WRITE,
                    MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    }
}
```

**Behind the Scenes:** - Small allocations (\<128 KB): Use heap via
`brk()` system call - Large allocations: Use `mmap()` to map anonymous
memory - Free list management (bins, arenas) - Metadata overhead
(headers, footers)

**Memory Allocation Hierarchy:**

    Application calls malloc()
            ↓
    C Library (glibc)
            ↓
    System Call (brk/mmap)
            ↓
    Kernel (page allocator)
            ↓
    MMU (page table update)
            ↓
    Physical Memory Assignment

------------------------------------------------------------------------

## 1.5 The Virtual Memory Abstraction

Virtual memory is one of computer science\'s most powerful abstractions.
It provides each process with the illusion of: 1. **Vast address space**
(often larger than physical RAM) 2. **Contiguous memory** (even if
physical memory is fragmented) 3. **Private memory** (isolated from
other processes) 4. **Uniform access** (same addressing model for all
memory)

### 1.5.1 Benefits of Virtual Memory

#### Benefit 1: Simplified Programming Model

Programmers can assume: - Memory starts at address 0 - Memory is
contiguous - Pointers just work (within the valid address space) - No
need to manage physical memory locations

#### Benefit 2: Memory Overcommitment

Physical memory can be overcommitted\--the sum of all virtual address
spaces can exceed physical RAM.

**Real Example:**

    Physical RAM: 16 GB
    Process 1:    8 GB virtual
    Process 2:    8 GB virtual  
    Process 3:    8 GB virtual
    Total:       24 GB virtual   → More than physical!

This works because: - Not all virtual pages are actually in use - Pages
can be swapped to disk - Many pages are shared (code, libraries)

#### Benefit 3: Security and Isolation

Each process has its own page table. Process A cannot access Process
B\'s memory.

    Process A's view:
    0x00000000 - 0x7FFFFFFF: User space
    0x80000000 - 0xFFFFFFFF: Kernel space

    Process B's view:  
    0x00000000 - 0x7FFFFFFF: User space (different physical frames!)
    0x80000000 - 0xFFFFFFFF: Kernel space (same physical frames)

#### Benefit 4: Memory-Mapped Files

Files can be mapped into virtual memory. Reading/writing memory
reads/writes the file.

``` {.sourceCode .c}
// Map a file into memory
int fd = open("database.db", O_RDWR);
void* ptr = mmap(NULL, file_size, PROT_READ|PROT_WRITE,
                 MAP_SHARED, fd, 0);
// Now ptr[x] reads/writes the file!
```

#### Benefit 5: Copy-on-Write (COW)

When `fork()` creates a child process, both parent and child initially
share the same physical pages (marked read-only). Only when one writes
to a page is it duplicated.

    Parent calls fork()
            ↓
    Child created with identical page tables
            ↓
    Both point to same physical frames (read-only)
            ↓
    Parent writes to page → Page Fault
            ↓
    Kernel copies page, updates parent's page table
            ↓
    Parent has private copy, child still has original

This makes `fork()` extremely fast, even for large processes.

### 1.5.2 The Cost of Virtual Memory

Virtual memory isn\'t free:

1.  **Translation overhead:** Every memory access requires address
    translation
2.  **TLB misses:** Cache misses in the TLB require expensive page table
    walks
3.  **Page table memory:** Page tables themselves consume memory
4.  **Page faults:** Loading pages from disk is extremely slow

**Performance Impact Example:**

``` {.sourceCode .c}
// Sequential access (good locality)
for (i = 0; i < ARRAY_SIZE; i++) {
    sum += array[i];
}
// TLB hit rate: ~99%+

// Random access (poor locality)  
for (i = 0; i < ARRAY_SIZE; i++) {
    sum += array[rand() % ARRAY_SIZE];
}
// TLB hit rate: can drop to 50% or worse
```

------------------------------------------------------------------------

## 1.6 Key Concepts and Terminology

Before diving deeper, let\'s establish precise definitions:

### Address Spaces

**Virtual Address:** The address used by a program (logical address)\
**Physical Address:** The actual address in RAM hardware\
**Address Space:** The set of all valid addresses (e.g., 32-bit = 4 GB
address space)

### Pages and Frames

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="480" viewBox="0 0 900 480" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter></defs>
  <rect width="900" height="480" style="fill:#FAFAFA" />
  <text x="450" y="36" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Virtual Address Format: 4 KB Paging (32-bit and 64-bit)</text>

  <!-- ===== 32-BIT ===== -->
  <text x="450" y="64" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">32-bit Virtual Address (4 GB address space, two-level paging)</text>

  <!-- Bit positions -->
  <text x="130" y="80" style="fill:#616161; font-size:11; text-anchor:middle">31</text>
  <text x="367" y="80" style="fill:#616161; font-size:11; text-anchor:middle">22</text>
  <text x="407" y="80" style="fill:#616161; font-size:11; text-anchor:middle">21</text>
  <text x="567" y="80" style="fill:#616161; font-size:11; text-anchor:middle">12</text>
  <text x="607" y="80" style="fill:#616161; font-size:11; text-anchor:middle">11</text>
  <text x="800" y="80" style="fill:#616161; font-size:11; text-anchor:middle">0</text>

  <rect x="20" y="86" width="360" height="50" rx="5" filter="url(#sh)" style="fill:#1565C0" />
  <text x="200" y="107" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Page Directory Index</text>
  <text x="200" y="125" style="fill:#BBDEFB; font-size:13; text-anchor:middle">bits 31:22 — 10 bits → 1024 entries in PD</text>

  <rect x="386" y="86" width="190" height="50" rx="5" filter="url(#sh)" style="fill:#00796B" />
  <text x="481" y="107" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Page Table Index</text>
  <text x="481" y="125" style="fill:#B2DFDB; font-size:13; text-anchor:middle">bits 21:12 — 10 bits</text>

  <rect x="582" y="86" width="298" height="50" rx="5" filter="url(#sh)" style="fill:#E65100" />
  <text x="731" y="107" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Page Offset</text>
  <text x="731" y="125" style="fill:#FFE0B2; font-size:13; text-anchor:middle">bits 11:0 — 12 bits → 4096 bytes (4 KB)</text>

  <!-- ===== 64-BIT ===== -->
  <text x="450" y="162" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">48-bit Virtual Address (x86-64, 256 TB address space, four-level paging)</text>

  <text x="48" y="178" style="fill:#616161; font-size:10; text-anchor:middle">47</text>
  <text x="176" y="178" style="fill:#616161; font-size:10; text-anchor:middle">39</text>
  <text x="196" y="178" style="fill:#616161; font-size:10; text-anchor:middle">38</text>
  <text x="320" y="178" style="fill:#616161; font-size:10; text-anchor:middle">30</text>
  <text x="340" y="178" style="fill:#616161; font-size:10; text-anchor:middle">29</text>
  <text x="465" y="178" style="fill:#616161; font-size:10; text-anchor:middle">21</text>
  <text x="484" y="178" style="fill:#616161; font-size:10; text-anchor:middle">20</text>
  <text x="610" y="178" style="fill:#616161; font-size:10; text-anchor:middle">12</text>
  <text x="630" y="178" style="fill:#616161; font-size:10; text-anchor:middle">11</text>
  <text x="867" y="178" style="fill:#616161; font-size:10; text-anchor:middle">0</text>

  <rect x="20" y="184" width="165" height="50" rx="5" filter="url(#sh)" style="fill:#1565C0" />
  <text x="102" y="205" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">PML4 Index</text>
  <text x="102" y="222" style="fill:#BBDEFB; font-size:11; text-anchor:middle">9 bits (47:39)</text>

  <rect x="188" y="184" width="140" height="50" rx="5" filter="url(#sh)" style="fill:#00796B" />
  <text x="258" y="205" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">PDPT Index</text>
  <text x="258" y="222" style="fill:#B2DFDB; font-size:11; text-anchor:middle">9 bits (38:30)</text>

  <rect x="332" y="184" width="140" height="50" rx="5" filter="url(#sh)" style="fill:#5C6BC0" />
  <text x="402" y="205" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">PD Index</text>
  <text x="402" y="222" style="fill:#E8EAF6; font-size:11; text-anchor:middle">9 bits (29:21)</text>

  <rect x="476" y="184" width="140" height="50" rx="5" filter="url(#sh)" style="fill:#E65100" />
  <text x="546" y="205" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">PT Index</text>
  <text x="546" y="222" style="fill:#FFE0B2; font-size:11; text-anchor:middle">9 bits (20:12)</text>

  <rect x="620" y="184" width="260" height="50" rx="5" filter="url(#sh)" style="fill:#37474F" />
  <text x="750" y="205" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Page Offset</text>
  <text x="750" y="222" style="fill:#B0BEC5; font-size:13; text-anchor:middle">12 bits (11:0) → 4 KB</text>

  <!-- ===== OFFSET STAYS THE SAME ANNOTATION ===== -->
  <rect x="20" y="252" width="860" height="50" rx="4" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:1.5" />
  <text x="450" y="272" style="fill:#2E7D32; font-size:14; font-weight:bold; text-anchor:middle">Key Rule: The Page Offset is NEVER translated — it passes through unchanged</text>
  <text x="450" y="292" style="fill:#212121; font-size:13; text-anchor:middle">Only the VPN (upper bits) changes during translation. The offset selects the byte within the page. Offset = VA mod 4096.</text>

  <!-- ===== COMPARISON TABLE ===== -->
  <rect x="20" y="316" width="860" height="140" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="450" y="336" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Page Size vs. Offset Bits</text>

  <rect x="30" y="346" width="840" height="26" rx="2" style="fill:#37474F" />
  <text x="200" y="363" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Page Size</text>
  <text x="400" y="363" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Offset Bits</text>
  <text x="600" y="363" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">VPN Bits (32-bit)</text>
  <text x="780" y="363" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">VPN Bits (48-bit)</text>

  <rect x="30" y="372" width="840" height="26" rx="2" style="fill:#E3F2FD" />
  <text x="200" y="389" style="fill:#1565C0; font-size:13; text-anchor:middle">4 KB  (standard)</text>
  <text x="400" y="389" style="fill:#212121; font-size:13; text-anchor:middle">12 bits</text>
  <text x="600" y="389" style="fill:#212121; font-size:13; text-anchor:middle">20 bits</text>
  <text x="780" y="389" style="fill:#212121; font-size:13; text-anchor:middle">36 bits (4 levels × 9)</text>

  <rect x="30" y="398" width="840" height="26" rx="2" style="fill:#E0F2F1" />
  <text x="200" y="412" style="fill:#00796B; font-size:12; text-anchor:middle">2 MB huge page</text>
  <text x="400" y="412" style="fill:#212121; font-size:12; text-anchor:middle">21 bits</text>
  <text x="600" y="412" style="fill:#212121; font-size:12; text-anchor:middle">11 bits</text>
  <text x="780" y="412" style="fill:#212121; font-size:12; text-anchor:middle">27 bits (3 levels)</text>
</svg>
</div>
<figcaption><strong>Figure 1.10:</strong> Virtual address bit layout for
x86-64: bits 47-39 index PGD, 38-30 PUD, 29-21 PMD, 20-12 PTE, and 11-0
are the page offset.</figcaption>
</figure>

**Page:** A fixed-size block of virtual memory (typically 4 KB)\
**Frame:** A fixed-size block of physical memory (same size as page)\
**Page Number:** The high-order bits of a virtual address\
**Offset:** The low-order bits (position within the page)

### Page Tables

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="400" viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter></defs>
  <rect width="900" height="400" style="fill:#FAFAFA" />
  <text x="450" y="36" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Physical Address Format: Frame Number + Offset</text>

  <!-- Physical address bar -->
  <text x="450" y="62" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">52-bit Physical Address (x86-64, supports up to 4 PB physical RAM)</text>

  <text x="200" y="78" style="fill:#616161; font-size:11; text-anchor:middle">bit 51</text>
  <text x="550" y="78" style="fill:#616161; font-size:11; text-anchor:middle">bit 12</text>
  <text x="590" y="78" style="fill:#616161; font-size:11; text-anchor:middle">bit 11</text>
  <text x="800" y="78" style="fill:#616161; font-size:11; text-anchor:middle">bit 0</text>

  <!-- PFN field -->
  <rect x="20" y="84" width="555" height="60" rx="6" filter="url(#sh)" style="fill:#00796B" />
  <text x="297" y="108" style="fill:#FFFFFF; font-size:16; font-weight:bold; text-anchor:middle">Physical Frame Number (PFN)</text>
  <text x="297" y="132" style="fill:#B2DFDB; font-size:14; text-anchor:middle">40 bits (51:12) — which 4 KB frame in physical RAM</text>

  <!-- Offset field (identical to VA offset) -->
  <rect x="581" y="84" width="299" height="60" rx="6" filter="url(#sh)" style="fill:#E65100" />
  <text x="730" y="108" style="fill:#FFFFFF; font-size:16; font-weight:bold; text-anchor:middle">Page Offset</text>
  <text x="730" y="132" style="fill:#FFE0B2; font-size:14; text-anchor:middle">12 bits — identical to VA offset</text>

  <!-- Annotation: offset same -->
  <rect x="20" y="162" width="860" height="42" rx="4" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:1.5" />
  <text x="450" y="179" style="fill:#2E7D32; font-size:14; font-weight:bold; text-anchor:middle">The 12-bit offset is identical in the virtual and physical address — it is never changed</text>
  <text x="450" y="197" style="fill:#212121; font-size:13; text-anchor:middle">Only the upper bits change: VPN (virtual) is replaced with PFN (physical) via the page table lookup</text>

  <!-- Worked example -->
  <rect x="20" y="220" width="860" height="160" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="450" y="242" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Worked Example: Full Address Translation</text>

  <!-- Virtual address breakdown -->
  <text x="35" y="266" style="fill:#1565C0; font-size:13; font-weight:bold">Virtual Address:  0x0000_7FFF_0010_0A40</text>
  <text x="35" y="284" style="fill:#424242; font-size:13">  VPN (bits 47:12) = 0x7FFF_0010_0   →  page table lookup  →  PFN = 0x000_0000_5A</text>
  <text x="35" y="302" style="fill:#424242; font-size:13">  Offset (bits 11:0) = 0xA40  →  unchanged</text>

  <line x1="35" y1="312" x2="865" y2="312" style="stroke:#9E9E9E; stroke-width:1; stroke-dasharray:4,3"></line>

  <text x="35" y="330" style="fill:#00796B; font-size:13; font-weight:bold">Physical Address:  0x5A_000 × 4096 + 0xA40</text>
  <text x="35" y="348" style="fill:#1565C0; font-size:15; font-weight:bold">                 = 0x0000_005A_000_0A40</text>
  <text x="35" y="366" style="fill:#616161; font-size:13">PFN 0x5A = Frame 90 in physical RAM — starts at byte 90 × 4096 = 368,640 (0x5A000)</text>
</svg>
</div>
<figcaption><strong>Figure 1.11:</strong> Physical address format: the
Physical Frame Number (PFN) occupies the upper bits; the page offset
(copied from the virtual address) occupies the lower 12
bits.</figcaption>
</figure>

**Page Table:** Data structure mapping virtual pages to physical frames\
**Page Table Entry (PTE):** One entry in the page table\
**Page Directory:** Higher-level page table (in multi-level schemes)\
**Translation Lookaside Buffer (TLB):** Hardware cache of recent
translations

### Page States

**Resident:** Page is in physical memory\
**Swapped:** Page is on disk (swap space)\
**Dirty:** Page has been modified\
**Present:** Page is accessible (resident and valid)\
**Valid:** Address is within process\'s address space

### Memory Operations

**Page Fault:** Exception when accessing a non-present page\
**Swapping:** Moving entire processes to/from disk\
**Paging:** Moving individual pages to/from disk\
**Thrashing:** System spends more time paging than executing

------------------------------------------------------------------------

## 1.7 A Concrete Example: Address Translation

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="620" viewBox="0 0 900 620" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
    <marker id="ab" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="at" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker>
  </defs>
  <rect width="900" height="620" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Step-by-Step Address Translation Example (32-bit, 4 KB pages)</text>

  <!-- Input: Virtual Address -->
  <rect x="30" y="60" width="840" height="68" rx="6" filter="url(#sh)" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:2" />
  <text x="50" y="84" style="fill:#1565C0; font-size:14; font-weight:bold">Virtual Address:  0x00403A7C</text>
  <text x="50" y="104" style="fill:#212121; font-size:13">Binary: 0000 0000 0100 0000 0011 1010 0111 1100</text>
  <text x="500" y="84" style="fill:#212121; font-size:13">|   Page size = 4 KB = 2^12 bytes   |   Page table entry size = 4 bytes</text>
  <text x="500" y="104" style="fill:#212121; font-size:13">|   Virtual Page Number (VPN) = upper 20 bits = 0x403</text>

  <!-- Step 1: Split -->
  <text x="30" y="152" style="fill:#212121; font-size:15; font-weight:bold">Step 1 — Split Virtual Address into VPN and Offset:</text>

  <!-- Bit breakdown -->
  <rect x="30" y="162" width="500" height="48" rx="4" style="fill:#1565C0" />
  <text x="200" y="183" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">VPN: bits 31-12</text>
  <text x="200" y="200" style="fill:#BBDEFB; font-size:14; text-anchor:middle">0x00403  (virtual page number)</text>
  <rect x="530" y="162" width="210" height="48" rx="4" style="fill:#E65100" />
  <text x="635" y="183" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Offset: bits 11-0</text>
  <text x="635" y="200" style="fill:#FFCCBC; font-size:14; text-anchor:middle">0xA7C  (byte in page)</text>

  <!-- Step 2: TLB Lookup -->
  <text x="30" y="236" style="fill:#212121; font-size:15; font-weight:bold">Step 2 — TLB Lookup with VPN:</text>
  <rect x="20" y="246" width="390" height="108" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />
  <text x="40" y="268" style="fill:#212121; font-size:13">Check TLB for VPN = 0x00403</text>
  <text x="40" y="288" style="fill:#2E7D32; font-size:13; font-weight:bold">TLB HIT!  PFN = 0x1B7  (found in TLB)</text>
  <text x="40" y="308" style="fill:#212121; font-size:13">TLB also confirms: R/W=1, U/S=1 (user writable)</text>
  <text x="40" y="328" style="fill:#212121; font-size:13">Latency: ~1–4 cycles (1 ns)</text>

  <!-- OR miss path -->
  <rect x="490" y="246" width="380" height="130" rx="6" filter="url(#sh)" style="fill:#FFF3E0; stroke:#E65100; stroke-width:2" />
  <text x="500" y="268" style="fill:#212121; font-size:13">If TLB MISS: Hardware walks page table</text>
  <text x="500" y="288" style="fill:#E65100; font-size:13; font-weight:bold">4 DRAM reads to find PFN</text>
  <text x="500" y="308" style="fill:#212121; font-size:13">PML4[0] → PDPT[0] → PD[1] → PT[0x003]</text>
  <text x="500" y="328" style="fill:#212121; font-size:13">PTE found: PFN = 0x1B7, then update TLB</text>
  <text x="500" y="344" style="fill:#212121; font-size:13">Latency: ~280 ns penalty</text>

  <text x="450" y="308" style="fill:#616161; font-size:16; font-weight:bold; text-anchor:middle">— OR —</text>

  <!-- Step 3: Compute PA -->
  <text x="30" y="400" style="fill:#212121; font-size:15; font-weight:bold">Step 3 — Compute Physical Address:</text>
  <rect x="30" y="410" width="840" height="80" rx="6" filter="url(#sh)" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:2" />
  <text x="50" y="434" style="fill:#2E7D32; font-size:14; font-weight:bold">Physical Address = PFN shifted left by 12 bits | Offset</text>
  <text x="50" y="458" style="fill:#212121; font-size:14">= 0x1B7 &lt;&lt; 12 | 0xA7C</text>
  <text x="50" y="480" style="fill:#212121; font-size:14">= 0x001B7000 | 0xA7C</text>
  <text x="400" y="434" style="fill:#2E7D32; font-size:14; font-weight:bold">= 0x001B7A7C</text>
  <text x="400" y="458" style="fill:#212121; font-size:13">The CPU now accesses physical address 0x001B7A7C in DRAM</text>
  <text x="400" y="480" style="fill:#212121; font-size:13">The page offset (0xA7C) is passed through unchanged!</text>

  <!-- Step 4: Summary -->
  <rect x="30" y="508" width="840" height="64" rx="6" filter="url(#sh)" style="fill:#1565C0" />
  <text x="50" y="532" style="fill:#FFFFFF; font-size:14; font-weight:bold">Summary of Translation:  VA: 0x00403A7C  →  [MMU: VPN=0x403, lookup, PFN=0x1B7]  →  PA: 0x001B7A7C</text>
  <text x="50" y="558" style="fill:#BBDEFB; font-size:13">The program uses VA 0x403A7C. The hardware silently and invisibly maps it to PA 0x1B7A7C. Program never knows!</text>
</svg>
</div>
<figcaption><strong>Figure 1.12:</strong> Step-by-step address
translation: virtual address decomposed into VPN and offset; TLB or page
table supplies PFN; physical address assembled.</figcaption>
</figure>

Let\'s trace a complete memory access from virtual address to physical
address.

**System Configuration:** - 32-bit address space - 4 KB (2\^12 byte)
pages - 1 GB (2\^30 byte) physical RAM = 256K frames

**Virtual Address:** 0x12345678

**Step 1: Split address into page number and offset**

**Step 2: Look up in TLB**

    TLB lookup for VPN 0x12345...
    TLB HIT! → Physical Frame Number: 0xA2B4C

**Step 3: Construct physical address**

    Physical Frame: 0xA2B4C
    Offset:         0x678

    Physical Address = (Frame Number << 12) | Offset
                     = (0xA2B4C << 12) | 0x678
                     = 0xA2B4C678

**Step 4: Access physical memory**

    Read from physical address 0xA2B4C678

**If TLB Miss had occurred:**

    TLB miss for VPN 0x12345
    → Hardware page table walk:
      1. Read Page Directory entry
      2. Read Page Table entry  
      3. Extract Physical Frame Number: 0xA2B4C
      4. Load into TLB
      5. Retry access (now TLB hit)

**If Page Not Present:**

    Page table entry for VPN 0x12345 has Present bit = 0
    → Page Fault Exception
    → Kernel page fault handler:
      1. Check if address valid
      2. Allocate physical frame
      3. Load page from disk (if swapped)
      4. Update PTE: Frame = 0xA2B4C, Present = 1
      5. Return from exception
    → CPU retries instruction (now page is present)

------------------------------------------------------------------------

## 1.8 The Translation Lookaside Buffer (TLB)

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="920" height="700" viewBox="0 0 920 700" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
    <!-- All markers use userSpaceOnUse — absolute pixel sizes, no stroke-width scaling -->
    <marker id="ab" markerunits="userSpaceOnUse" markerwidth="12" markerheight="9" refx="11" refy="4.5" orient="auto"><polygon points="0 0,12 4.5,0 9" style="fill:#1565C0"></polygon></marker>
    <marker id="at" markerunits="userSpaceOnUse" markerwidth="12" markerheight="9" refx="11" refy="4.5" orient="auto"><polygon points="0 0,12 4.5,0 9" style="fill:#2E7D32"></polygon></marker>
    <marker id="ao" markerunits="userSpaceOnUse" markerwidth="12" markerheight="9" refx="11" refy="4.5" orient="auto"><polygon points="0 0,12 4.5,0 9" style="fill:#E65100"></polygon></marker>
    <marker id="ateal" markerunits="userSpaceOnUse" markerwidth="12" markerheight="9" refx="11" refy="4.5" orient="auto"><polygon points="0 0,12 4.5,0 9" style="fill:#00796B"></polygon></marker>
    <marker id="ag" markerunits="userSpaceOnUse" markerwidth="12" markerheight="9" refx="11" refy="4.5" orient="auto"><polygon points="0 0,12 4.5,0 9" style="fill:#616161"></polygon></marker>
    <!-- Upward-pointing (for arrows entering boxes from below) -->
    <marker id="ao-up" markerunits="userSpaceOnUse" markerwidth="9" markerheight="12" refx="4.5" refy="11" orient="auto"><polygon points="0 12,4.5 0,9 12" style="fill:#E65100"></polygon></marker>
  </defs>
  <rect width="920" height="700" style="fill:#FAFAFA" />

  <!-- Title -->
  <text x="460" y="34" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Complete Address Translation Flow: TLB Hit and Miss Paths</text>

  <!-- ══════════════════════════════════════════════
       ROW 1: CPU  (centered at x=490)
  ══════════════════════════════════════════════ -->
  <rect x="390" y="52" width="200" height="58" rx="6" filter="url(#sh)" style="fill:#1565C0" />
  <text x="490" y="77" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">CPU Issues</text>
  <text x="490" y="95" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Virtual Address</text>
  <text x="490" y="111" style="fill:#BBDEFB; font-size:11; text-anchor:middle">VA = 0x7FFF5000</text>

  <!-- CPU → TLB -->
  <line x1="490" y1="110" x2="490" y2="141" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:2.5"></line>
  <text x="502" y="130" style="fill:#616161; font-size:11">VPN lookup</text>

  <!-- ══════════════════════════════════════════════
       ROW 2: TLB — x=370, w=240, right=610, y=143, h=58, bottom=201
  ══════════════════════════════════════════════ -->
  <rect x="370" y="143" width="240" height="58" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />
  <text x="490" y="168" style="fill:#212121; font-size:15; font-weight:bold; text-anchor:middle">TLB</text>
  <text x="490" y="186" style="fill:#424242; font-size:13; text-anchor:middle">Translation Lookaside Buffer</text>

  <!-- TLB → HIT diagonal (left) -->
  <text x="218" y="229" style="fill:#2E7D32; font-size:13; font-weight:bold">HIT (~95%)</text>
  <line x1="385" y1="199" x2="315" y2="247" marker-end="url(#at)" style="stroke:#2E7D32; stroke-width:2.5"></line>

  <!-- TLB → MISS diagonal (right) -->
  <text x="572" y="229" style="fill:#E65100; font-size:13; font-weight:bold">MISS (~5%)</text>
  <line x1="595" y1="199" x2="659" y2="247" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2.5"></line>

  <!-- ══════════════════════════════════════════════
       LEFT: HIT path — column centered ~x=259
       PFN box: x=165, w=188, right=353, center=259, y=249, h=54, bottom=303
  ══════════════════════════════════════════════ -->
  <rect x="165" y="249" width="188" height="54" rx="6" filter="url(#sh)" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:2" />
  <text x="259" y="274" style="fill:#2E7D32; font-size:13; font-weight:bold; text-anchor:middle">PFN Found in TLB</text>
  <text x="259" y="294" style="fill:#424242; font-size:12; text-anchor:middle">Latency: 1–4 cycles</text>

  <!-- HIT → Physical Address straight down -->
  <line x1="259" y1="303" x2="259" y2="355" marker-end="url(#at)" style="stroke:#2E7D32; stroke-width:2.5"></line>
  <text x="271" y="335" style="fill:#2E7D32; font-size:12; font-weight:bold">Fast path!</text>

  <!-- ══════════════════════════════════════════════
       RIGHT: MISS path — column centered ~x=684
       Walker: x=596, w=188, right=784, center=690, y=249, h=54, bottom=303
  ══════════════════════════════════════════════ -->
  <rect x="596" y="249" width="188" height="54" rx="6" filter="url(#sh)" style="fill:#FFF3E0; stroke:#E65100; stroke-width:2" />
  <text x="690" y="274" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Page Table Walker</text>
  <text x="690" y="294" style="fill:#424242; font-size:12; text-anchor:middle">Hardware page walk</text>

  <!-- Walker → Page Tables (DRAM) -->
  <line x1="690" y1="303" x2="690" y2="353" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2.5"></line>
  <text x="703" y="334" style="fill:#E65100; font-size:12">4 accesses</text>

  <!-- Page Tables (DRAM): x=596, w=188, right=784, center=690, y=355, h=66, bottom=421 -->
  <rect x="596" y="355" width="188" height="66" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />
  <text x="690" y="377" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">Page Tables (DRAM)</text>
  <text x="690" y="394" style="fill:#424242; font-size:12; text-anchor:middle">~70 ns each read</text>
  <text x="690" y="412" style="fill:#E65100; font-size:12; text-anchor:middle">Total: ~280 ns miss cost</text>

  <!-- ══════════════════════════════════════════════
       UPDATE TLB feedback:
       Route ABOVE the HIT/MISS boxes — exits PT top edge,
       goes UP clear of everything, LEFT, then DOWN into TLB top.
       PT top edge center: (690, 355)
       TLB top center: (490, 143)
       Route: (690,355) → UP to y=120 → LEFT to x=490 → DOWN to TLB top (490,143)
  ══════════════════════════════════════════════ -->
  <polyline points="690,355  690,120  490,120  490,143" marker-end="url(#ao)" style="fill:none; stroke:#E65100; stroke-width:1.8; stroke-dasharray:7,4"></polyline>
  <!-- Label along top horizontal segment -->
  <text x="590" y="113" font-style="fill:#E65100; font-size:11; text-anchor:middle">Update TLB</text>

  <!-- ══════════════════════════════════════════════
       Page Tables → Physical Address:
       HORIZONTAL arrow from PT left edge to PA right edge (same y-level).
       PT left: (596, 388).  PA right: (353, 385).
       Both boxes centered vertically at ~y=387–388 → clean horizontal.
  ══════════════════════════════════════════════ -->
  <line x1="596" y1="388" x2="354" y2="388" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2.5"></line>
  <text x="475" y="381" style="fill:#E65100; font-size:11; text-anchor:middle">PFN resolved → compute PA</text>

  <!-- ══════════════════════════════════════════════
       PHYSICAL ADDRESS: x=165, w=188, right=353, center=259, y=357, h=58, bottom=415
  ══════════════════════════════════════════════ -->
  <rect x="165" y="357" width="188" height="58" rx="6" filter="url(#sh)" style="fill:#00796B" />
  <text x="259" y="382" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Physical Address</text>
  <text x="259" y="402" style="fill:#FFFFFF; font-size:13; text-anchor:middle">PA = (PFN &lt;&lt; 12) | Offset</text>

  <!-- Physical Address → DRAM -->
  <line x1="259" y1="415" x2="259" y2="477" marker-end="url(#ateal)" style="stroke:#00796B; stroke-width:2.5"></line>

  <!-- DRAM -->
  <rect x="160" y="479" width="198" height="54" rx="6" filter="url(#sh)" style="fill:#757575" />
  <rect x="168" y="487" width="182" height="7" style="fill:#9E9E9E" />
  <rect x="168" y="500" width="182" height="7" style="fill:#9E9E9E" />
  <rect x="168" y="513" width="182" height="7" style="fill:#9E9E9E" />
  <rect x="160" y="479" width="198" height="54" rx="6" style="fill:none; stroke:#424242; stroke-width:1.5" />
  <text x="259" y="505" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">DRAM / Cache</text>
  <text x="259" y="522" style="fill:#E0E0E0; font-size:12; text-anchor:middle">Actual data fetched</text>

  <!-- ══════════════════════════════════════════════
       PERMISSION CHECK — LEFT of Physical Address
       PA left edge: x=165.
       Perm box: x=5, w=140, right=145, y=357, h=94
       Line: PA left (165,387) ← Perm right (145,387)
  ══════════════════════════════════════════════ -->
  <rect x="5" y="357" width="140" height="94" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:2" />
  <text x="75" y="378" style="fill:#212121; font-size:12; font-weight:bold; text-anchor:middle">Permission</text>
  <text x="75" y="394" style="fill:#212121; font-size:12; font-weight:bold; text-anchor:middle">Check</text>
  <text x="75" y="411" style="fill:#212121; font-size:12; text-anchor:middle">R/W/X/U/S bits</text>
  <text x="75" y="427" style="fill:#2E7D32; font-size:11; text-anchor:middle">Pass → proceed</text>
  <text x="75" y="442" style="fill:#E65100; font-size:11; text-anchor:middle">Fail → page fault</text>
  <!-- dashed line from PA left edge → Permission Check right edge -->
  <line x1="165" y1="387" x2="145" y2="387" marker-end="url(#ag)" style="stroke:#9E9E9E; stroke-width:2; stroke-dasharray:4,2"></line>

  <!-- ══════════════════════════════════════════════
       LATENCY SUMMARY + PATH LEGEND
  ══════════════════════════════════════════════ -->
  <rect x="30" y="556" width="398" height="130" rx="6" filter="url(#sh)" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="229" y="576" style="fill:#1565C0; font-size:15; font-weight:bold; text-anchor:middle">Latency Summary</text>
  <line x1="42" y1="584" x2="416" y2="584" style="stroke:#9E9E9E; stroke-width:1"></line>
  <rect x="42" y="590" width="374" height="34" rx="4" style="fill:#E8F5E9" />
  <text x="229" y="607" style="fill:#2E7D32; font-size:13; font-weight:bold; text-anchor:middle">TLB HIT PATH: 1–4 cycles (~1 ns)</text>
  <text x="229" y="622" style="fill:#212121; font-size:12; text-anchor:middle">No memory access — fastest possible</text>
  <rect x="42" y="628" width="374" height="34" rx="4" style="fill:#FFF3E0" />
  <text x="229" y="645" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">TLB MISS PATH: 4 × 70 ns ≈ 280 ns</text>
  <text x="229" y="660" style="fill:#212121; font-size:12; text-anchor:middle">≈ 840 CPU cycles wasted per TLB miss</text>
  <rect x="42" y="666" width="374" height="14" rx="3" style="fill:#1565C0" />
  <text x="229" y="677" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">95% hit rate → avg 19 cyc | 50% hit → avg 422 cyc</text>

  <rect x="442" y="556" width="448" height="130" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="666" y="576" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Path Legend</text>
  <line x1="454" y1="584" x2="878" y2="584" style="stroke:#9E9E9E; stroke-width:1"></line>
  <line x1="458" y1="602" x2="510" y2="602" marker-end="url(#at)" style="stroke:#2E7D32; stroke-width:2.5"></line>
  <text x="520" y="607" style="fill:#212121; font-size:13">TLB Hit — fast path</text>
  <line x1="458" y1="624" x2="510" y2="624" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2.5"></line>
  <text x="520" y="629" style="fill:#212121; font-size:13">TLB Miss — slow path</text>
  <line x1="458" y1="646" x2="510" y2="646" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:1.8; stroke-dasharray:7,4"></line>
  <text x="520" y="651" style="fill:#212121; font-size:13">TLB entry update (feedback)</text>
  <line x1="458" y1="668" x2="510" y2="668" marker-end="url(#ag)" style="stroke:#9E9E9E; stroke-width:2; stroke-dasharray:4,2"></line>
  <text x="520" y="673" style="fill:#212121; font-size:13">Permission check (always)</text>
</svg>
</div>
<figcaption><strong>Figure 1.13:</strong> Address translation control
flow: TLB hit returns physical address in 1-2 cycles (fast path); TLB
miss triggers a hardware page-table walk costing 100-300 cycles (slow
path).</figcaption>
</figure>

While page tables elegantly solve the problem of address translation,
they introduce a significant performance challenge: **every memory
access requires at least one additional memory read** to consult the
page table. For a simple memory load instruction, the CPU must:

1.  Read the page table entry from memory (\~100 nanoseconds)
2.  Use the PFN to calculate the physical address
3.  Read the actual data from memory (\~100 nanoseconds)

This doubles the effective memory access time! For a program making
millions of memory accesses per second, this overhead would be
catastrophic.

#### The Solution: Translation Lookaside Buffer

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="600" viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
    <marker id="ab" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="at" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker>
    <marker id="ao" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
  </defs>
  <rect width="900" height="600" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">TLB Structure and Operation: Fast Path vs. Miss Path</text>

  <!-- TLB structure (left column) -->
  <text x="30" y="68" style="fill:#212121; font-size:15; font-weight:bold">TLB Internal Structure (fully-associative, 64-entry example):</text>
  <rect x="22" y="78" width="440" height="36" rx="4" style="fill:#1565C0" />
  <text x="100" y="99" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">ASID</text>
  <text x="190" y="99" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">VPN (Tag)</text>
  <text x="310" y="99" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">PFN</text>
  <text x="400" y="99" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Flags</text>
  <text x="440" y="99" style="fill:#FFFFFF; font-size:13; font-weight:bold">V</text>

  <!-- TLB rows -->
  <rect x="22" y="114" width="440" height="30" style="fill:#E8F5E9; stroke:#9E9E9E; stroke-width:1" />
  <text x="100" y="133" style="fill:#212121; font-size:13; text-anchor:middle">0x01</text>
  <text x="190" y="133" style="fill:#212121; font-size:13; text-anchor:middle">0x7FFF5</text>
  <text x="310" y="133" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">0x1B7</text>
  <text x="400" y="133" style="fill:#212121; font-size:13; text-anchor:middle">RW-</text>
  <text x="449" y="133" style="fill:#2E7D32; font-size:13; font-weight:bold">1</text>

  <rect x="22" y="144" width="440" height="30" style="fill:#FFFFFF; stroke:#9E9E9E; stroke-width:1" />
  <text x="100" y="163" style="fill:#212121; font-size:13; text-anchor:middle">0x01</text>
  <text x="190" y="163" style="fill:#212121; font-size:13; text-anchor:middle">0x40000</text>
  <text x="310" y="163" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">0x2A1</text>
  <text x="400" y="163" style="fill:#212121; font-size:13; text-anchor:middle">R-X</text>
  <text x="449" y="163" style="fill:#2E7D32; font-size:13; font-weight:bold">1</text>

  <rect x="22" y="174" width="440" height="30" style="fill:#E8F5E9; stroke:#9E9E9E; stroke-width:1" />
  <text x="100" y="193" style="fill:#212121; font-size:13; text-anchor:middle">0x02</text>
  <text x="190" y="193" style="fill:#212121; font-size:13; text-anchor:middle">0x7FFF5</text>
  <text x="310" y="193" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">0x5C2</text>
  <text x="400" y="193" style="fill:#212121; font-size:13; text-anchor:middle">RW-</text>
  <text x="449" y="193" style="fill:#2E7D32; font-size:13; font-weight:bold">1</text>

  <rect x="22" y="204" width="440" height="30" style="fill:#FFFFFF; stroke:#9E9E9E; stroke-width:1" />
  <text x="100" y="223" style="fill:#424242; font-size:13; text-anchor:middle">0x01</text>
  <text x="190" y="223" style="fill:#424242; font-size:13; text-anchor:middle">0x90000</text>
  <text x="310" y="223" style="fill:#9E9E9E; font-size:13; font-weight:bold; text-anchor:middle">--</text>
  <text x="400" y="223" style="fill:#424242; font-size:13; text-anchor:middle">---</text>
  <text x="449" y="223" style="fill:#E65100; font-size:13; font-weight:bold">0</text>
  <text x="462" y="223" style="fill:#E65100; font-size:11">(invalid)</text>

  <rect x="22" y="234" width="440" height="20" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
  <text x="230" y="249" style="fill:#616161; font-size:12; text-anchor:middle">... 60 more entries ...</text>

  <!-- ASID note -->
  <rect x="22" y="264" width="440" height="50" rx="4" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="242" y="284" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:middle">ASID = Address Space Identifier</text>
  <text x="242" y="302" style="fill:#212121; font-size:13; text-anchor:middle">Allows multiple processes to share TLB without flushing on context switch</text>

  <!-- TLB HIT diagram (right top) -->
  <text x="496" y="68" style="fill:#2E7D32; font-size:15; font-weight:bold">TLB HIT Path (~1–4 cycles):</text>
  <rect x="490" y="78" width="388" height="220" rx="6" filter="url(#sh)" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:2" />

  <rect x="504" y="92" width="160" height="50" rx="4" style="fill:#1565C0" />
  <text x="584" y="117" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">CPU Virtual Addr</text>
  <text x="584" y="134" style="fill:#BBDEFB; font-size:13; text-anchor:middle">VPN=0x7FFF5 | Off=0x123</text>
  <line x1="664" y1="117" x2="714" y2="117" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:2.5"></line>

  <rect x="718" y="92" width="148" height="50" rx="4" style="fill:#F5F5F5; stroke:#2E7D32; stroke-width:2" />
  <text x="792" y="117" style="fill:#2E7D32; font-size:14; font-weight:bold; text-anchor:middle">TLB LOOKUP</text>
  <text x="792" y="134" style="fill:#424242; font-size:12; text-anchor:middle">VPN match found!</text>

  <line x1="792" y1="142" x2="792" y2="180" marker-end="url(#at)" style="stroke:#2E7D32; stroke-width:2.5"></line>
  <text x="800" y="165" style="fill:#2E7D32; font-size:12; font-weight:bold">HIT!</text>

  <rect x="718" y="182" width="148" height="50" rx="4" style="fill:#2E7D32" />
  <text x="792" y="207" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Physical Addr</text>
  <text x="792" y="224" style="fill:#B2DFDB; font-size:13; text-anchor:middle">PFN=0x1B7, Off=0x123</text>

  <line x1="718" y1="207" x2="668" y2="207" marker-end="url(#at)" style="stroke:#2E7D32; stroke-width:2.5"></line>
  <rect x="504" y="182" width="160" height="50" rx="4" style="fill:#00796B" />
  <text x="584" y="207" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Access Memory</text>
  <text x="584" y="224" style="fill:#B2DFDB; font-size:13; text-anchor:middle">PA: 0x1B7123</text>

  <rect x="504" y="248" width="362" height="40" rx="4" style="fill:#C8E6C9" />
  <text x="685" y="274" style="fill:#2E7D32; font-size:14; font-weight:bold; text-anchor:middle">Total: ~1–4 cycles. No memory access needed!</text>

  <!-- TLB MISS diagram (right bottom) -->
  <text x="496" y="328" style="fill:#E65100; font-size:15; font-weight:bold">TLB MISS Path (~280+ ns penalty):</text>
  <rect x="490" y="338" width="388" height="220" rx="6" filter="url(#sh)" style="fill:#FFF3E0; stroke:#E65100; stroke-width:2" />

  <rect x="504" y="352" width="134" height="46" rx="4" style="fill:#1565C0" />
  <text x="571" y="375" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Virtual Addr</text>
  <text x="571" y="391" style="fill:#BBDEFB; font-size:13; text-anchor:middle">VPN=0x90000</text>
  <line x1="638" y1="375" x2="680" y2="375" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:2.5"></line>

  <rect x="684" y="352" width="182" height="46" rx="4" style="fill:#F5F5F5; stroke:#E65100; stroke-width:2" />
  <text x="775" y="375" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">TLB LOOKUP</text>
  <text x="775" y="391" style="fill:#424242; font-size:12; text-anchor:middle">No match -- MISS</text>

  <line x1="775" y1="398" x2="775" y2="428" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2.5"></line>
  <rect x="684" y="430" width="182" height="46" rx="4" style="fill:#E65100" />
  <text x="775" y="453" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Page Table Walk</text>
  <text x="775" y="470" style="fill:#FFCCBC; font-size:13; text-anchor:middle">4 DRAM reads x 70ns</text>

  <line x1="684" y1="453" x2="638" y2="453" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2.5"></line>
  <rect x="504" y="430" width="130" height="46" rx="4" style="fill:#00796B" />
  <text x="569" y="453" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Update TLB</text>
  <text x="569" y="469" style="fill:#B2DFDB; font-size:13; text-anchor:middle">Install mapping</text>

  <rect x="504" y="492" width="362" height="40" rx="4" style="fill:#FFCCBC" />
  <text x="685" y="518" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">Total: ~280 ns = ~840 wasted CPU cycles!</text>

  <!-- TLB specs box -->
  <rect x="22" y="326" width="452" height="158" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="242" y="348" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Typical TLB Specifications</text>
  <text x="38" y="368" style="fill:#212121; font-size:13">L1 ITLB: 64-128 entries, fully-assoc, 1-cycle</text>
  <text x="38" y="386" style="fill:#212121; font-size:13">L1 DTLB: 64-64 entries, 4-way set-assoc, 1-cycle</text>
  <text x="38" y="404" style="fill:#212121; font-size:13">L2 STLB: 512-2048 entries, 4-12 cycle miss</text>
  <text x="38" y="422" style="fill:#212121; font-size:13">Intel Skylake: 64 L1 + 1536 L2 entries</text>
  <text x="38" y="440" style="fill:#212121; font-size:13">AMD Zen4:     64 L1 + 2048 L2 entries</text>
</svg>
</div>
<figcaption><strong>Figure 1.14:</strong> TLB operation: hardware
compares the VPN tag against all entries in parallel; a hit immediately
returns the cached PFN without touching DRAM.</figcaption>
</figure>

The **Translation Lookaside Buffer (TLB)** is a specialized hardware
cache that stores recently used virtual-to-physical address
translations. It sits between the CPU and the page table, intercepting
every address translation request.

**How the TLB Works:**

#### TLB Performance Impact

The performance difference between a TLB hit and miss is dramatic:

| Scenario | Cycles | Time (3 GHz CPU) | Relative Speed |
| --- | --- | --- | --- |
| **TLB Hit** | 1-2 | \~0.5 ns | 1x (baseline) |
| **TLB Miss** | 100-300 | \~50-100 ns | **100-200x slower** |


Modern processors typically achieve **95-99% TLB hit rates** during
normal operation, meaning most memory accesses avoid the slow page table
walk entirely.

#### TLB Structure

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="440" viewBox="0 0 900 440" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter></defs>
  <rect width="900" height="440" style="fill:#FAFAFA" />
  <text x="450" y="36" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">TLB Entry Structure: Fields and Their Roles</text>

  <!-- Main TLB entry bar -->
  <text x="450" y="62" style="fill:#616161; font-size:13; text-anchor:middle">A single TLB entry encodes everything needed for one virtual-to-physical translation plus access control</text>

  <!-- ASID -->
  <rect x="20" y="74" width="110" height="70" rx="5" filter="url(#sh)" style="fill:#5C6BC0" />
  <text x="75" y="100" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">ASID /</text>
  <text x="75" y="118" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">PCID</text>
  <text x="75" y="136" style="fill:#E8EAF6; font-size:12; text-anchor:middle">8–12 bit</text>

  <!-- VPN (tag) -->
  <rect x="136" y="74" width="220" height="70" rx="5" filter="url(#sh)" style="fill:#1565C0" />
  <text x="246" y="100" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">VPN (Tag)</text>
  <text x="246" y="118" style="fill:#BBDEFB; font-size:13; text-anchor:middle">Virtual Page Number</text>
  <text x="246" y="136" style="fill:#BBDEFB; font-size:12; text-anchor:middle">36 bits (x86-64, 4-level)</text>

  <!-- Valid bit -->
  <rect x="362" y="74" width="60" height="70" rx="5" filter="url(#sh)" style="fill:#2E7D32" />
  <text x="392" y="102" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">V</text>
  <text x="392" y="120" style="fill:#C8E6C9; font-size:13; text-anchor:middle">Valid</text>
  <text x="392" y="136" style="fill:#C8E6C9; font-size:12; text-anchor:middle">1 bit</text>

  <!-- PFN (data) -->
  <rect x="428" y="74" width="210" height="70" rx="5" filter="url(#sh)" style="fill:#00796B" />
  <text x="533" y="100" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">PFN (Data)</text>
  <text x="533" y="118" style="fill:#B2DFDB; font-size:13; text-anchor:middle">Physical Frame Number</text>
  <text x="533" y="136" style="fill:#B2DFDB; font-size:12; text-anchor:middle">40 bits (4 PB support)</text>

  <!-- Protection flags -->
  <rect x="644" y="74" width="60" height="70" rx="5" filter="url(#sh)" style="fill:#E65100" />
  <text x="674" y="100" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">R/W</text>
  <text x="674" y="118" style="fill:#FFE0B2; font-size:12; text-anchor:middle">Write</text>
  <text x="674" y="136" style="fill:#FFE0B2; font-size:12; text-anchor:middle">1 bit</text>

  <rect x="710" y="74" width="60" height="70" rx="5" filter="url(#sh)" style="fill:#E65100" />
  <text x="740" y="100" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">U/S</text>
  <text x="740" y="118" style="fill:#FFE0B2; font-size:12; text-anchor:middle">User</text>
  <text x="740" y="136" style="fill:#FFE0B2; font-size:12; text-anchor:middle">1 bit</text>

  <rect x="776" y="74" width="55" height="70" rx="5" filter="url(#sh)" style="fill:#C62828" />
  <text x="803" y="100" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">NX</text>
  <text x="803" y="118" style="fill:#FFCDD2; font-size:12; text-anchor:middle">No-Exec</text>
  <text x="803" y="136" style="fill:#FFCDD2; font-size:12; text-anchor:middle">1 bit</text>

  <rect x="837" y="74" width="43" height="70" rx="5" filter="url(#sh)" style="fill:#37474F" />
  <text x="858" y="96" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">PCD/</text>
  <text x="858" y="112" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">PWT</text>
  <text x="858" y="128" style="fill:#B0BEC5; font-size:11; text-anchor:middle">Cache</text>
  <text x="858" y="144" style="fill:#B0BEC5; font-size:11; text-anchor:middle">2 bits</text>

  <!-- Field explanations -->
  <rect x="20" y="162" width="860" height="258" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="450" y="182" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Field Descriptions and Hardware Behavior</text>

  <!-- ASID -->
  <rect x="35" y="194" width="12" height="12" rx="2" style="fill:#5C6BC0" />
  <text x="55" y="204" style="fill:#5C6BC0; font-size:13; font-weight:bold">ASID / PCID:</text>
  <text x="160" y="204" style="fill:#212121; font-size:13">Address Space ID / Process Context ID. Tags each entry to a specific process, eliminating</text>
  <text x="55" y="220" style="fill:#212121; font-size:13">full TLB flushes on context switches. x86-64 PCID: 12 bits (4096 distinct contexts).</text>

  <!-- VPN -->
  <rect x="35" y="232" width="12" height="12" rx="2" style="fill:#1565C0" />
  <text x="55" y="242" style="fill:#1565C0; font-size:13; font-weight:bold">VPN (Tag):</text>
  <text x="140" y="242" style="fill:#212121; font-size:13">Virtual Page Number being translated. Used as the lookup key — hardware compares</text>
  <text x="55" y="258" style="fill:#212121; font-size:13">incoming VPN against all TLB tags simultaneously (fully-associative) in a single cycle.</text>

  <!-- Valid -->
  <rect x="35" y="270" width="12" height="12" rx="2" style="fill:#2E7D32" />
  <text x="55" y="280" style="fill:#2E7D32; font-size:13; font-weight:bold">Valid:</text>
  <text x="115" y="280" style="fill:#212121; font-size:13">1=entry is live; 0=entry has been invalidated (by INVLPG or TLB flush). Invalid entries</text>
  <text x="55" y="296" style="fill:#212121; font-size:13">are ignored during lookup even if the VPN tag matches.</text>

  <!-- PFN -->
  <rect x="35" y="308" width="12" height="12" rx="2" style="fill:#00796B" />
  <text x="55" y="318" style="fill:#00796B; font-size:13; font-weight:bold">PFN (Data):</text>
  <text x="155" y="318" style="fill:#212121; font-size:13">Physical Frame Number — the result of the translation. PA = PFN × 4096 + offset.</text>
  <text x="55" y="334" style="fill:#212121; font-size:13">On TLB hit, the PFN is immediately used to form the physical address.</text>

  <!-- Protection flags -->
  <rect x="35" y="346" width="12" height="12" rx="2" style="fill:#E65100" />
  <text x="55" y="356" style="fill:#E65100; font-size:13; font-weight:bold">Protection Flags:</text>
  <text x="185" y="356" style="fill:#212121; font-size:13">R/W, U/S, NX copied from PTE into TLB entry. Hardware checks these on every</text>
  <text x="55" y="372" style="fill:#212121; font-size:13">access — a write to R/W=0 page raises a #PF even on TLB hit. NX prevents code execution.</text>

  <!-- G bit note -->
  <rect x="35" y="384" width="12" height="12" rx="2" style="fill:#9E9E9E" />
  <text x="55" y="394" style="fill:#616161; font-size:13; font-weight:bold">Global (G):</text>
  <text x="145" y="394" style="fill:#212121; font-size:13">When G=1, this entry is not flushed on CR3 writes (used for kernel pages shared across all processes).</text>
</svg>
</div>
<figcaption><strong>Figure 1.15:</strong> TLB entry structure: VPN tag,
Physical Frame Number, Address Space ID (ASID) for process isolation,
and permission/dirty/valid bits.</figcaption>
</figure>

A typical TLB is organized as an **associative cache**
(content-addressable memory):

**Entry Format:**

Each entry stores: - **Virtual Page Number (VPN):** The tag to match
against - **Physical Frame Number (PFN):** The translation result -
**Valid bit:** Whether this entry contains valid data - **Flags:**
Permissions (read/write/execute) from the PTE

**Size Example:** A typical L1 TLB might have: - 64 entries for 4 KB
pages - Covers: 64 x 4 KB = 256 KB of address space - Only 256 KB of
\"working set\" can be accessed without misses!

This limited coverage is called **TLB reach** and is a critical factor
in system performance. Programs with larger working sets will experience
more TLB misses.

#### When Does the TLB Get Updated?

The TLB is automatically managed by the hardware MMU:

**TLB is updated on:** - Every TLB miss (new entry added) - Page table
updates by the OS (corresponding entry invalidated)

**TLB is flushed (cleared) on:** - Context switch between processes
(different address spaces) - Explicit flush instruction (e.g., when
kernel updates page tables) - Some CPUs support ASID (Address Space
Identifier) to avoid flushing on context switches

#### Why the TLB Matters

The TLB is arguably the most important performance component in virtual
memory systems:

1.  **Makes Virtual Memory Practical:** Without TLBs, virtual memory
    would be too slow for production use
2.  **Working Set Matters:** Programs that access memory randomly suffer
    more TLB misses
3.  **Large Pages Help:** Using 2 MB pages instead of 4 KB pages
    increases TLB reach by 512x

**Real-World Example:**

Consider a database scanning a 1 GB table with random access: - With 4
KB pages: 262,144 pages, typical TLB: 64 entries - TLB covers: 256 KB
(0.025% of data) - Result: \~99.975% TLB miss rate = catastrophic
performance

- With 2 MB pages: 512 pages, same TLB: 64 entries\
- TLB covers: 128 MB (12.5% of data)
- Result: \~87.5% miss rate (still poor, but 10x fewer misses)

This is why databases and high-performance applications use huge pages
(covered in Chapter 2.7).

#### Key Takeaways

1.  **TLB is essential:** Virtual memory would be impractically slow
    without TLB caching
2.  **Hit rate is critical:** 95%+ hit rates are necessary for good
    performance
3.  **TLB reach is limited:** Only 256 KB - 128 MB of working set can be
    efficiently accessed
4.  **Hardware-managed:** The MMU automatically updates and manages the
    TLB
5.  **Performance tool:** Understanding TLB behavior is crucial for
    optimization (covered in Part IX)

The TLB transforms virtual memory from a theoretical elegance into a
practical, high-performance system. Modern processors invest significant
chip area in TLB structures precisely because this cache is so
performance-critical.

In the next section, we\'ll see how multi-level page tables address
another challenge: efficiently managing large, sparse address spaces.

## 1.9 Multi-Level Page Tables

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="500" viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr-b" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
  </defs>
  <rect width="900" height="500" style="fill:#FAFAFA" />
  <text x="450" y="36" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Page Table Mapping: Virtual Pages to Physical Frames</text>

  <!-- VPN column -->
  <rect x="20" y="56" width="200" height="38" rx="4" style="fill:#1565C0" />
  <text x="120" y="79" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Virtual Page # (VPN)</text>

  <rect x="20" y="96" width="200" height="34" rx="3" style="fill:#E3F2FD" />
  <text x="120" y="117" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">VPN 0  (0x0000)</text>

  <rect x="20" y="132" width="200" height="34" rx="3" style="fill:#E3F2FD" />
  <text x="120" y="153" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">VPN 1  (0x1000)</text>

  <rect x="20" y="168" width="200" height="34" rx="3" style="fill:#FAFAFA; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:4,2" />
  <text x="120" y="189" style="fill:#9E9E9E; font-size:14; text-anchor:middle">VPN 2  (not mapped)</text>

  <rect x="20" y="204" width="200" height="34" rx="3" style="fill:#E3F2FD" />
  <text x="120" y="225" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">VPN 3  (0x3000)</text>

  <rect x="20" y="240" width="200" height="34" rx="3" style="fill:#E0F2F1" />
  <text x="120" y="261" style="fill:#00796B; font-size:14; font-weight:bold; text-anchor:middle">VPN 4  (0x4000)</text>

  <rect x="20" y="276" width="200" height="34" rx="3" style="fill:#E0F2F1" />
  <text x="120" y="297" style="fill:#00796B; font-size:14; font-weight:bold; text-anchor:middle">VPN 5  (0x5000)</text>

  <rect x="20" y="312" width="200" height="34" rx="3" style="fill:#FAFAFA; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:4,2" />
  <text x="120" y="333" style="fill:#9E9E9E; font-size:14; text-anchor:middle">VPN 6  (not mapped)</text>

  <rect x="20" y="348" width="200" height="34" rx="3" style="fill:#E3F2FD" />
  <text x="120" y="369" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">VPN 7  (0x7000)</text>

  <!-- PTE column -->
  <rect x="340" y="56" width="220" height="38" rx="4" style="fill:#37474F" />
  <text x="450" y="79" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Page Table Entry</text>

  <rect x="340" y="96" width="220" height="34" rx="3" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="450" y="117" style="fill:#212121; font-size:13; text-anchor:middle">PFN=3, P=1, R/W, U/S</text>
  <rect x="340" y="132" width="220" height="34" rx="3" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="450" y="153" style="fill:#212121; font-size:13; text-anchor:middle">PFN=7, P=1, R/W, U/S</text>
  <rect x="340" y="168" width="220" height="34" rx="3" style="fill:#FAFAFA; stroke:#E0E0E0; stroke-width:1; stroke-dasharray:3,2" />
  <text x="450" y="189" style="fill:#9E9E9E; font-size:13; text-anchor:middle">P=0 (page fault if accessed)</text>
  <rect x="340" y="204" width="220" height="34" rx="3" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="450" y="225" style="fill:#212121; font-size:13; text-anchor:middle">PFN=1, P=1, R/W, U/S</text>
  <rect x="340" y="240" width="220" height="34" rx="3" style="fill:#E0F2F1; stroke:#00796B; stroke-width:1" />
  <text x="450" y="261" style="fill:#212121; font-size:13; text-anchor:middle">PFN=9, P=1, R/W, U/S</text>
  <rect x="340" y="276" width="220" height="34" rx="3" style="fill:#E0F2F1; stroke:#00796B; stroke-width:1" />
  <text x="450" y="297" style="fill:#212121; font-size:13; text-anchor:middle">PFN=2, P=1, R/W, U/S</text>
  <rect x="340" y="312" width="220" height="34" rx="3" style="fill:#FAFAFA; stroke:#E0E0E0; stroke-width:1; stroke-dasharray:3,2" />
  <text x="450" y="333" style="fill:#9E9E9E; font-size:13; text-anchor:middle">P=0</text>
  <rect x="340" y="348" width="220" height="34" rx="3" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="450" y="369" style="fill:#212121; font-size:13; text-anchor:middle">PFN=11, P=1, R=1, W=0, NX</text>

  <!-- PFN column -->
  <rect x="680" y="56" width="200" height="38" rx="4" style="fill:#00796B" />
  <text x="780" y="79" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">Physical Frame (PFN)</text>

  <rect x="680" y="96" width="200" height="34" rx="3" style="fill:#B2DFDB" />
  <text x="780" y="117" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Frame 3  (0x3000)</text>
  <rect x="680" y="130" width="200" height="34" rx="3" style="fill:#B2DFDB" />
  <text x="780" y="149" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Frame 7  (0x7000)</text>
  <rect x="680" y="164" width="200" height="38" rx="3" style="fill:#FFEBEE; stroke:#C62828; stroke-width:1" />
  <text x="780" y="181" style="fill:#C62828; font-size:13; font-weight:bold; text-anchor:middle">— (no frame allocated) —</text>
  <text x="780" y="197" style="fill:#C62828; font-size:11; text-anchor:middle">Page fault if accessed</text>
  <rect x="680" y="204" width="200" height="34" rx="3" style="fill:#B2DFDB" />
  <text x="780" y="225" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Frame 1  (0x1000)</text>
  <rect x="680" y="240" width="200" height="34" rx="3" style="fill:#B2DFDB" />
  <text x="780" y="261" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Frame 9  (0x9000)</text>
  <rect x="680" y="276" width="200" height="34" rx="3" style="fill:#B2DFDB" />
  <text x="780" y="297" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Frame 2  (0x2000)</text>
  <rect x="680" y="312" width="200" height="34" rx="3" style="fill:#FFEBEE; stroke:#C62828; stroke-width:1" />
  <text x="780" y="335" style="fill:#C62828; font-size:13; font-weight:bold; text-anchor:middle">— (no frame) —</text>
  <rect x="680" y="348" width="200" height="34" rx="3" style="fill:#B2DFDB" />
  <text x="780" y="369" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Frame 11 (0xB000)</text>

  <!-- Arrows VPN → PTE -->
  <line x1="220" y1="113" x2="338" y2="113" marker-end="url(#arr-b)" style="stroke:#1565C0; stroke-width:1.5"></line>
  <line x1="220" y1="149" x2="338" y2="149" marker-end="url(#arr-b)" style="stroke:#1565C0; stroke-width:1.5"></line>
  <line x1="220" y1="221" x2="338" y2="221" marker-end="url(#arr-b)" style="stroke:#1565C0; stroke-width:1.5"></line>
  <line x1="220" y1="258" x2="338" y2="258" marker-end="url(#arr-b)" style="stroke:#00796B; stroke-width:1.5"></line>
  <line x1="220" y1="293" x2="338" y2="293" marker-end="url(#arr-b)" style="stroke:#00796B; stroke-width:1.5"></line>
  <line x1="220" y1="365" x2="338" y2="365" marker-end="url(#arr-b)" style="stroke:#1565C0; stroke-width:1.5"></line>

  <!-- Arrows PTE → PFN -->
  <line x1="561" y1="113" x2="678" y2="113" marker-end="url(#arr-b)" style="stroke:#00796B; stroke-width:1.5"></line>
  <line x1="561" y1="149" x2="678" y2="147" marker-end="url(#arr-b)" style="stroke:#00796B; stroke-width:1.5"></line>
  <line x1="561" y1="221" x2="678" y2="221" marker-end="url(#arr-b)" style="stroke:#00796B; stroke-width:1.5"></line>
  <line x1="561" y1="258" x2="678" y2="258" marker-end="url(#arr-b)" style="stroke:#00796B; stroke-width:1.5"></line>
  <line x1="561" y1="293" x2="678" y2="293" marker-end="url(#arr-b)" style="stroke:#00796B; stroke-width:1.5"></line>
  <line x1="561" y1="365" x2="678" y2="365" marker-end="url(#arr-b)" style="stroke:#00796B; stroke-width:1.5"></line>

  <!-- Note at bottom -->
  <rect x="20" y="398" width="860" height="88" rx="4" style="fill:#FFF9E6; stroke:#F9A825; stroke-width:1.5" />
  <text x="450" y="418" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">Non-Contiguous Mapping in Action</text>
  <text x="450" y="438" style="fill:#212121; font-size:13; text-anchor:middle">VPN 0→Frame 3, VPN 1→Frame 7, VPN 3→Frame 1 : virtual pages appear contiguous to the program</text>
  <text x="450" y="456" style="fill:#212121; font-size:13; text-anchor:middle">but physically occupy non-adjacent frames scattered across RAM. This is the power of paging.</text>
  <text x="450" y="476" style="fill:#212121; font-size:13; text-anchor:middle">VPN 7 is mapped R=1 W=0 NX=1 → read-only, cannot be executed (e.g., read-only data segment)</text>
</svg>
</div>
<figcaption><strong>Figure 1.16:</strong> Page table mapping:
non-contiguous virtual pages map to arbitrary physical frames, providing
address-space isolation between processes.</figcaption>
</figure>

The page table design we\'ve discussed so far has a critical flaw: it
assumes a **single-level** page table that must contain an entry for
every possible virtual page. For modern 64-bit systems with vast address
spaces, this becomes completely impractical.

#### The Problem: Single-Level Page Tables Don\'t Scale

Consider a 64-bit system with 4 KB pages:

**Address Space Calculation:** - Virtual address space: 2\^48 bits = 256
TB (typical implementation) - Page size: 4 KB = 2\^12 bytes - Number of
pages: 256 TB / 4 KB = **68,719,476,736 pages**

**Page Table Size:** - Entries needed: 68.7 billion entries - Entry
size: 8 bytes (64-bit PTE) - **Total page table size: 512 GB per
process!**

This is absurd. The page table alone would consume more memory than most
systems have, and we haven\'t even allocated memory for the actual
program yet!

#### The Observation: Most Address Spaces Are Sparse

The key insight is that **programs don\'t use most of their address
space**. A typical program might use:

- Text segment: 10 MB (executable code)
- Data segment: 50 MB (global variables)
- Heap: 200 MB (dynamically allocated)
- Stack: 8 MB (function call frames)
- **Total: \~268 MB out of 256 TB (0.0001%)**

The remaining 99.9999% of the address space is unmapped and unused.
Allocating a complete page table for this sparse usage is incredibly
wasteful.

#### The Solution: Hierarchical Page Tables

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="620" viewBox="0 0 900 620" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
    <marker id="ab" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="at" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker>
    <marker id="ao" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
  </defs>
  <rect width="900" height="620" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Multi-Level Page Tables: x86-64 4-Level Hierarchy (CR3 Walk)</text>

  <!-- 64-bit virtual address breakdown -->
  <text x="30" y="66" style="fill:#212121; font-size:14; font-weight:bold">48-bit Virtual Address (x86-64 canonical form):</text>
  <!-- Sign extend 63-48 -->
  <rect x="22" y="76" width="80" height="38" rx="3" style="fill:#9E9E9E" />
  <text x="62" y="95" style="fill:#FFFFFF; font-size:12; text-anchor:middle">Sign Ext</text>
  <text x="62" y="109" style="fill:#E0E0E0; font-size:11; text-anchor:middle">bits 63-48</text>
  <!-- PML4 47-39 -->
  <rect x="104" y="76" width="112" height="38" rx="3" style="fill:#1565C0" />
  <text x="160" y="95" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">PML4 Index</text>
  <text x="160" y="109" style="fill:#BBDEFB; font-size:11; text-anchor:middle">bits 47-39 (9 bits)</text>
  <!-- PDP 38-30 -->
  <rect x="218" y="76" width="112" height="38" rx="3" style="fill:#1565C0; opacity:0.82" />
  <text x="274" y="95" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">PDPT Index</text>
  <text x="274" y="109" style="fill:#BBDEFB; font-size:11; text-anchor:middle">bits 38-30 (9 bits)</text>
  <!-- PD 29-21 -->
  <rect x="332" y="76" width="112" height="38" rx="3" style="fill:#00796B" />
  <text x="388" y="95" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">PD Index</text>
  <text x="388" y="109" style="fill:#B2DFDB; font-size:11; text-anchor:middle">bits 29-21 (9 bits)</text>
  <!-- PT 20-12 -->
  <rect x="446" y="76" width="112" height="38" rx="3" style="fill:#00796B; opacity:0.78" />
  <text x="502" y="95" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">PT Index</text>
  <text x="502" y="109" style="fill:#B2DFDB; font-size:11; text-anchor:middle">bits 20-12 (9 bits)</text>
  <!-- Offset 11-0 -->
  <rect x="560" y="76" width="110" height="38" rx="3" style="fill:#E65100" />
  <text x="615" y="95" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Page Offset</text>
  <text x="615" y="109" style="fill:#FFCCBC; font-size:11; text-anchor:middle">bits 11-0 (12 bits)</text>

  <!-- CR3 -->
  <rect x="30" y="140" width="100" height="50" rx="6" filter="url(#sh)" style="fill:#9E9E9E" />
  <text x="80" y="163" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">CR3</text>
  <text x="80" y="179" style="fill:#E0E0E0; font-size:12; text-anchor:middle">PML4 ptr</text>

  <line x1="130" y1="165" x2="178" y2="165" marker-end="url(#ab)" style="stroke:#9E9E9E; stroke-width:2.5"></line>

  <!-- PML4 Table -->
  <rect x="182" y="130" width="120" height="220" rx="4" filter="url(#sh)" style="fill:#FFFFFF; stroke:#1565C0; stroke-width:2" />
  <rect x="182" y="130" width="120" height="30" rx="4" style="fill:#1565C0" />
  <text x="242" y="149" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">PML4</text>
  <text x="242" y="163" style="fill:#BBDEFB; font-size:11; text-anchor:middle">512 entries</text>
  <rect x="190" y="170" width="104" height="26" rx="2" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="242" y="187" style="fill:#1565C0; font-size:12; text-anchor:middle">entry[0] → PDPT</text>
  <rect x="190" y="198" width="104" height="26" rx="2" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="242" y="215" style="fill:#1565C0; font-size:12; text-anchor:middle">entry[1] → PDPT</text>
  <rect x="190" y="226" width="104" height="26" rx="2" style="fill:#BDBDBD; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="242" y="243" style="fill:#9E9E9E; font-size:12; text-anchor:middle">entry[2] = NULL</text>
  <rect x="190" y="254" width="104" height="20" rx="2" style="fill:#F5F5F5" />
  <text x="242" y="269" style="fill:#616161; font-size:11; text-anchor:middle">... 509 more ...</text>
  <rect x="190" y="276" width="104" height="26" rx="2" style="fill:#BDBDBD; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="242" y="293" style="fill:#9E9E9E; font-size:12; text-anchor:middle">entry[511]=NULL</text>
  <text x="242" y="342" style="fill:#616161; font-size:11; text-anchor:middle">Only entries for</text>
  <text x="242" y="358" style="fill:#616161; font-size:11; text-anchor:middle">mapped regions</text>
  <text x="242" y="374" style="fill:#616161; font-size:11; text-anchor:middle">are non-null!</text>

  <!-- Arrow to PDPT -->
  <line x1="302" y1="183" x2="354" y2="183" marker-end="url(#ab)" style="stroke:#1565C0; stroke-width:2"></line>

  <!-- PDPT Table -->
  <rect x="358" y="130" width="120" height="200" rx="4" filter="url(#sh)" style="fill:#FFFFFF; stroke:#1565C0; stroke-width:2; opacity:0.9" />
  <rect x="358" y="130" width="120" height="30" rx="4" style="fill:#1565C0; opacity:0.82" />
  <text x="418" y="149" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">PDPT</text>
  <text x="418" y="163" style="fill:#BBDEFB; font-size:11; text-anchor:middle">512 entries</text>
  <rect x="366" y="170" width="104" height="26" rx="2" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1" />
  <text x="418" y="187" style="fill:#1565C0; font-size:12; text-anchor:middle">entry[0] → PD</text>
  <rect x="366" y="198" width="104" height="26" rx="2" style="fill:#BDBDBD; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="418" y="215" style="fill:#9E9E9E; font-size:12; text-anchor:middle">entry[1] = NULL</text>
  <rect x="366" y="226" width="104" height="20" rx="2" style="fill:#F5F5F5" />
  <text x="418" y="241" style="fill:#616161; font-size:11; text-anchor:middle">... 510 more ...</text>
  <rect x="366" y="248" width="104" height="26" rx="2" style="fill:#BDBDBD; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="418" y="265" style="fill:#9E9E9E; font-size:12; text-anchor:middle">entry[511]=NULL</text>

  <!-- Arrow to PD -->
  <line x1="478" y1="183" x2="530" y2="183" marker-end="url(#at)" style="stroke:#00796B; stroke-width:2"></line>

  <!-- PD Table -->
  <rect x="534" y="130" width="120" height="190" rx="4" filter="url(#sh)" style="fill:#FFFFFF; stroke:#00796B; stroke-width:2" />
  <rect x="534" y="130" width="120" height="30" rx="4" style="fill:#00796B" />
  <text x="594" y="149" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Page Directory</text>
  <text x="594" y="163" style="fill:#B2DFDB; font-size:11; text-anchor:middle">512 entries</text>
  <rect x="542" y="170" width="104" height="26" rx="2" style="fill:#E8F5E9; stroke:#00796B; stroke-width:1" />
  <text x="594" y="187" style="fill:#00796B; font-size:12; text-anchor:middle">entry[0] → PT</text>
  <rect x="542" y="198" width="104" height="26" rx="2" style="fill:#BDBDBD; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="594" y="215" style="fill:#9E9E9E; font-size:12; text-anchor:middle">entry[1] = NULL</text>
  <rect x="542" y="226" width="104" height="20" rx="2" style="fill:#F5F5F5" />
  <text x="594" y="241" style="fill:#616161; font-size:11; text-anchor:middle">... 510 more ...</text>
  <rect x="542" y="248" width="104" height="20" rx="2" style="fill:#BDBDBD; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="594" y="263" style="fill:#9E9E9E; font-size:12; text-anchor:middle">entry[511]=NULL</text>

  <!-- Arrow to PT -->
  <line x1="654" y1="183" x2="706" y2="183" marker-end="url(#at)" style="stroke:#00796B; stroke-width:2"></line>

  <!-- PT Table -->
  <rect x="710" y="130" width="120" height="190" rx="4" filter="url(#sh)" style="fill:#FFFFFF; stroke:#00796B; stroke-width:2; opacity:0.85" />
  <rect x="710" y="130" width="120" height="30" rx="4" style="fill:#00796B; opacity:0.78" />
  <text x="770" y="149" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">Page Table</text>
  <text x="770" y="163" style="fill:#B2DFDB; font-size:11; text-anchor:middle">512 PTEs</text>
  <rect x="718" y="170" width="104" height="26" rx="2" style="fill:#E8F5E9; stroke:#00796B; stroke-width:1" />
  <text x="770" y="187" style="fill:#00796B; font-size:12; text-anchor:middle">PTE[0]: PFN=0x1B7</text>
  <rect x="718" y="198" width="104" height="26" rx="2" style="fill:#E8F5E9; stroke:#00796B; stroke-width:1" />
  <text x="770" y="215" style="fill:#00796B; font-size:12; text-anchor:middle">PTE[1]: PFN=0x3C2</text>
  <rect x="718" y="226" width="104" height="20" rx="2" style="fill:#F5F5F5" />
  <text x="770" y="241" style="fill:#616161; font-size:11; text-anchor:middle">... 510 more ...</text>
  <rect x="718" y="248" width="104" height="26" rx="2" style="fill:#BDBDBD; stroke:#9E9E9E; stroke-width:1; stroke-dasharray:3,2" />
  <text x="770" y="265" style="fill:#9E9E9E; font-size:12; text-anchor:middle">PTE[511]=NULL</text>

  <!-- Arrow to Physical Page -->
  <line x1="830" y1="183" x2="855" y2="183" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2"></line>

  <!-- Physical Page -->
  <rect x="858" y="156" width="32" height="56" rx="3" style="fill:#E65100" />
  <text x="874" y="185" transform="rotate(-90,874,185)" style="fill:#FFFFFF; font-size:12; font-weight:bold; text-anchor:middle">Page 0x1B7</text>

  <!-- 4 accesses annotation -->
  <rect x="30" y="400" width="520" height="80" rx="6" filter="url(#sh)" style="fill:#FFF3E0; stroke:#E65100; stroke-width:2" />
  <text x="270" y="424" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">TLB Miss Penalty: 4 Separate DRAM Accesses!</text>
  <text x="50" y="446" style="fill:#212121; font-size:13">Access 1: Read PML4 entry from DRAM   (+70 ns)</text>
  <text x="50" y="462" style="fill:#212121; font-size:13">Access 2: Read PDPT entry from DRAM   (+70 ns)</text>
  <text x="50" y="478" style="fill:#212121; font-size:13">Access 3: Read PD entry from DRAM     (+70 ns)</text>
  <text x="310" y="446" style="fill:#212121; font-size:13">Access 4: Read PT (PTE) from DRAM     (+70 ns)</text>
  <text x="310" y="462" style="fill:#E65100; font-size:14; font-weight:bold">Total: 280 ns = ~840 wasted cycles</text>
  <text x="310" y="478" style="fill:#212121; font-size:13">+ actual data access (+70 ns more)</text>

  <!-- Memory savings explanation -->
  <rect x="560" y="400" width="316" height="80" rx="6" filter="url(#sh)" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:2" />
  <text x="718" y="424" style="fill:#2E7D32; font-size:14; font-weight:bold; text-anchor:middle">Memory Savings of Hierarchy</text>
  <text x="572" y="444" style="fill:#212121; font-size:13">Flat table for 256 TB: 512 GB/process</text>
  <text x="572" y="462" style="fill:#212121; font-size:13">4-level for typical process: ~1 MB</text>
  <text x="572" y="480" style="fill:#2E7D32; font-size:14; font-weight:bold">Saving: 512,000x reduction in PT memory!</text>

  <!-- Walkthrough example -->
  <rect x="30" y="498" width="816" height="106" rx="6" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="438" y="519" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Walk Example: VA = 0x0000_7F5A_3041_2ABC</text>
  <text x="50" y="539" style="fill:#212121; font-size:13">PML4 index = bits[47-39] = 0x0FF</text>
  <text x="50" y="557" style="fill:#212121; font-size:13">PDPT index = bits[38-30] = 0x168</text>
  <text x="50" y="575" style="fill:#212121; font-size:13">PD index   = bits[29-21] = 0x002</text>
  <text x="290" y="539" style="fill:#212121; font-size:13">PT index   = bits[20-12] = 0x012</text>
  <text x="290" y="557" style="fill:#212121; font-size:13">Offset     = bits[11-0]  = 0xABC</text>
  <text x="290" y="575" style="fill:#00796B; font-size:14; font-weight:bold">Physical = PFN &lt;&lt; 12 | 0xABC</text>
  <text x="530" y="539" style="fill:#212121; font-size:13">CR3 → PML4[0xFF] → PDPT[0x168]</text>
  <text x="530" y="557" style="fill:#212121; font-size:13">      → PD[0x002] → PT[0x012]</text>
  <text x="530" y="575" style="fill:#1565C0; font-size:14; font-weight:bold">→ Physical Frame Number → Data!</text>
</svg>
</div>
<figcaption><strong>Figure 1.17:</strong> x86-64 four-level page table
hierarchy (PGD to PUD to PMD to PTE): each level indexed by 9 bits of
the 48-bit virtual address, enabling sparse allocation.</figcaption>
</figure>

**Multi-level page tables** break the single large page table into a
tree structure, allocating page table memory **only for regions of the
address space that are actually in use**.

**Concept:** Instead of one huge table, create a hierarchy: - Level 1:
**Page Directory** (small, always present) - Level 2: **Page Tables**
(only created for used regions)

#### Example: Two-Level Page Tables

Let\'s walk through a concrete example with a 32-bit address space and 4
KB pages.

**Address Format:**

**Translation Process:**

    1. Virtual Address: 0x00403A7C

    2. Split address into components:
       Dir Index:   bits 31-22 = 0x001 = 1
       Table Index: bits 21-12 = 0x003 = 3
       Offset:      bits 11-0  = 0xA7C = 2684

    3. Walk the page table hierarchy:
       
       Step 1: Use Dir Index to find Page Table
       +-----------------------+
       |   Page Directory      |  ← Always in memory
       |  Entry 0: NULL        |
       |  Entry 1: PTE* 0x5000 |  ← Points to Page Table
       |  Entry 2: NULL        |
       |  ...                  |
       +-----------------------+
       
       Step 2: Use Table Index to find PFN
       +-----------------------+
       |  Page Table @ 0x5000  |  ← Only allocated if needed
       |  Entry 0: PFN 0x100   |
       |  Entry 1: PFN 0x101   |
       |  Entry 2: PFN 0x102   |
       |  Entry 3: PFN 0x1B7   |  ← Target entry
       |  ...                  |
       +-----------------------+
       
       Step 3: Combine PFN with Offset
       Physical Address = (0x1B7 << 12) | 0xA7C = 0x001B7A7C

    4. Access physical memory at 0x001B7A7C

#### Memory Savings

**Single-Level Page Table (32-bit system):** - Pages needed: 4 GB / 4 KB
= 1,048,576 entries - Entry size: 4 bytes - **Total size: 4 MB per
process** (always)

**Two-Level Page Table:** - Page Directory: 1,024 entries x 4 bytes =
**4 KB** (always present) - Page Tables: Only allocated for used regions

**Example Program Using 268 MB:** - Used pages: 268 MB / 4 KB = 68,608
pages - Page tables needed: 68,608 / 1,024 = 67 tables - Size: 67 x 4 KB
= **268 KB** - **Plus directory: 268 KB + 4 KB = 272 KB total**

**Savings: 4 MB → 272 KB (93% reduction!)**

For a 64-bit system with sparse usage, the savings are even more
dramatic.

#### How Many Levels?

Modern architectures use different numbers of levels:

| Architecture | Levels | Address Bits | Coverage |
| --- | --- | --- | --- |
| x86 (32-bit) | 2 | 32 bits | 4 GB |
| x86-64 (4-level) | 4 | 48 bits | 256 TB |
| x86-64 (5-level) | 5 | 57 bits | 128 PB |
| ARM64 (typical) | 4 | 48 bits | 256 TB |
| RISC-V Sv39 | 3 | 39 bits | 512 GB |
| RISC-V Sv48 | 4 | 48 bits | 256 TB |


**More levels = larger address space but slower page table walks.**

Modern 64-bit systems typically use **4-level page tables** as a sweet
spot between address space size and lookup performance.

#### Trade-offs

**Advantages:** ✅ **Huge memory savings** for sparse address spaces\
✅ **Pay only for what you use** (demand allocation)\
✅ **Enables large address spaces** (48-57 bits practical)\
✅ **Sharing between processes** easier at granular level

**Disadvantages:** ❌ **More complex hardware** (multiple memory
accesses)\
❌ **Slower on TLB miss** (must walk multiple levels)\
❌ **More page faults** possible (intermediate tables not present)

#### TLB Becomes Even More Critical

With multi-level page tables, a TLB miss becomes expensive:

**Cost of Address Translation:** - **TLB hit:** 1 cycle (\~0.3 ns) -
**TLB miss with 2-level PT:** 2 memory accesses (\~200 ns) = **667x
slower** - **TLB miss with 4-level PT:** 4 memory accesses (\~400 ns) =
**1,333x slower**

This makes the TLB\'s caching function absolutely critical. A program
with a 99% TLB hit rate will be dramatically faster than one with a 95%
hit rate, especially on systems with deep page table hierarchies.

#### Key Takeaways

1.  **Single-level page tables don\'t scale:** Would require gigabytes
    of memory per process
2.  **Address spaces are sparse:** Programs use tiny fractions of
    available address space
3.  **Multi-level hierarchies:** Allocate page table memory only for
    used regions
4.  **Memory savings are dramatic:** Often 90-99% reduction in page
    table overhead
5.  **TLB becomes essential:** Multiple memory accesses on TLB miss make
    caching critical
6.  **More levels = slower misses:** Trade-off between address space
    size and lookup cost

Multi-level page tables are a perfect example of **indirection solving a
scaling problem**. By adding a level of indirection (or several), we
transform an impractical memory requirement into a manageable one,
enabling the vast 64-bit address spaces that modern programs enjoy.

The specific implementations vary by architecture\--x86-64\'s 4-level
structure differs from ARM\'s implementation, and RISC-V offers multiple
options. We\'ll explore these architecture-specific details in Part III:
MMU in Modern Architectures.

------------------------------------------------------------------------

**This completes our introduction to the fundamental mechanisms of
address translation.** We\'ve covered: - The basic concept of pages and
page tables - How address translation works (virtual → physical) - The
critical role of the TLB in making translation fast - How multi-level
page tables make large address spaces practical

In the next section, we\'ll look at real-world examples of how these
mechanisms impact system performance and security.

## 1.10 Why MMU Matters: Real-World Impact

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="660" viewBox="0 0 900 660" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter></defs>
  <rect width="900" height="660" style="fill:#FAFAFA" />
  <text x="30" y="36" style="fill:#212121; font-size:20; font-weight:bold">Memory Latency Comparison: Access Times Across the Hierarchy</text>

  <!-- Y axis label -->
  <text x="22" y="320" transform="rotate(-90,22,320)" style="fill:#212121; font-size:14; font-weight:bold; text-anchor:middle">Access Latency (nanoseconds, log scale)</text>

  <!-- Chart area -->
  <rect x="80" y="60" width="790" height="462" rx="4" style="fill:#FFFFFF; stroke:#9E9E9E; stroke-width:1" />

  <!-- Grid lines -->
  <line x1="80" y1="420" x2="870" y2="420" style="stroke:#E0E0E0; stroke-width:1"></line>
  <line x1="80" y1="370" x2="870" y2="370" style="stroke:#E0E0E0; stroke-width:1"></line>
  <line x1="80" y1="310" x2="870" y2="310" style="stroke:#E0E0E0; stroke-width:1"></line>
  <line x1="80" y1="250" x2="870" y2="250" style="stroke:#E0E0E0; stroke-width:1"></line>
  <line x1="80" y1="190" x2="870" y2="190" style="stroke:#E0E0E0; stroke-width:1"></line>
  <line x1="80" y1="130" x2="870" y2="130" style="stroke:#E0E0E0; stroke-width:1"></line>
  <line x1="80" y1="70" x2="870" y2="70" style="stroke:#E0E0E0; stroke-width:1"></line>

  <!-- Y axis labels (log scale: 0.3, 1, 4, 14, 70, 25000, 10000000 ns) -->
  <text x="72" y="424" style="fill:#616161; font-size:12; text-anchor:end">0.3 ns</text>
  <text x="72" y="374" style="fill:#616161; font-size:12; text-anchor:end">1 ns</text>
  <text x="72" y="314" style="fill:#616161; font-size:12; text-anchor:end">4 ns</text>
  <text x="72" y="254" style="fill:#616161; font-size:12; text-anchor:end">14 ns</text>
  <text x="72" y="194" style="fill:#616161; font-size:12; text-anchor:end">70 ns</text>
  <text x="72" y="134" style="fill:#616161; font-size:12; text-anchor:end">25 us</text>
  <text x="72" y="74" style="fill:#616161; font-size:12; text-anchor:end">10 ms</text>

  <!-- Bars (log scale heights, bar x positions evenly spaced) -->
  <!-- Registers: 0.3 ns -->
  <rect x="100" y="416" width="80" height="4" rx="2" filter="url(#sh)" style="fill:#1565C0" />
  <text x="140" y="410" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:middle">0.3 ns</text>
  <text x="140" y="488" style="fill:#212121; font-size:13; text-anchor:middle">Registers</text>
  <text x="140" y="506" style="fill:#616161; font-size:11; text-anchor:middle">~1 cycle</text>

  <!-- L1: 1 ns -->
  <rect x="210" y="370" width="80" height="50" rx="2" filter="url(#sh)" style="fill:#1565C0; opacity:0.8" />
  <text x="250" y="365" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:middle">1 ns</text>
  <text x="250" y="488" style="fill:#212121; font-size:13; text-anchor:middle">L1 Cache</text>
  <text x="250" y="506" style="fill:#616161; font-size:11; text-anchor:middle">4 cycles</text>

  <!-- L2: 4 ns -->
  <rect x="320" y="310" width="80" height="110" rx="2" filter="url(#sh)" style="fill:#00796B" />
  <text x="360" y="305" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">4 ns</text>
  <text x="360" y="488" style="fill:#212121; font-size:13; text-anchor:middle">L2 Cache</text>
  <text x="360" y="506" style="fill:#616161; font-size:11; text-anchor:middle">12 cycles</text>

  <!-- L3: 14 ns -->
  <rect x="430" y="250" width="80" height="170" rx="2" filter="url(#sh)" style="fill:#00796B; opacity:0.75" />
  <text x="470" y="245" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">14 ns</text>
  <text x="470" y="488" style="fill:#212121; font-size:13; text-anchor:middle">L3 Cache</text>
  <text x="470" y="506" style="fill:#616161; font-size:11; text-anchor:middle">40 cycles</text>

  <!-- DRAM: 70 ns -->
  <rect x="540" y="190" width="80" height="230" rx="2" filter="url(#sh)" style="fill:#9E9E9E" />
  <text x="580" y="185" style="fill:#9E9E9E; font-size:13; font-weight:bold; text-anchor:middle">70 ns</text>
  <text x="580" y="488" style="fill:#212121; font-size:13; text-anchor:middle">DRAM</text>
  <text x="580" y="506" style="fill:#616161; font-size:11; text-anchor:middle">~200 cycles</text>

  <!-- SSD: 25 us = 25,000 ns -->
  <rect x="650" y="130" width="80" height="290" rx="2" filter="url(#sh)" style="fill:#E65100" />
  <text x="690" y="125" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">25 us</text>
  <text x="690" y="488" style="fill:#212121; font-size:13; text-anchor:middle">SSD/NVMe</text>
  <text x="690" y="506" style="fill:#616161; font-size:11; text-anchor:middle">~75,000 cycles</text>

  <!-- HDD: 10 ms -->
  <rect x="760" y="65" width="80" height="355" rx="2" filter="url(#sh)" style="fill:#B71C1C" />
  <text x="800" y="60" style="fill:#B71C1C; font-size:13; font-weight:bold; text-anchor:middle">10 ms</text>
  <text x="800" y="488" style="fill:#212121; font-size:13; text-anchor:middle">HDD</text>
  <text x="800" y="506" style="fill:#616161; font-size:11; text-anchor:middle">30M cycles</text>

  <!-- TLB miss annotation -->
  <line x1="540" y1="190" x2="400" y2="150" style="stroke:#E65100; stroke-width:1.5; stroke-dasharray:4,2"></line>
  <rect x="310" y="118" width="250" height="36" rx="4" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="435" y="138" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">TLB miss = 4x DRAM reads = 280 ns</text>

  <!-- Ratios annotation -->
  <rect x="82" y="544" width="786" height="96" rx="4" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="475" y="521" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Relative Performance Ratios (compared to L1 Cache = 1x)</text>
  <text x="130" y="598" style="fill:#212121; font-size:13; text-anchor:middle">Registers: 0.3x</text>
  <text x="250" y="598" style="fill:#212121; font-size:13; text-anchor:middle">L1: 1x</text>
  <text x="360" y="598" style="fill:#212121; font-size:13; text-anchor:middle">L2: 4x</text>
  <text x="455" y="598" style="fill:#212121; font-size:13; text-anchor:middle">L3: 14x</text>
  <text x="555" y="598" style="fill:#212121; font-size:13; text-anchor:middle">DRAM: 70x</text>
  <text x="668" y="598" style="fill:#212121; font-size:13; text-anchor:middle">SSD: 25,000x</text>
  <text x="790" y="598" style="fill:#212121; font-size:13; text-anchor:middle">HDD: 10,000,000x</text>
</svg>
</div>
<figcaption><strong>Figure 1.18:</strong> Memory access latency
comparison: L1 cache (~1 ns), L2 (~4 ns), L3 (~10 ns), DRAM (~100 ns),
NVMe SSD (~100 us), spinning disk (~10 ms).</figcaption>
</figure>

### Case Study 1: The Cost of TLB Misses

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="580" viewBox="0 0 900 580" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr-b" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="arr-o" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
    <marker id="arr-g" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#2E7D32"></polygon></marker>
    <marker id="arr-r" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#C62828"></polygon></marker>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
  </defs>

  <rect width="900" height="580" style="fill:#FAFAFA" />
  <text x="450" y="34" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Context Switch: TLB Flush vs. ASID/PCID Tagging</text>

  <!-- ===== TIMELINE BAR ===== -->
  <text x="450" y="58" style="fill:#616161; font-size:13; text-anchor:middle">Two approaches to maintaining TLB coherency across process switches</text>

  <!-- ===== LEFT: NAIVE FLUSH APPROACH ===== -->
  <rect x="20" y="72" width="400" height="480" rx="6" style="fill:#F5F5F5; stroke:#C62828; stroke-width:2" />
  <text x="220" y="94" style="fill:#C62828; font-size:15; font-weight:bold; text-anchor:middle">Approach 1: Full TLB Flush (Naïve)</text>

  <!-- State 1: Process A running -->
  <rect x="35" y="106" width="370" height="70" rx="4" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="220" y="126" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:middle">① Process A Running</text>
  <text x="220" y="146" style="fill:#212121; font-size:12; text-anchor:middle">TLB filled with A&#39;s translations</text>
  <text x="220" y="163" style="fill:#2E7D32; font-size:12; text-anchor:middle">TLB hit rate: ~95%  — Fast! ✓</text>

  <!-- Arrow down -->
  <line x1="220" y1="176" x2="220" y2="200" marker-end="url(#arr-b)" style="stroke:#37474F; stroke-width:2"></line>
  <text x="240" y="193" style="fill:#616161; font-size:12">OS schedules switch</text>

  <!-- Context switch / flush event -->
  <rect x="35" y="200" width="370" height="54" rx="4" style="fill:#FFEBEE; stroke:#C62828; stroke-width:2" />
  <text x="220" y="222" style="fill:#C62828; font-size:14; font-weight:bold; text-anchor:middle">② Context Switch — TLB FLUSHED</text>
  <text x="220" y="242" style="fill:#424242; font-size:12; text-anchor:middle">mov cr3, [B&#39;s page table] → ALL TLB entries invalidated</text>

  <!-- Arrow down -->
  <line x1="220" y1="254" x2="220" y2="278" marker-end="url(#arr-r)" style="stroke:#C62828; stroke-width:2"></line>

  <!-- State 2: Process B running — cold TLB -->
  <rect x="35" y="278" width="370" height="70" rx="4" style="fill:#FBE9E7; stroke:#E65100; stroke-width:1.5" />
  <text x="220" y="298" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">③ Process B Running — Cold TLB</text>
  <text x="220" y="316" style="fill:#212121; font-size:12; text-anchor:middle">Every access is a TLB miss initially</text>
  <text x="220" y="334" style="fill:#C62828; font-size:12; text-anchor:middle">TLB hit rate: ~0% initially — Very slow! ✗</text>

  <!-- Arrow down -->
  <line x1="220" y1="348" x2="220" y2="372" marker-end="url(#arr-b)" style="stroke:#37474F; stroke-width:2"></line>

  <!-- Warm-up cost -->
  <rect x="35" y="372" width="370" height="54" rx="4" style="fill:#FFF9E6; stroke:#F9A825; stroke-width:1.5" />
  <text x="220" y="392" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">④ TLB Warm-up Period</text>
  <text x="220" y="412" style="fill:#424242; font-size:12; text-anchor:middle">Hundreds of page walks required before TLB is useful</text>

  <!-- Cost box -->
  <rect x="35" y="440" width="370" height="80" rx="4" style="fill:#FFEBEE; stroke:#C62828; stroke-width:2" />
  <text x="220" y="462" style="fill:#C62828; font-size:14; font-weight:bold; text-anchor:middle">Cost Per Context Switch</text>
  <text x="220" y="482" style="fill:#424242; font-size:13; text-anchor:middle">• Each TLB miss: ~280 ns (4 DRAM accesses)</text>
  <text x="220" y="500" style="fill:#424242; font-size:13; text-anchor:middle">• 100–500 misses to warm TLB</text>
  <text x="220" y="518" style="fill:#C62828; font-size:13; text-anchor:middle">• Overhead: 28–140 µs per switch</text>

  <!-- ===== RIGHT: ASID/PCID APPROACH ===== -->
  <rect x="480" y="72" width="400" height="480" rx="6" style="fill:#F5F5F5; stroke:#2E7D32; stroke-width:2" />
  <text x="680" y="94" style="fill:#2E7D32; font-size:15; font-weight:bold; text-anchor:middle">Approach 2: ASID / PCID Tagging</text>

  <!-- State 1: Process A running -->
  <rect x="495" y="106" width="370" height="70" rx="4" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="680" y="126" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:middle">① Process A Running (ASID=1)</text>
  <text x="680" y="146" style="fill:#212121; font-size:12; text-anchor:middle">TLB entries tagged with ASID=1</text>
  <text x="680" y="163" style="fill:#2E7D32; font-size:12; text-anchor:middle">TLB hit rate: ~95% — Fast! ✓</text>

  <!-- Arrow down -->
  <line x1="680" y1="176" x2="680" y2="200" marker-end="url(#arr-b)" style="stroke:#37474F; stroke-width:2"></line>

  <!-- Context switch NO flush -->
  <rect x="495" y="200" width="370" height="54" rx="4" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:2" />
  <text x="680" y="222" style="fill:#2E7D32; font-size:14; font-weight:bold; text-anchor:middle">② Context Switch — NO FLUSH!</text>
  <text x="680" y="242" style="fill:#424242; font-size:12; text-anchor:middle">mov cr3, [B&#39;s PT] + PCID=2 → A&#39;s entries RETAINED in TLB</text>

  <!-- Arrow down -->
  <line x1="680" y1="254" x2="680" y2="278" marker-end="url(#arr-g)" style="stroke:#2E7D32; stroke-width:2"></line>

  <!-- State 2: Process B running — warm TLB -->
  <rect x="495" y="278" width="370" height="70" rx="4" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:1.5" />
  <text x="680" y="298" style="fill:#2E7D32; font-size:13; font-weight:bold; text-anchor:middle">③ Process B Running (ASID=2)</text>
  <text x="680" y="316" style="fill:#212121; font-size:12; text-anchor:middle">B&#39;s entries accumulate in TLB alongside A&#39;s</text>
  <text x="680" y="334" style="fill:#2E7D32; font-size:12; text-anchor:middle">Warms up quickly — misses only for new pages ✓</text>

  <!-- ASID tagging detail -->
  <rect x="495" y="360" width="370" height="90" rx="4" style="fill:#E0F2F1; stroke:#00796B; stroke-width:1.5" />
  <text x="680" y="380" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">TLB Entry With ASID/PCID Tag</text>
  <!-- mini TLB entry -->
  <rect x="510" y="390" width="70" height="36" rx="2" style="fill:#9E9E9E" />
  <text x="545" y="412" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">ASID</text>
  <rect x="583" y="390" width="90" height="36" rx="2" style="fill:#1565C0" />
  <text x="628" y="412" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">VPN</text>
  <rect x="676" y="390" width="80" height="36" rx="2" style="fill:#00796B" />
  <text x="716" y="412" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">PFN</text>
  <rect x="750" y="390" width="100" height="36" rx="2" style="fill:#E65100" />
  <text x="800" y="412" style="fill:#FFFFFF; font-size:11; font-weight:bold; text-anchor:middle">Flags</text>

  <!-- Benefit box -->
  <rect x="495" y="454" width="370" height="80" rx="4" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:2" />
  <text x="680" y="474" style="fill:#2E7D32; font-size:14; font-weight:bold; text-anchor:middle">Benefit: Near-Zero Switch Cost</text>
  <text x="680" y="494" style="fill:#212121; font-size:13; text-anchor:middle">• No TLB flush on context switch</text>
  <text x="680" y="512" style="fill:#212121; font-size:13; text-anchor:middle">• x86-64: 4096 PCIDs supported</text>
  <text x="680" y="530" style="fill:#2E7D32; font-size:13; text-anchor:middle">• 5–30% performance improvement</text>
</svg>
</div>
<figcaption><strong>Figure 1.19:</strong> Context switch and TLB
management: ASID-tagged TLBs allow entries from multiple address spaces
to coexist, eliminating full TLB flushes on every context
switch.</figcaption>
</figure>

**Scenario:** Database performing random lookups in a 100 GB dataset on
a system with 32 GB RAM.

**Analysis:** - Page size: 4 KB - Total pages: 25 million (100 GB / 4
KB) - Physical frames: 8 million (32 GB / 4 KB) - TLB size: 1,536
entries (Intel Xeon) - TLB coverage: 6 MB (1,536 x 4 KB)

**Result:**\
With random access patterns, TLB hit rate drops to \~5%. Each TLB miss
requires a page table walk (4 memory accesses for 4-level paging).
Performance can degrade by 60-80% compared to sequential access.

**Solution:**\
Use 2 MB huge pages: - TLB coverage: 3 GB (1,536 x 2 MB) - TLB hit rate
improves to 60% - Performance increase: 2-3x for this workload

### Case Study 2: Spectre and Meltdown

In 2018, researchers discovered that speculative execution in modern
CPUs could be exploited to leak protected memory \[Kocher et al., 2019;
Lipp et al., 2018\].

**The Vulnerability:** CPUs speculatively execute code before checking
permissions. Even though mis-speculated instructions are discarded, they
leave traces in the cache and TLB that can be measured.

**Attack Example (Simplified):**

``` {.sourceCode .c}
// Attacker code (user space)
if (x < array1_size) {  // Will be true eventually
    y = array2[array1[x] * 4096];  // Speculatively executed!
}
```

During speculative execution: 1. CPU loads `array1[x]` (x is out of
bounds, kernel memory) 2. CPU loads `array2[array1[x] * 4096]`\
3. Page brought into TLB/cache 4. Speculation was wrong → discard
results 5. BUT TLB/cache still contains traces of kernel memory! 6.
Attacker measures TLB/cache timing to infer kernel data

**Impact:** - Affected billions of CPUs (Intel, AMD, ARM) - Required OS
patches (KPTI: Kernel Page Table Isolation) - Performance overhead:
5-30% depending on workload

**Lesson:**\
Memory management isn\'t just about performance\--it\'s critical to
security. The MMU is part of the security perimeter.

### Case Study 3: Rowhammer

Rowhammer demonstrated that repeated accesses to DRAM rows can cause bit
flips in adjacent rows\--a hardware reliability issue that becomes a
security vulnerability \[Kim et al., 2014\].

**The Attack:**

``` {.sourceCode .c}
// Repeatedly access two rows (hammering)
while (1) {
    *addr1;
    *addr2;  
    clflush(addr1);  // Bypass cache
    clflush(addr2);
}
// Causes bit flips in adjacent physical rows
```

**MMU Connection:** Attackers used the MMU\'s address translation to: 1.
Determine which virtual addresses map to adjacent physical rows 2.
Bypass MMU protection to corrupt page tables 3. Gain kernel privileges

**Impact:** - Demonstrated in 2015 (Google Project Zero) - Exploitable
from JavaScript (no native code needed) - Led to TRR (Target Row
Refresh) in DRAM

------------------------------------------------------------------------

## 1.11 Looking Ahead

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="650" viewBox="0 0 900 650" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr-b" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
    <marker id="arr-o" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
    <marker id="arr-g" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#2E7D32"></polygon></marker>
    <marker id="arr-r" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#C62828"></polygon></marker>
    <filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
  </defs>

  <rect width="900" height="650" style="fill:#FAFAFA" />
  <text x="450" y="34" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Page Fault Handling: Complete Flow</text>

  <!-- Step 1: CPU access -->
  <rect x="300" y="52" width="300" height="52" rx="6" filter="url(#sh)" style="fill:#1565C0" />
  <text x="450" y="74" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">① CPU Memory Access</text>
  <text x="450" y="93" style="fill:#BBDEFB; font-size:12; text-anchor:middle">Program accesses virtual address 0x5000_1234</text>

  <line x1="450" y1="104" x2="450" y2="128" marker-end="url(#arr-b)" style="stroke:#1565C0; stroke-width:2.5"></line>

  <!-- Step 2: MMU checks -->
  <rect x="300" y="128" width="300" height="52" rx="6" filter="url(#sh)" style="fill:#37474F" />
  <text x="450" y="150" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">② MMU: TLB Lookup</text>
  <text x="450" y="168" style="fill:#B0BEC5; font-size:12; text-anchor:middle">TLB miss → Page Table Walk → P=0 in PTE</text>

  <line x1="450" y1="180" x2="450" y2="204" marker-end="url(#arr-r)" style="stroke:#C62828; stroke-width:2.5"></line>

  <!-- Step 3: Hardware trap -->
  <rect x="300" y="204" width="300" height="52" rx="6" filter="url(#sh)" style="fill:#C62828" />
  <text x="450" y="226" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">③ #PF Exception Raised</text>
  <text x="450" y="244" style="fill:#FFCDD2; font-size:12; text-anchor:middle">Hardware saves PC + CR2 (faulting VA) → OS</text>

  <line x1="450" y1="256" x2="450" y2="280" marker-end="url(#arr-o)" style="stroke:#E65100; stroke-width:2.5"></line>

  <!-- Step 4: OS validates -->
  <!-- Diamond for decision -->
  <polygon points="450,280 570,312 450,344 330,312" filter="url(#sh)" style="fill:#E65100"></polygon>
  <text x="450" y="308" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">④ Is VA Valid?</text>
  <text x="450" y="326" style="fill:#FFE0B2; font-size:11; text-anchor:middle">Check VMAs in OS</text>

  <!-- No path → SIGSEGV -->
  <line x1="570" y1="312" x2="660" y2="312" marker-end="url(#arr-r)" style="stroke:#C62828; stroke-width:2"></line>
  <text x="613" y="306" style="fill:#C62828; font-size:12; font-weight:bold; text-anchor:middle">NO</text>
  <rect x="660" y="288" width="220" height="48" rx="6" filter="url(#sh)" style="fill:#FFEBEE; stroke:#C62828; stroke-width:2" />
  <text x="770" y="308" style="fill:#C62828; font-size:14; font-weight:bold; text-anchor:middle">SIGSEGV Delivered</text>
  <text x="770" y="326" style="fill:#C62828; font-size:12; text-anchor:middle">Program killed (segfault)</text>

  <!-- Yes path → where is page -->
  <line x1="450" y1="344" x2="450" y2="368" marker-end="url(#arr-g)" style="stroke:#2E7D32; stroke-width:2"></line>
  <text x="464" y="360" style="fill:#2E7D32; font-size:12; font-weight:bold">YES</text>

  <!-- Step 5: Find page source -->
  <polygon points="450,368 590,404 450,440 310,404" filter="url(#sh)" style="fill:#5C6BC0"></polygon>
  <text x="450" y="400" style="fill:#FFFFFF; font-size:13; font-weight:bold; text-anchor:middle">⑤ Where Is the Page?</text>
  <text x="450" y="418" style="fill:#E8EAF6; font-size:11; text-anchor:middle">OS checks backing store</text>

  <!-- Four outcomes -->
  <!-- Outcome A: Zero fill (new allocation) -->
  <line x1="310" y1="404" x2="170" y2="450" marker-end="url(#arr-g)" style="stroke:#00796B; stroke-width:2"></line>
  <text x="220" y="432" style="fill:#00796B; font-size:11; text-anchor:middle">New alloc</text>
  <rect x="20" y="450" width="200" height="60" rx="4" filter="url(#sh)" style="fill:#E0F2F1; stroke:#00796B; stroke-width:1.5" />
  <text x="120" y="470" style="fill:#00796B; font-size:12; font-weight:bold; text-anchor:middle">Zero-Fill Page</text>
  <text x="120" y="486" style="fill:#424242; font-size:11; text-anchor:middle">Allocate frame, zero it</text>
  <text x="120" y="502" style="fill:#00796B; font-size:11; text-anchor:middle">~1 µs</text>

  <!-- Outcome B: File-backed (mmap) -->
  <line x1="390" y1="440" x2="310" y2="490" marker-end="url(#arr-b)" style="stroke:#1565C0; stroke-width:2"></line>
  <text x="320" y="466" style="fill:#1565C0; font-size:11; text-anchor:middle">File-backed</text>
  <rect x="226" y="490" width="200" height="60" rx="4" filter="url(#sh)" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="326" y="510" style="fill:#1565C0; font-size:12; font-weight:bold; text-anchor:middle">Load from File</text>
  <text x="326" y="526" style="fill:#424242; font-size:11; text-anchor:middle">Read from mmap&#39;d file</text>
  <text x="326" y="542" style="fill:#E65100; font-size:11; text-anchor:middle">~100 µs (SSD)</text>

  <!-- Outcome C: Swap -->
  <line x1="510" y1="440" x2="590" y2="490" marker-end="url(#arr-o)" style="stroke:#E65100; stroke-width:2"></line>
  <text x="570" y="466" style="fill:#E65100; font-size:11; text-anchor:middle">On swap</text>
  <rect x="464" y="490" width="200" height="60" rx="4" filter="url(#sh)" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="564" y="510" style="fill:#E65100; font-size:12; font-weight:bold; text-anchor:middle">Swap In from Disk</text>
  <text x="564" y="526" style="fill:#424242; font-size:11; text-anchor:middle">Read from swap partition</text>
  <text x="564" y="542" style="fill:#C62828; font-size:11; text-anchor:middle">~100 µs–10 ms</text>

  <!-- Outcome D: COW -->
  <line x1="590" y1="404" x2="740" y2="450" marker-end="url(#arr-b)" style="stroke:#9C27B0; stroke-width:2"></line>
  <text x="686" y="432" style="fill:#9C27B0; font-size:11; text-anchor:middle">COW fault</text>
  <rect x="694" y="450" width="200" height="60" rx="4" filter="url(#sh)" style="fill:#F3E5F5; stroke:#9C27B0; stroke-width:1.5" />
  <text x="794" y="470" style="fill:#9C27B0; font-size:12; font-weight:bold; text-anchor:middle">Copy-On-Write</text>
  <text x="794" y="486" style="fill:#424242; font-size:11; text-anchor:middle">Copy shared page → new frame</text>
  <text x="794" y="502" style="fill:#9C27B0; font-size:11; text-anchor:middle">~1 µs + copy time</text>

  <!-- Convergence: Update PTE and resume -->
  <!-- Arrows from all outcomes to final step -->
  <line x1="120" y1="510" x2="120" y2="590" style="stroke:#2E7D32; stroke-width:1.5; stroke-dasharray:3,2"></line>
  <line x1="120" y1="590" x2="295" y2="590" marker-end="url(#arr-g)" style="stroke:#2E7D32; stroke-width:1.5"></line>
  <line x1="326" y1="550" x2="326" y2="590" style="stroke:#2E7D32; stroke-width:1.5; stroke-dasharray:3,2"></line>
  <line x1="326" y1="590" x2="295" y2="590" style="stroke:#2E7D32; stroke-width:1.5"></line>
  <line x1="564" y1="550" x2="564" y2="590" style="stroke:#2E7D32; stroke-width:1.5; stroke-dasharray:3,2"></line>
  <line x1="564" y1="590" x2="605" y2="590" marker-end="url(#arr-g)" style="stroke:#2E7D32; stroke-width:1.5"></line>
  <line x1="794" y1="510" x2="794" y2="590" style="stroke:#2E7D32; stroke-width:1.5; stroke-dasharray:3,2"></line>
  <line x1="794" y1="590" x2="605" y2="590" style="stroke:#2E7D32; stroke-width:1.5"></line>

  <!-- Step 6: Update PTE and retry -->
  <rect x="295" y="568" width="310" height="60" rx="6" filter="url(#sh)" style="fill:#2E7D32" />
  <text x="450" y="590" style="fill:#FFFFFF; font-size:14; font-weight:bold; text-anchor:middle">⑥ Update PTE → Set P=1 → Retry</text>
  <text x="450" y="610" style="fill:#C8E6C9; font-size:12; text-anchor:middle">PTE updated, TLB filled, instruction re-executed transparently</text>

  <!-- Latency summary sidebar -->
  <rect x="20" y="52" width="270" height="130" rx="4" style="fill:#FFF9E6; stroke:#F9A825; stroke-width:1.5" />
  <text x="155" y="72" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Page Fault Cost Summary</text>
  <text x="35" y="93" style="fill:#2E7D32; font-size:12; font-weight:bold">Zero/COW fill:</text>
  <text x="35" y="110" style="fill:#424242; font-size:12">~1–10 µs</text>
  <text x="35" y="128" style="fill:#E65100; font-size:12; font-weight:bold">SSD swap in:</text>
  <text x="35" y="145" style="fill:#424242; font-size:12">~100 µs = 400,000 cycles</text>
  <text x="35" y="163" style="fill:#C62828; font-size:12; font-weight:bold">HDD swap in:</text>
  <text x="35" y="180" style="fill:#424242; font-size:12">~10 ms = 40,000,000 cycles!</text>
</svg>
</div>
<figcaption><strong>Figure 1.20:</strong> Page fault handling flow: CPU
raises fault on unmapped access; OS handler maps page into a free frame;
PTE updated; faulting instruction retried.</figcaption>
</figure>

This chapter has introduced the fundamental concepts of memory
management: - The memory wall and why management is necessary -
Evolution from simple base/bounds to modern paging - The role of
hardware (MMU), OS, and applications - Virtual memory abstraction and
its benefits - Real-world security and performance implications

**In the chapters ahead:**

**Chapter 2:** Virtual memory concepts in depth\--demand paging, page
replacement algorithms, working sets, thrashing

**Chapter 3:** Hardware implementation of MMUs\--page table formats,
multi-level paging, TLB design

**Part II:** Historical evolution\--from Atlas to modern architectures

**Part III:** Deep dives into x86, ARM, RISC-V, and other architectures

**Part IV:** Advanced techniques\--huge pages, NUMA, memory compression

**Part V:** Security\--memory protection, confidential computing,
isolation

**Part VI:** Vulnerabilities\--Spectre, Meltdown, Rowhammer, and
mitigations

**Part VII:** Debugging and testing MMU implementations

**Part VIII:** Future directions\--CXL, disaggregated memory, AI
workloads

**Part IX:** Performance optimization for real-world systems

------------------------------------------------------------------------

## 1.12 Chapter Summary

**Key Takeaways:**

1.  **Memory management bridges the memory wall** between fast CPUs and
    slow DRAM through caching and virtual memory.

2.  **Paging solves fragmentation** by using fixed-size pages, enabling
    efficient allocation and virtual memory.

3.  **The MMU performs address translation** billions of times per
    second, making virtual memory practical.

4.  **Virtual memory provides powerful abstractions**: large address
    spaces, isolation, memory overcommitment, and simplified
    programming.

5.  **Performance matters**: TLB misses and page faults can dominate
    execution time in memory-intensive workloads.

6.  **Security is fundamental**: The MMU enforces isolation, but
    vulnerabilities like Spectre and Rowhammer show that hardware memory
    protection is subtle and complex.

**Thought-Provoking Questions:**

1.  If CPU speeds continue increasing while memory latency stagnates,
    what percentage of CPU time will be spent waiting for memory?

2.  How large should page sizes be? Larger pages reduce translation
    overhead but increase internal fragmentation. What\'s the optimal
    tradeoff?

3.  Can we eliminate page tables entirely? What alternative translation
    mechanisms might be possible?

4.  Should applications be aware of physical memory layout (NUMA, memory
    tiers)? Or should the OS hide this complexity?

5.  With persistent memory (NVDIMMs, Optane), do we need to rethink the
    entire virtual memory model?

------------------------------------------------------------------------

## References and Further Reading

1.  **Hennessy, J. L., & Patterson, D. A. (2024)**. *Computer
    Architecture: A Quantitative Approach* (7th ed.). Morgan Kaufmann.
    Chapter 2: Memory Hierarchy Design.

2.  **Denning, P. J. (1970)**. \"Virtual memory\". *Computing Surveys*,
    2(3), 153-189.

3.  **Kilburn, T., Edwards, D. B. G., Lanigan, M. J., & Sumner, F. H.
    (1962)**. \"One-level storage system\". *IRE Transactions on
    Electronic Computers*, EC-11(2), 223-235.

4.  **Jacob, B., Ng, S. W., & Wang, D. T. (2010)**. *Memory Systems:
    Cache, DRAM, Disk*. Morgan Kaufmann.

5.  **Kocher, P., et al. (2019)**. \"Spectre attacks: Exploiting
    speculative execution\". *Communications of the ACM*, 63(7), 93-101.

6.  **Lipp, M., et al. (2018)**. \"Meltdown: Reading kernel memory from
    user space\". *27th USENIX Security Symposium*.

7.  **Kim, Y., et al. (2014)**. \"Flipping bits in memory without
    accessing them: An experimental study of DRAM disturbance errors\".
    *ISCA 2014*.

8.  **Arpaci-Dusseau, R. H., & Arpaci-Dusseau, A. C. (2018)**.
    *Operating Systems: Three Easy Pieces*. Chapter 18-23 (Virtual
    Memory). Available at: https://pages.cs.wisc.edu/\~remzi/OSTEP/

**Recommended Videos:** - MIT 6.004: \"Memory Hierarchy and Caches\"
(OCW) - CMU 15-213: \"Virtual Memory\" lecture by Bryant & O\'Hallaron

------------------------------------------------------------------------

*Next Chapter: Virtual Memory Concepts - Deep dive into demand paging,
page replacement algorithms, and the working set model.*
