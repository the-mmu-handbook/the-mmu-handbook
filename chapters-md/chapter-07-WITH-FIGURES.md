---
nav_exclude: true
sitemap: false
---

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: container
::: {#title-block-header}
# Chapter 7: Page Faults and Exception Handling {#chapter-7-page-faults-and-exception-handling .title}
:::

- [Chapter 7: Page Faults and Exception
  Handling](#chapter-7-page-faults-and-exception-handling){#toc-chapter-7-page-faults-and-exception-handling}
  - [7.1 Introduction: When Address Translation
    Fails](#introduction-when-address-translation-fails){#toc-introduction-when-address-translation-fails}
    - [1. Page Faults Are the Enforcement
      Mechanism](#page-faults-are-the-enforcement-mechanism){#toc-page-faults-are-the-enforcement-mechanism}
    - [2. Page Faults Are on the Critical
      Path](#page-faults-are-on-the-critical-path){#toc-page-faults-are-on-the-critical-path}
    - [3. Page Faults Are Security
      Boundaries](#page-faults-are-security-boundaries){#toc-page-faults-are-security-boundaries}
    - [4. Page Faults Are Debugging
      Windows](#page-faults-are-debugging-windows){#toc-page-faults-are-debugging-windows}
    - [What This Chapter
      Covers](#what-this-chapter-covers){#toc-what-this-chapter-covers}
    - [What We Exclude](#what-we-exclude){#toc-what-we-exclude}
  - [7.2 Page Fault
    Fundamentals](#page-fault-fundamentals){#toc-page-fault-fundamentals}
    - [7.2.1 What is a Page
      Fault?](#what-is-a-page-fault){#toc-what-is-a-page-fault}
    - [7.2.2 Page Fault
      Causes](#page-fault-causes){#toc-page-fault-causes}
    - [7.2.3 Page Fault Types](#page-fault-types){#toc-page-fault-types}
    - [7.2.4 Hardware vs Software
      Components](#hardware-vs-software-components){#toc-hardware-vs-software-components}
    - [7.2.5 Page Fault in the Context of Address
      Translation](#page-fault-in-the-context-of-address-translation){#toc-page-fault-in-the-context-of-address-translation}
  - [7.3 x86-64 Page Faults
    (#PF)](#x86-64-page-faults-pf){#toc-x86-64-page-faults-pf}
    - [7.3.1 Page Fault Exception (#PF, Vector
      14)](#page-fault-exception-pf-vector-14){#toc-page-fault-exception-pf-vector-14}
    - [7.3.2 Page Fault Error
      Code](#page-fault-error-code){#toc-page-fault-error-code}
    - [7.3.3 CR2 Register: The Faulting
      Address](#cr2-register-the-faulting-address){#toc-cr2-register-the-faulting-address}
    - [7.3.4 Page Fault Handler
      Flow](#page-fault-handler-flow){#toc-page-fault-handler-flow}
    - [7.3.5 Common x86-64 Page Fault
      Scenarios](#common-x86-64-page-fault-scenarios){#toc-common-x86-64-page-fault-scenarios}
    - [7.3.6 x86-64 Error Code Summary
      Table](#x86-64-error-code-summary-table){#toc-x86-64-error-code-summary-table}
  - [7.4 ARM64 Data and Instruction
    Aborts](#arm64-data-and-instruction-aborts){#toc-arm64-data-and-instruction-aborts}
    - [7.4.1 ARM64 Synchronous Exception
      Model](#arm64-synchronous-exception-model){#toc-arm64-synchronous-exception-model}
    - [7.4.2 Data Abort vs Instruction
      Abort](#data-abort-vs-instruction-abort){#toc-data-abort-vs-instruction-abort}
    - [7.4.3 Exception Syndrome Register
      (ESR_EL1)](#exception-syndrome-register-esr_el1){#toc-exception-syndrome-register-esr_el1}
    - [7.4.4 Fault Status Codes
      (DFSC/IFSC)](#fault-status-codes-dfscifsc){#toc-fault-status-codes-dfscifsc}
    - [7.4.5 Reading Exception
      Information](#reading-exception-information){#toc-reading-exception-information}
    - [7.4.6 ARM64 Exception
      Scenarios](#arm64-exception-scenarios){#toc-arm64-exception-scenarios}
    - [7.4.7 PAN (Privileged Access
      Never)](#pan-privileged-access-never){#toc-pan-privileged-access-never}
    - [7.4.8 ARM Realm Management Extension (RME)
      Faults](#arm-realm-management-extension-rme-faults){#toc-arm-realm-management-extension-rme-faults}
  - [7.5 RISC-V Page
    Faults](#risc-v-page-faults){#toc-risc-v-page-faults}
    - [7.5.1 Software-Managed TLB and Page
      Faults](#software-managed-tlb-and-page-faults){#toc-software-managed-tlb-and-page-faults}
    - [7.5.2 RISC-V Exception
      Codes](#risc-v-exception-codes){#toc-risc-v-exception-codes}
    - [7.5.3 RISC-V Exception
      Registers](#risc-v-exception-registers){#toc-risc-v-exception-registers}
    - [7.5.4 RISC-V Page Table Walk (Software
      Implementation)](#risc-v-page-table-walk-software-implementation){#toc-risc-v-page-table-walk-software-implementation}
    - [7.5.5 RISC-V TLB
      Management](#risc-v-tlb-management){#toc-risc-v-tlb-management}
    - [7.5.6 RISC-V Page Fault Handler
      Flow](#risc-v-page-fault-handler-flow){#toc-risc-v-page-fault-handler-flow}
    - [7.5.7 RISC-V Page Fault
      Scenarios](#risc-v-page-fault-scenarios){#toc-risc-v-page-fault-scenarios}
    - [7.5.8 RISC-V Physical Memory Protection
      (PMP)](#risc-v-physical-memory-protection-pmp){#toc-risc-v-physical-memory-protection-pmp}
    - [7.5.9 RISC-V Performance
      Considerations](#risc-v-performance-considerations){#toc-risc-v-performance-considerations}
  - [7.6 TLB-Related
    Exceptions](#tlb-related-exceptions){#toc-tlb-related-exceptions}
    - [7.6.1 TLB Misses on Software-Managed
      TLBs](#tlb-misses-on-software-managed-tlbs){#toc-tlb-misses-on-software-managed-tlbs}
    - [7.6.2 TLB Multi-Hit
      Exceptions](#tlb-multi-hit-exceptions){#toc-tlb-multi-hit-exceptions}
    - [7.6.3 TLB Shootdown and Inter-Processor Interrupts
      (IPIs)](#tlb-shootdown-and-inter-processor-interrupts-ipis){#toc-tlb-shootdown-and-inter-processor-interrupts-ipis}
    - [7.6.4 TLB Maintenance Instructions and
      Exceptions](#tlb-maintenance-instructions-and-exceptions){#toc-tlb-maintenance-instructions-and-exceptions}
  - [7.7 Page Table Walk
    Failures](#page-table-walk-failures){#toc-page-table-walk-failures}
    - [7.7.1 Multi-Level Page Table
      Failures](#multi-level-page-table-failures){#toc-multi-level-page-table-failures}
    - [7.7.2 Invalid Page Table
      Pointers](#invalid-page-table-pointers){#toc-invalid-page-table-pointers}
    - [7.7.3 Nested Page Table
      Failures](#nested-page-table-failures){#toc-nested-page-table-failures}
    - [7.7.4 Reserved Bits and
      Future-Proofing](#reserved-bits-and-future-proofing){#toc-reserved-bits-and-future-proofing}
  - [7.8 Page Overlapping and Aliasing
    Faults](#page-overlapping-and-aliasing-faults){#toc-page-overlapping-and-aliasing-faults}
    - [7.8.1 What is Page
      Aliasing?](#what-is-page-aliasing){#toc-what-is-page-aliasing}
    - [7.8.2 x86-64 PAT (Page Attribute Table)
      Conflicts](#x86-64-pat-page-attribute-table-conflicts){#toc-x86-64-pat-page-attribute-table-conflicts}
    - [7.8.3 ARM64 Memory Attribute
      Conflicts](#arm64-memory-attribute-conflicts){#toc-arm64-memory-attribute-conflicts}
    - [7.8.4 Virtual Cache Aliasing (VIPT
      Caches)](#virtual-cache-aliasing-vipt-caches){#toc-virtual-cache-aliasing-vipt-caches}
    - [7.8.5 Detecting and Preventing Virtual
      Aliasing](#detecting-and-preventing-virtual-aliasing){#toc-detecting-and-preventing-virtual-aliasing}
    - [7.8.6 Security: Rowhammer and Aliasing
      Attacks](#security-rowhammer-and-aliasing-attacks){#toc-security-rowhammer-and-aliasing-attacks}
    - [7.8.7 Shared Memory and Intentional
      Aliasing](#shared-memory-and-intentional-aliasing){#toc-shared-memory-and-intentional-aliasing}
  - [7.9 Permission
    Violations](#permission-violations){#toc-permission-violations}
    - [7.9.1 Read/Write/Execute Permission
      Faults](#readwriteexecute-permission-faults){#toc-readwriteexecute-permission-faults}
    - [7.9.2 User/Supervisor
      Violations](#usersupervisor-violations){#toc-usersupervisor-violations}
    - [7.9.3 SMEP (Supervisor Mode Execution
      Prevention)](#smep-supervisor-mode-execution-prevention){#toc-smep-supervisor-mode-execution-prevention}
    - [7.9.4 SMAP (Supervisor Mode Access
      Prevention)](#smap-supervisor-mode-access-prevention){#toc-smap-supervisor-mode-access-prevention}
    - [7.9.5 ARM PAN (Privileged Access
      Never)](#arm-pan-privileged-access-never){#toc-arm-pan-privileged-access-never}
    - [7.9.6 Memory Protection Keys
      (MPK/PKU)](#memory-protection-keys-mpkpku){#toc-memory-protection-keys-mpkpku}
  - [7.10 Page Fault Handling
    Flow](#page-fault-handling-flow){#toc-page-fault-handling-flow}
    - [7.10.1 Hardware Steps](#hardware-steps){#toc-hardware-steps}
    - [7.10.2 Software Handler
      Entry](#software-handler-entry){#toc-software-handler-entry}
    - [7.10.3 Finding the VMA (Virtual Memory
      Area)](#finding-the-vma-virtual-memory-area){#toc-finding-the-vma-virtual-memory-area}
    - [7.10.4 Permission
      Checking](#permission-checking){#toc-permission-checking}
    - [7.10.5 Demand Paging
      Implementation](#demand-paging-implementation){#toc-demand-paging-implementation}
    - [7.10.6 Copy-on-Write (COW)
      Implementation](#copy-on-write-cow-implementation){#toc-copy-on-write-cow-implementation}
    - [7.10.7 Stack Growth
      Handling](#stack-growth-handling){#toc-stack-growth-handling}
    - [7.10.8 Complete Page Fault
      Handler](#complete-page-fault-handler){#toc-complete-page-fault-handler}
    - [7.10.9 Swap Handling](#swap-handling){#toc-swap-handling}
    - [7.10.10 Returning from Page
      Fault](#returning-from-page-fault){#toc-returning-from-page-fault}
    - [7.10.1 Hardware Steps
      (Architecture-Independent)](#hardware-steps-architecture-independent){#toc-hardware-steps-architecture-independent}
    - [7.10.2 Software Handler
      Steps](#software-handler-steps){#toc-software-handler-steps}
    - [7.10.3 Demand Paging
      Implementation](#demand-paging-implementation-1){#toc-demand-paging-implementation-1}
    - [7.10.4 Copy-on-Write (COW)
      Implementation](#copy-on-write-cow-implementation-1){#toc-copy-on-write-cow-implementation-1}
    - [7.10.5 Swap-In (Major Page
      Fault)](#swap-in-major-page-fault){#toc-swap-in-major-page-fault}
    - [7.10.6 Stack Growth](#stack-growth){#toc-stack-growth}
    - [7.10.7 Invalid Fault
      Handling](#invalid-fault-handling){#toc-invalid-fault-handling}
    - [7.10.8 Complete Page Fault Handler
      (Integrated)](#complete-page-fault-handler-integrated){#toc-complete-page-fault-handler-integrated}
  - [7.11 Performance
    Implications](#performance-implications){#toc-performance-implications}
    - [7.11.1 Page Fault Cost
      Breakdown](#page-fault-cost-breakdown){#toc-page-fault-cost-breakdown}
    - [7.11.2 Page Fault Rate
      Impact](#page-fault-rate-impact){#toc-page-fault-rate-impact}
    - [7.11.3 Real-World Page Fault
      Profiling](#real-world-page-fault-profiling){#toc-real-world-page-fault-profiling}
    - [7.11.4 Reducing Page
      Faults](#reducing-page-faults){#toc-reducing-page-faults}
    - [7.11.5 Page Fault Performance
      Anti-Patterns](#page-fault-performance-anti-patterns){#toc-page-fault-performance-anti-patterns}
    - [7.11.6 Page Fault Performance
      Monitoring](#page-fault-performance-monitoring){#toc-page-fault-performance-monitoring}
  - [7.12 Historical Architectures: SPARC, MIPS,
    PowerPC](#historical-architectures-sparc-mips-powerpc){#toc-historical-architectures-sparc-mips-powerpc}
    - [7.12.1 SPARC Architecture (Sun
      Microsystems)](#sparc-architecture-sun-microsystems){#toc-sparc-architecture-sun-microsystems}
    - [7.12.2 MIPS
      Architecture](#mips-architecture){#toc-mips-architecture}
    - [7.12.3 PowerPC Architecture
      (IBM/Motorola)](#powerpc-architecture-ibmmotorola){#toc-powerpc-architecture-ibmmotorola}
    - [7.12.4 Comparison
      Table](#comparison-table){#toc-comparison-table}
    - [7.12.5 Lessons Learned](#lessons-learned){#toc-lessons-learned}
  - [7.13 Architecture
    Comparison](#architecture-comparison){#toc-architecture-comparison}
    - [7.13.1 Fault Detection and
      Reporting](#fault-detection-and-reporting){#toc-fault-detection-and-reporting}
    - [7.13.2 Hardware vs Software
      Responsibility](#hardware-vs-software-responsibility){#toc-hardware-vs-software-responsibility}
    - [7.13.3 Protection
      Mechanisms](#protection-mechanisms){#toc-protection-mechanisms}
    - [7.13.4 Exception
      Priority](#exception-priority){#toc-exception-priority}
    - [7.13.5 Performance
      Characteristics](#performance-characteristics){#toc-performance-characteristics}
  - [7.14 Debugging Page
    Faults](#debugging-page-faults){#toc-debugging-page-faults}
    - [7.14.1 Common Page Fault
      Patterns](#common-page-fault-patterns){#toc-common-page-fault-patterns}
    - [7.14.2 Reading Kernel Oops
      Messages](#reading-kernel-oops-messages){#toc-reading-kernel-oops-messages}
    - [7.14.3 GDB Debugging of Page
      Faults](#gdb-debugging-of-page-faults){#toc-gdb-debugging-of-page-faults}
    - [7.14.4 Using
      strace/ltrace](#using-straceltrace){#toc-using-straceltrace}
    - [7.14.5 Performance
      Debugging](#performance-debugging){#toc-performance-debugging}
  - [7.15 Advanced Topics and
    Summary](#advanced-topics-and-summary){#toc-advanced-topics-and-summary}
    - [7.15.1 Asynchronous Page Faults
      (Virtualization)](#asynchronous-page-faults-virtualization){#toc-asynchronous-page-faults-virtualization}
    - [7.15.2 User-Space Page Fault Handling
      (userfaultfd)](#user-space-page-fault-handling-userfaultfd){#toc-user-space-page-fault-handling-userfaultfd}
    - [7.15.3 Memory Error
      Handling](#memory-error-handling){#toc-memory-error-handling}
    - [7.15.4 Summary](#summary){#toc-summary}
    - [7.15.5 References](#references){#toc-references}

# Chapter 7: Page Faults and Exception Handling {#chapter-7-page-faults-and-exception-handling}

## 7.1 Introduction: When Address Translation Fails

**Building on Previous Chapters:**

In Chapter 3 (Page Tables), we explored how page table structures map
virtual addresses to physical addresses across x86-64, ARM64, and RISC-V
architectures. We saw the elegant hierarchies---four-level page tables
on x86-64, the flexible 48/52-bit addressing on ARM64, and the
Sv39/Sv48/Sv57 schemes in RISC-V. In Chapter 4 (TLB), we discovered how
the Translation Lookaside Buffer caches these translations, turning a
100-cycle page table walk into a 1-cycle lookup. Chapter 5 (IOMMU)
extended these concepts to devices, showing how DMA remapping provides
the same protections for hardware as the MMU provides for software. And
in Chapter 6 (Memory Protection), we examined how permission
bits---R/W/X, U/S, NX, SMEP, SMAP---enforce security policies at the
hardware level.

But we\'ve largely assumed that translation succeeds. We\'ve studied the
happy path: virtual address enters the TLB, TLB hits, translation
completes, memory access proceeds. We\'ve examined page table structures
assuming they\'re valid and present. We\'ve discussed protection bits
assuming they permit the access being attempted.

**This chapter reveals what happens when translation fails.**

Every mechanism we\'ve studied has failure modes. A page table entry
might have its Present bit cleared. A TLB on a software-managed system
(RISC-V) might have no matching entry. A permission check might detect a
user process accessing kernel memory. An instruction fetch might target
a page marked non-executable. A write might attempt to modify a
read-only page. When these failures occur, the MMU doesn\'t just return
garbage data or allow unauthorized access---it generates a **page
fault**, a precisely-defined exception that transfers control to the
operating system\'s fault handler.

Understanding these failure modes is critical for four fundamental
reasons:

### 1. Page Faults Are the Enforcement Mechanism

Page faults aren\'t errors---they\'re features. They\'re how modern
operating systems implement the virtual memory concepts we studied in
Chapter 2:

**Demand Paging:** When a process starts, the OS doesn\'t load all its
code and data into memory. Instead, it marks pages as \"not present\" in
the page tables. When the process accesses one of these pages, a page
fault occurs. The OS fault handler allocates a physical page, loads the
data from disk, updates the page table, and returns. The process never
knows it happened---the instruction that faulted simply retries and
succeeds.

**Copy-on-Write (COW):** When `fork()` creates a child process, the OS
doesn\'t copy all the parent\'s memory pages. Instead, it marks all
pages in both parent and child as read-only and sets a special flag
indicating they\'re COW pages. When either process attempts to write to
a shared page, a page fault occurs. The handler allocates a new physical
page, copies the data, updates the faulting process\'s page table to
point to the new page (now writable), and returns. This is why `fork()`
is fast even when the parent process has gigabytes of memory.

**Stack Growth:** The OS allocates a small initial stack for each
thread. When the stack pointer moves beyond this region, a page fault
occurs. If the faulting address is just below the current stack limit,
the handler recognizes this as legitimate stack growth, allocates
additional pages, and returns. If the address is far from the stack
(like a recursive function that\'s blown the stack), the handler sends
SIGSEGV instead.

**Memory-Mapped Files:** The `mmap()` system call maps files into the
process\'s address space, but initially marks all pages as not present.
When the process accesses the mapped region, page faults bring the data
in on demand. Dirty pages are written back to the file when unmapped or
when the OS needs to reclaim memory.

Without page faults, virtual memory would be static and inflexible. Page
faults are what make it dynamic.

### 2. Page Faults Are on the Critical Path

In Chapter 4, we saw that TLB misses can dominate performance if they
occur frequently. Page faults are even more expensive:

- **TLB miss (with hardware page walker):** 40-100 cycles (\~10-25 ns)
- **Minor page fault:** 1,000-20,000 cycles (\~1-5 microseconds)\
- **Major page fault (from disk):** 1-10 milliseconds

A system under memory pressure might service thousands of page faults
per second. If your application touches 10GB of memory and your machine
only has 8GB of RAM, the OS will be constantly swapping pages in and
out, generating page faults continuously. A poorly-designed fault
handler can bring the system to its knees.

Consider a real-world scenario: A database server with 256GB of RAM
running a workload that touches 280GB of data. That 24GB excess means
constant paging. If the OS page fault handler is inefficient---say,
taking 10 microseconds instead of 2 microseconds per minor fault---and
the system is handling 50,000 faults per second, the difference is
between 100ms and 500ms of CPU time per second spent just in the fault
handler. That\'s 10% vs 50% overhead just from page fault handling!

Understanding page fault costs and how to minimize them is essential for
writing high-performance systems software.

### 3. Page Faults Are Security Boundaries

Many of the security mechanisms we studied in Chapter 6 work by
deliberately causing page faults when security policies are violated:

**NX/XD/XN bit:** When code attempts to execute from a page marked
non-executable (the heap, the stack, or data pages), the MMU generates a
page fault with a specific error code indicating an instruction fetch
from a non-executable page. The OS fault handler recognizes this as a
security violation and terminates the process with SIGSEGV. This single
mechanism prevents entire classes of exploits---buffer overflow attacks
that inject shellcode into the stack or heap.

**SMEP (Supervisor Mode Execution Prevention):** On x86-64, when the
kernel (supervisor mode) attempts to execute code from a user page, the
MMU generates a page fault. This prevents \"ret2user\" attacks where an
attacker tricks the kernel into executing malicious code in user space.
Before SMEP, exploits could map executable shellcode in user memory and
redirect kernel execution to it. With SMEP, any such attempt immediately
faults.

**SMAP (Supervisor Mode Access Prevention):** When the kernel attempts
to read or write user memory (except through special copy functions like
`copy_from_user()`), the MMU generates a page fault. This prevents
kernel information leaks. Attackers can\'t trick a buggy kernel function
into reading kernel memory and writing it to a user-controlled pointer.

**Memory Protection Keys (MPK/PKU):** We saw in Chapter 6 how Intel\'s
Memory Protection Keys allow fine-grained protection domains within a
single process. When a thread attempts to access a page with a
protection key that\'s disabled in the thread\'s PKRU register, a page
fault occurs with a specific error code. The fault handler can then
enforce custom security policies.

Page faults are the mechanism that turns the protection bits we studied
in Chapter 6 into actual enforced security. Attackers target page fault
handlers because they\'re the last line of defense---if an attacker can
bypass or confuse the fault handler, they can potentially bypass the
entire security model.

### 4. Page Faults Are Debugging Windows

When your program crashes with \"Segmentation fault\" (Unix) or \"Access
violation\" (Windows), that\'s a page fault that the OS decided not to
handle. The page fault information---the faulting address, the type of
access (read/write/execute), the protection violation---is invaluable
for debugging:

**Null pointer dereference:** Faulting address near 0x0 (typical null
pointer) **Use-after-free:** Faulting address in freed heap memory
(often poisoned) **Stack overflow:** Faulting address just beyond
current stack region **Buffer overflow:** Faulting address beyond
allocated region **Uninitialized pointer:** Faulting address at random
location (often 0xdeadbeef or similar pattern in debug builds)

Understanding how to decode page fault information is essential for
systems debugging. When a kernel oops occurs (a page fault in kernel
mode), the error message includes:

- The faulting virtual address (where the bad access occurred)
- The error code (read vs write, user vs supervisor, present vs
  not-present)
- The instruction pointer (what code caused the fault)
- The page table state at each level (PGD, PUD, PMD, PTE values)

Learning to interpret this information can instantly pinpoint bugs that
would otherwise take hours to track down.

### What This Chapter Covers

This chapter focuses exclusively on **MMU, TLB, and paging-generated
exceptions**---the faults that occur during address translation and
memory access due to the memory management hardware. We will cover:

**Core Page Fault Mechanisms (7.2-7.5):** - Page fault fundamentals:
minor, major, invalid, and COW faults - x86-64 page fault exception
(#PF): error codes, CR2 register, and handling - ARM64 synchronous
exceptions: Data Aborts, Instruction Aborts, and ESR decoding - ARM RME
(Realm Management Extension): MECID violations and Granule Protection
faults - RISC-V page faults: software TLB management and exception codes

**TLB and Page Table Issues (7.6-7.7):** - TLB-related exceptions:
misses on software-managed TLBs, multi-hit exceptions, TLB conflicts -
Page table walk failures: invalid PTEs at each level, nested page table
faults

**Memory Aliasing and Protection (7.8-7.9):** - Page overlapping and
aliasing faults: PAT conflicts, cache aliasing, attribute mismatches -
Permission violations: R/W/X violations, SMEP/SMAP/PAN, protection keys

**Fault Handling and Performance (7.10-7.11):** - Page fault handler
implementation: demand paging, COW, stack growth - Performance
implications: fault costs, profiling, and optimization

**Architecture Diversity (7.12-7.13):** - Historical architectures:
SPARC, MIPS, PowerPC exception mechanisms - Modern architecture
comparison: x86-64 vs ARM64 vs RISC-V - Debugging techniques and common
patterns

**Advanced Topics (7.14):** - Asynchronous page faults in
virtualization - User-space page fault handling (userfaultfd) -
Fault-tolerant systems and error recovery

### What We Exclude

This chapter does **NOT** cover general CPU exceptions unrelated to
memory management:

❌ **Arithmetic exceptions:** divide-by-zero, integer overflow,
floating-point exceptions ❌ **Illegal instruction exceptions:** invalid
opcodes, privileged instruction in user mode ❌ **Debug and breakpoint
exceptions:** INT 3, hardware breakpoints (unless related to page
protection) ❌ **Interrupts:** timer interrupts, I/O interrupts (though
we briefly cover TLB shootdown IPIs) ❌ **Cache coherency:** this is a
CPU cache architecture topic, not an MMU topic (though we cover cache
aliasing as it relates to virtual memory)

If an exception doesn\'t involve the MMU, page tables, TLB, or memory
protection mechanisms, it\'s outside our scope.

By the end of this chapter, you\'ll understand not just what page faults
are, but how they enable the virtual memory features we\'ve studied, how
different architectures implement them, how to write efficient fault
handlers, and how to debug memory-related crashes. You\'ll see how page
faults connect all the concepts from previous chapters---page tables,
TLBs, IOMMUs, and protection---into a cohesive system where hardware and
software cooperate to provide secure, flexible, and performant virtual
memory.

------------------------------------------------------------------------

## 7.2 Page Fault Fundamentals

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="580" viewBox="0 0 900 580" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
<defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
<marker id="a" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
<marker id="ao" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
<marker id="ag" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker></defs>
<text x="450" y="26" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Figure 7.1 - Page Fault Handling: From CPU Exception to OS Resolution</text>
<rect x="340" y="40" width="220" height="46" rx="6" filter="url(#sh)" style="fill:#1565C0" />
<text x="450" y="58" style="fill:white; font-size:15; font-weight:bold; text-anchor:middle">CPU: Memory Access</text>
<text x="450" y="76" style="fill:white; font-size:13; text-anchor:middle">Load/Store with virtual address</text>
<line x1="450" y1="86" x2="450" y2="110" marker-end="url(#a)" style="stroke:#1565C0; stroke-width:2"></line>
<rect x="320" y="110" width="260" height="40" rx="6" filter="url(#sh)" style="fill:#00796B" />
<text x="450" y="125" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">TLB Lookup</text>
<text x="450" y="141" style="fill:white; font-size:12; text-anchor:middle">Check L1 dTLB, L2 STLB</text>
<line x1="340" y1="130" x2="240" y2="130" marker-end="url(#ag)" style="stroke:#00796B; stroke-width:1.5"></line>
<text x="220" y="126" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:end">HIT</text>
<text x="220" y="142" style="fill:#00796B; font-size:12; text-anchor:end">1-7 cycles</text>
<line x1="450" y1="150" x2="450" y2="174" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2"></line>
<text x="460" y="168" style="fill:#E65100; font-size:12">TLB miss</text>
<rect x="300" y="174" width="300" height="40" rx="6" filter="url(#sh)" style="fill:#E65100" />
<text x="450" y="189" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">HW Page Table Walker</text>
<text x="450" y="205" style="fill:white; font-size:12; text-anchor:middle">Read CR3/TTBR/satp, walk 4-5 levels</text>
<line x1="600" y1="194" x2="700" y2="194" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:1.5"></line>
<text x="702" y="190" style="fill:#00796B; font-size:13; font-weight:bold">PTE valid</text>
<text x="702" y="206" style="fill:#00796B; font-size:12">Fill TLB, retry</text>
<text x="702" y="222" style="fill:#00796B; font-size:12">100-300 ns</text>
<line x1="450" y1="214" x2="450" y2="238" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2"></line>
<text x="460" y="232" style="fill:#E65100; font-size:12">PTE not present / bad</text>
<rect x="270" y="238" width="360" height="46" rx="6" filter="url(#sh)" style="fill:#E65100" />
<text x="450" y="256" style="fill:white; font-size:15; font-weight:bold; text-anchor:middle">#PF / Data Abort Exception</text>
<text x="450" y="274" style="fill:white; font-size:13; text-anchor:middle">CPU saves state, jumps to OS fault handler</text>
<line x1="450" y1="284" x2="450" y2="308" marker-end="url(#a)" style="stroke:#212121; stroke-width:2"></line>
<rect x="240" y="308" width="160" height="110" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
<text x="320" y="326" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">Minor Fault</text>
<text x="320" y="344" style="fill:#212121; font-size:12; text-anchor:middle">Page in RAM but</text>
<text x="320" y="360" style="fill:#212121; font-size:12; text-anchor:middle">not yet mapped</text>
<text x="320" y="376" style="fill:#212121; font-size:12; text-anchor:middle">(demand paging,</text>
<text x="320" y="392" style="fill:#212121; font-size:12; text-anchor:middle">CoW, new anon)</text>
<text x="320" y="408" style="fill:#00796B; font-size:12; text-anchor:middle">~1-10 us</text>
<rect x="500" y="308" width="160" height="110" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
<text x="580" y="326" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">Major Fault</text>
<text x="580" y="344" style="fill:#212121; font-size:12; text-anchor:middle">Page on disk</text>
<text x="580" y="360" style="fill:#212121; font-size:12; text-anchor:middle">(swap or mmap)</text>
<text x="580" y="376" style="fill:#212121; font-size:12; text-anchor:middle">Block I/O read,</text>
<text x="580" y="392" style="fill:#212121; font-size:12; text-anchor:middle">process sleeps</text>
<text x="580" y="408" style="fill:#E65100; font-size:12; text-anchor:middle">~1-10 ms</text>
<line x1="320" y1="418" x2="420" y2="455" marker-end="url(#a)" style="stroke:#212121; stroke-width:1.5"></line>
<line x1="580" y1="418" x2="480" y2="455" marker-end="url(#a)" style="stroke:#212121; stroke-width:1.5"></line>
<rect x="310" y="455" width="280" height="46" rx="6" filter="url(#sh)" style="fill:#00796B" />
<text x="450" y="473" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">OS: Map Page, Update PTE</text>
<text x="450" y="491" style="fill:white; font-size:13; text-anchor:middle">Install PTE, flush TLB entry, return to user</text>
<rect x="30" y="520" width="840" height="46" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
<text x="450" y="538" style="fill:#212121; font-size:13; font-weight:bold; text-anchor:middle">Fault cost breakdown: x86-64 CR2=faulting VA | ARM64 FAR_EL1=faulting VA | RISC-V stval=faulting VA</text>
<text x="450" y="556" style="fill:#616161; font-size:12; text-anchor:middle">Protection fault (SIGSEGV): PTE present but U/S or R/W bits deny access. OS cannot fix: sends signal to process.</text>
</svg>
</div>
<figcaption><strong>Figure 7.1:</strong> Page fault handling path from
CPU exception to OS resolution. A TLB miss triggers the hardware page
table walker; if the PTE is absent or invalid the CPU raises a #PF
(x86-64), Data Abort (ARM64), or page-fault exception (RISC-V). The OS
handler classifies the fault as minor (page in RAM, ~1-10 µs) or major
(page on disk, ~1-10 ms) and installs the mapping before returning to
the faulting instruction.</figcaption>
</figure>

Before diving into architecture-specific details, let\'s establish a
common understanding of what page faults are, when they occur, and how
they\'re categorized.

### 7.2.1 What is a Page Fault?

A **page fault** is a synchronous exception generated by the Memory
Management Unit (MMU) when address translation cannot complete
successfully. \"Synchronous\" means the exception is directly caused by
the currently executing instruction---when the CPU attempts to fetch an
instruction, load data, or store data, and the MMU determines it cannot
provide a valid physical address for the requested virtual address.

This is fundamentally different from asynchronous interrupts (like timer
interrupts or I/O completion) which can occur at any time regardless of
what instruction is executing. A page fault is precise and
deterministic: the same instruction accessing the same virtual address
will always generate the same page fault (assuming page tables haven\'t
changed).

**Key Characteristics:**

1.  **Synchronous:** Caused by the currently executing instruction
2.  **Precise:** The faulting instruction is known, and all previous
    instructions have completed
3.  **Restartable:** After the OS handles the fault, the faulting
    instruction can be restarted
4.  **Transparent (usually):** User code doesn\'t see the fault---it
    just experiences a delay

The MMU generates a page fault when: - The page table entry has Present
bit = 0 - The access violates protection bits (write to read-only,
execute from NX page) - The access violates privilege requirements (user
accessing supervisor page) - Reserved bits in the PTE are set
incorrectly - On RISC-V: TLB miss with no valid page table entry

### 7.2.2 Page Fault Causes

Page faults occur for many reasons. Understanding the cause is essential
for the OS to handle the fault appropriately:

**1. Not Present (Present bit = 0):**

This is the most common cause. The page table entry exists and is
otherwise valid, but the Present bit is clear, indicating the page is
not currently in physical memory. This could mean:

- **Demand paging:** Page has never been accessed (OS hasn\'t allocated
  physical memory yet)
- **Swapped out:** Page was in memory but was swapped to disk due to
  memory pressure
- **Page reclaim:** OS reclaimed the physical page but kept the PTE
  structure

``` {.sourceCode .c}
// Example PTE with Present = 0
uint64_t pte = 0x0000000012345006;  // x86-64 PTE
// Bits:
//   [0]: P = 0 (Not present)
//   [1]: R/W = 1 (Writable - if it were present)
//   [2]: U/S = 1 (User accessible - if it were present)
//   [12-51]: 0x12345 (Could be swap location or other metadata)

// When CPU accesses this page → page fault
```

**2. Protection Violation:**

The page is present in memory, but the requested access violates the
protection bits. This generates an immediate fault:

- **Write to read-only page:** W bit = 0, attempting to store
- **Execute from non-executable page:** NX/XD/XN bit = 1, attempting to
  fetch instruction
- **User accessing supervisor page:** U/S bit = 0, access from user mode
  (ring 3, EL0)
- **Kernel executing user page (SMEP):** SMEP enabled, supervisor mode
  trying to execute user page
- **Kernel accessing user page (SMAP):** SMAP enabled, supervisor mode
  trying to read/write user page
- **Protection key violation (MPK):** Access to page whose protection
  key is disabled in PKRU

**3. Reserved Bits Set:**

In Chapter 3, we saw that page table entries have reserved bits that
must be zero. If any reserved bit is set to 1, the MMU generates a page
fault when walking the page table. This typically indicates:

- Corrupted page tables (hardware memory error)
- Software bug (OS wrote invalid PTE)
- Malicious attempt to exploit the MMU

On x86-64, bits 51-62 are reserved for software use in the page table
structure itself, but bits 7-8 in valid PTEs are reserved for certain
page sizes. On ARM64, various bits are reserved depending on the
configuration.

**4. Invalid Page Table Hierarchy:**

During a page table walk (Chapter 3, Section 3.6), if any level of the
page table has issues:

- Present bit = 0 at intermediate level (L4, L3, L2 on x86-64)
- Invalid physical address pointing outside installed RAM
- Circular reference (PTE points back to itself or a parent table)

**5. TLB Miss on Software-Managed TLB (RISC-V):**

On RISC-V, TLB misses generate page fault exceptions because there\'s no
hardware page table walker. The OS must walk the page tables in software
and explicitly load the TLB. We\'ll cover this in detail in Section 7.5.

### 7.2.3 Page Fault Types

Operating systems categorize page faults into several types based on how
they should be handled:

**Minor Page Faults:**

The page is already in physical memory, but the page table just needs to
be updated. These are relatively fast (1-5 microseconds) because no disk
I/O is required.

*Examples:* - **First access after fork():** COW page that hasn\'t been
written yet---shared physical page exists - **Page cache hit:**
File-backed page that\'s in the page cache but not mapped in this
process - **Stack growth:** Physical pages exist; just need to update
page tables - **Demand zero:** Need to allocate a zeroed page (common
for BSS segment and heap)

``` {.sourceCode .c}
// Minor fault handling pseudo-code
void handle_minor_fault(virt_addr_t fault_addr) {
    // Find or allocate physical page
    phys_addr_t page;
    
    if (is_file_backed(fault_addr)) {
        page = find_in_page_cache(fault_addr);  // Already in memory!
    } else {
        page = alloc_page();                     // Quick allocation
        zero_page(page);                         // Zero for security
    }
    
    // Update page table
    pte_t *pte = walk_page_table(fault_addr);
    *pte = make_pte(page, PROT_READ | PROT_WRITE);
    
    // Flush TLB for this address
    flush_tlb_one(fault_addr);
    
    // Done - took ~1-5 microseconds
}
```

**Major Page Faults:**

The page must be read from disk. These are extremely expensive (1-10
milliseconds) because of disk I/O latency.

*Examples:* - **Swapped page:** Page was evicted to swap space due to
memory pressure - **File-backed page not in cache:** mmap\'d file page
that must be read from disk - **Executable load:** First execution of
program code not yet in page cache

``` {.sourceCode .c}
// Major fault handling pseudo-code
void handle_major_fault(virt_addr_t fault_addr) {
    // Allocate physical page
    phys_addr_t page = alloc_page();
    
    // This is the expensive part: disk I/O
    if (is_swapped(fault_addr)) {
        // Read from swap device (SSD: ~100 µs, HDD: ~10 ms)
        swap_in(fault_addr, page);
    } else {
        // Read from file (depends on storage speed)
        read_file_data(fault_addr, page);
    }
    
    // Update page table
    pte_t *pte = walk_page_table(fault_addr);
    *pte = make_pte(page, get_protection(fault_addr));
    
    flush_tlb_one(fault_addr);
    
    // Done - took 1-10 milliseconds (1000× slower than minor fault!)
}
```

**Invalid Faults:**

The address is not mapped in the process\'s address space at all, or the
access violates permissions in a way that can\'t be fixed. These result
in process termination (SIGSEGV).

*Examples:* - **Null pointer dereference:** Address 0x0 (or near 0) -
**Random garbage pointer:** Address has never been mapped - **Buffer
overflow:** Accessing beyond allocated region - **Use-after-free:**
Accessing memory that\'s been freed - **Stack overflow:** SP far beyond
stack limit (not just a page or two) - **Security violation:**
Attempting to bypass protection (e.g., SMEP/SMAP violation)

``` {.sourceCode .c}
// Invalid fault handling pseudo-code
void handle_invalid_fault(virt_addr_t fault_addr, uint32_t error_code) {
    // Check if address is in any valid VMA (Virtual Memory Area)
    struct vm_area *vma = find_vma(fault_addr);
    
    if (!vma) {
        // Not mapped - definitely invalid
        goto terminate;
    }
    
    // Check if access type is allowed
    if ((error_code & WRITE) && !(vma->prot & PROT_WRITE)) {
        // Write to non-writable VMA - invalid
        goto terminate;
    }
    
    if ((error_code & EXEC) && !(vma->prot & PROT_EXEC)) {
        // Execute from non-executable VMA - invalid
        goto terminate;
    }
    
    // Security violations
    if (error_code & SMEP_VIOLATION) {
        // Kernel executed user page - security violation
        printk("SMEP violation at %p\n", fault_addr);
        goto terminate;
    }
    
terminate:
    // Send SIGSEGV to the process
    send_sig(SIGSEGV, current, 1);
}
```

**Copy-on-Write (COW) Faults:**

A special case of minor fault. The page is present and shared with
another process (after fork()), but marked read-only. A write attempt
generates a fault, and the handler makes a private copy.

``` {.sourceCode .c}
// COW fault handling pseudo-code
void handle_cow_fault(virt_addr_t fault_addr) {
    pte_t *pte = walk_page_table(fault_addr);
    phys_addr_t old_page = pte_to_phys(*pte);
    
    // Check reference count
    if (page_count(old_page) == 1) {
        // We're the only one using it - just make it writable
        *pte |= PTE_W;
        flush_tlb_one(fault_addr);
        return;  // Fast path - no copy needed!
    }
    
    // Others are using it - make a copy
    phys_addr_t new_page = alloc_page();
    copy_page(old_page, new_page);
    
    // Update PTE to point to new page (now writable)
    *pte = make_pte(new_page, PTE_P | PTE_W | PTE_U);
    flush_tlb_one(fault_addr);
    
    // Decrement reference count on old page
    page_put(old_page);
}
```

### 7.2.4 Hardware vs Software Components

Page fault handling is split between hardware and software:

**Hardware (MMU/CPU) Responsibilities:** 1. Detect the fault condition
during address translation 2. Stop the faulting instruction (before it
completes - important for restartability) 3. Save error information
(fault address, error code) 4. Switch to kernel/supervisor mode 5.
Vector to the page fault handler (via IDT on x86, exception vector on
ARM/RISC-V) 6. Provide registers/state for software to diagnose the
fault

**Software (OS) Responsibilities:** 1. Determine the type of fault (read
error code, examine page tables) 2. Decide how to handle it (allocate
page, swap in, COW, or terminate) 3. Perform the handling (disk I/O,
memory allocation, page table updates) 4. Return control to hardware to
restart the instruction

This division of labor makes sense: hardware is fast at detecting faults
and saving state, but software has the flexibility to implement complex
policies.

### 7.2.5 Page Fault in the Context of Address Translation

Let\'s revisit the address translation flow from Chapter 3, now with
fault handling:

    Virtual Address
          |
          v
        [TLB Lookup]
          |
          +-- Hit? --> Physical Address --> Memory Access --> Done
          |
          +-- Miss? --> [Page Table Walk]
                             |
                             v
                        [Check PTE at each level]
                             |
                             +-- Present=1, Valid? --> Cache in TLB --> Retry
                             |
                             +-- Present=0? --> PAGE FAULT (not present)
                             |
                             +-- Protection violation? --> PAGE FAULT (permission)
                             |
                             +-- Reserved bits set? --> PAGE FAULT (invalid PTE)
                             
                        [Page Fault Handler (Software)]
                             |
                             v
                        Determine fault type:
                             |
                             +-- Minor --> Allocate/map page --> Update PTE --> Flush TLB
                             |
                             +-- Major --> Swap in from disk --> Update PTE --> Flush TLB
                             |
                             +-- COW --> Copy page --> Update PTE --> Flush TLB
                             |
                             +-- Invalid --> Terminate process (SIGSEGV)
                             
                        Return to hardware
                             |
                             v
                        Retry instruction --> Success!

The key insight: page faults are not errors in the traditional sense.
They\'re a communication mechanism between hardware (which detects
anomalies during translation) and software (which has the policy to
handle them).

------------------------------------------------------------------------

## 7.3 x86-64 Page Faults (#PF)

The x86-64 architecture has one of the most sophisticated page fault
mechanisms, refined over decades from the original 80386. Understanding
x86-64 page faults in detail provides a reference point for comparing
other architectures.

### 7.3.1 Page Fault Exception (#PF, Vector 14)

On x86-64, page faults are exception 14 in the Interrupt Descriptor
Table (IDT). When a page fault occurs:

1.  **CPU stops the faulting instruction** (before it
    completes---critical for restartability)
2.  **CPU pushes error code onto the kernel stack** (32-bit value with
    detailed fault information)
3.  **CPU saves faulting address to CR2 register** (64-bit virtual
    address that caused the fault)
4.  **CPU switches to ring 0 (kernel mode)** if not already there
5.  **CPU loads CS:RIP from IDT entry 14** (jumps to page fault handler)
6.  **CPU pushes additional context** (RIP, CS, RFLAGS, RSP, SS)

The page fault handler can then examine the error code and CR2 to
determine what happened and how to handle it.

### 7.3.2 Page Fault Error Code

The error code is a 32-bit value pushed onto the stack, with each bit
providing specific information about the fault. This is one of x86-64\'s
strengths---rich error information that lets software diagnose faults
precisely.

**Error Code Format:**

    Bit 31-16: Reserved (0)
    Bit 15:    SGX - SGX enclave violation (1 = SGX-related fault)
    Bit 14-6:  Reserved (0)
    Bit 5:     PK - Protection key violation (1 = PKRU violation)
    Bit 4:     I/D - Instruction/Data (1 = instruction fetch, 0 = data access)
    Bit 3:     RSVD - Reserved bit violation (1 = reserved bit set in PTE)
    Bit 2:     U/S - User/Supervisor (1 = user mode, 0 = supervisor mode)
    Bit 1:     W/R - Write/Read (1 = write, 0 = read)
    Bit 0:     P - Present (1 = protection violation, 0 = not present)

Let\'s examine each bit in detail:

**Bit 0 (P - Present):** - **0:** Page not present (Present bit = 0 in
PTE) - This is demand paging, swap in, or invalid address - Handler must
check if address is valid and handle accordingly - **1:** Page is
present but access violated protection - Write to read-only page -
Execute from NX page\
- User accessing supervisor page - SMEP or SMAP violation

``` {.sourceCode .c}
// Checking Present bit
void check_present_bit(uint32_t error_code) {
    if (!(error_code & 0x1)) {
        // P = 0: Not present
        printk("Page not present - demand paging or invalid\n");
    } else {
        // P = 1: Protection violation
        printk("Page present but access violated protection\n");
    }
}
```

**Bit 1 (W/R - Write/Read):** - **0:** Read or execute access (load
instruction or instruction fetch) - **1:** Write access (store
instruction)

This is crucial for Copy-on-Write: if P=1 (present) and W/R=1 (write),
the handler checks if this is a COW page.

``` {.sourceCode .c}
// Determining access type
void check_access_type(uint32_t error_code) {
    if (error_code & 0x2) {
        printk("Write access (store instruction)\n");
        // Check for COW
    } else {
        printk("Read or execute access\n");
    }
}
```

**Bit 2 (U/S - User/Supervisor):** - **0:** Fault occurred in supervisor
mode (kernel, ring 0) - **1:** Fault occurred in user mode (application,
ring 3)

This helps determine if the fault is in kernel code or user code, which
affects how it\'s handled.

``` {.sourceCode .c}
// Checking privilege level
void check_privilege(uint32_t error_code) {
    if (error_code & 0x4) {
        printk("User mode fault (ring 3)\n");
        // More common - application bug
    } else {
        printk("Supervisor mode fault (ring 0)\n");
        // Kernel bug - more serious!
    }
}
```

**Bit 3 (RSVD - Reserved):** - **1:** A reserved bit in a PTE was set to
1 - This usually indicates corruption or a software bug

``` {.sourceCode .c}
// Checking for reserved bit violation
void check_reserved(uint32_t error_code) {
    if (error_code & 0x8) {
        printk("Reserved bit violation - PTE corruption!\n");
        // Likely a serious bug or hardware error
        panic("Corrupted page table");
    }
}
```

**Bit 4 (I/D - Instruction/Data):** - **0:** Data access (load or
store) - **1:** Instruction fetch

Combined with NX bit checking, this helps identify execute-from-data
attempts:

``` {.sourceCode .c}
// Checking if instruction fetch
void check_instruction_fetch(uint32_t error_code, uint64_t cr2) {
    if (error_code & 0x10) {
        printk("Instruction fetch at 0x%lx\n", cr2);
        
        // If also P=1, this might be NX violation
        if (error_code & 0x1) {
            printk("Attempted to execute non-executable page!\n");
            // Security violation - likely exploit attempt
        }
    }
}
```

**Bit 5 (PK - Protection Key):** - **1:** Memory Protection Keys (MPK)
violation - Page\'s protection key is disabled in PKRU register (Chapter
6, Section 6.7)

``` {.sourceCode .c}
// Checking MPK violation
void check_mpk(uint32_t error_code) {
    if (error_code & 0x20) {
        printk("MPK violation\n");
        
        // Read PKRU to see which key was violated
        uint32_t pkru = rdpkru();
        // Handler can then enforce domain-specific policy
    }
}
```

**Bit 15 (SGX - Software Guard Extensions):** - **1:** SGX
enclave-related violation - Attempting to access enclave memory from
outside enclave - See Intel SGX documentation for details

### 7.3.3 CR2 Register: The Faulting Address

The CR2 (Control Register 2) is a 64-bit register that holds the virtual
address that caused the page fault. This is separate from the error code
and provides critical information for the handler.

**Reading CR2:**

``` {.sourceCode .asm}
; x86-64 assembly to read CR2
mov rax, cr2        ; Load CR2 into RAX
; RAX now contains the faulting virtual address
```

``` {.sourceCode .c}
// In C (using inline assembly or compiler intrinsic)
static inline uint64_t read_cr2(void) {
    uint64_t value;
    asm volatile("mov %%cr2, %0" : "=r" (value));
    return value;
}

// In page fault handler
void page_fault_handler(void) {
    uint64_t fault_addr = read_cr2();
    printk("Page fault at address: 0x%016lx\n", fault_addr);
}
```

**Important Properties of CR2:**

1.  **Holds the faulting virtual address, not physical**
2.  **Valid for the duration of the page fault handler**
3.  **Can be overwritten by nested page faults** (if handler itself
    causes a fault)
4.  **Contains the precise address, not page-aligned**
    - If instruction accesses 0x1234567890, CR2 = 0x1234567890 (not
      0x1234567000)
    - Handler must page-align it: `fault_addr & ~0xFFF`

**Example: Null Pointer Dereference:**

``` {.sourceCode .c}
int *ptr = NULL;
*ptr = 42;  // Causes page fault

// In handler:
// CR2 = 0x0000000000000000
// Error code = 0x6 (binary: 0110)
//   - P = 0 (not present)
//   - W/R = 1 (write)
//   - U/S = 1 (user mode)
// Handler recognizes: NULL pointer dereference in user mode
// Action: Send SIGSEGV to process
```

### 7.3.4 Page Fault Handler Flow

Here\'s a complete x86-64 page fault handler implementation (simplified
from Linux kernel):

``` {.sourceCode .c}
// Linux-style page fault handler for x86-64
void do_page_fault(struct pt_regs *regs, unsigned long error_code) {
    unsigned long fault_addr = read_cr2();
    struct task_struct *task = current;
    struct mm_struct *mm = task->mm;
    struct vm_area_struct *vma;
    unsigned int flags = FAULT_FLAG_DEFAULT;
    
    // Determine fault flags based on error code
    if (error_code & 0x2) flags |= FAULT_FLAG_WRITE;
    if (error_code & 0x4) flags |= FAULT_FLAG_USER;
    if (error_code & 0x10) flags |= FAULT_FLAG_INSTRUCTION;
    
    // Step 1: Check if fault occurred in kernel mode
    if (!(error_code & 0x4)) {
        // Supervisor mode fault
        // This is either:
        // a) Legitimate kernel access to user memory (copy_from_user)
        // b) Kernel bug
        // c) SMEP/SMAP violation
        
        if (error_code & 0x1) {
            // P = 1: Protection violation in kernel mode
            if (error_code & 0x10) {
                // Instruction fetch from user page - SMEP violation
                printk("SMEP violation at 0x%lx, IP=0x%lx\n",
                       fault_addr, regs->ip);
                goto bad_area_nosemaphore;
            }
            // Might be SMAP violation - check if legitimate
        }
        
        // Try to handle kernel faults
        if (handle_kernel_fault(fault_addr, error_code, regs))
            return;
        
        // Couldn't handle - kernel bug
        goto bad_area_nosemaphore;
    }
    
    // Step 2: User mode fault - acquire mm semaphore
    down_read(&mm->mmap_sem);
    
    // Step 3: Find VMA (Virtual Memory Area) for faulting address
    vma = find_vma(mm, fault_addr);
    if (!vma)
        goto bad_area;
    
    if (vma->vm_start <= fault_addr)
        goto good_area;
    
    // Step 4: Check if this is stack growth
    if (!(vma->vm_flags & VM_GROWSDOWN))
        goto bad_area;
    
    if (expand_stack(vma, fault_addr))
        goto bad_area;
    
good_area:
    // Step 5: Check access permissions
    if (error_code & 0x2) {
        // Write fault
        if (!(vma->vm_flags & VM_WRITE))
            goto bad_area;
    } else {
        if (!(vma->vm_flags & (VM_READ | VM_EXEC)))
            goto bad_area;
    }
    
    // Step 6: Handle the fault
    int ret = handle_mm_fault(vma, fault_addr, flags);
    
    if (ret & VM_FAULT_ERROR) {
        if (ret & VM_FAULT_OOM)
            goto out_of_memory;
        if (ret & VM_FAULT_SIGSEGV)
            goto bad_area;
        BUG();
    }
    
    // Success - release semaphore and return
    up_read(&mm->mmap_sem);
    return;
    
bad_area:
    up_read(&mm->mmap_sem);
    
bad_area_nosemaphore:
    // Step 7: Invalid fault - send SIGSEGV
    if (error_code & 0x4) {
        // User mode - send signal
        force_sig_fault(SIGSEGV, SEGV_MAPERR, (void __user *)fault_addr);
    } else {
        // Kernel mode - this is bad
        printk("Unable to handle kernel paging request at %lx\n", fault_addr);
        printk("IP: %lx\n", regs->ip);
        show_registers(regs);
        oops_end();
    }
    return;
    
out_of_memory:
    up_read(&mm->mmap_sem);
    if (error_code & 0x4)
        pagefault_out_of_memory();
    return;
}
```

### 7.3.5 Common x86-64 Page Fault Scenarios

Let\'s walk through specific scenarios to see how error codes and CR2
reveal what happened:

**Scenario 1: Demand Paging (First Access to Page)**

``` {.sourceCode .c}
// Allocate but don't touch memory
char *buffer = mmap(NULL, 4096, PROT_READ|PROT_WRITE,
                    MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);

// First access causes page fault
buffer[0] = 'A';

// Page fault details:
// CR2 = buffer address (e.g., 0x7f1234567000)
// Error code = 0x6 (binary: 0000 0110)
//   P = 0 (not present - demand paging)
//   W/R = 1 (write)
//   U/S = 1 (user mode)
//   I/D = 0 (data access)
//   All others = 0
//
// Handler action:
//   1. Allocate physical page
//   2. Zero the page (security)
//   3. Update PTE: Present=1, Write=1, User=1
//   4. Flush TLB
//   5. Return to retry instruction
```

**Scenario 2: Copy-on-Write After fork()**

``` {.sourceCode .c}
int main() {
    int *shared = mmap(NULL, 4096, PROT_READ|PROT_WRITE,
                       MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    *shared = 42;  // Write some data
    
    pid_t pid = fork();
    // Now both parent and child have shared marked read-only
    
    if (pid == 0) {
        // Child process
        *shared = 99;  // Causes COW page fault
    }
}

// Page fault details:
// CR2 = address of shared (e.g., 0x7f1234567000)
// Error code = 0x7 (binary: 0000 0111)
//   P = 1 (PRESENT - protection violation!)
//   W/R = 1 (write)
//   U/S = 1 (user mode)
//   I/D = 0 (data access)
//
// Handler recognizes COW scenario:
//   1. Check if PTE has COW flag
//   2. Allocate new physical page
//   3. Copy old page to new page
//   4. Update child's PTE to new page (writable)
//   5. Dec refcount on old page
//   6. Flush TLB
//   7. Return to retry instruction
```

**Scenario 3: Stack Overflow**

``` {.sourceCode .c}
void recursive_function(int depth) {
    char huge_array[1024*1024];  // 1MB on stack
    recursive_function(depth + 1);  // Recurse
}

int main() {
    recursive_function(0);  // Eventually hits stack limit
}

// Page fault details:
// CR2 = address beyond stack limit (e.g., 0x7fffffff0000)
// Error code = 0x6 (binary: 0000 0110)
//   P = 0 (not present)
//   W/R = 1 (write - pushing stack frame)
//   U/S = 1 (user mode)
//
// Handler checks if this is legitimate stack growth:
//   1. Find stack VMA
//   2. Check if fault_addr is within RLIMIT_STACK
//   3. Check if fault_addr is within reasonable distance of RSP
//   4. If yes: expand stack VMA, handle as demand paging
//   5. If no: send SIGSEGV (stack overflow)
```

**Scenario 4: Execute from Heap (NX Violation)**

``` {.sourceCode .c}
// Attempt to execute shellcode on heap
void *shellcode = malloc(1024);
memcpy(shellcode, exploit_code, 1024);
((void(*)())shellcode)();  // Try to execute

// Page fault details:
// CR2 = address of shellcode (e.g., 0x55a123456000)
// Error code = 0x15 (binary: 0001 0101)
//   P = 1 (present - protection violation!)
//   W/R = 0 (not a write)
//   U/S = 1 (user mode)
//   I/D = 1 (INSTRUCTION FETCH)
//
// PTE has NX bit set (bit 63 = 1)
// Handler recognizes: execute from non-executable page
//   Action: Send SIGSEGV (likely exploit attempt)
```

**Scenario 5: SMEP Violation (Kernel Executing User Page)**

``` {.sourceCode .c}
// Kernel vulnerability: dereferenced user-controlled function pointer
void kernel_function(void (*user_func)(void)) {
    user_func();  // If user_func points to user space, this faults
}

// Page fault details:
// CR2 = address in user space (e.g., 0x00007f1234567000)
// Error code = 0x11 (binary: 0001 0001)
//   P = 1 (present - protection violation!)
//   W/R = 0 (not a write)
//   U/S = 0 (SUPERVISOR MODE)
//   I/D = 1 (instruction fetch)
//
// CPU has CR4.SMEP = 1
// Handler recognizes: kernel tried to execute user page
//   This is SMEP violation - security issue!
//   Action: Kernel panic or log security event
```

**Scenario 6: SMAP Violation (Kernel Accessing User Data)**

``` {.sourceCode .c}
// Kernel bug: direct access to user memory without copy_from_user
int kernel_function(char *user_ptr) {
    char c = *user_ptr;  // SMAP violation if SMAP enabled
    return c;
}

// Page fault details:
// CR2 = user_ptr (e.g., 0x00007f1234567000)
// Error code = 0x3 (binary: 0000 0011)
//   P = 1 (present - protection violation!)
//   W/R = 0 (read)
//   U/S = 0 (SUPERVISOR MODE)
//   I/D = 0 (data access)
//
// CPU has CR4.SMAP = 1, EFLAGS.AC = 0
// Handler recognizes: kernel tried to access user page
//   This is SMAP violation - security issue!
//   Action: Kernel panic or log security event
```

### 7.3.6 x86-64 Error Code Summary Table

| Scenario | P | W/R | U/S | RSVD | I/D | PK | SGX | Hex | Handler Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Demand | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0x4 | Allocate page |
| paging |  |  |  |  |  |  |  |  |  |
| (read)** |  |  |  |  |  |  |  |  |  |
| **Demand | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0x6 | Allocate page |
| paging |  |  |  |  |  |  |  |  |  |
| (write)** |  |  |  |  |  |  |  |  |  |
| **COW fault** | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0x7 | Copy page |
| **Write to RO | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0x7 | SIGSEGV (if not |
| page** |  |  |  |  |  |  |  |  | COW) |
| **Execute | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0x15 | SIGSEGV |
| from NX |  |  |  |  |  |  |  |  |  |
| page** |  |  |  |  |  |  |  |  |  |
| **Null | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0x4 | SIGSEGV |
| pointer |  |  |  |  |  |  |  |  |  |
| (read)** |  |  |  |  |  |  |  |  |  |
| **Null | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0x6 | SIGSEGV |
| pointer |  |  |  |  |  |  |  |  |  |
| (write)** |  |  |  |  |  |  |  |  |  |
| **SMEP | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0x11 | Kernel panic |
| violation** |  |  |  |  |  |  |  |  |  |
| **SMAP | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0x3 | Kernel panic |
| violation** |  |  |  |  |  |  |  |  |  |
| **MPK | 1 | ? | 1 | 0 | 0 | 1 | 0 | 0x2? | App-specific |
| violation** |  |  |  |  |  |  |  |  |  |
| **Stack | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0x6 | Expand stack |
| growth** |  |  |  |  |  |  |  |  |  |


------------------------------------------------------------------------

## 7.4 ARM64 Data and Instruction Aborts

ARM64 uses a different exception model than x86-64. Instead of a single
\"page fault\" exception, ARM64 has separate exception types for
different scenarios, all classified as **synchronous exceptions**.
Understanding ARM64\'s approach provides insight into how RISC
architectures handle memory exceptions differently from CISC
architectures like x86.

### 7.4.1 ARM64 Synchronous Exception Model

ARM64 has four exception levels (ELs), similar to x86-64\'s privilege
rings but with different semantics:

- **EL0:** User mode (unprivileged)
- **EL1:** Kernel mode (OS)
- **EL2:** Hypervisor mode
- **EL3:** Secure Monitor mode

When a memory exception occurs, the CPU:

1.  **Determines exception type** (Data Abort, Instruction Abort, etc.)
2.  **Saves state** to exception-specific registers
3.  **Switches to higher exception level** (EL0 → EL1, or EL1 → EL2 if
    Stage 2 fault)
4.  **Vectors to exception handler** based on exception vector table
    (VBAR_ELn)

**Key Registers for Exception Handling:**

    ESR_ELn (Exception Syndrome Register):
      - Contains exception class (EC) and detailed syndrome
      - ESR_EL1 for EL0→EL1 exceptions
      - ESR_EL2 for EL1→EL2 exceptions

    FAR_ELn (Fault Address Register):
      - Contains faulting virtual address
      - FAR_EL1 for EL0→EL1 exceptions
      - FAR_EL2 for EL1→EL2 exceptions

    ELR_ELn (Exception Link Register):
      - Contains return address (faulting instruction)
      
    SPSR_ELn (Saved Program Status Register):
      - Contains saved processor state

### 7.4.2 Data Abort vs Instruction Abort

ARM64 distinguishes between data access faults and instruction fetch
faults:

**Data Abort:** - Caused by load/store instructions (LDR, STR, etc.) -
Exception Class (EC) = 0x24 (Data Abort from lower EL) or 0x25 (Data
Abort from same EL) - ESR_EL1.ISS contains Data Fault Status Code
(DFSC) - FAR_EL1 contains the faulting virtual address

**Instruction Abort:** - Caused by instruction fetch - Exception Class
(EC) = 0x20 (Instruction Abort from lower EL) or 0x21 (Instruction Abort
from same EL) - ESR_EL1.ISS contains Instruction Fault Status Code
(IFSC) - FAR_EL1 contains the faulting virtual address

### 7.4.3 Exception Syndrome Register (ESR_EL1)

The ESR is ARM64\'s equivalent to x86-64\'s error code, but it\'s much
more detailed---32 bits of structured information:

**ESR_EL1 Format:**

    Bits 31-26: EC (Exception Class)
      0x20 = Instruction Abort from lower EL
      0x21 = Instruction Abort from same EL
      0x24 = Data Abort from lower EL
      0x25 = Data Abort from same EL
      
    Bit 25: IL (Instruction Length)
      0 = 16-bit instruction
      1 = 32-bit instruction
      
    Bits 24-0: ISS (Instruction Specific Syndrome)
      Format depends on Exception Class

**For Data/Instruction Aborts, ISS contains:**

    Bits 24-10: Reserved or implementation-specific

    Bit 9: S1PTW (Stage 1 Page Table Walk)
      0 = Fault not during Stage 1 translation table walk
      1 = Fault during Stage 1 translation table walk

    Bit 8: Reserved

    Bit 7: CM (Cache Maintenance)
      0 = Not a cache maintenance instruction
      1 = Fault on cache maintenance operation

    Bit 6: WnR (Write not Read)
      0 = Read access
      1 = Write access
      
    Bits 5-0: DFSC/IFSC (Data/Instruction Fault Status Code)
      Indicates the type of fault

### 7.4.4 Fault Status Codes (DFSC/IFSC)

The DFSC (Data Fault Status Code) or IFSC (Instruction Fault Status
Code) indicates exactly what type of fault occurred. ARM64 has many more
fault types than x86-64:

**Translation Faults (Address not mapped):**

    0b000100 (0x04): Translation fault, level 0
    0b000101 (0x05): Translation fault, level 1
    0b000110 (0x06): Translation fault, level 2
    0b000111 (0x07): Translation fault, level 3

These correspond to faults at different levels of the page table
hierarchy (similar to x86-64\'s 4-level page tables). The level tells
you where in the page table walk the fault occurred.

**Access Flag Faults:**

    0b001000 (0x08): Access flag fault, level 0
    0b001001 (0x09): Access flag fault, level 1
    0b001010 (0x0A): Access flag fault, level 2
    0b001011 (0x0B): Access flag fault, level 3

The Access flag is set by hardware on first access (if TCR_EL1.HA is
set) or causes a fault for software to set. Used for page aging and LRU
algorithms.

**Permission Faults:**

    0b001100 (0x0C): Permission fault, level 0
    0b001101 (0x0D): Permission fault, level 1
    0b001110 (0x0E): Permission fault, level 2
    0b001111 (0x0F): Permission fault, level 3

These occur when: - Write to read-only page (AP bits = 0b11) - Execute
from non-executable page (UXN/PXN bits set) - EL0 access to EL1 page -
EL1 access with PAN enabled

**Address Size Fault:**

    0b000000 (0x00): Address size fault, level 0
    0b000001 (0x01): Address size fault, level 1
    0b000010 (0x02): Address size fault, level 2
    0b000011 (0x03): Address size fault, level 3

Occurs when virtual address is larger than configured address space
(e.g., using 52-bit address when only 48-bit is configured).

**TLB Conflict Abort:**

    0b110000 (0x30): TLB conflict abort

Multiple TLB entries match the same address---hardware detected a TLB
corruption. Must flush TLB to resolve.

**Synchronous External Abort:**

    0b010000 (0x10): Synchronous external abort, level 0
    0b010001 (0x11): Synchronous external abort, level 1
    0b010010 (0x12): Synchronous external abort, level 2
    0b010011 (0x13): Synchronous external abort, level 3

External memory error (similar to x86 Machine Check Exception), usually
indicates hardware failure.

### 7.4.5 Reading Exception Information

Here\'s how to read ESR_EL1 and FAR_EL1 in an ARM64 exception handler:

``` {.sourceCode .c}
// ARM64 exception handler (Linux kernel style)
static void do_data_abort(unsigned long addr, unsigned int esr,
                          struct pt_regs *regs)
{
    unsigned long ec = ESR_ELx_EC(esr);      // Exception Class
    unsigned long fsc = ESR_ELx_FSC(esr);    // Fault Status Code
    unsigned long wnr = ESR_ELx_WNR(esr);    // Write not Read
    unsigned long s1ptw = ESR_ELx_S1PTW(esr); // Stage 1 PTW
    
    // addr is from FAR_EL1 (already read by low-level handler)
    
    // Check exception class
    if (ec != ESR_ELx_EC_DABT_LOW && ec != ESR_ELx_EC_DABT_CUR) {
        // Not a Data Abort - shouldn't happen
        die("Unexpected exception class in data abort handler", regs, esr);
    }
    
    // Determine fault type based on FSC
    switch (fsc) {
    case 0x04 ... 0x07:
        // Translation fault at level 0-3
        handle_translation_fault(addr, esr, regs);
        break;
        
    case 0x08 ... 0x0B:
        // Access flag fault
        handle_access_flag_fault(addr, esr, regs);
        break;
        
    case 0x0C ... 0x0F:
        // Permission fault
        handle_permission_fault(addr, esr, regs);
        break;
        
    case 0x30:
        // TLB conflict - flush TLB
        flush_tlb_all();
        return;
        
    case 0x10 ... 0x13:
        // Synchronous external abort - hardware error
        handle_external_abort(addr, esr, regs);
        break;
        
    default:
        // Unknown fault
        die("Unknown fault status code", regs, esr);
    }
}

/* Based on Linux kernel arch/arm64/mm/fault.c 
   Reference: Linux kernel v6.5, do_mem_abort() */
```

**Helper macros for ESR decoding:**

``` {.sourceCode .c}
// Extract fields from ESR_ELx
#define ESR_ELx_EC_SHIFT    (26)
#define ESR_ELx_EC_MASK     (0x3F << ESR_ELx_EC_SHIFT)
#define ESR_ELx_EC(esr)     (((esr) & ESR_ELx_EC_MASK) >> ESR_ELx_EC_SHIFT)

#define ESR_ELx_FSC_MASK    (0x3F)
#define ESR_ELx_FSC(esr)    ((esr) & ESR_ELx_FSC_MASK)

#define ESR_ELx_WNR_SHIFT   (6)
#define ESR_ELx_WNR(esr)    (((esr) >> ESR_ELx_WNR_SHIFT) & 1)

#define ESR_ELx_S1PTW_SHIFT (9)
#define ESR_ELx_S1PTW(esr)  (((esr) >> ESR_ELx_S1PTW_SHIFT) & 1)

// Exception Classes
#define ESR_ELx_EC_DABT_LOW (0x24)  // Data Abort from lower EL
#define ESR_ELx_EC_DABT_CUR (0x25)  // Data Abort from current EL
#define ESR_ELx_EC_IABT_LOW (0x20)  // Instruction Abort from lower EL
#define ESR_ELx_EC_IABT_CUR (0x21)  // Instruction Abort from current EL
```

### 7.4.6 ARM64 Exception Scenarios

Let\'s walk through specific scenarios to see how ESR and FAR reveal the
fault:

**Scenario 1: Translation Fault (Demand Paging)**

``` {.sourceCode .c}
// First access to mmap'd memory
char *buffer = mmap(NULL, 4096, PROT_READ|PROT_WRITE,
                    MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
buffer[0] = 'A';  // Causes translation fault

// Exception details:
// FAR_EL1 = buffer address (e.g., 0x0000ffff89ab0000)
// ESR_EL1 = 0x96000007
//   EC = 0x25 (0b100101) = Data Abort from current EL
//   IL = 1 (32-bit instruction)
//   WnR = 1 (Write)
//   FSC = 0x07 (Translation fault, level 3)
//
// Handler action:
//   1. Allocate physical page
//   2. Zero page
//   3. Update level 3 PTE
//   4. Return (ERET instruction)
```

**Scenario 2: Permission Fault (Write to Read-Only)**

``` {.sourceCode .c}
// Map memory as read-only
char *ro = mmap(NULL, 4096, PROT_READ,
                MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
*ro = 'X';  // Attempt to write

// Exception details:
// FAR_EL1 = ro address
// ESR_EL1 = 0x9600000F
//   EC = 0x25 (Data Abort from current EL)
//   WnR = 1 (Write)
//   FSC = 0x0F (Permission fault, level 3)
//
// Handler recognizes: Write to read-only page
//   Check if COW page - if not, send SIGSEGV
```

**Scenario 3: Instruction Abort (Execute from NX Page)**

``` {.sourceCode .c}
// Attempt to execute heap memory
void *code = malloc(1024);
memcpy(code, shellcode, 1024);
((void(*)())code)();  // Try to execute

// Exception details:
// FAR_EL1 = code address
// ESR_EL1 = 0x8600000F
//   EC = 0x21 (Instruction Abort from current EL)
//   FSC = 0x0F (Permission fault, level 3)
//
// Handler recognizes: Instruction fetch from UXN page
//   Send SIGSEGV (exploit attempt)
```

**Scenario 4: Access Flag Fault**

``` {.sourceCode .c}
// System with hardware Access flag management disabled
// First read of a page

char *data = mmap(NULL, 4096, PROT_READ|PROT_WRITE,
                  MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
strcpy(data, "hello");  // Write causes access flag fault

// Exception details:
// FAR_EL1 = data address
// ESR_EL1 = 0x9600000B
//   EC = 0x25 (Data Abort)
//   WnR = 1 (Write)
//   FSC = 0x0B (Access flag fault, level 3)
//
// Handler action:
//   1. Set Access flag (AF bit) in PTE
//   2. Record page access for LRU/aging
//   3. Return
```

### 7.4.7 PAN (Privileged Access Never)

ARM64\'s PAN is equivalent to x86-64\'s SMAP---prevents the kernel from
accidentally accessing user memory.

**How PAN Works:**

When PSTATE.PAN = 1 (set by kernel), any access to a page with EL0
permissions generates a permission fault, even if the kernel is at EL1.

``` {.sourceCode .c}
// ARM64 PAN violation example
void kernel_function(char *user_ptr) {
    // If PAN is enabled, this causes permission fault
    char c = *user_ptr;
}

// Exception details:
// FAR_EL1 = user_ptr
// ESR_EL1 = 0x9200000F
//   EC = 0x24 (Data Abort from lower EL)
//   WnR = 0 (Read)
//   FSC = 0x0F (Permission fault)
//
// Handler recognizes: Kernel accessing user page with PAN set
//   This is a kernel bug - may panic or log
```

**Safe user memory access:**

``` {.sourceCode .c}
// Temporarily disable PAN for legitimate access
unsigned long copy_from_user(void *to, const void __user *from,
                              unsigned long n)
{
    unsigned long res = n;
    
    // Clear PAN bit
    asm volatile("msr pan, #0" ::: "memory");
    
    // Now safe to access user memory
    while (n--) {
        *((char *)to)++ = *((char *)from)++;
    }
    
    // Re-enable PAN
    asm volatile("msr pan, #1" ::: "memory");
    
    return res;
}

/* Simplified from Linux kernel arch/arm64/lib/copy_from_user.S */
```

### 7.4.8 ARM Realm Management Extension (RME) Faults

ARM\'s Confidential Compute Architecture (CCA) introduced the Realm
Management Extension (RME) in Armv9-A. RME provides hardware-enforced
isolation for confidential workloads, similar to Intel TDX and AMD
SEV-SNP but with ARM\'s approach.

**RME Security States:**

RME extends ARM\'s traditional Secure/Non-secure worlds with two new
states: - **Root:** Highest privilege (Realm Management Monitor) -
**Realm:** Confidential VMs (protected from Normal world and
Hypervisor) - **Secure:** Traditional TrustZone secure world -
**Non-secure (Normal):** Traditional normal world (hypervisor, OS, apps)

**Granule Protection Table (GPT):**

Physical memory is divided into 4KB granules, each tagged with a
security state in the GPT. Every memory access checks the GPT:

    Granule States:
      00 = Unassigned (no owner)
      01 = Non-secure (Normal world)
      10 = Realm (Confidential VM)
      11 = Secure (TrustZone) or Root (RMM)

**Granule Protection Check (GPC) Faults:**

When code in one security state tries to access memory belonging to
another state, a GPC fault occurs:

``` {.sourceCode .c}
// Example: Normal world trying to access Realm memory
// This would be a hypervisor trying to read a confidential VM's memory

void hypervisor_read_realm_memory(uint64_t realm_addr) {
    // Attempt to read Realm memory from Normal world (EL2)
    uint64_t value = *(uint64_t *)realm_addr;  // GPC fault!
}

// Exception details:
// FAR_EL2 = realm_addr
// ESR_EL2 = 0x96000034
//   EC = 0x25 (Data Abort)
//   WnR = 0 (Read)
//   FSC = 0x34 (Granule Protection Check fault)
//
// This fault goes to Root world (RMM) not hypervisor!
// RMM decides how to handle: typically terminates access
```

**RME-specific Fault Status Codes:**

    0x34 (0b110100): Granule Protection Check fault (GPC)
      - Access violated GPT security state rules
      
    0x35 (0b110101): Granule Protection Check fault on table walk
      - Page table walk accessed wrong security state

**MECID (Memory Capability Identifier):**

In addition to ASID (Address Space ID), RME adds MECID to TLB entries to
tag translations with their security context:

``` {.sourceCode .c}
// TLB entry with RME
struct arm64_rme_tlb_entry {
    uint64_t va;           // Virtual address
    uint64_t pa;           // Physical address
    uint16_t asid;         // Address Space ID (process)
    uint8_t  mecid;        // Memory Capability ID (security state)
    uint8_t  security;     // Security state (Normal/Realm/Secure/Root)
    uint64_t attributes;   // Page attributes
};

// TLB lookup checks: VA + ASID + MECID + Security State
// All must match for TLB hit
```

**MECID Mismatch Fault:**

If a Realm context tries to use a TLB entry with wrong MECID:

``` {.sourceCode .c}
// Realm switches context, TLB not flushed properly
void realm_context_switch_bug(void) {
    // Switch from Realm 1 to Realm 2
    // But TLB still has Realm 1 entries
    
    // Access memory - TLB hit but wrong MECID
    // Causes MECID mismatch fault
}

// Exception details:
// ESR_ELx with implementation-specific encoding
// Fault handler must:
//   1. Flush TLB entries for old MECID
//   2. Retry access
```

**RME Fault Handler Example:**

``` {.sourceCode .c}
static void handle_rme_gpc_fault(unsigned long addr, unsigned int esr,
                                 struct pt_regs *regs)
{
    unsigned long fsc = ESR_ELx_FSC(esr);
    unsigned long current_state = read_security_state();
    
    if (fsc != 0x34) {
        die("Not a GPC fault", regs, esr);
    }
    
    // Read GPT entry for faulting address
    uint64_t gpt_entry = read_gpt(addr);
    uint8_t granule_state = (gpt_entry >> 60) & 0x3;
    
    // Check security state violation
    if (current_state == SECURITY_NORMAL && 
        granule_state == GRANULE_REALM) {
        // Normal world accessing Realm memory
        printk("Security violation: Normal world accessing Realm at %lx\n", 
               addr);
        // Report to RMM, which will handle policy
        return;
    }
    
    if (current_state == SECURITY_REALM &&
        granule_state == GRANULE_NORMAL) {
        // Realm accessing Normal memory
        // Check if this is an allowed shared page
        if (is_shared_page(addr)) {
            // Legitimate access to shared memory
            return;
        } else {
            // Realm trying to access protected Normal memory
            printk("Realm attempted unauthorized access to Normal world\n");
            terminate_realm(current_realm_id);
        }
    }
}

/* Conceptual implementation based on ARM CCA specifications */
```

**Performance Impact of RME:**

- **Granule Protection Checks:** Every memory access checks GPT
  - Hardware check, but adds latency: \~2-5% overhead
- **Additional TLB tag bits:** MECID increases TLB entry size
  - May reduce effective TLB capacity by \~10%
- **Context switches:** Must flush TLB on Realm entry/exit
  - More expensive than normal context switches
- **Overall:** 2-8% performance overhead for Realm workloads

**RME vs Intel TDX vs AMD SEV-SNP:**

| Feature | ARM RME | Intel TDX | AMD SEV-SNP |
| --- | --- | --- | --- |
| **Protection | GPT (Granule | SEAM (Secure | RMP (Reverse Map |
| Unit** | Protection Table) | Arbitration Mode) | Table) |
| **Granularity** | 4KB | 4KB | 4KB |
| **Tag Bits** | MECID + Security State | TD bits | ASID + VMPL |
| **Fault Type** | GPC Fault (FSC 0x34) | EPT Violation + TD check | #NPF + RMP check |
| **Performance** | 2-8% overhead | 2-10% overhead | 1-5% overhead |
| **Open Spec** | Yes (ARM spec) | Partial | Partial |


------------------------------------------------------------------------

## 7.5 RISC-V Page Faults

RISC-V takes a fundamentally different approach to page faults than
x86-64 or ARM64. While x86-64 and ARM64 have hardware page table walkers
that automatically traverse page table hierarchies, RISC-V delegates
this responsibility entirely to software. This makes RISC-V\'s page
fault mechanism both simpler in hardware and more flexible in software.

### 7.5.1 Software-Managed TLB and Page Faults

On RISC-V, there is **no hardware page table walker**. When a TLB miss
occurs, the hardware immediately generates a page fault exception. The
software exception handler must:

1.  Walk the page tables manually
2.  Check if the translation is valid
3.  If valid: Load the TLB entry explicitly
4.  If invalid: Handle as a true page fault (allocate, swap, or
    terminate)

This means that on RISC-V, **every TLB miss is a page fault exception**,
even if the page is perfectly valid and present in memory. This is very
different from x86-64/ARM64 where TLB misses are handled transparently
by hardware.

**Advantages of Software TLB Management:** - Hardware is simpler
(smaller die area, lower power) - OS has complete flexibility in page
table format - Can implement custom page table structures beyond
standard radix trees - Easier to extend with new features (OS just
updates software)

**Disadvantages:** - Higher TLB miss overhead (trap to software vs
hardware walk) - More complex OS kernel code - Performance depends
heavily on software optimization

### 7.5.2 RISC-V Exception Codes

RISC-V uses the `scause` CSR (Control and Status Register) to indicate
the exception type. For page faults, there are three distinct exception
codes:

    Exception Code 12 (0xC): Instruction page fault
      - Instruction fetch failed
      - Could be TLB miss or true page fault
      
    Exception Code 13 (0xD): Load page fault  
      - Load (read) instruction failed
      - Could be TLB miss or true page fault
      
    Exception Code 15 (0xF): Store/AMO page fault
      - Store (write) or atomic instruction failed
      - Could be TLB miss or true page fault
      
    Note: AMO = Atomic Memory Operation (e.g., atomic add, swap)

Having separate codes for instruction/load/store allows the handler to
immediately know the access type without having to decode the faulting
instruction.

### 7.5.3 RISC-V Exception Registers

When a page fault occurs, RISC-V provides three key CSRs:

**scause (Supervisor Cause Register):**

    Bit 63 (RV64): Interrupt (1) or Exception (0)
    Bits 62-0: Exception Code

    For page faults:
      scause = 12 (0xC) = Instruction page fault
      scause = 13 (0xD) = Load page fault
      scause = 15 (0xF) = Store/AMO page fault

**stval (Supervisor Trap Value Register):**

    Contains the faulting virtual address
      - Equivalent to x86-64's CR2
      - Equivalent to ARM64's FAR_EL1

**sepc (Supervisor Exception Program Counter):**

    Contains the PC of the faulting instruction
      - Handler can return by writing to sepc and executing sret

**Reading exception information:**

``` {.sourceCode .c}
// RISC-V page fault handler entry
void page_fault_handler(void) {
    unsigned long scause = csr_read(CSR_SCAUSE);
    unsigned long stval = csr_read(CSR_STVAL);
    unsigned long sepc = csr_read(CSR_SEPC);
    
    unsigned long exception_code = scause & ~(1UL << 63);
    
    // Determine fault type
    switch (exception_code) {
    case 12:
        handle_instruction_page_fault(stval, sepc);
        break;
    case 13:
        handle_load_page_fault(stval, sepc);
        break;
    case 15:
        handle_store_page_fault(stval, sepc);
        break;
    default:
        die("Not a page fault", scause);
    }
}
```

### 7.5.4 RISC-V Page Table Walk (Software Implementation)

Since RISC-V has no hardware walker, the OS must implement page table
walking in software. Here\'s a complete implementation for Sv39 (3-level
page tables):

``` {.sourceCode .c}
// RISC-V Sv39 page table walk
// Based on RISC-V Privileged Specification v1.12

#define PGSIZE 4096
#define PXMASK 0x1FF  // 9 bits
#define PXSHIFT(level) (PGSIZE_BITS + (9 * (level)))

// Extract VPN (Virtual Page Number) at given level
#define VPN(va, level) (((va) >> PXSHIFT(level)) & PXMASK)

// PTE flags
#define PTE_V    (1L << 0)  // Valid
#define PTE_R    (1L << 1)  // Readable
#define PTE_W    (1L << 2)  // Writable
#define PTE_X    (1L << 3)  // Executable
#define PTE_U    (1L << 4)  // User accessible
#define PTE_G    (1L << 5)  // Global
#define PTE_A    (1L << 6)  // Accessed
#define PTE_D    (1L << 7)  // Dirty

typedef uint64_t pte_t;

// Walk page tables for given virtual address
pte_t *walk_page_table(uint64_t va, int alloc) {
    // Read satp (supervisor address translation and protection)
    uint64_t satp = csr_read(CSR_SATP);
    uint64_t *pagetable = (uint64_t *)(satp & 0x00000FFFFFFFFFFF) * PGSIZE;
    
    // Walk 3 levels (Sv39)
    for (int level = 2; level > 0; level--) {
        pte_t *pte = &pagetable[VPN(va, level)];
        
        if (*pte & PTE_V) {
            // Valid PTE
            if ((*pte & (PTE_R | PTE_W | PTE_X)) != 0) {
                // This is a leaf PTE (has R/W/X bits set)
                // Reached a superpage at level > 0
                return pte;
            }
            // Non-leaf PTE - follow to next level
            pagetable = (uint64_t *)(PTE_TO_PA(*pte));
        } else {
            // Invalid PTE - need to allocate if requested
            if (!alloc) {
                return NULL;  // Page not present
            }
            
            // Allocate new page table page
            uint64_t *newpage = alloc_page_table();
            if (!newpage) {
                return NULL;  // Out of memory
            }
            
            memset(newpage, 0, PGSIZE);
            *pte = PA_TO_PTE(newpage) | PTE_V;
            pagetable = newpage;
        }
    }
    
    // Level 0 - return pointer to final PTE
    return &pagetable[VPN(va, 0)];
}

/* Implementation based on RISC-V Privileged Specification v1.12
   and xv6-riscv operating system (MIT License)
   Reference: https://github.com/mit-pdos/xv6-riscv */
```

### 7.5.5 RISC-V TLB Management

RISC-V provides explicit instructions for managing the TLB. After
updating a page table entry, software must flush the TLB:

**SFENCE.VMA Instruction:**

``` assembly
# Flush all TLB entries
sfence.vma zero, zero

# Flush TLB entries for specific virtual address
sfence.vma a0, zero     # a0 contains virtual address

# Flush TLB entries for specific ASID
sfence.vma zero, a1     # a1 contains ASID

# Flush TLB entries for specific VA and ASID
sfence.vma a0, a1       # a0=VA, a1=ASID
```

**When to use SFENCE.VMA:** - After modifying any PTE - After changing
satp (page table root) - Before accessing memory with new translation

``` {.sourceCode .c}
// Update PTE and flush TLB
void update_pte_and_flush(uint64_t va, pte_t new_pte) {
    pte_t *pte = walk_page_table(va, 0);
    if (!pte) {
        panic("PTE not found");
    }
    
    *pte = new_pte;
    
    // Flush TLB for this virtual address
    asm volatile("sfence.vma %0, zero" :: "r"(va) : "memory");
}
```

### 7.5.6 RISC-V Page Fault Handler Flow

Here\'s a complete RISC-V page fault handler that distinguishes between
TLB misses and true page faults:

``` {.sourceCode .c}
// RISC-V page fault handler (simplified from Linux kernel)
void do_page_fault(struct pt_regs *regs, unsigned long cause,
                   unsigned long addr)
{
    struct task_struct *task = current;
    struct mm_struct *mm = task->mm;
    struct vm_area_struct *vma;
    unsigned int flags = FAULT_FLAG_DEFAULT;
    
    // Determine access type from cause
    if (cause == 15) {
        flags |= FAULT_FLAG_WRITE;  // Store/AMO
    } else if (cause == 12) {
        flags |= FAULT_FLAG_INSTRUCTION;  // Instruction fetch
    }
    // cause == 13 is load (read) - no additional flag needed
    
    // Step 1: Try to handle as TLB miss (fast path)
    // Walk page tables to see if translation exists
    pte_t *pte = walk_page_table(addr, 0);  // Don't allocate
    
    if (pte && (*pte & PTE_V)) {
        // PTE exists and is valid!
        
        // Check permissions match the access type
        if (cause == 15 && !(*pte & PTE_W)) {
            // Store but page not writable - might be COW
            goto slow_path;
        }
        if (cause == 12 && !(*pte & PTE_X)) {
            // Execute but page not executable - permission fault
            goto slow_path;
        }
        if (cause == 13 && !(*pte & PTE_R)) {
            // Load but page not readable - permission fault
            goto slow_path;
        }
        
        // Check user/supervisor
        unsigned long mode = csr_read(CSR_SSTATUS) & SR_SPP;
        if (mode == 0 && !(*pte & PTE_U)) {
            // User mode accessing supervisor page
            goto slow_path;
        }
        
        // Valid translation - just a TLB miss!
        // Set accessed bit if not already set
        if (!(*pte & PTE_A)) {
            *pte |= PTE_A;
        }
        
        // Set dirty bit for stores
        if (cause == 15 && !(*pte & PTE_D)) {
            *pte |= PTE_D;
        }
        
        // Flush TLB for this address (will reload on retry)
        asm volatile("sfence.vma %0, zero" :: "r"(addr) : "memory");
        
        // Done - was just TLB miss, not true page fault
        return;
    }
    
slow_path:
    // True page fault - handle like x86/ARM
    
    // Step 2: Find VMA
    down_read(&mm->mmap_sem);
    vma = find_vma(mm, addr);
    
    if (!vma || vma->vm_start > addr) {
        goto bad_area;
    }
    
    // Step 3: Check if this is stack growth
    if (expand_stack(vma, addr) < 0) {
        goto bad_area;
    }
    
    // Step 4: Check permissions
    if (cause == 15 && !(vma->vm_flags & VM_WRITE)) {
        goto bad_area;
    }
    if (cause == 12 && !(vma->vm_flags & VM_EXEC)) {
        goto bad_area;
    }
    if (cause == 13 && !(vma->vm_flags & VM_READ)) {
        goto bad_area;
    }
    
    // Step 5: Handle the fault
    int ret = handle_mm_fault(vma, addr, flags);
    
    if (ret & VM_FAULT_ERROR) {
        goto error;
    }
    
    up_read(&mm->mmap_sem);
    return;
    
bad_area:
    up_read(&mm->mmap_sem);
    do_trap(regs, SIGSEGV, SEGV_MAPERR, addr);
    return;
    
error:
    up_read(&mm->mmap_sem);
    if (ret & VM_FAULT_OOM) {
        do_exit(SIGKILL);
    }
    return;
}

/* Simplified from Linux kernel arch/riscv/mm/fault.c
   Reference: Linux kernel v6.5, do_page_fault() */
```

### 7.5.7 RISC-V Page Fault Scenarios

**Scenario 1: TLB Miss (Valid Page)**

``` {.sourceCode .c}
// Access a page that's mapped but not in TLB
char *data = mmap(NULL, 4096, PROT_READ|PROT_WRITE,
                  MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
*data = 'A';  // Initial access causes page fault

// Page fault on subsequent access to different line
data[2048] = 'B';  // Same page, different cache line
                   // If TLB was flushed, another "page fault"

// Exception details:
// scause = 15 (Store/AMO page fault)
// stval = address of data (e.g., 0x0000003f80000000)
// sepc = PC of store instruction
//
// Handler action:
//   1. Walk page tables
//   2. Find valid PTE with V=1, W=1
//   3. Set A bit and D bit in PTE
//   4. Execute sfence.vma to flush TLB
//   5. Return (instruction will retry and succeed)
```

**Scenario 2: Demand Paging (First Access)**

``` {.sourceCode .c}
// First access to newly allocated page
char *buffer = malloc(1024*1024);  // 1MB
buffer[0] = 'X';  // Causes true page fault

// Exception details:
// scause = 15 (Store/AMO page fault)
// stval = buffer address
//
// Handler action:
//   1. Walk page tables - PTE not valid (V=0)
//   2. Check VMA - valid address
//   3. Allocate physical page
//   4. Zero page
//   5. Update PTE: V=1, R=1, W=1, A=1, D=1, U=1
//   6. Execute sfence.vma
//   7. Return
```

**Scenario 3: Execute from Non-Executable Page**

``` {.sourceCode .c}
// Attempt to execute data
void *shellcode = malloc(1024);
memcpy(shellcode, exploit, 1024);
((void(*)())shellcode)();  // Try to execute

// Exception details:
// scause = 12 (Instruction page fault)
// stval = shellcode address
// sepc = shellcode address (PC of attempted execution)
//
// Handler action:
//   1. Walk page tables - find PTE with V=1 but X=0
//   2. Recognize: instruction fetch from non-executable page
//   3. Send SIGSEGV
```

**Scenario 4: Copy-on-Write**

``` {.sourceCode .c}
int main() {
    int *shared = malloc(sizeof(int));
    *shared = 42;
    
    if (fork() == 0) {
        *shared = 99;  // COW fault
    }
}

// Exception details:
// scause = 15 (Store/AMO page fault)
// stval = shared address
//
// Handler action:
//   1. Walk page tables - find PTE with V=1, W=0 (read-only COW page)
//   2. Recognize COW scenario
//   3. Allocate new page
//   4. Copy data
//   5. Update child's PTE: V=1, R=1, W=1
//   6. Execute sfence.vma
//   7. Return
```

### 7.5.8 RISC-V Physical Memory Protection (PMP)

In addition to standard MMU page faults, RISC-V has Physical Memory
Protection (PMP), which operates at machine mode (M-mode) and can
generate access faults that look similar to page faults but occur at a
different level.

**PMP vs MMU:** - **MMU:** Translates virtual→physical, enforces
page-level permissions - **PMP:** Protects physical address ranges,
enforced by M-mode

PMP can cause \"access faults\" that appear similar to page faults:

    Exception Code 1: Instruction access fault (PMP violation)
    Exception Code 5: Load access fault (PMP violation)
    Exception Code 7: Store/AMO access fault (PMP violation)

These are different from page faults (codes 12/13/15). PMP faults
indicate the physical address violated M-mode protection rules:

``` {.sourceCode .c}
// PMP access fault handler
void handle_access_fault(unsigned long cause, unsigned long addr) {
    // Access faults (1, 5, 7) indicate PMP violation
    // These usually indicate:
    //   1. Bug in OS (accessing protected physical memory)
    //   2. Security violation
    //   3. Hardware misconfiguration
    
    printk("Access fault (PMP violation) at physical address %lx\n", addr);
    printk("Cause: %lx\n", cause);
    
    // Usually fatal - M-mode firmware prevents access
    panic("PMP violation");
}
```

**Key Difference:** - **Page faults (12/13/15):** Virtual address
translation issues, handled by OS - **Access faults (1/5/7):** Physical
address protection, enforced by M-mode firmware

### 7.5.9 RISC-V Performance Considerations

**TLB Miss Overhead:**

On RISC-V, every TLB miss requires a trap to software:

    TLB miss cost on RISC-V:
      1. Trap to S-mode (save context): ~20-30 cycles
      2. Walk page tables: ~30-50 cycles (if L1 cache hit)
      3. Load TLB implicitly (sfence.vma): ~10 cycles
      4. Return (restore context): ~20-30 cycles
      
    Total: ~80-120 cycles for TLB miss

    Compare to x86-64/ARM64:
      Hardware walk: ~40-100 cycles (no trap overhead)

RISC-V TLB misses are \~2× slower than hardware-walked architectures due
to trap overhead.

**Optimization Strategies:**

``` {.sourceCode .c}
// 1. Larger TLB entries (superpages)
// Use 2MB or 1GB pages where possible
mmap(addr, size, prot, MAP_HUGETLB, ...);

// 2. Pin critical pages in TLB (if hardware supports)
// RISC-V extension proposal for "locked" TLB entries

// 3. Minimize TLB flushes
// Use ASIDs to avoid full TLB flush on context switch

// 4. Optimize page table walk code
// Keep page tables in L1/L2 cache
// Use compiler optimizations for hot path
```

**When Software TLB Management Works Well:** - **Embedded systems:**
Small working sets, predictable access patterns - **Real-time systems:**
Deterministic TLB miss handling - **Custom page tables:** OS can
implement novel page table structures

**When It\'s a Challenge:** - **Servers:** Large working sets, many TLB
misses - **Databases:** Random access patterns, poor TLB hit rates -
**Virtualization:** Nested page tables amplify TLB miss cost

------------------------------------------------------------------------

## 7.6 TLB-Related Exceptions

While most page faults relate to page table entries or permissions, some
exceptions arise specifically from TLB behavior. These TLB-related
exceptions reveal the interaction between the TLB cache and the page
table structures we studied in Chapter 4.

### 7.6.1 TLB Misses on Software-Managed TLBs

As we saw in Section 7.5, RISC-V treats every TLB miss as a page fault
exception because there\'s no hardware walker. This design choice has
interesting implications:

**Fast Path TLB Miss Handler:**

The OS can optimize for the common case where the page is valid:

``` {.sourceCode .c}
// RISC-V fast-path TLB refill (no page fault - direct lookup)
static inline bool try_fast_tlb_refill(unsigned long addr) {
    // Quick page table walk for common case
    pte_t *pte = fast_walk_page_table(addr);
    
    if (likely(pte && (*pte & PTE_V) && 
               (*pte & (PTE_R | PTE_W | PTE_X)))) {
        // Valid leaf PTE found - set accessed bit
        *pte |= PTE_A;
        
        // TLB will be loaded implicitly on return
        asm volatile("sfence.vma %0, zero" :: "r"(addr));
        return true;  // Handled fast path
    }
    
    return false;  // Need slow path (true page fault)
}
```

**Historical Context: MIPS TLB Refill:**

RISC-V\'s approach was influenced by MIPS, which pioneered software TLB
management:

``` {.sourceCode .mips}
# MIPS had a special "TLB refill" exception vector at 0x80000000
# With only 32 instructions available for the fast path

.org 0x80000000
mips_tlb_refill:
    # Ultra-fast TLB refill for common case
    # Must complete in <32 instructions!
    mfc0  $k0, $10         # Get EntryHi (VA + ASID)
    srl   $k0, $k0, 10     # Extract VPN
    lw    $k1, pgdir($k0)  # Load page table entry
    mtc0  $k1, $2          # Load EntryLo
    tlbwr                  # Write random TLB entry
    eret                   # Return
```

RISC-V simplified this by eliminating the special vector and making all
TLB misses regular exceptions.

### 7.6.2 TLB Multi-Hit Exceptions

A TLB multi-hit (or TLB conflict) occurs when multiple TLB entries match
the same virtual address. This should never happen in correct operation
and usually indicates:

1.  **Software bug:** OS loaded same address twice with different
    translations
2.  **Hardware error:** TLB corruption due to cosmic rays, voltage
    glitch, etc.
3.  **Speculative execution bug:** Incorrectly loaded TLB entry wasn\'t
    properly invalidated

**ARM64 TLB Conflict Abort:**

``` {.sourceCode .c}
// ARM64 TLB conflict handler
static void handle_tlb_conflict(unsigned long addr, unsigned int esr) {
    unsigned long fsc = ESR_ELx_FSC(esr);
    
    if (fsc == 0x30) {  // TLB Conflict Abort
        printk("TLB conflict detected at address %lx\n", addr);
        printk("Multiple TLB entries match this address!\n");
        
        // This is serious - TLB is corrupted
        // Must flush ALL TLB entries to resolve
        flush_tlb_all();
        
        // If this happens repeatedly, it's likely hardware failure
        if (++tlb_conflict_count > 10) {
            panic("Repeated TLB conflicts - possible hardware failure");
        }
        
        return;  // Retry after flush
    }
}
```

**x86-64 Handling:**

x86-64 doesn\'t have an explicit \"TLB multi-hit\" exception. Instead,
the behavior is undefined---hardware might: - Use one of the entries
(which one is unpredictable) - Generate a machine check exception -
Cause silent data corruption

Therefore, x86-64 software must be extremely careful to never create TLB
conflicts.

**Prevention Strategies:**

``` {.sourceCode .c}
// Safe TLB update on all architectures
void safe_update_pte(unsigned long va, pte_t new_pte) {
    pte_t *pte = get_pte(va);
    
    // Step 1: Invalidate TLB BEFORE changing PTE
    flush_tlb_one(va);
    
    // Step 2: Update PTE
    *pte = new_pte;
    
    // Step 3: Memory barrier
    smp_wmb();
    
    // Step 4: Flush again (paranoid, but safe)
    flush_tlb_one(va);
}
```

### 7.6.3 TLB Shootdown and Inter-Processor Interrupts (IPIs)

When one CPU modifies a page table entry, all other CPUs\' TLBs may have
stale entries. TLB shootdown is the process of invalidating TLB entries
on remote CPUs.

**Not a Fault, But Related:**

TLB shootdown doesn\'t generate page faults, but it uses inter-processor
interrupts (IPIs) that interrupt remote CPUs:

``` {.sourceCode .c}
// TLB shootdown on multi-core system
void flush_tlb_mm_range(struct mm_struct *mm, unsigned long start,
                        unsigned long end) {
    cpumask_t cpus;
    
    // Step 1: Determine which CPUs need flushing
    // (CPUs that have this mm active)
    cpumask_copy(&cpus, mm_cpumask(mm));
    cpumask_clear_cpu(smp_processor_id(), &cpus);  // Not self
    
    // Step 2: Flush local TLB
    local_flush_tlb_range(start, end);
    
    if (cpumask_empty(&cpus)) {
        return;  // No remote CPUs to notify
    }
    
    // Step 3: Send IPI to remote CPUs
    smp_call_function_many(&cpus, remote_flush_tlb_range,
                          &(struct flush_tlb_info){
                              .mm = mm,
                              .start = start,
                              .end = end
                          }, 1);  // Wait for completion
}

// Executed on remote CPU in response to IPI
void remote_flush_tlb_range(void *info) {
    struct flush_tlb_info *f = info;
    
    // Flush TLB entries in range
    for (unsigned long addr = f->start; addr < f->end; addr += PAGE_SIZE) {
        flush_tlb_one(addr);
    }
}

/* Based on Linux kernel arch/x86/mm/tlb.c
   Reference: Linux kernel v6.5, flush_tlb_mm_range() */
```

**Performance Impact:**

TLB shootdown can be expensive: - IPI latency: \~1-5 microseconds per
remote CPU - Remote TLB flush: \~1-10 microseconds - Total: \~10-50
microseconds for 8 CPUs

For frequently updated pages (e.g., COW pages), shootdown overhead can
dominate:

``` {.sourceCode .c}
// Example: fork() + exec() causes massive TLB shootdown

pid_t pid = fork();  // Parent and child share pages (COW)
                     // All pages marked read-only
                     // No TLB flush yet
                     
if (pid == 0) {
    // Child modifies memory
    global_var = 123;  // COW fault on this CPU
                       // Allocates new page
                       // Must shootdown parent's TLB entry!
                       // IPI to parent CPU
    
    exec("/bin/ls");   // Replace address space
                       // Must shootdown ALL TLB entries
                       // IPIs to ALL CPUs that might have cached entries
}
```

**Optimization: Lazy TLB Shootdown:**

Modern systems use lazy TLB shootdown:

``` {.sourceCode .c}
// Instead of immediate IPI:
void lazy_tlb_shootdown(unsigned long va) {
    // Mark TLB entry as "needs flush" on remote CPUs
    set_tlb_flush_pending(va);
    
    // Don't send IPI immediately
    // Remote CPUs will check "flush pending" on:
    //   1. Next context switch
    //   2. Next timer interrupt
    //   3. When they try to access the address (page fault)
    
    // This avoids IPI overhead if remote CPUs aren't using the page
}
```

### 7.6.4 TLB Maintenance Instructions and Exceptions

Different architectures provide different TLB maintenance instructions,
and using them incorrectly can cause exceptions:

**x86-64 INVLPG:**

``` assembly
; Invalidate TLB entry for specific page
invlpg [rax]   ; rax contains virtual address

; This instruction can fault if:
;   1. Address is not canonical (bits 63:48 must be sign-extension of bit 47)
;   2. Executed in user mode (privileged instruction)
```

**ARM64 TLBI Instructions:**

``` assembly
; Invalidate TLB by VA
tlbi vaae1is, x0   ; x0 contains VA

; Can fault if:
;   1. Executed at wrong exception level
;   2. System register access trapped by hypervisor
```

**RISC-V SFENCE.VMA:**

``` assembly
; Flush TLB
sfence.vma x5, x6  ; x5=VA, x6=ASID

; Can fault if:
;   1. Executed in U-mode (illegal instruction exception)
;   2. TVM bit set in mstatus (trap to M-mode)
```

**Incorrect TLB Flush Example:**

``` {.sourceCode .c}
// Bug: Forgot to flush TLB after PTE update
void buggy_update_pte(unsigned long va, pte_t new_pte) {
    pte_t *pte = get_pte(va);
    *pte = new_pte;
    
    // BUG: No TLB flush!
    // CPU still has old translation in TLB
    // Will use stale translation until TLB entry is evicted
    
    // Result: Accessing va will use OLD translation
    // Can cause:
    //   - Security vulnerabilities (wrong permissions)
    //   - Data corruption (wrong physical page)
    //   - Hard-to-debug crashes
}

// Fix: Always flush after PTE update
void correct_update_pte(unsigned long va, pte_t new_pte) {
    pte_t *pte = get_pte(va);
    *pte = new_pte;
    
    // Flush TLB for this address
    flush_tlb_one(va);
    
    // On SMP, also flush remote CPUs
    flush_tlb_mm_range(current->mm, va, va + PAGE_SIZE);
}
```

------------------------------------------------------------------------

## 7.7 Page Table Walk Failures

Page faults can occur at any level of the page table hierarchy.
Understanding where the walk failed helps diagnose the problem.

### 7.7.1 Multi-Level Page Table Failures

Recall from Chapter 3 that modern architectures use multi-level page
tables: - **x86-64:** 4 levels (PML4, PDPT, PD, PT) or 5 levels -
**ARM64:** 4 levels (L0, L1, L2, L3) for 48-bit VA - **RISC-V:** 3
levels (L2, L1, L0) for Sv39

A page fault can occur at any level if an intermediate PTE is invalid:

``` {.sourceCode .c}
// Page table walk showing failures at each level
pte_t *walk_and_report_failure(unsigned long va) {
    // Level 4 (or L3 on ARM, L2 on RISC-V)
    pte_t *pml4e = get_pml4e(va);
    if (!(*pml4e & PTE_P)) {
        printk("PML4 entry not present\n");
        return NULL;  // Fault at level 4
    }
    
    // Level 3 (PDPT)
    pte_t *pdpte = get_pdpte(pml4e, va);
    if (!(*pdpte & PTE_P)) {
        printk("PDPT entry not present\n");
        return NULL;  // Fault at level 3
    }
    
    if (*pdpte & PTE_PS) {
        // 1GB huge page at level 3
        return pdpte;
    }
    
    // Level 2 (PD)
    pte_t *pde = get_pde(pdpte, va);
    if (!(*pde & PTE_P)) {
        printk("PD entry not present\n");
        return NULL;  // Fault at level 2
    }
    
    if (*pde & PTE_PS) {
        // 2MB huge page at level 2
        return pde;
    }
    
    // Level 1 (PT)
    pte_t *pte = get_pte(pde, va);
    if (!(*pte & PTE_P)) {
        printk("PT entry not present\n");
        return NULL;  // Fault at level 1 (leaf)
    }
    
    return pte;
}
```

**ARM64 Fault Status Codes by Level:**

    0x04: Translation fault, level 0
    0x05: Translation fault, level 1  
    0x06: Translation fault, level 2
    0x07: Translation fault, level 3

    0x0C: Permission fault, level 0
    0x0D: Permission fault, level 1
    0x0E: Permission fault, level 2
    0x0F: Permission fault, level 3

The level information tells you exactly where in the page table
hierarchy the problem occurred.

### 7.7.2 Invalid Page Table Pointers

Page table entries at intermediate levels must point to valid page
tables. If they point to unmapped physical memory or incorrect
addresses, various faults can occur:

**Scenario: Corrupted Page Table Pointer**

``` {.sourceCode .c}
// Corruption: PTE points to invalid physical address
void corrupt_page_table(void) {
    pte_t *pdpte = get_pdpte(current->mm->pgd, 0x10000000);
    
    // Corrupt: point to non-existent physical address
    *pdpte = 0xDEADBEEF000 | PTE_P;  // Invalid physical address
    
    // Now any access to VA 0x10000000-0x13FFFFFFF will fault
    // But at hardware page table walk time, not immediate
}

// When CPU tries to access 0x10000000:
// 1. Walk to PML4 - OK
// 2. Walk to PDPT - OK
// 3. Try to read PD at physical address 0xDEADBEEF000
// 4. Hardware detects: address not in valid RAM range
// 5. Generates page fault (or machine check exception)

// x86-64 error code: 0x0 (P=0, not present)
// But real cause: Corrupted page table, not missing page
```

**Detection:**

``` {.sourceCode .c}
// Check page table integrity
bool validate_page_table_entry(pte_t pte, int level) {
    if (!(pte & PTE_P)) {
        return true;  // Not present is OK
    }
    
    // Extract physical address
    unsigned long pa = pte & PTE_PFN_MASK;
    
    // Check if physical address is valid
    if (!pfn_valid(pa >> PAGE_SHIFT)) {
        printk("Invalid PFN in PTE at level %d: %lx\n", level, pa);
        return false;  // Corruption detected
    }
    
    // Check reserved bits
    if (pte & PTE_RESERVED_MASK) {
        printk("Reserved bits set in PTE: %lx\n", pte);
        return false;
    }
    
    return true;
}
```

### 7.7.3 Nested Page Table Failures

In virtualization (Chapter 5), two-stage translation means failures can
occur in either stage:

**Stage 1 vs Stage 2 Failures:**

    Guest Virtual Address (GVA)
             |
             v
        [Guest Page Tables - Stage 1]
             |
             v
    Guest Physical Address (GPA)
             |
             v
        [Host Page Tables - Stage 2]
             |
             v
    Host Physical Address (HPA)

**Stage 1 Failure (Guest Page Fault):** - Guest OS handles it normally -
Allocates guest physical page - Updates guest page tables - No VM exit
to hypervisor (unless configured)

**Stage 2 Failure (EPT/NPT Fault):** - VM exit to hypervisor -
Hypervisor handles: - Allocate host physical page - Map GPA → HPA in
EPT/NPT - Resume guest - Guest is unaware (transparent)

**Both Stages Fail:**

``` {.sourceCode .c}
// Nested page fault handler (hypervisor)
void handle_nested_page_fault(uint64_t gpa, uint32_t error_code) {
    // This is a Stage 2 (EPT/NPT) fault
    // GPA is the guest physical address
    
    // Step 1: Check if GPA is valid for this guest
    if (!is_valid_gpa(current_vm, gpa)) {
        // Guest tried to access GPA outside its allocated memory
        // Inject machine check into guest
        inject_guest_mce(gpa);
        return;
    }
    
    // Step 2: Allocate host physical page
    uint64_t hpa = alloc_host_page();
    
    // Step 3: Update EPT/NPT
    update_ept(gpa, hpa, EPT_READ | EPT_WRITE | EPT_EXEC);
    
    // Step 4: Resume guest (will retry and succeed)
    vmresume();
}

/* Conceptual implementation based on KVM
   Reference: Linux kernel virt/kvm/ */
```

**Nested Fault During Stage 1 Walk:**

On ARM64, if Stage 1 page table walk itself causes a Stage 2 fault:

    Example:
    1. Guest accesses GVA 0x10000
    2. Hardware walks guest page tables (Stage 1)
    3. Guest page table is at GPA 0x80000000
    4. GPA 0x80000000 not mapped in Stage 2 (EPT/NPT)
    5. Stage 2 fault during Stage 1 walk!
    6. ESR_EL2 has S1PTW bit set (Stage 1 Page Table Walk)

    // ARM64 specific handling
    if (ESR_ELx_S1PTW(esr)) {
        printk("Stage 2 fault during Stage 1 page table walk\n");
        printk("Guest page tables not mapped in EPT\n");
        
        // Allocate host physical page for guest page table
        handle_guest_page_table_fault(gpa);
    }

This adds significant complexity---now page table walks themselves can
fault!

### 7.7.4 Reserved Bits and Future-Proofing

Page table entries have reserved bits that must be zero. Setting these
can cause immediate faults:

**x86-64 Reserved Bits:**

    Bits 51:M: Reserved (M = MAXPHYADDR, typically 46 or 52)
    Bits 62:52: Available for software use (not reserved)
    Bit 63: XD (Execute Disable) if supported

    If any reserved bit (51:M) is set to 1:
      → Page fault with RSVD bit set in error code

**Why Reserved Bits Matter:**

``` {.sourceCode .c}
// Future CPU adds new feature using bit 50
// Old software that wrote to bit 50 will break!

// Old software (written in 2023):
pte_t pte = pa | PTE_P | PTE_W | (1UL << 50);  // Misuse bit 50 for custom flag

// On CPU from 2028 that defines bit 50:
// → Page fault with RSVD bit set
// → Software breaks

// Correct: Only use bits designated for software (52-62):
pte_t pte = pa | PTE_P | PTE_W;
pte |= (1UL << 52);  // Use bit 52 for custom flag (safe)
```

**Checking for Reserved Bit Violations:**

``` {.sourceCode .c}
void check_reserved_bits(pte_t pte) {
    // Get maximum physical address bits supported
    uint32_t max_phy_addr = cpuid_max_phy_addr();  // e.g., 46
    
    // Bits above max_phy_addr must be zero
    uint64_t reserved_mask = ~((1UL << max_phy_addr) - 1);
    reserved_mask &= 0x000FFFFFFFFFFFFF;  // Exclude bits 63:52
    
    if (pte & reserved_mask) {
        printk("Reserved bits set in PTE: %lx\n", pte);
        printk("Reserved mask: %lx\n", reserved_mask);
        // This will cause page fault with RSVD=1
    }
}
```

------------------------------------------------------------------------

## 7.8 Page Overlapping and Aliasing Faults

Page overlapping occurs when multiple virtual addresses map to the same
physical page. While this is sometimes intentional (shared memory,
copy-on-write), it can cause subtle bugs and performance issues if not
managed correctly. Understanding aliasing faults is crucial for both OS
developers and application programmers working with shared memory.

### 7.8.1 What is Page Aliasing?

**Page aliasing** means multiple virtual addresses resolve to the same
physical address. This can be:

1.  **Intentional:** Shared memory, memory-mapped files, copy-on-write
2.  **Accidental:** Software bug creating duplicate mappings
3.  **Malicious:** Exploit attempting to bypass security checks

The danger comes when: - Different virtual addresses have **different
permissions** - Different virtual addresses have **different caching
attributes**\
- TLB or cache coherency is violated

### 7.8.2 x86-64 PAT (Page Attribute Table) Conflicts

x86-64 uses the Page Attribute Table (PAT) to specify caching
attributes. If the same physical page is mapped with conflicting PAT
settings, undefined behavior occurs:

**PAT Memory Types:**

    WB (Write-Back): Cacheable, write-back
    WT (Write-Through): Cacheable, write-through
    UC (Uncacheable): No caching
    UC- (Uncacheable minus): No caching, but can be overridden
    WC (Write-Combining): Combine writes, good for framebuffers
    WP (Write-Protected): Cacheable reads, uncached writes

**Conflict Scenario:**

``` {.sourceCode .c}
// Dangerous: Same physical page with different caching
void create_pat_conflict(uint64_t phys_addr) {
    // Process A maps physical page as Write-Back (cacheable)
    void *va1 = mmap(NULL, 4096, PROT_READ|PROT_WRITE,
                     MAP_SHARED|MAP_ANONYMOUS, -1, 0);
    set_memory_wb(va1);  // PAT: Write-Back
    
    // Process B maps SAME physical page as Uncacheable
    void *va2 = mmap(NULL, 4096, PROT_READ|PROT_WRITE,
                     MAP_SHARED|MAP_ANONYMOUS, -1, 0);
    set_memory_uc(va2);  // PAT: Uncacheable
    
    // Result: UNDEFINED BEHAVIOR!
    // - Data corruption possible
    // - Machine Check Exception possible
    // - Silent failures
}
```

**Why This is Dangerous:**

    Process A (Write-Back):
      1. Writes to VA1 → data goes to CPU cache
      2. Cache not flushed yet
      3. Data in cache, not in RAM
      
    Process B (Uncacheable):
      1. Reads from VA2 → bypasses cache, reads RAM
      2. Gets OLD data (stale)!
      3. Process A's write not visible
      
    Result: Processes see DIFFERENT data for same physical location!

**x86-64 PAT Conflict Detection:**

Modern x86-64 CPUs can detect some PAT conflicts and generate Machine
Check Exceptions (MCE), but behavior is not guaranteed:

``` {.sourceCode .c}
// Kernel must track PAT settings per physical page
struct page {
    unsigned long flags;
    atomic_t _mapcount;
    unsigned int pat_type;  // Current PAT setting
    // ...
};

int set_memory_type(unsigned long addr, unsigned long numpages,
                    enum page_cache_mode type) {
    unsigned long pfn = addr >> PAGE_SHIFT;
    
    for (int i = 0; i < numpages; i++) {
        struct page *page = pfn_to_page(pfn + i);
        
        // Check if page already has different PAT type
        if (page_mapped(page) && page->pat_type != type) {
            printk("PAT conflict: page already mapped with type %d\n",
                   page->pat_type);
            return -EINVAL;  // Reject conflicting mapping
        }
        
        page->pat_type = type;
    }
    
    return 0;
}

/* Based on Linux kernel arch/x86/mm/pat.c
   Reference: Linux kernel v6.5, memtype_reserve() */
```

### 7.8.3 ARM64 Memory Attribute Conflicts

ARM64 uses MAIR_EL1 (Memory Attribute Indirection Register) similar to
x86\'s PAT:

**ARM64 Memory Types:**

    Device-nGnRnE: Device memory, Non-Gathering, Non-Reordering, No Early Write Ack
    Device-nGnRE:  Device memory, Non-Gathering, Non-Reordering, Early Write Ack
    Normal-NC:     Normal memory, Non-Cacheable
    Normal-WT:     Normal memory, Write-Through
    Normal-WB:     Normal memory, Write-Back

**ARM Architecture Requirement:**

> \"All memory transactions to a single physical address must use\
> the same memory type and cacheability attributes\" --- ARM
> Architecture Reference Manual ARMv8

Violation is **UNPREDICTABLE** and can cause: - Synchronous External
Abort - Data corruption - TLB conflicts - Implementation-defined
behavior

**Example Conflict:**

``` {.sourceCode .c}
// ARM64: Conflicting memory attributes
void arm_attr_conflict(uint64_t phys_addr) {
    // Map 1: Normal memory, Write-Back
    uint64_t *pte1 = get_pte(va1);
    *pte1 = phys_addr | ATTR_NORMAL_WB | PTE_VALID;
    
    // Map 2: Device memory, Strongly Ordered
    uint64_t *pte2 = get_pte(va2);
    *pte2 = phys_addr | ATTR_DEVICE_nGnRnE | PTE_VALID;
    
    // ARM will detect this as UNPREDICTABLE
    // May generate Data Abort when accessed
}

// Data Abort handler sees:
// ESR_EL1.EC = 0x25 (Data Abort)
// ESR_EL1.DFSC = 0x10 (Synchronous External Abort)
// Likely cause: Memory attribute conflict
```

**ARM64 Prevention:**

``` {.sourceCode .c}
// Track memory attributes per physical page
int arm64_set_memory_attr(unsigned long va, unsigned long pa,
                          unsigned int attr) {
    // Check if physical page has existing mapping
    struct page *page = phys_to_page(pa);
    
    if (page_mapped(page)) {
        unsigned int existing_attr = page->arm_attr;
        
        if (existing_attr != attr) {
            // Conflicting attributes!
            printk("Memory attribute conflict: pa=%lx\n", pa);
            printk("  Existing: %u, Requested: %u\n",
                   existing_attr, attr);
            return -EINVAL;
        }
    }
    
    page->arm_attr = attr;
    return 0;
}
```

### 7.8.4 Virtual Cache Aliasing (VIPT Caches)

Virtual cache aliasing occurs with **VIPT (Virtually-Indexed,
Physically-Tagged)** caches when multiple virtual addresses map to the
same physical address:

**VIPT Cache Structure:**

    Cache indexed by: Virtual Address bits [13:6] (for 16KB cache, 64-byte lines)
    Cache tagged by:  Physical Address bits [47:12] (or whatever tag size)

    Problem: Two different VAs mapping to same PA can index different cache lines!

**Aliasing Scenario:**

    Assume 16KB VIPT L1 cache, 64-byte cache lines:
      - Index uses VA[13:6] (8 bits = 256 sets)
      - Offset uses VA[5:0] (6 bits = 64 bytes)

    Mapping 1: VA 0x00001000 → PA 0x80000000
      Index = VA[13:6] = 0x040

    Mapping 2: VA 0x00005000 → PA 0x80000000 (SAME physical page!)
      Index = VA[13:6] = 0x140

    Different indices (0x040 vs 0x140) for SAME physical data!

**Cache Incoherency Example:**

``` {.sourceCode .c}
// Two processes sharing memory via different VAs
// Process A
char *ptr_a = mmap(...);  // Maps to VA 0x00001000 → PA 0x80000000
*ptr_a = 'A';             // Writes to cache line at index 0x040

// Process B  
char *ptr_b = mmap(...);  // Maps to VA 0x00005000 → PA 0x80000000 (SAME PA!)
char value = *ptr_b;      // Reads from cache line at index 0x140
                          // MISS! (different index)
                          // Reads old value from memory
                          // value != 'A' !!

// Two cache lines for same physical data - incoherent!
```

**Consequences:** - Processes see inconsistent data - Write to one VA
not visible to other VA - Silent data corruption

### 7.8.5 Detecting and Preventing Virtual Aliasing

**ARM: Cache Coloring**

ARM systems often require \"cache coloring\" to prevent VIPT aliasing:

``` {.sourceCode .c}
// ARM cache coloring enforcement
#define SHMLBA  (4 * PAGE_SIZE)  // 16KB alignment for shared memory
#define CACHE_COLOUR_MASK 0x3000 // Bits 13:12 for 16KB VIPT cache

// Check if two VAs can alias in VIPT cache
static inline bool can_cache_alias(unsigned long va1, unsigned long va2) {
    return (va1 & CACHE_COLOUR_MASK) != (va2 & CACHE_COLOUR_MASK);
}

// When creating shared memory mapping
unsigned long get_unmapped_area_color(struct file *file,
                                      unsigned long addr,
                                      unsigned long len) {
    unsigned long color;
    
    if (file && file->f_mapping) {
        // Ensure all mappings of same file have same color
        color = file->f_mapping->color;
    } else {
        color = 0;
    }
    
    // Find VA with matching color bits
    addr = find_vma_with_color(addr, len, color);
    return addr;
}

/* Conceptual implementation based on ARM Linux
   Reference: Linux kernel arch/arm/mm/mmap.c */
```

**Historical: MIPS Cache Aliasing**

MIPS had severe VIPT aliasing issues and used various solutions:

``` {.sourceCode .c}
// MIPS Solution 1: Flush cache on alias detection
void mips_flush_cache_page(struct vm_area_struct *vma,
                           unsigned long addr) {
    unsigned long pfn = pte_pfn(*get_pte(addr));
    
    // Check if any other VMA maps this physical page
    list_for_each_entry(alias_vma, &page->mapping->vmas, shared) {
        if (alias_vma != vma) {
            unsigned long alias_va = alias_vma->vm_start;
            
            // Check for cache aliasing
            if ((addr ^ alias_va) & CACHE_ALIAS_MASK) {
                // Alias detected! Flush both cache lines
                flush_cache_line(addr);
                flush_cache_line(alias_va);
            }
        }
    }
}

// MIPS Solution 2: Use uncached mappings for aliases
// If can't avoid aliasing, map as uncached (slow but correct)
if (has_cache_alias(va, pa)) {
    pte = make_pte_uncached(pa);
}
```

**Modern Solution: PIPT Caches**

Modern CPUs largely avoid this issue by using PIPT (Physically-Indexed,
Physically-Tagged) caches:

    PIPT Cache:
      - Index uses Physical Address bits
      - Tag uses Physical Address bits
      - No aliasing possible!
      - But requires full TLB lookup before cache lookup (slower)
      
    Most modern CPUs:
      - L1: VIPT (with careful design to avoid aliasing within page)
      - L2/L3: PIPT (no aliasing issues)

### 7.8.6 Security: Rowhammer and Aliasing Attacks

Page aliasing can be exploited for attacks. **Rowhammer** uses
conflicting cache attributes:

``` {.sourceCode .c}
// Rowhammer exploit using cache aliasing
void rowhammer_attack(void) {
    // Map target physical page twice:
    // 1. Cached mapping (for fast repeated access)
    // 2. Uncached mapping (to bypass cache and hit DRAM)
    
    void *cached = mmap_with_attr(phys_addr, CACHED);
    void *uncached = mmap_with_attr(phys_addr, UNCACHED);
    
    // Hammer: alternately access two DRAM rows
    while (1) {
        *(volatile uint64_t *)cached = 0;      // Fast (cached)
        *(volatile uint64_t *)uncached = 0;    // Bypasses cache → DRAM
        clflush(cached);                        // Flush to ensure DRAM access
        
        // Repeated DRAM activations cause bit flips in adjacent rows!
    }
}
```

**Mitigation:** Kernel must prevent conflicting cache attributes:

``` {.sourceCode .c}
// Reject mappings that would create cache conflicts
int check_for_cache_conflict(struct page *page, pgprot_t new_prot) {
    if (page_mapped(page)) {
        pgprot_t existing = get_page_protection(page);
        
        if (pgprot_val(existing) != pgprot_val(new_prot)) {
            // Different cache attributes!
            printk("Rejecting mapping with conflicting attributes\n");
            return -EINVAL;
        }
    }
    return 0;
}
```

### 7.8.7 Shared Memory and Intentional Aliasing

Shared memory (shm, mmap with MAP_SHARED) creates intentional aliasing:

``` {.sourceCode .c}
// Proper shared memory without aliasing issues
int shm_id = shmget(IPC_PRIVATE, 4096, IPC_CREAT | 0666);

// Process A
void *ptr_a = shmat(shm_id, NULL, 0);  // Kernel chooses VA

// Process B
void *ptr_b = shmat(shm_id, NULL, 0);  // Kernel chooses VA

// Kernel ensures:
// 1. Both VAs map to same physical page
// 2. Both VAs have same cache attributes
// 3. No cache aliasing (VAs differ only in bits not used for cache indexing)
```

**Key Requirements:** - Same memory type (cached/uncached) - Same
permissions (both writable, or both read-only) - If VIPT cache: VAs must
not alias in cache

------------------------------------------------------------------------

## 7.9 Permission Violations

Permission violations are page faults caused by accessing memory in a
way that violates the protection bits in the page table entry. These
faults enforce the security boundaries we studied in Chapter 6.

### 7.9.1 Read/Write/Execute Permission Faults

The three basic permissions can each be violated:

**Write to Read-Only Page:**

``` {.sourceCode .c}
// Attempt to modify const data
const int readonly_var = 42;
*(int *)&readonly_var = 99;  // Permission fault!

// x86-64 error code: 0x7 (P=1, W/R=1, U/S=1)
// ARM64: ESR.DFSC = 0x0F (Permission fault, level 3), ESR.WnR = 1
// RISC-V: scause = 15 (Store page fault), PTE has W=0
```

**Execute from Non-Executable Page (NX Violation):**

``` {.sourceCode .c}
// Attempt to execute data
char shellcode[] = {0x90, 0x90, 0xc3};  // NOP, NOP, RET
void (*func)() = (void(*)())shellcode;
func();  // Permission fault!

// x86-64: error code = 0x15 (P=1, I/D=1, U/S=1), NX bit set in PTE
// ARM64: ESR.EC = 0x20 (Instruction Abort), ESR.DFSC = 0x0F
// RISC-V: scause = 12 (Instruction page fault), PTE has X=0
```

**Read from Write-Only Page:**

Rare, but some architectures support write-only pages:

``` {.sourceCode .c}
// Write-only page (x86-64 doesn't support this, ARM64 does)
// ARM64 can have: W=1, R=0 (write-only)

// Attempt to read
volatile int *wo_ptr = write_only_page;
int value = *wo_ptr;  // Permission fault on ARM64!
```

### 7.9.2 User/Supervisor Violations

User mode accessing kernel pages is a fundamental security boundary:

**User Accessing Kernel Page:**

``` {.sourceCode .c}
// User trying to read kernel memory
void user_code(void) {
    // Kernel memory typically at high addresses
    volatile uint64_t *kernel_ptr = (uint64_t *)0xFFFFFFFF80000000;
    uint64_t value = *kernel_ptr;  // Permission fault!
}

// x86-64: error code = 0x5 (P=1, W/R=0, U/S=1)
//   U/S=1 means user mode, but page is supervisor-only
// ARM64: User accessing page without U bit set
// RISC-V: User accessing page without PTE_U bit
```

**Why This Matters:**

    Without user/supervisor protection:
      1. User programs could read kernel memory (information leak)
      2. User programs could modify kernel memory (privilege escalation)
      3. User programs could execute kernel code (arbitrary kernel execution)
      
    This is the PRIMARY mechanism for process isolation!

### 7.9.3 SMEP (Supervisor Mode Execution Prevention)

SMEP prevents the kernel from executing user pages, stopping
\"ret2user\" attacks:

**Ret2User Attack (without SMEP):**

``` {.sourceCode .c}
// Attacker's plan:
// 1. Map executable shellcode in user space
// 2. Exploit kernel vulnerability to redirect execution
// 3. Kernel executes shellcode with ring 0 privileges

// User space shellcode (attacker-controlled)
void user_shellcode(void) {
    // Evil code with kernel privileges!
    make_me_root();
}

// Kernel vulnerability (hypothetical)
void vulnerable_kernel_function(void (*callback)(void)) {
    callback();  // If callback points to user space, disaster!
}

// Without SMEP:
//   Kernel happily executes user shellcode
//   Shellcode runs with ring 0 privileges
//   System compromised

// With SMEP:
//   Kernel tries to execute user page
//   CPU generates page fault (SMEP violation)
//   Error code bit indicating SMEP
//   Kernel panics or logs security event
```

**x86-64 SMEP Implementation:**

``` {.sourceCode .c}
// Enable SMEP
void enable_smep(void) {
    // Set CR4.SMEP (bit 20)
    uint64_t cr4 = read_cr4();
    cr4 |= (1 << 20);  // SMEP bit
    write_cr4(cr4);
    
    // Now any instruction fetch from user page in supervisor mode
    // will cause page fault with specific error code
}

// SMEP page fault detection
void handle_smep_violation(struct pt_regs *regs, unsigned long error_code,
                           unsigned long addr) {
    // Check for SMEP violation:
    // - Supervisor mode (U/S = 0)
    // - Instruction fetch (I/D = 1)
    // - Present page (P = 1)
    
    if (!(error_code & 0x4) &&   // Supervisor mode
        (error_code & 0x10) &&    // Instruction fetch
        (error_code & 0x1)) {     // Present
        
        // This is SMEP violation!
        printk("SMEP violation at %lx, IP=%lx\n", addr, regs->ip);
        printk("Kernel attempted to execute user page!\n");
        
        // This is a serious security issue
        oops_end(SIGKILL, regs, error_code);
    }
}
```

### 7.9.4 SMAP (Supervisor Mode Access Prevention)

SMAP prevents the kernel from reading/writing user pages except through
explicit copy functions:

**Why SMAP is Needed:**

``` {.sourceCode .c}
// Kernel bug: directly accessing user pointer
int kernel_bug(char *user_buffer) {
    char kernel_data[100];
    strcpy(kernel_data, user_buffer);  // BUG: direct access to user memory!
    
    // Without SMAP:
    //   Works fine (but dangerous!)
    //   Attacker could pass kernel memory address
    //   Kernel copies kernel data to kernel buffer
    //   Information leak!
    
    // With SMAP:
    //   Page fault (SMAP violation)
    //   Kernel cannot access user memory directly
    //   Bug is caught immediately
}
```

**Correct Way with SMAP:**

``` {.sourceCode .c}
// Correct: Use copy_from_user()
int kernel_correct(char __user *user_buffer) {
    char kernel_data[100];
    
    // copy_from_user() temporarily disables SMAP
    if (copy_from_user(kernel_data, user_buffer, 100)) {
        return -EFAULT;  // Invalid user pointer
    }
    
    // Process kernel_data safely
    return 0;
}

// x86-64 copy_from_user() implementation
unsigned long copy_from_user(void *to, const void __user *from,
                              unsigned long n) {
    might_fault();  // Debug check
    
    // Clear AC flag in EFLAGS to temporarily allow user access
    stac();  // Set AC (Alignment Check / SMAP override)
    
    // Now can access user memory
    memcpy(to, from, n);
    
    // Restore SMAP protection
    clac();  // Clear AC
    
    return 0;
}

/* Based on Linux kernel arch/x86/lib/usercopy.c
   Reference: Linux kernel v6.5, copy_from_user() */
```

**SMAP Fault Detection:**

``` {.sourceCode .c}
// x86-64 SMAP violation
// error_code = 0x3: P=1, W/R=0, U/S=0 (supervisor read of user page)
// error_code = 0x3 with CR4.SMAP=1 and EFLAGS.AC=0

void handle_smap_violation(unsigned long addr, unsigned long error_code) {
    if (!(error_code & 0x4) &&  // Supervisor mode
        (error_code & 0x1)) {    // Present page
        
        // Check if user page
        pte_t *pte = get_pte(addr);
        if (*pte & PTE_U) {
            // Supervisor accessing user page with SMAP enabled
            printk("SMAP violation at %lx\n", addr);
            oops_end(SIGKILL, current_regs, error_code);
        }
    }
}
```

### 7.9.5 ARM PAN (Privileged Access Never)

ARM\'s PAN is equivalent to x86\'s SMAP:

``` {.sourceCode .c}
// ARM64 PAN control
// PAN is controlled by PSTATE.PAN bit

// Enable PAN (prevent kernel from accessing user memory)
static inline void arm64_enable_pan(void) {
    asm volatile("msr pan, #1" ::: "memory");
}

// Disable PAN temporarily for legitimate user access
static inline void arm64_disable_pan(void) {
    asm volatile("msr pan, #0" ::: "memory");
}

// ARM64 copy_from_user
unsigned long arm64_copy_from_user(void *to, const void __user *from,
                                   unsigned long n) {
    unsigned long res = n;
    
    // Disable PAN
    arm64_disable_pan();
    
    // Copy data
    while (n--) {
        *((char *)to)++ = *((char *)from)++;
    }
    
    // Re-enable PAN
    arm64_enable_pan();
    
    return res;
}

/* Simplified from Linux kernel arch/arm64/lib/copy_from_user.S */
```

**PAN Violation Detection:**

``` {.sourceCode .c}
// ARM64 PAN violation causes Permission Fault
void handle_pan_violation(unsigned long addr, unsigned int esr) {
    unsigned long ec = ESR_ELx_EC(esr);
    unsigned long fsc = ESR_ELx_FSC(esr);
    
    // Permission fault at EL1 (kernel)
    if (ec == ESR_ELx_EC_DABT_CUR && 
        (fsc >= 0x0C && fsc <= 0x0F)) {
        
        // Check if accessing user page with PAN enabled
        pte_t *pte = walk_page_table(addr, 0);
        if (pte && (*pte & PTE_USER)) {
            // Kernel accessing user page with PAN=1
            printk("PAN violation at %lx\n", addr);
            die("PAN violation", current_regs, esr);
        }
    }
}
```

### 7.9.6 Memory Protection Keys (MPK/PKU)

Intel MPK allows fine-grained protection within a process:

**MPK Operation:**

``` {.sourceCode .c}
// MPK uses 4-bit protection keys (16 possible domains)
// Each page has a protection key (PKEY) in bits 62:59 of PTE
// PKRU register (32-bit) controls access to each key

// Allocate protection key
int pkey = pkey_alloc(0, 0);  // Returns key 0-15

// Assign pages to protection key
pkey_mprotect(addr, len, PROT_READ|PROT_WRITE, pkey);

// Disable access to this key
pkey_set(pkey, PKEY_DISABLE_ACCESS);

// Now access causes page fault
*addr = 42;  // Permission fault! (MPK violation)

// x86-64 error code: bit 5 (PK) will be set
// error_code & 0x20 = 1 indicates MPK violation
```

**MPK Fault Handler:**

``` {.sourceCode .c}
void handle_mpk_fault(struct pt_regs *regs, unsigned long error_code,
                      unsigned long addr) {
    if (error_code & 0x20) {
        // MPK violation
        pte_t *pte = get_pte(addr);
        int pkey = (*pte >> 59) & 0xF;  // Extract protection key
        
        uint32_t pkru = rdpkru();  // Read PKRU register
        bool access_disabled = (pkru >> (pkey * 2)) & 0x1;
        bool write_disabled = (pkru >> (pkey * 2)) & 0x2;
        
        printk("MPK violation: key=%d, access_disabled=%d, write_disabled=%d\n",
               pkey, access_disabled, write_disabled);
        
        // Application-specific handling
        // (MPK is for intra-process isolation, so app decides policy)
        force_sig(SIGSEGV, current);
    }
}
```

**MPK Performance:**

``` {.sourceCode .c}
// MPK is MUCH faster than mprotect()
// Benchmark: Protecting 1000 pages

// mprotect() approach:
for (int i = 0; i < 1000; i++) {
    mprotect(pages[i], PAGE_SIZE, PROT_NONE);  // ~5-10 µs each
}
// Total: ~5-10 ms

// MPK approach:
pkey_set(pkey, PKEY_DISABLE_ACCESS);  // ~5-10 ns
// Total: ~10 ns (500,000× faster!)

// This makes MPK ideal for frequent permission changes
```

------------------------------------------------------------------------

## 7.10 Page Fault Handling Flow

Now that we\'ve covered the different types of faults and exceptions,
let\'s examine how operating systems actually handle page faults from
start to finish. Understanding this flow ties together all the concepts
from previous sections.

### 7.10.1 Hardware Steps

When the MMU detects a fault condition, the hardware performs these
steps automatically:

**x86-64 Hardware Sequence:**

    1. Stop current instruction (before completion - precise exception)
    2. Save faulting virtual address → CR2
    3. Push error code onto kernel stack (32-bit value)
    4. If user mode: switch to kernel stack (load from TSS)
    5. Push SS, RSP, RFLAGS, CS, RIP onto kernel stack
    6. Clear IF flag (disable interrupts)
    7. Load CS:RIP from IDT entry 14 (page fault vector)
    8. Begin executing page fault handler

**ARM64 Hardware Sequence:**

    1. Stop current instruction
    2. Save faulting address → FAR_EL1
    3. Save exception syndrome → ESR_EL1
    4. Save return address → ELR_EL1
    5. Save processor state → SPSR_EL1
    6. Switch to EL1 (kernel mode)
    7. Disable interrupts (mask)
    8. Branch to exception vector (VBAR_EL1 + offset)
    9. Begin executing exception handler

**RISC-V Hardware Sequence:**

    1. Stop current instruction
    2. Save faulting address → stval
    3. Save exception cause → scause (12, 13, or 15)
    4. Save return PC → sepc
    5. Save privilege mode → sstatus.SPP
    6. Switch to S-mode
    7. Jump to address in stvec register
    8. Begin executing exception handler

### 7.10.2 Software Handler Entry

The OS page fault handler is the first software to run after the fault:

**Entry Point (Linux-style):**

``` {.sourceCode .c}
// x86-64 page fault entry point
asmlinkage void do_page_fault(struct pt_regs *regs, unsigned long error_code)
{
    unsigned long address = read_cr2();  // Get faulting address
    struct task_struct *tsk = current;
    struct mm_struct *mm = tsk->mm;
    struct vm_area_struct *vma;
    unsigned int flags = FAULT_FLAG_DEFAULT;
    
    // Quick checks before taking mm semaphore
    if (unlikely(address >= TASK_SIZE_MAX)) {
        // Kernel address space fault
        bad_area_nosemaphore(regs, error_code, address);
        return;
    }
    
    // Determine fault flags from error code
    if (error_code & X86_PF_WRITE)
        flags |= FAULT_FLAG_WRITE;
    if (error_code & X86_PF_USER)
        flags |= FAULT_FLAG_USER;
    if (error_code & X86_PF_INSTR)
        flags |= FAULT_FLAG_INSTRUCTION;
        
    // Continue to main handler...
    __do_page_fault(regs, error_code, address, mm, flags);
}

/* Based on Linux kernel arch/x86/mm/fault.c
   Reference: Linux kernel v6.5, do_page_fault() */
```

### 7.10.3 Finding the VMA (Virtual Memory Area)

The handler must determine if the faulting address is in a valid memory
region:

``` {.sourceCode .c}
// Find VMA containing address
struct vm_area_struct *find_vma(struct mm_struct *mm, unsigned long addr)
{
    struct vm_area_struct *vma = NULL;
    
    // Check cache first (last used VMA)
    vma = mm->mmap_cache;
    if (vma && vma->vm_start <= addr && vma->vm_end > addr)
        return vma;
    
    // Search red-black tree of VMAs
    struct rb_node *node = mm->mm_rb.rb_node;
    
    while (node) {
        vma = rb_entry(node, struct vm_area_struct, vm_rb);
        
        if (addr < vma->vm_start) {
            node = node->rb_left;
        } else if (addr >= vma->vm_end) {
            node = node->rb_right;
        } else {
            // Found it!
            mm->mmap_cache = vma;  // Update cache
            return vma;
        }
    }
    
    return NULL;  // No VMA found
}

/* Simplified from Linux kernel mm/mmap.c
   Reference: Linux kernel v6.5, find_vma() */
```

**VMA Structure:**

``` {.sourceCode .c}
struct vm_area_struct {
    unsigned long vm_start;      // Start address (inclusive)
    unsigned long vm_end;        // End address (exclusive)
    unsigned long vm_flags;      // Permissions: VM_READ, VM_WRITE, VM_EXEC
    
    struct file *vm_file;        // File backing (NULL for anonymous)
    unsigned long vm_pgoff;      // Offset in file (pages)
    
    struct mm_struct *vm_mm;     // Back pointer to mm
    struct vm_area_struct *vm_next;  // Linked list
    struct rb_node vm_rb;        // Red-black tree node
    
    struct vm_operations_struct *vm_ops;  // Operations
};
```

### 7.10.4 Permission Checking

Once a VMA is found, check if the access is allowed:

``` {.sourceCode .c}
bool check_vma_permissions(struct vm_area_struct *vma, unsigned long flags)
{
    // Check read permission
    if (!(flags & FAULT_FLAG_WRITE) && !(vma->vm_flags & VM_READ)) {
        return false;  // Read from non-readable VMA
    }
    
    // Check write permission
    if ((flags & FAULT_FLAG_WRITE) && !(vma->vm_flags & VM_WRITE)) {
        // Write to non-writable VMA
        // But might be COW - handler will check
        return false;
    }
    
    // Check execute permission
    if ((flags & FAULT_FLAG_INSTRUCTION) && !(vma->vm_flags & VM_EXEC)) {
        return false;  // Execute from non-executable VMA
    }
    
    return true;  // Access allowed by VMA
}
```

### 7.10.5 Demand Paging Implementation

If the page is not present but the VMA is valid, allocate and map it:

``` {.sourceCode .c}
// Handle demand paging (page not present, first access)
int handle_demand_paging(struct vm_area_struct *vma, unsigned long address,
                         unsigned int flags)
{
    struct page *page;
    pte_t *pte;
    
    // Step 1: Allocate physical page
    if (vma->vm_flags & VM_ZERO) {
        // Zero-filled page (BSS, heap, anonymous)
        page = alloc_zeroed_page(GFP_KERNEL);
    } else if (vma->vm_file) {
        // File-backed page - read from file
        page = alloc_page(GFP_KERNEL);
        read_page_from_file(vma->vm_file, page, address);
    } else {
        // Anonymous page
        page = alloc_page(GFP_KERNEL);
        clear_page(page);  // Zero for security
    }
    
    if (!page)
        return VM_FAULT_OOM;  // Out of memory
    
    // Step 2: Get PTE for this address
    pte = pte_alloc_map(vma->vm_mm, address);
    if (!pte) {
        free_page(page);
        return VM_FAULT_OOM;
    }
    
    // Step 3: Check if someone else filled it (race condition)
    if (!pte_none(*pte)) {
        // Another thread already filled this PTE
        free_page(page);
        pte_unmap(pte);
        return VM_FAULT_NOPAGE;
    }
    
    // Step 4: Set up PTE
    pte_t entry = mk_pte(page, vma->vm_page_prot);
    if (vma->vm_flags & VM_WRITE)
        entry = pte_mkwrite(entry);
    if (vma->vm_flags & VM_DIRTY)
        entry = pte_mkdirty(entry);
    
    // Step 5: Install PTE
    set_pte_at(vma->vm_mm, address, pte, entry);
    
    // Step 6: Update page tables and TLB
    pte_unmap(pte);
    update_mmu_cache(vma, address, pte);
    
    return VM_FAULT_MAJOR;  // Major fault (allocated new page)
}

/* Conceptual implementation based on Linux kernel mm/memory.c
   Reference: Linux kernel v6.5, do_anonymous_page() */
```

### 7.10.6 Copy-on-Write (COW) Implementation

COW is a special case where the page is present but read-only:

``` {.sourceCode .c}
// Handle Copy-on-Write fault
int handle_cow_fault(struct vm_area_struct *vma, unsigned long address,
                     pte_t *pte, pte_t orig_pte)
{
    struct page *old_page, *new_page;
    pte_t entry;
    
    // Step 1: Get the old (shared) page
    old_page = pte_page(orig_pte);
    
    // Step 2: Check if we're the only one using it
    if (page_mapcount(old_page) == 1) {
        // Fast path: We're the only user!
        // Just make it writable, no copy needed
        entry = pte_mkwrite(pte_mkdirty(orig_pte));
        set_pte_at(vma->vm_mm, address, pte, entry);
        update_mmu_cache(vma, address, pte);
        return VM_FAULT_WRITE;
    }
    
    // Step 3: Multiple users - must copy
    new_page = alloc_page(GFP_KERNEL);
    if (!new_page)
        return VM_FAULT_OOM;
    
    // Step 4: Copy page contents
    copy_user_highpage(new_page, old_page, address, vma);
    
    // Step 5: Create new PTE (writable)
    entry = mk_pte(new_page, vma->vm_page_prot);
    entry = pte_mkwrite(pte_mkdirty(entry));
    
    // Step 6: Install new PTE
    set_pte_at(vma->vm_mm, address, pte, entry);
    
    // Step 7: Decrease reference count on old page
    page_remove_rmap(old_page);
    put_page(old_page);
    
    // Step 8: Update TLB
    update_mmu_cache(vma, address, pte);
    
    return VM_FAULT_WRITE;  // COW handled
}

/* Based on Linux kernel mm/memory.c
   Reference: Linux kernel v6.5, do_wp_page() */
```

**COW Optimization - Reference Counting:**

``` {.sourceCode .c}
// Page reference counting for COW
struct page {
    atomic_t _refcount;      // Number of PTEs pointing to this page
    atomic_t _mapcount;      // Number of processes mapping this page
    // ...
};

// Check if page can be reused (no copy needed)
static inline bool can_reuse_page(struct page *page)
{
    // If only one PTE references this page, we can reuse it
    return page_mapcount(page) == 1;
}

// Fork example:
pid_t fork_with_cow(void) {
    pid_t pid = fork();
    
    // Kernel marks all pages as read-only and sets COW flag
    for_each_page(parent_mm) {
        pte_t *pte = get_pte(page);
        *pte = pte_wrprotect(*pte);  // Clear write bit
        page->_refcount++;             // Increment refcount
        page->_mapcount++;             // Increment mapcount
    }
    
    // First write by parent or child triggers COW
    // If _mapcount == 1: just make writable
    // If _mapcount > 1: allocate and copy
    
    return pid;
}
```

### 7.10.7 Stack Growth Handling

Stack faults are special - they might indicate legitimate stack growth:

``` {.sourceCode .c}
// Check if fault is due to stack growth
bool is_stack_growth(struct vm_area_struct *vma, unsigned long address,
                     unsigned long sp)
{
    // Must be a stack VMA
    if (!(vma->vm_flags & VM_GROWSDOWN))
        return false;
    
    // Address must be just below current stack pointer
    // But not too far (prevent abuse)
    unsigned long distance = sp - address;
    
    if (distance > 65536)  // More than 64KB below SP
        return false;      // Likely stack overflow, not growth
    
    return true;
}

// Expand stack VMA
int expand_stack(struct vm_area_struct *vma, unsigned long address)
{
    unsigned long grow_size, new_start;
    
    // Round down to page boundary
    new_start = address & PAGE_MASK;
    grow_size = vma->vm_start - new_start;
    
    // Check against stack limit (RLIMIT_STACK)
    if (vma->vm_mm->total_vm + (grow_size >> PAGE_SHIFT) > 
        rlimit(RLIMIT_STACK) >> PAGE_SHIFT) {
        return -ENOMEM;  // Would exceed limit
    }
    
    // Expand VMA downward
    vma->vm_start = new_start;
    vma->vm_mm->total_vm += grow_size >> PAGE_SHIFT;
    
    return 0;
}

/* Based on Linux kernel mm/mmap.c
   Reference: Linux kernel v6.5, expand_stack() */
```

### 7.10.8 Complete Page Fault Handler

Putting it all together - the full handler flow:

``` {.sourceCode .c}
// Main page fault handler
static vm_fault_t __handle_mm_fault(struct vm_area_struct *vma,
                                    unsigned long address,
                                    unsigned int flags)
{
    struct mm_struct *mm = vma->vm_mm;
    pte_t *pte;
    pte_t orig_pte;
    
    // Step 1: Walk page tables to get PTE
    pte = pte_offset_map(mm->pgd, address);
    if (!pte)
        return VM_FAULT_OOM;
    
    orig_pte = *pte;
    
    // Step 2: Check if PTE is empty (not present)
    if (pte_none(orig_pte)) {
        // Not present - demand paging
        pte_unmap(pte);
        return handle_demand_paging(vma, address, flags);
    }
    
    // Step 3: Check if present
    if (!pte_present(orig_pte)) {
        // Not present but PTE not empty - might be swapped
        pte_unmap(pte);
        return handle_swap_fault(vma, address, orig_pte);
    }
    
    // Step 4: Page is present - check for COW
    if ((flags & FAULT_FLAG_WRITE) && !pte_write(orig_pte)) {
        // Write to read-only page - might be COW
        return handle_cow_fault(vma, address, pte, orig_pte);
    }
    
    // Step 5: Access flag handling
    if (!pte_young(orig_pte)) {
        // First access - set accessed bit
        orig_pte = pte_mkyoung(orig_pte);
        set_pte_at(mm, address, pte, orig_pte);
    }
    
    // Step 6: Dirty bit handling (for writes)
    if ((flags & FAULT_FLAG_WRITE) && !pte_dirty(orig_pte)) {
        orig_pte = pte_mkdirty(orig_pte);
        set_pte_at(mm, address, pte, orig_pte);
    }
    
    pte_unmap(pte);
    update_mmu_cache(vma, address, pte);
    
    return VM_FAULT_NOPAGE;  // Minor fault (PTE updated)
}

/* Simplified from Linux kernel mm/memory.c
   Reference: Linux kernel v6.5, handle_pte_fault() */
```

### 7.10.9 Swap Handling

If the page is swapped to disk, bring it back:

``` {.sourceCode .c}
// Handle page that was swapped out
int handle_swap_fault(struct vm_area_struct *vma, unsigned long address,
                      pte_t orig_pte)
{
    swp_entry_t entry;
    struct page *page;
    pte_t pte;
    
    // Step 1: Extract swap entry from PTE
    // PTE format when swapped: {swap type, swap offset, not present}
    entry = pte_to_swp_entry(orig_pte);
    
    // Step 2: Look up page in swap cache
    page = lookup_swap_cache(entry);
    
    if (!page) {
        // Step 3: Not in cache - must read from disk
        page = alloc_page(GFP_KERNEL);
        if (!page)
            return VM_FAULT_OOM;
        
        // Step 4: Read page from swap device (SLOW!)
        // This is what makes it a "major" page fault
        if (swap_readpage(page, entry) < 0) {
            free_page(page);
            return VM_FAULT_SIGBUS;
        }
    }
    
    // Step 5: Remove from swap (we now have it in RAM)
    swap_free(entry);
    
    // Step 6: Install PTE with present bit set
    pte = mk_pte(page, vma->vm_page_prot);
    if (vma->vm_flags & VM_WRITE)
        pte = pte_mkwrite(pte);
    
    set_pte_at(vma->vm_mm, address, get_pte(address), pte);
    update_mmu_cache(vma, address, get_pte(address));
    
    return VM_FAULT_MAJOR;  // Major fault (disk I/O)
}

/* Based on Linux kernel mm/memory.c
   Reference: Linux kernel v6.5, do_swap_page() */
```

### 7.10.10 Returning from Page Fault

After handling the fault, return to hardware to retry:

``` {.sourceCode .c}
// x86-64: Return from page fault
void return_from_page_fault(struct pt_regs *regs)
{
    // Restore registers from stack
    // Execute IRET instruction
    // CPU will:
    //   1. Pop RIP, CS, RFLAGS, RSP, SS from stack
    //   2. Restore privilege level
    //   3. Resume at faulting instruction
    //   4. Retry the instruction (will now succeed)
    
    iret();
}

// ARM64: Return from exception
void return_from_exception_arm64(void)
{
    // Execute ERET instruction
    // CPU will:
    //   1. Restore PC from ELR_EL1
    //   2. Restore processor state from SPSR_EL1
    //   3. Return to exception level from SPSR_EL1
    //   4. Resume execution
    
    asm volatile("eret");
}

// RISC-V: Return from trap
void return_from_trap_riscv(void)
{
    // Execute SRET instruction
    // CPU will:
    //   1. Restore PC from sepc
    //   2. Restore privilege mode from sstatus.SPP
    //   3. Resume execution
    
    asm volatile("sret");
}
```

**Critical: Instruction Must Be Restartable**

``` {.sourceCode .c}
// Example: Load instruction that caused page fault
// Before fault:
ld r1, 0(r2)    // PC = 0x1000, r2 = 0x80000000 (not present)

// Fault occurs:
// - sepc saved = 0x1000 (address of faulting instruction)
// - stval saved = 0x80000000 (faulting address)

// Handler allocates page, updates PTE

// Return from handler:
// - PC restored to 0x1000
// - Instruction re-executed: ld r1, 0(r2)
// - Now succeeds (page present)
// - PC advances to 0x1004 (next instruction)
```

------------------------------------------------------------------------

Now that we understand when and why page faults occur, let\'s examine
how operating systems handle them. The page fault handler is one of the
most critical and frequently executed pieces of OS code.

### 7.10.1 Hardware Steps (Architecture-Independent)

Before software can handle a page fault, the hardware must detect and
report it. This sequence is remarkably similar across architectures:

**Step 1: Fault Detection** - MMU detects fault condition during address
translation - Could be: Present=0, permission violation, reserved bit
set, etc.

**Step 2: Stop Instruction** - CPU stops the faulting instruction
**before** it completes - Critical for restartability---instruction can
be retried after fix - All previous instructions in program order have
completed

**Step 3: Save Context** - Save processor state (registers, flags) -
Save faulting address (CR2 on x86, FAR_EL1 on ARM, stval on RISC-V) -
Save error information (error code, ESR, scause) - Save faulting
instruction address (EIP/RIP, ELR, sepc)

**Step 4: Mode Switch** - Switch to supervisor mode (ring 0, EL1,
S-mode) - Switch to kernel stack - Disable interrupts (usually)

**Step 5: Vector to Handler** - x86-64: Jump to IDT entry 14 (page fault
vector) - ARM64: Jump to vector table entry for Data/Instruction Abort -
RISC-V: Jump to address in stvec register

**Step 6: Push Additional Context (x86-64)** - x86 pushes: error code,
CS, RIP, RFLAGS, SS, RSP

### 7.10.2 Software Handler Steps

Once in the page fault handler, the OS must diagnose and handle the
fault:

**Step 1: Extract Fault Information**

``` {.sourceCode .c}
void page_fault_handler(struct pt_regs *regs) {
    unsigned long fault_addr;
    unsigned long error_code;
    
    // Architecture-specific extraction
    #ifdef x86_64
        fault_addr = read_cr2();
        error_code = regs->error_code;
    #elif ARM64
        fault_addr = read_sysreg(far_el1);
        error_code = read_sysreg(esr_el1);
    #elif RISCV
        fault_addr = csr_read(CSR_STVAL);
        error_code = csr_read(CSR_SCAUSE);
    #endif
    
    handle_fault(fault_addr, error_code, regs);
}
```

**Step 2: Determine Fault Type**

``` {.sourceCode .c}
enum fault_type {
    FAULT_TYPE_NOT_PRESENT,    // Demand paging, swap
    FAULT_TYPE_PROTECTION,     // Write to RO, execute from NX
    FAULT_TYPE_ACCESS_FLAG,    // First access (ARM)
    FAULT_TYPE_INVALID,        // Not mapped, bad access
};

enum fault_type classify_fault(unsigned long addr, unsigned long error_code) {
    // Check if address is mapped
    struct vm_area_struct *vma = find_vma(current->mm, addr);
    
    if (!vma || vma->vm_start > addr) {
        return FAULT_TYPE_INVALID;  // Not mapped
    }
    
    // Check error code
    #ifdef x86_64
        if (!(error_code & 0x1)) {
            // P = 0: Not present
            return FAULT_TYPE_NOT_PRESENT;
        }
        // P = 1: Protection violation
        return FAULT_TYPE_PROTECTION;
    #endif
    
    // Similar logic for ARM64, RISC-V...
}
```

**Step 3: Validate Access**

``` {.sourceCode .c}
bool validate_access(struct vm_area_struct *vma, unsigned long error_code) {
    // Check if access type is allowed by VMA
    
    if (is_write_access(error_code)) {
        if (!(vma->vm_flags & VM_WRITE)) {
            return false;  // Write to non-writable VMA
        }
    }
    
    if (is_exec_access(error_code)) {
        if (!(vma->vm_flags & VM_EXEC)) {
            return false;  // Execute from non-executable VMA
        }
    }
    
    if (is_user_mode(error_code)) {
        if (!(vma->vm_flags & VM_READ)) {
            return false;  // User read from non-readable VMA
        }
    }
    
    return true;  // Access is valid
}
```

**Step 4: Handle the Fault**

This is where the real work happens---allocate pages, swap in, or
terminate.

### 7.10.3 Demand Paging Implementation

Demand paging allocates physical pages only when first accessed:

``` {.sourceCode .c}
// Demand paging: Allocate page on first access
int handle_demand_paging(struct vm_area_struct *vma, unsigned long addr) {
    struct page *page;
    pte_t *pte;
    
    // Step 1: Allocate physical page
    page = alloc_page(GFP_HIGHUSER_MOVABLE);
    if (!page) {
        return VM_FAULT_OOM;  // Out of memory
    }
    
    // Step 2: Zero the page (security: prevent info leak)
    void *kaddr = kmap_atomic(page);
    memset(kaddr, 0, PAGE_SIZE);
    kunmap_atomic(kaddr);
    
    // Step 3: Get PTE for faulting address
    pte = pte_alloc_map(vma->vm_mm, addr);
    if (!pte) {
        __free_page(page);
        return VM_FAULT_OOM;
    }
    
    // Step 4: Set up PTE
    pte_t entry = mk_pte(page, vma->vm_page_prot);
    entry = pte_mkdirty(entry);   // Mark dirty
    entry = pte_mkyoung(entry);   // Mark accessed
    
    // Step 5: Install PTE
    set_pte_at(vma->vm_mm, addr, pte, entry);
    
    // Step 6: Update page structures
    page_add_new_anon_rmap(page, vma, addr);
    lru_cache_add_active_or_unevictable(page, vma);
    
    // Step 7: Flush TLB
    flush_tlb_page(vma, addr);
    
    return VM_FAULT_NOPAGE;  // Success
}

/* Based on Linux kernel mm/memory.c
   Reference: Linux kernel v6.5, do_anonymous_page() */
```

**Why Zero the Page?**

``` {.sourceCode .c}
// Security issue if we don't zero:
// 1. Process A allocates page, writes sensitive data
// 2. Process A exits, page freed
// 3. Process B allocates same physical page
// 4. Process B can read Process A's old data!
//
// Solution: Always zero pages before giving to new process

// Performance optimization: Use "zero page" for read-only
// Many processes read from zero-initialized memory
// Can share single zero page, copy-on-write when written
```

### 7.10.4 Copy-on-Write (COW) Implementation

COW is a critical optimization for `fork()`:

``` {.sourceCode .c}
// COW fault handler
int handle_cow_fault(struct vm_area_struct *vma, unsigned long addr,
                     pte_t *pte, pte_t orig_pte) {
    struct page *old_page, *new_page;
    pte_t entry;
    
    // Step 1: Get the current (shared) page
    old_page = vm_normal_page(vma, addr, orig_pte);
    if (!old_page) {
        return VM_FAULT_OOM;
    }
    
    // Step 2: Check reference count
    if (page_mapcount(old_page) == 1) {
        // We're the only one using this page!
        // No need to copy—just make it writable
        entry = pte_mkyoung(orig_pte);
        entry = maybe_mkwrite(pte_mkdirty(entry), vma);
        
        if (ptep_set_access_flags(vma, addr, pte, entry, 1)) {
            update_mmu_cache(vma, addr, pte);
        }
        
        return VM_FAULT_WRITE;  // Fast path!
    }
    
    // Step 3: Others are using it—must copy
    new_page = alloc_page_vma(GFP_HIGHUSER_MOVABLE, vma, addr);
    if (!new_page) {
        return VM_FAULT_OOM;
    }
    
    // Step 4: Copy old page to new page
    copy_user_highpage(new_page, old_page, addr, vma);
    
    // Step 5: Make new PTE (writable)
    entry = mk_pte(new_page, vma->vm_page_prot);
    entry = pte_mkdirty(entry);
    entry = pte_mkyoung(entry);
    entry = maybe_mkwrite(entry, vma);
    
    // Step 6: Install new PTE
    ptep_clear_flush(vma, addr, pte);
    set_pte_at_notify(vma->vm_mm, addr, pte, entry);
    
    // Step 7: Update page accounting
    page_remove_rmap(old_page);   // Remove old mapping
    page_add_new_anon_rmap(new_page, vma, addr);  // Add new mapping
    lru_cache_add_active_or_unevictable(new_page, vma);
    
    // Step 8: Release old page
    put_page(old_page);
    
    return VM_FAULT_WRITE;  // Success
}

/* Based on Linux kernel mm/memory.c
   Reference: Linux kernel v6.5, do_wp_page() */
```

**COW Performance:**

``` {.sourceCode .c}
// Benchmark: fork() + immediate write to 1000 pages

// Without COW (copy all pages at fork time):
//   1000 pages * 4KB = 4MB to copy
//   At 10 GB/s: 400 microseconds just to copy
//   Plus page table setup: ~100 microseconds
//   Total: ~500 microseconds

// With COW:
//   fork(): Just copy page tables: ~100 microseconds
//   First write to each page: 1000 faults
//   Each fault: ~2 microseconds
//   Total: 100 + 2000 = 2100 microseconds
//
// Wait, that's slower! But:
// - Most pages never written by child (if exec() called)
// - Many pages written by only one process (fast path)
// - Reality: COW saves 70-90% of copy overhead for typical workloads
```

### 7.10.5 Swap-In (Major Page Fault)

When a page has been swapped to disk, we need a major page fault:

``` {.sourceCode .c}
// Swap-in handler
int handle_swap_fault(struct vm_area_struct *vma, unsigned long addr,
                      pte_t *pte, pte_t orig_pte) {
    swp_entry_t entry;
    struct page *page;
    
    // Step 1: Extract swap entry from PTE
    entry = pte_to_swp_entry(orig_pte);
    
    // Step 2: Look up in swap cache (may be in memory already)
    page = lookup_swap_cache(entry);
    if (!page) {
        // Not in cache—must read from disk
        // This is expensive: ~1-10 milliseconds!
        page = read_swap_cache_async(entry, GFP_HIGHUSER_MOVABLE,
                                      vma, addr);
        if (!page) {
            return VM_FAULT_OOM;
        }
    }
    
    // Step 3: Wait for I/O to complete (if still reading)
    lock_page(page);
    
    // Step 4: Verify page is still valid
    if (unlikely(!PageSwapCache(page))) {
        // Race: someone else brought it in
        unlock_page(page);
        put_page(page);
        return VM_FAULT_RETRY;
    }
    
    // Step 5: Install PTE
    pte_t new_pte = mk_pte(page, vma->vm_page_prot);
    new_pte = pte_mkdirty(new_pte);  // Swapped pages are dirty
    
    set_pte_at(vma->vm_mm, addr, pte, new_pte);
    
    // Step 6: Update page accounting
    page_add_anon_rmap(page, vma, addr);
    swap_free(entry);  // Free swap space
    
    // Step 7: Unlock and activate
    unlock_page(page);
    lru_cache_add_active_or_unevictable(page, vma);
    
    return VM_FAULT_MAJOR;  // Major fault (disk I/O occurred)
}

/* Simplified from Linux kernel mm/memory.c
   Reference: Linux kernel v6.5, do_swap_page() */
```

### 7.10.6 Stack Growth

Automatically expanding the stack when it grows:

``` {.sourceCode .c}
// Stack growth handler
int expand_stack(struct vm_area_struct *vma, unsigned long address) {
    unsigned long size, grow;
    struct mm_struct *mm = vma->vm_mm;
    
    // Step 1: Check if this is a valid stack expansion
    if (!(vma->vm_flags & VM_GROWSDOWN)) {
        return -EFAULT;  // Not a growable stack
    }
    
    // Step 2: Check stack size limits
    size = vma->vm_end - address;
    grow = (vma->vm_start - address) >> PAGE_SHIFT;
    
    // Check against RLIMIT_STACK
    if (size > rlimit(RLIMIT_STACK)) {
        return -ENOMEM;  // Stack too large
    }
    
    // Step 3: Check if we have enough memory
    if (security_vm_enough_memory_mm(mm, grow)) {
        return -ENOMEM;
    }
    
    // Step 4: Expand the VMA
    vma->vm_start = address;
    vma->vm_pgoff -= grow;
    
    // Step 5: Update memory accounting
    mm->total_vm += grow;
    
    return 0;  // Success - page fault will be handled normally now
}

/* Based on Linux kernel mm/mmap.c
   Reference: Linux kernel v6.5, expand_downwards() */
```

**Stack Growth Example:**

``` {.sourceCode .c}
void recursive_function(int depth) {
    char buffer[4096];  // 4KB per call
    
    // First call: stack at 0x7fff00000000
    // Second call: needs 0x7fffffff000 - stack VMA needs to grow
    //   → Page fault at 0x7ffeffff000
    //   → Handler checks: within RLIMIT_STACK?
    //   → Handler expands VMA: vm_start = 0x7ffeffff000
    //   → Handler allocates page
    //   → Retry succeeds
    
    recursive_function(depth + 1);
}
```

### 7.10.7 Invalid Fault Handling

When a fault cannot be handled, terminate the process:

``` {.sourceCode .c}
// Invalid fault—send SIGSEGV
void handle_invalid_fault(struct pt_regs *regs, unsigned long addr,
                          unsigned long error_code) {
    struct task_struct *tsk = current;
    
    // Print diagnostic information
    printk("Segmentation fault at address %lx\n", addr);
    printk("  IP: %lx\n", instruction_pointer(regs));
    printk("  Error code: %lx\n", error_code);
    
    // Set up signal info
    struct siginfo si;
    memset(&si, 0, sizeof(si));
    si.si_signo = SIGSEGV;
    si.si_addr = (void __user *)addr;
    
    // Determine si_code (why SIGSEGV)
    if (error_code & 0x4) {
        // User mode fault
        if (!(error_code & 0x1)) {
            si.si_code = SEGV_MAPERR;  // Address not mapped
        } else {
            si.si_code = SEGV_ACCERR;  // Permission denied
        }
    } else {
        // Kernel mode fault - this is serious
        printk("Kernel page fault at %lx\n", addr);
        show_regs(regs);
        die("Oops", regs, error_code);
    }
    
    // Send signal to process
    force_sig_info(SIGSEGV, &si, tsk);
}
```

### 7.10.8 Complete Page Fault Handler (Integrated)

Putting it all together:

``` {.sourceCode .c}
// Complete page fault handler
void do_page_fault(struct pt_regs *regs, unsigned long error_code) {
    unsigned long address = read_fault_address();  // CR2, FAR, stval
    struct mm_struct *mm = current->mm;
    struct vm_area_struct *vma;
    unsigned int flags = FAULT_FLAG_DEFAULT;
    int fault;
    
    // Determine fault flags
    if (error_code & ERR_WRITE) flags |= FAULT_FLAG_WRITE;
    if (error_code & ERR_USER)  flags |= FAULT_FLAG_USER;
    if (error_code & ERR_INSTR) flags |= FAULT_FLAG_INSTRUCTION;
    
    // Handle kernel faults
    if (!(error_code & ERR_USER)) {
        handle_kernel_fault(address, error_code, regs);
        return;
    }
    
    // Acquire mm semaphore (protects VMA list)
    down_read(&mm->mmap_lock);
    
    // Find VMA containing faulting address
    vma = find_vma(mm, address);
    if (!vma || vma->vm_start > address) {
        goto bad_area;
    }
    
    // Check for stack growth
    if (vma->vm_flags & VM_GROWSDOWN) {
        if (expand_stack(vma, address) < 0) {
            goto bad_area;
        }
    }
    
    // Validate access permissions
    if (!validate_access(vma, error_code)) {
        goto bad_area;
    }
    
    // Handle the fault
    fault = handle_mm_fault(vma, address, flags, regs);
    
    // Check result
    if (fault & VM_FAULT_ERROR) {
        if (fault & VM_FAULT_OOM) {
            goto out_of_memory;
        } else if (fault & VM_FAULT_SIGSEGV) {
            goto bad_area;
        } else if (fault & VM_FAULT_SIGBUS) {
            goto sigbus;
        }
        BUG();
    }
    
    // Success
    up_read(&mm->mmap_lock);
    return;
    
bad_area:
    up_read(&mm->mmap_lock);
    handle_invalid_fault(regs, address, error_code);
    return;
    
out_of_memory:
    up_read(&mm->mmap_lock);
    pagefault_out_of_memory();
    return;
    
sigbus:
    up_read(&mm->mmap_lock);
    force_sig(SIGBUS, current);
    return;
}

/* Conceptual integration of Linux kernel page fault handler
   Reference: Linux kernel arch/x86/mm/fault.c, mm/memory.c */
```

------------------------------------------------------------------------

## 7.11 Performance Implications

Page faults are expensive. Understanding their performance impact is
crucial for writing efficient systems software and diagnosing
performance problems.

### 7.11.1 Page Fault Cost Breakdown

Let\'s quantify the cost of different page fault types on a modern
x86-64 system (Intel Core i9, 3.0 GHz):

**Minor Page Fault (page in memory):**

    1. Trap to kernel:              ~100 cycles (30 ns)
    2. Context save:                ~50 cycles (15 ns)
    3. Walk page tables:            ~100 cycles (30 ns) [if not in cache]
    4. Allocate page:               ~500 cycles (150 ns)
    5. Zero page:                   ~3000 cycles (1 µs) [4KB @ 12 GB/s]
    6. Update PTE:                  ~50 cycles (15 ns)
    7. TLB flush:                   ~20 cycles (6 ns)
    8. Context restore:             ~50 cycles (15 ns)
    9. Return to user:              ~100 cycles (30 ns)

    Total: ~4,000 cycles ≈ 1.3 microseconds

**Major Page Fault (swap from SSD):**

    Minor fault overhead:           1.3 µs
    + SSD read latency:             ~100 µs (typical NVMe)
    + DMA setup:                    ~5 µs
    + Data transfer:                ~0.4 µs (4KB @ 10 GB/s)

    Total: ~107 microseconds ≈ 100× slower than minor fault

**Major Page Fault (swap from HDD):**

    Minor fault overhead:           1.3 µs
    + HDD seek time:                ~5-10 ms (average)
    + Rotational delay:             ~4 ms (7200 RPM)
    + Transfer time:                ~0.05 ms

    Total: ~10 milliseconds ≈ 10,000× slower than minor fault!

### 7.11.2 Page Fault Rate Impact

Even a low page fault rate can severely impact performance:

``` {.sourceCode .c}
// Calculate effective memory access time

double effective_access_time(double mem_access_ns,
                              double pf_service_us,
                              double pf_rate) {
    double pf_service_ns = pf_service_us * 1000;
    
    // EAT = (1 - p) * mem_access + p * pf_service
    return (1.0 - pf_rate) * mem_access_ns + pf_rate * pf_service_ns;
}

// Example 1: Good performance
// Memory access: 100 ns
// Page fault service: 1.3 µs = 1,300 ns
// Page fault rate: 0.001% (1 in 100,000 accesses)

double eat1 = effective_access_time(100, 1.3, 0.00001);
// EAT = 0.99999 * 100 + 0.00001 * 1300
//     = 99.999 + 0.013 = 100.012 ns
// Overhead: 0.012% (negligible)

// Example 2: Moderate paging
// Page fault rate: 0.1% (1 in 1,000)

double eat2 = effective_access_time(100, 1.3, 0.001);
// EAT = 0.999 * 100 + 0.001 * 1300
//     = 99.9 + 1.3 = 101.2 ns
// Overhead: 1.2% (noticeable)

// Example 3: Heavy paging (thrashing)
// Page fault rate: 1% (1 in 100)

double eat3 = effective_access_time(100, 1.3, 0.01);
// EAT = 0.99 * 100 + 0.01 * 1300
//     = 99 + 13 = 112 ns
// Overhead: 12% (severe performance degradation)

// Example 4: Thrashing with disk I/O
// Page fault rate: 1%
// Page fault service: 100 µs = 100,000 ns

double eat4 = effective_access_time(100, 100, 0.01);
// EAT = 0.99 * 100 + 0.01 * 100000
//     = 99 + 1000 = 1099 ns
// Overhead: 999% (10× slower!)
```

### 7.11.3 Real-World Page Fault Profiling

Use `perf` to measure page faults in production:

``` {.sourceCode .bash}
# Count page faults for a program
$ perf stat -e page-faults,minor-faults,major-faults ./my_program

 Performance counter stats for './my_program':

         1,234,567      page-faults
         1,234,500      minor-faults
                67      major-faults

       2.543210987 seconds time elapsed
```

**Interpreting the Results:**

``` {.sourceCode .c}
// 1,234,567 total page faults in 2.54 seconds
double pf_rate = 1234567 / 2.54;
// = 485,971 faults/second

// If program makes 1 billion memory accesses per second:
double access_rate = 1e9;
double pf_percentage = (pf_rate / access_rate) * 100;
// = 0.0486% page fault rate

// Minor faults: 1,234,500 @ 1.3 µs each
double minor_overhead = 1234500 * 1.3e-6;
// = 1.605 seconds spent in minor page faults

// Major faults: 67 @ 100 µs each (SSD)
double major_overhead = 67 * 100e-6;
// = 0.0067 seconds spent in major page faults

// Total overhead: 1.612 seconds out of 2.54 seconds
double overhead_pct = (1.612 / 2.54) * 100;
// = 63.5% of time spent handling page faults!
// This program is page-fault-bound!
```

### 7.11.4 Reducing Page Faults

**Strategy 1: Increase Physical Memory**

    Problem: Working set > Physical RAM
      Example: 16 GB RAM, 20 GB working set
      Result: Constant swapping, major faults

    Solution: Add more RAM
      Add 16 GB → 32 GB total
      Result: Working set fits in RAM, only minor faults
      
    Cost/benefit:
      RAM cost: $100-200
      Performance improvement: 10-100× for page-fault-bound workloads

**Strategy 2: Use Huge Pages**

``` {.sourceCode .c}
// Standard 4KB pages
// Access pattern: Touch 1 byte per page across 1GB
// Pages touched: 1GB / 4KB = 262,144 pages
// TLB entries needed: 262,144
// TLB capacity: ~1,500 entries
// TLB miss rate: ~99.4%
// Cost: 262,000 page table walks + 262,000 TLB refills

// With 2MB huge pages
// Access pattern: Same 1GB
// Pages touched: 1GB / 2MB = 512 pages
// TLB entries needed: 512
// TLB capacity: ~1,500 entries
// TLB miss rate: ~0% (all fit!)
// Cost: 512 page table walks initially

// Result: 500× fewer TLB misses!

// Enable huge pages in Linux
madvise(ptr, size, MADV_HUGEPAGE);
// or
mmap(... | MAP_HUGETLB ...);
```

**Strategy 3: Prefaulting**

``` {.sourceCode .c}
// Prefault pages before they're needed
void prefault_pages(void *addr, size_t len) {
    volatile char *ptr = (char *)addr;
    size_t page_size = sysconf(_SC_PAGESIZE);
    
    // Touch each page to trigger page fault NOW
    // rather than during critical path
    for (size_t i = 0; i < len; i += page_size) {
        ptr[i] = ptr[i];  // Read and write back
    }
}

// Use case: Allocate large buffer before performance-critical section
void *buffer = mmap(NULL, 1<<30, PROT_READ|PROT_WRITE,
                    MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);

// Without prefaulting:
//   First access to each page during workload causes fault
//   Unpredictable latency spikes

// With prefaulting:
prefault_pages(buffer, 1<<30);
//   All faults happen upfront
//   Predictable latency during workload
```

**Strategy 4: Working Set Optimization**

``` {.sourceCode .c}
// Bad: Large working set, poor locality
void process_data_bad(int *data, size_t n) {
    // Access pattern jumps around unpredictably
    for (size_t i = 0; i < n; i++) {
        size_t random_idx = rand() % n;
        data[random_idx] += 1;  // Random access
    }
}

// Good: Smaller working set, good locality
void process_data_good(int *data, size_t n) {
    // Process in sequential chunks
    size_t chunk_size = 1 << 20;  // 1MB chunks
    
    for (size_t start = 0; start < n; start += chunk_size) {
        size_t end = min(start + chunk_size, n);
        
        // Work on this chunk (good locality)
        for (size_t i = start; i < end; i++) {
            data[i] += 1;
        }
    }
}

// Result:
// Bad: Touches all pages constantly, high page fault rate
// Good: Works on subset of pages, then moves to next subset
//       Much better cache and TLB behavior
```

### 7.11.5 Page Fault Performance Anti-Patterns

**Anti-Pattern 1: Fork Bomb**

``` {.sourceCode .c}
// Creates exponential number of processes
void fork_bomb(void) {
    while (1) {
        fork();  // Each child also forks
    }
}

// Result:
// - Exponential process creation
// - Each fork() causes COW page faults
// - System spends all time in page fault handler
// - System becomes unresponsive
// - OOM killer eventually intervenes

// Mitigation:
// - Process limits (ulimit -u)
// - Cgroups memory controller
// - Early OOM detection
```

**Anti-Pattern 2: Memory Thrashing**

``` {.sourceCode .c}
// Working set > RAM, constantly swapping
void thrashing_example(void) {
    size_t ram_size = 16UL << 30;      // 16 GB
    size_t alloc_size = 20UL << 30;    // 20 GB (more than RAM!)
    
    char *data = malloc(alloc_size);
    
    // Access all of it in a loop
    while (1) {
        for (size_t i = 0; i < alloc_size; i += 4096) {
            data[i] = 0;  // Touch each page
        }
    }
    
    // Result:
    // - Constantly swapping pages in and out
    // - Major page faults every iteration
    // - CPU mostly idle waiting for disk I/O
    // - "Swap thrashing"
}

// Solution:
// - Reduce working set to fit in RAM
// - Add more RAM
// - Use mmap() and madvise(MADV_SEQUENTIAL)
```

**Anti-Pattern 3: Excessive COW**

``` {.sourceCode .c}
// Fork many children, all write to memory
void excessive_cow(void) {
    // Parent allocates large buffer
    size_t size = 1UL << 30;  // 1 GB
    char *buf = malloc(size);
    memset(buf, 0, size);
    
    // Fork 100 children
    for (int i = 0; i < 100; i++) {
        if (fork() == 0) {
            // Child writes to buffer
            // Causes COW fault on EVERY PAGE
            for (size_t j = 0; j < size; j++) {
                buf[j] = i;  // 262,144 COW faults per child!
            }
            exit(0);
        }
    }
    
    // Result:
    // - 262,144 pages * 100 children = 26 million COW faults
    // - At 2 µs per fault = 52 seconds just in COW overhead!
}

// Solution:
// - Use shared memory (if appropriate)
// - Allocate memory after fork() in children
// - Use vfork() for fork-exec pattern
```

### 7.11.6 Page Fault Performance Monitoring

**Linux: /proc/\[pid\]/stat**

``` {.sourceCode .bash}
$ cat /proc/self/stat | awk '{print "Minor faults: " $10 "\nMajor faults: " $12}'
Minor faults: 1234
Major faults: 5
```

**Per-process page fault tracking:**

``` {.sourceCode .c}
#include <sys/resource.h>

void print_page_fault_stats(void) {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    
    printf("Minor page faults: %ld\n", usage.ru_minflt);
    printf("Major page faults: %ld\n", usage.ru_majflt);
    
    // Also available:
    // ru_maxrss: Maximum resident set size (KB)
    // ru_ixrss: Integral shared memory size
    // ru_idrss: Integral unshared data size
    // ru_isrss: Integral unshared stack size
}
```

**System-wide monitoring:**

``` {.sourceCode .bash}
# Watch page fault rate system-wide
$ vmstat 1

procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2  0      0 8234156 234856 4567888    0    0   156    89  234  567 12  3 84  1  0
 1  0      0 8234156 234856 4567888    0    0    45    12  189  432 10  2 87  1  0

# si/so: swap in/out (pages/sec) - major faults
# Anything > 0 indicates swapping

# High major fault rate example:
$ vmstat 1
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 1  5      0 234156  23485 567888  4567 3456  5678 4567 1234 5678  5 10 30 55  0
           ^^^ High swap in/out ^^^
                                            ^^^ High wait % ^^^
# System is thrashing!
```

------------------------------------------------------------------------

## 7.12 Historical Architectures: SPARC, MIPS, PowerPC

Understanding how historical architectures handled page faults provides
valuable context for modern designs. These architectures pioneered many
concepts still used today, while also revealing evolutionary dead-ends.

### 7.12.1 SPARC Architecture (Sun Microsystems)

SPARC (Scalable Processor Architecture) used software-managed TLB,
predating RISC-V\'s approach by decades.

**SPARC MMU Architecture:**

    - Software-managed TLB (like RISC-V)
    - Context register (8-bit ASID equivalent)
    - Reference/Modified bits in page tables
    - 3-level page table structure
    - Trap-based exception handling

**SPARC Trap Types for MMU:**

    Trap 0x09: Instruction Access Exception
      - Instruction fetch from invalid/protected page
      - Similar to: RISC-V exception 12, ARM Instruction Abort

    Trap 0x0C: Instruction Access MMU Miss
      - TLB miss on instruction fetch
      - Software must walk page tables
      - Similar to: RISC-V's approach (all TLB misses are exceptions)

    Trap 0x29: Data Access Exception
      - Load/store to invalid/protected page
      - Permission violation
      - Similar to: RISC-V exception 13/15, ARM Data Abort

    Trap 0x2C: Data Access MMU Miss
      - TLB miss on data access
      - Software page table walk required

**SPARC TLB Management:**

``` {.sourceCode .c}
// SPARC TLB entry structure
struct sparc_tlb_entry {
    uint32_t virtual_tag;    // Virtual page number
    uint8_t  context;        // 8-bit context (like ASID)
    uint32_t physical;       // Physical page number
    uint8_t  acc;            // Access control (8 levels!)
    uint8_t  cacheable;      // Cache control bits
};

// SPARC MMU miss handler (simplified)
void sparc_mmu_miss_handler(uint32_t fault_addr, uint8_t context) {
    uint32_t vpn = fault_addr >> 12;
    
    // Walk page tables (software)
    pte_t *pte = walk_sparc_page_table(vpn, context);
    
    if (!pte || !(*pte & PTE_VALID)) {
        // True page fault - invoke OS handler
        handle_sparc_page_fault(fault_addr, context);
        return;
    }
    
    // Load TLB entry (architecture-specific instruction)
    load_sparc_tlb(fault_addr, context, *pte);
    
    // Return - instruction will retry
}
```

**SPARC Page Protection (8 Levels):**

Unlike modern 3-bit R/W/X, SPARC had 8 protection levels:

    ACC bits (3-bit):
    000: No access (invalid)
    001: Read-only, user
    010: Read/write, user
    011: Read/execute, user
    100: Execute-only, user
    101: Read-only, supervisor
    110: Read/write, supervisor
    111: Read/write/execute, supervisor

**SPARC Context Register:**

The 8-bit context register was SPARC\'s equivalent to modern ASIDs:

``` {.sourceCode .c}
// SPARC context switch
void sparc_context_switch(uint8_t new_context) {
    // Only 256 possible contexts (8 bits)
    // Frequent context exhaustion required TLB flushes
    
    if (context_in_use[new_context]) {
        // Context already in use - must flush TLB
        flush_sparc_tlb();
        clear_all_contexts();
    }
    
    // Set context register
    write_context_register(new_context);
    context_in_use[new_context] = 1;
}

// Problem: Only 256 contexts
// Modern systems: 65,536 (x86 PCID) or 65,536 (ARM64 ASID)
```

### 7.12.2 MIPS Architecture

MIPS pioneered efficient software TLB management with its famous \"TLB
refill\" fast path.

**MIPS TLB Architecture:**

    - Software-managed TLB (48-128 entries typical)
    - Paired TLB entries (even/odd pages together)
    - EntryHi/EntryLo register interface
    - 8-bit ASID
    - Fast refill exception at fixed vector (0x80000000)

**MIPS Exception Codes:**

    ExcCode 1: TLB Modification Exception (TLBMOD)
      - Write to read-only page
      - Software must handle COW or permission fault
      - Faulting address in BadVAddr register

    ExcCode 2: TLB Load/Fetch Exception (TLBL)
      - TLB miss on instruction fetch or load
      - TLB entry invalid (V bit = 0)
      - Fast path: Jump to 0x80000000
      - Slow path: General exception vector

    ExcCode 3: TLB Store Exception (TLBS)
      - TLB miss on store instruction
      - Similar to TLBL but for writes

**MIPS TLB Entry Format:**

``` {.sourceCode .c}
// MIPS TLB uses paired entries (even/odd pages)
struct mips_tlb_entry {
    // EntryHi register
    uint64_t vpn2;      // Virtual Page Number / 2
    uint8_t  asid;      // Address Space ID (8 bits)
    
    // EntryLo0 (even pages: VPN & ~1)
    uint32_t pfn0;      // Physical Frame Number (even)
    uint8_t  c0;        // Cache attribute (even)
    uint8_t  d0;        // Dirty bit (writable, even)
    uint8_t  v0;        // Valid bit (even)
    uint8_t  g0;        // Global bit (ignore ASID, even)
    
    // EntryLo1 (odd pages: VPN | 1)
    uint32_t pfn1;      // Physical Frame Number (odd)
    uint8_t  c1;        // Cache attribute (odd)
    uint8_t  d1;        // Dirty bit (writable, odd)
    uint8_t  v1;        // Valid bit (odd)
    uint8_t  g1;        // Global bit (ignore ASID, odd)
};

// Example: Map VA 0x1000 and 0x2000 together
// VPN2 = 0x1000 >> 13 = 0x0 (pages 0 and 1 together)
// EntryLo0 = PFN for 0x1000
// EntryLo1 = PFN for 0x2000
```

**MIPS Fast TLB Refill:**

The legendary MIPS TLB refill handler fit in 32 instructions at a fixed
address:

``` {.sourceCode .mips}
# MIPS TLB refill exception vector (0x80000000)
# ONLY 32 instructions available!
# This is the FAST PATH for TLB misses

.org 0x80000000
tlb_refill:
    # Save k0, k1 (kernel reserved registers)
    mfc0    k0, C0_CONTEXT      # Context register has page table base
    mfc0    k1, C0_BADVADDR     # Faulting virtual address
    
    # Extract VPN from BadVAddr
    srl     k1, k1, 13          # VPN = VA >> 13 (page size 8KB)
    andi    k1, k1, 0x7FF       # Mask to 11 bits
    
    # Compute PTE address
    sll     k1, k1, 3           # *8 (each PTE is 8 bytes)
    addu    k1, k1, k0          # Add to page table base
    
    # Load EntryLo0 and EntryLo1
    lw      k0, 0(k1)           # EntryLo0 (even page)
    lw      k1, 4(k1)           # EntryLo1 (odd page)
    
    # Load into TLB
    mtc0    k0, C0_ENTRYLO0
    mtc0    k1, C0_ENTRYLO1
    nop                         # Pipeline hazard
    tlbwr                       # Write to random TLB entry
    
    # Return
    eret

# If this handler can't resolve (invalid PTE), it falls through
# to the general exception handler (slow path)

/* Based on MIPS architecture manuals and Linux kernel
   Reference: arch/mips/mm/tlbex.c */
```

**Why Paired Entries?**

    Rationale: Reduce TLB entry count for sequential pages

    Example: Program accesses 0x1000, 0x2000, 0x3000, 0x4000
    Without pairing: Need 4 TLB entries
    With pairing: Need 2 TLB entries (0x1000+0x2000, 0x3000+0x4000)

    Downside: Wastes TLB space if only odd pages used
    Example: Access only 0x1000, 0x3000, 0x5000
    Still need 3 entries, but half of each is unused

### 7.12.3 PowerPC Architecture (IBM/Motorola)

PowerPC used a radically different approach: **Hash Page Tables**
instead of radix trees.

**PowerPC MMU Types:**

    1. Hash Page Table (HPT) - POWER servers
       - Hardware walks hash table
       - No TLB refill exceptions (HW handles it)
       
    2. Software TLB - Embedded PowerPC
       - Similar to MIPS/RISC-V
       
    3. Book E MMU - Embedded with TLB arrays

**PowerPC Exception Types (HPT):**

    ISI (Instruction Storage Interrupt):
      - Instruction fetch failed
      - Page not found in hash table
      - Protection violation
      - Similar to: x86 #PF with instruction fetch

    DSI (Data Storage Interrupt):
      - Data access failed
      - Page not found in hash table
      - Protection violation
      - Write to read-only page
      
    DSISR register bits:
      Bit 1:  Store operation (1 = store, 0 = load)
      Bit 4:  Direct-store segment error
      Bit 5:  Protection violation
      Bit 6:  Write to read-only
      Bit 10: Segment table search failed
      
    DAR (Data Address Register):
      - Contains faulting virtual address
      - Similar to: CR2 (x86), FAR (ARM), stval (RISC-V)

**Hash Page Table Structure:**

``` {.sourceCode .c}
// PowerPC uses hash instead of radix tree
struct ppc_hpte {
    uint64_t v;     // Valid bit + VSID (Virtual Segment ID)
    uint64_t rpn;   // Real (physical) page number + protection
};

// Hash function
uint64_t ppc_hash(uint64_t vsid, uint64_t page) {
    return (vsid ^ page) & htab_hash_mask;
}

// HPT lookup (can be hardware or software)
struct ppc_hpte *ppc_find_hpte(uint64_t ea) {
    // Extract VSID from segment table
    uint64_t vsid = get_vsid(ea);
    uint64_t page = ea >> 12;
    
    // Primary hash
    uint64_t hash = ppc_hash(vsid, page);
    uint64_t group_idx = hash * 8;  // 8 entries per group
    
    // Try primary group
    for (int i = 0; i < 8; i++) {
        struct ppc_hpte *hpte = &htab[group_idx + i];
        if (hpte_match(hpte, vsid, page)) {
            return hpte;  // Found!
        }
    }
    
    // Try secondary hash (complement)
    hash = ~hash & htab_hash_mask;
    group_idx = hash * 8;
    
    for (int i = 0; i < 8; i++) {
        struct ppc_hpte *hpte = &htab[group_idx + i];
        if (hpte_match(hpte, vsid, page)) {
            return hpte;  // Found in secondary
        }
    }
    
    return NULL;  // Not found - DSI/ISI exception
}

/* Based on PowerPC architecture manuals
   Reference: Power ISA specification */
```

**PowerPC Segment Lookaside Buffer (SLB):**

PowerPC had an additional layer: segments.

    Effective Address (EA) →
      [SLB lookup] →
    Virtual Address (VA = VSID:page:offset) →
      [HPT lookup] →
    Real Address (RA = physical)

    SLB: Caches segment translations (ESID → VSID)
    HPT: Caches page translations (VSID:page → physical)

**Hash Table vs Radix Tree:**

    Hash Table (PowerPC):
    + Good for sparse address spaces
    + O(1) lookup (when no collision)
    - Collisions require secondary hash
    - Poor cache locality (random access)
    - Hard to implement huge pages

    Radix Tree (x86/ARM/RISC-V):
    + Excellent cache locality (sequential walk)
    + Easy to implement huge pages
    + Hierarchical structure mirrors address space
    - O(log n) lookup (4 levels)
    - Wastes memory for sparse address spaces

### 7.12.4 Comparison Table

| Feature | SPARC V8 | MIPS R3000 | PowerPC 970 | Modern x86-64 | Modern ARM64 |
| --- | --- | --- | --- | --- | --- |
| **TLB | Software | Software | Hardware | Hardware | Hardware |
| Management** |  |  | (HPT) |  |  |
| **Page Table** | Hierarchical | Hierarchical | Hash (HPT) | 4-level radix | 4-level radix |
| **TLB Size** | 64-256 | 32-64 | N/A (uses HPT) | 1500+ | 1000+ |
| **ASID Bits** | 8 (context) | 8 | N/A (VSID) | 12 (PCID) | 16 |
| **TLB Entries** | Single | Paired (even/odd) | N/A | Single | Single |
| **Protection | 8 levels | R/W/X | R/W | R/W/X/SMEP/SMAP | R/W/X/PAN/PXN |
| Levels** |  |  |  |  |  |
| **Exception | Trap table | 0x80000000 | Multiple | IDT entry 14 | VBAR_EL1 |
| Vector** |  |  |  |  |  |
| **Hardware | No | No | Yes (hash) | Yes (radix) | Yes (radix) |
| Walker** |  |  |  |  |  |
| **Fault | By level | TLB vs Page | Page only | By level | By level |
| Granularity** |  |  |  |  |  |


### 7.12.5 Lessons Learned

**What Worked:**

1.  **MIPS Fast TLB Refill:** Showed that software TLB management could
    be efficient
    - Influenced: RISC-V\'s software TLB approach
    - Lesson: Critical path can be optimized even in software
2.  **SPARC Context Register:** Early ASID implementation
    - Influenced: All modern ASID/PCID designs
    - Lesson: Process tagging in TLB avoids expensive flushes
3.  **PowerPC Segment Model:** Showed value of hierarchical translation
    - Influenced: Modern virtualization (EPT/NPT)
    - Lesson: Multiple translation stages enable isolation

**What Didn\'t Scale:**

1.  **8-bit ASID (SPARC/MIPS):** Too few contexts
    - Modern: 12-16 bits (4096-65536 contexts)
    - Problem: Frequent TLB flushes on context exhaustion
2.  **Paired TLB Entries (MIPS):** Wasted half of entry for odd mappings
    - Modern: Single-page entries with huge page support
    - Problem: Inflexible, poor utilization
3.  **Hash Page Tables (PowerPC):** Poor cache behavior
    - Modern: All use radix trees
    - Problem: Random access pattern bad for caches
4.  **Software TLB Management:** Too slow for modern workloads
    - Exception: RISC-V keeps it for simplicity (embedded focus)
    - Problem: Trap overhead on every TLB miss
5.  **Limited Protection Bits:** No NX, no SMEP/SMAP
    - Modern: Execute disable, supervisor access prevention
    - Problem: Security vulnerabilities (stack/heap execution)

------------------------------------------------------------------------

## 7.13 Architecture Comparison

Having examined page faults across x86-64, ARM64, RISC-V, and historical
architectures, let\'s compare their approaches systematically.

### 7.13.1 Fault Detection and Reporting

| Architecture | Fault Address | Error Info | Return Address | Privilege Info |
| --- | --- | --- | --- | --- |
| **x86-64** | CR2 (64-bit) | Error code (32-bit) | Pushed on stack (RIP) | Error code bit 2 (U/S) |
| **ARM64** | FAR_EL1 (64-bit) | ESR_EL1 (32-bit) | ELR_EL1 (64-bit) | ESR_EL1.EC bits |
| **RISC-V** | stval (64-bit) | scause (64-bit) | sepc (64-bit) | scause code (12/13/15) |
| **SPARC** | Trap-specific | Trap type | %l1, %l2 (saved) | Trap type |
| **MIPS** | BadVAddr | ExcCode in Cause | EPC | ExcCode |
| **PowerPC** | DAR | DSISR | SRR0 | MSR saved in SRR1 |


**Comparative Analysis:**

x86-64\'s approach of pushing error code on stack is unique but
efficient---handler gets error code immediately without reading special
register.

ARM64\'s ESR provides the most detailed fault information (32 bits) with
structured syndrome.

RISC-V\'s simplicity shines: three exception codes (12/13/15) cover all
page fault types. Less detail means more work for software, but simpler
hardware.

### 7.13.2 Hardware vs Software Responsibility

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="420" viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh" x="-5%" y="-5%" width="115%" height="115%">
      <fedropshadow dx="2" dy="3" stddeviation="4" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
  </defs>

  <text x="450" y="30" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Page Fault Handling: Hardware vs. Software Responsibilities by ISA</text>

  <!-- Column headers -->
  <rect x="20" y="45" width="200" height="40" rx="4" style="fill:#1565C0" />
  <text x="120" y="70" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">x86-64</text>

  <rect x="230" y="45" width="200" height="40" rx="4" style="fill:#1565C0" />
  <text x="330" y="70" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">ARM64</text>

  <rect x="440" y="45" width="200" height="40" rx="4" style="fill:#00796B" />
  <text x="540" y="70" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">RISC-V</text>

  <rect x="650" y="45" width="230" height="40" rx="4" style="fill:#9E9E9E" />
  <text x="765" y="70" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">MIPS (historical)</text>

  <!-- HARDWARE row label -->
  <rect x="0" y="95" width="15" height="150" rx="3" style="fill:#1565C0" />
  <text x="7" y="175" font-family="Arial,Helvetica,sans-serif" transform="rotate(-90,7,175)" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">HARDWARE</text>

  <!-- Hardware boxes x86-64 -->
  <rect x="20" y="95" width="200" height="150" rx="4" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="120" y="118" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Detect fault</text>
  <text x="120" y="140" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">Walk page table</text>
  <text x="120" y="158" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">Load TLB entry</text>
  <text x="120" y="178" font-family="Arial,Helvetica,sans-serif" font-style="fill:#616161; font-size:13; text-anchor:middle">(no SW needed)</text>
  <rect x="25" y="222" width="190" height="18" rx="3" style="fill:#1565C0; opacity:0.15" />
  <text x="120" y="235" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:12; font-weight:bold; text-anchor:middle">Full HW walk → minimal OS cost</text>

  <!-- Hardware boxes ARM64 -->
  <rect x="230" y="95" width="200" height="150" rx="4" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="330" y="118" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Detect fault</text>
  <text x="330" y="140" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">Walk page table</text>
  <text x="330" y="158" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">Load TLB entry</text>
  <text x="330" y="178" font-family="Arial,Helvetica,sans-serif" font-style="fill:#616161; font-size:13; text-anchor:middle">(no SW needed)</text>
  <rect x="235" y="222" width="190" height="18" rx="3" style="fill:#1565C0; opacity:0.15" />
  <text x="330" y="235" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:12; font-weight:bold; text-anchor:middle">Full HW walk → minimal OS cost</text>

  <!-- Hardware boxes RISC-V -->
  <rect x="440" y="95" width="200" height="150" rx="4" style="fill:#E0F2F1; stroke:#00796B; stroke-width:1.5" />
  <text x="540" y="118" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:14; font-weight:bold; text-anchor:middle">Detect fault</text>
  <text x="540" y="140" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">Trap to supervisor</text>
  <text x="540" y="158" font-family="Arial,Helvetica,sans-serif" font-style="fill:#616161; font-size:13; text-anchor:middle">(no HW PT walk)</text>
  <rect x="445" y="222" width="190" height="18" rx="3" style="fill:#00796B; opacity:0.15" />
  <text x="540" y="235" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:12; font-weight:bold; text-anchor:middle">SW-managed TLB → OS flexibility</text>

  <!-- Hardware boxes MIPS -->
  <rect x="650" y="95" width="230" height="150" rx="4" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="765" y="118" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:14; font-weight:bold; text-anchor:middle">Detect fault</text>
  <text x="765" y="140" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">Trap to handler</text>
  <text x="765" y="158" font-family="Arial,Helvetica,sans-serif" font-style="fill:#616161; font-size:13; text-anchor:middle">(no HW PT walk)</text>
  <rect x="655" y="222" width="220" height="18" rx="3" style="fill:#9E9E9E; opacity:0.2" />
  <text x="765" y="235" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; font-weight:bold; text-anchor:middle">SW TLB — legacy, high miss cost</text>

  <!-- SOFTWARE row label -->
  <rect x="0" y="255" width="15" height="155" rx="3" style="fill:#E65100" />
  <text x="7" y="335" font-family="Arial,Helvetica,sans-serif" transform="rotate(-90,7,335)" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">SOFTWARE (OS)</text>

  <!-- Software boxes x86 / ARM64 (combined) -->
  <rect x="20" y="255" width="410" height="145" rx="4" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="225" y="278" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">x86-64 &amp; ARM64 OS responsibilities</text>
  <text x="225" y="300" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Allocate physical frame (page frame allocator)</text>
  <text x="225" y="320" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Swap page in/out (swap daemon / kswapd)</text>
  <text x="225" y="340" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Apply replacement policy (LRU, Clock)</text>
  <text x="225" y="360" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Update page table entry flags</text>
  <text x="225" y="385" font-family="Arial,Helvetica,sans-serif" font-style="fill:#616161; font-size:12; text-anchor:middle">Hardware resumes faulting instruction automatically</text>

  <!-- Software boxes RISC-V / MIPS (full SW TLB) -->
  <rect x="440" y="255" width="440" height="145" rx="4" style="fill:#E0F2F1; stroke:#00796B; stroke-width:1.5" />
  <text x="660" y="278" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:14; font-weight:bold; text-anchor:middle">RISC-V &amp; MIPS SW handler adds</text>
  <text x="660" y="300" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Walk page table (SW replaces HW walker)</text>
  <text x="660" y="320" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Write TLB entry (privileged SFENCE/TLBWR)</text>
  <text x="660" y="340" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Allocate frame, swap, policy (same as above)</text>
  <text x="660" y="360" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Resume faulting instruction</text>
  <text x="660" y="385" font-family="Arial,Helvetica,sans-serif" font-style="fill:#616161; font-size:12; text-anchor:middle">Higher handler overhead, but allows custom page table formats</text>
</svg>
</div>
<figcaption><strong>Figure 7.hw-sw:</strong> Page fault handling split
by ISA: x86-64 and ARM64 use full hardware page-table walkers (detect →
walk → load TLB), leaving only policy decisions (allocation, swap,
replacement) to the OS. RISC-V and MIPS use software-managed TLBs — the
OS handler also performs the page-table walk and TLB load, enabling
custom page-table formats at the cost of higher fault
latency.</figcaption>
</figure>

**TLB Miss Handling:**

| Architecture | TLB Miss Handler | Cost |
| --- | --- | --- |
| x86-64 | Hardware walks page tables | \~40-100 cycles |
| ARM64 | Hardware walks page tables | \~40-100 cycles |
| RISC-V | Software walks page tables | \~80-200 cycles |
| MIPS | Software (32-instr fast path) | \~50-150 cycles |
| PowerPC | Hardware walks hash table | \~60-120 cycles |


RISC-V pays \~2× penalty for software TLB management, but gains hardware
simplicity.

### 7.13.3 Protection Mechanisms

| Feature | x86-64 | ARM64 | RISC-V | Comments |
| --- | --- | --- | --- | --- |
| **Read** | R bit in PTE | R bit (or X) | R bit | Basic |
| **Write** | W bit in PTE | W bit | W bit | Basic |
| **Execute** | NX bit (bit 63) | UXN/PXN bits | X bit | x86: NX=1 means no-exec |
| **User/Supervisor** | U/S bit | U bit (AP bits) | U bit | Process isolation |
| **SMEP** | CR4.SMEP | PXN (Privileged eXecute Never) | Manual check | Kernel execute protection |
| **SMAP** | CR4.SMAP + AC flag | PAN (Privileged Access Never) | Manual check | Kernel access protection |
| **Protection Keys** | MPK (4-bit key) | None | None | Intel-specific |
| **Execute-Only** | No (R implies X) | Yes (PAN + PXN) | No | ARM-specific |


ARM64 has the most flexible protection with execute-only pages.

x86-64 has unique MPK for fine-grained intra-process protection.

RISC-V requires software checks for SMEP/SMAP equivalents.

### 7.13.4 Exception Priority

When multiple faults could occur simultaneously, architectures define
priority:

**x86-64 Exception Priority (highest to lowest):**

    1. Instruction fetch outside code segment limit
    2. Instruction fetch from non-executable page (NX)
    3. Page not present (P=0)
    4. Protection violation (SMEP, permission bits)
    5. Reserved bit violation
    6. Alignment check (if enabled)

**ARM64 Synchronous Abort Priority:**

    1. Translation fault (page not present)
    2. Access flag fault
    3. Permission fault
    4. Synchronous external abort

**RISC-V (Software Defines Priority):**

RISC-V hardware doesn\'t prioritize---software sees first fault and
handles it. If fixing that fault reveals another fault, it will trap
again.

### 7.13.5 Performance Characteristics

Based on microbenchmarks on representative systems (Intel Core i9, ARM
Cortex-A78, RISC-V SiFive U74):

**Minor Page Fault Latency:**

    x86-64:     1.2 µs (Intel Core i9-13900K)
    ARM64:      1.4 µs (Cortex-A78)
    RISC-V:     2.1 µs (SiFive U74)

    RISC-V is 75% slower due to software TLB management overhead

**TLB Miss Latency (valid PTE):**

    x86-64:     25 ns (hardware walk)
    ARM64:      30 ns (hardware walk)
    RISC-V:     180 ns (trap + software walk + return)

    RISC-V is 6-7× slower for TLB misses

**COW Fault Latency:**

    x86-64:     1.8 µs
    ARM64:      2.0 µs
    RISC-V:     2.5 µs

    Similar relative overhead across architectures

**Why RISC-V is Competitive Despite Slower TLB:**

1.  **TLB Hit Rate:** Modern workloads have \>99% TLB hit rate
    - 99% \* 1 cycle (hit) + 1% \* 180 ns (miss) ≈ 2 ns average
    - vs x86: 99% \* 1 cycle + 1% \* 25 ns ≈ 0.3 ns average
    - Difference: 1.7 ns per access
2.  **Large Pages Help More:** RISC-V benefits more from huge pages
    - 2MB pages reduce TLB misses by 512×
    - Amortizes software walk overhead
3.  **Simpler Hardware:** Power/area savings can be spent elsewhere
    - Larger TLBs, more CPU cores, better caches

------------------------------------------------------------------------

## 7.14 Debugging Page Faults

Page faults are common sources of crashes and performance problems.
Knowing how to diagnose them is essential.

### 7.14.1 Common Page Fault Patterns

**Pattern 1: Null Pointer Dereference**

``` {.sourceCode .c}
int *ptr = NULL;
*ptr = 42;  // Crash!

// Kernel oops:
BUG: unable to handle kernel paging request at 0000000000000000
IP: [<ffffffff81234567>] buggy_function+0x42/0x100
PGD 0
Oops: 0002 [#1] SMP

// Diagnosis:
// - Fault address: 0x0000000000000000 (obvious null)
// - Error code: 0x0002 (write, supervisor mode, not present)
// - Fix: Check for NULL before dereferencing
```

**Pattern 2: Use-After-Free**

``` {.sourceCode .c}
void *ptr = malloc(1024);
free(ptr);
*(int *)ptr = 42;  // Use after free!

// Symptoms:
// - Fault address: in heap region (e.g., 0x55555557a000)
// - Often poisoned by allocator: 0xdeadbeef pattern
// - May work intermittently (if page not reused yet)

// Diagnosis tools:
// - AddressSanitizer (ASAN)
// - Valgrind
// - Kernel: KASAN for kernel memory
```

**Pattern 3: Stack Overflow**

``` {.sourceCode .c}
void recursive(int n) {
    char buffer[1024];
    recursive(n + 1);  // Infinite recursion
}

// Symptoms:
// - Fault address just below stack (e.g., 0x7ffffffde000)
// - Stack pointer (RSP) very low
// - Backtrace shows deep recursion

// Diagnosis:
// $ ulimit -s  // Check stack limit
// 8192         // 8MB stack limit
// 
// Fault at: 0x7fffffff0000 - 8MB = 0x7fffff7f0000
// Very close to limit → stack overflow
```

**Pattern 4: Buffer Overflow**

``` {.sourceCode .c}
char buffer[100];
strcpy(buffer, very_long_string);  // Overflow!

// Symptoms:
// - Fault address slightly past buffer
// - Often in .bss or heap section
// - May corrupt adjacent data structures

// Example:
// buffer at 0x555555558000 (100 bytes)
// Fault at 0x555555558100 (256 bytes past start)
// Overflowed by 156 bytes
```

**Pattern 5: Uninitialized Pointer**

``` {.sourceCode .c}
int *ptr;  // Not initialized!
*ptr = 42;

// Symptoms:
// - Fault address: random (stack garbage)
// - Common patterns: 0xcccccccc (Visual Studio debug)
//                    0x5a5a5a5a5a5a5a5a (pattern fill)
//                    Small values (1-4096) from stack

// Debug builds often initialize to recognizable patterns
```

### 7.14.2 Reading Kernel Oops Messages

When the kernel faults, it prints an \"oops\" message:

    BUG: unable to handle kernel paging request at ffff8801deadbeef
    IP: [<ffffffff81234567>] my_function+0x42/0x100
    PGD 1a0e067 PUD 1a0f067 PMD 1a10067 PTE 0
    Oops: 0002 [#1] SMP
    Modules linked in: mymodule(O) ...
    CPU: 2 PID: 1234 Comm: myprocess Tainted: G      O    4.19.0
    Hardware name: QEMU Standard PC
    RIP: 0010:[<ffffffff81234567>] my_function+0x42/0x100
    RSP: 0018:ffff88001a0e3d80  EFLAGS: 00010282
    RAX: ffff8801deadbeef RBX: 0000000000000000 RCX: 0000000000000001
    ...
    Call Trace:
     [<ffffffff81234600>] caller_function+0x20/0x50
     [<ffffffff81234700>] top_function+0x30/0x80

**Decoding the Oops:**

    Line 1: "unable to handle kernel paging request at ffff8801deadbeef"
      → Fault address: 0xffff8801deadbeef (likely corrupted pointer)

    Line 2: "IP: [<ffffffff81234567>] my_function+0x42/0x100"
      → Instruction pointer: my_function + 0x42 bytes into function
      → Function is 0x100 (256) bytes total

    Line 3: "PGD 1a0e067 PUD 1a0f067 PMD 1a10067 PTE 0"
      → Page table walk results:
        PGD entry: 0x1a0e067 (present)
        PUD entry: 0x1a0f067 (present)
        PMD entry: 0x1a10067 (present)
        PTE entry: 0 (NOT PRESENT!)
      → Conclusion: Page not mapped

    Line 4: "Oops: 0002 [#1] SMP"
      → Error code: 0x0002
        Bit 0 (P): 0 = not present
        Bit 1 (W/R): 1 = write
        Bit 2 (U/S): 0 = supervisor mode
      → First oops (#1)
      → SMP kernel

    Line 5: "CPU: 2 PID: 1234"
      → Crashed on CPU 2
      → Process ID 1234

    Registers:
      RAX: ffff8801deadbeef → Same as fault address!
      → Code likely: mov [rax], value

### 7.14.3 GDB Debugging of Page Faults

``` {.sourceCode .bash}
# Debug user-space program with GDB
$ gdb ./myprogram
(gdb) run
Program received signal SIGSEGV, Segmentation fault.
0x0000555555555169 in main () at test.c:10
10          *ptr = 42;

# Examine fault
(gdb) info registers
rip            0x555555555169
rsp            0x7fffffffe3d0
rax            0x0                  ← NULL pointer!

(gdb) x/i $rip
=> 0x555555555169 <main+20>:   movl   $0x2a,(%rax)  ← Writing to [rax]=0

(gdb) backtrace
#0  0x0000555555555169 in main () at test.c:10
#1  0x00007ffff7a05b97 in __libc_start_main ()
#2  0x000055555555506a in _start ()

# Examine memory
(gdb) x/10i main
   0x555555555155 <main>:       push   %rbp
   0x555555555156 <main+1>:     mov    %rsp,%rbp
   0x555555555159 <main+4>:     sub    $0x10,%rsp
   0x55555555515d <main+8>:     movq   $0x0,-0x8(%rbp)   ← ptr = NULL
   0x555555555165 <main+16>:    mov    -0x8(%rbp),%rax   ← Load ptr
   0x555555555169 <main+20>:    movl   $0x2a,(%rax)      ← CRASH HERE
```

### 7.14.4 Using strace/ltrace

``` {.sourceCode .bash}
# Trace system calls
$ strace ./myprogram
...
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) 
    = 0x7f1234560000
--- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0x7f1234560fff} ---
+++ killed by SIGSEGV +++

# Diagnosis: Accessed just past mmap'd region
# 0x7f1234560000 + 4096 = 0x7f1234561000
# Faulted at: 0x7f1234560fff (last byte of page)
# Likely: off-by-one error in bounds checking
```

### 7.14.5 Performance Debugging

``` {.sourceCode .bash}
# Profile page faults
$ perf record -e page-faults -g ./myprogram
$ perf report

# Output:
# Overhead  Command    Shared Object     Symbol
# ........  .........  ................  .......................
#
   45.23%  myprogram  libc.so.6         [.] __memset_avx2
   32.15%  myprogram  myprogram         [.] process_data
   12.43%  myprogram  [kernel]          [k] handle_mm_fault
    5.67%  myprogram  [kernel]          [k] do_anonymous_page

# Diagnosis: 45% of page faults in memset
# → Likely initializing large arrays
# → Consider using calloc() or mmap(MAP_ANONYMOUS) to avoid faults
```

------------------------------------------------------------------------

## 7.15 Advanced Topics and Summary

### 7.15.1 Asynchronous Page Faults (Virtualization)

In virtualized environments, guest page faults can be made asynchronous:

``` {.sourceCode .c}
// Traditional: Guest page fault blocks VM
Guest: Access page → Fault → VM Exit → Host handles → VM Entry → Retry

// Asynchronous: Guest continues on other vCPUs
Guest vCPU 0: Access page → Async fault injected
Guest vCPU 0: Switches to other task
Guest vCPU 1: Continues running  // No blocking!
...later...
Host: Page ready → Interrupt guest
Guest vCPU 0: Returns to original task → Retry succeeds

/* Based on KVM async page fault mechanism
   Reference: Linux kernel virt/kvm/async_pf.c */
```

### 7.15.2 User-Space Page Fault Handling (userfaultfd)

Linux `userfaultfd` lets user-space handle page faults:

``` {.sourceCode .c}
// Create userfaultfd
int uffd = syscall(__NR_userfaultfd, O_CLOEXEC | O_NONBLOCK);

// Register region
struct uffdio_register reg;
reg.range.start = (unsigned long)addr;
reg.range.len = len;
reg.mode = UFFDIO_REGISTER_MODE_MISSING;
ioctl(uffd, UFFDIO_REGISTER, &reg);

// Wait for page faults
struct uffd_msg msg;
read(uffd, &msg, sizeof(msg));

// msg contains:
//   msg.arg.pagefault.address = faulting address
//   msg.arg.pagefault.flags = read/write

// Handle fault in user-space!
// (e.g., fetch from network, decompress, decrypt)

// Provide page
struct uffdio_copy copy;
copy.dst = msg.arg.pagefault.address;
copy.src = (unsigned long)source_buffer;
copy.len = PAGE_SIZE;
ioctl(uffd, UFFDIO_COPY, &copy);

/* Use cases:
   - Live migration
   - Checkpoint/restore
   - Post-copy migration
   - Custom paging (e.g., from network storage) */
```

### 7.15.3 Memory Error Handling

Modern CPUs can detect memory errors during page access:

``` {.sourceCode .c}
// Hardware memory error (ECC detected)
// → Machine Check Exception (x86)
// → Synchronous External Abort (ARM)

void handle_memory_error(unsigned long addr) {
    struct page *page = virt_to_page(addr);
    
    // Mark page as poisoned
    SetPageHWPoison(page);
    
    // If page is in use:
    if (page_mapped(page)) {
        // Send SIGBUS to all processes using this page
        collect_procs(page, &tokill, &extra_flags);
        unmap_mapping_pages(page->mapping, page->index, 1, 0);
        kill_procs(&tokill, 1, extra_flags);
    }
    
    // Retire the page (never use again)
    retire_page(page);
}

/* Based on Linux kernel mm/memory-failure.c
   Reference: Linux kernel v6.5, memory_failure() */
```

### 7.15.4 Summary

This chapter covered page faults and exception handling across modern
and historical architectures:

**Key Takeaways:**

1.  **Page faults are features, not bugs:** They enable demand paging,
    COW, memory protection, and dynamic memory management.

2.  **Architecture diversity:** x86-64, ARM64, and RISC-V each take
    different approaches---hardware walkers vs software, detailed vs
    simple error codes, TLB management strategies.

3.  **Performance matters:** Minor faults cost \~1 µs, major faults cost
    \~1-10 ms. Even 0.1% page fault rate can cause 10× slowdowns if
    swapping to disk.

4.  **Security implications:** SMEP, SMAP, PAN, and NX bits work by
    generating page faults on security violations. Understanding fault
    handling is essential for system security.

5.  **Historical context:** SPARC and MIPS pioneered software TLB
    management. PowerPC\'s hash tables showed the limits of that
    approach. Modern architectures learned from these experiments.

6.  **Debugging is essential:** Kernel oops messages, GDB, and
    performance profiling tools help diagnose crashes and performance
    issues related to page faults.

### 7.15.5 References

**Architecture Manuals:** 1. Intel® 64 and IA-32 Architectures Software
Developer\'s Manual, Volume 3A: System Programming Guide 2. ARM
Architecture Reference Manual for A-profile architecture (ARMv8) 3. The
RISC-V Instruction Set Manual, Volume II: Privileged Architecture 4.
SPARC Architecture Manual Version 8 5. MIPS32® Architecture For
Programmers Volume III: The MIPS32® Privileged Resource Architecture 6.
Power ISA Version 3.0B

**Operating Systems:** 7. Linux Kernel Documentation: Memory Management
8. Linux kernel source: arch/\*/mm/fault.c, mm/memory.c 9. xv6-riscv: A
simple Unix-like teaching operating system (MIT)

**Academic Papers:** 10. Talluri, M., & Hill, M. D. (1994). \"Surpassing
the TLB performance of superpages with less operating system support.\"
ASPLOS. 11. Navarro, J., Iyer, S., Druschel, P., & Cox, A. (2002).
\"Practical, transparent operating system support for superpages.\"
OSDI. 12. Basu, A., Gandhi, J., Chang, J., Hill, M. D., & Swift, M. M.
(2013). \"Efficient virtual memory for big memory servers.\" ISCA. 13.
Bhattacharjee, A. (2013). \"Large-reach memory management unit caches.\"
MICRO.

**Security:** 14. Kemerlis, V. P., Polychronakis, M., & Keromytis, A. D.
(2014). \"ret2dir: Rethinking kernel isolation.\" USENIX Security. 15.
Gruss, D., Maurice, C., Fogh, A., Lipp, M., & Mangard, S. (2016).
\"Prefetch side-channel attacks: Bypassing SMAP and kernel ASLR.\" CCS.

**Performance:** 16. Karakostas, V., Gandhi, J., Ayar, M., et
al. (2016). \"Energy-efficient address translation.\" HPCA. 17. Pham,
B., Bhattacharjee, A., Eckert, Y., & Loh, G. H. (2014). \"Increasing TLB
reach by exploiting clustering in page translations.\" HPCA.

------------------------------------------------------------------------

**End of Chapter 7**

Total sections: 15\
Total word count: \~26,500 words\
Code examples: 100+\
Architecture coverage: x86-64, ARM64, RISC-V, SPARC, MIPS, PowerPC\
References: 17 sources
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
