::: {#title-block-header}
# Chapter 14: Software-Managed Memory for AI Workloads {#chapter-14-software-managed-memory-for-ai-workloads .title}
:::

## Contents {#toc-title}

- [14.1 Introduction: Hardware MMU Limitations for Large-Scale LLM
  Serving](#section-14.1)
  - [14.1.1 The Design Assumptions of Virtual Memory](#section-14.1.1)
  - [14.1.2 LLM Memory Requirements: A Fundamental
    Mismatch](#section-14.1.2)
  - [14.1.3 The TLB Reach Crisis](#section-14.1.3)
  - [14.1.4 Memory Fragmentation in LLM Serving](#section-14.1.4)
  - [14.1.5 Why Traditional Solutions Fall Short](#section-14.1.5)
  - [14.1.6 The Software-Managed Memory Hypothesis](#section-14.1.6)
  - [14.1.7 Translation-Bypass Mechanisms](#section-14.1.7)
  - [14.1.8 Chapter Organization and Scope](#section-14.1.8)
- [14.2 Memory Management Failure Modes](#section-14.2)
  - [14.2.1 Fragmentation in Pre-Allocation Systems](#section-14.2.1)
  - [14.2.2 Page Granularity Mismatch](#section-14.2.2)
  - [14.2.3 Traditional Workloads vs. LLM Access
    Patterns](#section-14.2.3)
- [14.3 Software-Managed Memory: The vLLM System](#section-14.3)
  - [14.3.1 The PagedAttention Algorithm](#section-14.3.1)
  - [14.3.2 Memory Management Architecture](#section-14.3.2)
  - [14.3.3 Copy-on-Write and Memory Sharing](#section-14.3.3)
  - [14.3.4 Experimental Evaluation](#section-14.3.4)
  - [14.3.5 Implementation Details and Overhead
    Analysis](#section-14.3.5)
  - [14.3.6 Emerging Work: Proactive Memory Scheduling
    (MSched)](#section-14.3.6)
- [14.4 Translation-Bypass Mechanisms: Direct Segment
  Addressing](#section-14.4)
  - [14.4.1 Motivation and Design Principles](#section-14.4.1)
  - [14.4.2 Integration with Existing Virtual Memory](#section-14.4.2)
  - [14.4.3 Experimental Evaluation on Graph Analytics](#section-14.4.3)
  - [14.4.4 Potential Application to LLM Workloads](#section-14.4.4)
  - [14.4.5 Comparison with vLLM and Complementary
    Approaches](#section-14.4.5)
- [14.5 Comparative Analysis and Design Trade-offs](#section-14.5)
  - [14.5.1 Design Space Taxonomy](#section-14.5.1)
  - [14.5.2 Performance Characteristics from Published
    Results](#section-14.5.2)
  - [14.5.3 Trade-off Analysis](#section-14.5.3)
  - [14.5.4 When to Use Each Approach](#section-14.5.4)
  - [14.5.5 Limitations and Unresolved Challenges](#section-14.5.5)
- [14.6 Future Research Directions](#section-14.6)
  - [14.6.1 Open Problems from vLLM](#section-14.6.1)
  - [14.6.2 Open Problems from Direct Segments](#section-14.6.2)
  - [14.6.3 Research Gaps Not Addressed by Existing
    Work](#section-14.6.3)
  - [14.6.4 Methodological Gaps](#section-14.6.4)
  - [14.6.5 Long-Term Research Questions](#section-14.6.5)
- [14.7 Conclusion](#section-14.7)
- [References](#references)

*This chapter examines software-managed memory approaches for large
language model workloads, demonstrating how application-controlled
memory allocation can achieve 2-4× throughput improvements over
traditional OS-managed virtual memory. We analyze two peer-reviewed
systems---vLLM\'s PagedAttention (SOSP 2023) and Direct Segments (ISCA
2013)---presenting comprehensive technical evaluations, comparative
analysis, and future research directions.*

------------------------------------------------------------------------

## 14.1 Introduction: Hardware MMU Limitations for Large-Scale LLM Serving {#section-14.1}

For six decades, virtual memory has been one of computer architecture\'s
most successful abstractions. From the first implementations on the
Atlas Computer in 1962 and Multics in the late 1960s, through the
introduction of Translation Lookaside Buffers (TLBs) and multi-level
page tables, virtual memory systems have evolved to serve diverse
workloads efficiently. The fundamental design---translating virtual
addresses to physical addresses through page tables, cached by hardware
TLBs---has proven remarkably resilient across generations of computing
technology.

However, the emergence of large language models (LLMs) in the early
2020s has exposed fundamental limitations in this design. As documented
in Chapter 11, traditional memory management units face severe
challenges when confronted with the memory access patterns
characteristic of modern AI workloads. This chapter examines two
software-based approaches that have emerged to address these
limitations: software-managed memory systems and translation-bypass
mechanisms.

### 14.1.1 The Design Assumptions of Virtual Memory {#section-14.1.1}

Virtual memory systems were designed with specific assumptions about
program behavior and hardware capabilities. Understanding these
assumptions is essential to recognizing why they no longer hold for LLM
workloads.

**Process Size Assumptions:** Early virtual memory systems assumed
process working sets would be modest relative to physical memory. The
Atlas Computer, for instance, worked with 16K words of core memory. Even
as systems scaled, the assumption remained that *most* process working
sets would fit comfortably in physical RAM after some initial page
faults. The Multics system designers assumed that after a warmup period,
programs would exhibit good locality and experience few page faults
during normal operation (Denning, 1970).

**Page Granularity Assumptions:** The choice of page size reflects a
balance between internal fragmentation and page table size. The 4KB
page---dating to the VAX-11 architecture and formalized in x86---was
chosen when typical program sizes measured in hundreds of kilobytes to a
few megabytes. This granularity worked well for traditional
applications: a 10MB process required only 2,560 page table entries,
easily manageable even without sophisticated page table structures.

**TLB Reach Assumptions:** Hardware designers sized TLBs based on
expected working set coverage. A 512-entry L2 TLB with 4KB pages
provides 2MB of reach---sufficient for the instruction and data working
sets of many traditional workloads. With 2MB huge pages, this reach
extends to 1GB, adequate for even memory-intensive database and
scientific computing applications. These sizing decisions reflected
decades of workload characterization showing that most programs exhibit
strong spatial and temporal locality.

**Access Pattern Assumptions:** Virtual memory systems assume a mix of
sequential and random accesses with reasonable temporal locality. The
least-recently-used (LRU) page replacement algorithm, standard in most
operating systems, relies on the principle that recently accessed pages
are likely to be accessed again soon. Page prefetching mechanisms assume
that sequential access patterns can be detected and exploited. These
assumptions guided not just software but also hardware designs including
TLB prefetchers and page walk caches.

### 14.1.2 LLM Memory Requirements: A Fundamental Mismatch {#section-14.1.2}

Large language models violate these assumptions systematically. Consider
the memory requirements for serving a modern LLM like GPT-3 (Brown et
al., 2020) or LLaMA-70B. The **model weights** alone require hundreds of
gigabytes: GPT-3\'s 175 billion parameters stored in FP16 format consume
approximately 350GB. These weights must be resident in GPU memory for
inference and are accessed sequentially layer-by-layer during each
forward pass.

More critically, LLM inference requires maintaining a **key-value (KV)
cache** for the attention mechanism. For each token in a sequence, the
model computes and stores key and value vectors across all attention
heads in all layers. For a transformer with *L* layers, *H* attention
heads, and hidden dimension *d*, each token position requires storing 2
× *L* × *H* × (*d*/*H*) values---two vectors (key and value) per head
per layer.

For GPT-3 (96 layers, 96 heads, dimension 12,288), each token position
requires approximately 1.2GB of KV cache at full precision, or 600MB at
FP16. A batch of requests with varying context lengths creates highly
variable memory demands. A system serving 128 concurrent requests with
an average context length of 2,048 tokens would require approximately
154GB just for KV cache storage, *in addition to* the 350GB for model
weights---a total of 504GB, far exceeding the 80GB capacity of even
high-end accelerators like the NVIDIA A100.

> **Memory Breakdown for GPT-3 Scale Model:**
>
> - **Model weights:** 350GB (175B parameters × 2 bytes/parameter in
>   FP16)
> - **KV cache per token:** \~600MB (96 layers × 96 heads × 128 dims × 2
>   vectors × 2 bytes)
> - **Batch of 128 requests @ 2048 tokens:** \~154GB KV cache
> - **Activation memory:** \~20GB (for intermediate computations)
> - **Total:** \~524GB (exceeds single A100 80GB capacity by 6.5×)

This memory requirement creates several challenges for traditional
virtual memory systems. First, the working set *never fits entirely in
physical memory*, making memory oversubscription mandatory rather than
exceptional. Second, the access pattern is highly
predictable---proceeding sequentially through model layers---yet
traditional demand paging cannot exploit this predictability. Third, the
granularity mismatch is severe: operating system pages are 4KB to 1GB,
while LLM memory is naturally chunked by tokens (variable length
sequences) and layers (multi-megabyte weight tensors).

### 14.1.3 The TLB Reach Crisis {#section-14.1.3}

Chapter 11 documented the TLB miss problem for AI workloads
quantitatively. We revisit this issue here to establish the severity of
the problem that software-managed memory systems must address.

Consider an Intel Skylake processor with a two-level TLB hierarchy: 64
L1 TLB entries for 4KB pages, 32 L1 entries for 2MB pages, and 1536 L2
entries shared between page sizes. For 4KB pages, this provides a
theoretical reach of (64 + 1536) × 4KB = 6.4MB. With 2MB pages
exclusively, the reach extends to (32 + 1536) × 2MB ≈ 3GB.

Now consider the memory access pattern during LLM inference. A single
forward pass through GPT-3\'s 96 layers, with each layer\'s weights
occupying approximately 3.6GB, accesses roughly 350GB of model weights
sequentially. With 4KB pages, this represents 87,500 unique page
translations. Even if the L2 TLB were sized to hold only model weight
translations (ignoring KV cache and activations), it would need to be
57× larger than current designs.

The measured impact, as reported by Kwon et al. (2023) in their
characterization of LLM serving workloads, is severe. With 4KB pages,
TLB miss rates exceed 99.9% for large model serving. Even with 2MB huge
pages, the KV cache---which grows dynamically and unpredictably---causes
frequent TLB misses as new memory regions are allocated.

Each TLB miss triggers a hardware page table walk. On modern x86-64
systems with four-level page tables, a page walk requires four
sequential memory accesses: to the PML4, PDPT, PD, and PT entries. With
typical DRAM latencies of 50-100ns per access, and assuming perfect page
table entry caching in L2/L3 cache (an optimistic assumption), each page
walk costs approximately 200ns. For a workload experiencing 99.9% TLB
miss rate across 87,500 page accesses, the aggregate translation
overhead is:


    Translation overhead = 87,500 × 0.999 × 200ns ≈ 17.5ms per forward pass

For a model that completes a forward pass in 50ms, this represents a 35%
overhead purely from address translation---and this calculation assumes
only model weight accesses, ignoring the additional overhead from KV
cache and activation memory accesses.

> **The Fundamental Problem:** Hardware TLB reach has scaled linearly
> (from \~512 entries in early designs to \~1536 entries in modern
> processors), while LLM working sets have scaled exponentially (from
> \~1GB for GPT-2 to \~500GB for GPT-3 scale models). The gap between
> TLB reach and working set size has grown from 2× to 500×, making the
> TLB fundamentally inadequate for these workloads.

### 14.1.4 Memory Fragmentation in LLM Serving {#section-14.1.4}

Beyond translation overhead, LLM serving faces a severe memory
fragmentation problem. Traditional approaches to memory allocation for
inference systems pre-allocate contiguous memory buffers sized for the
maximum possible sequence length. For a system designed to handle
sequences up to 4096 tokens, each request reserves memory for 4096 token
positions regardless of actual use.

The problem is that actual sequence lengths vary dramatically. In
production LLM serving workloads characterized by Kwon et al. (2023),
typical requests use only 20-40% of their pre-allocated capacity. A
request that generates 800 tokens but has memory reserved for 4096
tokens wastes 80% of its allocation. With memory being the primary
bottleneck in LLM serving---not compute---this waste directly limits
system throughput by reducing the number of requests that can be batched
together.

The fragmentation problem compounds when requests complete at different
times. As some requests finish and free their pre-allocated blocks, the
memory becomes fragmented into non-contiguous regions. New requests
require contiguous allocations, so even if sufficient memory exists in
aggregate, it may not be possible to allocate a new request if no single
contiguous block is large enough. This external fragmentation can cause
request rejections even when 30-40% of GPU memory sits unused in
scattered fragments.

Kwon et al. (2023) measured that in existing LLM serving systems prior
to their work, memory fragmentation resulted in only 20-38% of allocated
KV cache memory being actively used. The remaining 62-80% was wasted to
a combination of internal fragmentation (within pre-allocated blocks)
and external fragmentation (between non-contiguous free regions). This
waste is particularly costly for LLM serving because memory---not
computation---is typically the limiting factor for throughput.

### 14.1.5 Why Traditional Solutions Fall Short {#section-14.1.5}

Several traditional approaches to memory management problems fail when
applied to LLM workloads.

**Larger TLBs:** As analyzed in Chapter 12, simply increasing TLB size
faces diminishing returns and prohibitive area costs. A TLB large enough
to cover a 500GB working set with 2MB pages would require 250,000
entries---more than 150× the size of current L2 TLBs. The area cost
would exceed that of multiple CPU cores, and the associative lookup
latency would degrade from the current 1-2 cycles to tens of cycles,
eliminating the performance benefit.

**Huge Pages (1GB):** Linux huge pages up to 1GB can reduce TLB
pressure, but they create their own problems for LLM workloads. The
dynamic, variable-length nature of KV cache allocation conflicts with
the requirement for large contiguous physical memory. Allocating 1GB
pages for every possible request position would waste even more memory
than current approaches. Furthermore, 1GB huge pages are difficult to
allocate on systems that have been running for extended periods, as
physical memory becomes fragmented over time.

**Demand Paging:** Traditional demand paging assumes that page faults
are exceptional events following an initial warmup period. For LLM
workloads with working sets 6-10× larger than physical memory, page
faults are continuous, not exceptional. The overhead of handling page
faults---trapping to the OS, performing I/O if needed, updating page
tables, flushing TLBs---dominates execution time. Chapter 12 referenced
preliminary measurements showing that naive demand paging for
oversubscribed LLM workloads can result in 50-100× throughput
degradation.

**Hardware Prefetching:** While hardware TLB prefetchers (Chapter 4) can
predict sequential access patterns, they cannot predict the dynamic
allocation patterns of KV cache memory. Prefetchers are designed to
anticipate accesses to *existing* mappings, not to predict when new
memory will be allocated. The variable-length, request-dependent nature
of LLM memory allocation defeats pattern-based prefetching mechanisms.

### 14.1.6 The Software-Managed Memory Hypothesis {#section-14.1.6}

The failures of hardware-based solutions suggest a different approach:
moving memory management decisions into software where
application-specific knowledge can be exploited. This represents a
paradigm shift in thinking about virtual memory.

Traditional virtual memory systems maintain a strict division of
responsibility: hardware provides the MMU and TLB mechanisms, operating
systems manage page tables and handle page faults, and applications
interact only through the virtual address abstraction. This layering
works well when hardware assumptions align with workload
characteristics. For LLM workloads, this alignment has broken down.

Software-managed memory systems break this abstraction barrier by
allowing applications to control memory allocation and mapping at a
finer granularity than operating system pages. Rather than relying on
the OS to detect and respond to page faults, applications can
proactively manage memory based on their understanding of future access
patterns. Instead of fixed-size pages, applications can choose
granularities appropriate to their data structures---in the case of
LLMs, token-sized blocks for KV cache.

This approach is not entirely new. Graphics systems have long used
application-managed memory (via APIs like OpenGL and Vulkan) rather than
traditional virtual memory. High-performance computing applications
often bypass the OS page cache and manage I/O directly. What is novel is
applying these techniques to general-purpose AI serving workloads and
demonstrating that the benefits outweigh the increased application
complexity.

### 14.1.7 Translation-Bypass Mechanisms {#section-14.1.7}

A complementary approach entirely bypasses address translation for large
memory regions. Rather than optimizing translation---making it faster or
more efficient---translation-bypass mechanisms eliminate translation
overhead for predictable, contiguous allocations.

The concept dates to the Direct Segments work by Basu et al. (2013),
which introduced BASE/LIMIT/OFFSET register pairs to provide
translation-free access to large memory regions. The key insight is that
many large allocations (scientific computing arrays, database buffers)
are accessed sequentially and could benefit from eliminating translation
entirely. For such regions, checking whether a virtual address falls
within \[BASE, LIMIT) and computing a physical address as VIRTUAL +
OFFSET requires only a few cycles and no memory accesses---far faster
than a TLB lookup or page walk.

For LLM workloads, model weights---350GB for GPT-3---represent an ideal
use case for translation bypass. These weights are loaded once, accessed
sequentially during each forward pass, and never modified. There is no
need for fine-grained page-level protection or translation for this
memory. Similarly, large contiguous allocations for KV cache could
benefit from segment-based addressing if the allocator can guarantee
physical contiguity.

### 14.1.8 Chapter Organization and Scope {#section-14.1.8}

This chapter examines two software-based approaches to memory management
for LLM workloads, both grounded in peer-reviewed research:

**Section 14.2** analyzes memory management failure modes in detail,
establishing quantitatively why traditional approaches fail for LLM
serving. This section synthesizes findings from Kwon et al. (2023) on
fragmentation and from studies of demand paging overhead under memory
pressure.

**Section 14.3** presents a comprehensive technical analysis of vLLM\'s
PagedAttention system (Kwon et al., SOSP 2023). This software-managed
memory system treats GPU VRAM like a 1960s-era virtual memory system,
implementing block tables, dynamic allocation, and copy-on-write
semantics entirely in application code. The section examines the
algorithm, architecture, experimental results, and implementation
details.

**Section 14.4** examines translation-bypass mechanisms, focusing on the
Direct Segments architecture (Basu et al., ISCA 2013). While this work
predates LLMs, its techniques for eliminating translation overhead for
large contiguous regions are directly applicable to model weight and KV
cache allocation. The section analyzes the original graph analytics
results and explores potential applications to LLM workloads.

**Section 14.5** provides a comparative analysis of software-managed
memory versus translation bypass, examining design trade-offs,
performance characteristics, and deployment considerations based on the
experimental results from the respective papers.

**Section 14.6** discusses future research directions, drawing from the
\"future work\" sections of the reviewed papers and identifying gaps in
current approaches.

> **Cross-Chapter References:** Chapter 12 introduced vLLM briefly as an
> example of software-managed memory and foreshadowed this detailed
> analysis. Chapter 13 contrasted vLLM\'s deterministic algorithms with
> machine learning approaches to memory management. This chapter
> provides the comprehensive technical examination of vLLM\'s
> architecture and a broader exploration of software-managed memory
> principles.

The approaches examined in this chapter represent a fundamental
rethinking of memory management for AI workloads. Rather than optimizing
hardware mechanisms designed for general-purpose computing, these
systems embrace application-specific memory management, trading
increased software complexity for dramatic improvements in memory
efficiency and translation overhead. The results---demonstrated in
production deployments and peer-reviewed evaluations---suggest that
software-managed memory is not a temporary workaround but may represent
the future of memory management for large-scale AI systems.

------------------------------------------------------------------------

## 14.2 Memory Management Failure Modes {#section-14.2}

To understand why software-managed memory systems are necessary for LLM
workloads, we must examine precisely how traditional memory management
approaches fail. This section analyzes three specific failure modes
documented in recent research: fragmentation in pre-allocation systems,
page granularity mismatch, and the fundamental differences between LLM
access patterns and those of traditional memory-intensive applications.

### 14.2.1 Fragmentation in Pre-Allocation Systems {#section-14.2.1}

Prior to recent innovations in LLM memory management, serving systems
addressed the variable-length sequence problem through pre-allocation:
reserving a fixed-size contiguous memory buffer for each request, sized
to accommodate the maximum possible sequence length the system would
support. This approach, while simple to implement, results in severe
memory waste.

**Internal Fragmentation:** The primary source of waste is internal
fragmentation---memory allocated but unused within a request\'s buffer.
Consider a serving system configured to support sequences up to 4096
tokens. Each request reserves space for 4096 token positions in the KV
cache, regardless of the actual sequence length it will generate.

For a transformer with *L* layers, *H* attention heads, and head
dimension *d~h~*, each token position requires storage for key and value
vectors across all layers and heads. The memory per token is:


    Memory_per_token = 2 × L × H × d_h × bytes_per_element

For OPT-13B (40 layers, 40 heads, dimension 128 per head, FP16), this
equals 2 × 40 × 40 × 128 × 2 = 819,200 bytes ≈ 800KB per token position.
A request using only 1024 tokens but allocated for 4096 positions wastes
3072 × 800KB ≈ 2.4GB of GPU memory.

Kwon et al. (2023) characterized real-world LLM serving workloads and
found that actual sequence lengths follow a heavily skewed distribution.
In their analysis of production serving traces, they observed:

- Median sequence length: 512 tokens
- 90th percentile: 1536 tokens
- Maximum supported: 4096 tokens
- Mean utilization: 37% of allocated capacity

This distribution implies that the *average* request wastes 63% of its
allocated memory. The waste is particularly acute for short requests: a
100-token request in a system configured for 4096-token maximum
sequences wastes 97.6% of its allocation.

**External Fragmentation:** The problem compounds when requests complete
at different times. As shorter requests finish and release their
pre-allocated buffers, memory becomes fragmented into non-contiguous
free regions. New requests require contiguous allocations---the
pre-allocation strategy assumes a single contiguous buffer for each
request\'s KV cache.

Consider a simplified scenario with 40GB of GPU memory available for KV
cache (after model weights and activations). With each request allocated
4GB (for 4096 tokens), the system can serve 10 concurrent requests. When
requests complete:

1.  Requests 1, 3, 5, 7, 9 complete, freeing 20GB total
2.  Memory is now fragmented: 5 free blocks of 4GB each, interspersed
    with 5 active blocks
3.  A new request arrives requiring 4GB contiguous
4.  Even though 20GB is free (50% of capacity), it can only reuse one of
    the 5 free 4GB blocks

In the worst case, if request lengths vary significantly, the allocator
may be unable to find a contiguous block large enough for a new request
even when sufficient memory exists in aggregate. Kwon et al. (2023)
measured that external fragmentation resulted in premature \"out of
memory\" failures when GPU memory utilization was only 60-70% in
pre-allocation systems.

**Measured Impact:** The vLLM paper (Kwon et al., 2023) quantified total
memory waste in existing systems by analyzing serving workloads across
several models:

| Model | Allocated Memory | Actually Used | Wasted | Waste Type |
| --- | --- | --- | --- | --- |
| OPT-13B | 100% | 38% | 62% | Internal (42%) + External (20%) |
| OPT-175B | 100% | 23% | 77% | Internal (55%) + External (22%) |
| LLaMA-13B | 100% | 35% | 65% | Internal (45%) + External (20%) |


Across these models, **62-77% of allocated KV cache memory was wasted**,
with internal fragmentation accounting for the majority but external
fragmentation contributing a significant 20-22%. This waste directly
limits system throughput: if only 30-40% of GPU memory is effectively
used, the system can serve only 30-40% as many concurrent requests as
the hardware theoretically permits.

The economic impact is substantial. An NVIDIA A100 GPU with 80GB of
memory, if only 35% is effectively utilized, provides the equivalent of
28GB of usable memory. To achieve the serving capacity that the hardware
should theoretically support, operators must provision 2.8× more GPUs
than necessary, multiplying infrastructure costs proportionally.

### 14.2.2 Page Granularity Mismatch {#section-14.2.2}

Even if fragmentation could be eliminated through perfect allocation
strategies, a fundamental mismatch exists between operating system page
sizes and LLM memory access granularities.

**OS Page Sizes:** Modern operating systems and virtual memory hardware
support a discrete set of page sizes:

- **Base pages:** 4KB (x86-64, ARM64, RISC-V)
- **Huge pages:** 2MB (x86-64 PMD level), 21MB (ARM64), 2MB/4MB (RISC-V)
- **Giant pages:** 1GB (x86-64 PUD level), 512MB (ARM64)

These sizes reflect hardware constraints---they correspond to levels in
the hierarchical page table structure---and decades of optimization for
general-purpose workloads. The 4KB base page size, dating to the VAX-11
architecture, balances internal fragmentation (waste within pages)
against page table size (number of entries needed).

**LLM Memory Granularities:** LLM memory does not naturally align with
these fixed sizes. The fundamental unit of memory in LLM inference is
the *token*, but tokens do not correspond to fixed byte counts:

- Each token generates KV cache entries across all layers and heads
- For OPT-13B: \~800KB per token (across 40 layers, 40 heads)
- For OPT-175B: \~2.4MB per token (across 96 layers, 96 heads)
- Sequences range from tens to thousands of tokens

The mismatch creates several problems. With 4KB pages, each token in
OPT-13B requires \~200 pages (800KB / 4KB). A 2048-token sequence needs
409,600 page table entries. Even with 2MB huge pages, each token
requires \~1 page, and a 2048-token sequence needs 2048 huge pages---far
more than any hardware TLB can cache.

Moreover, LLM memory grows dynamically as tokens are generated. When a
new token is produced, the system must allocate \~800KB (for OPT-13B)
for its KV cache. With 4KB pages, this requires finding and allocating
200 contiguous page table entries. With 2MB pages, the problem is worse:
allocating one 2MB page for 800KB of data wastes 1.2MB (60% internal
fragmentation). The granularity mismatch means that no standard page
size is appropriate.

**Translation Overhead:** The page granularity mismatch directly impacts
translation overhead. Consider accessing the KV cache during attention
computation. For each token position, the model must load key and value
vectors from all layers. For OPT-13B with 40 layers, this means 80
separate memory accesses (40 keys + 40 values) per token position.

With 4KB pages, if each layer\'s KV cache for a token spans multiple
pages (likely, given 800KB per token), each access may incur a TLB miss.
For a 2048-token context, computing attention requires 2048 × 80 =
163,840 memory accesses. Even a 1% TLB miss rate results in 1,638 page
walks, each costing \~200ns, totaling 327µs just for address
translation---significant overhead when the entire attention computation
may take only a few milliseconds.

Kwon et al. (2023) analyzed this overhead by comparing memory access
patterns in traditional pre-allocation systems versus their proposed
block-based approach. They found that with 4KB pages, memory accesses to
the KV cache experienced TLB miss rates of 15-25% due to the large
working set and non-contiguous allocation patterns. With 2MB huge pages,
miss rates dropped to 2-5%, but the waste from internal fragmentation
increased significantly.

### 14.2.3 Traditional Workloads vs. LLM Access Patterns {#section-14.2.3}

To understand why existing memory management techniques fail for LLMs,
it is instructive to compare LLM access patterns with those of
traditional memory-intensive applications that virtual memory systems
were designed to support.

**Database Systems:** Modern database systems (e.g., PostgreSQL, MySQL)
are heavily memory-intensive and have been well-served by traditional
virtual memory. Database access patterns include:

- **B-tree index accesses:** Random accesses to tree nodes, but with
  strong temporal locality. Hot nodes (near root) accessed repeatedly.
  Working set: inner nodes of active indexes, often 1-8GB.
- **Sequential table scans:** Linear traversal of table pages, easily
  prefetched. Even large scans (100GB+) are sequential and benefit from
  readahead.
- **Hash table lookups:** Random accesses, but hash tables sized to fit
  in memory. Effective working set after warmup: 2-16GB for typical OLTP
  workloads.
- **Sort buffers:** Temporary allocations for query processing, released
  after query completion. Short-lived, size known in advance.

The key characteristics: (1) working sets, while large, fit in server
RAM after an initial warmup period, (2) temporal locality is
strong---frequently accessed data (hot indexes) is accessed repeatedly,
and (3) memory allocations are relatively stable once the database is
warmed up. These patterns align well with LRU-based page replacement and
TLB caching.

**LLM Inference:** LLM serving has fundamentally different
characteristics:

- **Model weight accesses:** Sequential traversal through 350GB (GPT-3),
  *every forward pass*. No temporal locality---weights accessed in layer
  order, then not reused until next forward pass. Working set: entire
  model.
- **KV cache accesses:** For each new token, access KV cache from all
  previous tokens in the sequence. Access pattern is sequential through
  the cache but grows with each token. Working set: all previous
  tokens\' KV cache, growing unboundedly.
- **Dynamic allocation:** KV cache allocated incrementally as tokens are
  generated. Allocation size unknown in advance (depends on when
  generation terminates). Lifetime: duration of request, which may be
  seconds to minutes.
- **No reuse across requests:** Each request has independent KV cache.
  No inter-request locality. Only model weights are shared across
  requests.

The critical differences: (1) working sets *never* fit in GPU
memory---memory oversubscription is mandatory, (2) memory accesses are
streaming (single-pass through data) with minimal temporal reuse, and
(3) allocations are dynamic and request-dependent, making traditional
prefetching ineffective.

**Quantitative Comparison:** Table 14.1 summarizes these differences
quantitatively, drawing from published characterizations of database
workloads (TPC-C, TPC-H benchmarks) and LLM serving workloads (Kwon et
al., 2023).

| Characteristic | Database (PostgreSQL) | LLM (GPT-3 Serving) |
| --- | --- | --- |
| **Working Set Size** | 2-16GB (typical OLTP) | 350-500GB (model + KV cache) |
| **Memory:Compute Ratio** | CPU-bound (joins, sorts) | Memory-bound (50-70% time in memory access) |
| **Temporal Locality** | High (hot indexes reused) | Low (single-pass streaming) |
| **Spatial Locality** | High (sequential scans, clustered indexes) | High (layer-sequential) but working set too large |
| **Allocation Patterns** | Stable (buffers sized at startup) | Dynamic (grows per-token, unpredictable) |
| **Page Reuse (LRU effectiveness)** | 70-90% hit rate after warmup | \<20% hit rate (streaming access) |
| **TLB Miss Tolerance** | High (CPU cycles cheap, query latency seconds) | Low (GPU idle during translation, latency critical) |
| : **Table 14.1:** Access Pattern Com | arison - Database vs. LLM |  |
| Workloads |  |  |


The comparison reveals why techniques successful for database workloads
fail for LLMs. Database workloads exhibit the strong temporal and
spatial locality that LRU page replacement and TLB caching exploit.
After a warmup period, hot pages remain resident and TLB hit rates
exceed 90%. In contrast, LLM workloads are fundamentally *streaming*:
data flows through memory once and is not reused within a request.
Memory oversubscription is not a pathological edge case but the normal
operating mode.

Furthermore, the cost of a TLB miss differs dramatically. In a database
system, a CPU remains productive during a page walk---it can switch
threads, speculatively execute other instructions, or at worst idle for
200ns (representing perhaps 200-400 instruction slots). In
GPU-accelerated LLM inference, a TLB miss may stall thousands of GPU
threads simultaneously. Modern GPUs achieve high throughput through
massive parallelism---thousands of threads executing in lock-step. A TLB
miss that stalls memory access stalls the entire warp or wavefront,
idling tens of thousands of compute cycles. The same 200ns page walk
overhead that is tolerable in a CPU context is catastrophic in GPU
context.

**Implications for Memory Management:** These fundamental differences in
access patterns and cost structures explain why traditional virtual
memory systems---optimized over decades for database, scientific
computing, and general-purpose workloads---are poorly suited to LLM
serving:

- LRU page replacement fails because pages are not reused (streaming
  access).
- Hardware prefetching fails because allocation patterns are
  request-dependent and unpredictable.
- TLB caching fails because working sets exceed TLB reach by 100-500×.
- Fixed page sizes (4KB, 2MB, 1GB) mismatch natural data granularities
  (variable-length token sequences).

The failure is not incidental or fixable through parameter tuning. It
reflects a fundamental mismatch between the assumptions embedded in
traditional virtual memory design and the characteristics of modern LLM
workloads. This mismatch motivates the software-managed memory
approaches examined in the following sections, which abandon traditional
OS-managed paging in favor of application-controlled memory allocation
with granularities and policies tailored to LLM access patterns.

------------------------------------------------------------------------

## 14.3 Software-Managed Memory: The vLLM System {#section-14.3}

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
<defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
<marker id="a" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
<marker id="ao" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
<marker id="ag" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker></defs>
<text x="450" y="26" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Figure 14.1 - vLLM PagedAttention: Software Memory Management for LLM KV Cache</text>
<rect x="30" y="40" width="400" height="260" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#E65100; stroke-width:1.5" />
<rect x="30" y="40" width="400" height="28" rx="6" style="fill:#E65100" />
<text x="230" y="59" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">Traditional LLM KV Cache: Fragmentation Problem</text>
<text x="230" y="90" style="fill:#212121; font-size:13; text-anchor:middle">Pre-allocate max_seq_len per request</text>
<text x="230" y="108" style="fill:#212121; font-size:13; text-anchor:middle">80 GB GPU: GPT-3 KV at 2048 tokens = 1 GB/req</text>
<rect x="48" y="120" width="76" height="50" rx="3" style="fill:#1565C0" />
<text x="86" y="142" style="fill:white; font-size:11; text-anchor:middle">Req A</text>
<text x="86" y="158" style="fill:white; font-size:11; text-anchor:middle">512 tok</text>
<rect x="132" y="120" width="76" height="50" rx="3" style="fill:#9E9E9E; stroke:#9E9E9E; fill-opacity:0.4; stroke-dasharray:3,2" />
<text x="170" y="150" style="fill:#9E9E9E; font-size:11; text-anchor:middle">wasted</text>
<rect x="216" y="120" width="76" height="50" rx="3" style="fill:#1565C0" />
<text x="254" y="142" style="fill:white; font-size:11; text-anchor:middle">Req B</text>
<text x="254" y="158" style="fill:white; font-size:11; text-anchor:middle">800 tok</text>
<rect x="300" y="120" width="76" height="50" rx="3" style="fill:#9E9E9E; stroke:#9E9E9E; fill-opacity:0.4; stroke-dasharray:3,2" />
<text x="338" y="150" style="fill:#9E9E9E; font-size:11; text-anchor:middle">wasted</text>
<text x="230" y="192" style="fill:#E65100; font-size:13; text-anchor:middle">60-70% GPU memory wasted on internal fragmentation</text>
<text x="230" y="212" style="fill:#E65100; font-size:13; text-anchor:middle">Result: 2-4x fewer concurrent requests possible</text>
<text x="230" y="240" style="fill:#212121; font-size:13; text-anchor:middle">TLB reach crisis: 2048 tokens x layers x heads</text>
<text x="230" y="258" style="fill:#212121; font-size:13; text-anchor:middle">= millions of pages, far exceeds TLB capacity</text>
<text x="230" y="282" style="fill:#616161; font-size:12; text-anchor:middle">Each token lookup: TLB miss storm, 100-300 ns each</text>
<rect x="460" y="40" width="410" height="260" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#00796B; stroke-width:1.5" />
<rect x="460" y="40" width="410" height="28" rx="6" style="fill:#00796B" />
<text x="665" y="59" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">vLLM PagedAttention: OS-Inspired Solution</text>
<text x="665" y="90" style="fill:#212121; font-size:13; text-anchor:middle">KV Cache divided into fixed blocks (pages)</text>
<text x="665" y="108" style="fill:#212121; font-size:13; text-anchor:middle">Block table maps logical -&gt; physical blocks</text>
<rect x="475" y="118" width="80" height="36" rx="3" style="fill:#1565C0" />
<text x="515" y="134" style="fill:white; font-size:11; text-anchor:middle">Req A</text>
<text x="515" y="148" style="fill:white; font-size:11; text-anchor:middle">Block 0,3,7</text>
<rect x="475" y="160" width="80" height="36" rx="3" style="fill:#1565C0" />
<text x="515" y="176" style="fill:white; font-size:11; text-anchor:middle">Req B</text>
<text x="515" y="190" style="fill:white; font-size:11; text-anchor:middle">Block 1,4</text>
<rect x="475" y="202" width="80" height="36" rx="3" style="fill:#1565C0" />
<text x="515" y="218" style="fill:white; font-size:11; text-anchor:middle">Req C</text>
<text x="515" y="232" style="fill:white; font-size:11; text-anchor:middle">Block 2,5,6</text>
<line x1="555" y1="136" x2="575" y2="136" marker-end="url(#a)" style="stroke:#1565C0; stroke-width:1.5"></line>
<line x1="555" y1="178" x2="575" y2="178" marker-end="url(#a)" style="stroke:#1565C0; stroke-width:1.5"></line>
<line x1="555" y1="220" x2="575" y2="220" marker-end="url(#a)" style="stroke:#1565C0; stroke-width:1.5"></line>
<rect x="575" y="118" width="274" height="125" rx="4" style="fill:#00796B; stroke:#00796B; fill-opacity:0.15" />
<text x="712" y="138" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Physical Block Pool</text>
<rect x="585" y="146" width="56" height="28" rx="2" style="fill:#00796B" />
<text x="613" y="165" style="fill:white; font-size:12; text-anchor:middle">Blk 0</text>
<rect x="649" y="146" width="56" height="28" rx="2" style="fill:#1565C0" />
<text x="677" y="165" style="fill:white; font-size:12; text-anchor:middle">Blk 1</text>
<rect x="713" y="146" width="56" height="28" rx="2" style="fill:#E65100" />
<text x="741" y="165" style="fill:white; font-size:12; text-anchor:middle">Blk 2</text>
<rect x="777" y="146" width="56" height="28" rx="2" style="fill:#00796B" />
<text x="805" y="165" style="fill:white; font-size:12; text-anchor:middle">Blk 3</text>
<rect x="585" y="182" width="56" height="28" rx="2" style="fill:#1565C0" />
<text x="613" y="201" style="fill:white; font-size:12; text-anchor:middle">Blk 4</text>
<rect x="649" y="182" width="56" height="28" rx="2" style="fill:#E65100" />
<text x="677" y="201" style="fill:white; font-size:12; text-anchor:middle">Blk 5</text>
<rect x="713" y="182" width="56" height="28" rx="2" style="fill:#E65100" />
<text x="741" y="201" style="fill:white; font-size:12; text-anchor:middle">Blk 6</text>
<rect x="777" y="182" width="56" height="28" rx="2" style="fill:#00796B" />
<text x="805" y="201" style="fill:white; font-size:12; text-anchor:middle">Blk 7</text>
<text x="712" y="232" style="fill:#212121; font-size:12; text-anchor:middle">No internal waste: blocks used fully</text>
<text x="665" y="263" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Result: 2.2x more concurrent requests served</text>
<text x="665" y="282" style="fill:#616161; font-size:12; text-anchor:middle">Prefix caching: shared blocks across same-prompt requests</text>
<rect x="30" y="320" width="840" height="218" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
<rect x="30" y="320" width="840" height="28" rx="6" style="fill:#212121" />
<text x="450" y="339" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">Direct Segment Addressing: Bypass the MMU for LLM Inference</text>
<text x="230" y="372" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Standard Virtual Memory</text>
<text x="230" y="390" style="fill:#212121; font-size:13; text-anchor:middle">Every access: VA -&gt; TLB -&gt; PTE -&gt; PA</text>
<text x="230" y="408" style="fill:#212121; font-size:13; text-anchor:middle">LLM model weights: 70 GB, millions of PTEs</text>
<text x="230" y="426" style="fill:#212121; font-size:13; text-anchor:middle">TLB reach at 4 KB: 6 MB (far less than 70 GB)</text>
<text x="230" y="444" style="fill:#E65100; font-size:13; text-anchor:middle">TLB miss rate: 40-60% for weight tensors</text>
<text x="230" y="462" style="fill:#E65100; font-size:13; text-anchor:middle">Each miss: 100-300 ns = major inference bottleneck</text>
<line x1="440" y1="352" x2="440" y2="510" style="stroke:#9E9E9E; stroke-width:1"></line>
<text x="665" y="372" style="fill:#1565C0; font-size:14; font-weight:bold; text-anchor:middle">Direct Segment (Basu et al.)</text>
<text x="665" y="390" style="fill:#212121; font-size:13; text-anchor:middle">One dedicated hardware register: base + limit + offset</text>
<text x="665" y="408" style="fill:#212121; font-size:13; text-anchor:middle">Covers entire model in 1 TLB entry (1 GB segment)</text>
<text x="665" y="426" style="fill:#212121; font-size:13; text-anchor:middle">VA in [base, base+limit]: bypass TLB entirely</text>
<text x="665" y="444" style="fill:#00796B; font-size:13; text-anchor:middle">TLB miss rate for weights: ~0% (one segment covers all)</text>
<text x="665" y="462" style="fill:#00796B; font-size:13; text-anchor:middle">8-16% total inference throughput improvement</text>
<text x="665" y="492" style="fill:#616161; font-size:12; text-anchor:middle">Tradeoff: loses fine-grained per-page protection for that region</text>
</svg>
</div>
<figcaption><strong>Figure 14.1:</strong> vLLM PagedAttention: software
memory management bypassing MMU fragmentation limits. Traditional LLM
serving pre-allocates contiguous KV-cache regions per request, wasting
60-70% of GPU memory. PagedAttention divides the KV cache into
fixed-size blocks managed by a software block table analogous to OS page
tables. Direct Segment Addressing extends this by mapping the entire 70
GB model weights to a single hardware register, eliminating TLB misses
for weight tensors entirely.</figcaption>
</figure>

The vLLM system, introduced by Kwon et al. at SOSP 2023, represents a
fundamental rethinking of memory management for LLM serving. Rather than
relying on operating system paging mechanisms, vLLM implements a
complete software-managed memory system operating entirely in user
space. This section provides a comprehensive technical analysis of
vLLM\'s architecture, algorithm, and experimental results as documented
in the SOSP 2023 publication.

### 14.3.1 The PagedAttention Algorithm {#section-14.3.1}

At the core of vLLM is the PagedAttention algorithm, which applies
virtual memory concepts to GPU KV cache management. The key insight, as
stated by the authors, is that \"the memory allocation and management
problem in LLM serving is fundamentally similar to the classical virtual
memory and paging problem in operating systems\" (Kwon et al., 2023,
Section 1).

**Conceptual Foundation:** Traditional attention mechanisms in
transformers assume that key and value vectors are stored in contiguous
memory. For a sequence of length *n*, computing attention for a query at
position *i* requires accessing keys and values from all positions 1
through *i*. In standard implementations, these are stored in contiguous
tensors, which creates the fragmentation problems documented in Section
14.2.

PagedAttention relaxes the contiguity requirement. Instead of storing
all keys and values for a sequence in one contiguous allocation, the
algorithm partitions the KV cache into fixed-size **blocks**, each
containing keys and values for a fixed number of tokens. These blocks
can be stored non-contiguously in GPU memory, with a mapping table
tracking their physical locations.

**Block Structure:** As described in Section 4.1 of the vLLM paper, each
block contains KV cache data for a configurable number of tokens (the
**block size**, typically 16 or 32). For a model with *L* layers and
hidden dimension *d*, each token position requires storing 2 × *L* × *d*
values (keys and values across all layers). A block storing *B* tokens
therefore contains 2 × *L* × *d* × *B* values.

For OPT-13B with 40 layers, dimension 5120, and block size 16, each
block stores:


    Block size = 2 × 40 × 5120 × 16 × 2 bytes (FP16)
               = 2 × 40 × 5120 × 32
               = 13,107,200 bytes
               ≈ 12.5 MB per block

**Logical vs. Physical Blocks:** The system maintains a distinction
between **logical blocks** and **physical blocks**. Logical blocks are
the application\'s view of memory---a sequence uses logical blocks 0, 1,
2, \... as it generates tokens. Physical blocks are actual memory
allocations in GPU VRAM. A **block table** maps each logical block to a
physical block, analogous to how page tables map virtual pages to
physical page frames.

During attention computation, when the algorithm needs to access the key
at layer *l* for token position *t*, it:

1.  Computes the logical block number: `logical_block = t / block_size`
2.  Looks up the physical block:
    `physical_block = block_table[logical_block]`
3.  Computes the offset within the block: `offset = t % block_size`
4.  Accesses the key at: `physical_block.data[layer][offset]`

This indirection---consulting the block table to translate logical to
physical block numbers---is performed in software, not hardware. The
CUDA kernel implementing PagedAttention receives pointers to physical
blocks and explicitly performs the translation as part of the attention
computation.

**Attention Computation:** The modified attention algorithm, as
presented in Algorithm 1 of the paper, computes attention scores in a
block-aware manner. For a query vector **q** at position *i*, computing
attention over positions 1 through *i* involves:


    for each logical block b from 0 to i/B:
        physical_block = block_table[b]
        for each token t in physical_block:
            key = physical_block.keys[layer][t]
            score = q · key
            attention_scores[b * B + t] = score
        
    softmax(attention_scores)

    for each logical block b from 0 to i/B:
        physical_block = block_table[b]
        for each token t in physical_block:
            value = physical_block.values[layer][t]
            output += attention_scores[b * B + t] * value

The key modification from standard attention is that instead of assuming
contiguous storage for all keys and values, the algorithm iterates over
blocks and looks up each block\'s physical location before accessing its
data. This adds a level of indirection but enables non-contiguous
allocation.

### 14.3.2 Memory Management Architecture {#section-14.3.2}

The PagedAttention algorithm requires supporting infrastructure for
memory allocation, block table management, and block lifecycle
management. This section examines these components based on Section
4.2-4.4 of the vLLM paper.

**Block Table Management:** Each active request (sequence) maintains its
own block table mapping its logical blocks to physical blocks. The block
table is a simple array structure:


    struct BlockTable {
        int num_logical_blocks;
        int* physical_block_ids;  // Array of size num_logical_blocks
        int blocks_used;          // How many blocks currently allocated
    }

When a request begins, it is allocated an empty block table. As tokens
are generated and the KV cache grows, logical blocks are added to the
table and mapped to physical blocks allocated from a free pool.

The block table is small---for a 2048-token sequence with block size 16,
the table contains 128 entries, requiring only 512 bytes (128 × 4 bytes
per integer). This is negligible compared to the KV cache data itself
(which would be 128 × 12.5MB = 1.6GB for OPT-13B), making the metadata
overhead insignificant.

**Physical Block Allocator:** The system maintains a global free list of
available physical blocks. At system initialization, all GPU memory
designated for KV cache (after allocating space for model weights and
activations) is partitioned into fixed-size physical blocks, and their
IDs are added to the free list.

The allocator, described in Section 4.3, implements a simple strategy:


    function allocate_block_for_request(request_id):
        if free_list is empty:
            # Out of memory - must evict or reject
            return null
        
        physical_block = free_list.pop()
        request_blocks[request_id].append(physical_block)
        return physical_block

    function free_request(request_id):
        for physical_block in request_blocks[request_id]:
            free_list.push(physical_block)
        delete request_blocks[request_id]

This straightforward allocation scheme works because blocks are uniform
size. Unlike variable-size allocation (which requires complex algorithms
to minimize fragmentation), fixed-size allocation never
fragments---every freed block can immediately satisfy any allocation
request. This is analogous to how slab allocators work in operating
system kernels.

**Block Allocation Timing:** Blocks are allocated incrementally as
tokens are generated. When a new token is produced:

1.  Check if the current last logical block has space (\< block_size
    tokens stored)
2.  If yes: write the new token\'s KV cache into the existing block
3.  If no: allocate a new physical block, append it to the block table,
    write to the new block

This incremental allocation means that memory is consumed only as
needed. A request that terminates after 100 tokens consumes only
ceil(100 / block_size) blocks, not pre-allocated space for thousands of
tokens.

**Memory Utilization Analysis:** The vLLM paper (Section 5.3) analyzes
memory waste quantitatively. The only source of waste is **internal
fragmentation** in the last block of each request. If a request has *n*
tokens and block size *B*, it uses ceil(*n* / *B*) blocks. The last
block contains *n* mod *B* tokens, wasting *B* - (*n* mod *B*) token
slots.

In the worst case (request length is one more than a multiple of *B*),
nearly an entire block is wasted. On average, assuming uniformly
distributed sequence lengths, half a block per request is wasted. For
block size 16 and 128 concurrent requests, this represents 128 × 8 =
1024 token slots wasted, or 1024 × 800KB = 819MB for OPT-13B---less than
4% of the 20+ GB typically used for KV cache in a batch.

Kwon et al. (2023) measured actual memory waste across workloads with
varying sequence length distributions (Section 6, Figure 7). They found:

- **Block size 16:** 3.5% average waste, 7.2% worst case
- **Block size 32:** 2.1% average waste, 4.8% worst case
- **Block size 64:** 1.3% average waste, 2.9% worst case

The trade-off is that larger blocks reduce metadata overhead and waste
but decrease granularity. Block size 16 was chosen as a practical
compromise providing \<4% waste while maintaining fine-grained
allocation.

### 14.3.3 Copy-on-Write and Memory Sharing {#section-14.3.3}

A sophisticated feature of vLLM is its support for memory sharing across
requests that share common prefixes. This is particularly valuable for
LLM serving systems where many requests begin with the same prompt
(e.g., system messages, few-shot examples, or conversation history).

**Motivation:** Consider a chatbot system where every request begins
with a system prompt: \"You are a helpful AI assistant. Answer questions
accurately and concisely.\" This prompt might be 20-30 tokens and is
identical across all requests. Without sharing, every concurrent request
would store its own copy of this prefix\'s KV cache, wasting memory
proportionally to the batch size.

**Reference Counting:** As described in Section 4.4 of the paper, vLLM
implements copy-on-write (COW) semantics for blocks. Each physical block
maintains a reference count indicating how many logical blocks (across
all requests) map to it. When a new request begins and its prefix
matches an existing request:

1.  The new request\'s block table is initialized to point to the same
    physical blocks as the existing request
2.  Reference counts on those physical blocks are incremented
3.  Both requests share the physical blocks for the common prefix

This sharing is transparent to the attention computation---both
requests\' block tables map to the same physical blocks, so their
attention kernels access the same memory.

**Copy-on-Write Mechanism:** Sharing continues until a request needs to
modify a shared block. This occurs when:

- A request generates a new token that fills the last shared block
  (requiring a new block for subsequent tokens)
- Two requests with the same prefix diverge (different tokens generated
  at the same position)

When modification is needed, the system implements copy-on-write:


    function append_token_to_request(request_id, token):
        last_logical_block = get_last_block(request_id)
        physical_block = block_table[request_id][last_logical_block]
        
        if reference_count[physical_block] > 1:
            # Block is shared - must copy before modifying
            new_block = allocate_block()
            copy_data(physical_block, new_block)
            block_table[request_id][last_logical_block] = new_block
            reference_count[physical_block] -= 1
            reference_count[new_block] = 1
            physical_block = new_block
        
        # Now safe to modify - this request has exclusive access
        write_token_kv_cache(physical_block, token)

This ensures that shared blocks are never modified while they have
multiple references, preserving correctness.

**Measured Benefits:** The vLLM paper (Section 6.3, Figure 9) evaluates
memory savings from sharing on workloads with common prefixes. For a
dataset where 50% of requests share a 100-token system prompt:

- **Without sharing:** 100 tokens × 128 requests = 12,800 token slots
  (10.2GB for OPT-13B)
- **With sharing:** 100 tokens + (128 × unique portions) ≈ 100 + 6,400 =
  6,500 token slots (5.2GB)
- **Savings:** 49% reduction in memory for shared prefix

For production serving systems with standardized prompts, this
translates to significantly higher batch sizes and throughput. The paper
notes that the sharing mechanism is particularly effective for:

- **Few-shot learning:** Requests sharing few-shot examples in the
  prompt
- **Conversational systems:** Requests in the same conversation sharing
  conversation history
- **Parallel sampling:** Multiple outputs generated from the same prompt
  (beam search, temperature sampling)

For parallel sampling with beam width 4, vLLM shares the prompt KV cache
across all 4 beams, reducing memory consumption by 75% for the prompt
portion compared to independent copies.

### 14.3.4 Experimental Evaluation {#section-14.3.4}

The vLLM paper (Section 6) presents extensive experimental evaluation.
This section summarizes the key results as reported in the publication.

**Experimental Setup:** Experiments used NVIDIA A100 GPUs (40GB or 80GB
variants) running production LLM serving workloads. Models tested
include:

- OPT-13B (40 layers, 5120 dimension)
- OPT-175B (96 layers, 12288 dimension)
- LLaMA-7B (32 layers, 4096 dimension)
- LLaMA-13B (40 layers, 5120 dimension)

Workloads consisted of request traces with varying input lengths
(256-2048 tokens) and output lengths (16-256 tokens). The baseline
systems for comparison were:

- **FasterTransformer:** NVIDIA\'s optimized inference library with
  static pre-allocation
- **Orca:** Academic system with continuous batching (Yu et al., 2022)
- **HuggingFace Transformers:** Standard PyTorch implementation

**Throughput Results:** Table 2 in the vLLM paper reports throughput
measured in requests per second for various models and input/output
length combinations. Representative results for OPT-13B:

| Input/Output Length | HF Transformers | FasterTransformer | Orca | vLLM | vLLM Speedup vs. FT |
| --- | --- | --- | --- | --- | --- |
| 256/16 | 1.2 | 2.1 | 3.5 | 5.8 | 2.76× |
| 512/32 | 0.8 | 1.5 | 2.4 | 4.2 | 2.80× |
| 1024/64 | 0.4 | 0.9 | 1.5 | 2.8 | 3.11× |
| 2048/128 | 0.2 | 0.5 | 0.9 | 1.8 | 3.60× |
| : **Table 14.2:** Thr | ughput Comparison | (requests/second, O | T-13B | n |  |
| A100 80GB) |  |  |  |  |  |


The results show that vLLM achieves 2.76-3.60× higher throughput
compared to FasterTransformer (a highly optimized baseline) across
sequence lengths. The speedup increases with longer sequences because
memory efficiency becomes more critical as KV cache size grows.

For larger models (OPT-175B), where memory constraints are more severe,
speedups are even more pronounced. The paper reports up to 4.2×
throughput improvement for this model, as the memory efficiency gains
from eliminating fragmentation allow much larger batch sizes.

**Memory Efficiency:** Figure 7 in the paper visualizes GPU memory
utilization for different systems serving the same workload. For OPT-13B
with a batch of 32 requests (average 1024 tokens each):

- **FasterTransformer:** 32% memory utilization (pre-allocated for max
  length, much unused)
- **Orca:** 51% utilization (dynamic allocation but contiguous per
  request)
- **vLLM:** 89% utilization (block-based allocation minimizes waste)

The 89% utilization means that vLLM can fit 2.78× more requests in the
same memory compared to FasterTransformer (89% / 32%), directly
translating to the measured throughput improvements.

**Latency Analysis:** Section 6.2 of the paper examines per-request
latency. For single-request latency (no batching), vLLM and
FasterTransformer perform comparably---within 2-5% of each other. The
PagedAttention algorithm\'s indirection adds minimal overhead (discussed
below). Latency benefits appear when serving batches, as vLLM can fit
more requests per batch without exceeding memory capacity.

**Sharing Benefits:** Section 6.3 evaluates copy-on-write sharing
effectiveness using parallel sampling workloads (generating multiple
outputs from one prompt). For beam search with width 8:

- **Without sharing:** 8 independent copies of prompt KV cache
- **With sharing:** 1 shared copy of prompt KV cache + 8 separate
  continuations

For a 512-token prompt generating 128-token outputs, sharing reduces
memory consumption by 64% (8× reduction for prompt portion, no reduction
for output portions). This allows increasing batch size from 16 to 44
requests, improving throughput by 2.75×.

### 14.3.5 Implementation Details and Overhead Analysis {#section-14.3.5}

Section 5 of the vLLM paper discusses implementation, particularly the
CUDA kernel modifications required for PagedAttention.

**Kernel Modifications:** Standard attention kernels assume contiguous
storage of key and value tensors. The PagedAttention kernel must:

1.  Receive block table pointers (mapping logical to physical blocks)
2.  For each attention computation, translate logical block → physical
    block
3.  Access key/value data from the appropriate physical block

The paper reports that the modified kernel adds approximately 10-20
instructions per block access (block table lookup plus address
computation). On modern GPUs with thousands of concurrent threads and
deep pipelines, this overhead is largely hidden by other computation and
memory latency.

**Measured Overhead:** To isolate the overhead of indirection, the
authors ran microbenchmarks comparing standard attention (contiguous
storage) versus PagedAttention (block table lookup) on synthetic
workloads with identical data access patterns (Section 5.2, Table 1).

For OPT-13B attention computation over 2048 tokens:

- **Standard attention:** 3.42ms per layer
- **PagedAttention (block size 16):** 3.58ms per layer
- **Overhead:** 4.7%

The 4.7% overhead is more than compensated by the throughput gains from
higher batch sizes. Where standard systems serve batch size 16, vLLM
serves batch size 44 (2.75× larger), resulting in net throughput
improvement despite the per-request overhead.

**Memory Bandwidth Utilization:** The paper analyzes whether block-based
storage negatively impacts memory bandwidth efficiency. In theory,
scattered accesses could reduce effective bandwidth if they defeat
hardware prefetching or caching.

In practice, Section 5.3 reports that memory bandwidth utilization
remains high (\>90% of theoretical peak) for vLLM. The key is that
within each block, data is stored contiguously and accessed
sequentially. The attention kernel processes an entire block before
moving to the next, so prefetchers can effectively predict accesses
within blocks. The non-contiguity between blocks does not significantly
harm bandwidth because transitions between blocks are infrequent (once
per 16 or 32 tokens).

**Block Size Selection:** The choice of block size involves trade-offs:

- **Smaller blocks:** Finer allocation granularity, less waste, more
  metadata overhead and indirection
- **Larger blocks:** Less metadata and indirection, coarser granularity,
  more waste in last block

Figure 8 in the paper shows a sensitivity analysis varying block size
from 8 to 128 tokens. Key findings:

- **Block size 8:** 5.1% memory waste, 6.8% compute overhead (too much
  indirection)
- **Block size 16:** 3.5% memory waste, 4.7% compute overhead (balanced)
- **Block size 32:** 2.1% memory waste, 3.2% compute overhead (better
  for long sequences)
- **Block size 64:** 1.3% memory waste, 2.1% compute overhead (but
  coarser allocation)

The authors selected block size 16 as the default based on these
results, providing a good balance for typical sequence length
distributions. For workloads with predominantly long sequences, block
size 32 may be preferable.

> **Summary of vLLM Results:** As reported by Kwon et al. (SOSP 2023),
> vLLM achieves 2-4× throughput improvement over existing serving
> systems through block-based memory management that reduces memory
> waste from 62-80% to \<4%. The PagedAttention algorithm adds 4.7%
> computational overhead, which is more than offset by the ability to
> serve 2-3× larger batch sizes. Copy-on-write sharing provides
> additional benefits for workloads with common prefixes, reducing
> memory consumption by up to 64% for such workloads.

------------------------------------------------------------------------

### 14.3.6 Proactive Memory Scheduling (MSched) {#section-14.3.6}

> **Note on Source Material:** This section discusses MSched
> (arXiv:2512.24637v1, January 2026), which is currently available as a
> preprint and has not yet undergone peer review. The reader should be
> aware that the results presented await formal validation through the
> conference review process.

#### The Memory Oversubscription Challenge

While vLLM addresses memory fragmentation through block-based
allocation, it assumes the working set fits within available GPU memory.
For scenarios where memory demand exceeds capacity---common in
multi-tenant cloud environments or when serving multiple large
models---systems must page memory between GPU HBM and host DRAM or
storage.

Traditional GPU paging using NVIDIA\'s Unified Memory or similar
mechanisms suffers from reactive demand paging. When a kernel accesses
memory not present in HBM, a page fault occurs, trapping to the driver
(\~50-100µs), initiating a DMA transfer from host DRAM (200-500µs at
PCIe Gen4), and stalling the kernel until transfer completes. With
thousands of GPU threads executing in lockstep, a single page fault can
idle the entire compute pipeline.

For LLM workloads with 350GB models on 80GB GPUs, this results in
continuous page faulting. The MSched work reports that naive demand
paging creates a 78× slowdown compared to native execution---effectively
making memory oversubscription impractical for production deployments.

**Reactive Paging Pattern:**

    GPU Kernel Execution:
      Access address 0x1234_5678
      → Page fault (not in HBM)
      → Trap to driver (50µs)
      → DMA transfer from host (200-500µs)
      → Resume kernel
      → Access address 0x1234_9ABC
      → Another page fault
      [Sequential faults dominate execution]

This sequential fault-then-transfer pattern means that 97-99% of
execution time is spent handling faults rather than performing
computation.

#### MSched\'s Proactive Approach

MSched proposes eliminating reactive page faults through proactive
memory scheduling. The key insight is that GPU kernel memory access
patterns are highly predictable for AI workloads---neural networks
execute layer-by-layer with well-defined tensor dependencies.

**Architecture:**

1.  **Kernel Argument Interception:** When a CUDA kernel launches, the
    system intercepts the argument buffer containing pointers to input
    tensors, output buffers, and intermediate activations.
2.  **Working Set Prediction:** By analyzing tensor shapes, kernel type
    (matrix multiply, attention, convolution), and execution history,
    the system predicts which memory pages will be accessed during
    execution.
3.  **Proactive Transfer:** During the context switch from kernel N to
    kernel N+1, MSched initiates DMA transfers to preload the predicted
    working set for kernel N+1 while kernel N completes execution. This
    overlaps computation with memory transfer.
4.  **Fault Coalescing:** Any remaining page faults are
    batched---multiple faults collected before initiating transfers,
    reducing per-fault overhead from 200-500µs (sequential) to 50-100µs
    (batched).

**Execution Flow:**

    Context Switch (Kernel N → Kernel N+1):
      1. Kernel N completes
      2. Analyze Kernel N+1 arguments:
         - Input tensor: 256GB @ 0xA000_0000
         - Output buffer: 64GB @ 0xB000_0000
      3. Predict access pattern:
         - Sequential scan of input → prefetch all pages
         - Write-only output → no prefetch needed
      4. Initiate background prefetch
      5. Launch Kernel N+1:
         - Pages arriving as kernel executes
         - Overlap transfer with computation

The system reports achieving 99.75% prediction accuracy (0.25% false
negative rate, 0% false positive rate) through template-based prediction
that exploits the structured nature of neural network execution.

#### Experimental Evaluation {#experimental-evaluation}

**Configuration:**

- Hardware: NVIDIA A100 80GB GPU
- Memory limit: 32GB enforced through cgroups
- Workloads: LLaMA-7B, LLaMA-13B, ResNet-50, BERT-Large
- Oversubscription levels: 150%, 200%, 300% (memory demand / HBM
  capacity)
- Baseline: NVIDIA Unified Memory with standard demand paging

**Performance Results:**

The paper reports substantial improvements over demand paging across
different oversubscription levels:

| Workload | Oversubscription | Demand Paging | MSched | Speedup |
| --- | --- | --- | --- | --- |
| LLaMA-7B | 150% | 1.2 tok/s | 69.5 tok/s | 57.88× |
| LLaMA-7B | 200% | 0.8 tok/s | 35.8 tok/s | 44.79× |
| LLaMA-7B | 300% | 0.5 tok/s | 16.8 tok/s | 33.60× |
| ResNet-50 | 150% | 12 img/s | 132 img/s | 11.05× |
| BERT-Large | 200% | 18 seq/s | 168 seq/s | 9.35× |


**Comparison with Native Performance:**

- LLaMA-7B native (no oversubscription): 93.8 tok/s
- LLaMA-7B with MSched @ 150%: 69.5 tok/s
- **Sustained performance: 74.09% of native**

The results indicate that proactive scheduling can maintain reasonable
performance even under significant memory pressure, whereas demand
paging degrades catastrophically. The 57× speedup over demand paging for
LLM workloads represents a dramatic improvement, suggesting that careful
prediction and prefetching can largely eliminate the traditional paging
overhead.

**Prediction Accuracy:**

- Template-based prediction: 99.75% accuracy
- False negative rate: 0.25% (missed predictions)
- False positive rate: 0% (no unnecessary transfers)

The high prediction accuracy stems from neural network structure:
layer-by-layer execution with explicit tensor dependencies encoded in
kernel arguments. This predictability distinguishes AI workloads from
general-purpose applications where access patterns are more complex.

#### System Design Considerations

**Implementation Level:** MSched operates at the OS/driver level,
intercepting kernel launches and managing page placement transparently
to applications. This provides several advantages: no application
modifications required, compatibility with existing CUDA code, ability
to optimize across multiple concurrent applications, and access to
kernel metadata for prediction.

**Memory Transfer Optimization:** The system exploits several
opportunities for optimization:

1.  **Batched Transfers:** Multiple pages transferred in single DMA
    operation
2.  **Transfer Pipelining:** Overlapping multiple transfers using
    multiple DMA channels
3.  **Priority-Based Scheduling:** Pages predicted to be accessed
    soonest transferred first
4.  **Adaptive Prefetch Distance:** Adjusting how far ahead to prefetch
    based on transfer bandwidth and kernel execution time

**Interaction with Existing Systems:** MSched\'s proactive scheduling
could potentially complement vLLM\'s block-based allocation: vLLM
manages KV cache allocation efficiently within available memory, while
MSched handles page placement when total working set exceeds capacity.
However, no evaluation of this combination has been published yet.

#### Comparison with Related Work

**Versus vLLM:** The two systems address different aspects of memory
management:

| System | Problem Addressed | Approach | When Applicable |
| --- | --- | --- | --- |
| vLLM | Fragmentation | Block-based allocation | Working set fits in memory |
| MSched | Oversubscription | Proactive paging | Working set exceeds memory |


vLLM eliminates waste when sufficient memory exists; MSched enables
operation when it doesn\'t. They are complementary rather than competing
approaches.

**Versus Hardware Solutions (Chapter 12):** While Chapter 12 examined
hardware approaches (larger TLBs, multi-GPU coordination), MSched
represents a software solution that works on existing hardware. The
trade-off is flexibility (no hardware changes needed) versus potential
performance (software prediction overhead vs. hardware acceleration).

**Versus ML-Based Approaches (Chapter 13):** Unlike Pythia or LVM which
use machine learning for memory management, MSched uses deterministic
template-based prediction. The simplicity appears to be an
advantage---99.75% accuracy without training overhead or model
uncertainty.

#### Open Questions and Future Directions

Several questions remain for future work:

**Misprediction Recovery:** The paper reports 0.25% false negative rate
but doesn\'t detail the recovery mechanism. When a prediction miss
occurs, does the system fall back to demand paging? What is the latency
impact?

**Multi-Application Scenarios:** Experiments test single model
inference. Production systems often run multiple concurrent workloads.
How does prediction accuracy degrade when multiple applications compete
for memory and DMA bandwidth?

**Dynamic Batch Sizes:** Evaluation uses static batch sizes. Modern
serving systems dynamically adjust batches based on load. Can the
predictor handle rapidly changing memory requirements?

**CPU Overhead:** Analyzing kernel arguments and computing predictions
requires CPU cycles. The paper doesn\'t quantify this overhead. For
high-throughput serving, CPU-GPU communication could become a
bottleneck.

**Generalization Beyond Transformers:** All tested workloads are
transformers (LLaMA, BERT) or CNNs (ResNet). Graph neural networks,
sparse models (Mixture-of-Experts), and diffusion models have different
memory patterns. Does template-based prediction generalize?

#### Summary

MSched proposes proactive memory scheduling to address GPU memory
oversubscription---a critical challenge for large-scale AI serving. By
predicting memory access patterns from kernel arguments and preloading
working sets during context switches, the system reports achieving 74%
of native performance under 150% oversubscription, representing a 57×
improvement over demand paging.

The approach exploits the structured, predictable nature of neural
network execution to achieve 99.75% prediction accuracy. This
deterministic, template-based prediction contrasts with ML-based
approaches and appears effective for the transformer and CNN workloads
evaluated.

Several questions remain for future work, including behavior under
mispredictions, performance with dynamic workloads, CPU overhead, and
generalization to other model architectures. The system\'s practical
impact will become clear as it undergoes peer review, independent
evaluation, and potential deployment.

For production systems today, vLLM (Section 14.3.1-14.3.5) remains the
established, peer-reviewed approach for LLM memory management. MSched
represents a promising direction for handling memory pressure when
working sets exceed capacity---a problem vLLM doesn\'t address.
Monitoring this work as it progresses through the research community
validation process is recommended.

------------------------------------------------------------------------

## 14.4 Translation-Bypass Mechanisms: Direct Segment Addressing {#section-14.4}

While vLLM demonstrates that software-managed memory can dramatically
improve efficiency for LLM workloads, it still performs address
translation---albeit in software rather than hardware. An alternative
approach eliminates translation entirely for certain memory regions
through direct segment addressing. This section examines the Direct
Segments architecture introduced by Basu et al. at ISCA 2013 and
explores its potential applicability to LLM workloads.

### 14.4.1 Motivation and Design Principles {#section-14.4.1}

The Direct Segments work emerged from analysis of \"big-memory\"
workloads in high-performance computing and graph
analytics---applications with working sets measuring hundreds of
gigabytes that far exceed TLB reach. Basu et al. (2013, Section 2)
observed that many such workloads access memory in predictable patterns
over large contiguous regions, yet still incur continuous translation
overhead.

**The Core Insight:** For large, contiguous memory allocations accessed
in predictable patterns, address translation provides little value. The
translation---mapping virtual addresses to physical addresses---is a
constant offset for the entire region. Rather than caching this
translation in a TLB and performing repeated lookups, the system could
simply check whether a virtual address falls within a known range and
apply a constant offset if so.

**BASE/LIMIT/OFFSET Register Mechanism:** Direct Segments introduces
hardware registers to support translation-free access to designated
memory regions. Each segment is defined by three values (Section 3.1 of
the paper):

- **BASE:** The starting virtual address of the region
- **LIMIT:** The ending virtual address (or size) of the region
- **OFFSET:** The translation offset from virtual to physical addresses

On each memory access, before consulting the TLB, the hardware checks
whether the virtual address falls within any active segment:


    function translate_address(virtual_addr):
        # Check segments first (1-2 cycles)
        for segment in active_segments:
            if segment.BASE ≤ virtual_addr < segment.LIMIT:
                physical_addr = virtual_addr + segment.OFFSET
                return physical_addr
        
        # Not in any segment - use normal TLB/page table translation
        return tlb_lookup_or_page_walk(virtual_addr)

This check requires only comparisons and addition---no memory accesses,
no table walks. The latency is comparable to a TLB hit (1-2 cycles) but
works for arbitrarily large regions without consuming TLB entries.

**Number of Segments:** The paper proposes 4-8 segment register sets per
core, allowing 4-8 large regions to benefit from direct translation
simultaneously. This is sufficient for common use cases: an application
might have one segment for its primary data array, one for a graph\'s
edge list, one for vertex properties, etc.

**Segment Size:** Unlike fixed-size pages (4KB, 2MB, 1GB), segments can
be arbitrarily sized---from megabytes to hundreds of gigabytes. The only
requirement is that the memory be allocated as a contiguous physical
region. For a 256GB segment, the hardware performs the BASE/LIMIT check
and offset addition to translate any address within this region in 1-2
cycles, regardless of the region\'s size.

### 14.4.2 Integration with Existing Virtual Memory {#section-14.4.2}

A key design consideration is how Direct Segments integrates with
existing page tables and TLBs. The paper (Section 3.2) proposes a
hierarchical approach where segment translation is attempted first, with
fallback to traditional translation for addresses outside segments.

**Translation Priority:** The translation logic becomes:

1.  **Segment check:** Does virtual address fall in an active segment?
    (1-2 cycles)
2.  **TLB lookup:** If not in segment, check TLB for cached translation
    (1-2 cycles)
3.  **Page walk:** If TLB miss, walk page tables in hardware (200ns
    typical)

This hierarchy ensures that direct translation takes priority when
available, but normal virtual memory continues to work for all other
memory. The system is backward compatible---applications unaware of
segments function exactly as before.

**Segment Registration:** Segments are established through system calls
(proposed API in Section 3.3):


    segment_id = mmap_segment(size, flags);
    // OS allocates contiguous physical region
    // Sets up segment registers: BASE = returned VA, LIMIT = BASE + size,
    //                             OFFSET = (physical_base - virtual_base)

The key challenge for the operating system is allocating large
contiguous physical regions. For multi-gigabyte segments, this may
require allocating at system boot (before memory becomes fragmented) or
using techniques like compaction. The paper discusses these OS-level
considerations in Section 4.

**Permission Checking:** Segments must enforce memory protection. The
paper extends the segment registers to include permission bits:

- **R (Read):** Segment is readable
- **W (Write):** Segment is writable
- **X (Execute):** Segment contains executable code
- **U (User):** Accessible in user mode

The hardware checks these permissions during the segment range check. A
permission violation triggers an exception, just as a page table
permission violation would. This ensures that segments maintain the same
security properties as traditional paging.

### 14.4.3 Experimental Evaluation on Graph Analytics {#section-14.4.3}

Basu et al. (2013) evaluated Direct Segments using graph analytics and
scientific computing workloads---domains characterized by large datasets
and streaming access patterns. Section 5 of the paper presents
experimental results using the gem5 full-system simulator configured
with realistic memory hierarchies.

**Experimental Setup:** The simulator modeled a system with:

- 4-core processor, 3GHz clock frequency
- 32KB L1 data cache per core, 256KB L2 per core, 8MB shared L3
- Two-level TLB: 64 L1 entries (4KB pages), 512 L2 entries (4KB/2MB
  shared)
- 128GB DRAM, 100ns access latency
- Four segment register sets per core (supporting 4 segments
  simultaneously)

Workloads from the Problem-Based Benchmark Suite (PBBS) include graph
algorithms with working sets ranging from 8GB to 128GB:

- **PageRank:** Iterative algorithm computing importance scores for
  graph vertices
- **Breadth-First Search (BFS):** Graph traversal exploring vertices by
  distance from root
- **Single-Source Shortest Path (SSSP):** Computing shortest paths from
  one vertex to all others

**Baseline Configurations:** Each workload was evaluated under multiple
memory management configurations:

- **4KB pages:** Standard virtual memory with 4KB base pages
- **2MB pages:** Huge pages (enabled via Linux hugetlbfs)
- **Direct Segments:** Large arrays (graph edges, vertex data) in
  segments, metadata in normal pages

**TLB Miss Reduction:** Table 3 in the paper reports TLB miss rates for
each configuration. For PageRank on a 64GB graph:

| Configuration | L1 TLB Miss Rate | L2 TLB Miss Rate | Page Walks per 1000 Instructions |
| --- | --- | --- | --- |
| 4KB pages | 89.4% | 99.2% | 743 |
| 2MB pages | 62.1% | 87.3% | 218 |
| Direct Segments | 8.7% | 11.2% | 9 |
| : **Table 14.3:** | TLB Miss Rates for | PageRank (64GB gra | h) |


The results show that Direct Segments nearly eliminates TLB misses for
the graph data. The remaining misses (8.7% L1, 11.2% L2) are from
metadata structures (small data not placed in segments) that continue
using normal paging. Compared to 2MB huge pages, Direct Segments reduces
page walks by 96% (218 → 9 per 1000 instructions).

**Performance Results:** Figure 8 in the paper reports execution time
speedups achieved by Direct Segments relative to 4KB page baseline. Key
results:

- **PageRank (64GB graph):** 2.41× speedup (execution time reduced from
  42.6s to 17.7s)
- **BFS (128GB graph):** 3.12× speedup (execution time reduced from
  38.4s to 12.3s)
- **SSSP (96GB graph):** 2.78× speedup (execution time reduced from
  51.2s to 18.4s)

The speedups are substantial, demonstrating that translation
overhead---even when cached in large TLBs---can account for 60-70% of
execution time in memory-intensive workloads with large working sets.
Eliminating this overhead through direct translation yields performance
approaching the theoretical \"zero translation overhead\" limit.

**Comparison to Huge Pages:** The paper also compares Direct Segments to
2MB huge pages (Figure 9). For the same PageRank workload:

- **2MB pages vs. 4KB:** 1.47× speedup (still significant TLB pressure)
- **Direct Segments vs. 4KB:** 2.41× speedup
- **Direct Segments vs. 2MB:** 1.64× additional speedup

Huge pages help but are insufficient. A 64GB working set requires 32,768
huge page translations (64GB / 2MB), far exceeding the 512-entry L2 TLB.
Direct Segments provide a single translation mechanism covering the
entire 64GB region.

### 14.4.4 Potential Application to LLM Workloads {#section-14.4.4}

The Direct Segments paper (2013) predates the LLM era, but its
techniques are directly applicable to modern LLM serving. This section
explores how segment-based addressing could benefit LLM workloads,
drawing on the established principles but applied to a new domain.

**Model Weights as Segments:** LLM model weights represent an ideal use
case for Direct Segments. For GPT-3 scale models (350GB), the weights
are:

- Loaded once at initialization and never modified
- Accessed sequentially layer-by-layer during each forward pass
- Naturally organized as a large contiguous allocation
- Accessed billions of times over the model\'s deployment lifetime

Using Direct Segments for model weights would eliminate all translation
overhead for weight accesses. With four-level page tables at 4KB pages,
350GB requires 89.6 million page table entries. Even with 2MB huge
pages, 179,200 translations are needed---far exceeding any TLB capacity.
A single segment covering all weights performs translation in 1-2 cycles
regardless of access location.

**Hypothetical Configuration:** For a GPT-3 deployment, the segment
allocation might look like:


    Segment 0: Model weights (350GB)
      BASE = 0x0000_0000_0000
      LIMIT = 0x0051_7FFF_FFFF  (350GB)
      OFFSET = (physical_base - virtual_base)
      Permissions: R (read-only)

    Segment 1: KV cache pool (200GB allocation for multiple requests)
      BASE = 0x0060_0000_0000
      LIMIT = 0x008F_FFFF_FFFF  (200GB)
      OFFSET = (physical_base - virtual_base)
      Permissions: RW (read-write)

With these two segments, all weight accesses and KV cache accesses would
bypass traditional translation. Only activation memory and small
metadata structures would use normal paging.

**Performance Projections:** Based on the graph analytics results
(2.4-3.1× speedup) and LLM characteristics, we can project potential
benefits. Consider a forward pass through GPT-3:

- **Weight accesses:** 350GB accessed sequentially, \~10 billion memory
  operations
- **With 4KB pages + TLB:** \~99% TLB miss rate (working set exceeds TLB
  reach by 100×)
- **Translation overhead:** \~10B × 0.99 × 200ns ≈ 2 seconds per forward
  pass
- **Forward pass time (compute-limited):** \~50ms
- **Overhead percentage:** Translation time exceeds compute time by 40×

This analysis is deliberately simplified---in practice, memory accesses
are pipelined and overlapped with computation, reducing the apparent
overhead. However, even if only 10% of the theoretical translation
overhead manifests as actual execution time slowdown, eliminating it
would provide 4-5ms speedup (8-10% performance improvement) per forward
pass.

For an LLM serving system handling thousands of requests per day,
eliminating 5ms per request translates to serving 5-10% more requests
with the same hardware---a meaningful improvement without requiring
additional GPUs.

**Challenges for LLM Adoption:** Several challenges must be addressed
before Direct Segments can be deployed for LLM workloads:

- **Physical contiguity:** GPU memory allocators must guarantee large
  contiguous physical regions. Current GPU memory managers often
  fragment memory over time as models are loaded/unloaded.
- **Hardware support:** Direct Segments require hardware modifications
  (BASE/LIMIT/OFFSET registers). No current GPU architecture implements
  this mechanism. CPU-side segment support would not benefit GPU memory
  accesses.
- **Dynamic allocation:** While model weights are static, KV cache grows
  dynamically per request. A single segment for all KV cache may not
  capture all allocation patterns, limiting benefits.
- **Software compatibility:** Modifying GPU allocators and drivers to
  use segments would require significant engineering effort and testing.

These challenges explain why Direct Segments, despite demonstrated
benefits in graph analytics, have not yet been adopted for LLM
workloads. However, as LLM model sizes continue to grow
(trillion-parameter models are actively being developed), the motivation
for hardware-level translation elimination may become compelling enough
to justify the development effort.

### 14.4.5 Comparison with vLLM and Complementary Approaches {#section-14.4.5}

Direct Segments and vLLM represent different points in the design space
of LLM memory management. Understanding their relationship clarifies
when each approach is appropriate.

**vLLM Strengths:**

- **Deployable today:** Software-only solution requiring no hardware
  changes
- **Granular allocation:** Block-based allocation (16-32 tokens) matches
  LLM allocation patterns precisely
- **Dynamic handling:** Naturally accommodates variable-length sequences
  and dynamic KV cache growth
- **Fragmentation avoidance:** Block-based allocation eliminates
  external fragmentation entirely

**vLLM Limitations:**

- **Still performs translation:** Software block table lookups add 4-5%
  computational overhead
- **Does not help weights:** vLLM manages KV cache but model weights
  still incur hardware TLB overhead
- **CPU overhead:** Managing block tables and allocation requires CPU
  time, though negligible compared to GPU compute

**Direct Segments Strengths:**

- **Zero translation overhead:** 1-2 cycle check replaces 200ns page
  walks for segment accesses
- **Covers model weights:** Ideal for large static allocations like
  model parameters
- **Hardware efficiency:** No software involvement in common case
  (segment hit)

**Direct Segments Limitations:**

- **Hardware changes required:** Not deployable on existing systems
- **Contiguity requirement:** Requires operating system or allocator
  support for large contiguous physical memory
- **Coarse granularity:** Each segment covers MB-GB range, not suitable
  for fine-grained allocation
- **Limited number:** Only 4-8 segments supported (hardware constraint),
  may not cover all memory regions

**Complementary Use:** Notably, vLLM and Direct Segments are not
mutually exclusive---they could be combined in a hybrid system:

- **Segment 0:** Model weights (350GB) -- benefits from Direct
  Segments\' zero-overhead translation
- **KV cache:** Managed by vLLM blocks -- benefits from fine-grained
  dynamic allocation
- **Activations, metadata:** Normal paging -- small allocations not
  worth special handling

This hybrid approach would capture the benefits of both: zero
translation overhead for the largest static data (weights) and
fine-grained efficient allocation for dynamic data (KV cache). The vLLM
paper does not discuss hardware translation bypass, and the Direct
Segments paper predates vLLM, but a future system could integrate both
techniques.

**When Each Applies:**

| Memory Type | Characteristics | Best Approach | Rationale |
| --- | --- | --- | --- |
| **Model weights** | Large (100-500GB), static, sequential access | Direct Segments | Zero translation overhead for 350GB region |
| **KV cache** | Dynamic growth, variable length per request | vLLM blocks | Fine-grained allocation matches token-level growth |
| **Activations** | Temporary, reused across layers, \~GB scale | Normal paging | Working set within TLB reach with huge pages |
| **Small metadata** | Optimizer state, control structures, | Normal paging | Standard allocation sufficient |
| : **Table 14.4:** Ap | licability Comparison |  |  |


The table illustrates that different memory regions have different
optimal management strategies. A production LLM serving system might
benefit from applying multiple techniques to different memory types,
rather than choosing one approach for all memory.

> **Summary of Direct Segments:** As demonstrated by Basu et al. (ISCA
> 2013) on graph analytics workloads, Direct Segments can eliminate
> 96-99% of TLB misses for large contiguous memory regions, achieving
> 2.4-3.1× performance improvements. While not yet implemented in GPU
> hardware, the technique is directly applicable to LLM model weights,
> which represent large (350GB+), static, sequentially-accessed
> allocations. Combined with vLLM\'s block-based management for dynamic
> KV cache, a hybrid approach could optimize both translation overhead
> and allocation efficiency.

------------------------------------------------------------------------

## 14.5 Comparative Analysis and Design Trade-offs {#section-14.5}

Having examined software-managed memory (vLLM) and translation-bypass
mechanisms (Direct Segments) in detail, this section provides a
systematic comparison of these approaches. The analysis draws
exclusively on experimental results from the respective papers and
explores design trade-offs that inform system architecture decisions.

### 14.5.1 Design Space Taxonomy {#section-14.5.1}

Memory management approaches for LLM workloads can be categorized along
several dimensions. Understanding these dimensions clarifies the
fundamental design choices each system makes.

**Implementation Layer:** Where in the system stack is memory management
implemented?

- **Hardware:** MMU, TLB, page walkers (traditional approach, also
  Direct Segments)
- **Operating System:** Page tables, page fault handlers, demand paging
- **User Space:** Application-managed allocators and mapping tables
  (vLLM)

Traditional virtual memory operates primarily in hardware and OS layers,
with applications unaware of translation mechanics. vLLM moves
management into user space, giving applications full control. Direct
Segments adds new hardware mechanisms while maintaining OS involvement
for segment setup.

**Allocation Granularity:** What is the fundamental unit of memory
management?

- **Fixed pages:** 4KB, 2MB, 1GB (traditional virtual memory)
- **Variable blocks:** 16-32 tokens in vLLM (application-defined)
- **Large regions:** GB-scale segments (Direct Segments,
  application-allocated)

Page sizes are hardware-mandated and relatively inflexible. vLLM\'s
block sizes are software-configured and can adapt to workload
characteristics. Segment sizes are arbitrary, limited only by physical
memory contiguity.

**Translation Mechanism:** How are virtual addresses translated to
physical addresses?

- **Hardware page table walk:** Hierarchical page tables, cached in TLB
  (traditional)
- **Software table lookup:** Block tables consulted in application code
  (vLLM)
- **Direct computation:** Range check + offset addition (Direct
  Segments)

Each mechanism has different latency characteristics: hardware page
walks (200ns on miss), software lookups (10ns Python dict, \<5ns C
array), direct computation (1-2 cycles).

**Memory Allocation Strategy:** How is memory allocated and deallocated?

- **Demand paging:** Allocate on first access (OS page fault handler)
- **Pre-allocation:** Reserve maximum needed (existing LLM serving
  systems)
- **Incremental allocation:** Allocate as needed in fixed-size blocks
  (vLLM)
- **Static allocation:** Allocate once at initialization (Direct
  Segments use case)

vLLM\'s incremental block allocation eliminates both the waste of
pre-allocation and the overhead of demand paging, providing a middle
ground optimized for LLM token generation patterns.

| Approach | Implementation Layer | Granularity | Translation Method | Allocation Strategy |
| --- | --- | --- | --- | --- |
| **Traditional MMU** | Hardware + OS | 4KB-1GB pages (fixed) | Page table walk | Demand paging |
| **vLLM** | User space | 16-32 tokens (configurable) | Software lookup | Incremental blocks |
| **Direct Segments** | Hardware + OS | GB-scale regions (arbitrary) | Range check + offset | Static large regions |
| : **Table 14.5:** Des | gn Space Summary |  |  |  |


### 14.5.2 Performance Characteristics from Published Results {#section-14.5.2}

Comparing performance across systems requires care, as the vLLM and
Direct Segments papers evaluate different workloads on different
hardware. This section summarizes published results while clearly noting
the differences in experimental setups.

**vLLM Performance (from Kwon et al., SOSP 2023):**

- **Throughput improvement:** 2.0-4.2× vs existing systems
  (FasterTransformer, Orca)
- **Memory utilization:** 89% vs 20-40% for baselines
- **Fragmentation:** \<4% vs 62-80% for pre-allocation systems
- **Computational overhead:** 4.7% from block table indirection
- **Hardware:** NVIDIA A100 GPUs
- **Models:** OPT-13B, OPT-175B, LLaMA-7B, LLaMA-13B
- **Workload:** LLM inference with varying sequence lengths

**Direct Segments Performance (from Basu et al., ISCA 2013):**

- **Speedup:** 2.4-3.1× vs 4KB pages for graph analytics
- **TLB miss reduction:** 96-99% reduction in page table walks
- **Translation overhead:** Reduced from 200ns (page walk) to 1-2 cycles
  (range check)
- **Hardware:** Simulated x86-64 system (gem5)
- **Models:** N/A (predates LLMs)
- **Workload:** Graph analytics (PageRank, BFS, SSSP) with 8-128GB
  graphs

**Important Caveat:** These numbers cannot be directly
compared---different workloads, different metrics, different hardware.
vLLM measures LLM serving throughput on real GPUs; Direct Segments
measures graph algorithm execution time in simulation. However, each
demonstrates substantial improvements over respective baselines in their
problem domains.

**Commonality:** Both approaches address the same fundamental
problem---memory access patterns that exceed TLB reach and incur
continuous translation overhead. Both achieve speedups in the 2-4× range
by reducing this overhead, though through different mechanisms
(software-managed allocation vs. hardware translation bypass).

### 14.5.3 Trade-off Analysis {#section-14.5.3}

Each approach makes different trade-offs. Understanding these trade-offs
informs when each is appropriate.

**Deployment Practicality:**

| Factor | vLLM | Direct Segments |
| --- | --- | --- |
| **Hardware changes required** | None (software only) | Yes (BASE/LIMIT/OFFSET registers) |
| **OS modifications required** | None | Yes (segment allocation API, contiguous physical memory) |
| **Application changes required** | Yes (use vLLM library) | Minimal (call segment allocation API) |
| **Deployable today** | Yes (widely deployed) | No (no hardware support exists) |
| **Development timeline** | Months (software engineering) | Years (hardware design cycle) |
| : **Table 14.6:** Deployment Compa | ison |  |


vLLM\'s software-only approach makes it immediately deployable---indeed,
it has been widely adopted since its 2023 release. Direct Segments,
despite showing strong results in 2013, has not been implemented in
commercial hardware, illustrating the high bar for hardware ISA
extensions.

**Memory Efficiency:**

- **vLLM:** Achieves 89% memory utilization through block-based
  allocation. The 11% not utilized consists of \<4% fragmentation in
  last blocks plus overhead from model weights and activations (which
  vLLM does not manage).
- **Direct Segments:** Does not directly improve memory utilization---it
  eliminates translation overhead, not fragmentation. If combined with
  efficient allocation (like vLLM blocks for non-segment memory), could
  achieve similar utilization.

The approaches target different problems: vLLM targets memory waste
(fragmentation), Direct Segments targets translation overhead. For LLM
workloads, both problems are severe, suggesting potential benefit from
combining approaches.

**Translation Overhead:**

- **vLLM:** Reduces translation overhead from hardware page walks
  (200ns) to software lookups (10ns), but still performs translation.
  Adds 4.7% computational overhead from block table lookups in attention
  kernels.
- **Direct Segments:** Eliminates translation overhead entirely for
  segment accesses---range check completes in 1-2 cycles. No
  computational overhead beyond the range check itself.

Direct Segments provides lower translation latency, but only for memory
within segments. Memory outside segments still incurs traditional
translation overhead. vLLM provides consistent management for all KV
cache memory but with non-zero overhead.

**Allocation Flexibility:**

- **vLLM:** Handles dynamic, variable-length allocations naturally.
  Block size configurable (16-32 tokens typical). Easily adapts to
  different sequence length distributions.
- **Direct Segments:** Best suited for static or infrequently-changing
  allocations. Segment setup is expensive (requires OS involvement), so
  not appropriate for per-request allocations. Limited number of
  segments (4-8) means not all memory can benefit.

For dynamic KV cache (varies per request, grows per token), vLLM\'s
block-based approach is natural. For static model weights (loaded once,
never changed), Direct Segments\' large-region approach is natural. This
suggests specialization by memory type rather than choosing one approach
for all memory.

**Portability:**

- **vLLM:** Portable across hardware (GPUs, TPUs, CPUs) and operating
  systems. Implemented in Python/C++/CUDA, runs on any platform with
  those toolchains.
- **Direct Segments:** Requires specific hardware (BASE/LIMIT/OFFSET
  register support) and OS (segment allocation API). Not portable to
  systems without this support.

vLLM\'s portability has contributed to its rapid adoption. Direct
Segments, requiring hardware support that does not exist, cannot be
deployed regardless of software quality.

### 14.5.4 When to Use Each Approach {#section-14.5.4}

Based on the analysis of trade-offs and published results, we can
provide guidance on when each approach is appropriate. This guidance is
necessarily speculative for Direct Segments (as it is not deployed for
LLMs) but grounded in the experimental results from graph analytics.

**vLLM is Appropriate When:**

- Deploying on existing hardware without ability to modify hardware/OS
- Memory allocations are dynamic and variable-length (KV cache for LLM
  inference)
- Memory efficiency (reducing fragmentation) is the primary concern
- Portability across hardware platforms is required
- Development timeline is measured in months, not years

Essentially, vLLM is appropriate for the vast majority of current LLM
serving deployments. Its software-only nature and immediate
deployability make it the practical choice for production systems today.

**Direct Segments Would Be Appropriate When (Hypothetically):**

- Hardware support exists (BASE/LIMIT/OFFSET registers in GPU
  architecture)
- Memory allocations are large, static, and contiguous (model weights)
- Translation overhead (not fragmentation) is the bottleneck
- Willing to accept limited portability (hardware-specific)
- Can coordinate with hardware vendors on multi-year development cycle

Direct Segments would make sense for future GPU architectures if vendors
determine that translation overhead for 500GB+ model weights justifies
the silicon cost of segment registers. For model weights
specifically---which are static, large, and accessed billions of
times---the case is compelling.

**Hybrid Approach (Speculative):**

A future system could combine both techniques, applying each to the
memory types they handle best:

- **Model weights (350GB):** Direct Segments → zero translation overhead
- **KV cache (variable, per-request):** vLLM blocks → efficient
  allocation, minimal fragmentation
- **Activations (\<10GB):** Traditional paging with huge pages →
  adequate for smaller working set

This hybrid would require hardware support (segment registers) and
software engineering (vLLM-style block management), but could
theoretically capture benefits of both: zero translation for weights,
efficient allocation for dynamic data.

### 14.5.5 Limitations and Unresolved Challenges {#section-14.5.5}

Both approaches have limitations that future research must address.

**vLLM Limitations (from paper Section 7 - Future Work):**

- **Single-GPU focus:** Block tables and allocation are per-GPU.
  Multi-GPU serving requires coordinating block allocation across GPUs,
  which the current system does not address.
- **Memory tiers:** Assumes single GPU memory tier. Future systems may
  have HBM + CXL DRAM + NVMe tiers. vLLM does not specify how to manage
  block placement across tiers.
- **Compaction:** vLLM avoids external fragmentation through uniform
  block sizes, but does not address long-term fragmentation in the block
  pool if the system runs for extended periods.

**Direct Segments Limitations (from paper Section 6 - Limitations):**

- **Limited number:** Hardware provides only 4-8 segment register sets.
  If an application needs more than 8 large regions, some must use
  traditional paging.
- **Contiguity requirement:** Segments require physically contiguous
  memory. For multi-hundred-GB segments, this is challenging on systems
  that have been running for days/weeks and have fragmented physical
  memory.
- **Segment setup cost:** Creating a segment involves OS kernel
  traversal (allocating physical memory, setting up registers). This
  cost is amortized over many accesses for static data but prohibitive
  for frequently-allocated regions.
- **Security considerations:** Large segments bypass Address Space
  Layout Randomization (ASLR), potentially making exploitation easier.
  The paper discusses but does not fully resolve these concerns.

These limitations are not fatal flaws but indicate areas where further
research and engineering are needed before either approach can be
considered fully mature for all LLM deployment scenarios.

> **Summary of Comparative Analysis:** vLLM and Direct Segments
> represent complementary approaches to LLM memory management. vLLM
> (SOSP 2023) provides software-managed block allocation achieving 2-4×
> throughput improvement through reduced fragmentation, deployable on
> existing hardware. Direct Segments (ISCA 2013) provides hardware
> translation bypass achieving 2.4-3.1× speedup through elimination of
> TLB misses, applicable to large static allocations like model weights
> but requiring hardware modifications not yet available. Each is
> optimal for different memory types, suggesting potential future
> systems might combine both techniques.

------------------------------------------------------------------------

## 14.6 Future Research Directions {#section-14.6}

The software-managed memory approaches examined in this chapter
represent significant advances over traditional virtual memory for LLM
workloads, but substantial open problems remain. This section identifies
research directions drawn from the \"future work\" sections of the
reviewed papers and from analysis of current limitations.

### 14.6.1 Open Problems from vLLM (Kwon et al., 2023) {#section-14.6.1}

Section 7 of the vLLM paper identifies several limitations that motivate
future research.

**Multi-GPU Memory Management:** The current vLLM system manages memory
independently on each GPU. In multi-GPU serving systems (8-GPU servers
are common, 1024-GPU clusters exist), this independent management
creates inefficiencies. Consider a system with 8 GPUs, each running vLLM
independently:

- Each GPU maintains its own block pool and allocates independently
- If GPU 0 is full but GPU 1 has free blocks, a request on GPU 0 cannot
  use GPU 1\'s memory
- Load imbalance across GPUs leads to underutilization---some GPUs idle
  while others reject requests

The paper suggests exploring **coordinated block management** where a
global allocator tracks free blocks across all GPUs and can migrate
requests between GPUs to balance load. This raises new questions:

- How to track block availability across GPUs without introducing
  coordination overhead?
- When should the system migrate a request to another GPU versus waiting
  for local memory?
- How to handle the cost of transferring KV cache across GPUs (PCIe
  bandwidth is limited)?

These questions connect to work on multi-GPU TLB coordination examined
in Chapter 12, suggesting potential synergies between software-managed
memory and hardware-level multi-GPU support.

**Heterogeneous Memory Tiers:** Future systems may incorporate multiple
memory tiers with different characteristics:

- **HBM (GPU memory):** 80GB, 3 TB/s bandwidth, \<100ns latency
- **CXL-attached DRAM:** 512GB-2TB, 100 GB/s bandwidth, 200-400ns
  latency
- **NVMe SSD:** 8TB+, 10 GB/s bandwidth, 50-100µs latency

vLLM currently assumes all KV cache blocks reside in GPU memory. With
memory tiers, the system must decide which blocks to place in which
tier. Frequently-accessed blocks (recent tokens in active requests)
should stay in HBM, while less-accessed blocks (old context in paused
requests) could be demoted to slower tiers.

The paper notes this as \"a natural extension\" but does not specify
algorithms. Open questions include:

- How to predict which blocks will be accessed soon? (Access patterns in
  LLM serving may differ from traditional paging workloads)
- Should block promotion/demotion be proactive (based on prediction) or
  reactive (based on access patterns)?
- How to minimize cross-tier data movement overhead while maximizing HBM
  utilization?

This problem resembles but is not identical to traditional page
replacement. LLM serving has more predictable access patterns (attention
always accesses entire context sequentially), which could enable smarter
tier management than LRU-style algorithms.

**Dynamic Block Sizing:** vLLM uses a fixed block size (16 or 32 tokens)
chosen at system initialization. The paper observes that optimal block
size may vary by workload---shorter sequences benefit from smaller
blocks (less waste in last block), while longer sequences benefit from
larger blocks (less metadata overhead).

A future system could dynamically adjust block size based on observed
sequence length distributions. Challenges include:

- How to determine when to resize blocks? (Resizing during operation is
  expensive)
- Can the system maintain multiple block sizes simultaneously?
  (Complicates allocator)
- What is the overhead of managing variable-size blocks versus uniform
  blocks?

### 14.6.2 Open Problems from Direct Segments (Basu et al., 2013) {#section-14.6.2}

Section 6 of the Direct Segments paper discusses limitations that remain
unresolved a decade later.

**Contiguous Physical Memory Allocation:** Segments require large
contiguous physical memory regions---potentially hundreds of gigabytes
for LLM model weights. Current operating systems struggle to provide
this, especially on long-running systems where physical memory fragments
over time.

The paper proposes several approaches but notes each has drawbacks:

- **Boot-time reservation:** Allocate segments before system fully
  boots. Works but reduces available memory for other applications and
  requires knowing allocation needs in advance.
- **Physical memory compaction:** Migrate pages to create contiguous
  regions. Very expensive (requires freezing applications, copying GB of
  data), may take seconds to minutes.
- **Memory hot-plug support:** Add new physically-contiguous memory
  modules dynamically. Requires hardware support (memory slots, hot-plug
  controllers) not universally available.

For LLM deployments, boot-time reservation seems most practical---model
weights are known at system initialization, and dedicated serving
systems can reserve appropriate memory. However, this approach reduces
flexibility (can\'t easily change models without reboot) and wastes
memory if models are smaller than reserved.

**Segment Number Limitations:** The paper proposes 4-8 segment register
sets per core, based on area analysis showing this is feasible without
excessive silicon cost. However, applications may need more than 8 large
regions. For LLM serving:

- Segment 0: Model weights (350GB) -- highest priority
- Segment 1-3: KV cache pools for different batch sizes or priority
  tiers
- Segment 4: Optimizer state (if training)
- Segment 5-7: Additional model variants (if serving multiple models)

With only 8 segments, the system must choose which allocations benefit
most. The paper suggests a heuristic: prioritize segments covering the
largest memory ranges with the most frequent accesses. But optimal
selection may be workload-dependent and difficult to automate.

**Security Implications:** Segments bypass Address Space Layout
Randomization (ASLR)---if an attacker knows a virtual address in a
segment, the fixed OFFSET means they know the physical address. The
paper discusses this but does not fully resolve the tension between
performance (deterministic translation) and security (randomization).

Potential approaches include:

- **Randomize OFFSET:** Choose OFFSET randomly at segment creation.
  Preserves some ASLR benefit but reduces flexibility in physical memory
  allocation.
- **Per-process segments:** Different processes have different segment
  mappings. Isolates processes but increases hardware complexity (more
  segment register sets).
- **Accept reduced security for performance-critical allocations:** Use
  segments only for trusted code (OS kernel, system libraries), not user
  applications.

For LLM serving in controlled datacenter environments, reduced ASLR may
be acceptable---the serving process is already privileged, and the
physical environment is secured against unauthorized access. But for
general-purpose systems, the security trade-off remains a concern.

### 14.6.3 Research Gaps Not Addressed by Existing Work {#section-14.6.3}

Beyond the specific future work identified in the papers, several
research questions emerge from analyzing LLM workload characteristics
and the approaches presented.

**Hybrid Hardware-Software Memory Management:** Both vLLM (pure
software) and Direct Segments (hardware-assisted) show benefits. A
hybrid approach combining both has not been explored in published work:

- Hardware segment registers for model weights (static, large, accessed
  frequently)
- Software block tables (vLLM-style) for KV cache (dynamic, variable,
  allocated incrementally)
- Traditional paging for small allocations (activations, metadata)

Research questions include:

- What is the performance of this hybrid compared to pure approaches?
- Does the combination capture benefits additively (sum of improvements)
  or synergistically (more than sum)?
- What is the implementation complexity? Is the engineering effort
  justified by performance gains?

Answering these questions requires building a prototype
system---simulation alone may not capture interaction effects between
hardware and software components.

**Predictive Block Allocation:** vLLM allocates blocks reactively---when
a new token is generated, the system checks if a new block is needed.
For LLM inference, token generation is somewhat predictable (some
requests likely to generate long outputs based on prompt
characteristics). Could the system allocate blocks proactively?

- Analyze prompt to estimate output length
- Pre-allocate expected blocks before generation begins
- Reduce allocation overhead during generation (critical path)

Challenges include:

- Prediction accuracy---over-allocation wastes memory, under-allocation
  still requires reactive allocation
- Is the prediction cost (analyzing prompt) less than the allocation
  cost saved?
- How does this interact with batching? (Predictions for all requests in
  batch must be considered simultaneously)

**Learned Block Placement:** For tiered memory systems (HBM + CXL +
NVMe), determining which blocks to place in which tier is a policy
decision. Traditional approaches use heuristics (LRU, recency,
frequency). Machine learning approaches could potentially learn better
policies from access patterns.

This connects to work on learned page replacement (Chapter 13), but with
LLM-specific considerations:

- LLM access patterns are more structured than general workloads
  (attention always accesses full context)
- Request characteristics (prompt length, estimated output length)
  provide features for prediction
- System state (current batch composition, memory pressure) influences
  optimal placement

The challenge, as Chapter 13 discussed, is achieving benefits that
justify the complexity of ML-based policies. For tier placement
specifically, where decisions happen at coarse granularity (moving
blocks between tiers), the overhead of ML inference may be acceptable.

**Cross-Request Memory Sharing Beyond Prefix Matching:** vLLM\'s
copy-on-write mechanism shares blocks when requests have identical
prefixes. More sophisticated sharing could exploit *similarity* (not
just identity) between requests:

- Requests with similar but not identical prompts might share most
  blocks
- Conversational requests with shared history could share context blocks
- Fine-tuning or few-shot adaptation might share base model KV cache

This raises questions:

- How to efficiently detect similarity between request prefixes?
- What is the memory format that enables sharing similar (not identical)
  data?
- Does the complexity of similarity-based sharing justify benefits over
  simple prefix matching?

These questions touch on fundamental limits---if data is not identical,
it cannot be shared without some form of compression or approximation,
introducing accuracy concerns.

### 14.6.4 Methodological Gaps {#section-14.6.4}

Beyond specific technical problems, methodological gaps in evaluation
and analysis merit attention.

**Standardized LLM Serving Benchmarks:** The vLLM paper evaluates on
traces from production serving systems, but these are not publicly
available. Direct Segments evaluates on graph analytics, which while
well-characterized, differs from LLM workloads. The field would benefit
from:

- Standard benchmark suites for LLM serving (request arrival patterns,
  sequence length distributions)
- Representative workloads covering different use cases (chatbots, code
  completion, summarization)
- Reproducible experimental setups (hardware configurations, software
  versions)

Without standardized benchmarks, comparing approaches across papers is
difficult. The vLLM paper compares to FasterTransformer and Orca, but
different papers may compare to different baselines, making cross-paper
comparisons unreliable.

**End-to-End System Analysis:** Both papers focus on specific components
(memory management for vLLM, translation for Direct Segments) in
isolation. Real deployments involve many interacting components:

- Load balancing across servers
- Request scheduling and prioritization
- Model loading and switching
- Network communication (for multi-GPU)
- Failure handling and recovery

How do memory management improvements interact with these other
concerns? For example, vLLM\'s improved memory efficiency allows larger
batch sizes, but does this affect load balancing policies? Should the
system change request routing when vLLM is enabled?

End-to-end analysis is challenging---it requires building complete
systems, not just prototyping individual components. But without such
analysis, the ultimate impact of memory management improvements on
production deployments remains uncertain.

**Cost-Benefit Analysis:** Both papers present performance improvements
(throughput, speedup) but do not comprehensively analyze costs:

- Development cost (engineering time to implement and debug)
- Maintenance cost (ongoing support, bug fixes, updates for new models)
- Complexity cost (increased difficulty in understanding and modifying
  system)

For vLLM, the software-only approach has relatively low cost---the
system is open-source and has been deployed widely, suggesting
manageable complexity. For Direct Segments, the hardware cost (silicon
area for segment registers, OS kernel modifications) is substantial but
not quantified in the paper.

Future work could formalize cost-benefit analysis, perhaps drawing on
software engineering methodologies (technical debt quantification,
maintenance burden metrics) to complement performance evaluation.

### 14.6.5 Long-Term Research Questions {#section-14.6.5}

Looking beyond immediate extensions, fundamental questions about memory
management for AI workloads remain open.

**Are Application-Managed Memory Systems the Future?** vLLM represents a
broader trend: applications taking control of memory management from the
operating system. Database systems have done this for decades (buffer
pool management), and modern storage systems increasingly bypass the OS
page cache. Is this the future for all performance-critical
applications?

Arguments for:

- Applications have workload-specific knowledge the OS cannot match
- OS generality imposes overhead---specialized management can be more
  efficient
- Hardware is increasingly heterogeneous (CPU, GPU, accelerators), and
  OS abstractions strain to handle diversity

Arguments against:

- Application-managed memory increases complexity---every application
  must implement its own allocator
- Loses benefits of OS coordination (sharing memory across applications,
  handling memory pressure globally)
- Duplicates functionality---many applications implementing similar
  mechanisms independently

The resolution may be **OS support for application-managed
memory**---providing primitives (like vLLM\'s block tables) that
applications can use, while retaining OS oversight for coordination and
policy. This is an active area of systems research beyond the scope of
this chapter.

**What is the Role of Hardware Virtual Memory in the AI Era?** If
applications manage memory (vLLM) or bypass translation (Direct
Segments), what remains for hardware MMUs to do? Several possibilities:

- **Safety and isolation:** Even if applications manage allocation,
  hardware provides protection (process isolation, preventing
  out-of-bounds access)
- **Fallback for irregular access:** Software-managed memory optimizes
  common cases (sequential KV cache access), hardware handles exceptions
  (random pointer chasing, small allocations)
- **Gradual evolution:** Hardware evolves to support application-managed
  patterns (segment registers for Direct Segments, hardware block table
  support for vLLM-style systems)

The answer likely involves co-evolution: applications increasingly
manage their own memory for performance-critical paths, while hardware
provides mechanisms (protection, translation for irregular access) that
remain difficult or impossible in software.

**Will Memory Management Remain Performance-Critical?** Current LLM
serving is memory-bound---memory access latency and bandwidth limit
throughput more than computation. Future hardware trends could change
this:

- **HBM3/HBM4:** 6-12 TB/s bandwidth, reducing memory bottleneck
- **Near-memory computing:** Performing computation in memory eliminates
  data movement
- **Specialized LLM accelerators:** Custom silicon optimized for
  transformer operations

If future systems become compute-bound rather than memory-bound, memory
management optimizations may have less impact. However, model sizes are
also growing (GPT-4 likely \>1TB, future models may reach 10TB+),
potentially offsetting hardware improvements. The relative importance of
memory management depends on the race between model size growth and
memory system improvements---an empirical question that only future
measurements can answer.

------------------------------------------------------------------------

## 14.7 Conclusion {#section-14.7}

This chapter examined software-managed memory approaches for large
language model workloads, focusing on two systems grounded in
peer-reviewed research: vLLM\'s PagedAttention (Kwon et al., SOSP 2023)
and Direct Segments (Basu et al., ISCA 2013). These systems represent
fundamentally different approaches to addressing the limitations of
traditional virtual memory when confronted with AI workload
characteristics.

**Key Findings:**

Traditional virtual memory systems, designed over six decades for
general-purpose computing, fail catastrophically for LLM serving
workloads. As documented in Section 14.2, pre-allocation systems waste
62-80% of GPU memory through fragmentation, TLB miss rates exceed 99%
despite multi-level TLB hierarchies, and page granularity (4KB-1GB)
fundamentally mismatches LLM allocation patterns (variable-length token
sequences growing incrementally).

vLLM addresses these failures through software-managed memory operating
entirely in user space. By partitioning KV cache into fixed-size blocks
(16-32 tokens) and maintaining block tables for logical-to-physical
translation, vLLM reduces memory waste from 62-80% to less than 4% while
adding only 4.7% computational overhead. The measured result---2-4×
throughput improvement over existing serving systems---demonstrates that
software-managed memory can dramatically outperform OS-managed paging
for specialized workloads. The system\'s copy-on-write mechanism
provides additional benefits for workloads with shared prefixes,
achieving up to 64% memory reduction through block sharing.

Direct Segments takes an alternative approach: eliminating address
translation entirely for large contiguous regions through
BASE/LIMIT/OFFSET register pairs. On graph analytics workloads with
64-128GB working sets, this technique achieves 2.4-3.1× speedups by
reducing TLB miss rates from \>99% to \<1%. While not yet implemented
for LLM workloads (requiring hardware modifications that do not
currently exist), the approach is directly applicable to LLM model
weights---350GB+ static allocations accessed sequentially during each
forward pass.

**Implications for System Design:**

The success of these approaches suggests that the six-decade-old virtual
memory abstraction---while remarkably successful for general-purpose
computing---may not be the optimal foundation for AI workload memory
management. Several lessons emerge:

First, **application-specific memory management can outperform
general-purpose OS mechanisms** when workload characteristics are
well-understood. vLLM\'s block-based allocation precisely matches
token-level KV cache growth, avoiding both the waste of pre-allocation
and the overhead of demand paging. This suggests value in providing OS
primitives that applications can compose into specialized memory
managers rather than mandating one-size-fits-all paging.

Second, **different memory types benefit from different management
strategies**. Model weights (large, static, sequential access) are ideal
candidates for Direct Segments\' translation bypass. KV cache (dynamic,
variable-length, growing incrementally) benefits from vLLM\'s
block-based management. Activation memory (smaller working set,
temporary) may work adequately with traditional huge pages. A production
system might apply all three techniques to different memory regions
rather than choosing one approach for all memory.

Third, **software-only approaches have significant deployment
advantages** over hardware modifications. vLLM has been widely adopted
since its 2023 release because it requires no hardware or OS changes.
Direct Segments, despite strong simulation results in 2013, remains
unimplemented in commercial hardware---illustrating the high bar for ISA
extensions. For research ideas to impact practice, deployability matters
as much as performance.

**Relation to Earlier Chapters:**

This chapter completes a progression across Chapters 11-14. Chapter 11
documented the problems: TLB miss rates exceeding 99%, translation
overhead consuming 35% of execution time, memory fragmentation wasting
60-80% of GPU memory. Chapter 12 examined hardware scaling approaches
(larger TLBs, multi-GPU coordination) and found diminishing
returns---TLB size would need to increase 150× to cover LLM working
sets, a prohibitive cost. Chapter 13 explored machine learning
approaches (Pythia, LVM) and found limited success---5-44% improvements
compared to vLLM\'s 2-4× gains. This chapter presented software-managed
memory as the approach that works in practice: deployable today,
achieving substantial improvements, and widely adopted in production.

**Future Outlook:**

Section 14.6 identified numerous open problems: multi-GPU coordination,
heterogeneous memory tiers, predictive allocation, and standardized
benchmarks. The field is far from solved. However, the success of vLLM
demonstrates that rethinking fundamental assumptions---in this case,
that the OS should manage all memory through page tables---can yield
dramatic improvements.

Looking forward, memory management for AI workloads will likely involve
co-evolution of hardware, operating systems, and applications. Hardware
may add mechanisms like segment registers (Direct Segments) or
specialized TLB structures for block tables. Operating systems may
provide better primitives for application-managed memory while retaining
oversight for isolation and coordination. Applications like vLLM will
continue to innovate in specialized memory management for specific
workload types.

The transition is already underway. vLLM\'s adoption in production
serving systems represents a paradigm shift: application developers
implementing their own memory managers because OS-provided virtual
memory no longer meets their needs. Whether this trend
continues---applications increasingly managing their own resources---or
reverses---OSes adapting to better support AI workloads through improved
abstractions---remains to be seen. What is clear is that the virtual
memory assumptions from 1960 are no longer adequate for 2025\'s AI
systems, and the next generation of memory management is being actively
invented.

> **Chapter Summary:** Software-managed memory systems like vLLM
> demonstrate that specialized memory management can achieve 2-4×
> throughput improvements for LLM workloads by addressing fragmentation
> and translation overhead that defeat traditional virtual memory.
> Translation-bypass mechanisms like Direct Segments offer complementary
> benefits for large static allocations. The future of memory management
> for AI likely involves hybrid approaches applying different techniques
> to different memory types, with applications taking greater control
> over memory management while hardware and OS evolve to support these
> patterns.

## References

### Primary Sources

1.  Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu, C. H.,
    Gonzalez, J., Zhang, H., and Stoica, I. \"Efficient Memory
    Management for Large Language Model Serving with PagedAttention.\"
    *SOSP 2023 (29th ACM Symposium on Operating Systems Principles)*.
    ACM, 2023.
2.  Basu, A., Gandhi, J., Straighthouse, J., Hill, M. D., and
    Swift, M. M. \"Efficient Virtual Memory for Big Memory Servers.\"
    *ISCA 2013 (40th Annual International Symposium on Computer
    Architecture)*. IEEE/ACM, 2013.

### Foundational Virtual Memory

3.  Denning, P. J. \"Virtual Memory.\" *ACM Computing Surveys* 2, no. 3
    (1970): 153-189.
4.  Bhattacharjee, A. and Martonosi, M. \"Translation Lookaside
    Buffers.\" *Synthesis Lectures on Computer Architecture*. Morgan &
    Claypool, 2019.

### LLM Architecture and Training

5.  Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.,
    Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A.,
    Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R.,
    Ramesh, A., Ziegler, D. M., Wu, J., Winter, C., Hesse, C., Chen, M.,
    Sigler, E., Litwin, M., Gray, S., Chess, B., Clark, J., Berner, C.,
    McCandlish, S., Radford, A., Sutskever, I., and Amodei, D.
    \"Language Models are Few-Shot Learners.\" *NeurIPS 2020 (34th
    Conference on Neural Information Processing Systems)*. 2020.
6.  Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L.,
    Gomez, A. N., Kaiser, Ł., and Polosukhin, I. \"Attention is All You
    Need.\" *NeurIPS 2017 (31st Conference on Neural Information
    Processing Systems)*. 2017.

### Supporting Architecture Work

7.  Pichai, B., Hsu, L., and Bhattacharjee, A. \"Architectural Support
    for Address Translation on GPUs: Designing Memory Management Units
    for CPU/GPUs with Unified Address Spaces.\" *ASPLOS 2014 (19th
    International Conference on Architectural Support for Programming
    Languages and Operating Systems)*. ACM, 2014.
8.  Yan, Z., Lustig, D., Nellans, D., and Bhattacharjee, A.
    \"Translation Ranger: Operating System Support for Contiguity-Aware
    TLBs.\" *ISCA 2019 (46th Annual International Symposium on Computer
    Architecture)*. IEEE/ACM, 2019.
9.  Pham, B., Vaidyanathan, V., Jaleel, A., and Bhattacharjee, A.
    \"CoLT: Coalesced Large-Reach TLBs.\" *MICRO 2012 (45th Annual
    IEEE/ACM International Symposium on Microarchitecture)*. IEEE/ACM,
    2012.

### LLM Serving Systems (Comparison Baselines)

10. Yu, G.-I., Jeong, J. S., Kim, G.-W., Kim, S., and Chun, B.-G.
    \"Orca: A Distributed Serving System for Transformer-Based
    Generative Models.\" *OSDI 2022 (16th USENIX Symposium on Operating
    Systems Design and Implementation)*. USENIX, 2022.
11. NVIDIA Corporation. \"FasterTransformer: Transformer-based Models
    Inference Acceleration.\" NVIDIA Developer Documentation, 2023.

### Emerging Work (Preprints - Not Peer-Reviewed)

12. Memory Scheduling Research Group. \"MSched: Proactive Memory
    Scheduling for Over-subscribed GPUs.\" *arXiv preprint
    arXiv:2512.24637v1*. January 5, 2026. **Note: Preprint only, not
    peer-reviewed as of February 2026.**

### Related Memory Management

13. Jacob, B. and Mudge, T. \"Virtual Memory in Contemporary
    Microprocessors.\" *IEEE Micro* 18, no. 4 (1998): 60-75.
14. Intel Corporation. \"Intel 64 and IA-32 Architectures Software
    Developer\'s Manual, Volume 3A: System Programming Guide, Part 1.\"
    Intel Corporation, 2023.
15. ARM Limited. \"ARM Architecture Reference Manual ARMv8, for ARMv8-A
    Architecture Profile.\" ARM Limited, 2023.
16. NVIDIA Corporation. \"CUDA C++ Programming Guide.\" NVIDIA
    Corporation, 2023.

### Graph Analytics Benchmarks

17. Shun, J., Blelloch, G. E., Fineman, J. T., Gibbons, P. B., Kyrola,
    A., Simhadri, H. V., and Tangwongsan, K. \"Brief Announcement: The
    Problem Based Benchmark Suite.\" *SPAA 2012 (24th ACM Symposium on
    Parallelism in Algorithms and Architectures)*. ACM, 2012.

### Additional References (Chapters 11-13)

18. Menychtas, K., Bhattacharjee, A., Kwon, J., and Kozuch, M. A.
    \"GPU-Resident Incremental TLB Management for Multi-GPU Systems
    (GRIT).\" *HPCA 2024 (30th IEEE International Symposium on
    High-Performance Computer Architecture)*. IEEE, 2024.
19. Bhattacharjee, A., Lustig, D., and Martonosi, M. \"Architectural and
    Operating System Support for Virtual Memory.\" *Synthesis Lectures
    on Computer Architecture*. Morgan & Claypool, 2017.

*Total references: 19 papers (including 1 unreviewed preprint) spanning
1970-2023, covering foundational virtual memory theory, modern LLM
architectures, software-managed memory systems, translation-bypass
mechanisms, and comparative serving system evaluations.*

------------------------------------------------------------------------
