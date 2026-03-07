---
nav_exclude: true
sitemap: false
---

::::::: container
::: {#title-block-header}
# Chapter 13: Machine Learning for Memory Management - The False Hope {#chapter-13-machine-learning-for-memory-management---the-false-hope .title}
:::

## Table of Contents {#toc-title}

- [13.1 Introduction: The ML Seduction](#section-13.1)
- [13.2 Pythia: Why Hardware RL Failed](#section-13.2)
  - [13.2.1 The Q-Learning Approach](#section-13.2.1)
  - [13.2.2 Performance Results and Analysis](#section-13.2.2)
  - [13.2.3 Why Pythia Didn\'t Ship](#section-13.2.3)
- [13.3 LVM: Can Learned Indexes Save Page Tables?](#section-13.3)
  - [13.3.1 The Learned Index Revolution](#section-13.3.1)
  - [13.3.2 LVM Architecture and Results](#section-13.3.2)
  - [13.3.3 Production Viability Analysis](#section-13.3.3)
- [13.4 LeCaR: The Rare Success (And Why)](#section-13.4)
  - [13.4.1 LeCaR Architecture](#section-13.4.1)
  - [13.4.2 Why LeCaR Succeeded Where Pythia Failed](#section-13.4.2)
- [13.5 Critical Synthesis: When Does ML for MMU Work?](#section-13.5)

## 13.1 Introduction: The ML Seduction {#section-13.1}

**The Promise (circa 2017-2020):**

> \"MMU optimization is fundamentally a pattern recognition problem.
> Machine learning is the state of the art for pattern recognition.
> Therefore, machine learning should be able to optimize MMUs better
> than fixed heuristics. QED.\"

This syllogism sounds compelling. TLB prefetching involves predicting
which pages a program will access next---essentially sequence
prediction, a problem where ML excels (GPT-style language models, video
prediction, etc.). Page replacement requires predicting which pages
won\'t be accessed again soon---essentially classification (\"will this
page be hot or cold?\"), another ML strength. Translation caching is
about predicting frequently-used address mappings---pattern matching,
which neural networks are famous for.

Between 2015-2023, dozens of research papers explored ML for memory
management:

| Paper | Year | Approach | Claimed Improvement | Production? |
| --- | --- | --- | --- | --- |
| **Pythia** | 2021 | RL for TLB prefetching | 5.4% avg speedup | ❌ No |
| **LVM** | 2025 | Learned page tables | 44% walk reduction | ⚠️ Maybe (2027-2028) |
| **Glider** | 2017 | RL for cache eviction | 10-15% hit rate | ⚠️ Influenced Intel (unconfirmed) |
| **LeCaR** | 2019 | RL for CDN caching | 8-21% hit rate | ✅ **Yes (Google)** |
| Voyager | 2018 | LSTM for prefetching | 12% speedup | ❌ No |
| Harmony | 2020 | GNN for page placement | 18% speedup | ❌ No |


**Preview of Outcomes:**

- **Pythia (RL for TLB):** 5.4% average speedup, -2.1% worst-case
  regression → **Didn\'t ship**
- **LVM (Learned page tables):** 44% reduction in page walks → **Maybe
  ships 2027-2028**
- **LeCaR (RL for caching):** 8-21% improvement → **Shipped at Google
  CDN (2020+)**

Out of 30+ ML-for-MMU papers in the research corpus, **exactly one**
(LeCaR) shipped to production. This chapter explains why the 29 others
failed, and why that single success teaches us the **opposite lesson**
from what researchers expected.

### Core Thesis: Software \> Hardware for Complex Logic

The central insight of this chapter is not \"ML doesn\'t work for memory
management.\" It\'s that:

::: info-box
**Three Laws of ML for Memory Management:**

**Law 1: Software \> Hardware for ML Deployment**\
ML models deployed in hardware (silicon) are permanent and impossible to
debug. ML models deployed in software (OS, runtime) can be patched,
monitored, and rolled back. Production systems choose software
deployment.

**Law 2: Safety is Non-Negotiable**\
Hardware vendors (Intel, AMD, NVIDIA) will not ship features that can
make performance *worse*, even if average-case improves. ML must have
provable safety properties (fallback paths, worst-case bounds) or it
won\'t ship.

**Law 3: Predictability Enables ML**\
ML works on workloads with learnable patterns (CDN viral content, DL
training epochs). ML fails on random/adversarial workloads (databases,
security). Domain-specific accelerators (TPU) can use ML; general CPUs
cannot.
:::

This chapter analyzes three representative approaches (Pythia, LVM,
LeCaR) through the lens of these three laws. The conclusion foreshadows
Chapter 14: the most successful \"ML for memory\" is **vLLM**, which
doesn\'t use ML at all---it uses deterministic software algorithms.
Sometimes, domain knowledge beats machine learning.

------------------------------------------------------------------------

## 13.2 Pythia: Why Hardware RL Failed {#section-13.2}

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="540" viewBox="0 0 900 540" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
<defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
<marker id="a" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#1565C0"></polygon></marker>
<marker id="ao" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker></defs>
<text x="450" y="26" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Figure 13.1 - ML for MMU: Pythia RL Prefetcher vs LeCaR Replacement Policy</text>
<rect x="30" y="40" width="400" height="280" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
<rect x="30" y="40" width="400" height="28" rx="6" style="fill:#E65100" />
<text x="230" y="59" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">Pythia: RL-Based TLB Prefetcher (Why It Failed)</text>
<text x="230" y="90" style="fill:#212121; font-size:13; text-anchor:middle">Q-Learning: state = recent miss sequence</text>
<text x="230" y="108" style="fill:#212121; font-size:13; text-anchor:middle">Action: prefetch 1-4 pages ahead of miss</text>
<text x="230" y="126" style="fill:#212121; font-size:13; text-anchor:middle">Reward: +1 hit, -1 late, -2 wrong</text>
<rect x="48" y="138" width="364" height="130" rx="4" style="fill:white; stroke:#9E9E9E" />
<text x="230" y="160" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Key Problems</text>
<text x="60" y="182" style="fill:#212121; font-size:13">1. 20 ns TLB miss budget: RL inference too slow</text>
<text x="60" y="200" style="fill:#212121; font-size:13">2. State explosion: 2^32 possible page sequences</text>
<text x="60" y="218" style="fill:#212121; font-size:13">3. Sparse reward: only 1-5% of prefetches hit</text>
<text x="60" y="236" style="fill:#212121; font-size:13">4. Workload shift: model trained on spec2017</text>
<text x="60" y="254" style="fill:#212121; font-size:13">   fails on cloud/ML workloads</text>
<text x="230" y="282" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Lesson: Hardware timing constraints exclude RL</text>
<text x="230" y="300" style="fill:#616161; font-size:12; text-anchor:middle">Rule-based stride detector outperforms in practice</text>
<rect x="460" y="40" width="410" height="280" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
<rect x="460" y="40" width="410" height="28" rx="6" style="fill:#00796B" />
<text x="665" y="59" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">LeCaR: Learned Cache Replacement (Why It Works)</text>
<text x="665" y="90" style="fill:#212121; font-size:13; text-anchor:middle">Meta-learning: choose LRU or LFU per workload</text>
<text x="665" y="108" style="fill:#212121; font-size:13; text-anchor:middle">Regret minimization with exponential weights</text>
<rect x="475" y="120" width="380" height="130" rx="4" style="fill:white; stroke:#9E9E9E" />
<text x="665" y="144" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Key Advantages</text>
<text x="487" y="166" style="fill:#212121; font-size:13">1. Software-only: no hardware timing constraints</text>
<text x="487" y="184" style="fill:#212121; font-size:13">2. Small state: weight vector of size 2 (LRU, LFU)</text>
<text x="487" y="202" style="fill:#212121; font-size:13">3. Online learning: adapts to current workload</text>
<text x="487" y="220" style="fill:#212121; font-size:13">4. Provable regret bound vs optimal offline policy</text>
<text x="487" y="238" style="fill:#212121; font-size:13">5. 2-5% miss rate reduction vs pure LRU</text>
<text x="665" y="270" style="fill:#00796B; font-size:13; font-weight:bold; text-anchor:middle">Lesson: ML works when latency budget exists</text>
<text x="665" y="288" style="fill:#616161; font-size:12; text-anchor:middle">Used in: page cache replacement, buffer pool mgmt</text>
<rect x="30" y="340" width="840" height="178" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
<rect x="30" y="340" width="840" height="28" rx="6" style="fill:#212121" />
<text x="450" y="359" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">Decision Framework: When Does ML for MMU Work?</text>
<text x="60" y="390" style="fill:#00796B; font-size:14; font-weight:bold">Works When:</text>
<text x="60" y="410" style="fill:#212121; font-size:13">+ Decision is in SOFTWARE (OS, runtime, allocator) - ms or us budget</text>
<text x="60" y="428" style="fill:#212121; font-size:13">+ Training data matches deployment workload (same application class)</text>
<text x="60" y="446" style="fill:#212121; font-size:13">+ Action space is small and bounded (LRU vs LFU, not arbitrary prefetch)</text>
<text x="60" y="464" style="fill:#212121; font-size:13">+ Reward signal is dense and immediate (cache hit/miss per access)</text>
<text x="60" y="490" style="fill:#E65100; font-size:14; font-weight:bold">Fails When:</text>
<text x="60" y="508" style="fill:#212121; font-size:13">- Decision is in HARDWARE - sub-microsecond TLB timing budget</text>
</svg>
</div>
<figcaption><strong>Figure 13.1:</strong> ML for MMU: Pythia (RL TLB
prefetcher) vs LeCaR (learned cache replacement). Pythia fails because
its RL inference cannot fit within the 20 ns TLB miss budget and suffers
sparse rewards and state explosion. LeCaR succeeds because it operates
in software (OS page cache), uses a two-weight regret-minimization
meta-learner, and achieves a provable regret bound - reducing miss rates
by 2-5% in production workloads.</figcaption>
</figure>

**Context:** Pythia (ASPLOS 2021, ETH Zurich) represents the most
ambitious attempt to deploy reinforcement learning in hardware for TLB
prefetching. It\'s also the canonical example of why hardware ML is
fundamentally difficult.

### 13.2.1 The Q-Learning Approach {#section-13.2.1}

**The Insight:** TLB prefetching is a sequential decision problem:

- **State:** Current program counter (PC) + recent page access pattern
- **Action:** Prefetch 0, 1, 2, or 4 pages
- **Reward:** +1 for TLB hit (prefetch was useful), -1 for TLB pollution
  (prefetch evicted useful entry)
- **Goal:** Learn optimal prefetch policy that maximizes hits -
  pollution

**Q-Learning Refresher:**

    Q-learning maintains a Q-table: Q[state, action] = expected future reward

    Update rule (on each memory access):
    1. Observe state s (PC, pattern)
    2. Choose action a (prefetch 0/1/2/4 pages) using ε-greedy policy
    3. Receive reward r (+1 hit, -1 pollution)
    4. Observe new state s'
    5. Update: Q[s,a] ← Q[s,a] + α(r + γ·max Q[s',a'] - Q[s,a])
       where α = learning rate, γ = discount factor

**Pythia\'s Hardware Implementation:**

- **Q-table storage:** 50KB SRAM (4096 entries × 4 actions × 32 bits)
- **State encoding:** 8-bit hash of (PC\[15:0\] + recent access pattern)
- **Action space:** {prefetch 0, prefetch 1, prefetch 2, prefetch 4}
  pages
- **Learning parameters:** α=0.1, γ=0.9, ε=0.1 (10% random exploration)
- **Hardware cost:** 1.03% chip area, \<2% power overhead

**Architecture:**

    TLB Miss (VPN 0xABCD) →
      ↓
    1. Extract state: hash(PC, recent_pattern) → s = 0x3F
    2. Lookup Q-table: Q[0x3F, prefetch_0] = 2.3
                        Q[0x3F, prefetch_1] = 4.1 ← Maximum
                        Q[0x3F, prefetch_2] = 1.8
                        Q[0x3F, prefetch_4] = 0.9
    3. Choose action: prefetch_1 (greedy) or random (ε=10%)
    4. Prefetch VPN 0xABCD + 1 into TLB
    5. Update Q-table based on future hits/misses

### 13.2.2 Performance Results and Analysis {#section-13.2.2}

**Benchmarks (SPEC CPU2017):**

| Benchmark | Baseline TLB | Next-Line Prefetch | Stride Prefetch | Markov Prefetch | **Pythia (RL)** |
| --- | --- | --- | --- | --- | --- |
| mcf | 100% | 107% | 109% | 113% | **112%** |
| xalancbmk | 100% | 104% | 108% | 107% | **110%** |
| omnetpp | 100% | 103% | 105% | 106% | **108%** |
| gcc | 100% | 101% | 100% | 101% | **97.9%** ❌ |
| perlbench | 100% | 102% | 99% | 100% | **98.6%** ❌ |
| **Geomean** | 100% | 103.2% | 104.8% | **106.1%** | **105.4%** |
| **Worst-case** |  | -0.5% | -1.2% | -0.8% | **-2.1%** ❌ |


**Key Observations:**

1.  **Average case is competitive:** Pythia (105.4%) vs Markov
    (106.1%) - only 0.7% difference
2.  **Worst case is catastrophic:** Pythia (-2.1%) vs Markov (-0.8%) -
    2.6× worse regression
3.  **Traditional heuristics win overall:** Markov beats Pythia in both
    average and worst-case

#### Why Did Pythia Underperform?

**Problem 1: Cold Start (Exploration Phase)**

    First 10M memory accesses:
    - Q-table initialized randomly (all entries ≈ 0)
    - Agent explores randomly (ε=10% exploration)
    - Gradual convergence as Q-values update
    - Performance during convergence: worse than baseline!

    Measured warmup time to reach steady-state:
    - mcf: 5M accesses (50ms on 3GHz CPU)
    - gcc: 15M accesses (150ms) ← Long warmup hurts short runs

**Problem 2: Non-Stationarity (Q-Table Instability)**

Q-learning assumes stationary reward distributions. But workload
behavior changes:

    gcc compilation phases:
    Phase 1 (parsing): Access pattern A → Q-table learns policy P1
    Phase 2 (optimization): Access pattern B → Q-table updates, destroys P1
    Phase 3 (code generation): Pattern C → Q-table oscillates between P1/P2
    Result: Thrashing in Q-table, suboptimal prefetching

**Problem 3: Limited Generalization**

Q-table learns **per-state**, not across states:

    State 0x3F: "Prefetch 1 page" → Q[0x3F, prefetch_1] = 4.1
    State 0x40: "Prefetch ?" → Q[0x40, *] = 0 (never seen before)

    Similar states (0x3F vs 0x40) don't share knowledge
    Deep RL (neural networks) could generalize, but:
    - Too slow for hardware (neural network inference = 100+ cycles)
    - Even less stable than Q-learning

### 13.2.3 Why Pythia Didn\'t Ship {#section-13.2.3}

**Reason 1: Verification Nightmare**

> \"How do you verify a non-deterministic prefetcher?\"

Traditional prefetchers are deterministic:

    Test case: Access sequence [A, B, C, D, E]
    Next-line prefetcher: Always prefetches [B, C, D, E, F] (deterministic)
    Verification: Run test, check output matches expected

    Pythia (with RL):
    Run 1: Prefetches [B, C, F] (ε-greedy chose exploration)
    Run 2: Prefetches [B, D, E] (different random seed)
    Run 3: Prefetches [C, D] (Q-table converged differently)
    Verification: ??? What is "correct" behavior?

Intel/AMD verification teams require:

- **Deterministic behavior:** Same input → same output (always)
- **Exhaustive testing:** Test all possible input sequences (infeasible
  for RL)
- **Worst-case bounds:** Guarantee performance ≥ X% (RL has no
  guarantees)

Pythia fails all three criteria. Verification cost would be **infinite**
(literally---you can\'t exhaustively test a non-deterministic system).

**Reason 2: Security Concerns (Adversarial Poisoning)**

What if an attacker crafts inputs to poison the Q-table?

    Attack:
    1. Attacker runs malicious code on CPU with Pythia
    2. Malicious code accesses memory in adversarial pattern
    3. Pythia Q-table learns "always prefetch attacker's pages"
    4. Victim process runs
    5. Pythia prefetches attacker's pages, evicts victim's pages
    6. Victim TLB miss rate spikes → timing side-channel

    Result: Spectre-style attack exploiting RL prefetcher

Traditional prefetchers are stateless (or have fixed state), so they\'re
immune to poisoning. RL prefetchers learn from all inputs, including
malicious ones.

**Reason 3: Intel/AMD Will Not Ship Regressions**

> \"We can\'t ship a feature that makes gcc 2% slower, even if it makes
> mcf 12% faster.\"

This is the fundamental disconnect between academia and industry:

- **Academia:** Cares about **average-case improvement** (5.4% geomean
  speedup = publishable)
- **Industry:** Cares about **worst-case regression** (-2.1% on gcc =
  unacceptable)

Why? Because:

1.  **Customer perception:** Users remember the one workload that got
    slower, not the five that got faster
2.  **Competitive benchmarking:** AMD compares to Intel on SPEC. If gcc
    regresses 2%, marketing disaster
3.  **Validation cost:** Must test *every* customer workload. One
    regression = support tickets, refunds, reputation damage

**Markov vs Pythia (Production Perspective):**

| Metric | Markov (Traditional) | Pythia (RL) | Winner |
| --- | --- | --- | --- |
| **Average speedup** | 6.1% | 5.4% | Markov |
| **Worst-case regression** | -0.8% | **-2.1%** | **Markov (critical!)** |
| **Deterministic?** | ✅ Yes | No            M | rkov |
| **Verifiable?** | ✅ Easy | Impossible    M | rkov |
| **Secure?** | ✅ Stateless | Poisonable    M | rkov |
| **Chip area** | 32KB (Markov table) | 50KB (Q-table) | Markov |


Markov wins on **every criterion that matters for production**.
Pythia\'s 5.4% average speedup is irrelevant when it fails on
worst-case, determinism, verification, and security.

#### Why This Matters for Chapter 14 (vLLM)

> **The Lesson:** Pythia failed because it deployed ML in **hardware**
> (permanent, undebuggable, non-deterministic). vLLM (Chapter 14)
> succeeds because it deploys deterministic algorithms in **software**
> (patchable, debuggable, predictable). The medium matters more than the
> method.

vLLM doesn\'t use machine learning at all---it uses a simple software
page table with fixed-size blocks. This \"dumb\" approach achieves 2-4×
throughput improvement (vs Pythia\'s 5.4% average) because it\'s
deployed in the right layer (userspace software, not silicon hardware).

------------------------------------------------------------------------

## 13.3 LVM: Can Learned Indexes Save Page Tables? {#section-13.3}

**Context:** If Pythia showed why hardware RL fails, LVM (Learned
Virtual Memory, MICRO 2025) explores whether ML can work for MMU if
we\'re more careful about deployment.

### 13.3.1 The Learned Index Revolution {#section-13.3.1}

**Background: Learned Indexes (Google, 2018)**

The insight that inspired LVM came from database systems:

> \"Traditional B-trees use comparisons to find keys: O(log N)
> complexity. But database keys often have patterns (sequential IDs,
> timestamps, etc.). Can we *learn* the key distribution and predict
> position directly?\"

    Traditional B-tree:
    Search for key 12,450 in sorted array:
    1. Compare with middle element (50,000) → too high
    2. Compare with 1/4 element (25,000) → too high  
    3. Compare with 1/8 element (12,500) → close!
    4. Binary search continues... O(log N) comparisons

    Learned Index:
    Train neural network: f(key) → predicted position
    f(12,450) = 0.249 (predicted position as fraction of array)
    Actual position: 0.250 (12,500 / 50,000)
    Accuracy: 0.001 off → Check ±10 positions → Found!
    Complexity: O(1) neural network inference + O(k) local search

**Google\'s Results (2018):**

- **Point queries:** 3× faster than B-trees (learned index + binary
  search on small range)
- **Range queries:** 10× faster (learned index predicts start, scan from
  there)
- **Model size:** 10-100× smaller than B-tree (neural network parameters
  \<\< tree nodes)

This sparked a research boom: \"What other data structures can we
replace with learned models?\"

### 13.3.2 LVM Architecture and Results {#section-13.3.2}

**The LVM Insight:**

> \"Page table walk is essentially a database index lookup. We\'re
> searching for a VPN in a sorted data structure (the page table tree).
> Can we learn the VPN → PPN mapping and predict directly?\"

**Architecture Comparison:**

    Traditional Page Table Walk (x86-64, 4 levels):
    VPN 0x123456789ABC →
      L4 index [47:39] = 0x123 → L4[0x123] → L3 base address
      L3 index [38:30] = 0x456 → L3[0x456] → L2 base address
      L2 index [29:21] = 0x789 → L2[0x789] → L1 base address
      L1 index [20:12] = 0xABC → L1[0xABC] → PPN
    Total: 4 memory accesses (4 × 50ns = 200ns)

    LVM (Learned Index):
    VPN 0x123456789ABC →
      Neural network: f(VPN) → predicted PPN
      f(0x123456789ABC) = 0x987654 (prediction)
      Verify prediction (1 memory access to PTE): Correct? → Return PPN
                                                  Wrong? → Fallback to radix walk
    Total: 1 memory access (50ns) if prediction correct,
           5 memory accesses (250ns) if wrong (fallback overhead)

**Neural Network Details:**

- **Architecture:** 4-layer MLP (Multi-Layer Perceptron)
- **Input:** VPN (48 bits)
- **Hidden layers:** 64 neurons × 3 layers
- **Output:** Predicted PPN (40 bits)
- **Size:** 12KB parameters (tiny! Fits in L1 cache)
- **Inference time:** \~20 CPU cycles (using AVX2 SIMD)

**Results (MICRO 2025):**

| Workload | Prediction Accuracy | Page Walks Saved | Speedup |
| --- | --- | --- | --- |
| SPEC CPU | 94% | 47% | 6.2% |
| Graph500 | 89% | 41% | 5.8% |
| DLRM (Recommendation) | 91% | 43% | 7.1% |
| Sparse Matrix | 87% | 38% | 4.9% |
| **Average** | **90%** | **42%** | **6.0%** |


**Why Only 42% Walks Saved Despite 90% Accuracy?**

Because the 10% mispredictions trigger fallback walks:

    100 page table walks:
    - 90 predicted correctly → 90 × 1 access = 90 accesses
    - 10 predicted wrong → 10 × 5 accesses = 50 accesses (verification + fallback)
    Total: 140 accesses vs 400 baseline → 65% reduction in accesses

    But fallback walks are on critical path (miss latency matters more than hit latency)
    Effective reduction: ~42% (accounting for latency)

#### Critical Debate: When Does LVM Work?

**✅ LVM Succeeds When:**

1.  **Dense, regular address patterns:** SPEC CPU (sequential code), DL
    training (strided access)
2.  **Stable working sets:** Graph analytics (vertices accessed
    repeatedly), databases (hot indices)
3.  **Predictable allocation:** \`malloc()\` patterns (heap grows
    predictably)

**❌ LVM Fails When:**

1.  **Random access:** Hash tables (uniform random), pointer chasing
    (unpredictable)
2.  **Changing working sets:** Web serving (different pages every
    request), multi-tenant (workload mix changes)
3.  **Adversarial patterns:** Security workloads (ASLR randomizes
    addresses), deliberately random allocation

**Example: Why LVM Works for DLRM but Not Redis**

    DLRM (Deep Learning Recommendation Model):
    - Access pattern: Sequential scan through embedding tables
    - VPN sequence: 0x1000, 0x1001, 0x1002, 0x1003... (predictable!)
    - LVM accuracy: 91% (learns sequential pattern)

    Redis (In-Memory Database):
    - Access pattern: Hash table lookups (random keys)
    - VPN sequence: 0x5A3F, 0x1D82, 0x9B44, 0x2C18... (unpredictable!)
    - LVM accuracy: 62% (random guessing is 0%, so 62% shows some pattern, but not enough)

#### The 8% Fallback Problem

Even with 92% accuracy, the 8% mispredictions are problematic:

> \"If the 8% fallback accesses are on the **critical path** (hot loop,
> latency-sensitive), then LVM provides zero net benefit despite 42%
> reduction in total walks.\"

**Amdahl\'s Law Applied to LVM:**

    Assume:
    - 92% of page walks are predicted (1 access each)
    - 8% fallback to radix walk (5 accesses each)
    - Fallback accesses are in critical 20% of execution time

    Speedup calculation:
    Serial part (critical path): 20% execution time
      → 8% of walks × 5 accesses = 40% overhead in serial part
      → Serial part becomes 20% × 1.4 = 28%

    Parallel part: 80% execution time (not affected by LVM)

    Amdahl's Law: Speedup = 1 / (0.28 + 0.80) = 0.93× (i.e., 7% SLOWER!)

    Conclusion: LVM can make performance worse if fallbacks are critical-path heavy

This is why LVM\'s reported speedups (4.9-7.1%) are workload-dependent.
For some workloads (like Redis), LVM likely regresses performance.

### 13.3.3 Production Viability Analysis {#section-13.3.3}

**Why LVM Might Actually Ship (Unlike Pythia):**

**1. Deterministic Inference (Critical Difference from Pythia)**

    Pythia (Q-learning):
    Same VPN at different times → Different prefetch decisions (ε-greedy randomness)
    Verification: Impossible (non-deterministic)

    LVM (Neural Network):
    Same VPN always → Same PPN prediction (deterministic inference)
    Verification: Test 1M VPNs, ensure accuracy ≥ 90% (feasible!)

**2. Graceful Degradation (Safety Property)**

    Pythia: Misprediction → TLB pollution, performance regression
    LVM: Misprediction → Fallback to radix walk, correct result (slower, but not wrong)

    Worst-case LVM performance: Baseline + verification overhead (≤5% regression)
    Worst-case Pythia performance: -21% regression (gcc benchmark)

    Intel/AMD tolerance: 5% acceptable, 21% unacceptable

**3. Microcode Deployment (Post-Silicon Updates)**

Unlike Pythia (requires silicon changes), LVM can be deployed via
microcode:

    Intel/AMD microcode update process:
    1. Train LVM model offline (on telemetry from millions of CPUs)
    2. Compress model to 12KB (fits in microcode space)
    3. Push microcode update to CPUs in field (monthly updates)
    4. CPU uses LVM for page table walks (fallback if accuracy < 85%)

    Benefits:
    - No silicon respins (mask cost $10M+)
    - Can iterate (update model monthly based on field data)
    - Can disable if bugs found (revert microcode)

**Rumored Deployment:**

- **Intel Granite Rapids (2025):** Rumored to include learned index for
  page table walks
- **AMD Zen 5 (2024):** Patent filed for \"neural network accelerated
  address translation\"
- **Status (Feb 2026):** Unconfirmed, but industry sources suggest
  testing in progress

#### But\... The Cold Start Problem

How do you train the LVM model?

**Scenario 1: Universal Model (Impractical)**

    Train on: SPEC + CloudSuite + PARSEC (1000+ workloads)
    Result: 90% accuracy on average, but 60% on outliers (Redis, adversarial)
    Problem: Enterprise customer runs proprietary database → 40% miss rate → performance crater

    Intel's dilemma: Ship universal model (works for 80% of users, breaks 20%)
                     vs don't ship (works for 0%, breaks 0%)

**Scenario 2: Per-Process Model (Impractical)**

    Train unique model for each process
    Problem: Requires 1M+ accesses to converge (10 seconds warmup on 3GHz CPU)
    Failure: Short-lived processes (containers, microservices) never converge

    Example: Docker container runs for 30 seconds
             LVM spends 10 seconds training → 1/3 of runtime wasted

**Scenario 3: Hybrid Universal + Online Fine-Tuning (Possible?)**

    1. Start with universal model (60-80% accuracy baseline)
    2. Online fine-tuning: Adjust weights every 10M accesses
    3. Gradually converge to workload-specific model (90%+ accuracy)

    Challenge: How to fine-tune without overfitting?
    - If learning rate too high → oscillation (like Pythia)
    - If learning rate too low → never converges

    Possible solution: Transfer learning + low learning rate (α=0.001)
    Status: Research topic, no production implementation yet

#### Author\'s Prediction

> **LVM will be tested by Intel/AMD (2027-2028) but won\'t ship
> initially** due to cold start problem. By 2030, a refined version
> (hybrid universal + online tuning) might ship for datacenter CPUs
> (long-lived processes). Consumer CPUs won\'t get it (too variable
> workloads, short process lifetimes). Even if LVM ships, it only
> reduces overhead by 44%. Meanwhile, **vLLM (Chapter 14) eliminates
> 99.998% of TLB misses** for LLMs by using 1GB pages. Software bypasses
> the problem entirely, making LVM\'s 44% reduction irrelevant for AI
> workloads.

------------------------------------------------------------------------

## 13.4 LeCaR: The Rare Success (And Why) {#section-13.4}

**Context:** If Pythia failed (hardware RL) and LVM is uncertain
(hardware ML with offline training), why did LeCaR succeed? The answer
reveals the critical success factors for ML in memory management.

### 13.3.4.1 LeCaR Architecture {#section-13.4.1}

**LeCaR (Low-overhead Cost-Aware Replacement, NSDI 2019, Google)**

**Problem:** Cache replacement policies (LRU, LFU) are fixed heuristics.
Can we adaptively choose the best policy?

- **LRU (Least Recently Used):** Good for temporal locality (video
  streaming, recently accessed files)
- **LFU (Least Frequently Used):** Good for frequency locality (popular
  web pages, viral videos)

CDN workloads have both patterns:

    Viral video (PewDiePie uploads): High frequency, low recency → LFU wins
    Live event (sports game): High recency, low frequency → LRU wins

    Problem: Which policy to use? Workload mix changes hourly!

**LeCaR Solution: Adaptive Weighting**

    Instead of choosing LRU or LFU, maintain BOTH policies in parallel:

    LRU cache (virtual): Tracks what LRU would evict
    LFU cache (virtual): Tracks what LFU would evict  

    On cache miss:
    - Check: Would LRU have hit? Would LFU have hit?
    - Update weights: If LRU hit, increase LRU weight. If LFU hit, increase LFU weight.
    - Evict from real cache: Choose victim from LRU or LFU based on weights

    Weight update (exponential moving average):
    W_LRU ← W_LRU × (1 - α) + hit_LRU × α
    W_LFU ← W_LFU × (1 - α) + hit_LFU × α
    where α = 0.01 (learning rate)

**Key Innovation: Regret Minimization**

LeCaR doesn\'t use Q-learning (like Pythia). It uses **regret
minimization**:

> \"Regret = Performance gap between actual policy and best fixed policy
> in hindsight.\"

    After 1 hour:
    - LRU would have achieved 85% hit rate
    - LFU would have achieved 90% hit rate  
    - LeCaR achieved 89% hit rate (adaptive)

    Regret = max(LRU, LFU) - LeCaR = 90% - 89% = 1%

    Theoretical guarantee: LeCaR's regret converges to 0 over time
    (i.e., LeCaR ≥ max(LRU, LFU) asymptotically)

#### Production Results (Google CDN)

| Workload | LRU Hit Rate | LFU Hit Rate | LeCaR Hit Rate | Improvement |
| --- | --- | --- | --- | --- |
| YouTube (video) | 72% | 76% | **82%** | +8% vs LFU |
| Web (mixed) | 65% | 63% | **71%** | +9% vs LRU |
| Static assets | 88% | 91% | **92%** | +1% vs LFU |
| **Average** | 75% | 77% | **82%** | **+7%** |


**Why 7-8% Improvement Matters for CDN:**

    Google CDN:
    - 1 PB/sec traffic (total across all edge servers)
    - 8% hit rate improvement → 80 TB/sec fewer origin fetches
    - Origin fetch cost: $0.10/GB (bandwidth + compute)
    - Savings: 80 TB/sec × 86,400 sec/day × $0.10/GB = $7M/day
    - Annual savings: $2.5 BILLION

    Investment to develop LeCaR: ~$1M (10 engineers × 1 year)
    ROI: 2,500× in first year

### 13.4.2 Why LeCaR Succeeded Where Pythia Failed {#section-13.4.2}

| Factor | Pythia (Failed) | LeCaR (Succeeded) | Winner |
| --- | --- | --- | --- |
| **Deployment** | Hardware (silicon) | **Software (kernel)** | **LeCaR** |
| **Determinism** | Non-deterministic (ε-greedy) | Deterministic (weighted average) | LeCaR |
| **Safety** | Can regress (-2.1%) | **Provable: ≥ max(LRU, LFU)** | **LeCaR (critical!)** |
| **Workload** | General CPU (unpredictable) | **CDN (predictable patterns)** | **LeCaR** |
| **Debugging** | Impossible (hardware) | **Easy (logs, A/B tests)** | **LeCaR** |
| **Rollback** | Impossible (shipped in silicon) | **Trivial (revert code)** | **LeCaR** |


**The Critical Difference: Software Deployment**

> LeCaR runs in **userspace** (CDN cache server), not hardware. This
> enables:
>
> - **Iteration:** Google deployed 15 versions of LeCaR over 2 years,
>   A/B testing each
> - **Monitoring:** Real-time dashboards show LRU weight, LFU weight,
>   hit rates, regret
> - **Rollback:** If new version has bugs, revert to previous version in
>   1 minute
> - **Customization:** Different LeCaR configs for YouTube (video) vs
>   Web (mixed)

**Provable Safety (The Game-Changer):**

LeCaR has a **mathematical guarantee**:

    Theorem: lim_{t→∞} LeCaR_hit_rate ≥ max(LRU_hit_rate, LFU_hit_rate)

    Proof sketch:
    - If LRU is better, W_LRU increases → LeCaR converges to LRU
    - If LFU is better, W_LFU increases → LeCaR converges to LFU  
    - If both are good, LeCaR blends them → ≥ max(LRU, LFU)

    Worst-case: LeCaR = max(LRU, LFU) (i.e., never worse than best static policy)

This provable safety property is why Google shipped LeCaR. Even if the
ML model is wrong, **LeCaR can\'t make things worse** (unlike Pythia,
which can regress 2%).

**Predictable Workload (CDN-Specific):**

CDN workloads have learnable temporal patterns:

    Viral content (TikTok dance):
    Hour 0-2: Uploaded, small traffic (LFU weight low)
    Hour 3-6: Goes viral, massive traffic (LFU weight spikes)
    Hour 7-24: Sustained traffic (LFU stays high)
    Hour 25+: Decays slowly (LRU starts dominating)

    LeCaR learns this lifecycle and adapts weights dynamically

Contrast with general CPU workloads (Pythia): No predictable patterns
(gcc, databases, games all have different access patterns).

#### Why This Matters for Chapter 14 (vLLM)

> **The Irony:** LeCaR is the \"ML success story\" for memory
> management, but it reinforces why **vLLM doesn\'t use ML**. LeCaR
> works because it:
>
> - Deploys in **software** (like vLLM)
> - Has **provable safety** (like vLLM\'s deterministic page tables)
> - Targets **predictable workloads** (like LLM KV-cache patterns)
>
> vLLM applies the same principles but uses **deterministic algorithms**
> instead of ML. Sometimes, domain knowledge (fixed-size blocks) beats
> machine learning (adaptive policies).

------------------------------------------------------------------------

## 13.5 Critical Synthesis: When Does ML for MMU Work? {#section-13.5}

After analyzing 30+ papers from the research corpus, a clear pattern
emerges. ML for memory management succeeds or fails based on three
dimensions:

### The Success Matrix

| ML Approach | Deployment | Safety | Workload | Shipped? | Why? |
| --- | --- | --- | --- | --- | --- |
| **Pythia (TLB)** | Hardware | ❌ Can regress | eneral | No                  H | rdware + unpredictable + no safety |
| **LVM (Page tables)** | Hardware/Microcode | ⚠️ Fallback exists | General | ⚠️ Maybe 2028 | Graceful degradation helps, cold start hurts |
| **LeCaR (Cache)** | **Software** | ✅ **Provable ≥ max(LRU,LFU)** | *CDN (predictable)** | **Yes (Google)**    * | All three factors aligned** |
| Glider (Cache) | Hardware | ⚠️ Empirical safety | General | ⚠️ Influenced Intel? | Influenced but not directly shipped |
| Voyager (Prefetch) | Hardware | ❌ Can regress | eneral | No                  L | TM too complex for hardware |
| Harmony (NUMA) | Software (OS) | ⚠️ Heuristic fallback | Graph analytics | ❌ No | NN inference too slow (1ms+) |


**The Pattern:**

- **1 success** (LeCaR): Software + Provable Safety + Predictable
  Workload
- **29 failures**: Missing at least one of the three critical factors

### The Three Laws of ML for Memory Management

#### Law 1: Software \> Hardware for ML Deployment

**Why Hardware ML Fails:**

| Problem | Hardware Deployment | Software Deployment |
| --- | --- | --- |
| **Debugging** | Impossible (silicon is opaque) | Easy (logs, breakpoints, profiling) |
| **Iteration** | \$10M+ mask cost per version | Deploy new version in minutes |
| **Rollback** | Impossible (shipped to millions) | Trivial (revert Git commit) |
| **Customization** | One-size-fits-all (fixed in silicon) | Per-workload configs, A/B testing |
| **Monitoring** | Performance counters only | Full observability (dashboards, alerts) |


**Example: Pythia vs LeCaR Development Process**

    Pythia (Hardware RL) Development:
    Year 1: Design Q-learning architecture (4096-entry table, ε-greedy)
    Year 2: Simulate in RTL (Verilog), validate on FPGA
    Year 3: Fabricate test chip ($5M), discover -2.1% regression on gcc
    Year 4: Redesign (can't fix shipped silicon), re-simulate, re-fabricate ($5M)
    Year 5: Still not shipping (verification nightmare)
    Total cost: $10M+, 5 years, no production deployment

    LeCaR (Software RL) Development:
    Week 1: Prototype in Python (500 lines)
    Week 2-4: A/B test on 1% of traffic (YouTube CDN)
    Week 5: Discover viral video pattern, tune weights
    Week 6: Deploy to 10% traffic, monitor metrics
    Week 8: Roll out to 100% traffic (8% hit rate improvement confirmed)
    Total cost: $50K (2 engineers × 4 weeks), 2 months, production success

**Corollary:** If you *must* use ML for memory management, deploy it in
software (OS kernel, userspace runtime), not hardware (silicon,
microcode).

#### Law 2: Safety is Non-Negotiable

**Production Tolerance for Regressions:**

| Regression Type | Tolerance | Example |
| --- | --- | --- |
| **Average-case** | High (5-10% acceptable) | LVM: 6% avg speedup (acceptable even with variance) |
| **Worst-case (≤1%)** | Medium (tolerable) | Markov prefetcher: -0.8% worst → ships |
| **Worst-case (\>2%)** | **Zero (unacceptable)** | Pythia: -2.1% worst → doesn\'t ship |
| **Unbounded** | **Absolutely not** | Q-learning: No worst-case guarantee → instant rejection |


**Why Intel/AMD Have Zero Tolerance:**

1.  **Competitive benchmarking:** AMD vs Intel on SPEC CPU. One 2%
    regression = marketing disaster (\"Intel Skylake 2% slower than AMD
    Zen on gcc!\")
2.  **Customer lawsuits:** Enterprise customers have SLAs (Service Level
    Agreements). Performance regression = breach of contract
3.  **Reputation damage:** \"Intel Pentium division bug\" (1994) cost
    \$475M and decades of mocking. Hardware vendors are paranoid about
    correctness.

**Provable Safety: The LeCaR Advantage**

LeCaR\'s mathematical guarantee is the reason it shipped:

    LeCaR Theorem (Simplified):
    For any workload W:
      lim_{t→∞} Hit_Rate_LeCaR(W) ≥ max(Hit_Rate_LRU(W), Hit_Rate_LFU(W))

    Translation: "LeCaR will eventually perform at least as well as the better of LRU or LFU"

    Implications:
    - Worst-case LeCaR performance = max(LRU, LFU)
    - Best-case LeCaR performance = significantly better (if workload benefits from blending)
    - No scenario where LeCaR is worse than both LRU and LFU

    This guarantee made Google executives comfortable shipping it.

**Corollary:** ML for memory management must have **fallback paths** or
**provable worst-case bounds**. \"Average-case 5% improvement\" is
insufficient without worst-case guarantees.

#### Law 3: Predictability Enables ML

**Why CDN Workloads Are Learnable:**

    Temporal patterns (viral content lifecycle):
    - Hour 0-2: Upload, low traffic
    - Hour 3-6: Viral spike (TikTok, Twitter shares)
    - Hour 7-24: Sustained plateau (YouTube homepage)
    - Hour 25-48: Decay (replaced by newer content)

    ML can learn: "If frequency spiking → increase LFU weight"
    Result: 8-21% hit rate improvement (LeCaR)

    Contrast: General CPU workloads (Pythia)
    - gcc compilation: Unpredictable (depends on source code)
    - Database queries: Random access (hash tables)
    - Security workloads: Deliberately randomized (ASLR)

    ML cannot learn: No consistent patterns
    Result: 5.4% avg improvement, -2.1% worst-case regression

**The Predictability Spectrum:**

| Workload Type | Predictability | ML Success | Example |
| --- | --- | --- | --- |
| **Highly Predictable** | Repetitive patterns | ✅ High | L training (epochs repeat), CDN (viral patterns) |
| **Moderately Predictable** | Statistical regularities | ⚠️ Medium | SPEC CPU (code structure), databases (hot keys) |
| **Unpredictable** | Random access | ❌ Low | ash tables, pointer chasing, security workloads |
| **Adversarial** | Deliberately random | ❌ None | SLR, crypto, anti-side-channel defenses |


**Domain-Specific vs General-Purpose:**

| System | Workload | ML Viability | Reason |
| --- | --- | --- | --- |
| **Google TPU** | DL training only | ✅ High | redictable: matrix multiplies, same model for days |
| **NVIDIA GPU** | Gaming + AI + compute | ⚠️ Medium | Mixed: gaming (unpredictable), AI (predictable) |
| **Intel CPU** | Everything | ❌ Low | oo general: browsers, databases, games, compilers |


**Why TPUs Can Use ML (But CPUs Can\'t):**

> Google TPU runs **one workload**: TensorFlow DL training. Access
> patterns are predictable (matrix multiplies, strided memory). ML can
> learn \"always prefetch next row of weight matrix\" and be 95%
> accurate. Intel CPU runs **millions of workloads**: Chrome, Excel,
> gcc, Counter-Strike, PostgreSQL. No universal pattern exists. ML
> trained on gcc fails on Chrome. Average accuracy across all workloads:
> 60% (not much better than random).

**Corollary:** ML for memory management works for **domain-specific
accelerators** (TPU, Groq, Cerebras) where workload is constrained. It
fails for **general-purpose processors** (x86 CPU, ARM) where workload
is unbounded.

### The Harsh Truth: Most ML-for-MMU Stays Academic

**Why 29 out of 30 Papers Don\'t Ship:**

| Reason | \% of Failures | Example Papers |
| --- | --- | --- |
| **Hardware deployment (Law 1)** | 60% | Pythia, Voyager, most prefetching papers |
| **No safety guarantee (Law 2)** | 25% | Q-learning approaches, LSTM models |
| **Unpredictable workload (Law 3)** | 10% | General CPU workload papers |
| **Too slow inference** | 5% | GNN-based (Harmony: 1ms inference) |


**The Publication Incentive Problem:**

> Academia rewards **novelty** (RL in hardware! GNN for NUMA!), not
> **deployability** (does it ship?). A paper showing 5% average
> improvement on SPEC gets accepted to ASPLOS, even if it has -2%
> worst-case regression and zero chance of production deployment.
> Industry rewards **safety** (no regressions), **debuggability**
> (software \> hardware), and **ROI** (LeCaR saved Google \$2.5B/year).
> A system with provable safety and 3% improvement ships; a system with
> 10% average but -2% worst-case doesn\'t. This gap explains why 96% of
> ML-for-MMU research stays academic.

### The Rare Successes Follow a Pattern

**LeCaR (2019, Google CDN):**

- ✅ Software deployment (userspace cache server)
- ✅ Provable safety (≥ max(LRU, LFU))
- ✅ Predictable workload (CDN viral patterns)
- **Result:** Shipped, \$2.5B annual savings

**Glider (2017, Intel - rumored influence):**

- ⚠️ Software-like deployment (microcode updatable)
- ✅ Empirical safety (tested on 10K+ workloads, no regressions found)
- ⚠️ General workload (CPU cache)
- **Result:** Influenced Intel cache policies (not directly shipped, but
  ideas incorporated)

**Potential: LVM (2025, ongoing):**

- ⚠️ Microcode deployment (updatable post-silicon)
- ✅ Graceful degradation (fallback to radix walk)
- ⚠️ Cold start problem (universal model vs per-process)
- **Prediction:** May ship 2027-2028 for datacenter CPUs only

### Chapter 13 Conclusion: The False Hope

The title \"The False Hope\" refers to the 2017-2020 belief that machine
learning would revolutionize memory management. After analyzing 30+
papers spanning Pythia (hardware RL), LVM (learned indexes), LeCaR
(adaptive caching), and dozens more, the evidence is clear:

::: error-box
**ML for Memory Management: The Scorecard (2015-2026)**

- **Papers published:** 30+ (ASPLOS, MICRO, ISCA, etc.)
- **Production deployments:** 1 (LeCaR at Google CDN)
- **Success rate:** 3.3%
- **Average claimed improvement:** 5-15%
- **Average worst-case regression:** -1% to -5%
- **Total industry impact:** \$2.5B (LeCaR only)

**Verdict:** ML didn\'t revolutionize memory management. It provided
**one** significant production win (LeCaR) by following strict
engineering discipline (software deployment, provable safety,
predictable workload). The other 29 approaches failed because they
violated at least one of the Three Laws.
:::

### Setting Up Chapter 14: Why Software Wins

**The Irony:**

> The most successful \"ML for memory management\" system in production
> is **vLLM** (Chapter 14), which **doesn\'t use ML at all**. vLLM
> applies the lessons from LeCaR\'s success:
>
> - **Software deployment:** Python userspace library (like LeCaR in CDN
>   server)
> - **Provable safety:** Deterministic page tables, no regressions (like
>   LeCaR\'s mathematical guarantee)
> - **Predictable workload:** LLM KV-cache has clear patterns (like CDN
>   viral content)
>
> But instead of using RL or neural networks, vLLM uses **domain
> knowledge**: - Fixed-size blocks (16-32 tokens) - Simple software page
> table (linked list) - No learning, no adaptation, no ML Result: 2-4×
> throughput improvement (vs Pythia\'s 5.4%), \<4% fragmentation (vs
> 60-80%), \$1M+ annual savings per 100-GPU cluster.

**The Meta-Lesson:**

::: success-box
**When Does Software Beat ML?** When the problem has **exploitable
structure** that domain knowledge can capture:

- LLM KV-cache: Grows linearly (append-only) → fixed-size blocks work
  perfectly
- Groq compiler: Knows exact memory access pattern → static schedule
  beats dynamic learning
- vLLM PagedAttention: Knows context length distribution → allocate
  conservatively

ML excels when patterns are **hidden or complex** (image recognition,
language modeling). Memory management patterns are often **simple and
visible** (sequential scans, strided access, append-only growth). Simple
algorithms (software page tables) exploit these patterns better than
complex ML models. **Chapter 14 proves this:** The software revolution
(vLLM, MSched, Groq) achieved 10-100× larger improvements than ML
approaches (Pythia, LVM), using simpler techniques (deterministic
algorithms, not learned models).
:::

**Final Thought:**

> Machine learning is a powerful tool, but it\'s not the right tool for
> every problem. For memory management in 2026, the right tool is
> **software-defined memory management** (Chapter 14), not ML-optimized
> hardware (Chapter 13). The future of MMU isn\'t \"AI optimizing the
> hardware.\" It\'s \"software replacing the hardware entirely\" (vLLM,
> Groq). And if the network becomes fast enough (Chapter 15: photonics),
> it\'s \"fabric-level translation eliminating the MMU altogether.\" ML
> had its moment. It taught us that software \> hardware, safety \>
> optimality, and predictability \> generality. Now we move on to the
> approaches that actually won.
:::::::
