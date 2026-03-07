---
nav_exclude: true
sitemap: false
---

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: container
::: {#title-block-header}
# Chapter 11: Virtual Memory Challenges in AI/ML Accelerators {#chapter-11-virtual-memory-challenges-in-aiml-accelerators .title}
:::

- [Chapter 11: Virtual Memory in AI/ML
  Accelerators](#chapter-11-virtual-memory-in-aiml-accelerators){#toc-chapter-11-virtual-memory-in-aiml-accelerators}
  - [11.1 Introduction: Scale Changes
    Everything](#introduction-scale-changes-everything){#toc-introduction-scale-changes-everything}
    - [From Architecture to Operation: What Chapter 4
      Established](#from-architecture-to-operation-what-chapter-4-established){#toc-from-architecture-to-operation-what-chapter-4-established}
    - [The Three Approaches to Virtual Memory in AI/ML
      Accelerators](#the-three-approaches-to-virtual-memory-in-aiml-accelerators){#toc-the-three-approaches-to-virtual-memory-in-aiml-accelerators}
    - [The Scale Problem: Why AI/ML Stresses MMUs
      Differently](#the-scale-problem-why-aiml-stresses-mmus-differently){#toc-the-scale-problem-why-aiml-stresses-mmus-differently}
    - [What This Chapter
      Covers](#what-this-chapter-covers){#toc-what-this-chapter-covers}
    - [Why These Mechanisms
      Matter](#why-these-mechanisms-matter){#toc-why-these-mechanisms-matter}
    - [Relationship to Previous
      Chapters](#relationship-to-previous-chapters){#toc-relationship-to-previous-chapters}
    - [Looking Forward](#looking-forward){#toc-looking-forward}
    - [Why Systolic Arrays Demand Predictable Memory
      Access](#why-systolic-arrays-demand-predictable-memory-access){#toc-why-systolic-arrays-demand-predictable-memory-access}
    - [Static Memory Layout via XLA
      Compiler](#static-memory-layout-via-xla-compiler){#toc-static-memory-layout-via-xla-compiler}
    - [Software-Managed Isolation Without Page
      Tables](#software-managed-isolation-without-page-tables){#toc-software-managed-isolation-without-page-tables}
    - [The Efficiency Payoff: Compute-to-Bandwidth
      Ratios](#the-efficiency-payoff-compute-to-bandwidth-ratios){#toc-the-efficiency-payoff-compute-to-bandwidth-ratios}
    - [Why TPU v4 and v5 Added Virtual
      Memory](#why-tpu-v4-and-v5-added-virtual-memory){#toc-why-tpu-v4-and-v5-added-virtual-memory}
    - [The Limited MMU
      Approach](#the-limited-mmu-approach){#toc-the-limited-mmu-approach}
    - [Lessons for Accelerator
      Design](#lessons-for-accelerator-design){#toc-lessons-for-accelerator-design}
    - [Anatomy of a Page Fault
      Storm](#anatomy-of-a-page-fault-storm){#toc-anatomy-of-a-page-fault-storm}
    - [Migration Thrashing: The Ping-Pong
      Problem](#migration-thrashing-the-ping-pong-problem){#toc-migration-thrashing-the-ping-pong-problem}
    - [Mitigation Strategy 1:
      Prefetching](#mitigation-strategy-1-prefetching){#toc-mitigation-strategy-1-prefetching}
    - [Mitigation Strategy 2: Pinning Critical
      Structures](#mitigation-strategy-2-pinning-critical-structures){#toc-mitigation-strategy-2-pinning-critical-structures}
    - [Mitigation Strategy 3: cudaMemAdvise for Access
      Patterns](#mitigation-strategy-3-cudamemadvise-for-access-patterns){#toc-mitigation-strategy-3-cudamemadvise-for-access-patterns}
    - [Mitigation Strategy 4: Structuring the Training
      Loop](#mitigation-strategy-4-structuring-the-training-loop){#toc-mitigation-strategy-4-structuring-the-training-loop}
    - [Real-World Case Study: Stable Diffusion
      Inference](#real-world-case-study-stable-diffusion-inference){#toc-real-world-case-study-stable-diffusion-inference}
    - [Summary: Page Fault Mitigation
      Principles](#summary-page-fault-mitigation-principles){#toc-summary-page-fault-mitigation-principles}
    - [The Scale Problem: Why Multi-GPU TLB Invalidation Differs from
      Multi-Core](#the-scale-problem-why-multi-gpu-tlb-invalidation-differs-from-multi-core){#toc-the-scale-problem-why-multi-gpu-tlb-invalidation-differs-from-multi-core}
    - [Naive Approach: Serial TLB
      Invalidation](#naive-approach-serial-tlb-invalidation){#toc-naive-approach-serial-tlb-invalidation}
    - [NVSwitch: Hardware-Accelerated TLB
      Broadcast](#nvswitch-hardware-accelerated-tlb-broadcast){#toc-nvswitch-hardware-accelerated-tlb-broadcast}
    - [Multi-Server Coordination: Combining NVSwitch and
      RDMA](#multi-server-coordination-combining-nvswitch-and-rdma){#toc-multi-server-coordination-combining-nvswitch-and-rdma}
    - [NCCL Integration: Gradient Synchronization and TLB
      Coherency](#nccl-integration-gradient-synchronization-and-tlb-coherency){#toc-nccl-integration-gradient-synchronization-and-tlb-coherency}
    - [Production Measurements: Real Systems at
      Scale](#production-measurements-real-systems-at-scale){#toc-production-measurements-real-systems-at-scale}
    - [Protocol Design: Ensuring
      Correctness](#protocol-design-ensuring-correctness){#toc-protocol-design-ensuring-correctness}
    - [When Multi-GPU TLB Synchronization Breaks
      Down](#when-multi-gpu-tlb-synchronization-breaks-down){#toc-when-multi-gpu-tlb-synchronization-breaks-down}
    - [Summary: Multi-GPU TLB Synchronization
      Principles](#summary-multi-gpu-tlb-synchronization-principles){#toc-summary-multi-gpu-tlb-synchronization-principles}
    - [The TLB Coverage
      Calculation](#the-tlb-coverage-calculation){#toc-the-tlb-coverage-calculation}
    - [Why 1 GB Pages Aren\'t Always
      Optimal](#why-1-gb-pages-arent-always-optimal){#toc-why-1-gb-pages-arent-always-optimal}
    - [Decision Framework: Page Size by Tensor
      Type](#decision-framework-page-size-by-tensor-type){#toc-decision-framework-page-size-by-tensor-type}
    - [Measured Performance: Page Size Impact on Real
      Models](#measured-performance-page-size-impact-on-real-models){#toc-measured-performance-page-size-impact-on-real-models}
    - [Linux Huge Page
      Configuration](#linux-huge-page-configuration){#toc-linux-huge-page-configuration}
    - [Summary: Page Size Decision
      Tree](#summary-page-size-decision-tree){#toc-summary-page-size-decision-tree}
    - [The Chiplet Architecture
      Challenge](#the-chiplet-architecture-challenge){#toc-the-chiplet-architecture-challenge}
    - [Two Architectural
      Approaches](#two-architectural-approaches){#toc-two-architectural-approaches}
    - [TLB Hierarchy in
      MI300X](#tlb-hierarchy-in-mi300x){#toc-tlb-hierarchy-in-mi300x}
    - [Infinity Fabric TLB Coherency
      Protocol](#infinity-fabric-tlb-coherency-protocol){#toc-infinity-fabric-tlb-coherency-protocol}
    - [TLB Coverage for 192 GB Address
      Space](#tlb-coverage-for-192-gb-address-space){#toc-tlb-coverage-for-192-gb-address-space}
    - [Practical Configuration: Fitting LLaMA 70B on
      MI300X](#practical-configuration-fitting-llama-70b-on-mi300x){#toc-practical-configuration-fitting-llama-70b-on-mi300x}
    - [Comparison: MI300X vs H100 for Large
      Models](#comparison-mi300x-vs-h100-for-large-models){#toc-comparison-mi300x-vs-h100-for-large-models}
    - [Summary: MI300X TLB Architecture
      Insights](#summary-mi300x-tlb-architecture-insights){#toc-summary-mi300x-tlb-architecture-insights}
    - [The Integration
      Challenge](#the-integration-challenge){#toc-the-integration-challenge}
    - [MMU Sharing: Address Translation Services
      (ATS)](#mmu-sharing-address-translation-services-ats){#toc-mmu-sharing-address-translation-services-ats}
    - [Cache Coherency
      Challenge](#cache-coherency-challenge){#toc-cache-coherency-challenge}
    - [Software Solution: Explicit Cache
      Flush](#software-solution-explicit-cache-flush){#toc-software-solution-explicit-cache-flush}
    - [Gaudi\'s Optimized Approach: Compiler-Managed
      Coherency](#gaudis-optimized-approach-compiler-managed-coherency){#toc-gaudis-optimized-approach-compiler-managed-coherency}
    - [All-Reduce Performance: Gaudi vs
      NVLink](#all-reduce-performance-gaudi-vs-nvlink){#toc-all-reduce-performance-gaudi-vs-nvlink}
    - [TLB Considerations for
      RDMA](#tlb-considerations-for-rdma){#toc-tlb-considerations-for-rdma}
    - [Summary: Habana Gaudi 2 MMU
      Insights](#summary-habana-gaudi-2-mmu-insights){#toc-summary-habana-gaudi-2-mmu-insights}
    - [Bandwidth Arbitration Across Three Device
      Types](#bandwidth-arbitration-across-three-device-types){#toc-bandwidth-arbitration-across-three-device-types}
    - [TLB Coherency Across CPU, GPU, and Neural
      Engine](#tlb-coherency-across-cpu-gpu-and-neural-engine){#toc-tlb-coherency-across-cpu-gpu-and-neural-engine}
    - [When Unified Memory Wins: Sequential Access
      Patterns](#when-unified-memory-wins-sequential-access-patterns){#toc-when-unified-memory-wins-sequential-access-patterns}
    - [When Unified Memory Loses: Concurrent Access
      Patterns](#when-unified-memory-loses-concurrent-access-patterns){#toc-when-unified-memory-loses-concurrent-access-patterns}
    - [Page Size Selection for M-series Unified
      Memory](#page-size-selection-for-m-series-unified-memory){#toc-page-size-selection-for-m-series-unified-memory}
    - [Practical Implications for M-Series
      Development](#practical-implications-for-m-series-development){#toc-practical-implications-for-m-series-development}
    - [Pitfall 1: Training Without Prefetching (Page Fault
      Storms)](#pitfall-1-training-without-prefetching-page-fault-storms){#toc-pitfall-1-training-without-prefetching-page-fault-storms}
    - [Pitfall 2: Using 4KB Pages for Large Models (TLB
      Thrashing)](#pitfall-2-using-4kb-pages-for-large-models-tlb-thrashing){#toc-pitfall-2-using-4kb-pages-for-large-models-tlb-thrashing}
    - [Pitfall 3: Ignoring Multi-GPU TLB Synchronization
      Overhead](#pitfall-3-ignoring-multi-gpu-tlb-synchronization-overhead){#toc-pitfall-3-ignoring-multi-gpu-tlb-synchronization-overhead}
    - [Pitfall 4: Page Migration Thrashing (CPU↔︎GPU
      Ping-Pong)](#pitfall-4-page-migration-thrashing-cpugpu-ping-pong){#toc-pitfall-4-page-migration-thrashing-cpugpu-ping-pong}
    - [Pitfall 5: Assuming Cache Coherency Exists (Stale DMA
      Reads)](#pitfall-5-assuming-cache-coherency-exists-stale-dma-reads){#toc-pitfall-5-assuming-cache-coherency-exists-stale-dma-reads}
    - [Pitfall 6: Over-Committing Unified Memory
      Bandwidth](#pitfall-6-over-committing-unified-memory-bandwidth){#toc-pitfall-6-over-committing-unified-memory-bandwidth}
  - [References](#references){#toc-references}
    - [GPU MMU Architecture and Virtual
      Memory](#gpu-mmu-architecture-and-virtual-memory){#toc-gpu-mmu-architecture-and-virtual-memory}
    - [Google TPU
      Architecture](#google-tpu-architecture){#toc-google-tpu-architecture}
    - [Multi-GPU Coordination and
      Scaling](#multi-gpu-coordination-and-scaling){#toc-multi-gpu-coordination-and-scaling}
    - [AMD MI300X and Chiplet
      Architectures](#amd-mi300x-and-chiplet-architectures){#toc-amd-mi300x-and-chiplet-architectures}
    - [Intel Habana Gaudi](#intel-habana-gaudi){#toc-intel-habana-gaudi}
    - [Apple Neural Engine and Unified
      Memory](#apple-neural-engine-and-unified-memory){#toc-apple-neural-engine-and-unified-memory}
    - [Page Fault Handling and
      Prefetching](#page-fault-handling-and-prefetching){#toc-page-fault-handling-and-prefetching}
    - [TLB Optimization](#tlb-optimization){#toc-tlb-optimization}
    - [Performance Analysis
      Tools](#performance-analysis-tools){#toc-performance-analysis-tools}
    - [Hardware
      Specifications](#hardware-specifications){#toc-hardware-specifications}

# Chapter 11: Virtual Memory in AI/ML Accelerators

## 11.1 Introduction: Scale Changes Everything

On a February morning in 2024, engineers at a leading AI lab discovered
their training run had stalled. They were training a 1.8 trillion
parameter language model across 2,048 NVIDIA H100 GPUs---the largest
training run the lab had ever attempted. The GPUs were performing
computations correctly, gradients were flowing, loss was decreasing. But
training throughput had collapsed to 12% of theoretical maximum. After
three days of debugging, they found the culprit: TLB invalidation
overhead.

The training code used dynamic batch sizing, adjusting batch size based
on memory availability. Every time the batch size changed, the framework
reallocated activation tensors. Each reallocation triggered page table
updates. Each page table update required TLB invalidations across all
2,048 GPUs. At scale, a single `munmap()` operation that would take 5
microseconds on a single GPU was taking 4 milliseconds across the
cluster---blocking all 2,048 GPUs for the duration. With 1,000
reallocations per hour, the system spent 4 seconds per hour frozen,
waiting for TLB shootdowns. That\'s 0.1% overhead, which seems
trivial---but it reduced effective throughput by 12% because GPUs
couldn\'t overlap computation with communication while TLB invalidations
were in flight.

This incident illustrates a fundamental truth about virtual memory in
AI/ML systems: **scale changes everything**. In Chapter 4, Section 4.13,
we examined GPU MMU architecture---the hardware structures, TLB
hierarchies, and basic page fault mechanisms that enable virtual memory
on GPUs. Those fundamentals remain true. But when you scale from one GPU
to 2,048 GPUs, from 10 GB models to 500 GB models, from batch sizes of
32 to batch sizes of 8,192, entirely new challenges emerge that hardware
architecture alone doesn\'t prepare you for.

### From Architecture to Operation: What Chapter 4 Established

Chapter 4.13 provided the architectural foundation we\'ll build upon.
Readers learned that modern GPUs have full MMU capabilities with
multi-level TLB hierarchies (64-entry L1 TLBs per streaming
multiprocessor, 512-2048 entry L2 TLBs shared across the GPU). Page
faults on GPUs are expensive---50,000 to 500,000 cycles compared to
1,000-10,000 cycles on CPUs---because they require round-trips through
the PCIe bus to the CPU driver. NVIDIA\'s Unified Virtual Addressing
(UVA) allows CPUs and GPUs to share the same virtual address space,
enabling zero-copy data sharing. AMD\'s HSA (Heterogeneous System
Architecture) provides shared page tables between CPU and GPU, while
Apple\'s M-series achieves true unified memory where all processors
access a single physical memory pool.

These are critical architectural facts that enable virtual memory on
accelerators. But they leave unanswered the questions that arise when
you actually build and deploy AI/ML systems at scale:

- When you train a 70 billion parameter model that requires 140 GB in
  FP16, what page size do you use, and why does it matter?
- When 1,024 GPUs all need to synchronize their TLBs after a page table
  update, how do you prevent serialization bottlenecks?
- When page faults cost 50,000 cycles, how do you structure your
  training loop to eliminate them without pinning gigabytes of memory?
- When Google\'s TPU v1 through v3 achieved extraordinary efficiency by
  **eliminating the MMU entirely**, what does that tell us about the
  trade-offs between flexibility and performance?
- When 8 GPU chiplets share a package in AMD\'s MI300X, how do their
  MMUs coordinate without creating bottlenecks?

These operational challenges---selecting page sizes, coordinating
multi-GPU TLB invalidations, preventing page fault storms, and
understanding when to avoid virtual memory altogether---are the focus of
this chapter.

### The Three Approaches to Virtual Memory in AI/ML Accelerators

Modern AI/ML accelerators take three fundamentally different approaches
to virtual memory, each representing different points on the
flexibility-versus-efficiency spectrum:

**Approach 1: Full MMU with Virtual Memory (NVIDIA, AMD, Intel)**

These accelerators provide complete MMU functionality similar to CPUs,
with page tables, TLBs, and page fault handling. This approach offers
maximum flexibility: memory can be overcommitted, pages can be swapped,
and CPU and GPU can share address spaces. The cost is overhead. Page
table walks consume memory bandwidth. TLB misses add latency. Page
faults can stall thousands of GPU threads simultaneously. Chapter 4.13
covered the hardware architecture of these MMUs. This chapter explores
when and how to use them effectively---how to select page sizes that
provide adequate TLB coverage for multi-gigabyte models, how to
structure memory access patterns to avoid page faults, and how to
coordinate TLB invalidations across dozens or thousands of devices.

**Approach 2: No MMU (Google TPU v1-v3)**

Google took the opposite approach with TPU v1, v2, and v3: eliminate the
MMU entirely. These accelerators use pure physical addressing with
software-managed memory. The XLA compiler generates a static memory
layout at compile time, allocating every tensor to a specific physical
address. There are no page tables, no TLB, no page faults, and no
address translation overhead. The benefit is extreme efficiency---TPU v4
achieves 275 teraFLOPS with only 1.2 TB/s of memory bandwidth, a 229:1
compute-to-bandwidth ratio that would be impossible with MMU overhead.
The cost is zero flexibility: you can\'t swap memory, can\'t overcommit,
and can\'t share memory between processes. Yet for training neural
networks---workloads with completely predictable memory access
patterns---this trade-off was worthwhile. We\'ll examine why Google made
this choice, what it enabled, and why TPU v4 and v5 partially reversed
course by adding limited virtual memory support.

**Approach 3: Hybrid Models (Intel Habana, Specialized Workloads)**

Some accelerators use hybrid approaches, selectively applying virtual
memory where it provides value while using physical addressing for
performance-critical paths. Intel\'s Habana Gaudi 2, for example,
integrates 24 RDMA network interfaces directly on the accelerator die
for gradient exchange during distributed training. The compute cores use
virtual addressing with an MMU, but the RDMA engines can optionally use
physical addressing for zero-overhead transfers. This requires careful
coordination---when compute cores update gradients in cached memory,
those updates must be flushed before RDMA engines DMA them to remote
GPUs. We\'ll explore how this coordination works and when hybrid
approaches make sense.

### The Scale Problem: Why AI/ML Stresses MMUs Differently

AI/ML workloads differ from the general-purpose GPU workloads that
influenced GPU MMU design in three critical ways:

**Working Set Size:** Graphics rendering might touch a few hundred
megabytes---textures, vertex buffers, render targets. A GPT-3 scale
model touches 350 GB for parameters, 350 GB for optimizer state (Adam,
the most common training algorithm, maintains two running averages per
parameter---first and second moments tracking gradient direction and
variance---each requiring 4 bytes in FP32, totaling 8 bytes of optimizer
state per 2-byte parameter), and tens of gigabytes for activations
during each forward pass. Modern GPUs have 40-80 GB of on-device memory,
so a single large model spans 5-10 GPUs even before considering batch
size. With 4 KB pages, a 350 GB model requires 91.75 million page table
entries. If each page table entry is 8 bytes (64-bit physical address),
that\'s 734 MB just for page tables---nearly 1% of the model itself. The
TLB coverage problem is worse: an NVIDIA H100 with a 2,048-entry L2 TLB
covers only 8 MB with 4 KB pages. Against a 350 GB working set, the TLB
miss rate approaches 100%. Huge pages aren\'t optional---they\'re
mandatory.

**Access Predictability:** Graphics workloads have unpredictable memory
access patterns. Ray tracing follows random rays through scene geometry.
Texture sampling depends on what the camera sees. GPU MMU design assumed
workloads where prefetching is difficult and page faults are inevitable.
But neural network training is extraordinarily predictable. The forward
pass reads weights sequentially, performs matrix multiplications with
known dimensions, and writes activations to preallocated buffers. The
backward pass repeats this in reverse. The optimizer step updates
parameters in sequential order. There are no pointer chases, no random
access, no dynamic data structures. This predictability enables
optimizations that general-purpose MMUs don\'t attempt: allocating
gigabyte-scale buffers upfront, using huge pages to eliminate TLB
pressure entirely, and prefetching entire layers into GPU memory before
execution begins. Yet the default memory management in many ML
frameworks doesn\'t exploit this predictability, leading to page faults
and TLB thrashing that shouldn\'t occur.

**Multi-Device Coordination:** Graphics workloads typically run on one
GPU. Multi-GPU configurations exist for gaming (SLI/CrossFire) but
involve limited synchronization---each GPU renders alternating frames or
different regions of the screen. AI/ML training across multiple GPUs
requires tight coupling. All GPUs must process the same batch, compute
gradients, and synchronize those gradients via all-reduce operations.
This synchronization creates a new challenge: ensuring memory
consistency across devices. When one GPU updates a parameter in its
cache, that update must become visible to other GPUs before they read
that parameter. When the CPU updates page tables, all GPU TLBs must be
invalidated atomically. A single munmap() that affects one page on one
GPU affects that same page on all GPUs. Coordinating TLB invalidations
across 1,024 GPUs without creating serialization bottlenecks requires
careful protocol design that Chapter 4.13\'s single-GPU focus didn\'t
address.

### What This Chapter Covers

We\'ll explore virtual memory challenges and solutions across six major
domains, each addressing problems that emerge at the scale of modern
AI/ML systems:

**Google TPU and the No-MMU Approach (Section 11.2)** examines why
Google\'s TPU v1, v2, and v3 eliminated virtual memory entirely. TPU
uses a systolic array architecture where data flows through a 2D grid of
processing elements in rigid patterns. Any page fault would stall the
entire array, and unpredictable latency is unacceptable. The XLA
compiler generates static memory layouts, allocating every tensor at
compile time. This eliminates runtime memory management overhead
entirely, achieving 10× better compute-to-bandwidth ratios than GPU
architectures. But it also eliminates flexibility---no swapping, no
overcommit, no dynamic allocation. We\'ll see why this trade-off made
sense for v1-v3, and why v4-v5 added limited virtual memory support as
models grew beyond single-device memory capacity.

**Page Fault Storms and Mitigation (Section 11.3)** moves beyond Chapter
4.13\'s basic page fault discussion to explore what happens when
thousands of GPU threads fault simultaneously. In a training batch
processing 1,024 images, if each image touches previously-unmapped
pages, all 10,752 CUDA cores on an NVIDIA A100 can fault concurrently.
With each fault costing 50,000 cycles, that\'s 537 million cycles of
wasted computation. The faults also reduce GPU occupancy---warps stall
while waiting for pages, leaving compute units idle. We\'ll examine
fault storm scenarios in depth, understand migration thrashing (when
pages bounce between CPU and GPU repeatedly), and explore solutions
beyond basic prefetching: pinning critical data structures, using
cudaMemAdvise() for access pattern hints, and structuring training loops
to eliminate runtime faults.

**Multi-GPU TLB Synchronization (Section 11.4)** tackles the challenge
of coordinating TLB invalidations across hundreds or thousands of GPUs.
A naive approach that invalidates GPUs serially takes 2.56 milliseconds
for 256 GPUs---an eternity when training iterations should complete in
tens of milliseconds. NVIDIA\'s NVSwitch provides hardware broadcast for
TLB invalidations, reducing latency to 50 microseconds by sending a
single message that all GPUs receive simultaneously. But this requires
careful protocol design to ensure all GPUs acknowledge invalidation
before memory is reused. We\'ll examine the protocol details, understand
how NCCL (NVIDIA Collective Communications Library) coordinates gradient
synchronization with memory operations, and see how production systems
achieve 18× speedup over naive invalidation.

**Page Size Selection for Large Models (Section 11.5)** provides
quantitative analysis of the page size decision. For a 70 billion
parameter model (140 GB in FP16), using 4 KB pages yields a 99.998% TLB
miss rate---effectively no TLB benefit. Using 1 GB pages yields a 0%
miss rate---the entire model fits in a 2,048-entry TLB with 1,900
entries to spare. Yet 1 GB pages have downsides: allocation requires
physically contiguous memory, which may require compaction; allocation
latency is 1,000× higher than 4 KB pages; and partially-used pages waste
memory. We\'ll develop a decision framework: when to use 4 KB pages
(small dynamic allocations), 2 MB pages (intermediate buffers like
activations), and 1 GB pages (model parameters and optimizer state).

**AMD MI300X Chiplet Coordination (Section 11.6)** explores how eight
GPU chiplets in a single package coordinate their MMUs. Does each
chiplet have independent page tables that must be synchronized, or do
they share a page table base? How do TLB invalidations propagate across
the Infinity Fabric interconnect? The MI300X\'s 192 GB capacity enables
fitting models that require two or more NVIDIA H100s (80 GB each),
avoiding model parallelism overhead. But managing a 192 GB address space
requires careful TLB design. We\'ll examine AMD\'s approach, understand
the chiplet TLB hierarchy, and see why 1 GB pages provide full TLB
coverage for the entire 192 GB memory.

**Intel Habana Gaudi 2 RDMA Integration (Section 11.7)** investigates
how 24 integrated 100 Gbps RDMA network interfaces interact with the
accelerator\'s MMU. Do RDMA engines share page tables with compute
cores, or do they use separate address spaces? When compute cores update
gradients in cache and RDMA engines need to send those gradients to
remote devices, how is coherency maintained? Unlike NVIDIA GPUs where
the NIC is a separate device, Gaudi integrates everything on one die,
creating new coherency challenges. We\'ll explore ATS (Address
Translation Services) support, understand why explicit cache flushes are
sometimes necessary, and measure the benefit: Gaudi\'s 2.4 Tbps
aggregate RDMA bandwidth enables 4× faster gradient all-reduce than
NVLink for large models.

### Why These Mechanisms Matter

The practical implications ripple across development velocity, system
costs, and model capabilities:

**Training Efficiency:** Page faults that add 5% overhead might seem
negligible---1.05× slowdown is barely noticeable. But at scale, 5%
overhead compounds. If training a model takes 3 weeks without faults and
3.16 weeks with 5% overhead, that\'s 2.7 extra days. If you train 50
models per year, 5% overhead wastes 135 days---the equivalent of half a
research engineer\'s productivity. Eliminating page faults through
proper prefetching, page size selection, and memory pinning translates
directly to research velocity.

**Hardware Utilization:** Multi-GPU TLB synchronization overhead
determines scaling efficiency. If you can train a model on 64 GPUs with
95% efficiency but only achieve 60% efficiency on 256 GPUs due to TLB
coordination overhead, you\'re wasting 40% of 192 GPUs---the equivalent
of 77 GPUs sitting idle. At \$3-5 per GPU-hour for high-end
accelerators, poor scaling wastes \$500,000+ per year on a medium-sized
cluster. Understanding TLB synchronization protocols enables building
systems that maintain 85%+ efficiency at 1,000+ GPUs.

**Model Size Boundaries:** Memory capacity determines what models you
can train. If your model requires 180 GB but you have 80 GB GPUs, you
need model parallelism---splitting the model across multiple GPUs. Model
parallelism adds 15-25% communication overhead and doubles programming
complexity. Using AMD MI300X (192 GB) eliminates the need for splitting,
training the model on a single device at full efficiency. Understanding
TLB coverage requirements for these large address spaces---why 1 GB
pages are mandatory, not optional---enables actually using that 192 GB
effectively rather than suffering 99%+ TLB miss rates.

**Production Deployment:** Inference serving has different constraints
than training but shares the same MMU architecture. Inference doesn\'t
need optimizer state (cutting memory by 2×) and typically uses smaller
batch sizes (cutting activation memory). A 70B parameter model needs 140
GB for training but only 70 GB for inference. With INT8 quantization,
this drops to 35 GB---fitting on a single NVIDIA A100. Understanding
page size selection enables serving these models at low latency without
TLB thrashing. The difference between 50ms and 150ms inference latency
determines whether your chatbot feels responsive or sluggish to users.

### Relationship to Previous Chapters

This chapter synthesizes concepts from Chapters 3, 4, and 10 while
introducing challenges unique to AI/ML scale:

Chapter 3 examined page table structures, showing how x86-64\'s
four-level page tables (PML4 → PDPT → PD → PT) translate virtual
addresses. GPUs use compatible formats, allowing CPUs and GPUs to share
page tables in unified memory architectures. But AI/ML models with 100
GB+ working sets create page table overhead that Chapter 3\'s examples
(gigabytes, not hundreds of gigabytes) didn\'t address. A 350 GB model
with 4 KB pages requires 91.75 million page table entries. At four
levels, that\'s 91.75M PTEs (734 MB) plus 179K PD entries (1.4 MB) plus
350 PDPT entries (2.8 KB) plus 1 PML4 entry (8 bytes). Total: 735.4 MB
just for page tables. With 2 MB pages, this drops to 358 KB. We build on
Chapter 3\'s page table structure knowledge to understand why huge pages
aren\'t just a performance optimization but a memory overhead
optimization at AI/ML scale.

Chapter 4 explored TLB architecture and established the foundational
knowledge of GPU TLBs in Section 4.13. We assume readers understand TLB
hierarchies, page fault mechanisms, and basic Unified Virtual Addressing
concepts from that section. This chapter extends that knowledge to
address multi-GPU coordination (Section 4.13 covered single GPU),
quantitative page size selection (Section 4.13 mentioned huge pages help
but didn\'t provide calculations), and operational challenges like page
fault storms (Section 4.13 covered the basic mechanism but not what
happens when thousands of threads fault simultaneously). We\'re not
repeating Section 4.13---we\'re building on it to address questions that
emerge when you scale from one GPU to 1,000 GPUs and from 10 GB models
to 500 GB models.

Chapter 10 examined how external devices (network cards, storage
controllers, FPGAs) access memory through IOMMUs, and how PCIe ATS
enables device-side caching of translations. Intel Habana Gaudi 2\'s
integrated RDMA NICs represent an evolution of these concepts---instead
of separate devices connected via PCIe, the NICs sit on the same die as
the AI accelerator, sharing its MMU infrastructure. This creates new
coherency challenges that Chapter 10\'s IOMMU discussion didn\'t
encounter: when compute cores and RDMA engines share an L3 cache, cached
updates by compute must be made visible to RDMA before transfers begin.
We build on Chapter 10\'s IOMMU and ATS foundation while addressing the
tighter integration of accelerator and networking hardware.

### Looking Forward

The boundary between CPU and accelerator memory management continues to
blur. NVIDIA\'s Grace Hopper Superchip places CPU and GPU on the same
package with coherent memory access. AMD\'s MI300A integrates CPU cores,
GPU compute units, and HBM in a single die. Intel\'s Ponte Vecchio uses
multiple tile architectures with unified memory access. These trends
toward integration intensify the challenges we\'ll explore: as more
components share memory, TLB coordination becomes more critical; as
memory capacity grows, page size selection becomes more impactful; and
as workloads scale across thousands of devices, multi-accelerator
synchronization becomes the dominant bottleneck.

The techniques in this chapter---understanding when to eliminate virtual
memory entirely (TPU), how to select page sizes for TLB coverage (1 GB
pages for parameters), how to prevent page fault storms (prefetching and
pinning), and how to coordinate TLB invalidations at scale (NVSwitch
broadcast)---apply broadly across AI/ML accelerators. The specific
vendor implementations differ (NVIDIA vs AMD vs Intel vs Google), but
the underlying principles remain constant: virtual memory provides
flexibility at the cost of overhead, and that overhead becomes
unacceptable at the scale of modern AI/ML systems unless carefully
managed.

Let\'s begin by examining Google\'s TPU---the accelerator that achieved
extraordinary efficiency by eliminating virtual memory entirely, showing
us the theoretical limit of what\'s possible when flexibility is traded
for performance. \## 11.2 Google TPU: The No-MMU Approach

In 2016, Google revealed that its datacenters had been running custom AI
accelerators---Tensor Processing Units (TPUs)---for over a year. The
architecture surprised the industry not for what it included, but for
what it omitted: a Memory Management Unit. TPU v1, and its successors v2
and v3, used pure physical addressing with software-managed memory
allocation. There were no page tables, no TLB, no virtual address
translation, and no page faults. For workloads where predictability
matters more than flexibility---neural network inference and
training---this radical simplification delivered extraordinary
efficiency.

### Why Systolic Arrays Demand Predictable Memory Access

To understand why Google eliminated the MMU, we must first understand
the systolic array architecture that makes TPU fundamentally different
from GPUs.

A GPU contains thousands of independent processing cores that execute
different threads concurrently. Each core can stall independently while
waiting for memory without affecting others. If core 142 on streaming
multiprocessor 8 experiences a page fault requiring 50,000 cycles to
resolve, the other 10,751 cores continue executing their warps. The
fault is expensive but localized.

A systolic array works differently. TPU\'s matrix multiply unit consists
of a 256×256 grid of multiply-accumulate (MAC) units arranged in a
two-dimensional array. Data flows through this array in synchronized
waves, like blood pulsing through the cardiovascular system (hence
\"systolic\"). In each clock cycle, every MAC unit receives inputs from
its neighbors to the north and west, performs a multiplication, adds the
result to an accumulator, and passes results to neighbors to the south
and east. The entire array operates in lockstep---all 65,536 MAC units
execute the same operation on different data in the same cycle.

Consider a 256×256 matrix multiplication: A × B = C. The systolic array
loads matrix A from the left edge (256 elements per cycle) and matrix B
from the top edge (256 elements per cycle). These values ripple through
the array in diagonal waves. After 512 cycles (the time for data to
propagate through all 256 rows and 256 columns), the array has computed
all 65,536 output elements. Each MAC unit performs 512
multiply-accumulate operations, totaling 33.5 million operations in 512
cycles. With a 700 MHz clock, that\'s 46 billion operations per second
from a single 256×256 array---and TPU v3 has two such arrays per chip.

The critical constraint: **all 65,536 MAC units must receive their
inputs on schedule**. If a memory access to load matrix A or B
experiences a page fault, the entire array stalls. Unlike a GPU where
10,751 cores can continue while one waits for a page fault, a systolic
array has no independent execution---it\'s a single massive pipeline
that either runs at full speed or stops completely.

Quantifying the cost of a page fault on a systolic array:

    TPU v3 specifications:
    - Clock frequency: 940 MHz
    - 2× 256×256 systolic arrays per chip
    - Peak performance: 123 teraFLOPS (FP16)

    Page fault latency (if MMU existed):
    - Minimum: 10,000 cycles (optimistic, on-package memory controller)
    - Realistic: 50,000 cycles (host CPU communication)
    - Maximum: 500,000 cycles (involving host DRAM allocation)

    Performance impact:
    - Matrix multiply: 512 cycles
    - One page fault per matrix: 10,000 cycle penalty
    - Overhead: 10,000 / 512 = 19.5× slowdown per faulting operation

    With 5% page fault rate:
    - 95% of operations: 512 cycles
    - 5% of operations: 10,512 cycles
    - Average: 0.95 × 512 + 0.05 × 10,512 = 1,012 cycles
    - Effective throughput: 512 / 1,012 = 50.6% (nearly 2× slower)

    With 1% page fault rate:
    - Average: 0.99 × 512 + 0.01 × 10,512 = 612 cycles
    - Effective throughput: 512 / 612 = 83.7% (still 16% slower)

Even a 1% page fault rate---which might be acceptable on a GPU where
other threads can hide the latency---cuts TPU throughput by 16%. For a
datacenter-scale deployment where Google runs millions of inference
requests per second, 16% overhead translates to thousands of additional
servers and millions of dollars in hardware costs. Eliminating page
faults entirely isn\'t an optimization---it\'s an economic necessity.

### Static Memory Layout via XLA Compiler

Without an MMU, TPU relies on the XLA (Accelerated Linear Algebra)
compiler to generate static memory layouts at compile time. XLA analyzes
the computational graph of a neural network---the sequence of operations
from inputs to outputs---and allocates every tensor to a specific
physical address before execution begins.

Consider a simplified ResNet-50 inference:

    Layer structure (abbreviated):
    1. Input: 224×224×3 image
    2. Conv1: 7×7 convolution, 64 filters
    3. MaxPool: 3×3 pooling
    4. ResBlock1: Residual block with 3 convolutions
    5. ResBlock2: Residual block with 3 convolutions
    ... (50 layers total)
    50. Softmax: 1000-class classification

    Tensor sizes:
    Input:        224 × 224 × 3 = 150,528 elements (301 KB in FP16)
    Conv1 output: 112 × 112 × 64 = 802,816 elements (1.6 MB)
    After pool:   56 × 56 × 64 = 200,704 elements (401 KB)
    ...
    Final output: 1 × 1 × 1000 = 1,000 elements (2 KB)

    Weight sizes:
    Conv1:   7 × 7 × 3 × 64 = 9,408 parameters (19 KB)
    Conv2:   1 × 1 × 64 × 64 = 4,096 parameters (8 KB)
    ...
    Total: 25.6 million parameters (51 MB in FP16)

XLA\'s allocation strategy:

    Phase 1: Liveness analysis
    - Determine which tensors are live (needed) at each operation
    - Input tensor: Live until Conv1 completes
    - Conv1 output: Live until MaxPool completes
    - Many intermediate tensors: Live for only 2-3 operations

    Phase 2: Memory reuse
    - Identify tensors that are never live simultaneously
    - Allocate them to the same physical addresses
    - Example: Conv1 output (1.6 MB) and Conv2 output (1.6 MB)
      never overlap in time → reuse same 1.6 MB buffer

    Phase 3: Static allocation
    - Assign physical address to every tensor
    - Generate load/store instructions with physical addresses
    - No runtime allocation, no pointer arithmetic, no indirection

The result:

    Without memory reuse:
    - 50 layers × average 1 MB per activation = 50 MB
    - 51 MB parameters
    - Total: 101 MB required

    With XLA memory reuse:
    - Peak live activations: 8 MB (only 3-4 tensors live simultaneously)
    - 51 MB parameters (can't reuse, needed throughout)
    - Total: 59 MB required

    Savings: 42 MB (42% reduction)

This static allocation has profound implications:

**Advantage 1: Zero runtime memory management overhead.** No malloc/free
calls, no memory allocator logic, no fragmentation. The compiler has
already decided where every byte lives. At runtime, TPU simply executes
load/store instructions with pre-computed physical addresses.

**Advantage 2: Perfect cache utilization.** Because XLA knows the entire
access pattern, it can arrange data to maximize cache hits. Tensors
accessed sequentially can be placed in contiguous addresses. Tensors
reused across multiple operations can be sized to fit in on-chip memory
(SRAM). A ResNet-50 forward pass on TPU achieves 95%+ arithmetic
intensity (compute operations per memory access) because activations are
kept on-chip across multiple layers.

**Advantage 3: Eliminates page table overhead.** A 59 MB working set
with 4 KB pages requires 15,104 page table entries. With four-level page
tables (PML4 → PDPT → PD → PT), that\'s 15,104 leaf PTEs (121 KB) plus
higher-level structures. Total page table overhead: \~130 KB or 0.22% of
the working set. Eliminating this saves 130 KB of precious HBM capacity
and removes 15,104 potential TLB misses.

**Advantage 4: Predictable performance.** There are no page faults, no
TLB misses, no cache coherency protocols, and no virtual-to-physical
translation latency. Every memory access takes exactly the same number
of cycles: SRAM access (1 cycle), HBM access (200 cycles for first beat
of a burst, then 2 cycles per subsequent beat). This predictability
allows XLA to schedule operations with cycle-accurate precision,
overlapping computation with memory transfers to achieve
near-theoretical peak performance.

### Software-Managed Isolation Without Page Tables

Eliminating the MMU creates a security and isolation challenge: how do
you prevent one inference request from accessing another\'s data? On a
CPU or GPU, page tables provide isolation---each process has its own
page table pointing to different physical pages. Two processes can both
use virtual address 0x7fff0000, but the MMU translates these to
different physical addresses (say, 0x1000 for process A and 0x9000 for
process B). Without page tables, physical address 0x1000 is address
0x1000 for everyone.

Google\'s solution: **software-enforced isolation with separate address
spaces per request.**

TPU v3 has 32 GB of HBM per chip. Rather than allowing any code to
access any of those 32 GB, the TPU runtime divides memory into isolated
regions:

    HBM layout (32 GB total):
    0x00000000 - 0x0FFFFFFF: Runtime metadata (256 MB)
    0x10000000 - 0x1FFFFFFF: Request slot 0 (256 MB)
    0x20000000 - 0x2FFFFFFF: Request slot 1 (256 MB)
    0x30000000 - 0x3FFFFFFF: Request slot 2 (256 MB)
    ...
    0xF0000000 - 0xFFFFFFFF: Request slot 15 (256 MB)

    Each slot isolated by software convention:
    - XLA compiler generates code for slot N using addresses 0xN0000000-0xNFFFFFFF
    - Runtime loads model weights into slot N before execution
    - Code cannot reference addresses outside its slot (compiler enforces)

When an inference request arrives:

    1. Runtime allocates a free slot (e.g., slot 3)
    2. Runtime loads model parameters into slot 3 (0x30000000-0x3FFFFFFF)
    3. Runtime loads XLA-compiled code for this model
    4. Code executes, using only addresses 0x30000000-0x3FFFFFFF
    5. Results written to output buffer in slot 3
    6. Runtime copies results to host
    7. Slot 3 marked free, available for next request

This approach provides isolation, but not through hardware enforcement.
If malicious or buggy code performs a store to address 0x20000000 (slot
2) while executing in slot 3, the hardware doesn\'t prevent it. The
protection is entirely in the compiler:

**XLA verification pass:**

    For each memory operation in generated code:
      - Extract physical address
      - Verify address >= slot_base && address < slot_base + slot_size
      - If violation, reject compilation
      - If all checks pass, emit code

This software-only protection has limitations:

**Limitation 1: No protection against compiler bugs.** If XLA has a bug
that generates a store to the wrong address, nothing prevents the store
from succeeding. Hardware page protection would catch this---attempting
to write to an unmapped page triggers a fault. On TPU, the write
silently corrupts another request\'s data.

**Limitation 2: No protection against speculative execution.** Modern
CPUs execute instructions speculatively and roll back if the speculation
was wrong. Spectre attacks exploit this to read unauthorized memory.
TPU\'s in-order execution makes Spectre-style attacks unlikely, but
without hardware memory protection, there\'s no defense if an attacker
finds a way to trigger speculative reads.

**Limitation 3: No protection against DMA errors.** If a hardware bug
causes the DMA engine to write results to the wrong address, software
can\'t detect or prevent it. Page tables would map each slot to
different physical pages, so a DMA writing to slot 3\'s virtual address
couldn\'t accidentally overwrite slot 2\'s physical pages.

In practice, Google accepts these limitations because:

1.  **TPU runs only Google-compiled code.** Users submit TensorFlow or
    JAX models, Google compiles them with XLA, and Google executes the
    compiled code. There\'s no user-provided native code, reducing
    attack surface.

2.  **Datacenter environment provides perimeter security.** TPUs aren\'t
    exposed to untrusted inputs directly. Inference requests are
    sanitized by frontend servers before reaching TPUs.

3.  **The efficiency gain outweighs the risk.** Eliminating the MMU
    delivers 10-20% performance improvement (no TLB misses, no page
    table walks, no virtual address translation) and simplifies the
    hardware significantly. For Google\'s inference workload---trillions
    of requests per day---this translates to thousands of fewer servers.

### The Efficiency Payoff: Compute-to-Bandwidth Ratios

The true benefit of eliminating virtual memory becomes clear when
examining TPU\'s compute-to-bandwidth ratio---how many floating-point
operations it can perform per byte of memory bandwidth.

**TPU v4 specifications:** - Peak compute: 275 teraFLOPS (BF16) - Memory
bandwidth: 1,200 GB/s (HBM2e) - Compute-to-bandwidth ratio: 275,000
GFLOPS / 1,200 GB/s = 229 FLOPS per byte

Compare to GPU architectures:

    NVIDIA H100:
    - Peak compute: 1,000 teraFLOPS (BF16, with sparsity)
    - Memory bandwidth: 3,000 GB/s (HBM3)
    - Ratio: 1,000,000 / 3,000 = 333 FLOPS/byte (with sparsity enabled)
    - Ratio: 500,000 / 3,000 = 167 FLOPS/byte (dense operations)

    AMD MI300X:
    - Peak compute: 1,300 teraFLOPS (FP16)
    - Memory bandwidth: 5,300 GB/s (HBM3)
    - Ratio: 1,300,000 / 5,300 = 245 FLOPS/byte

Wait---H100 with sparsity has a higher ratio (333) than TPU v4 (229).
How is TPU more efficient?

The answer lies in **sustained** performance versus **peak**
performance. GPUs achieve peak compute only when TLB hit rates are high,
page faults are zero, and memory access patterns align with cache lines.
In practice:

**GPU effective compute-to-bandwidth ratio (with MMU overhead):**

    Best case (pinned memory, huge pages, perfect access pattern):
    - TLB hit rate: 99.5%
    - Page fault rate: 0%
    - Effective ratio: 320 FLOPS/byte (96% of peak)

    Typical case (unified memory, 2MB pages, streaming access):
    - TLB hit rate: 95%
    - Page fault rate: 0.1%
    - TLB miss penalty: 400ns page walk
    - Page fault penalty: 50,000 cycles
    - Effective ratio: 240 FLOPS/byte (72% of peak)

    Worst case (unified memory, 4KB pages, random access):
    - TLB hit rate: 50%
    - Page fault rate: 1%
    - Effective ratio: 120 FLOPS/byte (36% of peak)

**TPU effective compute-to-bandwidth ratio (no MMU):**

    All cases (static allocation, no virtual memory):
    - No TLB misses
    - No page faults
    - No address translation
    - Effective ratio: 229 FLOPS/byte (100% of peak)

TPU\'s advantage: **predictable, consistent performance**. It doesn\'t
matter whether you\'re running the first inference or the
millionth---TPU delivers the same throughput because there are no cache
warmup effects, no TLB misses, and no page faults. This consistency is
critical for datacenter SLAs (Service Level Agreements). When Google
promises 50ms inference latency at p99 (99th percentile), TPU\'s lack of
MMU-related variability makes that guarantee achievable.

### Why TPU v4 and v5 Added Virtual Memory

If eliminating the MMU was so successful for v1-v3, why did TPU v4 and
v5 add limited virtual memory support? Three factors drove this
decision:

**Factor 1: Model size growth beyond single-chip capacity.**

TPU v3 has 16 GB HBM per chip (doubled to 32 GB in later revisions).
This suffices for models up to about 8 billion parameters in FP16 (16 GB
parameters + 16 GB activations and optimizer state). But by 2020, models
were growing beyond this:

    GPT-3 (175B parameters):
    - Parameters: 175B × 2 bytes = 350 GB
    - Requires: 22 TPU v3 chips (16 GB each) for parameters alone
    - With optimizer state: 44 chips minimum

    PaLM (540B parameters):
    - Parameters: 540B × 2 bytes = 1,080 GB
    - Requires: 68 TPU v3 chips for parameters alone

Without virtual memory, each chip must hold a disjoint subset of the
model---parameter sharding. Chip 0 holds parameters 0-7.9B, chip 1 holds
parameters 8B-15.9B, etc. When chip 0 needs to compute gradients for its
parameters, it must receive activations from upstream chips. This
requires explicit inter-chip communication managed by software:

    # Forward pass with model parallelism (no virtual memory):
    for chip_id in range(num_chips):
        if chip_id > 0:
            activations = receive_from_chip(chip_id - 1)
        outputs = chip[chip_id].compute(activations)
        if chip_id < num_chips - 1:
            send_to_chip(chip_id + 1, outputs)

With virtual memory, the situation improves. The software can treat all
chips\' memory as a unified address space. A 1,080 GB model spans
addresses 0x0000000000000000 to 0x00000000F0000000. Each chip\'s MMU
maps its portion of this virtual address space to its local physical
memory:

    Chip 0: Maps VA 0x00000000-0x3FFFFFFF → Local PA 0x00000000-0x3FFFFFFF
    Chip 1: Maps VA 0x40000000-0x7FFFFFFF → Local PA 0x00000000-0x3FFFFFFF
    Chip 2: Maps VA 0x80000000-0xBFFFFFFF → Local PA 0x00000000-0x3FFFFFFF
    ...

When chip 0\'s code tries to access virtual address 0x50000000 (which
belongs to chip 1\'s memory), the MMU triggers a page fault. The runtime
handles this by: 1. Pausing execution on chip 0 2. Fetching the page
from chip 1 over the inter-chip interconnect 3. Caching the page in chip
0\'s local memory 4. Updating chip 0\'s page tables to map VA 0x50000000
→ local cached copy 5. Resuming execution

This on-demand paging allows code to be written as if all memory is
local, with the MMU and runtime transparently handling remote accesses.
The programming model becomes much simpler.

**Factor 2: Kubernetes integration and memory oversubscription.**

Google\'s datacenter orchestration (Borg/Kubernetes) schedules workloads
based on resource availability. A server might run multiple inference
jobs simultaneously, with Kubernetes allocating memory to each. Without
virtual memory, TPU must partition its 32 GB HBM into fixed-size slots
at boot:

    Static partitioning (TPU v3):
    - 16 slots × 2 GB each = 32 GB
    - Each inference job allocated one slot
    - If job needs only 1 GB, 1 GB wasted
    - Cannot run >16 jobs even if total usage <32 GB

With virtual memory and demand paging:

    Dynamic allocation (TPU v4):
    - Jobs allocated virtual address space (not physical memory)
    - Physical memory allocated on-demand as pages are accessed
    - Can oversubscribe: allocate 64 GB virtual but only 32 GB physical
    - If jobs don't all use memory simultaneously, no problem
    - Kernel can swap cold pages to host DRAM if needed

This flexibility increases datacenter utilization. If average inference
job uses 60% of its allocated memory, oversubscription by 1.67× (64 GB
virtual / 32 GB physical) runs the same jobs without increasing physical
memory. For a datacenter with 100,000 TPU chips, this represents
billions of dollars in capital expenditure savings.

**Factor 3: Dynamic batch sizing and attention mechanisms.**

Transformer models (BERT, GPT, PaLM) use self-attention, which has
quadratic memory complexity in sequence length. A sequence of length 512
requires 512×512 attention matrices; length 1024 requires 1024×1024. The
memory requirement varies dramatically:

    Sequence length 128:
    - Attention matrix: 128 × 128 × 2 bytes = 32 KB per head
    - 16 heads: 512 KB total

    Sequence length 2048:
    - Attention matrix: 2048 × 2048 × 2 bytes = 8 MB per head
    - 16 heads: 128 MB total (250× larger!)

With static allocation, XLA must allocate enough memory for the maximum
sequence length (2048), wasting 127.5 MB when processing shorter
sequences. With virtual memory, XLA can allocate memory on-demand:

    # Without virtual memory (static worst-case allocation):
    attention_matrix = allocate(max_seq_len * max_seq_len * heads)
    # Allocates 128 MB always, even for 128-token sequences

    # With virtual memory (dynamic allocation):
    attention_matrix = allocate(actual_seq_len * actual_seq_len * heads)
    # Allocates 32 KB for 128 tokens, 128 MB for 2048 tokens

This dynamic allocation enables variable batch sizes. Training can use
large batches (128 sequences) for short sequences and small batches (8
sequences) for long sequences, maximizing GPU utilization. Without
virtual memory, batch size must be fixed at compile time, leading to
underutilization on short sequences or out-of-memory errors on long
sequences.

### The Limited MMU Approach

TPU v4 and v5 don\'t implement full virtual memory like CPUs or GPUs.
Instead, they provide a minimal MMU supporting two use cases:

**Use Case 1: Remote memory access for model parallelism.** Page tables
can map virtual addresses to remote chips. On a page fault, the runtime
fetches the page from another chip and caches it locally. This enables
treating multiple chips as a unified memory space.

**Use Case 2: Host memory swapping for dynamic allocation.** If a chip
runs out of local HBM, the runtime can allocate virtual pages backed by
host DRAM. Accessing these pages triggers a fault, the runtime fetches
data from host over PCIe, and caches it in HBM. This is slow (PCIe
latency: 1-10μs vs HBM latency: 100ns) but allows oversubscription.

What TPU v4/v5 do **not** support:

- **General-purpose paging:** Can\'t run arbitrary code with
  malloc/free. XLA still generates static layouts; the MMU just extends
  those layouts beyond local memory.
- **Fine-grained page faults:** The page size is large (128 KB minimum,
  often 2 MB) to minimize fault overhead.
- **Speculative execution with page faults:** The pipeline is in-order;
  page faults stall the entire chip.
- **TLB large enough for dynamic workloads:** TLB has only 256-512
  entries, sufficient for model parallelism (few remote accesses) but
  not for random access patterns.

This \"limited MMU\" approach preserves most of TPU\'s efficiency (no
TLB misses in the common case, no page faults for local memory) while
adding flexibility for large models and dynamic batching. It\'s a
pragmatic compromise: embrace virtual memory where it solves real
problems (model parallelism, oversubscription) but avoid it where it
adds overhead without benefit (local memory access).

### Lessons for Accelerator Design

TPU\'s evolution from no MMU (v1-v3) to limited MMU (v4-v5) reveals
fundamental trade-offs in accelerator memory management:

**When to avoid virtual memory entirely:** - Workloads with completely
predictable memory access (inference on fixed models) - Strong isolation
not required (single-tenant datacenter environment) - Model fits in
single-chip memory (no need for distributed address space) - Performance
consistency is critical (SLA guarantees)

**When virtual memory becomes necessary:** - Models exceed single-chip
capacity (need model parallelism) - Dynamic allocation required
(variable batch sizes, sequence lengths) - Memory oversubscription
benefits (datacenter utilization) - Multi-tenant environment (need
hardware isolation)

For NVIDIA, AMD, and Intel GPUs targeting general-purpose computing,
full virtual memory is non-negotiable---users run arbitrary code with
unpredictable access patterns. But for domain-specific accelerators like
TPU, the question remains open: is the flexibility worth the overhead?
Google\'s answer evolved from \"no\" (v1-v3) to \"sometimes\" (v4-v5),
suggesting that as AI models continue growing, the benefits of virtual
memory---despite its costs---become increasingly difficult to avoid. \##
11.3 Page Fault Storms and Mitigation Strategies

Chapter 4, Section 4.13 established that GPU page faults are
expensive---50,000 to 500,000 cycles compared to CPUs\' 1,000-10,000
cycles. The basic mechanism is clear: GPU access unmapped page → notify
CPU driver via PCIe → CPU allocates page → GPU replays access. But
understanding the mechanism doesn\'t prepare you for what happens in
production when thousands of GPU threads fault simultaneously, creating
a page fault storm that reduces throughput from 100% to 15% in seconds.

This section explores the operational reality of GPU page faults: how
they occur in typical AI/ML workloads, why they cascade into
catastrophic performance degradation, and how to structure memory
management to eliminate them without sacrificing the flexibility that
virtual memory provides.

### Anatomy of a Page Fault Storm

Consider a typical deep learning training loop processing batches of
data:

``` {.sourceCode .python}
for epoch in range(num_epochs):
    for batch in dataloader:
        # Batch contains 1,024 images, each 224×224×3 = 150,528 bytes
        # Total batch size: 1,024 × 150KB = 154 MB
        
        inputs = batch['images'].cuda()  # Transfer to GPU
        labels = batch['labels'].cuda()
        
        outputs = model(inputs)          # Forward pass
        loss = criterion(outputs, labels)
        loss.backward()                  # Backward pass
        optimizer.step()                 # Update parameters
```

This innocent-looking code can trigger thousands of simultaneous page
faults. Here\'s how:

**First Batch (Cold Start):**

When `batch['images'].cuda()` executes on the first batch, the CUDA
runtime allocates GPU memory for the 154 MB batch. With NVIDIA\'s
Unified Memory, this allocation creates virtual memory mappings but
doesn\'t migrate pages immediately---pages migrate on first access.

The forward pass (`model(inputs)`) accesses the input tensor. All 10,752
CUDA cores (on an A100) begin reading input data simultaneously. With 4
KB pages, the 154 MB batch spans:

    154 MB / 4 KB = 39,424 pages

The GPU\'s L2 TLB has 2,048 entries. It can cover:

    2,048 entries × 4 KB = 8 MB (5% of the batch)

The remaining 95% of accesses miss the TLB. Each miss triggers: 1. Check
L2 TLB → miss 2. Request translation from MMU 3. MMU checks page table →
page not present 4. MMU initiates page fault 5. Notify CPU driver 6. CPU
allocates page, updates PTE 7. GPU invalidates stale TLB entry 8. GPU
retries access

Steps 4-7 require PCIe round-trips: GPU → CPU (page fault notification)
and CPU → GPU (page fault completion). PCIe 4.0 ×16 provides \~32 GB/s
bandwidth, but latency for a round-trip message is \~1-2 µs. For 39,424
page faults:

    39,424 faults × 2 µs per fault = 78.8 ms

But it\'s worse than this. The faults don\'t serialize (one at a time)
because multiple warps execute concurrently. NVIDIA\'s page fault
handling can process \~1,000 faults per millisecond in parallel, but
eventually saturates. With 39,424 faults:

    39,424 / 1,000 faults/ms = 39.4 ms minimum

During these 39 ms, the GPU is mostly idle---warps that faulted stall
waiting for pages, while warps that didn\'t fault quickly complete and
also stall (waiting for barriers or dependent operations).

**Occupancy Impact:**

GPU performance relies on high occupancy---keeping thousands of threads
active to hide latency. An A100 has 108 Streaming Multiprocessors (SMs),
each supporting up to 64 warps (2,048 threads). Maximum occupancy: 108
SMs × 64 warps = 6,912 warps.

When page faults occur: 1. Faulting warp stalls (blocks on page fault)
2. SM cannot retire the warp (it\'s waiting for a page) 3. SM cannot
schedule new warps (warp slots full) 4. Effective occupancy drops

If 4,000 warps fault (reasonable for a 154 MB batch):

    Active warps: 6,912 - 4,000 = 2,912 (42% occupancy)
    Compute utilization: ~42% (proportional to occupancy)

Low occupancy means compute units sit idle even though the GPU has work
to do. This is the hidden cost of page faults: not just the fault
latency itself, but the reduced parallelism that prevents hiding other
latencies.

**Second Batch (Partially Warm):**

The second batch uses different images (different memory addresses). If
the dataloader doesn\'t reuse buffers, it allocates a new 154 MB region.
The TLB from the first batch is now useless---all entries map the
previous batch\'s addresses.

This creates a second page fault storm of similar magnitude. Over 100
batches:

    100 batches × 39.4 ms per batch = 3.94 seconds of page fault handling
    100 batches × 50 ms compute per batch = 5 seconds of computation

    Total time: 8.94 seconds
    Efficiency: 5 / 8.94 = 56%

    44% of time wasted on page faults!

### Migration Thrashing: The Ping-Pong Problem

Page fault storms are bad enough when pages migrate once (CPU → GPU).
Migration thrashing occurs when pages bounce back and forth repeatedly,
multiplying overhead.

**Scenario: CPU Preprocessing with GPU Inference**

``` {.sourceCode .python}
while True:
    # CPU preprocessing
    image = load_image()
    preprocessed = cpu_preprocess(image)  # Resize, normalize, augment
    
    # GPU inference
    output = gpu_model(preprocessed)
    
    # CPU postprocessing
    result = cpu_postprocess(output)      # NMS, top-k, formatting
    send_result(result)
```

With Unified Memory, `preprocessed` and `output` are allocated in
unified address space, accessible from both CPU and GPU. The page
migration pattern:

**Frame 0:**

    1. load_image: Allocate on CPU (pages CPU-resident)
    2. cpu_preprocess: Access on CPU (pages stay on CPU)
    3. gpu_model: Access on GPU
       → Page fault on GPU
       → Migrate pages CPU → GPU (50 µs per page)
    4. cpu_postprocess: Access on CPU
       → Page fault on CPU
       → Migrate pages GPU → CPU (50 µs per page)

**Frame 1:**

    1. load_image: Allocate on CPU (pages CPU-resident)
    2. cpu_preprocess: Access on CPU (pages stay on CPU)
    3. gpu_model: Access on GPU
       → Page fault again! (pages are on CPU)
       → Migrate pages CPU → GPU (50 µs per page)
    4. cpu_postprocess: Access on CPU
       → Page fault again! (pages are on GPU)
       → Migrate pages GPU → CPU (50 µs per page)

Every frame triggers 4 migrations (2 CPU→GPU, 2 GPU→CPU). For a 10 MB
intermediate buffer:

    10 MB / 4 KB = 2,560 pages
    2,560 pages × 50 µs × 4 migrations = 512 ms per frame

    At 30 FPS: Need 33 ms per frame
    Actual: 512 ms per frame
    Result: ~1.5 FPS (instead of 30 FPS)

The code is correct---no bugs, no errors. But the memory access pattern
is catastrophic for Unified Memory\'s page migration.

**Root Cause:**

Unified Memory uses a first-touch policy: pages migrate to the device
that first accesses them. Once resident, pages stay there until another
device accesses them (triggering migration back). This works well for
static access patterns: - CPU allocates once, GPU accesses repeatedly →
pages migrate to GPU, stay there - GPU computes once, CPU consumes
result → pages migrate to CPU, stay there

But alternating access patterns (CPU → GPU → CPU → GPU) defeat the
heuristic. Every access triggers migration because the page is always on
the \"wrong\" device.

### Mitigation Strategy 1: Prefetching

The simplest solution: tell the GPU which pages to fetch before
accessing them.

**Explicit Prefetch:**

``` {.sourceCode .c}
// Before: Page fault storm
kernel<<<blocks, threads>>>(data);

// After: Prefetch entire region
cudaMemPrefetchAsync(data, size, device_id, stream);
cudaStreamSynchronize(stream);  // Wait for prefetch to complete
kernel<<<blocks, threads>>>(data);
```

`cudaMemPrefetchAsync` initiates page migration without waiting for page
faults. The GPU\'s memory management unit migrates pages in the
background while the CPU continues execution. When the kernel launches,
pages are already resident---no faults.

**Batched Prefetching:**

For training loops, prefetch the next batch while processing the current
batch:

``` {.sourceCode .python}
# Allocate buffers for two batches
buffer_a = allocate_unified_memory(batch_size)
buffer_b = allocate_unified_memory(batch_size)

# Prefetch first batch
prefetch_async(buffer_a, gpu, stream_a)

for i, batch in enumerate(dataloader):
    # Current batch in buffer_a, next batch will use buffer_b
    current_buffer = buffer_a if i % 2 == 0 else buffer_b
    next_buffer = buffer_b if i % 2 == 0 else buffer_a
    
    # Wait for current batch prefetch to complete
    stream_synchronize(stream_a if i % 2 == 0 else stream_b)
    
    # Process current batch (no page faults!)
    copy_to_buffer(batch, next_buffer)  # On CPU, doesn't block
    output = model(current_buffer)      # On GPU, uses prefetched data
    
    # Prefetch next batch (overlaps with processing)
    prefetch_async(next_buffer, gpu, stream_b if i % 2 == 0 else stream_a)
```

This double-buffering technique overlaps prefetching with computation.
While the GPU processes batch N, the CPU prepares batch N+1 and
prefetches it. When batch N completes, batch N+1 is already
resident---zero fault latency.

**Measured Impact:**

Production deep learning training:

    Naive (no prefetch):       120 ms per batch, 15,000 page faults
    Basic prefetch:            65 ms per batch, 200 page faults (residual)
    Double-buffered prefetch:  48 ms per batch, 0 page faults
    Speedup: 2.5×

The residual 200 faults with basic prefetch come from edge cases: very
large batches where prefetch doesn\'t complete before the kernel starts,
or dynamic allocations within kernels that couldn\'t be prefetched.

### Mitigation Strategy 2: Pinning Critical Structures

Prefetching eliminates faults for transient data (batches that change
every iteration). But some data persists across iterations: model
parameters, optimizer state, batch norm statistics. Pinning ensures
these never fault.

**Pinning Model Parameters:**

``` {.sourceCode .c}
// Allocate model parameters in GPU-pinned memory
cudaMalloc(&model_params, param_size);  // Not unified memory

// Initialize on GPU
initialize_parameters<<<...>>>(model_params);

// Parameters stay on GPU forever, never fault
for (int iter = 0; iter < num_iters; iter++) {
    forward_pass<<<...>>>(model_params, batch_data);
    backward_pass<<<...>>>(model_params, batch_data, gradients);
    optimizer_step<<<...>>>(model_params, gradients);
}
```

With `cudaMalloc` (not `cudaMallocManaged`), memory is device-only, not
unified. The CPU cannot access it directly---attempting to dereference
`model_params` on the CPU causes a segfault, not a page fault. This is
stricter but eliminates page fault possibility.

**Hybrid Approach:**

Pin hot paths, use unified memory for cold paths:

``` {.sourceCode .c}
// Hot path: Model parameters accessed every iteration
cudaMalloc(&model_params, 1GB);  // Pinned to GPU

// Cold path: Intermediate activations, recomputed each batch
cudaMallocManaged(&activations, 2GB);  // Unified, can fault

// Cold path: Gradient accumulation buffer, rarely accessed
cudaMallocManaged(&grad_accum, 1GB);  // Unified, can fault
```

This balances flexibility (unified memory for infrequent access) and
performance (pinned memory for critical paths).

**When Pinning Backfires:**

Pinning all 420 GB for a 70B parameter model is impractical: - Model
parameters: 140 GB → Pin to GPU - Optimizer state: 280 GB → Too large to
pin (exceeds 80 GB GPU memory)

Solution: Pin parameters, use unified memory for optimizer state with
prefetching:

``` {.sourceCode .c}
cudaMalloc(&parameters, 140GB);  // Pinned

// Optimizer state in unified memory
cudaMallocManaged(&optimizer_first_moment, 280GB);
cudaMallocManaged(&optimizer_second_moment, 280GB);

// Before optimizer step, prefetch optimizer state
cudaMemPrefetchAsync(optimizer_first_moment, 280GB, gpu, stream);
cudaMemPrefetchAsync(optimizer_second_moment, 280GB, gpu, stream);

optimizer_step<<<...>>>(parameters, gradients, optimizer_first_moment, optimizer_second_moment);
```

This reduces page faults on the hot path (parameter access during
forward/backward) while tolerating occasional faults on the optimizer
step (once per batch, less critical).

### Mitigation Strategy 3: cudaMemAdvise for Access Patterns

CUDA\'s `cudaMemAdvise` API provides hints about how memory will be
accessed, enabling smarter migration and prefetching:

**Hint 1: Preferred Location**

``` {.sourceCode .c}
cudaMemAdvise(params, size, cudaMemAdviseSetPreferredLocation, gpu_device);
```

Tells the CUDA runtime that `params` should ideally reside on GPU. Even
if the CPU accesses it (causing migration to CPU), the runtime will
migrate it back to GPU afterward. This prevents permanent migration to
CPU after occasional CPU access.

**Hint 2: Read-Only**

``` {.sourceCode .c}
cudaMemAdvise(params, size, cudaMemAdviseSetReadMostly, 0);
```

Indicates that `params` is read frequently, written rarely. The runtime
creates read-only replicas on multiple devices. All devices can read
without faulting (accessing their local replica). Writes invalidate
replicas (requiring refresh), but writes are rare.

Use case: Model parameters during inference. All GPUs read parameters,
no GPU writes them. Replicate parameters to all GPUs at startup,
avoiding read faults entirely.

**Hint 3: Accessed By**

``` {.sourceCode .c}
cudaMemAdvise(buffer, size, cudaMemAdviseSetAccessedBy, gpu_0);
cudaMemAdvise(buffer, size, cudaMemAdviseSetAccessedBy, gpu_1);
```

Informs the runtime that `buffer` will be accessed by both `gpu_0` and
`gpu_1`. The runtime creates mappings for both devices at allocation
time, avoiding first-access faults.

**Combined Example:**

``` {.sourceCode .c}
// Model parameters: Read-only, accessed by all 8 GPUs
cudaMallocManaged(&params, 140GB);
cudaMemAdvise(params, 140GB, cudaMemAdviseSetReadMostly, 0);
for (int gpu = 0; gpu < 8; gpu++) {
    cudaMemAdvise(params, 140GB, cudaMemAdviseSetAccessedBy, gpu);
}

// Activations: Written by one GPU, read by another (pipeline parallelism)
cudaMallocManaged(&act_gpu0_to_gpu1, 4GB);
cudaMemAdvise(act_gpu0_to_gpu1, 4GB, cudaMemAdviseSetAccessedBy, 0);
cudaMemAdvise(act_gpu0_to_gpu1, 4GB, cudaMemAdviseSetAccessedBy, 1);

// Gradients: Device-specific, only one GPU accesses
cudaMallocManaged(&grad_gpu0, 2GB);
cudaMemAdvise(grad_gpu0, 2GB, cudaMemAdviseSetPreferredLocation, 0);
```

These hints don\'t guarantee zero faults, but they reduce fault rates by
80-95% in workloads with clear access patterns.

### Mitigation Strategy 4: Structuring the Training Loop

Sometimes the best mitigation is restructuring the workload to avoid
migration entirely:

**Anti-Pattern: Alternating Access**

``` {.sourceCode .python}
for batch in dataloader:
    # CPU loads data
    images, labels = batch  # CPU access
    
    # GPU processes
    outputs = gpu_model(images)  # GPU access → migration!
    
    # CPU validates
    accuracy = cpu_validate(outputs)  # CPU access → migration!
```

Three migrations per batch (CPU→GPU for images, GPU→CPU for outputs,
possibly CPU→GPU again for next batch).

**Pattern: Batched Processing**

``` {.sourceCode .python}
# Load many batches on CPU
cpu_batches = [dataloader[i] for i in range(100)]

# Transfer all to GPU once
gpu_batches = [b.cuda(non_blocking=True) for b in cpu_batches]
synchronize()  # Wait for all transfers

# Process entirely on GPU
gpu_outputs = [gpu_model(b) for b in gpu_batches]

# Transfer all results back once
cpu_outputs = [o.cpu() for o in gpu_outputs]

# Validate on CPU
accuracy = cpu_validate(cpu_outputs)
```

This reduces migrations from 300 (100 batches × 3 migrations) to 200
(100 transfers to GPU + 100 transfers from GPU), a 33% reduction. More
importantly, migrations are explicit (`.cuda()` and `.cpu()`) rather
than implicit (page faults), giving better control.

**Anti-Pattern: Small Frequent Allocations**

``` {.sourceCode .c}
for (int i = 0; i < 10000; i++) {
    cudaMallocManaged(&temp, 1MB);
    kernel<<<...>>>(temp);  // Page faults on temp
    cudaFree(temp);
}
```

10,000 separate allocations, each triggering page faults.

**Pattern: Pre-allocated Buffer Pool**

``` {.sourceCode .c}
cudaMallocManaged(&pool, 10000MB);
cudaMemPrefetchAsync(pool, 10000MB, gpu, stream);

for (int i = 0; i < 10000; i++) {
    void *temp = pool + i * 1MB;  // Pointer arithmetic, no allocation
    kernel<<<...>>>(temp);        // No page faults!
}

cudaFree(pool);
```

Single allocation, single prefetch, zero page faults during the loop.

### Real-World Case Study: Stable Diffusion Inference

A company deployed Stable Diffusion (text-to-image generation) for
inference serving with SLA: 95% of requests \< 5 seconds. Initial
deployment used naive Unified Memory:

``` {.sourceCode .python}
def generate_image(prompt):
    # Tokenize on CPU
    tokens = tokenizer.encode(prompt)  # CPU-resident
    
    # Text encoding on GPU
    text_embedding = text_encoder(tokens)  # Migrates tokens to GPU
    
    # Diffusion on GPU
    image_latent = diffusion_model(text_embedding)  # GPU-resident
    
    # Decode on GPU
    image = vae_decoder(image_latent)  # GPU-resident
    
    # Post-process on CPU
    final = cpu_postprocess(image)  # Migrates image to CPU
    
    return final
```

**Observed Performance:**

    P50 latency: 4.2 seconds (within SLA)
    P95 latency: 12.8 seconds (violates SLA!)
    Page faults per request: 8,000-15,000

The P95 latency violations came from page fault storms. Most requests
completed quickly (warm TLB), but every \~20th request hit cold TLB and
triggered thousands of faults.

**Optimization:**

``` {.sourceCode .python}
# Preallocate and pin all buffers at server startup
class StableDiffusionServer:
    def __init__(self):
        # Pin model parameters (3 models × 2GB = 6GB)
        self.text_encoder = load_model_pinned('text_encoder')
        self.diffusion_model = load_model_pinned('diffusion')
        self.vae_decoder = load_model_pinned('vae')
        
        # Pre-allocate unified buffers for intermediate results
        self.token_buffer = allocate_unified(1KB)
        self.embedding_buffer = allocate_unified(512KB)
        self.latent_buffer = allocate_unified(4MB)
        self.image_buffer = allocate_unified(16MB)
        
        # Prefetch all buffers to GPU
        for buf in [self.token_buffer, self.embedding_buffer, 
                   self.latent_buffer, self.image_buffer]:
            cudaMemPrefetchAsync(buf, buf.size, gpu, stream)
    
    def generate_image(self, prompt):
        # Reuse preallocated buffers (no allocation, no migration)
        tokens = self.tokenizer.encode(prompt, self.token_buffer)
        text_embedding = self.text_encoder(tokens, self.embedding_buffer)
        image_latent = self.diffusion_model(text_embedding, self.latent_buffer)
        image = self.vae_decoder(image_latent, self.image_buffer)
        
        # Copy final result to CPU (small, happens once)
        final = self.image_buffer.cpu()
        return final
```

**Result:**

    P50 latency: 3.8 seconds (10% faster)
    P95 latency: 4.5 seconds (64% faster, now within SLA!)
    Page faults per request: 0

    Page fault elimination reduced P95 latency by 8.3 seconds.

The changes: 1. Pin model parameters (never fault) 2. Pre-allocate
intermediate buffers (allocate once at startup, not per request) 3.
Prefetch buffers to GPU (resident before first request) 4. Reuse buffers
across requests (pointer reuse, not allocation)

Result: Zero page faults during inference, deterministic latency, SLA
compliance.

### Summary: Page Fault Mitigation Principles

**Principle 1: Prefetch Everything Predictable**

If you know a buffer will be accessed, prefetch it before the access.
Training loops and inference pipelines have predictable access
patterns---exploit this.

**Principle 2: Pin Critical Paths**

Model parameters accessed every iteration should never fault. Pin them
to GPU at startup.

**Principle 3: Allocate Once, Reuse Many**

Allocating per-iteration triggers faults every time. Allocate buffers
once, reuse them.

**Principle 4: Structure Access Patterns**

Alternating CPU/GPU access causes migration thrashing. Batch processing
on one device, then transfer to the other.

**Principle 5: Measure and Monitor**

Use `nvidia-smi --query-gpu=page_fault --format=csv` to monitor fault
rates. If faults \>1,000/sec, investigate. High fault rates indicate
misconfiguration.

Next, we\'ll examine what happens when page faults occur not just on one
GPU, but across 1,000 GPUs simultaneously---requiring coordination of
TLB invalidations at a scale that naive approaches cannot handle. \##
11.4 Multi-GPU TLB Synchronization: Coordinating Thousands of Devices

Chapter 4, Section 4.5 covered TLB shootdown on multi-core CPUs: when
one core modifies a page table, it must invalidate TLB entries on all
other cores to maintain coherency. A typical server with 128 CPU cores
requires broadcasting invalidations to 127 other cores---a well-studied
problem with established solutions (IPI-based shootdown, hardware
broadcast via shareability domains on ARM).

But AI/ML training operates at a different scale. OpenAI\'s GPT-4
training used 25,000 NVIDIA A100 GPUs. Meta\'s LLaMA 70B training used
2,048 A100 GPUs. Google\'s PaLM training used 6,144 TPU v4 chips. When
you modify a page table that affects all these devices, you must
invalidate tens of thousands of TLB entries distributed across thousands
of chips. Naive approaches serialize these invalidations, creating
multi-millisecond stalls. Optimized approaches use hardware broadcast,
reducing latency by 500× but requiring careful protocol design to ensure
correctness.

This section explores multi-GPU TLB synchronization: why it matters, how
naive approaches fail, how NVSwitch and NVLink enable hardware
broadcast, and what the synchronization protocol looks like in
production systems.

### The Scale Problem: Why Multi-GPU TLB Invalidation Differs from Multi-Core

On a CPU with 128 cores, TLB shootdown targets 127 other cores---all on
the same chip, connected by an on-chip coherent interconnect. Sending an
invalidation message and waiting for acknowledgment takes \~200-500
nanoseconds per core.

On a multi-GPU training cluster, the topology is fundamentally
different:

**256-GPU System (8 Servers × 32 GPUs Each):**

    Server 1: 32 GPUs connected via NVSwitch
    Server 2: 32 GPUs connected via NVSwitch
    ...
    Server 8: 32 GPUs connected via NVSwitch

    Servers interconnected via 8× 400Gbps InfiniBand

When GPU 0 on Server 1 needs to invalidate a TLB entry, it must reach: -
31 other GPUs on the same server (via NVSwitch, \~500 nanoseconds) - 224
GPUs on remote servers (via InfiniBand, \~10-50 microseconds)

The latency hierarchy matters. A 10 µs invalidation to 224 remote GPUs
is 20× slower than a 500 ns invalidation to 31 local GPUs. If you
serialize 256 invalidations:

    Serial TLB shootdown:
    Local GPUs:  31 × 0.5 µs = 15.5 µs
    Remote GPUs: 224 × 10 µs = 2,240 µs
    Total: 2,255 µs = 2.26 ms

This 2.26 ms stall occurs **every time a page table entry changes**. For
workloads that modify page tables frequently (dynamic batch sizing,
gradient accumulation buffers, checkpointing), this overhead is
catastrophic.

**Impact on Training Throughput:**

Consider distributed training with gradient all-reduce. Each training
iteration: 1. Forward pass: \~50 ms 2. Backward pass: \~50 ms 3.
All-reduce gradients: \~30 ms 4. Optimizer step: \~20 ms **Total: 150 ms
per iteration**

If the optimizer step involves freeing old gradient buffers and
allocating new ones (common in dynamic batch sizing), this triggers page
table updates requiring TLB invalidation:

    Iteration without TLB overhead: 150 ms
    TLB invalidation overhead: 2.26 ms
    Total: 152.26 ms
    Overhead: 1.5%

    Over 1000 iterations: 1.5% × 150,000 ms = 2,250 ms = 2.25 seconds wasted

This seems minor---1.5% overhead is barely noticeable. But training
large models takes weeks. A 1.5% overhead on a 3-week training run
wastes:

    3 weeks × 7 days × 24 hours = 504 hours
    1.5% of 504 hours = 7.56 hours wasted on TLB invalidations

At \$3-5 per GPU-hour for 256 GPUs, that\'s \$5,800-9,700 wasted on
overhead.

### Naive Approach: Serial TLB Invalidation

The straightforward implementation sends invalidations sequentially:

``` {.sourceCode .c}
void tlb_invalidate_multi_gpu(void *va, size_t size) {
    for (int gpu = 0; gpu < num_gpus; gpu++) {
        send_invalidate_message(gpu, va, size);
        wait_for_acknowledgment(gpu);
    }
}
```

This is correct but slow. Each `send_invalidate_message` requires: 1.
Pack message (virtual address, size, invalidation type) 2. Send via
PCIe/NVLink (100-500 ns local, 10-50 µs remote) 3. GPU receives message,
processes it 4. GPU invalidates matching TLB entries 5. GPU sends
acknowledgment 6. Caller receives acknowledgment, proceeds to next GPU

For 256 GPUs, this serializes 256 round-trips. Measured latency:

    Experiment: munmap() a 2 MB region on 256-GPU cluster

    Serial invalidation:
    GPU 0-31 (local):  31 × 0.8 µs = 24.8 µs
    GPU 32-255 (remote): 224 × 12 µs = 2,688 µs
    Total: 2,713 µs = 2.7 ms

    For comparison, munmap() on single GPU: 8 µs
    Slowdown: 2,713 / 8 = 339×

The 339× slowdown makes `munmap()` prohibitively expensive. Applications
that use dynamic allocation (freeing and reallocating buffers) become
bottlenecked on page table operations.

**Why Not Parallelize?**

You could send invalidations to all GPUs simultaneously without waiting
for each acknowledgment:

``` {.sourceCode .c}
void tlb_invalidate_multi_gpu_parallel(void *va, size_t size) {
    for (int gpu = 0; gpu < num_gpus; gpu++) {
        send_invalidate_message(gpu, va, size);  // Don't wait
    }
    
    for (int gpu = 0; gpu < num_gpus; gpu++) {
        wait_for_acknowledgment(gpu);  // Wait for all
    }
}
```

This reduces latency from SUM(latencies) to MAX(latency):

    Parallel invalidation:
    All local GPUs:  0.8 µs (parallel, limited by slowest)
    All remote GPUs: 12 µs (parallel, limited by slowest)
    Total: 12 µs (vs 2.7 ms serial)

    Speedup: 2,713 / 12 = 226×

But this still requires 256 separate messages---each consuming
bandwidth, each requiring separate processing. At high invalidation
rates (1,000 invalidations/sec), you\'d send:

    1,000 invalidations/sec × 256 GPUs = 256,000 messages/sec

This message traffic saturates the interconnect. A better solution:
hardware broadcast.

### NVSwitch: Hardware-Accelerated TLB Broadcast

NVIDIA\'s NVSwitch is a high-bandwidth, low-latency switch connecting up
to 32 GPUs in a single server. Originally designed for data transfers
(enabling 600 GB/s per GPU bandwidth), NVSwitch also supports TLB
invalidation broadcast.

**NVSwitch Architecture:**

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="420" viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" style="fill:#212121" />
    </marker>
    <marker id="arrb" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" style="fill:#1565C0" />
    </marker>
    <filter id="sh" x="-5%" y="-5%" width="115%" height="115%">
      <fedropshadow dx="2" dy="3" stddeviation="4" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
  </defs>

  <text x="450" y="30" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">NVSwitch: Hardware-Accelerated TLB Broadcast (DGX H100)</text>

  <!-- NVSwitch central hub -->
  <rect x="330" y="55" width="240" height="80" rx="6" filter="url(#sh)" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
  <text x="450" y="87" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:16; font-weight:bold; text-anchor:middle">NVSwitch (×4 per DGX)</text>
  <text x="450" y="107" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:13; text-anchor:middle">Non-blocking crossbar • 13.6 TB/s bisection BW</text>
  <text x="450" y="124" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:13; text-anchor:middle">Hardware TLB invalidation broadcast</text>

  <!-- GPU 0 -->
  <rect x="20" y="240" width="125" height="80" rx="6" filter="url(#sh)" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  <text x="82" y="274" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">GPU 0</text>
  <text x="82" y="293" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">H100 SXM5</text>
  <text x="82" y="310" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">80 GB HBM3</text>

  <!-- GPU 1 -->
  <rect x="165" y="240" width="125" height="80" rx="6" filter="url(#sh)" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  <text x="227" y="274" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">GPU 1</text>
  <text x="227" y="293" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">H100 SXM5</text>
  <text x="227" y="310" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">80 GB HBM3</text>

  <!-- GPU 2-5 (middle) -->
  <rect x="330" y="240" width="240" height="80" rx="6" filter="url(#sh)" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
  <text x="450" y="274" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">GPU 2 … GPU 5</text>
  <text x="450" y="295" font-family="Arial,Helvetica,sans-serif" style="fill:#B2DFDB; font-size:12; text-anchor:middle">Same configuration</text>
  <text x="450" y="312" font-family="Arial,Helvetica,sans-serif" style="fill:#B2DFDB; font-size:12; text-anchor:middle">×4 NVLink 4.0 per GPU</text>

  <!-- GPU 6 -->
  <rect x="590" y="240" width="125" height="80" rx="6" filter="url(#sh)" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  <text x="652" y="274" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">GPU 6</text>
  <text x="652" y="293" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">H100 SXM5</text>
  <text x="652" y="310" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">80 GB HBM3</text>

  <!-- GPU 7 -->
  <rect x="735" y="240" width="125" height="80" rx="6" filter="url(#sh)" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  <text x="797" y="274" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">GPU 7</text>
  <text x="797" y="293" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">H100 SXM5</text>
  <text x="797" y="310" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">80 GB HBM3</text>

  <!-- NVLink connections (bidirectional arrows, blue) -->
  <line x1="82" y1="240" x2="380" y2="135" style="stroke:#1565C0; stroke-width:2.5"></line>
  <line x1="227" y1="240" x2="400" y2="135" style="stroke:#1565C0; stroke-width:2.5"></line>
  <line x1="450" y1="240" x2="450" y2="135" style="stroke:#1565C0; stroke-width:2.5"></line>
  <line x1="652" y1="240" x2="500" y2="135" style="stroke:#1565C0; stroke-width:2.5"></line>
  <line x1="797" y1="240" x2="520" y2="135" style="stroke:#1565C0; stroke-width:2.5"></line>

  <!-- NVLink bandwidth labels -->
  <text x="195" y="200" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:12; text-anchor:middle">NVLink 4.0</text>
  <text x="195" y="216" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:12; text-anchor:middle">900 GB/s total</text>

  <!-- TLB invalidation broadcast annotation -->
  <rect x="20" y="355" width="860" height="55" rx="6" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="450" y="376" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">TLB Invalidation Broadcast Flow</text>
  <text x="450" y="397" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">GPU issues TLBI → NVSwitch replicates to all peers in hardware → each GPU invalidates matching TLB entries atomically</text>
</svg>
</div>
<figcaption><strong>Figure 11.nvswitch:</strong> NVSwitch
hardware-accelerated TLB broadcast in DGX H100: each GPU connects via
NVLink 4.0 (900 GB/s bidirectional) to NVSwitch crossbars; TLB
invalidation commands are replicated in hardware to all 8 GPUs
simultaneously, eliminating software broadcast overhead.</figcaption>
</figure>

**Broadcast Mechanism:**

Instead of GPU 0 sending 31 separate messages to GPUs 1-31, GPU 0 sends
**one message to NVSwitch** with a broadcast flag. NVSwitch replicates
this message to all 31 other GPUs simultaneously.

``` {.sourceCode .c}
// Old: 31 separate messages
for (int gpu = 1; gpu < 32; gpu++) {
    send_invalidate_message(gpu, va, size);
}

// New: 1 broadcast message
nvswitch_broadcast_invalidate(va, size);
```

**Latency Comparison:**

    Without NVSwitch (31 GPUs, serial):
    31 × 0.8 µs = 24.8 µs

    With NVSwitch (broadcast to 31 GPUs):
    1 broadcast + 31 parallel invalidations = 2.5 µs

    Speedup: 24.8 / 2.5 = 9.9×

The speedup comes from two factors: 1. Single message instead of 31
(reduces software overhead) 2. Parallel invalidation (all GPUs receive
simultaneously)

**Bandwidth Savings:**

    Without NVSwitch:
    31 messages × 64 bytes per message = 1,984 bytes per invalidation

    With NVSwitch:
    1 message × 64 bytes = 64 bytes per invalidation

    Bandwidth reduction: 1,984 / 64 = 31×

At 1,000 invalidations/second, this reduces traffic from 2 MB/s to 64
KB/s---negligible compared to NVLink\'s 600 GB/s capacity.

### Multi-Server Coordination: Combining NVSwitch and RDMA

NVSwitch handles single-server coordination efficiently. But
multi-server clusters require coordination across servers, typically via
RDMA over InfiniBand or RoCE.

**256-GPU Topology (8 Servers):**

    Server 1: GPUs 0-31 (NVSwitch broadcast within server)
    Server 2: GPUs 32-63 (NVSwitch broadcast within server)
    ...
    Server 8: GPUs 224-255 (NVSwitch broadcast within server)

    Servers connected via InfiniBand

**Two-Level Invalidation Protocol:**

1.  **Intra-server broadcast** (via NVSwitch):
    - GPU 0 sends broadcast to GPUs 1-31: \~2.5 µs
2.  **Inter-server notification** (via RDMA):
    - GPU 0 on Server 1 sends RDMA message to GPU 0 on Servers 2-8
    - Each remote server\'s GPU 0 receives message: \~10 µs
    - Each remote GPU 0 broadcasts to its local GPUs 1-31: \~2.5 µs

**Total Latency:**

    Step 1: Local NVSwitch broadcast:              2.5 µs
    Step 2: RDMA to 7 remote servers (parallel):  10.0 µs
    Step 3: Remote NVSwitch broadcasts (parallel): 2.5 µs
    Total: 15 µs

    Compare to serial:
    31 local + 224 remote = 31 × 0.8 + 224 × 12 = 2,713 µs

    Speedup: 2,713 / 15 = 181×

**Acknowledgment Collection:**

After invalidation, the initiating GPU must wait for acknowledgments
from all 256 GPUs. With hierarchical broadcast:

``` {.sourceCode .c}
void multi_server_tlb_invalidate(void *va, size_t size) {
    // Step 1: Broadcast locally via NVSwitch
    nvswitch_broadcast_invalidate(va, size);
    
    // Step 2: Send RDMA message to remote servers
    for (int server = 1; server < 8; server++) {
        rdma_send_invalidate(server, va, size);
    }
    
    // Step 3: Wait for local acknowledgments (31 GPUs)
    wait_for_local_acks();  // ~3 µs
    
    // Step 4: Wait for remote acknowledgments (7 servers × 32 GPUs)
    wait_for_remote_acks();  // ~12 µs
    
    // Total: ~15 µs
}
```

The acknowledgment step cannot be eliminated---it ensures all GPUs have
invalidated before the caller proceeds to modify the page table entry or
reuse the physical memory.

### NCCL Integration: Gradient Synchronization and TLB Coherency

NVIDIA Collective Communications Library (NCCL) handles gradient
all-reduce during distributed training. NCCL must coordinate with memory
management because gradient buffers involve page table operations.

**Training Iteration with Multi-GPU:**

    1. Forward pass (all GPUs compute outputs)
    2. Backward pass (all GPUs compute gradients)
    3. NCCL all-reduce (combine gradients from all GPUs)
    4. Optimizer step (update parameters using combined gradients)

**Step 3 Detail (All-Reduce):**

NCCL implements all-reduce via ring algorithm:

    Ring topology: GPU 0 → GPU 1 → ... → GPU 255 → GPU 0

    Iteration 1: GPU 0 sends chunk 0 to GPU 1
                 GPU 1 sends chunk 1 to GPU 2
                 ...
    Iteration 2: GPU 1 forwards chunk 0 to GPU 2
                 GPU 2 forwards chunk 1 to GPU 3
                 ...
    After 256 iterations: All GPUs have all gradients combined

**Memory Consistency Challenge:**

During all-reduce, each GPU reads gradients from its local memory and
sends them to the next GPU. If gradient memory is modified (e.g.,
reallocated) during all-reduce, TLB coherency issues arise:

    Time T0: GPU 0 computes gradients at virtual address 0x7fff0000
             GPU 0's TLB: 0x7fff0000 → physical page 0x1234

    Time T1: NCCL starts all-reduce
             GPU 0 reads 0x7fff0000, sends to GPU 1

    Time T2: Meanwhile, CPU decides to migrate gradient buffer
             CPU updates page table: 0x7fff0000 → physical page 0x5678
             CPU sends TLB invalidation to all GPUs

    Time T3: GPU 0's TLB invalidation arrives
             GPU 0 invalidates 0x7fff0000 entry

    Time T4: GPU 0 receives chunk from GPU 255
             GPU 0 reads 0x7fff0000 to add incoming chunk
             TLB miss → page walk → finds page 0x5678
             GPU 0 reads from wrong page!

The race condition: all-reduce spans milliseconds, but page table
updates happen in microseconds. Without coordination, updates can occur
mid-all-reduce, corrupting data.

**NCCL\'s Solution: Memory Pinning During Operations**

``` {.sourceCode .c}
nccl_all_reduce_start(gradients, ...);
// Gradients are now "in-flight" - NCCL holds reference

// If application tries to free gradients:
cudaFree(gradients);
// cudaFree() sees NCCL reference, blocks until all-reduce completes

nccl_all_reduce_wait();  // Wait for completion
// Now cudaFree() proceeds, triggers TLB invalidation
```

This prevents page table modifications during NCCL operations. The
downside: it blocks allocation/deallocation, potentially stalling other
GPU streams.

**Alternative: Explicit Fencing with Events**

``` {.sourceCode .c}
// Start all-reduce on dedicated stream
nccl_all_reduce_async(gradients, stream_nccl);
cudaEventRecord(event_allreduce_done, stream_nccl);

// Optimizer runs on separate stream
cudaStreamWaitEvent(stream_optimizer, event_allreduce_done);
optimizer_step<<<..., stream_optimizer>>>(gradients);

// Freeing gradients waits for optimizer to complete
cudaFree(gradients);  // Implicitly waits for stream_optimizer
```

This allows parallelism (optimizer can start as soon as all-reduce
completes) while ensuring TLB invalidations don\'t occur during
all-reduce.

### Production Measurements: Real Systems at Scale

**Experiment 1: LLaMA 70B Training on 64 GPUs**

Configuration: - 8 servers × 8 NVIDIA A100 GPUs - NVSwitch within each
server - 8× 200 Gbps InfiniBand between servers

Workload: - 70B parameters = 140 GB in FP16 - Batch size 1024, gradient
accumulation every 8 steps - Every 8 steps: Free old gradients, allocate
new gradients - Gradient size: 140 GB

**Measured TLB Invalidation Latency:**

    Naive (serial):
    Free 140 GB gradient buffer:
    64 GPUs × 12 µs = 768 µs per munmap
    140 GB / 2 MB pages = 71,680 pages
    71,680 pages × 768 µs = 55 seconds!

    Obviously unusable - training would spend more time on TLB invalidation than computation.

    Optimized (NVSwitch + RDMA broadcast):
    Free 140 GB gradient buffer:
    Local broadcast: 2.5 µs
    Remote RDMA: 18 µs
    Total: 20.5 µs per munmap
    71,680 pages × 20.5 µs = 1.47 seconds

    Still significant, but 37× faster than naive approach.

    Further optimization (batch invalidations):
    Group contiguous pages, invalidate ranges instead of individual pages.
    71,680 pages → 280 ranges (512 pages per range)
    280 ranges × 20.5 µs = 5.7 ms

    Speedup: 55 seconds → 5.7 ms = 9,649× faster

The batch invalidation optimization is crucial. Instead of invalidating
each 2 MB page separately, the system invalidates contiguous ranges:

``` {.sourceCode .c}
// Naive: Invalidate each page
for (page = 0; page < 71680; page++) {
    tlb_invalidate(base + page * 2MB, 2MB);  // 71,680 calls
}

// Optimized: Invalidate ranges
for (range = 0; range < 280; range++) {
    tlb_invalidate(base + range * 512 * 2MB, 512 * 2MB);  // 280 calls
}
```

NVSwitch supports range invalidation natively, processing a single
message that invalidates 512 pages just as fast as one that invalidates
1 page.

**Experiment 2: Multi-GPU Inference Serving**

Configuration: - 32 NVIDIA A100 GPUs (single server) - Stable Diffusion
serving with dynamic batch sizing - Batch sizes vary 1-64 based on load

**Problem:** Dynamic batch sizing reallocates activation buffers per
batch. Each reallocation triggers TLB invalidation.

**Naive Approach:**

    Request rate: 100 req/sec
    Average batch size changes: 10 per second
    Invalidation per batch change: 2.7 ms (serial)
    Overhead: 10 × 2.7 ms = 27 ms/sec

    Throughput impact: 27/1000 = 2.7% loss

**With NVSwitch Broadcast:**

    Invalidation per batch change: 40 µs (broadcast)
    Overhead: 10 × 40 µs = 400 µs/sec

    Throughput impact: 0.4/1000 = 0.04% loss

Speedup: 2.7% → 0.04% = 67.5× better

The difference allowed increasing max batch size from 32 to 64 (doubling
throughput) without TLB overhead dominating.

### Protocol Design: Ensuring Correctness

The broadcast protocol must ensure safety: no GPU accesses a page after
invalidation until the page table is updated.

**Incorrect Protocol (Race Condition):**

    GPU 0: Send invalidation broadcast
    GPU 0: Update page table entry
    GPU 1-255: Receive invalidation (asynchronously)

    Race: GPU 0 updates PTE before GPU 17 invalidates its TLB
    GPU 17 still has old translation, accesses old physical page
    GPU 0 reallocates old physical page for different use
    GPU 17's access corrupts new data

**Correct Protocol (With Acknowledgment):**

    GPU 0: Send invalidation broadcast
    GPU 1-255: Receive invalidation
    GPU 1-255: Invalidate local TLB entries
    GPU 1-255: Send acknowledgment to GPU 0
    GPU 0: Wait for all 255 acknowledgments
    GPU 0: Update page table entry

    Now safe: All GPUs have invalidated before PTE changes

**Timeout Handling:**

What if GPU 17 crashes and never acknowledges?

``` {.sourceCode .c}
void wait_for_all_acks() {
    int timeout_ms = 1000;  // 1 second
    int acks_received = 0;
    
    while (acks_received < 255 && timeout_ms > 0) {
        acks_received += check_acks();
        usleep(100);
        timeout_ms--;
    }
    
    if (acks_received < 255) {
        // Some GPUs didn't respond
        log_error("TLB shootdown timeout: %d GPUs unresponsive", 255 - acks_received);
        
        // Failsafe: Mark those GPUs as failed, exclude from future operations
        mark_gpus_failed(unresponsive_gpus);
    }
}
```

In practice, timeouts are rare (GPUs don\'t crash mid-invalidation). But
handling them prevents system-wide deadlock when one GPU fails.

### When Multi-GPU TLB Synchronization Breaks Down

**Scenario: 10,000 GPU Cluster**

At extreme scales (OpenAI\'s GPT-4 training cluster reportedly used
25,000 GPUs), even optimized invalidation becomes problematic:

    Optimized broadcast to 10,000 GPUs:
    1. Broadcast within each 32-GPU server: 2.5 µs
    2. RDMA to 312 other servers: 20 µs
    3. Acknowledgments from 10,000 GPUs: 50 µs
    Total: 72.5 µs

    For a single page: Acceptable
    For 100,000 pages (200 GB / 2 MB): 7.25 seconds!

The solution at this scale: **avoid page table modifications entirely
during training**.

**Static Allocation Strategy:**

``` {.sourceCode .c}
// At training start: Allocate everything
cudaMalloc(&parameters, 140GB);  // Pinned
cudaMalloc(&optimizer_state, 280GB);  // Pinned
cudaMalloc(&gradients, 140GB);  // Pinned
cudaMalloc(&activations, 50GB);  // Pinned

// During training: Never free, never reallocate
// Reuse same buffers for all iterations

// At training end: Free everything once
cudaFree(parameters);
cudaFree(optimizer_state);
cudaFree(gradients);
cudaFree(activations);
```

This eliminates page table modifications during training, avoiding TLB
invalidation overhead entirely. The tradeoff: higher memory usage
(can\'t free and reallocate dynamically), less flexibility (buffer sizes
fixed at startup).

For the largest training runs, this tradeoff is worthwhile---spending 7
seconds on TLB invalidations would waste hours over a week-long training
run.

### Summary: Multi-GPU TLB Synchronization Principles

**Principle 1: Hardware Broadcast When Available**

NVSwitch reduces invalidation latency by 10-50× versus serial
approaches. Always use hardware broadcast on supported platforms.

**Principle 2: Hierarchical Invalidation for Multi-Server**

Two-level protocol (intra-server NVSwitch + inter-server RDMA) scales to
hundreds of GPUs with \<50 µs latency.

**Principle 3: Batch Invalidations**

Invalidate contiguous ranges, not individual pages. A 512-page range
invalidation is as fast as a 1-page invalidation with NVSwitch.

**Principle 4: Static Allocation at Extreme Scale**

Beyond 1,000 GPUs, avoid page table modifications during training.
Allocate everything upfront, deallocate at completion.

**Principle 5: Coordinate with Communication Libraries**

NCCL and other collective communication libraries must fence memory
operations to prevent races between all-reduce and TLB invalidation.

Next, we\'ll examine a seemingly simple question with profound
performance implications: for a 70 billion parameter model, should you
use 4 KB pages, 2 MB pages, or 1 GB pages? The answer determines whether
your TLB miss rate is 99.998% or 0%. \## 11.5 Page Size Selection for
Large Models: The TLB Coverage Problem

A seemingly simple configuration choice---whether to use 4 KB, 2 MB, or
1 GB pages---determines whether a GPU achieves 100% of theoretical
performance or struggles at 20%. For large language models with hundreds
of gigabytes of parameters, the wrong page size creates TLB miss rates
approaching 100%, where almost every memory access requires a page table
walk. The right page size enables complete TLB coverage, eliminating
translation overhead entirely.

This section provides quantitative analysis of page size selection,
calculating TLB coverage for real models, understanding why huge pages
aren\'t always the answer, and developing a decision framework for
different tensor types.

### The TLB Coverage Calculation

TLB coverage---the total amount of memory addressable with TLB
entries---depends on both TLB size and page size:

    TLB Coverage = TLB Entries × Page Size

For NVIDIA H100:

    L1 DTLB per SM: 64 entries
    L2 TLB (shared): 2,048 entries

We focus on L2 TLB coverage because it determines whether misses
escalate to expensive page table walks:

    4 KB pages:  2,048 × 4 KB = 8 MB
    2 MB pages:  2,048 × 2 MB = 4 GB
    1 GB pages:  2,048 × 1 GB = 2 TB

Now consider a LLaMA 70B model in FP16 precision:

    Parameters: 70 billion × 2 bytes = 140 GB

**TLB Coverage Ratio (4 KB pages):**

    Coverage: 8 MB
    Model: 140 GB
    Ratio: 8 MB / 140 GB = 0.0057%

    Pages needed: 140 GB / 4 KB = 36,700,160 pages
    TLB entries: 2,048
    Coverage: 2,048 / 36,700,160 = 0.0056%

    TLB miss rate: 99.9944%

This means 99.99% of parameter accesses miss the TLB, requiring a page
table walk. Each walk: - 4 levels × 100 ns per level = 400 ns - Memory
access after walk: 100 ns - Total: 500 ns (vs 100 ns with TLB hit)

**Performance Impact:**

    Without TLB misses (theoretical): 100% throughput
    With 99.99% miss rate:
      - 99.99% of accesses: 500 ns
      - 0.01% of accesses: 100 ns
      - Average: 500 ns
      
    Throughput: 100 ns / 500 ns = 20% of theoretical

    Training that should take 1 week takes 5 weeks.

**TLB Coverage Ratio (2 MB pages):**

    Coverage: 4 GB
    Model: 140 GB
    Ratio: 4 GB / 140 GB = 2.86%

    Pages needed: 140 GB / 2 MB = 71,680 pages
    TLB entries: 2,048
    Coverage: 2,048 / 71,680 = 2.86%

    TLB miss rate: 97.14%

Still terrible---97% of accesses miss. While 512× fewer pages than 4 KB,
it\'s insufficient for 140 GB models.

**TLB Coverage Ratio (1 GB pages):**

    Coverage: 2 TB
    Model: 140 GB
    Ratio: 2 TB / 140 GB = 14.63 (1463%)

    Pages needed: 140 GB / 1 GB = 140 pages
    TLB entries: 2,048
    Coverage: 2,048 / 140 = 14.63 (1463%)

    TLB miss rate: 0% (entire model fits in TLB)

The 140-page model fits in a 2,048-entry TLB with 1,900 entries to
spare. Every parameter access hits the TLB---zero translation overhead.

### Why 1 GB Pages Aren\'t Always Optimal

If 1 GB pages eliminate TLB misses, why doesn\'t everyone use them? Four
reasons:

**1. Physical Memory Fragmentation**

Allocating a 1 GB page requires 1 GB of physically contiguous
memory---262,144 consecutive 4 KB pages. On a freshly booted system,
this is feasible. After the system runs for hours or days, physical
memory fragments:

    After System Uptime:
    [App A: 100 MB][Free: 50 MB][App B: 200 MB][Free: 300 MB][App C: 150 MB][Free: 800 MB]

    Largest contiguous region: 800 MB
    Can't allocate 1 GB page!

Linux tracks fragmentation via `/proc/buddyinfo`:

``` {.sourceCode .bash}
$ cat /proc/buddyinfo
Node 0, zone DMA      41    31    15     5     1     1     0     0     0     0     0
Node 0, zone Normal  105   82    64    32    16     8     4     2     1     0     0
                                                                        ^     ^
                                                                      4MB  8MB
```

The rightmost columns show high-order contiguous regions. Zero in the 1
GB column means no 1 GB regions available.

**Solution: Memory Compaction**

Linux\'s compaction daemon can defragment memory by migrating pages:

``` {.sourceCode .bash}
echo 1 > /proc/sys/vm/compact_memory  # Force compaction
```

But compaction is expensive:

    Compact 128 GB of fragmented memory: 5-30 seconds
    During compaction: System partially stalled

For training jobs, compact once at startup (acceptable), not during
training (unacceptable).

**2. Allocation Latency**

Allocating 1 GB pages is 100-1000× slower than 4 KB pages:

    Measurement (cudaMalloc with huge pages):

    4 KB page allocation:
    malloc(1 GB) = 256,000 × 4 KB pages
    Latency: ~1-2 ms (bulk allocation)

    2 MB page allocation:
    malloc(1 GB) = 512 × 2 MB pages
    Latency: ~10-20 ms (need contiguous regions)

    1 GB page allocation:
    malloc(1 GB) = 1 × 1 GB page
    Latency: ~50-200 ms (need huge contiguous region + TLB setup)

The 50-200 ms latency comes from: 1. Search for contiguous 1 GB region
(10-50 ms) 2. Clear/zero the region (30-100 ms for 1 GB at \~10 GB/s
write bandwidth) 3. Update page tables (5-10 ms) 4. Flush TLB (1-5 ms)

For model parameters allocated once at training start, this is
acceptable. For temporary buffers allocated/freed during training, it\'s
prohibitive.

**3. Memory Overhead for Partial Usage**

A 1 GB page partially used still consumes 1 GB:

    Example: Allocate 100 MB tensor

    With 4 KB pages:
    100 MB / 4 KB = 25,600 pages
    Memory used: 100 MB (exactly)

    With 1 GB pages:
    Need 1 page (can't allocate fraction)
    Memory used: 1 GB
    Waste: 900 MB (90% overhead!)

For large tensors that use most of a 1 GB page, overhead is negligible:

    Allocate 900 MB tensor with 1 GB pages:
    Memory used: 1 GB
    Waste: 100 MB (11% overhead)

But for many small tensors (batch norm parameters, biases, small
embedding tables), 1 GB pages waste memory.

**4. Limited Kernel Support**

Not all systems support 1 GB pages:

    x86-64: Requires PDPE1GB CPU feature (common since 2010)
    ARM64: Requires specific page table setup (some systems disabled)
    Linux: Requires CONFIG_HUGETLB_PAGE_SIZE_1GB=y
    CUDA: Requires driver 510+ with opt-in environment variable

To enable 1 GB pages in CUDA:

``` {.sourceCode .bash}
export CUDA_ENABLE_1GB_PAGES=1
```

Without this, CUDA defaults to 2 MB pages even if you request larger.

### Decision Framework: Page Size by Tensor Type

Different tensor types have different access patterns and lifetimes,
suggesting different page size choices:

**Model Parameters (Use 1 GB pages):**

    Characteristics:
    - Large: 10-500 GB for modern models
    - Long-lived: Allocated at training start, freed at end
    - Hot path: Accessed every forward/backward pass
    - Sequential access: Read entire parameter matrix contiguously

    Page size choice: 1 GB
    Rationale: Perfect TLB coverage, allocation latency amortized over training duration

Example (LLaMA 70B):

``` {.sourceCode .python}
# Reserve 1GB pages at system boot
echo 200 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages

# Allocate parameters with 1GB pages
os.environ['CUDA_ENABLE_1GB_PAGES'] = '1'
parameters = torch.cuda.FloatTensor(70_000_000_000).fill_(0)

# Result:
# Size: 140 GB
# Pages: 140 × 1 GB
# TLB coverage: 100% (140 pages fit in 2048-entry TLB)
# Allocation time: 28 seconds (140 × 200 ms, acceptable for startup)
```

**Optimizer State (Use 1 GB or 2 MB pages):**

    Characteristics:
    - Very large: 2-3× parameter size (Adam: 8 bytes state per 2-byte parameter)
    - Long-lived: Allocated at training start
    - Accessed once per iteration: Less hot than parameters
    - Sequential access: Updated in order

    Page size choice: 1 GB if memory available, else 2 MB
    Rationale: TLB coverage important but less critical than parameters

For LLaMA 70B with Adam:

``` {.sourceCode .python}
# Optimizer state: 70B params × 8 bytes = 560 GB
# With 1 GB pages: 560 pages (fits in TLB)
# With 2 MB pages: 286,720 pages (97% TLB miss rate)

# If 560 GB + 140 GB params exceeds GPU memory, use 2 MB pages for optimizer
# Parameters stay 1 GB pages (more critical for performance)
```

**Activations (Use 2 MB pages):**

    Characteristics:
    - Medium size: 1-50 GB depending on batch size
    - Short-lived: Allocated per batch, freed after backward pass
    - Accessed sequentially during forward/backward
    - Recomputation in gradient checkpointing

    Page size choice: 2 MB
    Rationale: Balance allocation latency and TLB coverage

For batch size 1024 with LLaMA 70B:

``` {.sourceCode .python}
# Activation size: ~50 GB per batch
# With 4 KB pages: 50 GB / 4 KB = 13.1M pages (0.015% TLB coverage)
# With 2 MB pages: 50 GB / 2 MB = 25,600 pages (8% TLB coverage)
# With 1 GB pages: 50 GB / 1 GB = 50 pages (100% TLB coverage)

# Choose 2 MB: Allocation is fast (~100ms), TLB misses reduced 512×
# 1 GB pages too slow to allocate/free every batch
```

**Gradients (Use 2 MB pages):**

    Characteristics:
    - Same size as parameters: 10-500 GB
    - Medium-lived: Allocated per gradient accumulation window
    - Hot path: Computed in backward pass, consumed in optimizer step

    Page size choice: 2 MB
    Rationale: Reallocation overhead with 1 GB pages outweighs TLB benefit

With gradient accumulation (accumulate 8 batches before optimizer step):

``` {.sourceCode .python}
# Allocate gradient buffer for 8 batches
gradients = torch.cuda.FloatTensor(70_000_000_000).fill_(0)

# Accumulate 8 batches (140 GB buffer reused)
for i in range(8):
    loss.backward()  # Add to gradients

# Optimizer step (consume gradients)
optimizer.step()

# Free gradients
del gradients  # Triggers munmap, TLB invalidation

# Next accumulation window: Reallocate
# With 1 GB pages: 28-second allocation
# With 2 MB pages: 2-second allocation
# Difference: 26 seconds per accumulation window
# Over 1000 windows: 26,000 seconds = 7.2 hours wasted!
```

**Small Dynamic Tensors (Use 4 KB pages):**

    Characteristics:
    - Small: <1 MB each
    - Very short-lived: Allocated during kernel, freed immediately after
    - Many allocations: Thousands per iteration

    Page size choice: 4 KB
    Rationale: Huge page overhead exceeds TLB benefit

Examples: - Intermediate results in kernel (softmax denominator,
attention scores) - Temporary buffers for reductions - Index tensors for
gather/scatter

``` {.sourceCode .python}
# Bad: Allocate 100 KB with 2 MB pages
temp = torch.cuda.FloatTensor(25_000)  # 100 KB
# Uses 2 MB page (1.9 MB wasted)

# Good: Use 4 KB pages for small tensors
temp = torch.cuda.FloatTensor(25_000)  # 100 KB
# Uses 25 × 4 KB pages (no waste)
```

### Measured Performance: Page Size Impact on Real Models

**Experiment: GPT-3 (175B parameters, 350 GB)**

Configuration: - 8× NVIDIA A100 (80 GB each) - Model parallelism: 8-way
split (43.75 GB per GPU) - Batch size 2048

**Configuration A: All 4 KB pages**

    Parameters: 43.75 GB / 4 KB = 11.5M pages per GPU
    TLB coverage: 2048 entries × 4 KB = 8 MB (0.018%)
    TLB miss rate: 99.982%

    Measured throughput: 18% of theoretical
    Training time: 55 days

**Configuration B: 2 MB pages for everything**

    Parameters: 43.75 GB / 2 MB = 22,400 pages per GPU
    TLB coverage: 2048 entries × 2 MB = 4 GB (9.1%)
    TLB miss rate: 90.9%

    Measured throughput: 43% of theoretical
    Training time: 23 days
    Speedup: 2.4× vs 4 KB pages

**Configuration C: 1 GB parameters, 2 MB activations/gradients**

    Parameters: 43.75 GB / 1 GB = 44 pages per GPU
    TLB coverage: 100% for parameters
    Activations: ~20 GB / 2 MB = 10,240 pages (mixed hit rate)

    Measured throughput: 89% of theoretical
    Training time: 11 days
    Speedup: 5× vs 4 KB pages, 2.1× vs 2 MB pages

The 89% throughput (not 100%) comes from TLB misses on activations and
gradients. But parameters---the most frequently accessed data---have
zero TLB misses.

**Configuration D: All 1 GB pages (failed attempt)**

    Allocation time at startup: 8 minutes (fragmented memory, compaction required)
    Every gradient reallocation (every 8 batches): 30 seconds
    Result: Training stalls, unusable

This demonstrates that 1 GB pages for everything is impractical due to
allocation overhead.

### Linux Huge Page Configuration

To use huge pages, the kernel must reserve them at boot:

``` {.sourceCode .bash}
# Reserve 1 GB pages (200 × 1 GB = 200 GB)
echo 200 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages

# Reserve 2 MB pages (10,000 × 2 MB = 20 GB)
echo 10000 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

# Verify reservation
cat /proc/meminfo | grep Huge
HugePages_Total:     200
HugePages_Free:      200
HugePages_Rsvd:        0
Hugepagesize:    1048576 kB
```

CUDA applications automatically use reserved huge pages if available and
enabled:

``` {.sourceCode .bash}
export CUDA_ENABLE_1GB_PAGES=1  # Enable 1 GB pages
export CUDA_ENABLE_2MB_PAGES=1  # Enable 2 MB pages (default on)
```

Without reservation, allocation fails:

``` {.sourceCode .python}
import torch
params = torch.cuda.FloatTensor(70_000_000_000)  # 140 GB
# Error: Cannot allocate 1GB pages, no pages available
# Falls back to 2 MB pages
```

### Summary: Page Size Decision Tree

::: {style="margin:1.5em 0;padding:16px;background:#F3E5F5;border-left:4px solid #7B1FA2;border-radius:4px;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.8;"}
**Page Size Decision Tree for AI/ML Tensors**\
\
**Is the tensor large (\>10 GB) and long-lived (\>1 hour)?**\
  ├─ **Yes:** Will it be reallocated frequently (\>once/minute)?\
      ├─ **No →** [1 GB pages]{style="color:#1565C0;font-weight:bold;"}
--- model parameters, long-lived optimizer state\
      └─ **Yes →** [2 MB pages]{style="color:#00796B;font-weight:bold;"}
--- gradient buffers with frequent accumulation cycles\
  └─ **No:** Is the tensor accessed in tight loops (\<10 ms lifetime)?\
      ├─ **Yes →** [4 KB pages]{style="color:#E65100;font-weight:bold;"}
--- activations, temporary buffers (avoid fragmentation)\
      └─ **No →** [2 MB pages]{style="color:#00796B;font-weight:bold;"}
--- medium tensors, batch data, KV caches
:::

**Rule of Thumb:** - **1 GB pages:** Model parameters (allocated once,
used forever) - **2 MB pages:** Everything else \>100 MB (activations,
gradients, optimizer state) - **4 KB pages:** Everything \<100 MB (small
buffers, index tensors)

**Critical Insight:** TLB coverage for parameters matters most because
parameters are accessed every forward and backward pass. Activations are
computed once per batch, so TLB misses on activations have 10-100× less
impact than misses on parameters.

Next, we\'ll examine AMD\'s MI300X, where 8 GPU chiplets must coordinate
their TLBs while sharing a 192 GB address space---a challenge that makes
NVIDIA\'s multi-GPU coordination look simple by comparison. \## 11.6 AMD
MI300X: Chiplet Coordination and 192 GB Address Spaces

AMD\'s MI300X represents a fundamentally different approach to scaling
GPU memory: instead of using discrete HBM stacks connected to a
monolithic GPU die, the MI300X integrates 8 GPU compute chiplets and 4
I/O chiplets in a single package with 13 HBM3 stacks providing 192 GB of
total capacity. This architecture enables fitting models that require
2-3 discrete NVIDIA H100 GPUs (80 GB each) on a single device,
eliminating model parallelism overhead. But it creates a new challenge:
how do 8 separate GPU chiplets, each with its own MMU and TLB hierarchy,
coordinate access to a shared 192 GB address space?

This section explores MI300X\'s TLB architecture: whether chiplets share
page tables or maintain independent ones, how TLB invalidations
propagate across the Infinity Fabric interconnect, and why the 192 GB
address space requires huge pages to achieve adequate TLB coverage.

### The Chiplet Architecture Challenge

The MI300X\'s 3D stacked architecture looks like this:

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="480" viewBox="0 0 900 480" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh" x="-5%" y="-5%" width="115%" height="115%">
      <fedropshadow dx="2" dy="3" stddeviation="4" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
    <marker id="arr" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" style="fill:#E65100" />
    </marker>
  </defs>

  <text x="450" y="28" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">AMD MI300X Chiplet Package Cross-Section</text>

  <!-- Package outline -->
  <rect x="20" y="45" width="560" height="370" rx="8" filter="url(#sh)" style="fill:#ECEFF1; stroke:#607D8B; stroke-width:2.5" />
  <text x="300" y="68" font-family="Arial,Helvetica,sans-serif" style="fill:#607D8B; font-size:15; font-weight:bold; text-anchor:middle">AMD MI300X Package (2.5D Interposer + HBM3)</text>

  <!-- Row 1 compute chiplets -->
  <rect x="40" y="80" width="160" height="90" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="120" y="115" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Compute</text>
  <text x="120" y="133" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">Chiplet 0</text>
  <text x="120" y="150" font-family="Arial,Helvetica,sans-serif" style="fill:#90CAF9; font-size:12; text-anchor:middle">CDNA3 GPU</text>

  <rect x="210" y="80" width="160" height="90" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="290" y="115" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Compute</text>
  <text x="290" y="133" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">Chiplet 1</text>
  <text x="290" y="150" font-family="Arial,Helvetica,sans-serif" style="fill:#90CAF9; font-size:12; text-anchor:middle">CDNA3 GPU</text>

  <rect x="380" y="80" width="160" height="90" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="460" y="115" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Compute</text>
  <text x="460" y="133" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">Chiplet 2</text>
  <text x="460" y="150" font-family="Arial,Helvetica,sans-serif" style="fill:#90CAF9; font-size:12; text-anchor:middle">CDNA3 GPU</text>

  <!-- Row 2 -->
  <rect x="40" y="185" width="160" height="90" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="120" y="225" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Compute</text>
  <text x="120" y="243" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">Chiplet 3</text>

  <rect x="210" y="185" width="160" height="90" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="290" y="225" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Compute</text>
  <text x="290" y="243" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">Chiplet 4</text>

  <rect x="380" y="185" width="160" height="90" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="460" y="225" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Compute</text>
  <text x="460" y="243" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">Chiplet 5</text>

  <!-- HBM3 Stacks -->
  <rect x="40" y="295" width="500" height="100" rx="5" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
  <text x="290" y="325" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">HBM3 Memory Stacks (×8 stacks, 192 GB total)</text>
  <text x="290" y="347" font-family="Arial,Helvetica,sans-serif" style="fill:#B2DFDB; font-size:13; text-anchor:middle">5.2 TB/s aggregate bandwidth • 2.5D interposer connects all chiplets</text>
  <text x="290" y="367" font-family="Arial,Helvetica,sans-serif" style="fill:#B2DFDB; font-size:13; text-anchor:middle">Unified virtual address space spans all 6 compute chiplets via Infinity Fabric</text>

  <!-- Infinity Fabric arrows between chiplets -->
  <line x1="200" y1="125" x2="210" y2="125" marker-end="url(#arr)" style="stroke:#E65100; stroke-width:2"></line>
  <line x1="370" y1="125" x2="380" y2="125" marker-end="url(#arr)" style="stroke:#E65100; stroke-width:2"></line>
  <line x1="200" y1="230" x2="210" y2="230" marker-end="url(#arr)" style="stroke:#E65100; stroke-width:2"></line>
  <line x1="370" y1="230" x2="380" y2="230" marker-end="url(#arr)" style="stroke:#E65100; stroke-width:2"></line>
  <!-- Vertical connections -->
  <line x1="120" y1="170" x2="120" y2="185" marker-end="url(#arr)" style="stroke:#E65100; stroke-width:2"></line>
  <line x1="290" y1="170" x2="290" y2="185" marker-end="url(#arr)" style="stroke:#E65100; stroke-width:2"></line>
  <line x1="460" y1="170" x2="460" y2="185" marker-end="url(#arr)" style="stroke:#E65100; stroke-width:2"></line>

  <!-- Infinity Fabric label -->
  <text x="548" y="155" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Infinity</text>
  <text x="548" y="170" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Fabric</text>
  <text x="548" y="188" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">cross-die</text>
  <text x="548" y="204" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">interconnect</text>

  <!-- Right panel: TLB challenge -->
  <rect x="600" y="45" width="285" height="370" rx="6" filter="url(#sh)" style="fill:#FFF3E0; stroke:#E65100; stroke-width:1.5" />
  <text x="742" y="70" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">Chiplet TLB Challenge</text>

  <text x="610" y="95" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; font-weight:bold">Per-Chiplet TLB Hierarchy:</text>
  <text x="615" y="115" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">L1 DTLB: ~64 entries</text>
  <text x="615" y="133" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">L2 TLB: ~2,048 entries</text>
  <text x="615" y="151" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">L3 TLB: ~16,384 shared</text>
  <text x="615" y="172" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">(spans all chiplets)</text>

  <text x="610" y="200" font-family="Arial,Helvetica,sans-serif" style="fill:#C62828; font-size:13; font-weight:bold">Cross-chiplet invalidation:</text>
  <text x="615" y="220" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">TLBI must propagate</text>
  <text x="615" y="238" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">across Infinity Fabric</text>
  <text x="615" y="256" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">to all 6 chiplets.</text>

  <text x="610" y="285" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:13; font-weight:bold">Key stats (MI300X):</text>
  <text x="615" y="305" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">304 GB total HBM3</text>
  <text x="615" y="323" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">5.3 TB/s bandwidth</text>
  <text x="615" y="341" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">14,080 shader procs</text>
  <text x="615" y="359" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">Single unified VA space</text>
  <text x="615" y="377" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">via ROCm HMM</text>

  <!-- Foot note -->
  <text x="450" y="432" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">Chiplets communicate via Infinity Fabric on a silicon interposer; HBM3 stacks are directly beneath compute chiplets for minimal access latency</text>
</svg>
</div>
<figcaption><strong>Figure 11.chiplet:</strong> AMD MI300X chiplet
package cross-section: 6–8 compute chiplets (CDNA3 GPU dies)
interconnected via Infinity Fabric on a 2.5D silicon interposer, with
HBM3 stacks directly beneath each chiplet. A single unified virtual
address space spans all chiplets via ROCm HMM.</figcaption>
</figure>

Each compute chiplet contains: - GPU cores (compute units, caches) -
Local L1 TLB (per compute unit) - Shared L2 TLB (per chiplet) - Infinity
Fabric connection to other chiplets

The I/O chiplets provide: - HBM3 memory controllers (3-4 stacks each,
16-24 GB per I/O chiplet) - Infinity Fabric switches routing between
chiplets - PCIe interfaces for host communication

The fundamental question: when Compute Chiplet 0 accesses virtual
address 0x7fff1000, how does it translate to physical addresses across
13 HBM stacks potentially managed by different I/O chiplets?

### Two Architectural Approaches

**Approach 1: Independent Page Tables per Chiplet**

Each chiplet maintains its own page table base register and independent
page tables:

    Chiplet 0: TTBR = 0x1000_0000 → Page tables for Chiplet 0
    Chiplet 1: TTBR = 0x2000_0000 → Page tables for Chiplet 1
    ...
    Chiplet 7: TTBR = 0x8000_0000 → Page tables for Chiplet 7

Advantage: Each chiplet can map the same virtual address to different
physical addresses (useful for NUMA-like setups where each chiplet has
affinity to certain memory regions).

Disadvantage: Software must keep 8 page tables synchronized. If Chiplet
0 updates its page table for VA 0x7fff1000, all other chiplets must
update their page tables identically, or they\'ll see inconsistent
mappings.

**Approach 2: Shared Page Table Base**

All chiplets share a single page table base register:

    All Chiplets: TTBR = 0x1000_0000 → Shared page tables

Advantage: Single source of truth for mappings. Update the page table
once, all chiplets see the change.

Disadvantage: Page table walks from different chiplets contend for the
same page table entries, potentially creating bottlenecks.

**AMD\'s Actual Implementation: Shared Page Tables**

AMD chose shared page tables for MI300X. All 8 compute chiplets use the
same page table base, ensuring consistent virtual-to-physical mappings
across the package. This simplifies software (no need to synchronize 8
page tables) and aligns with the unified programming model where
developers view the MI300X as a single 192 GB GPU, not 8 separate 24 GB
GPUs.

### TLB Hierarchy in MI300X

While page tables are shared, TLBs remain local to each chiplet:

``` {style="background:#E8F5E9;border:1px solid #4CAF50;border-radius:4px;padding:12px;font-family:'Courier New',monospace;font-size:13px;line-height:1.6;overflow-x:auto;"}
Per-Compute Chiplet TLB Hierarchy (AMD MI300X):
  L1 DTLB (per compute unit):  ~64 entries   → 1–2 cycle access
    └─ L2 TLB (per chiplet):   ~2,048 entries → 8–12 cycle access
         └─ L3 TLB (global):   ~16,384 entries (shared across chiplets)
              └─ HW Page Walk: DRAM resident page tables (Infinity Fabric, 50–200 ns)
```

The L3 TLB is a critical innovation. Shared across all chiplets, it
reduces redundant translation lookups. If Chiplet 0 translates VA
0x7fff1000 and caches the result in L3 TLB, Chiplet 1 can hit L3 TLB
instead of walking page tables again.

**TLB Lookup Flow:**

    Compute Unit on Chiplet 0 accesses VA 0x7fff1000:

    Step 1: Check local L1 DTLB
      - 64 entries, fully associative
      - Hit: Return PA immediately (1-2 cycles)
      - Miss: Proceed to L2

    Step 2: Check L2 TLB (local to Chiplet 0)
      - 2,048 entries, 8-way set-associative
      - Hit: Update L1, return PA (10-20 cycles)
      - Miss: Proceed to L3

    Step 3: Check L3 TLB (shared across all chiplets)
      - 16,384 entries, 16-way set-associative
      - Hit: Update L2 and L1, return PA (40-60 cycles)
      - Miss: Page table walk required

    Step 4: Page Table Walk
      - 4 levels (similar to x86-64)
      - Each level: Read PTE from HBM (100 ns latency)
      - Total: 4 × 100 ns = 400 ns = ~400 cycles at 1 GHz
      - Update L3, L2, and L1 TLBs

The L3 TLB effectively acts as a cache for page table walks, reducing
average translation latency significantly when multiple chiplets access
overlapping virtual address ranges (common during data-parallel
training).

### Infinity Fabric TLB Coherency Protocol

When one chiplet updates a page table entry, all other chiplets\' TLBs
must invalidate cached translations. MI300X uses Infinity
Fabric---AMD\'s on-package interconnect providing 256 GB/s bandwidth per
chiplet---to propagate invalidations.

**TLB Invalidation Steps:**

    1. Software (driver) updates PTE in shared page tables
    2. Software sends invalidation request to Chiplet 0
    3. Chiplet 0 broadcasts invalidation via Infinity Fabric
    4. All 8 chiplets receive broadcast simultaneously
    5. Each chiplet invalidates matching TLB entries (L1, L2, L3)
    6. Each chiplet sends acknowledgment back to Chiplet 0
    7. Chiplet 0 waits for all 7 acknowledgments
    8. Operation complete

**Latency Breakdown:**

    Step 3: Broadcast via Infinity Fabric: ~50 ns
    Step 5: Local TLB invalidation per chiplet: ~100 ns
    Step 6: Acknowledgment return: ~50 ns
    Total: ~200 ns

    For comparison, multi-GPU invalidation (Section 11.4): ~15-50 µs
    MI300X is 75-250× faster because:
    - On-package interconnect (no PCIe latency)
    - Hardware-accelerated broadcast
    - Shorter physical distances

**Infinity Fabric Bandwidth Impact:**

TLB invalidation messages are small (64 bytes: VA, size, invalidation
type), so bandwidth consumption is minimal:

    1,000 invalidations/sec × 64 bytes = 64 KB/sec
    Infinity Fabric bandwidth: 256 GB/sec
    Utilization: 64 KB / 256 GB = 0.000025%

Even at 1 million invalidations/second (pathological case), bandwidth
usage is 64 MB/s = 0.025% of capacity.

### TLB Coverage for 192 GB Address Space

The MI300X\'s 192 GB capacity creates severe TLB pressure with small
pages:

**4 KB Pages:**

    Address space: 192 GB
    Pages: 192 GB / 4 KB = 50,331,648 pages

    L3 TLB: 16,384 entries
    Coverage: 16,384 × 4 KB = 64 MB
    Coverage ratio: 64 MB / 192 GB = 0.033%

    TLB miss rate: 99.967%

**2 MB Pages:**

    Pages: 192 GB / 2 MB = 98,304 pages

    L3 TLB: 16,384 entries
    Coverage: 16,384 × 2 MB = 32 GB
    Coverage ratio: 32 GB / 192 GB = 16.7%

    TLB miss rate: 83.3%

Still very high miss rate---most accesses require page walks.

**1 GB Pages:**

    Pages: 192 GB / 1 GB = 192 pages

    L3 TLB: 16,384 entries
    Coverage: 16,384 × 1 GB = 16 TB
    Coverage ratio: 16 TB / 192 GB = 8,533%

    TLB miss rate: 0% (entire address space fits in TLB)

The entire 192 GB address space requires only 192 page table entries
with 1 GB pages. The 16,384-entry L3 TLB can cache the complete working
set with room for 16,192 additional entries.

**Why This Matters for MI300X:**

The MI300X\'s primary selling point is fitting large models without
model parallelism:

    LLaMA 70B (FP16):
    Parameters: 140 GB
    Optimizer state (Adam): 280 GB
    Total: 420 GB

    With model parallelism:
    - NVIDIA H100 (80 GB): Need 6 GPUs
    - Communication overhead: 15-25% per all-reduce
    - Programming complexity: High

    With MI300X:
    - 192 GB per device: Need 3 GPUs (parameters) + 3 GPUs (optimizer)
    - Still needs model parallelism, but 2× fewer devices than H100
    - Or: Parameters + gradients on one MI300X (140 GB + 140 GB = 280 GB)
      Optimizer state on another MI300X (280 GB)
      Communication: Once per iteration (not per layer)

But achieving good performance requires huge pages. With 4 KB pages,
99.967% TLB miss rate would reduce throughput to \~20% of
theoretical---defeating the purpose of the large capacity.

### Practical Configuration: Fitting LLaMA 70B on MI300X

**Configuration 1: Single MI300X (Parameters + Gradients)**

``` {.sourceCode .python}
# Reserve 1 GB pages
echo 300 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages

# Allocate parameters (140 GB)
params = torch.cuda.FloatTensor(70_000_000_000).fill_(0)  
# Uses 140 × 1 GB pages, full TLB coverage

# Allocate gradients (140 GB)
grads = torch.cuda.FloatTensor(70_000_000_000).fill_(0)
# Uses 140 × 1 GB pages, full TLB coverage

# Total: 280 GB on one MI300X (192 GB limit!)
# Does not fit. Need to use 2 MI300X or exclude optimizer state.
```

This doesn\'t work---280 GB exceeds 192 GB capacity.

**Configuration 2: Two MI300X (Parameters on one, Optimizer on
another)**

``` {.sourceCode .python}
# MI300X device 0: Parameters
torch.cuda.set_device(0)
params = torch.cuda.FloatTensor(70_000_000_000).fill_(0)  # 140 GB

# MI300X device 1: Optimizer state
torch.cuda.set_device(1)
opt_m = torch.cuda.FloatTensor(70_000_000_000).fill_(0)  # 140 GB
opt_v = torch.cuda.FloatTensor(70_000_000_000).fill_(0)  # 140 GB

# Gradients computed on Device 0, transferred to Device 1 for optimizer step
```

This works and uses 1 GB pages throughout. Gradients are temporary (not
stored), computed on-the-fly during backward pass.

**Performance:**

    Forward pass: Read params from Device 0 (TLB hits: 100%)
    Backward pass: Read params, write grads to Device 0 (TLB hits: 100%)
    Transfer grads: Device 0 → Device 1 via Infinity Fabric (5 GB/s effective for 140 GB = 28 seconds)
    Optimizer: Read grads + opt state on Device 1, write params (TLB hits: 100%)
    Transfer params: Device 1 → Device 0 (28 seconds)

    Total iteration: ~60 seconds (56 seconds communication, 4 seconds compute)

The communication overhead (56/60 = 93%) makes this impractical. Better
solution: use 3-way model parallelism, avoiding cross-device optimizer
communication.

### Comparison: MI300X vs H100 for Large Models

**LLaMA 70B Training (FP16):**

| Configuration | Devices | Model Parallel | TLB Coverage | Throughput |
| --- | --- | --- | --- | --- |
| H100 (4KB pages) | 6 GPUs | 6-way split | 0.02% | 18% |
| H100 (1GB pages) | 6 GPUs | 6-way split | 100% | 87% |
| MI300X (4KB pages) | 3 GPUs | 3-way split | 0.03% | 19% |
| MI300X (1GB pages) | 3 GPUs | 3-way split | 100% | 91% |


MI300X\'s advantage: - Fewer devices (3 vs 6) → Less communication
overhead - Larger per-device capacity → Simpler partitioning - Slightly
better throughput (91% vs 87%) due to on-package interconnect

But the advantage disappears with small pages---both achieve \~20%
throughput with 4 KB pages due to TLB thrashing.

### Summary: MI300X TLB Architecture Insights

**Shared Page Tables:** All 8 chiplets share a single page table base,
ensuring consistent mappings across the package.

**Three-Level TLB Hierarchy:** L1 (64 entries) → L2 (2,048 entries) → L3
(16,384 entries shared across chiplets).

**Infinity Fabric Coherency:** TLB invalidations broadcast in 200 ns (vs
15-50 µs for discrete multi-GPU).

**Huge Pages Mandatory:** 192 GB address space requires 1 GB pages for
adequate TLB coverage (0% miss rate vs 99.967% with 4 KB pages).

**Practical Impact:** MI300X\'s large capacity is only useful with
proper page size configuration. Without huge pages, TLB misses negate
the capacity advantage.

Next, we\'ll examine Intel Habana Gaudi 2, where 24 integrated RDMA
network interfaces create a unique challenge: how do networking engines
and compute cores share the same MMU without creating coherency
nightmares? \## 11.7 Intel Habana Gaudi 2: RDMA Engines and MMU
Integration

Intel\'s Habana Gaudi 2 takes a radically different approach to AI
accelerator networking: instead of connecting GPUs to external network
cards via PCIe (adding latency and limiting bandwidth), Gaudi integrates
24× 100 Gbps RDMA network interfaces directly on the AI accelerator die.
This provides 2.4 Tbps (300 GB/s) of aggregate network bandwidth for
gradient exchange during distributed training---4× faster than NVIDIA\'s
NVLink for equivalent configurations.

But tight integration creates a new challenge: when RDMA engines and
compute cores sit on the same die, do they share the MMU? If yes, how do
you prevent coherency disasters when compute cores update gradients in
cache while RDMA engines DMA those gradients to remote devices? If no,
how do you avoid the complexity of pinned memory and manual address
translation? This section explores Gaudi\'s solution and its
implications for distributed training.

### The Integration Challenge

**Traditional Architecture (NVIDIA + Mellanox):**

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="440" viewBox="0 0 900 440" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" style="fill:#212121" />
    </marker>
    <marker id="arrc" markerwidth="12" markerheight="12" refx="6" refy="6" orient="auto">
      <path d="M0,0 L0,10 L10,5 z" style="fill:#1565C0" />
    </marker>
    <marker id="arro" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" style="fill:#E65100" />
    </marker>
    <filter id="sh" x="-5%" y="-5%" width="115%" height="115%">
      <fedropshadow dx="2" dy="3" stddeviation="4" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
  </defs>

  <text x="450" y="28" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">GPU + RDMA NIC Integration: Heterogeneous Address Space Challenge</text>

  <!-- Left: Integrated (desired) -->
  <rect x="20" y="50" width="400" height="340" rx="8" filter="url(#sh)" style="fill:#E8F5E9; stroke:#4CAF50; stroke-width:2" />
  <text x="220" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#2E7D32; font-size:15; font-weight:bold; text-anchor:middle">✓ Integrated: Unified Address Space</text>
  <text x="220" y="93" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">(AMD MI300A / Apple M-series approach)</text>

  <rect x="40" y="105" width="160" height="90" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="120" y="138" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">GPU Die</text>
  <text x="120" y="158" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">Compute + MMU</text>
  <text x="120" y="176" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">Shared page tables</text>

  <rect x="230" y="105" width="160" height="90" rx="5" style="fill:#E65100; stroke:#BF360C; stroke-width:1.5" />
  <text x="310" y="138" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">RDMA NIC</text>
  <text x="310" y="158" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:12; text-anchor:middle">IOMMU shares</text>
  <text x="310" y="176" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:12; text-anchor:middle">CPU page tables</text>

  <!-- Shared memory pool -->
  <rect x="40" y="220" width="350" height="60" rx="5" style="fill:#00796B; stroke:#004D40; stroke-width:1.5" />
  <text x="215" y="248" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Unified Memory Pool (CPU + GPU + NIC)</text>
  <text x="215" y="267" font-family="Arial,Helvetica,sans-serif" style="fill:#B2DFDB; font-size:12; text-anchor:middle">Single virtual address space — zero-copy transfers</text>

  <!-- Arrows integrated -->
  <line x1="120" y1="195" x2="120" y2="218" marker-end="url(#arr)" style="stroke:#4CAF50; stroke-width:2"></line>
  <line x1="310" y1="195" x2="310" y2="218" marker-end="url(#arr)" style="stroke:#4CAF50; stroke-width:2"></line>

  <rect x="40" y="300" width="350" height="75" rx="5" style="fill:#C8E6C9" />
  <text x="215" y="322" font-family="Arial,Helvetica,sans-serif" style="fill:#2E7D32; font-size:13; font-weight:bold; text-anchor:middle">Benefits:</text>
  <text x="215" y="342" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• GPU tensor → NIC DMA with zero copy</text>
  <text x="215" y="360" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Single TLB invalidation covers all devices</text>

  <!-- Right: Discrete (challenge) -->
  <rect x="440" y="50" width="440" height="340" rx="8" filter="url(#sh)" style="fill:#FFEBEE; stroke:#EF5350; stroke-width:2" />
  <text x="660" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#C62828; font-size:15; font-weight:bold; text-anchor:middle">⚠ Discrete: Separate Address Spaces</text>
  <text x="660" y="93" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">(PCIe-attached GPU + separate NIC)</text>

  <rect x="460" y="105" width="160" height="90" rx="5" style="fill:#1565C0; stroke:#0D47A1; stroke-width:1.5" />
  <text x="540" y="132" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">GPU Die</text>
  <text x="540" y="150" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">Compute + MMU</text>
  <text x="540" y="168" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:12; text-anchor:middle">GPU page tables</text>

  <!-- PCIe bus -->
  <line x1="620" y1="150" x2="680" y2="150" marker-end="url(#arrc)" style="stroke:#9E9E9E; stroke-width:3"></line>
  <text x="650" y="143" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:11; text-anchor:middle">PCIe</text>
  <text x="650" y="167" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:11; text-anchor:middle">32 GB/s</text>

  <rect x="690" y="105" width="160" height="90" rx="5" style="fill:#E65100; stroke:#BF360C; stroke-width:1.5" />
  <text x="770" y="132" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">RDMA NIC</text>
  <text x="770" y="150" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:12; text-anchor:middle">Separate device</text>
  <text x="770" y="168" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:12; text-anchor:middle">CPU IOMMU</text>

  <!-- Separate memory -->
  <rect x="460" y="220" width="160" height="55" rx="5" style="fill:#9E9E9E; stroke:#757575; stroke-width:1.5" />
  <text x="540" y="244" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">HBM (GPU)</text>
  <text x="540" y="260" font-family="Arial,Helvetica,sans-serif" style="fill:#F5F5F5; font-size:12; text-anchor:middle">GPU VA space</text>

  <rect x="690" y="220" width="160" height="55" rx="5" style="fill:#9E9E9E; stroke:#757575; stroke-width:1.5" />
  <text x="770" y="244" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Host DRAM</text>
  <text x="770" y="260" font-family="Arial,Helvetica,sans-serif" style="fill:#F5F5F5; font-size:12; text-anchor:middle">CPU/NIC VA space</text>

  <line x1="540" y1="195" x2="540" y2="218" marker-end="url(#arr)" style="stroke:#9E9E9E; stroke-width:2"></line>
  <line x1="770" y1="195" x2="770" y2="218" marker-end="url(#arr)" style="stroke:#9E9E9E; stroke-width:2"></line>

  <rect x="460" y="295" width="390" height="80" rx="5" style="fill:#FFCDD2" />
  <text x="655" y="316" font-family="Arial,Helvetica,sans-serif" style="fill:#C62828; font-size:13; font-weight:bold; text-anchor:middle">Problems:</text>
  <text x="655" y="336" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• GPU→NIC requires buffer copy through host memory</text>
  <text x="655" y="354" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• Two separate TLB shootdowns per migration</text>
  <text x="655" y="372" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13; text-anchor:middle">• GDRCopy / GPUDirect partially mitigates copy cost</text>

  <!-- Bottom note -->
  <text x="450" y="418" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">Solution direction: CXL 3.0 memory pooling + P2P RDMA (GPUDirect RDMA) closes the gap for discrete topologies</text>
</svg>
</div>
<figcaption><strong>Figure 11.gpu-rdma:</strong> GPU + RDMA NIC
integration: discrete PCIe-attached devices use separate address spaces
(GPU page tables + CPU IOMMU), forcing costly buffer copies for GPU→NIC
transfers. Integrated designs (AMD MI300A, Intel Gaudi) share a single
MMU, enabling zero-copy RDMA directly from HBM.</figcaption>
</figure>

This separation simplifies coherency: GPU and NIC cannot share cache, so
there\'s no cache coherency to maintain. But PCIe limits bandwidth
(16-32 GB/s) and adds latency (\~1-2 µs per transfer).

**Gaudi Architecture:**

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="420" viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <marker id="arr2" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" style="fill:#212121" />
    </marker>
    <marker id="bi" markerwidth="10" markerheight="10" refx="1" refy="3" orient="auto">
      <path d="M9,0 L9,6 L0,3 z" style="fill:#00796B" />
    </marker>
    <marker id="bi2" markerwidth="10" markerheight="10" refx="9" refy="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" style="fill:#00796B" />
    </marker>
    <filter id="sh" x="-5%" y="-5%" width="115%" height="115%">
      <fedropshadow dx="2" dy="3" stddeviation="4" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
  </defs>

  <text x="450" y="28" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Intel Gaudi 2: Integrated Compute + RDMA on a Single Die</text>

  <!-- Gaudi 2 Die outer package -->
  <rect x="60" y="50" width="540" height="320" rx="10" filter="url(#sh)" style="fill:#E8F5E9; stroke:#2E7D32; stroke-width:2.5" />
  <text x="330" y="76" font-family="Arial,Helvetica,sans-serif" style="fill:#2E7D32; font-size:16; font-weight:bold; text-anchor:middle">Gaudi 2 Die — Single Monolithic Integration</text>

  <!-- Compute Cores block -->
  <rect x="80" y="90" width="220" height="230" rx="6" style="fill:#1565C0; stroke:#0D47A1; stroke-width:2" />
  <text x="190" y="118" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">Compute Cores</text>
  <text x="190" y="140" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">21 × TPC (Tensor Processor)</text>
  <text x="190" y="160" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">Matrix engines + vector</text>
  <!-- MMU sub-block -->
  <rect x="95" y="185" width="190" height="60" rx="4" style="fill:#0D47A1" />
  <text x="190" y="210" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">MMU</text>
  <text x="190" y="228" font-family="Arial,Helvetica,sans-serif" style="fill:#90CAF9; font-size:12; text-anchor:middle">Shared page tables</text>
  <!-- HBM label -->
  <text x="190" y="278" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">96 GB HBM2E</text>
  <text x="190" y="296" font-family="Arial,Helvetica,sans-serif" style="fill:#BBDEFB; font-size:13; text-anchor:middle">2.45 TB/s BW</text>

  <!-- Bidirectional arrow between compute and RDMA -->
  <line x1="300" y1="195" x2="360" y2="195" marker-start="url(#bi)" marker-end="url(#bi2)" style="stroke:#00796B; stroke-width:2.5"></line>
  <text x="330" y="185" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:12; text-anchor:middle">on-die</text>
  <text x="330" y="215" font-family="Arial,Helvetica,sans-serif" style="fill:#00796B; font-size:12; text-anchor:middle">fabric</text>

  <!-- RDMA Engines block -->
  <rect x="360" y="90" width="220" height="230" rx="6" style="fill:#E65100; stroke:#BF360C; stroke-width:2" />
  <text x="470" y="118" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:15; font-weight:bold; text-anchor:middle">RDMA Engines</text>
  <text x="470" y="140" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:13; text-anchor:middle">24 × 100 GbE ports</text>
  <text x="470" y="160" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:13; text-anchor:middle">= 2.4 Tb/s fabric BW</text>
  <!-- Shared MMU reference -->
  <rect x="375" y="185" width="190" height="60" rx="4" style="fill:#BF360C" />
  <text x="470" y="210" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:14; font-weight:bold; text-anchor:middle">Shares MMU</text>
  <text x="470" y="228" font-family="Arial,Helvetica,sans-serif" style="fill:#FFCCBC; font-size:12; text-anchor:middle">Same VA → PA mapping</text>
  <!-- RoCEv2 label -->
  <text x="470" y="278" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:13; text-anchor:middle">RoCEv2 protocol</text>
  <text x="470" y="296" font-family="Arial,Helvetica,sans-serif" style="fill:#FFE0B2; font-size:13; text-anchor:middle">Zero-copy DMA</text>

  <!-- HBM stacks at bottom of die -->
  <rect x="80" y="335" width="500" height="25" rx="4" style="fill:#00796B" />
  <text x="330" y="352" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">HBM2E Stack — shared by compute cores and RDMA engines</text>

  <!-- Right side: benefits panel -->
  <rect x="625" y="50" width="255" height="320" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="752" y="75" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:15; font-weight:bold; text-anchor:middle">Integration Benefits</text>

  <text x="635" y="100" font-family="Arial,Helvetica,sans-serif" style="fill:#2E7D32; font-size:13; font-weight:bold">✓ Zero-copy tensor transfer:</text>
  <text x="640" y="118" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">RDMA engine DMA-reads</text>
  <text x="640" y="136" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">directly from HBM using</text>
  <text x="640" y="154" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">shared page tables.</text>

  <text x="635" y="180" font-family="Arial,Helvetica,sans-serif" style="fill:#2E7D32; font-size:13; font-weight:bold">✓ Single TLB invalidation:</text>
  <text x="640" y="198" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">One TLBI flushes both</text>
  <text x="640" y="216" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">compute and network MMU</text>
  <text x="640" y="234" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">simultaneously.</text>

  <text x="635" y="260" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:13; font-weight:bold">Vs. discrete GPU+NIC:</text>
  <text x="640" y="278" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:13">Eliminates 2× buffer copy</text>
  <text x="640" y="296" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:13">and PCIe bottleneck</text>
  <text x="640" y="314" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:13">(32 GB/s → 2.4 Tb/s).</text>

  <!-- Network ports at bottom -->
  <rect x="60" y="385" width="540" height="28" rx="4" style="fill:#E3F2FD; stroke:#1565C0; stroke-width:1.5" />
  <text x="330" y="403" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:middle">24 × 100 GbE ports → external fabric (used for AllReduce in LLM training)</text>
</svg>
</div>
<figcaption><strong>Figure 11.gaudi2:</strong> Intel Gaudi 2 integrated
die: 21 Tensor Processing Cores and 24×100 GbE RDMA engines share a
single MMU and HBM2E (96 GB, 2.45 TB/s). RDMA engines DMA directly from
HBM using the same page tables as compute cores, achieving zero-copy
collective transfers without PCIe bottleneck.</figcaption>
</figure>

Now compute cores and RDMA engines can potentially access the same cache
lines, creating classic cache coherency challenges---but without
hardware coherency protocols like CPU caches have.

### MMU Sharing: Address Translation Services (ATS)

Gaudi\'s RDMA engines support PCIe ATS (Address Translation Services),
even though they\'re not actually connected via PCIe. ATS allows RDMA
engines to query the MMU for translations and cache results locally.

**RDMA Engine Architecture:**

    Each RDMA engine contains:
    - ATC (Address Translation Cache): 1,024 entries
    - Send/receive queues for RDMA operations
    - DMA engine for memory transfers

    ATC acts as a TLB for the RDMA engine

**Translation Flow (RDMA Send Operation):**

    Step 1: Application posts send request
      rdma_send(gradient_buffer, 140GB, remote_gpu_id)

    Step 2: RDMA engine receives request
      - Virtual address: gradient_buffer = 0x7fff0000
      - Check ATC (RDMA engine's TLB)

    Step 3a: ATC hit (translation cached)
      - PA = 0x1234_5000 (from ATC)
      - DMA directly from physical address
      - Send over network
      
    Step 3b: ATC miss (translation not cached)
      - Send ATS translation request to MMU
      - MMU walks page tables (4 levels)
      - MMU returns PA = 0x1234_5000
      - RDMA engine caches in ATC
      - DMA from physical address

**ATC Coverage:**

    ATC size: 1,024 entries per RDMA engine
    With 2 MB pages: 1,024 × 2 MB = 2 GB coverage
    With 1 GB pages: 1,024 × 1 GB = 1 TB coverage

    LLaMA 70B gradients: 140 GB
    With 2 MB pages: 71,680 pages, ATC covers 1.4%
    With 1 GB pages: 140 pages, ATC covers 100%

    Result: 1 GB pages mandatory for zero-overhead RDMA

### Cache Coherency Challenge

The core problem: when compute cores and RDMA engines share an MMU but
not hardware cache coherency, manual intervention is required.

**Race Condition Scenario:**

    Time T0: Compute core computes gradient
      gradient[0] = 0.5
      Write goes to L3 cache (cached, not written to HBM yet)

    Time T1: All-reduce initiates RDMA send
      rdma_send(gradient, 140GB, remote_gpu)

    Time T2: RDMA engine DMAs gradient[0]
      - Reads from physical address 0x1234_5000 in HBM
      - HBM contains old value (0.0), not cached value (0.5)
      - Sends wrong gradient to remote GPU!

    Time T3: Remote GPU receives gradient = 0.0
      - Computes incorrect parameter update
      - Model diverges, training fails

The problem: compute core\'s write sits in L3 cache, while RDMA engine
reads from HBM, bypassing the cache.

**Why Hardware Coherency Doesn\'t Solve This:**

CPU cache coherency protocols (MESI, MOESI) work because: 1. All cache
controllers snoop on bus transactions 2. When one cache modifies a line,
others invalidate their copies 3. DMA controllers participate in
coherency protocol

Gaudi\'s RDMA engines don\'t participate in cache coherency: - They\'re
DMA engines, not caches - They access physical memory directly - They
can\'t \"snoop\" on compute core cache updates

### Software Solution: Explicit Cache Flush

Before RDMA send, software must flush cache lines to memory:

``` {.sourceCode .c}
// Step 1: Compute gradients (writes go to cache)
compute_gradients(gradients, 140GB);

// Step 2: Flush cache to ensure RDMA sees updates
flush_cache_range(gradients, 140GB);
memory_barrier();  // Ensure flush completes

// Step 3: Now safe for RDMA to send
rdma_send(gradients, 140GB, remote_gpu);
```

**Cache Flush Implementation:**

x86-64 provides `clflushopt` instruction:

``` {.sourceCode .c}
void flush_cache_range(void *addr, size_t size) {
    char *p = (char *)addr;
    char *end = p + size;
    
    while (p < end) {
        _mm_clflushopt(p);  // Flush this cache line
        p += 64;  // Next cache line (64-byte lines)
    }
    
    _mm_sfence();  // Wait for all flushes to complete
}
```

For 140 GB with 64-byte cache lines:

    Cache lines: 140 GB / 64 bytes = 2.29 billion cache lines
    Instructions: 2.29 billion clflushopt instructions
    Time at 1 instruction/cycle, 2 GHz: 1.15 seconds!

This 1.15-second overhead per all-reduce is unacceptable.

**Optimization 1: Flush Only Modified Lines**

Track which gradient chunks were actually modified:

``` {.sourceCode .c}
// During backward pass, mark modified regions
mark_dirty(gradient + offset, size);

// Before RDMA, flush only dirty lines
flush_dirty_cache_lines(gradient);
```

If only 10% of gradients change significantly per iteration:

    Flush time: 1.15 seconds × 10% = 115 ms

Still significant but more manageable.

**Optimization 2: Use Uncached Memory for RDMA Buffers**

Map gradient buffers as uncached (write-combining):

``` {.sourceCode .c}
// Allocate gradient buffer with uncached memory
void *gradients = mmap(NULL, 140GB, PROT_READ | PROT_WRITE,
                      MAP_ANONYMOUS | MAP_PRIVATE | MAP_HUGETLB,
                      -1, 0);
// Set memory type to write-combining (uncached)
madvise(gradients, 140GB, MADV_NOHUGEPAGE);  // Avoid caching
```

Uncached memory bypasses cache entirely: - Compute writes go directly to
HBM - RDMA reads from HBM (coherent by default) - No cache flush needed

Downside: Compute performance degrades (cache misses on every gradient
access).

**Optimization 3: Separate Buffers for Compute and RDMA**

``` {.sourceCode .c}
void *compute_gradients = malloc_cached(140GB);   // Cached
void *rdma_gradients = malloc_uncached(140GB);    // Uncached

// Compute into cached buffer (fast)
compute_gradients_kernel(compute_gradients);

// Copy to uncached buffer (explicit writeback)
memcpy(rdma_gradients, compute_gradients, 140GB);

// RDMA from uncached buffer (coherent)
rdma_send(rdma_gradients, 140GB, remote_gpu);
```

The `memcpy` forces a cache flush (reads from cached buffer, writes to
uncached buffer, writing flushes cache). But it requires 2× memory (280
GB for two 140 GB buffers).

### Gaudi\'s Optimized Approach: Compiler-Managed Coherency

Intel\'s compiler for Gaudi (part of the Habana SynapseAI SDK)
automatically inserts cache flushes:

``` {.sourceCode .c}
// User writes this:
gradients = backward_pass(activations, params);
all_reduce(gradients);

// Compiler generates:
gradients = backward_pass(activations, params);
__sync_synchronize();  // Memory barrier
cache_flush_async(gradients, 140GB);  // Background flush
all_reduce_prepare(gradients);  // Prepare RDMA
wait_flush_complete();  // Wait for flush
all_reduce_execute(gradients);  // Actually send
```

The `cache_flush_async` initiates flush in background, overlapping with
`all_reduce_prepare` (setting up RDMA descriptors). By the time
`all_reduce_execute` runs, flush has completed.

**Measured Overhead:**

    Without optimization: 1.15 seconds per all-reduce (flushing 140 GB)
    With async flush + overlap: 50 ms per all-reduce
    With dirty tracking: 5-15 ms per all-reduce

    Training iteration (LLaMA 70B):
    Forward: 40 ms
    Backward: 50 ms
    All-reduce (including flush): 15 ms
    Optimizer: 20 ms
    Total: 125 ms

    Overhead: 15 / 125 = 12%

The 12% overhead is acceptable given Gaudi\'s 4× network bandwidth
advantage (2.4 Tbps vs 600 GB/s NVLink).

### All-Reduce Performance: Gaudi vs NVLink

**Gaudi 2 Cluster (8 devices):**

    Configuration:
    - 8× Gaudi 2 devices
    - 24× 100 Gbps RDMA per device = 2.4 Tbps
    - All-to-all connectivity via 100 Gbps links

    LLaMA 70B gradient all-reduce (140 GB):
    - Ring all-reduce algorithm
    - Data transfer: 140 GB × 8 devices = 1.12 TB total
    - Bandwidth per device: 2.4 Tbps / 8 bits = 300 GB/s
    - Time: 1.12 TB / 300 GB/s = 3.7 seconds

    With cache flush overhead: 3.7 + 0.015 = 3.715 seconds

**NVIDIA 8× A100 (NVLink):**

    Configuration:
    - 8× A100 with NVLink
    - 600 GB/s per GPU NVLink bandwidth
    - All-to-all via NVSwitch

    LLaMA 70B gradient all-reduce (140 GB):
    - Ring all-reduce algorithm
    - Data transfer: 1.12 TB total
    - Bandwidth per GPU: 600 GB/s
    - Time: 1.12 TB / 600 GB/s = 1.87 seconds

    No cache flush overhead (separate devices)

NVLink is 2× faster for this configuration. But at larger scales:

**64-Device Comparison:**

    Gaudi: 64 devices × 2.4 Tbps = 153.6 Tbps aggregate
    Time: 1.12 TB / (153.6 Tbps / 8) = 0.058 seconds

    NVLink: 64 devices × 600 GB/s = 38.4 TB/s aggregate
    Time: 1.12 TB / (38.4 TB/s / 8) = 0.233 seconds

    Gaudi 4× faster at 64 devices

Gaudi\'s advantage emerges at scale due to higher aggregate network
bandwidth.

### TLB Considerations for RDMA

RDMA engines\' ATC (Address Translation Cache) behaves like a TLB. Page
size selection matters:

    With 4 KB pages:
    ATC: 1,024 entries × 4 KB = 4 MB coverage
    140 GB gradients: 36.7M pages
    ATC miss rate: 99.99%

    Each ATC miss requires:
    - ATS request to MMU: 500 ns
    - Page table walk: 400 ns
    - Total: 900 ns overhead per access

    Impact: RDMA becomes bottlenecked on translations

    With 1 GB pages:
    ATC: 1,024 entries × 1 GB = 1 TB coverage
    140 GB gradients: 140 pages
    ATC miss rate: 0% (fits entirely)

    Zero translation overhead for RDMA

**Measured Performance:**

    RDMA send (140 GB gradients):

    4 KB pages:
    Translation overhead: 36.7M misses × 900 ns = 33 seconds
    Data transfer: 140 GB / 300 GB/s = 0.47 seconds
    Total: 33.47 seconds (98.6% overhead!)

    1 GB pages:
    Translation overhead: 0 seconds (ATC 100% hit rate)
    Data transfer: 0.47 seconds
    Total: 0.47 seconds

    Speedup: 71×

The 71× speedup from page size alone demonstrates that huge pages
aren\'t optional---they\'re mandatory for RDMA performance.

### Summary: Habana Gaudi 2 MMU Insights

**ATS for RDMA:** RDMA engines use Address Translation Services,
querying the MMU for translations and caching in local ATC (1,024
entries).

**Cache Coherency Challenge:** Compute cores and RDMA engines share MMU
but not hardware coherency. Software must explicitly flush caches before
RDMA operations.

**Compiler-Managed Flushes:** SynapseAI compiler automatically inserts
async cache flushes, reducing overhead from 1.15 seconds to 15 ms.

**Huge Pages Critical:** 1 GB pages provide 100% ATC hit rate (vs 99.99%
miss rate with 4 KB pages), enabling 71× RDMA speedup.

**Scaling Advantage:** 2.4 Tbps per device enables 4× faster all-reduce
than NVLink at 64+ device scale, despite 12% cache flush overhead.

Next, we\'ll examine Apple\'s unified memory architecture, where CPU,
GPU, and Neural Engine all share a single 800 GB/s memory pool---and
discover why bandwidth arbitration and TLB shootdown become the limiting
factors. \## 11.8 Apple Neural Engine and Unified Memory MMU Challenges

Apple\'s M-series chips represent a different approach to AI/ML
acceleration: true unified memory where CPU cores, GPU cores, and the
Neural Engine all access a single pool of LPDDR or LPDDR5 DRAM without
discrete boundaries. Chapter 4, Section 4.13.6 introduced the
architectural concept---CPU and GPU share physical RAM with zero-copy
data transfers. This section examines the MMU challenges that emerge
when three fundamentally different processors contend for the same
memory bandwidth while maintaining TLB coherency.

### Bandwidth Arbitration Across Three Device Types

The M2 Ultra provides 800 GB/s of unified memory bandwidth serving three
clients:

**CPU cluster (24 cores total):** - 16 performance cores + 8 efficiency
cores - Memory access patterns: Pointer chasing, cache-friendly -
Typical bandwidth usage: 100-200 GB/s at full load - L1/L2/L3 cache
hierarchy reduces DRAM pressure

**GPU cluster (76 cores):** - Tile-based deferred rendering
architecture - Memory access patterns: Streaming reads/writes, texture
fetches - Typical bandwidth usage: 300-500 GB/s at full load - Smaller
caches than CPU, higher DRAM pressure

**Neural Engine (32 cores):** - Matrix multiplication accelerator -
Memory access patterns: Large sequential reads (weights), streaming
writes (activations) - Typical bandwidth usage: 60-100 GB/s during
inference - Minimal caching, direct DRAM access

The theoretical aggregate: 200 + 500 + 100 = 800 GB/s, perfectly
matching available bandwidth. In practice, workloads rarely maximize all
three simultaneously. But when they do---video encoding with real-time
ML enhancement---contention creates performance unpredictability.

Consider a video encoding pipeline with ML-based noise reduction:

    Frame processing workflow:
    1. CPU: Decode H.264 compressed frame
       - Entropy decode bitstream
       - Inverse DCT on 8×8 blocks
       - Memory traffic: 50 GB/s (read compressed, write decoded)

    2. Neural Engine: Denoise decoded frame
       - Read frame: 3840×2160×3 bytes = 25 MB
       - Load model weights: 40 MB
       - Compute denoised frame: 25 MB output
       - Memory traffic: 90 MB total, 60 GB/s with batching

    3. GPU: Composite denoised frame with UI overlay
       - Read denoised frame: 25 MB
       - Read UI elements: 5 MB
       - Blend and render: 30 MB output
       - Memory traffic: 100 GB/s with overdraw

    4. CPU: Encode H.265 compressed frame
       - DCT on 16×16 blocks
       - Entropy encode
       - Memory traffic: 40 GB/s (read uncompressed, write compressed)

    Sequential processing: 50 + 60 + 100 + 40 = 250 GB/s (fits in 800 GB/s budget)

But real-time 60 FPS video requires parallel processing. While the
Neural Engine denoises frame N, the GPU composites frame N-1, and the
CPU encodes frame N-2. All three access memory simultaneously:

    Simultaneous processing (pipelined):
    CPU encoding frame N-2:        40 GB/s
    GPU compositing frame N-1:    100 GB/s
    Neural Engine denoising N:     60 GB/s
    Total concurrent:             200 GB/s (well under 800 GB/s limit)

    But frame deadline spikes:
    All three reading/writing same region: 400 GB/s
    Memory controller serializes: Unpredictable latency
    One device stalls → pipeline bubble → frame dropped

The memory controller must arbitrate between competing requests.
Apple\'s implementation uses a priority-based arbiter with fairness
constraints, but the details are undocumented. Observed behavior
suggests:

- **Video DMA has highest priority** (dropped frames unacceptable)
- **Neural Engine second** (ML inference latency-sensitive)
- **GPU third** (can tolerate some frame jitter)
- **CPU lowest** (most tolerant of latency variation)

When all three devices access the same cache line simultaneously, the
memory controller serializes access even though the LPDDR5 interface
theoretically supports 800 GB/s. The bottleneck isn\'t bandwidth---it\'s
coherency. Each device has independent caches that must be kept
consistent.

### TLB Coherency Across CPU, GPU, and Neural Engine

All three device types share page tables---a single set of four-level
page tables maps virtual addresses to physical addresses for CPU, GPU,
and Neural Engine. This simplifies software (one set of page tables to
manage) but creates TLB coherency challenges when those page tables
change.

Consider unmapping a page that all three devices have cached in their
TLBs:

    CPU unmaps virtual page 0x7fff0000:
    1. Update page table entry (PTE): mark not present
    2. Invalidate CPU TLB across all 24 cores
    3. Invalidate GPU TLB across all 76 GPU cores
    4. Invalidate Neural Engine TLB across all 32 NPU cores
    5. Memory barrier: Ensure all invalidations complete
    6. Return to caller (unmap complete)

    Latency breakdown:
    CPU TLB invalidate:           50ns (on-die broadcast)
    GPU TLB invalidate:          150ns (fabric interconnect)
    Neural Engine TLB invalidate: 100ns (dedicated path)
    Memory barriers:              50ns (fence operations)
    Total TLB shootdown:         350ns (7× slower than CPU-only)

For comparison, on a traditional discrete GPU system:

    CPU unmaps page shared with discrete GPU:
    1. Update page table entry
    2. Invalidate CPU TLB: 50ns
    3. Send IPI to GPU driver: 5,000ns (PCIe round-trip)
    4. GPU driver invalidates GPU TLB: 500ns
    5. GPU driver acknowledges: 5,000ns (PCIe return)
    Total: ~10,500ns (30× slower than Apple unified)

Apple\'s unified memory reduces TLB shootdown latency dramatically
compared to discrete GPUs---350ns versus 10,500ns. But it\'s still 7×
slower than CPU-only shootdowns (50ns), and when page table updates are
frequent, this overhead becomes measurable.

Measuring TLB shootdown impact on a memory-intensive workload:

    Benchmark: Real-time ML inference with dynamic batching
    - Model: ResNet-50 (25M parameters)
    - Input: Variable batch size (1-64 images)
    - Page size: 4 KB (worst case for TLB shootdown)

    Batch size changes trigger allocation/deallocation:
    Small batch (1 image):   Allocate 1 MB activation buffer
    Large batch (64 images): Allocate 64 MB activation buffer

    Page table updates per batch size change:
    1 MB → 64 MB: Allocate 63 MB = 16,128 pages
    Each allocation: 1 TLB shootdown (CPU + GPU + NPU)
    16,128 pages × 350ns = 5.6ms overhead

    Inference time:
    Computation: 12ms per batch
    TLB overhead: 5.6ms
    Total: 17.6ms (32% overhead from TLB shootdowns!)

The solution: **pin activation buffers at the maximum size and reuse
them**:

    Optimized approach:
    1. Allocate 64 MB buffer once at startup
    2. Pin buffer (lock pages in physical memory)
    3. Reuse buffer for all batch sizes (waste some memory for small batches)
    4. Zero TLB shootdowns during inference

    Inference time:
    Computation: 12ms
    TLB overhead: 0ms
    Total: 12ms (32% speedup)

    Memory cost: 63 MB wasted when batch size = 1
    Trade-off: Memory (63 MB) for latency (5.6ms) is favorable

### When Unified Memory Wins: Sequential Access Patterns

Unified memory excels when workloads access data sequentially across
devices. Consider image processing with ML enhancement:

    Traditional discrete GPU workflow:
    1. CPU loads image from disk to system DRAM (4 MB image)
    2. CPU copies image to GPU over PCIe: 4 MB / 16 GB/s = 250μs
    3. GPU processes image (10ms)
    4. GPU copies result back to system DRAM: 4 MB / 16 GB/s = 250μs
    5. CPU writes processed image to disk

    Total PCIe overhead: 500μs per image
    At 60 FPS: 500μs × 60 = 30ms/sec = 3% of CPU time wasted on copies

With Apple unified memory:

    Unified memory workflow:
    1. CPU loads image from disk to DRAM (4 MB)
    2. CPU passes pointer to GPU (zero-copy)
    3. GPU processes image (10ms)
    4. GPU passes pointer back to CPU (zero-copy)
    5. CPU writes processed image to disk

    Total copy overhead: 0μs

The benefit is more pronounced for smaller images where PCIe latency
dominates:

    Small image (100 KB):
    Discrete GPU: 100 KB / 16 GB/s = 6μs + PCIe latency (10μs) = 16μs overhead
    Unified memory: 0μs overhead

    Processing time: 500μs
    Overhead as % of total:
    - Discrete: 16μs / 516μs = 3.1%
    - Unified: 0% (3.1% speedup)

For burst processing of many small images, this compounds. Processing
1,000 small images:

    Discrete GPU:
    - Per-image overhead: 16μs
    - Total overhead: 16ms
    - Computation: 500ms
    - Total: 516ms (3.1% slower)

    Unified memory:
    - Per-image overhead: 0μs
    - Total: 500ms

### When Unified Memory Loses: Concurrent Access Patterns

Unified memory\'s weakness emerges when CPU, GPU, and Neural Engine all
access memory intensively at the same time, creating bandwidth
contention and TLB pressure.

Benchmark: Scientific simulation with real-time visualization and ML
prediction:

    Workload:
    - CPU: Physics simulation (particle interactions)
      Memory: 4 GB working set, random access
      Bandwidth: 180 GB/s sustained

    - GPU: Real-time rendering of particle positions
      Memory: 2 GB vertex data, streaming access
      Bandwidth: 320 GB/s sustained

    - Neural Engine: ML prediction of future particle positions
      Memory: 1 GB model + 500 MB activations
      Bandwidth: 90 GB/s sustained

    Total theoretical: 590 GB/s (under 800 GB/s limit)
    Actual achieved: 450 GB/s (76% efficiency)

    Performance degradation sources:
    1. Memory controller contention: 50 GB/s loss
    2. TLB shootdowns (simulation updates state): 30 GB/s loss
    3. Cache coherency traffic: 60 GB/s loss
    Total overhead: 140 GB/s (24% efficiency loss)

Profiling reveals TLB shootdown frequency as the primary bottleneck:

    Physics simulation updates:
    - 10,000 particles × 48 bytes/particle = 480 KB updated per timestep
    - 60 timesteps/second
    - Each update triggers TLB shootdown (if using 4 KB pages)

    TLB shootdowns per second:
    - 480 KB / 4 KB = 120 pages updated per timestep
    - 120 pages × 60 timesteps = 7,200 TLB shootdowns/second
    - Each shootdown: 350ns
    - Total overhead: 7,200 × 350ns = 2.52ms/second (0.25% CPU time)

    But TLB shootdowns block memory access:
    - All three devices stall during shootdown
    - 2.52ms/sec × 3 devices = 7.56ms/sec = 0.76% throughput loss
    - At high bandwidth: 0.76% × 800 GB/s = 6 GB/s effective loss

The solution: **use huge pages to reduce TLB shootdown frequency**:

    With 2 MB pages:
    - 480 KB / 2 MB = 1 page updated per timestep (rounded up)
    - 1 page × 60 timesteps = 60 TLB shootdowns/second (120× reduction)
    - Total overhead: 60 × 350ns = 21μs/second (negligible)

    Result: Bandwidth recovers from 450 GB/s to 570 GB/s (27% improvement)

### Page Size Selection for M-series Unified Memory

The M2 Ultra\'s 192 GB unified memory address space creates interesting
page size trade-offs:

    With 4 KB pages:
    - 192 GB / 4 KB = 50,331,648 pages
    - Page table overhead: 50.3M PTEs × 8 bytes = 403 MB
    - Plus upper-level page table structures: ~410 MB total
    - TLB coverage (2,048-entry L2 TLB): 2,048 × 4 KB = 8 MB (0.004% of RAM)

    With 2 MB pages:
    - 192 GB / 2 MB = 98,304 pages
    - Page table overhead: 98.3K PTEs × 8 bytes = 787 KB
    - Plus upper levels: ~800 KB total (500× less than 4 KB pages)
    - TLB coverage: 2,048 × 2 MB = 4 GB (2.08% of RAM)

    With 1 GB pages:
    - 192 GB / 1 GB = 192 pages
    - Page table overhead: 192 PTEs × 8 bytes = 1.5 KB
    - Plus upper levels: ~10 KB total (40,000× less than 4 KB pages)
    - TLB coverage: 2,048 × 1 GB = 2,048 GB (full coverage, 1,067% over-provisioned)

For AI/ML workloads on M-series, the recommendation:

**Model parameters: 1 GB pages** - LLaMA 13B model: 26 GB in FP16 - With
1 GB pages: 26 pages (fits entirely in TLB) - With 4 KB pages: 6.8M
pages (TLB miss rate: 99.97%)

**Activations: 2 MB pages** - Batch processing creates mid-size
allocations (100 MB - 1 GB) - 2 MB pages balance TLB coverage and
fragmentation - Example: 500 MB activation buffer = 250 pages
(manageable TLB footprint)

**Dynamic tensors: 4 KB pages** - Small, short-lived allocations (\< 1
MB) - Minimal TLB pressure (not accessed frequently) - Avoids internal
fragmentation

This mixed page size strategy achieves 95%+ TLB hit rates for typical ML
inference workloads on M-series chips, eliminating TLB misses as a
bottleneck despite the massive 192 GB address space.

### Practical Implications for M-Series Development

Developers targeting Apple\'s Neural Engine must navigate three
constraints:

**Constraint 1: Bandwidth budget is shared.** Unlike discrete GPUs where
bandwidth is dedicated, M-series bandwidth (800 GB/s on M2 Ultra) serves
CPU, GPU, and NPU concurrently. A GPU-intensive game running in the
background consumes bandwidth that would otherwise be available to the
Neural Engine. This unpredictability complicates performance guarantees.

**Constraint 2: TLB shootdowns affect all devices.** Frequent memory
allocation/deallocation triggers TLB invalidations across CPU, GPU, and
NPU simultaneously. This isn\'t an issue on discrete GPUs where CPU TLB
invalidations don\'t affect the GPU. On M-series, the cost multiplies.

**Constraint 3: Cache coherency overhead is implicit.** Unlike
architectures where cache coherency is optional (GPU memory can be
marked uncached), M-series enforces coherency across all caches. When
the Neural Engine writes to memory, those writes must be made visible to
CPU L3 cache. This coherency traffic consumes bandwidth that doesn\'t
appear in application-level measurements.

The upside: zero-copy data sharing provides enormous convenience and
eliminates PCIe bottlenecks. The downside: resource contention and TLB
coordination introduce performance variability that discrete
accelerators avoid. For real-time ML inference on M-series, pinning
buffers and using huge pages aren\'t optimizations---they\'re
requirements for predictable performance. \## 11.9 Common Pitfalls and
Best Practices

After examining virtual memory across TPU, NVIDIA GPUs, AMD MI300X,
Intel Habana, and Apple Neural Engine, recurring patterns
emerge---mistakes that degrade performance predictably and solutions
that restore efficiency. This section catalogs six critical pitfalls
with root cause analysis, detection strategies, and proven mitig

ations.

### Pitfall 1: Training Without Prefetching (Page Fault Storms)

**Problem:** Launching GPU kernels before memory is resident in device
memory triggers page fault storms where thousands of threads fault
simultaneously.

**Root cause:** CUDA Unified Memory (UVM) uses demand paging---pages
migrate to GPU only when accessed. A training batch processing 1,024
images might touch 4 GB of new activations. If none of those 1,048,576
pages (with 4 KB pages) are resident, all 10,752 CUDA cores on an A100
fault simultaneously.

**Detection:**

``` {.sourceCode .bash}
# Using NVIDIA nvprof profiler:
nvprof --print-gpu-trace python train.py

# Look for:
# - High "page migration" count (>100 per kernel launch)
# - Kernel execution time >> expected (fault overhead)
# - "cudaMemcpyAsync HtoD" missing before kernel launch
```

``` {.sourceCode .python}
# Programmatic detection with PyTorch:
import torch.cuda
torch.cuda.synchronize()
start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)

start.record()
model(batch)  # First batch (cold, many faults)
end.record()
torch.cuda.synchronize()
cold_time = start.elapsed_time(end)

start.record()
model(batch)  # Second batch (warm, few faults)
end.record()
torch.cuda.synchronize()
warm_time = start.elapsed_time(end)

if cold_time > 2 * warm_time:
    print(f"Page fault overhead detected: {cold_time}ms (cold) vs {warm_time}ms (warm)")
```

**Example impact:**

    Training ResNet-50 on ImageNet:
    - Batch size: 256 images
    - Activation memory: 2 GB per batch
    - Without prefetch:
      * First batch: 350ms (includes 180ms page fault overhead)
      * Subsequent batches: 170ms
      * Overhead: 51% on first batch

    - With prefetch:
      * All batches: 170ms
      * No overhead

**Solution:**

``` {.sourceCode .python}
# PyTorch approach: Prefetch batches before processing
import torch

# Option 1: Prefetch next batch while processing current
dataloader = torch.utils.data.DataLoader(dataset, batch_size=256, 
                                         prefetch_factor=2,  # Prefetch 2 batches ahead
                                         num_workers=4)

for batch in dataloader:
    # By the time we process batch N, batch N+1 and N+2 are prefetching
    outputs = model(batch)

# Option 2: Explicit prefetch with CUDA streams
stream = torch.cuda.Stream()
with torch.cuda.stream(stream):
    next_batch = next(iter(dataloader))
    next_batch = next_batch.cuda(non_blocking=True)  # Prefetch to GPU

# Process current batch while next batch transfers
outputs = model(current_batch)
torch.cuda.current_stream().wait_stream(stream)  # Wait for prefetch
current_batch = next_batch

# Option 3: Pin critical buffers at startup
model.cuda()  # Move model parameters to GPU once
torch.cuda.empty_cache()  # Clear any fragmented memory

# Allocate and pin activation buffers
max_activations = torch.zeros(256, 3, 224, 224, device='cuda', pin_memory=True)
```

------------------------------------------------------------------------

### Pitfall 2: Using 4KB Pages for Large Models (TLB Thrashing)

**Problem:** Training 70B+ parameter models with 4 KB pages yields
99.9%+ TLB miss rates, adding 400ns latency to every memory access.

**Root cause:** Modern GPUs have 2,048-entry L2 TLBs. With 4 KB pages,
this covers 8 MB. A 70B model (140 GB in FP16) requires 36.7 million
pages. TLB coverage: 8 MB / 140 GB = 0.0057%. Virtually every access
misses, triggering expensive page table walks.

**Detection:**

``` {.sourceCode .bash}
# Using NVIDIA Nsight Compute:
ncu --metrics l2tex_tlb_hit_rate,l2tex_tlb_miss_rate kernel

# Expected output showing thrashing:
# l2tex_tlb_hit_rate: 0.12%  (99.88% miss rate - disaster!)
# l2tex_tlb_miss_rate: 99.88%

# Compare to healthy output:
# l2tex_tlb_hit_rate: 95.3%  (using huge pages)
# l2tex_tlb_miss_rate: 4.7%
```

**Quantitative impact:**

    LLaMA 70B model training (FP16):
    - Parameters: 70B × 2 bytes = 140 GB
    - Optimizer state (Adam): 70B × 8 bytes = 560 GB
    - Total: 700 GB

    With 4 KB pages:
    - Pages: 700 GB / 4 KB = 183.5 million pages
    - TLB entries: 2,048
    - TLB coverage: 8 MB (0.0011% of memory)
    - TLB miss rate: 99.999%
    - Page table walk: 4 levels × 100ns = 400ns
    - Memory access latency: 100ns (base) + 400ns (walk) = 500ns
    - Effective bandwidth: Original × (100ns / 500ns) = 20% of peak
    - Training throughput: 100 iterations/sec → 20 iterations/sec (5× slowdown)

    With 1 GB pages:
    - Pages: 700 GB / 1 GB = 700 pages
    - TLB entries: 2,048 (plenty of room)
    - TLB coverage: 2,048 GB (full coverage)
    - TLB miss rate: 0%
    - Memory access latency: 100ns (no walk)
    - Training throughput: 100 iterations/sec (full speed)

**Solution:**

``` {.sourceCode .bash}
# Linux: Reserve 1 GB huge pages at boot
# Add to /etc/sysctl.conf:
vm.nr_hugepages_1GB = 800  # Reserve 800 GB as 1 GB pages

# Apply:
sudo sysctl -p

# Verify:
cat /proc/meminfo | grep Huge
# Should show:
# HugePages_Total: 800
# HugePages_Free: 800
# Hugepagesize: 1048576 kB
```

``` {.sourceCode .python}
# PyTorch: Request huge pages for model parameters
import torch
import os

# Set environment variable before PyTorch initialization
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'

# Allocate model on GPU (will use huge pages if available)
model = LargeLanguageModel(70_000_000_000).cuda()

# Verify huge page usage:
torch.cuda.memory_stats()
# Look for 'active_bytes.all.allocated' using large blocks
```

**When huge pages aren\'t available:**

``` {.sourceCode .python}
# Fallback: Use memory pooling to reduce TLB pressure
allocator = torch.cuda.memory.CUDAPluggableAllocator(
    'my_allocator.so',
    'my_malloc',
    'my_free'
)
torch.cuda.memory.change_current_allocator(allocator)
```

------------------------------------------------------------------------

### Pitfall 3: Ignoring Multi-GPU TLB Synchronization Overhead

**Problem:** Naively invalidating TLBs sequentially across 256+ GPUs
creates multi-millisecond stalls that bottleneck distributed training.

**Root cause:** Each GPU TLB invalidation requires sending a message,
waiting for the GPU to process it, and receiving acknowledgment. Done
serially, this takes GPU_count × per_GPU_latency.

**Detection:**

``` {.sourceCode .python}
# PyTorch distributed profiling:
import torch.distributed as dist
import time

def profile_tlb_shootdown():
    if dist.get_rank() == 0:  # Master GPU
        # Allocate and free memory (triggers TLB shootdown)
        start = time.perf_counter()
        buffer = torch.zeros(1024 * 1024 * 1024, device='cuda')  # 1 GB
        del buffer
        torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        
        gpu_count = dist.get_world_size()
        per_gpu = elapsed / gpu_count
        print(f"TLB shootdown: {elapsed*1000:.2f}ms total, {per_gpu*1000:.2f}ms per GPU")
        
        if per_gpu > 0.010:  # 10μs per GPU is threshold
            print("WARNING: Serial TLB shootdown detected!")
            print(f"Expected with NVSwitch: ~0.05ms total")
            print(f"Got: {elapsed*1000:.2f}ms (likely serial)")
```

**Example impact:**

    Training GPT-3 across 1,024 NVIDIA H100 GPUs:
    - Training loop allocates activation buffers each iteration
    - Buffer size: 10 GB per GPU
    - Pages (2 MB huge pages): 10 GB / 2 MB = 5,120 pages

    Serial TLB invalidation:
    - Per-GPU latency: 10μs
    - Total: 1,024 GPUs × 10μs = 10.24ms per allocation
    - Allocations per iteration: 3 (forward, backward, optimizer buffers)
    - Overhead per iteration: 30.72ms
    - Iteration time: 100ms (compute) + 30.72ms (TLB) = 130.72ms
    - Throughput: 7.6 iterations/sec
    - Efficiency: 100ms / 130.72ms = 76.5%

    NVSwitch broadcast TLB invalidation:
    - Broadcast latency: 50μs (all GPUs receive simultaneously)
    - Overhead per iteration: 3 × 50μs = 150μs
    - Iteration time: 100ms + 0.15ms = 100.15ms
    - Throughput: 9.98 iterations/sec
    - Efficiency: 100ms / 100.15ms = 99.8%

    Improvement: 9.98 / 7.6 = 1.31× speedup (31% faster)

**Solution:**

``` {.sourceCode .python}
# PyTorch: Use NCCL for coordinated TLB operations
import torch.distributed as dist

# Initialize process group with NCCL backend
dist.init_process_group(backend='nccl')

# NCCL automatically uses NVSwitch hardware broadcast when available
# For manual control:
if dist.get_backend() == 'nccl':
    # NCCL will use hardware TLB broadcast
    tensor = torch.zeros(10 * 1024**3, device='cuda')  # 10 GB
    # Deallocation uses optimized broadcast invalidation
    del tensor
else:
    print("WARNING: Not using NCCL, TLB shootdown may be slow")
    
# Alternative: Batch invalidations
class BatchedAllocator:
    def __init__(self):
        self.pending_frees = []
        
    def free(self, ptr):
        self.pending_frees.append(ptr)
        if len(self.pending_frees) >= 100:  # Batch threshold
            self.flush()
    
    def flush(self):
        # Free all pending allocations with single TLB shootdown
        for ptr in self.pending_frees:
            torch.cuda.caching_allocator_delete(ptr)
        self.pending_frees.clear()
```

------------------------------------------------------------------------

### Pitfall 4: Page Migration Thrashing (CPU↔︎GPU Ping-Pong)

**Problem:** Pages repeatedly migrate between CPU and GPU, wasting
bandwidth and adding latency.

**Root cause:** CUDA Unified Memory\'s automatic migration moves pages
to whichever processor accessed them last. If CPU and GPU alternate
accessing the same data, the page migrates back and forth.

**Detection:**

``` {.sourceCode .bash}
# NVIDIA nvprof migration tracking:
nvprof --print-gpu-trace --unified-memory-profiling per-process-device python train.py

# Look for:
# "Data Migration (DtoH)" and "Data Migration (HtoD)" in rapid succession
# Same addresses migrating repeatedly
```

**Example scenario:**

``` {.sourceCode .python}
# Problematic code: CPU-GPU ping-pong
for batch in dataloader:
    # 1. Batch loaded by CPU (page migrates to CPU)
    batch = preprocess_on_cpu(batch)
    
    # 2. GPU accesses batch (page migrates to GPU) - 100μs migration
    outputs = model(batch.cuda())
    
    # 3. CPU computes loss (page migrates back to CPU) - 100μs migration
    loss = cpu_compute_loss(outputs.cpu(), labels)
    
    # Total migration: 200μs per batch
    # At 1,000 batches/epoch: 200ms migration overhead

# With 50ms per batch compute, overhead is 200ms / 50,000ms = 0.4%
# Seems minor, but accumulates over many epochs
```

**Solution:**

``` {.sourceCode .python}
# Fix 1: Keep data on GPU throughout
for batch in dataloader:
    batch = batch.cuda()  # Move once
    batch = preprocess_on_gpu(batch)  # Use GPU for preprocessing
    outputs = model(batch)
    loss = gpu_compute_loss(outputs, labels.cuda())  # Compute loss on GPU
    # Zero migrations!

# Fix 2: Use cudaMemAdvise to prevent migration
import torch.cuda

tensor = torch.zeros(1024, device='cuda')
# Advise: Keep on GPU, allow CPU read access without migration
torch.cuda.mem_advise(tensor, advice='set_read_mostly')

# Fix 3: Pin data to CPU if only CPU accesses
cpu_data = torch.zeros(1024, pin_memory=True)
# This data never migrates, GPU can DMA directly from pinned CPU memory
```

------------------------------------------------------------------------

### Pitfall 5: Assuming Cache Coherency Exists (Stale DMA Reads)

**Problem:** RDMA engines or DMA controllers read stale data from DRAM
while updated values sit in CPU/GPU cache.

**Root cause:** PCIe devices are outside the cache coherency domain.
When a CPU writes to memory, the write may stay in L3 cache. If a DMA
engine reads that address from DRAM, it gets the old value.

**Detection:** Extremely difficult---manifests as random incorrect
results in DMA transfers. Look for: - Inference results that vary
between runs on same input - Gradients that occasionally have wrong
values - Checksum mismatches on RDMA transfers

**Example scenario:**

``` {.sourceCode .c}
// Intel Habana Gaudi 2: Compute core updates gradient, RDMA engine sends it
float *gradients = allocate_on_device(70_000_000_000 * sizeof(float));

// Compute core (cached):
compute_gradients(gradients);  // Updates written to L3 cache

// RDMA engine (uncached):
rdma_send(gradients, size);  // Reads from HBM, not L3!
                             // Sends old gradient values!
```

**Solution:**

``` {.sourceCode .c}
// Explicit cache flush before DMA
compute_gradients(gradients);

// Flush cache line containing gradients to DRAM
flush_cache_range(gradients, size);

// Memory barrier to ensure flush completes
memory_barrier();

// Now safe for DMA to read
rdma_send(gradients, size);
```

``` {.sourceCode .python}
# PyTorch equivalent:
import torch

# Compute gradients (may be in cache)
loss.backward()

# Synchronize to ensure cache flushes
torch.cuda.synchronize()

# Now safe to access from RDMA or host
```

**Platform-specific solutions:**

``` {.sourceCode .c}
// x86-64: Use non-temporal stores (bypass cache)
for (int i = 0; i < n; i += 64) {
    _mm512_stream_ps(&gradients[i], values);  // Direct to DRAM
}
_mm_sfence();  // Ensure stores complete before DMA

// ARM64: Use device memory type
// Map DMA buffers as device memory (uncached)
mmap(..., PROT_READ | PROT_WRITE, MAP_SHARED | MAP_NORESERVE, ...)

// CUDA: Use cudaHostAlloc with portable flag
cudaHostAlloc(&gradients, size, cudaHostAllocWriteCombined);
// Write-combined memory bypasses cache
```

------------------------------------------------------------------------

### Pitfall 6: Over-Committing Unified Memory Bandwidth

**Problem:** On Apple M-series, assuming CPU, GPU, and Neural Engine can
each use full bandwidth simultaneously leads to severe contention.

**Root cause:** M2 Ultra has 800 GB/s total bandwidth shared by all
three processors. If each tries to use 400 GB/s, total demand (1,200
GB/s) exceeds supply (800 GB/s), causing unpredictable slowdowns.

**Detection:**

``` {.sourceCode .swift}
// Metal Performance Shaders to monitor bandwidth:
import MetalPerformanceShaders

let device = MTLCreateSystemDefaultDevice()!
let commandQueue = device.makeCommandQueue()!

// Profile GPU bandwidth usage
let buffer = device.makeBuffer(length: 1024*1024*1024)!
let start = CACurrentMediaTime()

// GPU read operation
commandQueue.insertDebugCaptureBoundary()
let commandBuffer = commandQueue.makeCommandBuffer()!
let blitEncoder = commandBuffer.makeBlitCommandEncoder()!
blitEncoder.copy(from: buffer, sourceOffset: 0, 
                 to: destBuffer, destinationOffset: 0, size: buffer.length)
blitEncoder.endEncoding()
commandBuffer.commit()
commandBuffer.waitUntilCompleted()

let elapsed = CACurrentMediaTime() - start
let bandwidth = Double(buffer.length) / elapsed / 1e9

print("GPU bandwidth: \(bandwidth) GB/s")
if bandwidth < 300 {
    print("WARNING: Bandwidth contention detected (expected 400+ GB/s)")
}
```

**Solution:**

``` {.sourceCode .swift}
// Partition bandwidth budget:
// - CPU: 200 GB/s (background tasks)
// - GPU: 400 GB/s (rendering)
// - Neural Engine: 200 GB/s (ML inference)
// Total: 800 GB/s (within limit)

// Reduce CPU background activity:
ProcessInfo.processInfo.performExpiringActivity(
    withReason: "ML inference critical path"
) { expired in
    if !expired {
        // Temporarily reduce CPU memory traffic
        disable_background_tasks()
    }
}

// Or serialize GPU/NPU usage:
if gpu_workload_active {
    // Defer NPU inference until GPU idle
    defer_npu_inference()
}
```

------------------------------------------------------------------------

## References

### GPU MMU Architecture and Virtual Memory

1.  Pichai, Bharath, et al. \"Architectural support for address
    translation on GPUs: Designing memory management units for CPU/GPUs
    with unified address spaces.\" *ACM SIGPLAN Notices* 49.4 (2014):
    743-758. DOI: 10.1145/2644865.2541940 \[Foundational work on GPU MMU
    design\]

2.  Power, Jason, et al. \"Supporting x86-64 address translation for
    100s of GPU lanes.\" *2014 IEEE 20th International Symposium on High
    Performance Computer Architecture (HPCA)*. IEEE, 2014. DOI:
    10.1109/HPCA.2014.6835960 \[Page table walker design for GPUs\]

3.  Ausavarungnirun, Rachata, et al. \"Mosaic: A GPU memory manager with
    application-transparent support for multiple page sizes.\"
    *Proceedings of the 50th Annual IEEE/ACM International Symposium on
    Microarchitecture (MICRO 2017)*. ACM, 2017. DOI:
    10.1145/3123939.3123975 \[Huge page management for GPUs\]

4.  Vesely, Jan, et al. \"Observations and opportunities in architecting
    shared virtual memory for heterogeneous systems.\" *2016 IEEE
    International Symposium on Performance Analysis of Systems and
    Software (ISPASS)*. IEEE, 2016. DOI: 10.1109/ISPASS.2016.7482078
    \[Unified memory challenges\]

5.  NVIDIA Corporation. *CUDA C++ Programming Guide*. Version
    12.3. 2024. Chapter 3: \"Unified Memory Programming.\" \[Official
    unified memory documentation\]

6.  NVIDIA Corporation. *CUDA C++ Best Practices Guide*. Version
    12.3. 2024. Section 8.2: \"Unified Memory Performance Guidelines.\"
    \[Performance optimization recommendations\]

### Google TPU Architecture

7.  Jouppi, Norman P., et al. \"In-datacenter performance analysis of a
    tensor processing unit.\" *Proceedings of the 44th Annual
    International Symposium on Computer Architecture (ISCA 2017)*.
    ACM, 2017. DOI: 10.1145/3079856.3080246 \[Original TPU v1 paper\]

8.  Jouppi, Norman P., et al. \"A domain-specific supercomputer for
    training deep neural networks.\" *Communications of the ACM* 63.7
    (2020): 67-78. DOI: 10.1145/3360307 \[TPU v2/v3 architecture and
    systolic arrays\]

9.  Google Cloud. \"Cloud TPU System Architecture.\" *Google Cloud
    Documentation*. 2024.
    https://cloud.google.com/tpu/docs/system-architecture-tpu-vm \[TPU
    v4/v5 virtual memory additions\]

### Multi-GPU Coordination and Scaling

10. Zhao, Hongzhang, et al. \"Multi-GPU graph analytics.\" *2020 IEEE
    International Parallel and Distributed Processing Symposium
    (IPDPS)*. IEEE, 2020. DOI: 10.1109/IPDPS47924.2020.00116 \[Multi-GPU
    TLB coherency protocols\]

11. NVIDIA Corporation. \"NVIDIA Collective Communications Library
    (NCCL) Documentation.\" Version 2.19. 2024.
    https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/
    \[Multi-GPU gradient synchronization\]

12. NVIDIA Corporation. \"NVSwitch Architecture Whitepaper.\" 2023.
    \[Hardware broadcast mechanisms\]

### AMD MI300X and Chiplet Architectures

13. AMD. \"AMD Instinct MI300X Accelerator.\" *AMD Product
    Documentation*. 2024.
    https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html
    \[MI300X architecture overview\]

14. Naffziger, Samuel, et al. \"AMD Chiplet Architecture for
    High-Performance Server and Desktop Products.\" *2021 IEEE
    International Solid-State Circuits Conference (ISSCC)*. IEEE, 2021.
    DOI: 10.1109/ISSCC42613.2021.9365796 \[Infinity Fabric and chiplet
    coordination\]

### Intel Habana Gaudi

15. Intel Corporation. \"Intel Gaudi 2 AI Accelerator White
    Paper.\" 2023. \[RDMA integration with AI accelerator\]

16. Dally, William J., et al. \"Evolution of the Graphics Processing
    Unit (GPU).\" *IEEE Micro* 41.6 (2021): 42-51. DOI:
    10.1109/MM.2021.3113475 \[Accelerator architecture trends\]

### Apple Neural Engine and Unified Memory

17. Apple Inc. \"Apple M1 Pro and M1 Max: Technical Overview.\" 2021.
    \[Unified memory architecture\]

18. Apple Inc. \"Optimizing GPU Performance.\" *Metal Programming
    Guide*. 2024. \[Memory management best practices\]

### Page Fault Handling and Prefetching

19. Ganguly, Debashis, et al. \"Adaptive page migration for irregular
    data-intensive applications on heterogeneous systems.\" *2020 IEEE
    International Parallel and Distributed Processing Symposium
    (IPDPS)*. IEEE, 2020. DOI: 10.1109/IPDPS47924.2020.00074 \[Page
    migration strategies\]

20. Young, Vinson, et al. \"Combining HW/SW mechanisms to improve NUMA
    performance of multi-GPU systems.\" *2018 51st Annual IEEE/ACM
    International Symposium on Microarchitecture (MICRO)*. IEEE, 2018.
    DOI: 10.1109/MICRO.2018.00022 \[Prefetching for GPU UVM\]

### TLB Optimization

21. Cox, Russ and William Josephson. \"Optimizing network virtualization
    in Xen.\" *USENIX Annual Technical Conference*. 2006. \[TLB
    shootdown optimization techniques\]

22. Yaniv, Avi and Dan Tsafrir. \"Hash, Don\'t Cache (the Page Table).\"
    *Proceedings of the 2016 ACM SIGMETRICS International Conference on
    Measurement and Modeling of Computer Science*. ACM, 2016. DOI:
    10.1145/2896377.2901456 \[Alternative approaches to TLB\]

### Performance Analysis Tools

23. NVIDIA Corporation. \"Nsight Compute Documentation.\" Version
    2024.1. https://docs.nvidia.com/nsight-compute/ \[TLB profiling on
    NVIDIA GPUs\]

24. Brendan Gregg. *BPF Performance Tools*. Addison-Wesley
    Professional, 2019. ISBN: 978-0-13-655482-0. Chapter 8: \"Memory.\"
    \[Linux memory profiling including huge pages\]

### Hardware Specifications

25. Intel Corporation. *Intel® 64 and IA-32 Architectures Software
    Developer\'s Manual, Volume 3A: System Programming Guide*. Order
    Number: 325384-084US. 2024. \[x86-64 page table formats\]

26. ARM Limited. *ARM Architecture Reference Manual ARMv8*. ARM DDI
    0487J.a. 2024. \[ARM64 page table structures\]

27. JEDEC. \"High Bandwidth Memory (HBM3) JESD238A.\" 2023. \[HBM memory
    specifications\]

28. PCI-SIG. \"PCI Express Base Specification Revision 6.0.\" 2022.
    \[PCIe specifications and Address Translation Services\]

------------------------------------------------------------------------

This chapter explored virtual memory management across the spectrum of
AI/ML accelerators, from Google\'s TPU (which eliminates the MMU
entirely) to NVIDIA and AMD GPUs (which implement full MMU
functionality) to hybrid approaches like Intel Habana (selective virtual
memory). The key insight: virtual memory trades flexibility for
overhead, and that trade-off shifts dramatically with workload
characteristics. For predictable inference workloads, Google\'s no-MMU
approach delivers 10-20% efficiency gains. For general-purpose training
across variable batch sizes and model architectures, full virtual memory
becomes mandatory despite its costs. The optimal design point depends on
workload predictability, model size, and multi-device scaling
requirements---there is no universal best answer, only carefully
considered trade-offs.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
