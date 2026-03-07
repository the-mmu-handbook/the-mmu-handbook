---
nav_exclude: true
sitemap: false
---

::: {#title-block-header}
# Chapter 8: Advanced MMU Topics - System Integration and Optimization {#chapter-8-advanced-mmu-topics---system-integration-and-optimization .title}
:::

- [8.5 Page Replacement Algorithms: Making the Eviction
  Decision](#page-replacement-algorithms-making-the-eviction-decision){#toc-page-replacement-algorithms-making-the-eviction-decision}
  - [8.5.1 The Ideal: Bélády\'s MIN
    Algorithm](#the-ideal-béládys-min-algorithm){#toc-the-ideal-béládys-min-algorithm}
  - [8.5.2 LRU: Least Recently
    Used](#lru-least-recently-used){#toc-lru-least-recently-used}
  - [8.5.3 Clock Algorithm: Approximating LRU with A
    Bits](#clock-algorithm-approximating-lru-with-a-bits){#toc-clock-algorithm-approximating-lru-with-a-bits}
  - [8.5.4 Two-List LRU: Active and
    Inactive](#two-list-lru-active-and-inactive){#toc-two-list-lru-active-and-inactive}
  - [8.5.5 Multi-Generational LRU (MGLRU): Modern
    Linux](#multi-generational-lru-mglru-modern-linux){#toc-multi-generational-lru-mglru-modern-linux}
- [8.6 Memory Reclaim: When and How to Free
  Memory](#memory-reclaim-when-and-how-to-free-memory){#toc-memory-reclaim-when-and-how-to-free-memory}
  - [8.6.1 Watermarks: Detecting Memory
    Pressure](#watermarks-detecting-memory-pressure){#toc-watermarks-detecting-memory-pressure}
  - [8.6.2 kswapd: Background Reclaim
    Daemon](#kswapd-background-reclaim-daemon){#toc-kswapd-background-reclaim-daemon}
  - [8.6.3 Direct Reclaim: The Emergency
    Path](#direct-reclaim-the-emergency-path){#toc-direct-reclaim-the-emergency-path}
  - [8.6.4 vm.swappiness: Tuning Reclaim
    Behavior](#vm.swappiness-tuning-reclaim-behavior){#toc-vm.swappiness-tuning-reclaim-behavior}
  - [8.6.5 OOM Killer: The Last
    Resort](#oom-killer-the-last-resort){#toc-oom-killer-the-last-resort}
- [8.7 Page Table Management: The Hidden Memory
  Consumer](#page-table-management-the-hidden-memory-consumer){#toc-page-table-management-the-hidden-memory-consumer}
  - [8.7.1 Page Table Memory
    Overhead](#page-table-memory-overhead){#toc-page-table-memory-overhead}
  - [8.7.2 Lazy Allocation](#lazy-allocation){#toc-lazy-allocation}
  - [8.7.3 Huge Pages: Reducing Page Table
    Overhead](#huge-pages-reducing-page-table-overhead){#toc-huge-pages-reducing-page-table-overhead}
- [8.8 Performance Analysis and
  Tuning](#performance-analysis-and-tuning){#toc-performance-analysis-and-tuning}
  - [8.8.1 Diagnostic Tools](#diagnostic-tools){#toc-diagnostic-tools}
  - [8.8.2 Complete Case Study: Solving the PostgreSQL
    OOM](#complete-case-study-solving-the-postgresql-oom){#toc-complete-case-study-solving-the-postgresql-oom}
- [8.9 Summary: The Complete
  Picture](#summary-the-complete-picture){#toc-summary-the-complete-picture}
  - [The Hardware-Software
    Contract](#the-hardware-software-contract){#toc-the-hardware-software-contract}
  - [Bridging the
    Chapters](#bridging-the-chapters){#toc-bridging-the-chapters}
  - [Practical
    Takeaways](#practical-takeaways){#toc-practical-takeaways}
  - [The Big Picture](#the-big-picture){#toc-the-big-picture}
- [References](#references){#toc-references}
- [8.5 Page Replacement Algorithms: Making the
  Choice](#page-replacement-algorithms-making-the-choice){#toc-page-replacement-algorithms-making-the-choice}
  - [8.5.1 The Ideal: Least Recently Used
    (LRU)](#the-ideal-least-recently-used-lru){#toc-the-ideal-least-recently-used-lru}
  - [8.5.2 Clock Algorithm: Practical LRU
    Approximation](#clock-algorithm-practical-lru-approximation){#toc-clock-algorithm-practical-lru-approximation}
  - [8.5.3 Enhanced Clock: Two
    Lists](#enhanced-clock-two-lists){#toc-enhanced-clock-two-lists}
  - [8.5.4 Multi-Generational LRU (MGLRU): Linux\'s Modern
    Approach](#multi-generational-lru-mglru-linuxs-modern-approach){#toc-multi-generational-lru-mglru-linuxs-modern-approach}
- [8.6 Memory Reclaim: The Timing and
  Urgency](#memory-reclaim-the-timing-and-urgency){#toc-memory-reclaim-the-timing-and-urgency}
  - [8.6.1 Watermarks: Three Levels of
    Urgency](#watermarks-three-levels-of-urgency){#toc-watermarks-three-levels-of-urgency}
  - [8.6.2 kswapd: The Background
    Reclaimer](#kswapd-the-background-reclaimer){#toc-kswapd-the-background-reclaimer}
  - [8.6.3 Direct Reclaim: When kswapd Can\'t Keep
    Up](#direct-reclaim-when-kswapd-cant-keep-up){#toc-direct-reclaim-when-kswapd-cant-keep-up}
  - [8.6.4 vm.swappiness: Balancing Anonymous vs File
    Pages](#vm.swappiness-balancing-anonymous-vs-file-pages){#toc-vm.swappiness-balancing-anonymous-vs-file-pages}
  - [8.6.5 OOM Killer: The Nuclear
    Option](#oom-killer-the-nuclear-option){#toc-oom-killer-the-nuclear-option}
- [8.7 Page Table Management: Metadata
  Memory](#page-table-management-metadata-memory){#toc-page-table-management-metadata-memory}
  - [8.7.1 Calculating Page Table
    Overhead](#calculating-page-table-overhead){#toc-calculating-page-table-overhead}
  - [8.7.2 Lazy Allocation: Saving
    Memory](#lazy-allocation-saving-memory){#toc-lazy-allocation-saving-memory}
  - [8.7.3 Page Table Reclamation Under
    Pressure](#page-table-reclamation-under-pressure){#toc-page-table-reclamation-under-pressure}
  - [8.7.4 Huge Pages: Dramatic Overhead
    Reduction](#huge-pages-dramatic-overhead-reduction){#toc-huge-pages-dramatic-overhead-reduction}
- [8.8 Performance Analysis: Putting It All
  Together](#performance-analysis-putting-it-all-together){#toc-performance-analysis-putting-it-all-together}
  - [8.8.1 The Complete PostgreSQL OOM Case
    Study](#the-complete-postgresql-oom-case-study){#toc-the-complete-postgresql-oom-case-study}
- [8.9 Summary: The Complete
  Picture](#summary-the-complete-picture-1){#toc-summary-the-complete-picture-1}
  - [The Hardware-Software
    Contract](#the-hardware-software-contract-1){#toc-the-hardware-software-contract-1}
  - [Key Insights
    Revisited](#key-insights-revisited){#toc-key-insights-revisited}
  - [Bridging All
    Chapters](#bridging-all-chapters){#toc-bridging-all-chapters}
  - [Practical Takeaways by
    Role](#practical-takeaways-by-role){#toc-practical-takeaways-by-role}
  - [The Bigger Picture](#the-bigger-picture){#toc-the-bigger-picture}
- [References](#references-1){#toc-references-1}
- [8.5 Page Replacement Algorithms: From Theory to
  Practice](#page-replacement-algorithms-from-theory-to-practice){#toc-page-replacement-algorithms-from-theory-to-practice}
  - [8.5.1 The Ideal: Perfect
    LRU](#the-ideal-perfect-lru){#toc-the-ideal-perfect-lru}
  - [8.5.2 Clock Algorithm: Practical LRU
    Approximation](#clock-algorithm-practical-lru-approximation-1){#toc-clock-algorithm-practical-lru-approximation-1}
  - [8.5.3 Two-Handed Clock: Considering
    Cleanliness](#two-handed-clock-considering-cleanliness){#toc-two-handed-clock-considering-cleanliness}
  - [8.5.4 Multi-Generational LRU (MGLRU): Modern
    Sophistication](#multi-generational-lru-mglru-modern-sophistication){#toc-multi-generational-lru-mglru-modern-sophistication}
- [8.6 Memory Reclaim: When and How to Free
  Pages](#memory-reclaim-when-and-how-to-free-pages){#toc-memory-reclaim-when-and-how-to-free-pages}
  - [8.6.1 Watermarks: Detecting Memory
    Pressure](#watermarks-detecting-memory-pressure-1){#toc-watermarks-detecting-memory-pressure-1}
  - [8.6.2 kswapd: Background Reclaim
    Daemon](#kswapd-background-reclaim-daemon-1){#toc-kswapd-background-reclaim-daemon-1}
  - [8.6.3 Direct Reclaim: The Emergency
    Path](#direct-reclaim-the-emergency-path-1){#toc-direct-reclaim-the-emergency-path-1}
  - [8.6.4 Swappiness: Tuning Reclaim
    Behavior](#swappiness-tuning-reclaim-behavior){#toc-swappiness-tuning-reclaim-behavior}
  - [8.6.5 OOM Killer: The Last
    Resort](#oom-killer-the-last-resort-1){#toc-oom-killer-the-last-resort-1}
- [8.7 Page Table Management: The
  Meta-Problem](#page-table-management-the-meta-problem){#toc-page-table-management-the-meta-problem}
  - [8.7.1 Page Table Overhead
    Calculations](#page-table-overhead-calculations){#toc-page-table-overhead-calculations}
  - [8.7.2 Lazy Allocation: Avoiding
    Waste](#lazy-allocation-avoiding-waste){#toc-lazy-allocation-avoiding-waste}
  - [8.7.3 Page Table
    Reclamation](#page-table-reclamation){#toc-page-table-reclamation}
  - [8.7.4 Compact vs Sparse
    Layouts](#compact-vs-sparse-layouts){#toc-compact-vs-sparse-layouts}
  - [8.7.5 Huge Pages: The Ultimate
    Optimization](#huge-pages-the-ultimate-optimization){#toc-huge-pages-the-ultimate-optimization}
- [8.8 Performance Analysis and
  Tuning](#performance-analysis-and-tuning-1){#toc-performance-analysis-and-tuning-1}
  - [8.8.1 Essential Profiling
    Tools](#essential-profiling-tools){#toc-essential-profiling-tools}
  - [8.8.2 Common Performance
    Issues](#common-performance-issues){#toc-common-performance-issues}
  - [8.8.3 Tuning
    Parameters](#tuning-parameters){#toc-tuning-parameters}
- [8.9 Conclusion: The Complete
  Picture](#conclusion-the-complete-picture){#toc-conclusion-the-complete-picture}
  - [Integration with Previous
    Chapters](#integration-with-previous-chapters){#toc-integration-with-previous-chapters}
  - [Practical
    Takeaways](#practical-takeaways-1){#toc-practical-takeaways-1}
  - [The Big Picture](#the-big-picture-1){#toc-the-big-picture-1}
  - [References](#references-2){#toc-references-2}

## 8.5 Page Replacement Algorithms: Making the Eviction Decision

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif" style="max-width:100%;height:auto;display:block;margin:0 auto;">
<defs><filter id="sh"><fedropshadow dx="2" dy="3" stddeviation="3" flood-opacity="0.18"></fedropshadow></filter>
<marker id="ao" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#E65100"></polygon></marker>
<marker id="ag" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" style="fill:#00796B"></polygon></marker></defs>
<text x="450" y="26" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Figure 8.2 - Page Replacement: Clock Algorithm and Linux Two-List LRU</text>
<rect x="30" y="40" width="380" height="300" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
<rect x="30" y="40" width="380" height="28" rx="6" style="fill:#1565C0" />
<text x="220" y="59" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">Clock (Second-Chance) Algorithm</text>
<text x="220" y="90" style="fill:#212121; font-size:13; text-anchor:middle">Clock hand sweeps frame list. If A-bit=1: clear it,</text>
<text x="220" y="106" style="fill:#212121; font-size:13; text-anchor:middle">advance. If A-bit=0: evict this frame.</text>
<circle cx="220" cy="210" r="90" style="fill:none; stroke:#9E9E9E; stroke-width:1.5"></circle>
<rect x="280" y="130" width="52" height="30" rx="4" style="fill:#00796B" />
<text x="306" y="150" style="fill:white; font-size:13; text-anchor:middle">A=1</text>
<rect x="308" y="183" width="52" height="30" rx="4" style="fill:#00796B" />
<text x="334" y="203" style="fill:white; font-size:13; text-anchor:middle">A=1</text>
<rect x="290" y="240" width="52" height="30" rx="4" style="fill:#9E9E9E" />
<text x="316" y="260" style="fill:white; font-size:13; text-anchor:middle">A=0</text>
<rect x="240" y="270" width="52" height="30" rx="4" style="fill:#9E9E9E" />
<text x="266" y="290" style="fill:white; font-size:13; text-anchor:middle">A=0</text>
<rect x="160" y="258" width="52" height="30" rx="4" style="fill:#E65100" />
<text x="186" y="278" style="fill:white; font-size:13; text-anchor:middle">EVICT</text>
<rect x="116" y="206" width="52" height="30" rx="4" style="fill:#00796B" />
<text x="142" y="226" style="fill:white; font-size:13; text-anchor:middle">A=1</text>
<rect x="130" y="148" width="52" height="30" rx="4" style="fill:#9E9E9E" />
<text x="156" y="168" style="fill:white; font-size:13; text-anchor:middle">A=0</text>
<rect x="174" y="110" width="52" height="30" rx="4" style="fill:#1565C0" />
<text x="200" y="130" style="fill:white; font-size:13; text-anchor:middle">A=1</text>
<line x1="186" y1="258" x2="186" y2="240" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2"></line>
<text x="120" y="310" style="fill:#616161; font-size:12">Clock hand pointer</text>
<text x="120" y="326" style="fill:#616161; font-size:12">A=1 cleared on pass</text>
<text x="120" y="342" style="fill:#E65100; font-size:12">A=0 = evict candidate</text>
<rect x="490" y="40" width="380" height="300" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
<rect x="490" y="40" width="380" height="28" rx="6" style="fill:#1565C0" />
<text x="680" y="59" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">Linux Two-List LRU (Active + Inactive)</text>
<text x="680" y="88" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:middle">Active List (hot pages)</text>
<rect x="505" y="96" width="350" height="28" rx="3" style="fill:#1565C0" />
<text x="680" y="115" style="fill:white; font-size:13; text-anchor:middle">Page A - recently accessed x2</text>
<rect x="505" y="128" width="350" height="28" rx="3" style="fill:#1565C0" />
<text x="680" y="147" style="fill:white; font-size:13; text-anchor:middle">Page B - recently accessed x2</text>
<rect x="505" y="160" width="350" height="28" rx="3" style="fill:#1565C0" />
<text x="680" y="179" style="fill:white; font-size:13; text-anchor:middle">Page C - recently accessed x2</text>
<line x1="680" y1="196" x2="680" y2="210" marker-end="url(#ao)" style="stroke:#E65100; stroke-width:2"></line>
<text x="760" y="206" style="fill:#E65100; font-size:12">demoted on age</text>
<text x="680" y="228" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:middle">Inactive List (cold pages)</text>
<rect x="505" y="236" width="350" height="28" rx="3" style="fill:#9E9E9E" />
<text x="680" y="255" style="fill:white; font-size:13; text-anchor:middle">Page D - accessed once</text>
<rect x="505" y="268" width="350" height="28" rx="3" style="fill:#E65100" />
<text x="680" y="287" style="fill:white; font-size:13; text-anchor:middle">Page E - eviction candidate (tail)</text>
<line x1="680" y1="212" x2="680" y2="232" style="stroke:#212121; stroke-width:1.5; stroke-dasharray:4,2"></line>
<text x="500" y="318" style="fill:#616161; font-size:12">Accessed again from inactive: promoted to active head</text>
<text x="500" y="334" style="fill:#616161; font-size:12">Not accessed: drifts to inactive tail, then evicted</text>
<rect x="30" y="362" width="840" height="170" rx="6" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1" />
<rect x="30" y="362" width="840" height="28" rx="6" style="fill:#00796B" />
<text x="450" y="381" style="fill:white; font-size:14; font-weight:bold; text-anchor:middle">Linux Memory Pressure: Watermarks and Reclaim Thresholds</text>
<text x="120" y="415" style="fill:#00796B; font-size:14; font-weight:bold; text-anchor:middle">HIGH watermark</text>
<text x="120" y="433" style="fill:#212121; font-size:13; text-anchor:middle">Normal: kswapd sleeps</text>
<text x="120" y="451" style="fill:#212121; font-size:13; text-anchor:middle">No reclaim pressure</text>
<line x1="250" y1="395" x2="250" y2="510" style="stroke:#9E9E9E; stroke-width:1"></line>
<text x="450" y="415" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">LOW watermark</text>
<text x="450" y="433" style="fill:#212121; font-size:13; text-anchor:middle">kswapd wakes, background</text>
<text x="450" y="451" style="fill:#212121; font-size:13; text-anchor:middle">reclaim starts</text>
<line x1="650" y1="395" x2="650" y2="510" style="stroke:#9E9E9E; stroke-width:1"></line>
<text x="780" y="415" style="fill:#E65100; font-size:14; font-weight:bold; text-anchor:middle">MIN watermark</text>
<text x="780" y="433" style="fill:#212121; font-size:13; text-anchor:middle">Direct reclaim: allocating</text>
<text x="780" y="451" style="fill:#212121; font-size:13; text-anchor:middle">process reclaims pages</text>
<text x="780" y="469" style="fill:#212121; font-size:13; text-anchor:middle">itself (allocation stalls)</text>
<text x="450" y="500" style="fill:#616161; font-size:12; text-anchor:middle">OOM killer invoked if MIN watermark breached and no reclaimable pages remain</text>
</svg>
</div>
<figcaption><strong>Figure 8.2:</strong> Page replacement algorithms:
Clock (Second-Chance) and Linux Two-List LRU. The clock hand sweeps the
frame list clearing accessed bits; pages with A=0 on the second pass are
evicted. Linux refines this with an active (hot) and inactive (cold)
list separated by a reference-count threshold; pages demoted to the
inactive tail become eviction candidates. Watermarks control when kswapd
performs background reclaim vs when allocating processes reclaim
directly.</figcaption>
</figure>

Now that we understand how hardware provides A/D bits, we can explore
how operating systems use them to decide which pages to evict. The goal
is to minimize page faults---we want to evict pages that won\'t be
needed soon.

### 8.5.1 The Ideal: Bélády\'s MIN Algorithm

The theoretical optimal algorithm is simple: evict the page that will be
accessed furthest in the future. If page A won\'t be accessed for 10
seconds and page B won\'t be accessed for 2 seconds, evict page A.

This MIN algorithm (also called Bélády\'s optimal algorithm) provides
the theoretical lower bound for page fault rate---no algorithm can do
better. But there\'s a problem: it requires perfect knowledge of future
memory accesses, which is impossible.

Still, MIN is useful as a benchmark. We can simulate it in traces and
compare real algorithms against it to see how close we get to optimal.

### 8.5.2 LRU: Least Recently Used

Since we can\'t predict the future, we rely on the past. The Least
Recently Used (LRU) algorithm assumes that pages accessed recently are
likely to be accessed again soon (temporal locality). So it evicts the
page that hasn\'t been accessed for the longest time.

Perfect LRU would require tracking the exact time of last access for
every page:

``` {.sourceCode .c}
// Perfect LRU (theoretical—too expensive in practice)
struct page_lru {
    struct page *page;
    uint64_t last_access_timestamp;  // Nanosecond precision
};

struct page *lru_evict_perfect(void) {
    struct page *victim = NULL;
    uint64_t oldest_time = UINT64_MAX;
    
    // Scan all pages, find oldest
    for_each_page(page) {
        if (page->last_access_timestamp < oldest_time) {
            oldest_time = page->last_access_timestamp;
            victim = page;
        }
    }
    
    return victim;
}

// And on EVERY memory access:
void update_lru_timestamp(struct page *page) {
    page->last_access_timestamp = get_nanoseconds();
}
```

The problem: this is impossibly expensive. Consider a system with 8 GB
RAM (2 million 4KB pages). Updating a timestamp on every memory access
means:

    CPU runs at 1 billion memory accesses/second
    Each timestamp update:
      - Read current time: ~30 cycles
      - Write to page struct: ~50 cycles (cache miss likely)
      - Total: ~80 cycles = 80 nanoseconds

    Overhead: 1 billion accesses × 80 ns = 80 billion nanoseconds = 80 seconds
    CPU would spend ALL its time updating timestamps!

This doesn\'t even account for the memory overhead (8 bytes per page ×
2M pages = 16 MB just for timestamps) or the contention on the timestamp
cache lines in multi-core systems.

> ⚠️ **PERFORMANCE TRAP**
>
> Perfect LRU requires updating metadata on EVERY memory access. At
> billions of accesses per second, the overhead would be 100% of CPU
> time. The system would spend all its effort tracking accesses and none
> actually doing useful work. This is why no real system implements
> perfect LRU.

### 8.5.3 Clock Algorithm: Approximating LRU with A Bits

The Clock algorithm (also called Second Chance) brilliantly approximates
LRU using only the Accessed bit. Instead of tracking exact access times,
it uses a binary approximation: accessed-since-last-scan vs
not-accessed-since-last-scan.

The algorithm treats all pages as arranged in a circular list (imagine a
clock face). A \"hand\" scans through pages:

``` {.sourceCode .c}
// Clock algorithm implementation
struct page_clock {
    struct page **pages;       // Circular array of pages
    unsigned int clock_hand;   // Current position (0 to nr_pages-1)
    unsigned int nr_pages;     // Total pages in clock
};

struct page *clock_evict(struct page_clock *clock) {
    while (1) {
        // Get page at current clock hand position
        struct page *page = clock->pages[clock->clock_hand];
        pte_t *pte = get_pte_for_page(page);
        
        // Check Accessed bit
        if (pte_young(*pte)) {
            // A=1: Page was accessed recently
            // Give it a "second chance"—clear A bit and move on
            *pte = pte_mkold(*pte);  // Clear A bit
            
            // This page now has A=0
            // If accessed again before hand returns, A will be set to 1
            // If not accessed, next time hand visits we'll evict it
            
        } else {
            // A=0: Page wasn't accessed since last time hand passed
            // This page has had its "second chance"—evict it
            struct page *victim = page;
            
            // Remove from clock (replace with last page)
            clock->pages[clock->clock_hand] = 
                clock->pages[clock->nr_pages - 1];
            clock->nr_pages--;
            
            return victim;
        }
        
        // Move clock hand forward
        clock->clock_hand++;
        if (clock->clock_hand >= clock->nr_pages) {
            clock->clock_hand = 0;  // Wrap around
        }
    }
}

/* Based on classical Clock algorithm from Corbató's Multics
   Reference: Corbató, F. J. (1968) */
```

Let\'s trace through an example to see how it works:

    Initial state: All pages recently accessed
    Clock: [A=1] [B=1] [C=1] [D=1] [E=1]
            ↑
           hand

    Need to evict one page. Start scanning:

    Step 1: Page A, A=1
      → Clear to 0, advance hand
    Clock: [A=0] [B=1] [C=1] [D=1] [E=1]
                  ↑
                 hand

    Step 2: Page B, A=1
      → Clear to 0, advance hand
    Clock: [A=0] [B=0] [C=1] [D=1] [E=1]
                        ↑
                       hand

    Step 3: Page C, A=1
      → Clear to 0, advance hand
    Clock: [A=0] [B=0] [C=0] [D=1] [E=1]
                              ↑
                             hand

    Step 4: Page D, A=1
      → Clear to 0, advance hand
    Clock: [A=0] [B=0] [C=0] [D=0] [E=1]
                                    ↑
                                   hand

    Step 5: Page E, A=1
      → Clear to 0, wrap around
    Clock: [A=0] [B=0] [C=0] [D=0] [E=0]
            ↑
           hand

    Step 6: Page A again, A=0
      → EVICT page A!
      → A hasn't been accessed for full rotation

The beauty: pages accessed during the scan get A=1 set by hardware.
Those pages survive because the scan clears their bit to 0 but they\'ll
immediately get set back to 1 on next access:

    Clock after first rotation (all A=0):
    Time T0: [A=0] [B=0] [C=0] [D=0] [E=0]
              ↑
             hand

    Time T1: User accesses page C
      → Hardware sets C.A=1
    Clock: [A=0] [B=0] [C=1] [D=0] [E=0]

    Time T2: Clock hand reaches C
      → Sees A=1, clears it, moves on
    Clock: [A=0] [B=0] [C=0] [D=0] [E=0]
                        ↑ (hand advanced)

    Page C survived! If not accessed, would have been evicted.

> 💡 **KEY INSIGHT**
>
> Clock algorithm gives pages a \"second chance.\" First time the hand
> encounters a page, if A=1, it clears the bit and moves on. Second time
> the hand encounters that same page, if A is still 0 (not accessed in
> the meantime), it evicts the page. This approximates LRU: pages not
> accessed for a full rotation are cold and safe to evict.

Performance characteristics:

    Best case: All pages have A=0 (cold pages)
      → Find eviction candidate immediately
      → Cost: O(1)

    Worst case: All pages have A=1 (all hot)
      → Must scan all pages, clearing A bits
      → Then scan again to find victim
      → Cost: O(2n) where n = number of pages
      → But this triggers TLB flush!

    Average case: Most pages cold, some hot
      → Scan ~5-10 pages before finding A=0
      → Cost: O(1) amortized

The TLB flush is critical but expensive:

``` {.sourceCode .c}
void clock_evict_with_flush(struct page_clock *clock) {
    bool any_cleared = false;
    
    while (1) {
        struct page *page = clock->pages[clock->clock_hand];
        pte_t *pte = get_pte_for_page(page);
        
        if (pte_young(*pte)) {
            *pte = pte_mkold(*pte);
            any_cleared = true;
        } else {
            // Before evicting, flush TLB if we cleared any A bits
            // Must ensure TLB doesn't cache stale A=1 values
            if (any_cleared) {
                flush_tlb_all();  // Expensive: 10-50 µs
                any_cleared = false;
            }
            return page;
        }
        
        advance_hand(clock);
    }
}
```

### 8.5.4 Two-List LRU: Active and Inactive

Simple Clock doesn\'t distinguish between clean and dirty pages. Linux
uses a more sophisticated approach with two lists:

``` {.sourceCode .c}
// Linux-style two-list LRU
struct lruvec {
    struct list_head active_list;    // Recently accessed pages
    struct list_head inactive_list;  // Candidates for eviction
    
    unsigned long nr_active;
    unsigned long nr_inactive;
};

// Life cycle of a page:
// 1. New page → Active list (with A=1)
// 2. Periodic scan:
//      If A=1: Clear A, stay in Active
//      If A=0: Move to Inactive
// 3. In Inactive:
//      If accessed: Promote to Active
//      If not accessed: Evict
```

The eviction process works through the inactive list first:

``` {.sourceCode .c}
struct page *evict_from_inactive(struct lruvec *lru) {
    struct page *page;
    
    // Scan inactive list for eviction candidate
    list_for_each_entry(page, &lru->inactive_list, lru) {
        pte_t *pte = get_pte_for_page(page);
        
        // Last chance: check if accessed while in inactive
        if (pte_young(*pte)) {
            // Accessed! This page is hotter than we thought
            // Promote back to active list
            *pte = pte_mkold(*pte);  // Clear for next time
            list_move(&page->lru, &lru->active_list);
            lru->nr_inactive--;
            lru->nr_active++;
            continue;  // Try next page
        }
        
        // Still not accessed—safe to evict
        // Prefer clean pages over dirty
        if (!pte_dirty(*pte)) {
            // Clean page—evict immediately
            list_del(&page->lru);
            lru->nr_inactive--;
            return page;
        }
    }
    
    // All inactive pages are dirty—must evict one anyway
    page = list_first_entry(&lru->inactive_list, struct page, lru);
    list_del(&page->lru);
    lru->nr_inactive--;
    return page;
}

/* Conceptual implementation based on Linux mm/vmscan.c */
```

Refilling the inactive list happens periodically:

``` {.sourceCode .c}
void refill_inactive_list(struct lruvec *lru) {
    struct page *page, *next;
    unsigned long target = lru->nr_active / 4;  // Move 25% of active
    unsigned long moved = 0;
    
    // Scan active list
    list_for_each_entry_safe(page, next, &lru->active_list, lru) {
        if (moved >= target)
            break;
        
        pte_t *pte = get_pte_for_page(page);
        
        if (pte_young(*pte)) {
            // Still being accessed—keep in active
            *pte = pte_mkold(*pte);  // Clear for monitoring
            // Could also move to tail of active list for true LRU
            continue;
        }
        
        // Not accessed recently—demote to inactive
        list_move(&page->lru, &lru->inactive_list);
        lru->nr_active--;
        lru->nr_inactive++;
        moved++;
    }
    
    // Must flush TLB after clearing A bits
    if (moved > 0)
        flush_tlb_all();
}
```

This gives pages multiple opportunities to demonstrate they\'re hot: 1.
In active list with A=1: stays active 2. In active list with A=0:
demoted to inactive 3. In inactive list but accessed: promoted back to
active 4. In inactive list without access: evicted

> 📊 **REAL NUMBERS - TWO-LIST EFFECTIVENESS**
>
> **Benchmark: Compile Linux kernel under memory pressure (4 GB RAM, 8
> GB needed)**
>
> Simple Clock algorithm: - Page faults: 2,145,672 - Compile time: 12m
> 45s - Pages incorrectly evicted then faulted back: \~320,000
>
> Two-list LRU: - Page faults: 1,823,441 (15% reduction) - Compile time:
> 10m 52s (15% faster) - Pages incorrectly evicted: \~180,000 (44%
> reduction)
>
> The two-list approach significantly reduces thrashing by giving pages
> multiple chances to prove they\'re hot.

### 8.5.5 Multi-Generational LRU (MGLRU): Modern Linux

Linux 5.18+ uses an even more sophisticated approach: Multi-Generational
LRU with four generations:

``` {.sourceCode .c}
// MGLRU: 4 generations of pages
#define MAX_NR_GENS 4

struct lru_gen {
    // Four separate lists, one per generation
    struct list_head lists[MAX_NR_GENS][ANON_AND_FILE];
    
    unsigned long min_seq;  // Oldest generation number
    unsigned long max_seq;  // Newest generation number
    
    // At any time:
    // Gen 0 (oldest): min_seq % MAX_NR_GENS
    // Gen 1: (min_seq + 1) % MAX_NR_GENS
    // Gen 2: (min_seq + 2) % MAX_NR_GENS
    // Gen 3 (newest): max_seq % MAX_NR_GENS = (min_seq + 3) % MAX_NR_GENS
};
```

Pages age through generations based on access patterns:

``` {.sourceCode .c}
void mglru_mark_accessed(struct lru_gen *lrugen, struct page *page) {
    // Move to youngest generation
    unsigned int youngest = lrugen->max_seq % MAX_NR_GENS;
    list_move(&page->lru, &lrugen->lists[youngest][page_type]);
    page->generation = lrugen->max_seq;
}

void mglru_age_generations(struct lru_gen *lrugen) {
    // Periodically scan and age pages
    // Pages in max_seq (youngest) that have A=1: stay
    // Pages in max_seq that have A=0: get older (gen decrements)
    
    // Create new generation
    lrugen->max_seq++;
    lrugen->min_seq++;  // Oldest falls off
    
    // Scan newest generation
    unsigned int newest = lrugen->max_seq % MAX_NR_GENS;
    struct page *page;
    
    list_for_each_entry(page, &lrugen->lists[newest][ANON], lru) {
        pte_t *pte = get_pte_for_page(page);
        
        if (pte_young(*pte)) {
            // Accessed—stays in newest generation
            *pte = pte_mkold(*pte);
        } else {
            // Not accessed—ages to next older generation
            unsigned int older = (lrugen->max_seq - 1) % MAX_NR_GENS;
            list_move(&page->lru, &lrugen->lists[older][ANON]);
            page->generation--;
        }
    }
}

struct page *mglru_evict(struct lru_gen *lrugen) {
    // Evict from oldest generation
    unsigned int oldest = lrugen->min_seq % MAX_NR_GENS;
    struct page *page;
    
    list_for_each_entry(page, &lrugen->lists[oldest][ANON], lru) {
        pte_t *pte = get_pte_for_page(page);
        
        // Last chance check
        if (pte_young(*pte)) {
            // Accessed! Promote to newest
            mglru_mark_accessed(lrugen, page);
            continue;
        }
        
        // Not accessed for 4 generations—evict
        list_del(&page->lru);
        return page;
    }
    
    return NULL;
}

/* Conceptual based on Linux MGLRU by Yu Zhao
   Reference: mm/vmscan.c in Linux 5.18+ */
```

The four-generation approach provides better filtering:

    Hot page life cycle:
      Gen 3 (newest): Accessed, stays
      Gen 3: Accessed again, stays
      Gen 3: Accessed repeatedly, stays
      → Never ages beyond Gen 3

    Warm page life cycle:
      Gen 3: Accessed, stays
      Gen 2: Not accessed, ages
      Gen 3: Accessed again, promoted back
      Gen 2: Not accessed, ages
      → Bounces between Gen 2-3

    Cold page life cycle:
      Gen 3: Not accessed, ages
      Gen 2: Not accessed, ages
      Gen 1: Not accessed, ages
      Gen 0: Not accessed, ages
      → Evicted from Gen 0

> 💡 **KEY INSIGHT**
>
> MGLRU requires a page to be NOT accessed for MULTIPLE scan periods
> before evicting it. This filters out one-time scans that pollute
> simpler LRU. A page that gets accessed once during a sequential scan
> won\'t survive 4 generations, but a page in the actual working set
> will.

Performance improvement is measurable:

> 📊 **REAL NUMBERS - MGLRU VS CLASSIC LRU**
>
> **Same kernel compile benchmark (4 GB RAM, 8 GB needed):**
>
> Classic two-list LRU (Linux 5.17): - Compile time: 10m 52s - Page
> faults: 1,823,441 - Reclaim efficiency: 78% (pages evicted that
> weren\'t re-accessed soon)
>
> MGLRU (Linux 6.1): - Compile time: 8m 49s (19% faster!) - Page faults:
> 1,465,223 (20% reduction) - Reclaim efficiency: 89% (better at
> identifying truly cold pages)
>
> Improvement: MGLRU\'s multi-generation filtering reduces bad eviction
> decisions by 44%.

The cost is slightly more memory (4 list heads instead of 2) and
slightly more complex aging logic, but the benefits outweigh the costs
for most workloads.

------------------------------------------------------------------------

## 8.6 Memory Reclaim: When and How to Free Memory

Page replacement algorithms decide **which** pages to evict. But they
don\'t decide **when** to start evicting or **how aggressively**.
That\'s the job of the memory reclaim system.

### 8.6.1 Watermarks: Detecting Memory Pressure

Linux uses three watermark levels per memory zone to detect pressure:

``` {.sourceCode .c}
struct zone {
    unsigned long watermark[NR_WMARK];
    unsigned long nr_free_pages;
    // WMARK_MIN, WMARK_LOW, WMARK_HIGH
};

enum zone_watermark {
    WMARK_MIN,   // Critical—OOM imminent
    WMARK_LOW,   // Low—start background reclaim  
    WMARK_HIGH,  // Comfortable—enough free memory
};
```

The watermarks define three states:

<figure
style="margin:2.5em 0;text-align:center;page-break-inside:avoid;">
<div
style="display:inline-block;max-width:100%;overflow-x:auto;border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;">
<svg width="900" height="500" viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:0 auto;">
  <defs>
    <filter id="sh" x="-5%" y="-5%" width="115%" height="115%">
      <fedropshadow dx="2" dy="3" stddeviation="4" flood-color="rgba(0,0,0,0.18)"></fedropshadow>
    </filter>
  </defs>

  <text x="450" y="30" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:20; font-weight:bold; text-anchor:middle">Linux Memory Reclaim Watermarks (8 GB Zone Example)</text>

  <!-- Memory bar (vertical, left side) -->
  <!-- Total 8 GB = full bar height 360px -->
  <!-- WMARK_HIGH = 96 MB = 1.2% → 4px from top -->
  <!-- WMARK_LOW  = 64 MB = 0.8% → 3px from top -->
  <!-- WMARK_MIN  = 32 MB = 0.4% → 1.4px from top -->
  <!-- For visual clarity, scale zones not to percentage but to readable sizes -->

  <!-- Zone 1: Comfortable (WMARK_HIGH to top) — large -->
  <rect x="120" y="55" width="120" height="120" rx="0" style="fill:#4CAF50" />
  <text x="180" y="100" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Comfortable</text>
  <text x="180" y="118" font-family="Arial,Helvetica,sans-serif" style="fill:#E8F5E9; font-size:12; text-anchor:middle">≥ WMARK_HIGH</text>
  <text x="180" y="136" font-family="Arial,Helvetica,sans-serif" style="fill:#E8F5E9; font-size:12; text-anchor:middle">(≥ 96 MB free)</text>

  <!-- WMARK_HIGH line -->
  <rect x="120" y="175" width="120" height="3" style="fill:#1565C0" />
  <text x="50" y="179" font-family="Arial,Helvetica,sans-serif" style="fill:#1565C0; font-size:13; font-weight:bold; text-anchor:end">WMARK_HIGH</text>
  <text x="50" y="194" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:end">96 MB (1.2%)</text>

  <!-- Zone 2: Background reclaim -->
  <rect x="120" y="178" width="120" height="120" rx="0" style="fill:#FF9800" />
  <text x="180" y="222" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Background</text>
  <text x="180" y="240" font-family="Arial,Helvetica,sans-serif" style="fill:#FFF8E1; font-size:12; text-anchor:middle">Reclaim Zone</text>
  <text x="180" y="258" font-family="Arial,Helvetica,sans-serif" style="fill:#FFF8E1; font-size:12; text-anchor:middle">kswapd active</text>

  <!-- WMARK_LOW line -->
  <rect x="120" y="298" width="120" height="3" style="fill:#E65100" />
  <text x="50" y="302" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:13; font-weight:bold; text-anchor:end">WMARK_LOW</text>
  <text x="50" y="317" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:end">64 MB (0.8%)</text>

  <!-- Zone 3: Critical / Direct reclaim -->
  <rect x="120" y="301" width="120" height="80" rx="0" style="fill:#F44336" />
  <text x="180" y="328" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">Critical</text>
  <text x="180" y="346" font-family="Arial,Helvetica,sans-serif" style="fill:#FFEBEE; font-size:12; text-anchor:middle">Direct reclaim</text>
  <text x="180" y="364" font-family="Arial,Helvetica,sans-serif" style="fill:#FFEBEE; font-size:12; text-anchor:middle">alloc stalls</text>

  <!-- WMARK_MIN line -->
  <rect x="120" y="381" width="120" height="3" style="fill:#B71C1C" />
  <text x="50" y="385" font-family="Arial,Helvetica,sans-serif" style="fill:#B71C1C; font-size:13; font-weight:bold; text-anchor:end">WMARK_MIN</text>
  <text x="50" y="400" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:end">32 MB (0.4%)</text>

  <!-- Zone 4: OOM -->
  <rect x="120" y="384" width="120" height="60" rx="0" style="fill:#7B1FA2" />
  <text x="180" y="411" font-family="Arial,Helvetica,sans-serif" style="fill:#fff; font-size:13; font-weight:bold; text-anchor:middle">OOM Zone</text>
  <text x="180" y="430" font-family="Arial,Helvetica,sans-serif" style="fill:#F3E5F5; font-size:12; text-anchor:middle">OOM killer fires</text>

  <!-- Bottom label -->
  <text x="180" y="460" font-family="Arial,Helvetica,sans-serif" style="fill:#616161; font-size:12; text-anchor:middle">0 MB free</text>

  <!-- Right panel: Actions per zone -->
  <rect x="290" y="55" width="580" height="430" rx="6" filter="url(#sh)" style="fill:#F5F5F5; stroke:#9E9E9E; stroke-width:1.5" />
  <text x="580" y="80" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:16; font-weight:bold; text-anchor:middle">System Actions per Zone</text>

  <!-- Comfortable -->
  <rect x="305" y="90" width="550" height="95" rx="4" style="fill:#E8F5E9; stroke:#4CAF50; stroke-width:1.5" />
  <text x="315" y="112" font-family="Arial,Helvetica,sans-serif" style="fill:#2E7D32; font-size:14; font-weight:bold">● Comfortable Zone (above WMARK_HIGH)</text>
  <text x="325" y="132" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• kswapd sleeps — no reclaim pressure</text>
  <text x="325" y="150" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• Allocations succeed immediately from free list</text>
  <text x="325" y="168" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• THP (Transparent Huge Pages) can be compacted proactively</text>

  <!-- Background reclaim -->
  <rect x="305" y="195" width="550" height="95" rx="4" style="fill:#FFF8E1; stroke:#FF9800; stroke-width:1.5" />
  <text x="315" y="217" font-family="Arial,Helvetica,sans-serif" style="fill:#E65100; font-size:14; font-weight:bold">● Background Reclaim Zone (LOW → HIGH)</text>
  <text x="325" y="237" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• kswapd thread wakes up, scans LRU lists</text>
  <text x="325" y="255" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• Evicts cold pages, writes dirty pages to swap asynchronously</text>
  <text x="325" y="273" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• Allocation requests still succeed (no stalls yet)</text>

  <!-- Critical -->
  <rect x="305" y="300" width="550" height="95" rx="4" style="fill:#FFEBEE; stroke:#F44336; stroke-width:1.5" />
  <text x="315" y="322" font-family="Arial,Helvetica,sans-serif" style="fill:#C62828; font-size:14; font-weight:bold">● Critical Zone (MIN → LOW)</text>
  <text x="325" y="342" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• Allocating process itself performs direct reclaim (synchronous)</text>
  <text x="325" y="360" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• Allocation latency spikes — visible to applications</text>
  <text x="325" y="378" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• THP allocation disabled, compaction suspended</text>

  <!-- OOM -->
  <rect x="305" y="405" width="550" height="70" rx="4" style="fill:#F3E5F5; stroke:#7B1FA2; stroke-width:1.5" />
  <text x="315" y="427" font-family="Arial,Helvetica,sans-serif" style="fill:#6A1B9A; font-size:14; font-weight:bold">● OOM Zone (below WMARK_MIN, reclaim failed)</text>
  <text x="325" y="447" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• OOM killer selects a process to terminate (highest oom_score)</text>
  <text x="325" y="465" font-family="Arial,Helvetica,sans-serif" style="fill:#212121; font-size:13">• /proc/sys/vm/panic_on_oom can force kernel panic instead</text>
</svg>
</div>
<figcaption><strong>Figure 8.watermarks:</strong> Linux memory reclaim
watermarks for an 8 GB zone: free memory above WMARK_HIGH (96 MB, 1.2%)
is comfortable — kswapd sleeps. Below WMARK_HIGH, kswapd wakes for
background reclaim. Below WMARK_LOW (64 MB), allocation latency rises.
Below WMARK_MIN (32 MB), allocating processes perform synchronous direct
reclaim. If reclaim fails, the OOM killer terminates a
process.</figcaption>
</figure>

Checking watermarks:

``` {.sourceCode .c}
bool zone_watermark_ok(struct zone *zone, unsigned int order,
                       unsigned long mark) {
    unsigned long free_pages = zone_page_state(zone, NR_FREE_PAGES);
    unsigned long min = mark;
    
    // Adjust for high-order allocations
    // Larger allocations need more free pages
    min += (1UL << order);
    
    // Also need some pages reserved for atomic allocations
    min += zone->lowmem_reserve;
    
    return free_pages >= min;
}
```

Tuning watermarks:

``` {.sourceCode .bash}
# System default: scale with memory size
# For 8 GB: min = 32 MB, low = 64 MB, high = 96 MB

# Increase min_free_kbytes for latency-sensitive workloads
# Keeps more memory free to avoid direct reclaim
echo 262144 > /proc/sys/vm/min_free_kbytes  # 256 MB

# This also scales low and high watermarks proportionally
```

### 8.6.2 kswapd: Background Reclaim Daemon

The kernel thread `kswapd` runs in the background, waking when memory
drops below low watermark:

``` {.sourceCode .c}
// kswapd kernel thread (simplified)
int kswapd(void *p) {
    struct pglist_data *pgdat = (struct pglist_data *)p;
    
    while (!kthread_should_stop()) {
        // Sleep until low watermark breached
        wait_event_interruptible(pgdat->kswapd_wait,
                                 need_reclaim(pgdat));
        
        // Reclaim until high watermark reached
        while (below_high_watermark(pgdat)) {
            // Reclaim in small batches
            unsigned long nr_reclaimed = shrink_node(pgdat, 32);
            
            // Be nice—yield CPU periodically
            if (nr_reclaimed > 1024) {
                schedule();
            }
            
            // Check if we're making progress
            if (nr_reclaimed == 0) {
                // Stuck—might need to give up
                break;
            }
        }
    }
    
    return 0;
}

/* Based on Linux kernel mm/vmscan.c */
```

kswapd workflow:

    T0: Free memory = 80 MB
        → Above low watermark (64 MB)
        → kswapd sleeping

    T1: Application allocates memory
        Free memory = 60 MB
        → Below low watermark!
        → Wake kswapd

    T2: kswapd starts reclaiming
        Reclaim 32 pages
        Free memory = 60 MB + 128 KB = 60.125 MB

    T3: Application still allocating
        Free memory = 58 MB

    T4: kswapd reclaims more
        Free memory = 70 MB

        ...continue until...

    T100: Free memory = 98 MB
          → Above high watermark (96 MB)
          → kswapd goes back to sleep

    Total time: ~100 ms of background work
    Applications barely noticed

> 💡 **KEY INSIGHT**
>
> kswapd runs in the background, reclaiming memory before applications
> run out. This avoids the disaster of direct reclaim (where allocating
> processes block on reclaim). Most of the time, kswapd keeps up and
> applications never experience allocation delays.

### 8.6.3 Direct Reclaim: The Emergency Path

When kswapd can\'t keep up, allocating processes must reclaim memory
themselves:

``` {.sourceCode .c}
struct page *__alloc_pages(gfp_t gfp_mask, unsigned int order) {
    struct page *page;
    
    // Try fast path first
    page = get_page_from_freelist(gfp_mask, order);
    if (page)
        return page;  // Success!
    
    // No free pages—wake kswapd
    wakeup_kswapd();
    
    // Try again (maybe kswapd already freed some)
    page = get_page_from_freelist(gfp_mask, order);
    if (page)
        return page;
    
    // Still no memory—DIRECT RECLAIM
    // The allocating process does the work
    if (gfp_mask & __GFP_DIRECT_RECLAIM) {
        unsigned long nr_reclaimed;
        
        // Reclaim synchronously
        nr_reclaimed = try_to_free_pages(gfp_mask, order);
        
        if (nr_reclaimed > 0) {
            // Try allocation again
            page = get_page_from_freelist(gfp_mask, order);
            if (page)
                return page;
        }
    }
    
    // Extreme: invoke OOM killer
    if (gfp_mask & __GFP_NOFAIL) {
        page = __alloc_pages_may_oom(gfp_mask, order);
    }
    
    return NULL;  // Allocation failed
}

/* Based on Linux kernel mm/page_alloc.c */
```

The timeline of disaster:

    Application calls malloc(1 MB):

    T0:     Allocation starts
    T1:     Fast path: No free pages
    T2:     Wake kswapd
    T100ms: Wait for kswapd
    T100ms: Still no free pages
    T100ms: Enter DIRECT RECLAIM
    T100ms: Scan 100 pages for eviction
    T102ms: Found 50 dirty pages, 50 clean pages
    T102ms: Evict 50 clean pages (fast)
    T103ms: Must evict dirty pages too
    T103ms: Write 50 dirty pages to disk
    T103ms: Each write: 5 ms on spinning disk
    T353ms: Disk writes complete (50 × 5 ms = 250 ms)
    T354ms: Pages freed, allocation succeeds
    T354ms: malloc() FINALLY returns

    Application was BLOCKED for 354 milliseconds!

> ⚠️ **PERFORMANCE TRAP**
>
> Direct reclaim blocks the allocating process. If that process is
> handling a user request (web server, database query, UI interaction),
> the user sees a freeze. A simple `malloc()` call that normally takes
> microseconds can take hundreds of milliseconds. This unpredictable
> latency is why keeping memory above low watermark is critical.

Real-world impact:

    Database query with direct reclaim:
      Normal: 5 ms query time
      With direct reclaim: 5 ms + 350 ms = 355 ms
      User sees: 70× slower query!

    Web server request:
      Normal: 50 ms response
      With direct reclaim: 50 ms + 350 ms = 400 ms
      User sees: 8× slower page load
      
    Real-time system:
      Normal: 1 ms deadline
      With direct reclaim: 350 ms
      Result: MISSED DEADLINE (350× over budget!)

### 8.6.4 vm.swappiness: Tuning Reclaim Behavior

The `vm.swappiness` parameter controls the balance between swapping
anonymous pages and evicting file-backed pages:

``` {.sourceCode .c}
// vm.swappiness: 0-200 (default 60)
int vm_swappiness = 60;

void get_scan_count(struct lruvec *lruvec, struct scan_control *sc,
                    unsigned long *nr) {
    unsigned long anon_prio, file_prio;
    
    // Swappiness affects priority
    // Higher swappiness = more aggressive anonymous eviction
    anon_prio = swappiness;
    file_prio = 200 - swappiness;
    
    // Calculate how many pages to scan in each list
    unsigned long ap = anon_prio * lruvec->nr_anon;
    unsigned long fp = file_prio * lruvec->nr_file;
    
    unsigned long total = ap + fp;
    nr[LRU_ANON] = (ap * sc->nr_to_scan) / total;
    nr[LRU_FILE] = (fp * sc->nr_to_scan) / total;
}

/* Based on Linux kernel mm/vmscan.c */
```

Different workloads need different settings:

``` {.sourceCode .bash}
# Database server: Avoid swapping (keep DB buffers in RAM)
sysctl vm.swappiness=1
# Effect: Evicts file cache first, only swaps when desperate
# Good for: Databases with large in-memory caches

# Desktop: Balance (default)
sysctl vm.swappiness=60
# Effect: Balances anonymous vs file eviction
# Good for: General purpose systems

# File server: Aggressive swapping
sysctl vm.swappiness=100
# Effect: Keeps file cache, swaps applications
# Good for: File servers, build servers (lots of file I/O)
```

Real example - database tuning:

    PostgreSQL server: 64 GB RAM, 48 GB shared_buffers

    Problem with vm.swappiness=60:
      - Under pressure, kernel swaps out 2 GB of DB buffers
      - Queries hit swap instead of RAM
      - Query time: 5 ms → 100 ms (20× slower!)
      
    Solution: vm.swappiness=1
      - Kernel evicts file cache instead
      - DB buffers stay in RAM
      - Query time: remains 5 ms
      
    Result: 20× performance improvement from one sysctl!

### 8.6.5 OOM Killer: The Last Resort

When reclaim fails and memory is critically low, the OOM (Out Of Memory)
killer selects and kills a process:

``` {.sourceCode .c}
void out_of_memory(struct oom_control *oc) {
    struct task_struct *victim;
    
    // Select victim based on badness score
    victim = select_bad_process(oc);
    
    if (!victim) {
        panic("Out of memory and no killable process");
    }
    
    // Log the kill
    pr_err("Out of memory: Killed process %d (%s) "
           "total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB\n",
           victim->pid, victim->comm,
           K(victim->mm->total_vm),
           K(get_mm_counter(victim->mm, MM_ANONPAGES)),
           K(get_mm_counter(victim->mm, MM_FILEPAGES)));
    
    // Send SIGKILL
    do_send_sig_info(SIGKILL, SEND_SIG_FORCED, victim);
    
    mark_oom_victim(victim);
}

unsigned long oom_badness(struct task_struct *p) {
    unsigned long points = 0;
    
    // Base score: memory usage
    points = get_mm_rss(p->mm);  // Resident set
    points += get_mm_counter(p->mm, MM_SWAPENTS);  // Swapped pages
    points += p->mm->total_vm / 2;  // Virtual memory (half weight)
    
    // Convert to percentage of RAM
    points = (points * 1000) / totalram_pages();
    
    // User adjustment
    points += p->signal->oom_score_adj;
    
    // Penalties
    if (has_capability_noaudit(p, CAP_SYS_ADMIN))
        points -= points / 4;  // Root processes: -25%
    
    if (is_global_init(p))
        return 0;  // Never kill init (PID 1)
    
    return points < 0 ? 0 : points;
}

/* Based on Linux kernel mm/oom_kill.c */
```

The OOM killer\'s decision process:

    System state:
      MemTotal: 8 GB
      MemFree: 4 MB (critical!)
      
    Process scores:
      PID 1    init        12 MB   Score: 0      (never kill)
      PID 145  sshd        8 MB    Score: 5      (system service)
      PID 1234 chrome      2.5 GB  Score: 850    ← KILL THIS
      PID 2341 postgres    1.8 GB  Score: 420    (oom_adj=-100)
      PID 3456 httpd       500 MB  Score: 180    
      
    Decision: Kill PID 1234 (chrome) - highest score

Protecting critical processes:

``` {.sourceCode .bash}
# Protect PostgreSQL from OOM killer
echo -500 > /proc/$(pidof postgres)/oom_score_adj
# Negative oom_score_adj makes it less likely to be killed

# Make a development process more likely to die
echo 500 > /proc/$(pidof dev_app)/oom_score_adj
```

------------------------------------------------------------------------

## 8.7 Page Table Management: The Hidden Memory Consumer

We\'ve focused on evicting data pages, but page tables themselves
consume significant memory. This section explores when to allocate them,
when to free them, and how their layout affects performance.

### 8.7.1 Page Table Memory Overhead

Every process needs page tables to translate its virtual addresses. The
question is: how much memory do they consume?

For x86-64 with 4-level page tables, the overhead depends on address
space density:

``` {.sourceCode .c}
// Calculate page table overhead
unsigned long calc_pt_overhead(unsigned long mapped_bytes) {
    unsigned long pages = mapped_bytes / PAGE_SIZE;
    
    // Leaf level: One PTE per page (8 bytes each)
    // Grouped in page tables (512 PTEs per 4KB table)
    unsigned long pt_pages = (pages + 511) / 512;
    
    // Next level: One PDE per page table
    unsigned long pd_pages = (pt_pages + 511) / 512;
    
    // Next level: One PDPTE per page directory
    unsigned long pdpt_pages = (pd_pages + 511) / 512;
    
    // Top level: Always one PML4
    unsigned long pml4_pages = 1;
    
    // Total overhead
    unsigned long total_pages = pt_pages + pd_pages + pdpt_pages + pml4_pages;
    return total_pages * PAGE_SIZE;
}

// Example: 10 GB mapped
// 10 GB = 2,621,440 pages
// PTs:   2,621,440 / 512 = 5,120 (20 MB)
// PDs:   5,120 / 512 = 10 (40 KB)
// PDPTs: 10 / 512 = 1 (4 KB)
// PML4:  1 (4 KB)
// Total: 5,132 pages = 20 MB overhead (0.2%)
```

This seems small---0.2% overhead. But problems arise with scale:

    Database server: 100 processes × 10 GB each
      Per-process: 20 MB page tables
      Total: 100 × 20 MB = 2 GB just for page tables!
      
    VM host: 8 VMs × 16 GB each
      Guest page tables: 8 × 32 MB = 256 MB
      Host EPT: 8 × 32 MB = 256 MB
      Total: 512 MB for page table metadata
      
    Container host: 1000 containers
      Even if each only maps 100 MB: 1000 × 0.2 MB = 200 MB

> 📊 **REAL NUMBERS - PAGE TABLE OVERHEAD SCALING**
>
> **Small system (8 GB RAM, 20 processes):** - Application memory: 6
> GB - Page tables: 120 MB (2%) - Impact: Negligible
>
> **Large system (256 GB RAM, 500 processes):** - Application memory:
> 200 GB - Page tables: 4 GB (2%) - Impact: Noticeable---could run 2
> more VMs without PT overhead
>
> **Huge system (1 TB RAM, 2000 processes):** - Application memory: 800
> GB - Page tables: 16 GB (2%) - Impact: Significant---16 GB unavailable
> for applications

### 8.7.2 Lazy Allocation

Operating systems don\'t allocate all page table levels immediately.
They allocate on-demand:

``` {.sourceCode .c}
// Page fault handler allocates page tables as needed
int handle_mm_fault(struct vm_area_struct *vma, unsigned long address) {
    pgd_t *pgd;
    p4d_t *p4d;
    pud_t *pud;
    pmd_t *pmd;
    pte_t *pte;
    
    // Top level always exists
    pgd = pgd_offset(vma->vm_mm, address);
    
    // Allocate P4D if needed
    p4d = p4d_alloc(vma->vm_mm, pgd, address);
    if (!p4d)
        return VM_FAULT_OOM;
    
    // Allocate PUD if needed
    pud = pud_alloc(vma->vm_mm, p4d, address);
    if (!pud)
        return VM_FAULT_OOM;
    
    // Allocate PMD if needed
    pmd = pmd_alloc(vma->vm_mm, pud, address);
    if (!pmd)
        return VM_FAULT_OOM;
    
    // Allocate PTE if needed
    pte = pte_alloc(vma->vm_mm, pmd, address);
    if (!pte)
        return VM_FAULT_OOM;
    
    // Now handle the actual page fault
    return handle_pte_fault(vma, address, pte, ...);
}

/* Based on Linux kernel mm/memory.c */
```

Savings from lazy allocation:

    Sparse address space example:
      Code at:  0x00400000 (4 MB)
      Heap at:  0x10000000 (256 MB)
      Stack at: 0x7FFFFFFFFFFF (top of address space)
      
    Wasteful (allocate all levels):
      Would need page tables for entire 256 TB space
      Cost: Gigabytes of page table memory
      
    Lazy (allocate on-demand):
      PML4: 1 page (4 KB) - always allocated
      PDPTs: 3 pages (12 KB) - one for code, heap, stack
      PDs: 3 pages (12 KB)
      PTs: ~10 pages (40 KB)
      Total: ~68 KB
      
    Savings: Gigabytes → 68 KB = 10,000× reduction!

> 💡 **KEY INSIGHT**
>
> Lazy page table allocation is why sparse address spaces work. A
> process can have a 256 TB address space but only pay for the page
> tables it actually uses. Without lazy allocation, every process would
> consume gigabytes just for empty page table structures.

### 8.7.3 Huge Pages: Reducing Page Table Overhead

Chapter 4 showed how huge pages improve TLB coverage. They also
dramatically reduce page table overhead:

``` {.sourceCode .c}
// Page table overhead with 4KB pages
// Mapping 100 GB:
//   262,144,000 pages / 512 (per PT) = 512,000 PTs
//   512,000 × 4 KB = 2 GB of page table overhead
//   Plus 1000 PDs, 2 PDPTs, 1 PML4
//   Total: ~2 GB (2% overhead)

// Page table overhead with 2MB pages
// Mapping 100 GB:
//   51,200 huge pages (no PTs needed!)
//   51,200 / 512 (per PD) = 100 PDs
//   100 / 512 = 1 PDPT
//   1 PML4
//   Total: ~400 KB (0.0004% overhead)
//   
// Reduction: 2 GB → 400 KB = 5000× less!
```

Linux Transparent Huge Pages (THP) automatically promotes pages:

``` {.sourceCode .c}
// khugepaged daemon scans for promotion opportunities
void khugepaged_scan_mm_slot(struct mm_slot *mm_slot) {
    struct mm_struct *mm = mm_slot->mm;
    struct vm_area_struct *vma;
    
    for_each_vma(vma) {
        unsigned long address;
        
        // Scan VMA in 2MB chunks
        for (address = vma->vm_start; 
             address < vma->vm_end; 
             address += HPAGE_PMD_SIZE) {
            
            // Check if 512 consecutive 4KB pages are present
            // and meet criteria for huge page
            if (khugepaged_scan_pmd(mm, vma, address))
                collapse_huge_page(mm, address, vma);
        }
    }
}

int collapse_huge_page(struct mm_struct *mm, unsigned long address,
                       struct vm_area_struct *vma) {
    // Allocate 2MB huge page
    struct page *hpage = alloc_hugepage_vma(vma, address);
    if (!hpage)
        return -ENOMEM;
    
    // Copy 512 × 4KB pages into huge page
    for (int i = 0; i < HPAGE_PMD_NR; i++) {
        struct page *page = get_page_at(address + i * PAGE_SIZE);
        copy_page(hpage + i, page);
    }
    
    // Update page tables: Replace 512 PTEs with 1 PMD
    pmd_t *pmd = pmd_offset(..., address);
    
    // Free the old page table (512 PTEs)
    pte_t *pte = pte_offset_map(pmd, address);
    pte_free(mm, pte);  // Freed 4KB!
    
    // Install huge page at PMD level
    set_pmd_at(mm, address, pmd, mk_huge_pmd(hpage, vma->vm_page_prot));
    
    return 0;
}

/* Based on Linux kernel mm/huge_memory.c */
```

------------------------------------------------------------------------

## 8.8 Performance Analysis and Tuning

Armed with understanding of the mechanisms, let\'s explore how to
measure and optimize memory management.

### 8.8.1 Diagnostic Tools

**/proc/meminfo - System Memory Status**

``` {.sourceCode .bash}
$ cat /proc/meminfo
MemTotal:       65536000 kB   # Total RAM
MemFree:         2097152 kB   # Truly free
MemAvailable:   17825792 kB   # Free + reclaimable
Buffers:          524288 kB   # Filesystem metadata
Cached:         35651584 kB   # Page cache
Active:         45088768 kB   # Recently used
Inactive:       15728640 kB   # Eviction candidates
Active(anon):   28672000 kB   # Active application memory
Active(file):   16416768 kB   # Active file cache
PageTables:      8388608 kB   # PT memory ← Watch this!
Dirty:            102400 kB   # Needs writeback
```

Red flags in meminfo:

``` {.sourceCode .bash}
# Red Flag 1: High PageTables
PageTables: 8388608 kB  # 8 GB in page tables!
# For 32 GB RSS, expect ~64 MB
# 8 GB = 125× higher than normal!
# → Fragmented memory or too many processes

# Red Flag 2: Low MemAvailable despite high Cached
MemFree:      1024 kB
Cached:   35651584 kB (34 GB)
MemAvailable: 2097152 kB  # Only 2 GB "available"?
# → Most cache is un-reclaimable (tmpfs, ramdisk, etc.)

# Red Flag 3: High Dirty
Dirty: 10485760 kB  # 10 GB dirty!
# → Disk writes backed up, memory pressure imminent
```

**vmstat - Real-Time Monitoring**

``` {.sourceCode .bash}
$ vmstat 1
procs memory    swap          io     system      cpu
 r  b  swpd free buff cache   si so  bi   bo   in   cs  us sy id wa
 2  0   102 4096  512 12288    0  0   0    0  500 1000 10  5 85  0
 1  0   102 3584  512 12288    0 128  0 5120 600 1100 15 10 75  0
```

Red flags in vmstat:

``` {.sourceCode .bash}
# Red Flag: Heavy swapping
 si    so      # Swap in/out (KB/s)
5120 10240     # Swapping 5 MB in, 10 MB out per second
               # → System is thrashing!
               
# Red Flag: High wait time
 wa             # I/O wait percentage
 45             # 45% time waiting for I/O
               # → Disk bottleneck (swapping or dirty writeback)
```

### 8.8.2 Complete Case Study: Solving the PostgreSQL OOM

Let\'s return to our opening mystery and solve it step by step:

**Initial Problem:**

``` {.sourceCode .bash}
$ free -h
              total    used    free  shared  buff/cache  available
Mem:           64G     45G    2.1G    156M         16G        17G

kernel: Out of memory: Killed process 2847 (postgres)
```

**Investigation Step 1: Check Page Table Overhead**

``` {.sourceCode .bash}
$ cat /proc/meminfo | grep PageTables
PageTables:      8388608 kB  # 8 GB!

# For 48 GB of PostgreSQL (3 × 16 GB), expect:
# 48 GB × 0.002 = 96 MB of page tables
# Actual: 8 GB = 83× higher than expected!
```

**Investigation Step 2: Check Process Details**

``` {.sourceCode .bash}
$ cat /proc/2847/status | grep -E 'VmPTE|VmSize|VmRSS'
VmSize: 17825244 kB  # 17 GB virtual
VmRSS:  15728640 kB  # 15 GB resident
VmPTE:   2621440 kB  # 2.5 GB page tables for this process alone!

# Expected PT for 15 GB RSS: 30 MB
# Actual: 2.5 GB = 83× too high
# Something is creating way too many page tables
```

**Investigation Step 3: Check Memory Mappings**

``` {.sourceCode .bash}
$ cat /proc/2847/maps | wc -l
45678  # 45,000 VMAs!

$ cat /proc/2847/maps | head -20
00400000-00500000 r-xp 00000000 08:01 12345  /usr/bin/postgres
...
7f1234000000-7f1234001000 rw-p 00000000 00:00 0  # Tiny 4KB mapping
7f1234001000-7f1234002000 rw-p 00000000 00:00 0  # Another 4KB
7f1234002000-7f1234003000 rw-p 00000000 00:00 0  # And another...
# Thousands of tiny allocations!
```

**Root Cause:** PostgreSQL was configured with: - `huge_pages = off`
(default) - `shared_buffers = 16GB` - Many small `work_mem` allocations
creating 45,000 VMAs - Each VMA needs page table pages - Fragmented
allocations require more page tables

**The Fix:**

``` {.sourceCode .bash}
# Step 1: Enable huge pages in kernel
echo 24576 > /proc/sys/vm/nr_hugepages  # 24576 × 2MB = 48 GB

$ cat /proc/meminfo | grep HugePages
HugePages_Total:   24576
HugePages_Free:    24576

# Step 2: Configure PostgreSQL
# In postgresql.conf:
huge_pages = on
shared_buffers = 16GB

# Step 3: Restart PostgreSQL
systemctl restart postgresql@{1,2,3}

# Step 4: Verify
$ cat /proc/meminfo | grep HugePages
HugePages_Total:   24576
HugePages_Free:        0  # All allocated!

$ cat /proc/meminfo | grep PageTables
PageTables:      524288 kB  # 512 MB (down from 8 GB!)
```

**Results:**

    Before huge pages:
      PageTables: 8 GB
      MemAvailable: 17 GB (misleading)
      OOM kills: Frequent
      Query performance: Variable (sometimes slow)

    After huge pages:
      PageTables: 512 MB (16× reduction!)
      MemAvailable: 24 GB (realistic)
      OOM kills: None
      Query performance: 15% faster (better TLB efficiency)

    Explanation of "17 GB available":
      Total RAM: 64 GB
      Active anon: 41 GB (applications)
      Page tables: 8 GB (un-reclaimable)
      Buffers/cache: 15 GB (reclaimable)
      Free: 2 GB
      
      "Available" calculation:
        Free + reclaimable = 2 GB + 15 GB = 17 GB
        
      But actual allocatable:
        64 GB total - 41 GB used - 8 GB PT = 15 GB
        
      Difference: 17 GB "available" but only 15 GB actually allocatable
      When postgres tried to allocate 18 GB → OOM!

> 💡 **KEY INSIGHT**
>
> The \"available\" memory metric is misleading because it doesn\'t
> account for un-reclaimable overhead like page tables. With 8 GB in
> page tables (12.5% of RAM!), the system had far less memory available
> than `free` suggested. Huge pages solved two problems: reduced page
> table overhead from 8 GB to 512 MB (16× reduction), and improved TLB
> efficiency for better query performance.

------------------------------------------------------------------------

## 8.9 Summary: The Complete Picture

We\'ve now completed our journey through MMU systems and virtual memory.
This final chapter tied together all the concepts from Chapters 1-7,
showing how hardware mechanisms enable software policies.

### The Hardware-Software Contract

The MMU provides mechanisms: - **Page tables** (Chapter 3): Multi-level
translation structures - **TLB** (Chapter 4): Caching to avoid expensive
walks - **Accessed/Dirty bits** (this chapter): Tracking page usage -
**Page faults** (Chapter 7): Exceptions when translation fails -
**Nested translation** (this chapter): Two-stage VM support

The OS implements policies: - **When to allocate** page tables: Lazy
allocation saves 10,000× - **Which pages to evict**: Clock/MGLRU using A
bits - **How aggressively to reclaim**: Watermarks and kswapd - **When
to use huge pages**: Reduces overhead 500×

Together they enable: - Process isolation (each process has own address
space) - Memory overcommit (allocate more than physical RAM) - Efficient
memory use (lazy allocation, page sharing) - Predictable performance
(intelligent eviction policies) - Virtualization (nested page tables)

### Bridging the Chapters

**From Chapter 1** (Basics): Virtual memory abstraction enables
isolation and overcommit → **This chapter showed**: How page replacement
and reclaim actually implement overcommit

**From Chapter 2** (Concepts): Demand paging delays allocation → **This
chapter showed**: How eviction policies decide which pages to swap out

**From Chapter 3** (Page Tables): Multi-level structures save memory →
**This chapter showed**: When to allocate/free these structures, their
hidden cost

**From Chapter 4** (TLB): Caching avoids expensive walks → **This
chapter showed**: How page replacement affects TLB (evicting hot pages =
TLB misses)

**From Chapter 7** (Page Faults): Faults trigger on missing pages →
**This chapter showed**: Which pages to evict triggers which future
faults

### Practical Takeaways

**For System Administrators:**

Monitor the right metrics:

``` {.sourceCode .bash}
# Not just free memory
watch -n1 'cat /proc/meminfo | grep -E "MemAvailable|PageTables|Dirty|Active"'

# Watch for swapping
vmstat 1

# Check per-process page tables
cat /proc/*/status | grep VmPTE | sort -rn | head
```

Tune for your workload:

``` {.sourceCode .bash}
# Database: avoid swapping
sysctl vm.swappiness=1
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# Ensure adequate free memory
sysctl vm.min_free_kbytes=262144  # 256 MB
```

**For Application Developers:**

Use huge pages for large allocations:

``` {.sourceCode .c}
// Request huge pages explicitly
void *ptr = mmap(NULL, 1 << 30,  // 1 GB
                 PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS | MAP_HUGETLB,
                 -1, 0);
```

Avoid memory fragmentation:

``` {.sourceCode .c}
// Bad: Many small allocations
for (int i = 0; i < 1000000; i++)
    ptrs[i] = malloc(4096);  // 1M page tables!

// Good: Fewer large allocations  
void *big = malloc(1 << 30);  // 1 GB, fewer page tables
```

Use madvise() hints:

``` {.sourceCode .c}
// Tell kernel about access patterns
madvise(ptr, size, MADV_SEQUENTIAL);  // Sequential access
madvise(ptr, size, MADV_DONTNEED);    // Done with this memory
madvise(ptr, size, MADV_WILLNEED);    // Will need soon
```

**For Hypervisor Operators:**

Pre-populate EPT to avoid boot slowdown:

``` {.sourceCode .c}
// Allocate common regions before VM runs
prepopulate_ept(vm, low_memory, 1MB);
prepopulate_ept(vm, kernel_region, 1GB);
```

Use huge pages at both levels:

``` {.sourceCode .bash}
# Host: Enable THP
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# Guest: Also enable THP
# Benefits multiply: guest PT uses huge pages, EPT maps them with huge pages
```

### The Big Picture

Modern virtual memory systems are a marvel of hardware-software
co-design. The MMU provides the building blocks---multi-level page
tables, TLB caching, A/D bits, page faults. The OS orchestrates these
mechanisms into sophisticated policies---lazy allocation, intelligent
eviction, background reclaim, huge page promotion.

When you next see \"Out of Memory\" or notice swapping, you\'ll
understand the complete story: from hardware setting A bits during
translation, through page table walks and TLB lookups, to the kernel\'s
page replacement decisions and the OOM killer\'s selection logic.

The key insight: there is no \"perfect\" policy. Different workloads
need different tuning: - **Databases:** Huge pages, low swappiness,
adequate min_free - **Desktops:** Balanced swappiness, moderate
watermarks - **VMs:** Pre-populated EPT, huge pages at both levels\
- **Real-time:** Locked pages, no swapping

Understanding both mechanisms (Chapters 1-7) and policies (this chapter)
empowers you to make informed decisions for your specific use case.

------------------------------------------------------------------------

## References

1.  Denning, P. J. (1970). \"Virtual Memory.\" *ACM Computing Surveys*,
    2(3), 153-189.

2.  Corbató, F. J. (1968). \"A paging experiment with the Multics
    system.\" *MIT Project MAC*.

3.  Adams, K., & Agesen, O. (2006). \"A comparison of software and
    hardware techniques for x86 virtualization.\" *ACM SIGPLAN Notices*,
    41(11), 2-13.

4.  Zhao, Y. (2022). \"Multi-Gen LRU.\" Linux kernel mailing list.
    Merged in Linux 5.18.

5.  Intel Corporation (2024). *Intel 64 and IA-32 Architectures Software
    Developer\'s Manual, Volume 3*.

6.  ARM Ltd (2024). *ARM Architecture Reference Manual, ARMv8-A*.

7.  RISC-V International (2021). *The RISC-V Instruction Set Manual,
    Volume II: Privileged Architecture*.

8.  Linux Kernel (v6.5). *mm/vmscan.c, mm/oom_kill.c, mm/huge_memory.c*.

9.  Arcangeli, A. (2011). \"Transparent Huge Pages.\" Linux kernel
    documentation.

10. Gregg, B. (2020). *Systems Performance: Enterprise and the Cloud,
    2nd Edition*. Addison-Wesley.

------------------------------------------------------------------------

**End of Chapter 8**

## 8.5 Page Replacement Algorithms: Making the Choice

We now understand the hardware mechanisms---the MMU sets A and D bits
automatically (or we handle faults if software-managed). But
understanding the mechanisms doesn\'t tell us the policy. When memory
fills up and we must evict pages, which specific pages should we choose?

### 8.5.1 The Ideal: Least Recently Used (LRU)

The theoretically optimal algorithm is conceptually simple: evict the
page that will be accessed furthest in the future. If we knew the
future, we\'d evict the page that won\'t be needed for the longest time.
This \"MIN\" or \"Bélády\'s\" algorithm is provably optimal---it
produces the minimum number of page faults.

Unfortunately, predicting the future is impossible. The next best thing
is to assume that the past predicts the future---that is, pages accessed
recently will likely be accessed again soon (temporal locality). This
gives us Least Recently Used (LRU): evict the page that hasn\'t been
accessed for the longest time.

Perfect LRU would require tracking the exact time of last access for
every page:

``` {.sourceCode .c}
// Perfect LRU (theoretical)
struct lru_page {
    struct page *page;
    uint64_t last_access_timestamp;  // Nanosecond precision
};

struct page *perfect_lru_evict(void) {
    struct lru_page *victim = NULL;
    uint64_t oldest_time = UINT64_MAX;
    
    // Scan all pages to find least recently used
    for_each_page(page) {
        if (page->last_access_timestamp < oldest_time) {
            oldest_time = page->last_access_timestamp;
            victim = page;
        }
    }
    
    return victim->page;
}

// This would require updating timestamp on EVERY memory access!
void on_every_memory_access(unsigned long va) {
    struct page *page = va_to_page(va);
    page->last_access_timestamp = get_nanoseconds();
    
    // Also need to maintain sorted list or heap
    // to avoid O(n) scan on every eviction
    update_lru_ordering(page);
}
```

The problem is catastrophic overhead:

    Cost analysis for perfect LRU:

    Memory overhead:
      - 8 bytes per page for timestamp
      - For 16 GB RAM: 4M pages × 8 bytes = 32 MB just for timestamps

    Update overhead (the killer):
      - Update on EVERY memory access
      - At 10 billion accesses/second: 10B timestamp updates/sec
      - Each update: read timestamp, write new value, potentially update ordering
      - Minimum: 10B × 10 ns = 100 seconds of CPU per second!
      - Impossible—CPU would spend all time updating timestamps

    Contention overhead:
      - Multiple cores accessing same pages
      - Cache line bouncing on timestamp updates
      - Lock contention if maintaining ordered list
      - Performance collapse in SMP systems

Perfect LRU is a theoretical ideal, not a practical implementation. Real
systems approximate LRU using the Accessed bit and clever data
structures.

> ⚠️ **PERFORMANCE TRAP**
>
> Trying to track exact access ordering would require updating state on
> every memory access. At modern memory access rates (billions per
> second), even a single atomic increment per access would consume 100%
> of CPU time. The solution is to approximate---track coarse-grained
> access information (accessed in last N seconds) rather than exact
> timestamps.

### 8.5.2 Clock Algorithm: Practical LRU Approximation

The Clock algorithm, also called \"Second Chance,\" elegantly
approximates LRU using only the Accessed bit. It organizes pages in a
circular list (like a clock face) and uses a clock hand to scan through
them:

``` {.sourceCode .c}
// Clock algorithm implementation
struct clock_eviction {
    struct page **pages;      // Circular array of pages
    unsigned int clock_hand;  // Current position (like clock hand)
    unsigned int nr_pages;    // Total pages in clock
};

struct page *clock_algorithm_evict(struct clock_eviction *clock) {
    struct page *victim;
    unsigned int scanned = 0;
    
    // Scan in circular fashion until we find a victim
    while (1) {
        struct page *page = clock->pages[clock->clock_hand];
        pte_t *pte = get_pte_for_page(page);
        
        // Check the Accessed bit
        if (pte_young(*pte)) {
            // Accessed recently—give it a second chance
            // Clear the A bit and move on
            // If accessed again before we return, survives another round
            *pte = pte_mkold(*pte);
            
            // Advance clock hand
            clock->clock_hand = (clock->clock_hand + 1) % clock->nr_pages;
            scanned++;
            
        } else {
            // A bit is 0—not accessed since last time we cleared it
            // This page has had its second chance and wasn't used
            // Evict it
            victim = page;
            
            // Remove from clock (shift remaining pages)
            for (unsigned int i = clock->clock_hand; i < clock->nr_pages - 1; i++) {
                clock->pages[i] = clock->pages[i + 1];
            }
            clock->nr_pages--;
            
            // If we scanned many pages, might need TLB flush
            if (scanned > 32) {
                flush_tlb_all();
            }
            
            return victim;
        }
        
        // Safety: prevent infinite loop
        if (scanned > clock->nr_pages * 2) {
            // All pages accessed—just take first one
            return clock->pages[clock->clock_hand];
        }
    }
}

/* Based on classic Clock algorithm
   Reference: Corbató, F. J. (1968) "A paging experiment with the Multics system" */
```

Here\'s how it works in practice:

    Initial state (all pages recently accessed):
      Pages: [A=1] [B=1] [C=1] [D=1] [E=1]
              ^hand

    Need to evict one page:

    Scan #1: Check page A
      - A=1, so clear to A=0, advance hand
      Pages: [A=0] [B=1] [C=1] [D=1] [E=1]
                    ^hand

    Scan #2: Check page B
      - B=1, so clear to B=0, advance hand
      Pages: [A=0] [B=0] [C=1] [D=1] [E=1]
                           ^hand

    Scan #3: Check page C
      - C=1, so clear to C=0, advance hand
      Pages: [A=0] [B=0] [C=0] [D=1] [E=1]
                                  ^hand

    Scan #4: Check page D
      - D=1, so clear to D=0, advance hand
      Pages: [A=0] [B=0] [C=0] [D=0] [E=1]
                                         ^hand

    Scan #5: Check page E
      - E=1, so clear to E=0, wrap around
      Pages: [A=0] [B=0] [C=0] [D=0] [E=0]
             ^hand

    Scan #6: Check page A again
      - A=0, so EVICT page A
      Pages: [B=0] [C=0] [D=0] [E=0]
             ^hand

The beauty of Clock: pages get a second chance. If page A is accessed
between Scan #1 and Scan #6, hardware sets A=1 again, and it survives:

    Same scenario, but page A accessed after Scan #1:

    After Scan #1: Pages: [A=0] [B=1] [C=1] [D=1] [E=1]
    Application accesses page A → hardware sets A=1
    Now: Pages: [A=1] [B=1] [C=1] [D=1] [E=1]

    ...scans continue...

    Scan #6: Check page A
      - A=1 (was accessed!), clear to A=0, advance
      - Page A survives this round

    Continue scanning for a page with A=0...

> 💡 **KEY INSIGHT**
>
> Clock gives pages a \"second chance\" by clearing the A bit instead of
> immediately evicting. Only pages that remain unused for a full
> rotation of the clock hand get evicted. This binary approximation
> (used-in-last-rotation vs not-used) is much cheaper than perfect
> LRU\'s exact timestamps but still captures temporal locality
> effectively.

Performance characteristics:

    Average case (moderate memory pressure):
      - Scan 5-10 pages before finding A=0
      - Cost: 10 × 10 ns (check A bit) + 50 µs (TLB flush) ≈ 50 µs per eviction

    Worst case (extreme memory pressure, all pages hot):
      - Scan all pages, all have A=1
      - Clear all, scan again, take first
      - Cost: 2 × nr_pages × 10 ns + TLB flush
      - For 100,000 pages: 2 × 100k × 10ns + 50µs = 2050 µs = 2ms

    Best case (memory pressure eases):
      - First page checked has A=0
      - Cost: 10 ns + 50 µs ≈ 50 µs

    Amortized: O(1) per eviction assuming reasonable mix of hot/cold pages

Clock is simple, effective, and used (with variations) in many operating
systems including early UNIX variants and embedded systems.

### 8.5.3 Enhanced Clock: Two Lists

Basic Clock doesn\'t distinguish between clean and dirty pages. Recall
from Section 8.4 that evicting dirty pages is 50-5000× more expensive
than clean pages (depending on storage speed). Modern systems use a
two-list enhancement:

``` {.sourceCode .c}
// Two-list LRU
struct lruvec {
    struct list_head inactive_list;  // Candidates for eviction
    struct list_head active_list;    // Recently accessed pages
    
    unsigned long nr_inactive;
    unsigned long nr_active;
    
    // Target ratio: typically 2:1 (active:inactive)
    unsigned long target_inactive_ratio;
};

// Move pages from active to inactive based on A bit
void refill_inactive_list(struct lruvec *lru) {
    struct page *page, *next;
    unsigned long target = lru->nr_active / lru->target_inactive_ratio;
    
    // Scan active list until inactive list is large enough
    list_for_each_entry_safe(page, next, &lru->active_list, lru) {
        if (lru->nr_inactive >= target)
            break;
        
        pte_t *pte = get_pte_for_page(page);
        
        if (pte_young(*pte)) {
            // Still being accessed—clear bit and keep in active
            *pte = pte_mkold(*pte);
            
            // Move to tail of active list (make it "younger" in the list)
            list_move_tail(&page->lru, &lru->active_list);
            
        } else {
            // Not accessed recently—demote to inactive
            list_move(&page->lru, &lru->inactive_list);
            lru->nr_active--;
            lru->nr_inactive++;
        }
    }
    
    // Flush TLB if we cleared many A bits
    flush_tlb_all();
}

// Evict from inactive list
struct page *evict_from_inactive(struct lruvec *lru) {
    struct page *page, *next;
    
    list_for_each_entry_safe(page, next, &lru->inactive_list, lru) {
        pte_t *pte = get_pte_for_page(page);
        
        // Last-minute check: was it accessed while in inactive?
        if (pte_young(*pte)) {
            // Accessed! Promote back to active
            *pte = pte_mkold(*pte);
            list_move(&page->lru, &lru->active_list);
            lru->nr_inactive--;
            lru->nr_active++;
            continue;  // Don't evict this one
        }
        
        // Prefer clean pages for eviction
        if (!pte_dirty(*pte)) {
            // Clean page—evict immediately
            list_del(&page->lru);
            lru->nr_inactive--;
            return page;
        }
    }
    
    // All inactive pages are dirty—must evict one anyway
    // Take first dirty page
    page = list_first_entry(&lru->inactive_list, struct page, lru);
    list_del(&page->lru);
    lru->nr_inactive--;
    
    return page;
}

/* Conceptual implementation based on Linux mm/vmscan.c
   Reference: shrink_active_list() and shrink_inactive_list() */
```

Page lifecycle in two-list LRU:

    1. Page allocated → Added to active list (A=1)
       Assumption: newly allocated pages likely to be used

    2. Periodic scan of active list:
       - If A=1: Clear A bit, keep in active
       - If A=0: Demote to inactive list
       
    3. Page in inactive list:
       - If accessed: Promote back to active (A=1)
       - If not accessed: Candidate for eviction
       
    4. Eviction from inactive:
       - Scan inactive list
       - Prefer clean pages (D=0)
       - Last-minute promotion if A=1
       - Evict first suitable page

This provides better behavior than single-list Clock:

    Comparison: Single-list Clock vs Two-list LRU

    Scenario: Working set of 1000 pages, need to evict 100 pages

    Single-list Clock:
      - Scan through all 1000 pages
      - Clear A bits on 900 hot pages
      - Find 100 pages with A=0
      - Cost: 1000 scans + 1 TLB flush = ~50 µs
      
    Two-list LRU:
      - Active list has 900 pages (working set)
      - Inactive list has 100 pages (not in working set)
      - Scan only inactive list (100 pages)
      - Cost: 100 scans + 1 TLB flush = ~20 µs
      
    Speed-up: 2.5× faster for eviction

    Additional benefit:
      - Naturally separates hot (active) from cold (inactive)
      - Protects working set from one-time scans
      - Prioritizes clean pages (faster to evict)

The two-list approach also handles the \"scan problem\" better. Imagine
a process that scans through a 2 GB file once. With single-list Clock,
those 2 GB of pages would pollute the entire clock, potentially evicting
the actual working set. With two-list LRU, scan pages enter active but
quickly demote to inactive when not re-accessed, limiting their impact.

### 8.5.4 Multi-Generational LRU (MGLRU): Linux\'s Modern Approach

Linux 5.18+ introduces Multi-Generational LRU, which takes the two-list
concept further by using four generations of pages. Instead of just
\"active\" and \"inactive,\" pages age through generations based on
their access patterns:

``` {.sourceCode .c}
// MGLRU: Four generations
#define MAX_NR_GENS 4

struct lru_gen {
    // Four lists, one per generation
    struct list_head lists[MAX_NR_GENS][ANON_AND_FILE];
    
    // Generation numbers (continuously incrementing)
    unsigned long min_seq;  // Oldest generation
    unsigned long max_seq;  // Youngest generation
    
    // At any time, we have 4 active generations:
    // - max_seq (newest, generation 3)
    // - max_seq - 1 (generation 2)
    // - max_seq - 2 (generation 1)
    // - min_seq = max_seq - 3 (oldest, generation 0)
    
    // Timestamps for aging decisions
    unsigned long timestamps[MAX_NR_GENS];
};

// Mark a page as accessed—move to youngest generation
void mglru_mark_page_accessed(struct lru_gen *lrugen, struct page *page) {
    unsigned int youngest_gen = lrugen->max_seq % MAX_NR_GENS;
    
    // Move to youngest generation list
    list_move(&page->lru, &lrugen->lists[youngest_gen][page_type(page)]);
    
    // Record this page is in the youngest generation
    page->flags = (page->flags & ~PAGE_GEN_MASK) | lrugen->max_seq;
}

// Age pages through generations
void mglru_age_generations(struct lru_gen *lrugen) {
    unsigned int gen;
    struct page *page;
    
    // Scan the current youngest generation
    unsigned int scan_gen = lrugen->max_seq % MAX_NR_GENS;
    
    list_for_each_entry(page, &lrugen->lists[scan_gen][ANON], lru) {
        pte_t *pte = get_pte_for_page(page);
        
        if (pte_young(*pte)) {
            // Accessed—stays in youngest generation
            *pte = pte_mkold(*pte);
        } else {
            // Not accessed—will age to next generation
            // This happens automatically when we increment max_seq below
        }
    }
    
    // Create a new generation
    lrugen->max_seq++;
    lrugen->min_seq++;  // Oldest generation now "falls off"
    lrugen->timestamps[lrugen->max_seq % MAX_NR_GENS] = jiffies;
    
    // Pages that weren't accessed stay in their old generation slot
    // which is now one generation older relative to max_seq
}

// Evict from oldest generation
struct page *mglru_evict_page(struct lru_gen *lrugen) {
    unsigned int oldest_gen = lrugen->min_seq % MAX_NR_GENS;
    struct page *page;
    
    // Try to evict from oldest generation
    list_for_each_entry(page, &lrugen->lists[oldest_gen][ANON], lru) {
        pte_t *pte = get_pte_for_page(page);
        
        // Last-chance check
        if (pte_young(*pte)) {
            // Accessed! Promote to youngest generation
            mglru_mark_page_accessed(lrugen, page);
            continue;
        }
        
        // Not accessed for 4 full generations—safe to evict
        list_del(&page->lru);
        return page;
    }
    
    // Oldest generation empty or all pages accessed
    return NULL;
}

/* Conceptual implementation based on Linux MGLRU by Yu Zhao
   Reference: mm/vmscan.c in Linux 5.18+ */
```

How MGLRU filters pages over time:

    Hot page (frequently accessed):
      Gen 3: Accessed → stays in Gen 3
      Gen 3: Accessed again → stays in Gen 3
      Gen 3: Accessed repeatedly → always in Gen 3
      Never ages beyond Gen 3, never evicted

    Warm page (occasionally accessed):
      Gen 3: Accessed → stays in Gen 3
      Gen 2: Not accessed → ages from 3→2
      Gen 3: Accessed again → promoted back to Gen 3
      Gen 2: Not accessed → ages 3→2 again
      Bounces between Gen 2-3, rarely evicted

    Cool page (rarely accessed):
      Gen 3: Accessed once → stays in Gen 3
      Gen 2: Not accessed → ages to Gen 2
      Gen 1: Not accessed → ages to Gen 1
      Gen 3: Accessed (one-time scan) → back to Gen 3
      Gen 2: Not accessed → ages to Gen 2
      Eventually evicted from Gen 0

    Cold page (never accessed):
      Gen 3: Not accessed → ages to Gen 2
      Gen 2: Not accessed → ages to Gen 1
      Gen 1: Not accessed → ages to Gen 0
      Gen 0: Not accessed → EVICTED
      Takes 4 generation cycles to evict

The multi-generation approach provides better filtering than two-list
LRU:

> 💡 **KEY INSIGHT**
>
> MGLRU requires pages to be NOT accessed for MULTIPLE scan periods
> before evicting them. A page touched once during a sequential file
> scan will enter Gen 3 but won\'t survive aging through Gen 2→1→0
> without repeated access. This filters out one-time scans that pollute
> simpler LRU variants, while true working set pages (accessed
> repeatedly) remain in Gen 3.

Real-world performance improvement:

> 📊 **REAL NUMBERS - MGLRU EFFECTIVENESS**
>
> **Benchmark: Kernel compilation under memory pressure (4 GB RAM, 6 GB
> needed)**
>
> **Classic two-list LRU (Linux 5.17):** - Compile time: 11m 23s - Page
> faults: 2,147,832 - Incorrect evictions (pages evicted then faulted
> back soon): \~340,000
>
> **MGLRU (Linux 6.1):** - Compile time: 9m 12s (19% faster!) - Page
> faults: 1,738,924 (19% reduction) - Incorrect evictions: \~189,000
> (44% reduction!)
>
> The four-generation filtering dramatically reduces thrashing by better
> identifying truly cold pages versus temporarily unused pages.

The cost of MGLRU is minimal: four list heads instead of two (negligible
memory), and slightly more complex aging logic (still O(1) per page).
The benefits---fewer bad eviction decisions and less
thrashing---outweigh the costs for virtually all workloads.

------------------------------------------------------------------------

## 8.6 Memory Reclaim: The Timing and Urgency

Page replacement algorithms tell us **which** pages to evict. But they
don\'t tell us **when** to start evicting, **how many** to evict at
once, or **how aggressively** to reclaim. That\'s the job of the memory
reclaim subsystem.

### 8.6.1 Watermarks: Three Levels of Urgency

Linux maintains three watermark levels per memory zone to detect and
respond to memory pressure:

``` {.sourceCode .c}
// Per-zone watermarks
struct zone {
    unsigned long watermark[NR_WMARK];
    unsigned long nr_free_pages;
    
    // Other zone state...
};

enum zone_watermarks {
    WMARK_MIN,   // Minimum free—critical level
    WMARK_LOW,   // Low free—warning level
    WMARK_HIGH,  // High free—comfortable level
    NR_WMARK
};
```

These watermarks define three distinct states:

The kernel checks watermarks on every allocation:

``` {.sourceCode .c}
bool zone_watermark_ok(struct zone *zone, unsigned int order,
                       unsigned long mark) {
    unsigned long free_pages = zone_page_state(zone, NR_FREE_PAGES);
    unsigned long min = mark;
    
    // Adjust minimum for high-order allocations
    // Larger contiguous allocations need more free pages
    min += (1UL << order);
    
    // Reserve some memory for atomic allocations
    // (interrupts, network packets, etc. that can't wait)
    min += zone->lowmem_reserve;
    
    return free_pages >= min;
}
```

Tuning watermarks affects system behavior:

``` {.sourceCode .bash}
# View current setting
cat /proc/sys/vm/min_free_kbytes
# 65536 (64 MB on this system)

# Increase for latency-sensitive workloads
# More reserved memory = less likely to hit direct reclaim
echo 262144 > /proc/sys/vm/min_free_kbytes  # 256 MB

# This automatically scales LOW and HIGH proportionally
# min=256 MB → low=384 MB → high=512 MB

# Decrease for memory-constrained systems
# Less reserved = more usable for applications
echo 16384 > /proc/sys/vm/min_free_kbytes   # 16 MB
# But risk more frequent direct reclaim
```

### 8.6.2 kswapd: The Background Reclaimer

The kernel thread `kswapd` runs on each NUMA node, performing background
memory reclamation:

``` {.sourceCode .c}
// kswapd main loop (simplified)
int kswapd(void *p) {
    struct pglist_data *pgdat = (struct pglist_data *)p;
    
    set_freezable();
    
    // Main loop
    while (!kthread_should_stop()) {
        // Sleep until woken (memory drops below low watermark)
        wait_event_freezable(pgdat->kswapd_wait,
                            kswapd_should_run(pgdat));
        
        // Reclaim until high watermark reached
        unsigned long nr_reclaimed = 0;
        
        while (below_high_watermark(pgdat)) {
            // Reclaim in batches (typically 32 pages at a time)
            // This prevents monopolizing CPU
            nr_reclaimed += shrink_node(pgdat, 32);
            
            // Yield CPU periodically
            if (nr_reclaimed > 1024) {
                schedule();  // Let other tasks run
                nr_reclaimed = 0;
            }
            
            // Safety: if we're making no progress, give up
            if (nr_reclaimed == 0)
                break;
        }
    }
    
    return 0;
}

/* Based on Linux kernel mm/vmscan.c
   Reference: kswapd() function */
```

The timeline of background reclaim:

    T0:    Free memory: 80 MB (above low watermark of 64 MB)
           kswapd: sleeping

    T1:    Application allocates memory
           Free memory drops to 60 MB
           → Crosses low watermark (64 MB)
           → Wake kswapd

    T2:    kswapd starts working
           Scans LRU lists, identifies cold pages
           Evicts 32 pages (128 KB)
           Free memory: 60.125 MB

    T3:    Application continues allocating
           Free memory: 58 MB

    T4:    kswapd continues reclaiming
           Evicts another 32 pages
           Free memory: 58.125 MB

           ...this continues for ~100 iterations...

    T50:   Free memory reaches 97 MB
           → Above high watermark (96 MB)
           → kswapd goes back to sleep

    Total time: ~50 milliseconds of background work
    Applications barely noticed

kswapd runs with low priority and yields frequently, so it doesn\'t
interfere with application workloads. The goal is to reclaim memory
proactively, before applications run out.

> 💡 **KEY INSIGHT**
>
> kswapd is the kernel\'s \"garbage collector\" for memory. It runs in
> the background when memory gets low, freeing up space before
> applications actually need it. Most of the time on a well-tuned
> system, kswapd keeps up with demand and applications never experience
> allocation failures or delays.

### 8.6.3 Direct Reclaim: When kswapd Can\'t Keep Up

When memory pressure is severe or sudden, kswapd can\'t keep up. In this
case, the allocating process must reclaim memory itself---direct
reclaim:

``` {.sourceCode .c}
// Allocation path with direct reclaim
struct page *__alloc_pages_slowpath(gfp_t gfp_mask, unsigned int order) {
    struct page *page;
    
    // Try fast allocation first
    page = get_page_from_freelist(gfp_mask, order);
    if (page)
        return page;  // Lucky! Found free page
    
    // No luck—wake kswapd if not already running
    wakeup_all_kswapds(order);
    
    // Give kswapd a chance to work
    wait_for_completion_timeout(&kswapd_done, msecs_to_jiffies(100));
    
    // Try again
    page = get_page_from_freelist(gfp_mask, order);
    if (page)
        return page;  // kswapd freed enough
    
    // Still no memory—time for DIRECT RECLAIM
    // The calling process must do the work itself
    if (gfp_mask & __GFP_DIRECT_RECLAIM) {
        unsigned long nr_reclaimed;
        
        // Reclaim synchronously (blocks the caller!)
        nr_reclaimed = try_to_free_pages(zonelist, order, gfp_mask);
        
        if (nr_reclaimed) {
            // Freed some pages, try allocation again
            page = get_page_from_freelist(gfp_mask, order);
            if (page)
                return page;
        }
    }
    
    // Desperate: invoke OOM killer
    if (gfp_mask & __GFP_NOFAIL) {
        page = __alloc_pages_may_oom(gfp_mask, order);
    }
    
    return NULL;  // Allocation failed
}

/* Based on Linux kernel mm/page_alloc.c
   Reference: __alloc_pages_slowpath() */
```

The disaster timeline---direct reclaim blocking an application:

    Application calls malloc(1 MB):

    T0:     Allocation request
    T1:     Fast path: No free pages available
    T2:     Wake kswapd (if sleeping)
    T100ms: Wait 100ms for kswapd to free pages
    T100ms: Still no free pages!
    T100ms: Enter DIRECT RECLAIM
    T100ms: Scan inactive list for eviction candidates
    T101ms: Found 100 pages to evict (32 clean, 68 dirty)
    T102ms: Evict 32 clean pages instantly (1 ms)
    T102ms: Must evict 68 dirty pages
    T102ms: Write first dirty page to disk
    T107ms: First page written (5 ms disk latency)
    T107ms: Write second dirty page...
            ...
    T442ms: All 68 pages written (68 × 5 ms = 340 ms)
    T443ms: Free memory now available
    T443ms: Allocation succeeds
    T443ms: malloc() FINALLY returns after 443 milliseconds!

> ⚠️ **PERFORMANCE TRAP**
>
> Direct reclaim blocks the allocating process, turning a
> normally-microsecond memory allocation into a potentially multi-second
> operation. If the allocating process is handling a user request (web
> server, database query, UI interaction), the user experiences a
> freeze. This is why tuning watermarks to avoid direct reclaim is
> critical for predictable latency.

Real-world impact:

    Example: Web server handling HTTP request

    Normal path (plenty of memory):
      malloc(): 50 µs
      Total request: 50 ms
      
    With direct reclaim:
      malloc(): 443 ms (8860× slower!)
      Total request: 493 ms
      User experience: 10× slower page load
      
    Example: Database query

    Normal path:
      Query execution: 5 ms
      
    With direct reclaim:
      malloc() during query: 443 ms
      Query execution: 448 ms (90× slower!)
      User experience: Timeout (application expects <100ms)

Direct reclaim is unpredictable and can strike any allocation at any
time. The only defense is keeping memory above the low watermark through
adequate physical RAM and proper `min_free_kbytes` tuning.

### 8.6.4 vm.swappiness: Balancing Anonymous vs File Pages

The `vm.swappiness` sysctl controls the kernel\'s preference for
evicting anonymous pages (swap) versus file-backed pages (drop from
cache):

``` {.sourceCode .c}
// vm.swappiness range: 0-200, default 60
int vm_swappiness = 60;

void get_scan_count(struct lruvec *lruvec, struct scan_control *sc,
                    unsigned long *nr) {
    unsigned long anon_prio, file_prio;
    
    // Calculate priorities based on swappiness
    // Higher swappiness = more willing to swap anonymous pages
    // Lower swappiness = prefer evicting file pages
    anon_prio = swappiness;
    file_prio = 200 - swappiness;
    
    // Weight by actual page counts
    unsigned long ap = anon_prio * lruvec->nr_anon_pages;
    unsigned long fp = file_prio * lruvec->nr_file_pages;
    
    unsigned long total = ap + fp;
    
    // Divide scan budget proportionally
    nr[LRU_ANON] = (ap * sc->nr_to_scan) / total;
    nr[LRU_FILE] = (fp * sc->nr_to_scan) / total;
}

/* Based on Linux kernel mm/vmscan.c */
```

What different swappiness values mean:

``` {.sourceCode .bash}
# vm.swappiness=0: Never swap (almost)
# Only swap in absolutely desperate OOM scenarios
# Aggressively evict file pages instead
sysctl vm.swappiness=0

# Effect:
# - File cache evicted first
# - Anonymous pages (app memory) kept in RAM
# - Good for: Databases, applications with critical working sets
# - Bad for: Systems with important file caches

# vm.swappiness=1: Minimal swapping (recommended for databases)
sysctl vm.swappiness=1

# Effect:
# - Strongly prefer file eviction
# - Only swap when file cache exhausted
# - Good for: Database servers, Redis, Memcached
# - PostgreSQL, MySQL often recommend this

# vm.swappiness=60: Balanced (default)
sysctl vm.swappiness=60

# Effect:
# - Balance anonymous and file eviction
# - Evict based on actual access patterns
# - Good for: General-purpose systems, desktops

# vm.swappiness=100: Treat anonymous and file equally
sysctl vm.swappiness=100

# Effect:
# - No preference between swapping and file eviction
# - Swap more aggressively
# - Good for: Systems with fast SSDs, heavy file I/O workloads
```

Real example: Database server tuning

    PostgreSQL server configuration:
      RAM: 64 GB
      shared_buffers: 48 GB (database buffer cache)
      Work_mem allocations: Several GB
      
    Problem with vm.swappiness=60 (default):
      Under memory pressure:
      - Kernel balanced between swap and file eviction
      - Swapped out 2 GB of PostgreSQL buffers
      - Database queries hit swap instead of RAM
      - Query latency: 5 ms → 150 ms (30× slower!)
      - Throughput collapsed
      
    Solution: vm.swappiness=1
      Under same memory pressure:
      - Kernel evicted file cache instead
      - PostgreSQL buffers stayed in RAM
      - Query latency: 5 ms (unchanged)
      - Throughput maintained
      
    Result: One sysctl tuning prevented 30× performance degradation!

### 8.6.5 OOM Killer: The Nuclear Option

When all reclaim efforts fail and memory is critically low, the kernel
invokes the Out-Of-Memory killer:

``` {.sourceCode .c}
// OOM killer decision process
void out_of_memory(struct oom_control *oc) {
    struct task_struct *victim;
    
    // Can we even kill anything?
    if (oom_killer_disabled)
        return;
    
    // Try one more reclaim attempt
    if (try_to_free_mem_cgroup_pages(oc->memcg))
        return;  // Success! No need to kill
    
    // Select victim based on badness score
    victim = select_bad_process(oc);
    
    if (!victim) {
        // No process can be killed (all critical)
        panic("Out of memory and no killable process");
    }
    
    // Log the kill for debugging
    pr_err("Out of memory: Killed process %d (%s) "
           "total-vm:%luKB, anon-rss:%luKB, file-rss:%luKB, "
           "shmem-rss:%luKB, UID:%u\n",
           victim->pid, victim->comm,
           K(victim->mm->total_vm),
           K(get_mm_counter(victim->mm, MM_ANONPAGES)),
           K(get_mm_counter(victim->mm, MM_FILEPAGES)),
           K(get_mm_counter(victim->mm, MM_SHMEMPAGES)),
           from_kuid(&init_user_ns, task_uid(victim)));
    
    // Send SIGKILL
    do_send_sig_info(SIGKILL, SEND_SIG_FORCED, victim, PIDTYPE_PID);
    
    mark_oom_victim(victim);
}

// Calculate badness score
unsigned long oom_badness(struct task_struct *p,
                         unsigned long totalpages) {
    long points = 0;
    
    // Primary factor: memory usage as percentage of total RAM
    points = get_mm_rss(p->mm);  // Resident pages
    points += get_mm_counter(p->mm, MM_SWAPENTS);  // Swapped pages
    points += p->mm->total_vm / 2;  // Virtual memory (half weight)
    
    // Convert to points (0-1000)
    points = points * 1000 / totalpages;
    
    // User adjustment
    points += p->signal->oom_score_adj;
    
    // Special cases
    if (is_global_init(p))
        return 0;  // Never kill init (PID 1)
    
    if (p->flags & PF_KTHREAD)
        return 0;  // Never kill kernel threads
    
    // Root processes get -25% adjustment
    if (has_capability_noaudit(p, CAP_SYS_ADMIN))
        points -= points / 4;
    
    return points < 0 ? 0 : points;
}

/* Based on Linux kernel mm/oom_kill.c */
```

The OOM killer\'s selection:

    System state during OOM:
      Total RAM: 8 GB
      Free memory: 2 MB (critical!)
      
    Process list and scores:
      PID 1    init        RSS:12 MB    Score:0      (never kill)
      PID 145  sshd        RSS:8 MB     Score:5      (system service, root)
      PID 1234 chrome      RSS:2.5 GB   Score:850    ← HIGHEST SCORE
      PID 2341 postgres    RSS:1.8 GB   Score:420    (oom_adj=-100 protection)
      PID 3456 httpd       RSS:500 MB   Score:180
      PID 4567 cron        RSS:4 MB     Score:2
      
    OOM killer decision:
      "Killed process 1234 (chrome) total-vm:2621440kB"
      
    Why chrome?
      - Highest memory usage
      - No protection (oom_score_adj=0)
      - Not a system-critical process
      - Badness score: 850/1000

Protecting critical processes:

``` {.sourceCode .bash}
# Protect PostgreSQL from OOM killer
# Negative oom_score_adj makes it less likely to be killed
echo -500 > /proc/$(pidof postgres)/oom_score_adj

# Make a batch job more likely to be killed
echo 500 > /proc/$(pidof batch_job)/oom_score_adj

# Completely disable OOM kill for a process (dangerous!)
echo -1000 > /proc/$(pidof critical_service)/oom_score_adj
```

------------------------------------------------------------------------

## 8.7 Page Table Management: Metadata Memory

We\'ve focused on managing data pages. But page tables themselves
consume memory---sometimes significant amounts. When and how do we
manage this metadata?

### 8.7.1 Calculating Page Table Overhead

For x86-64 with 4-level page tables, the overhead depends on how dense
or sparse the address space is:

``` {.sourceCode .c}
// Page table overhead calculation
unsigned long calc_pt_overhead(unsigned long mapped_bytes) {
    unsigned long pages = mapped_bytes / PAGE_SIZE;  // 4KB pages
    
    // Level 1: Page Tables (PTs)
    // One PTE (8 bytes) per page, 512 PTEs per 4KB PT
    unsigned long nr_pts = (pages + 511) / 512;
    
    // Level 2: Page Directories (PDs)
    // One PDE per PT, 512 PDEs per 4KB PD
    unsigned long nr_pds = (nr_pts + 511) / 512;
    
    // Level 3: PDPTs
    // One PDPTE per PD, 512 PDPTEs per 4KB PDPT
    unsigned long nr_pdpts = (nr_pds + 511) / 512;
    
    // Level 4: PML4 (always 1)
    unsigned long nr_pml4s = 1;
    
    // Total pages used for page tables
    unsigned long total_pt_pages = nr_pts + nr_pds + nr_pdpts + nr_pml4s;
    
    return total_pt_pages * PAGE_SIZE;
}

// Example: Process mapping 10 GB
//   10 GB = 2,621,440 pages
//   PTs:   2,621,440 / 512 = 5,120 (20 MB)
//   PDs:   5,120 / 512 = 10 (40 KB)
//   PDPTs: 10 / 512 = 1 (4 KB)
//   PML4:  1 (4 KB)
//   Total: 20,528 KB ≈ 20 MB (0.2% of 10 GB)
```

This seems small---0.2% overhead for dense mappings. But scale matters:

    Small system (8 GB RAM, 20 processes):
      Average 2 GB per process
      Page tables: 20 × 4 MB = 80 MB total
      Impact: 1% of RAM—negligible
      
    Large system (256 GB RAM, 500 processes):
      Average 10 GB per process
      Page tables: 500 × 20 MB = 10 GB total
      Impact: 4% of RAM—noticeable
      
    VM host (1 TB RAM, 100 VMs × 32 GB each):
      Guest page tables: 100 × 64 MB = 6.4 GB
      Host EPT tables: 100 × 64 MB = 6.4 GB
      Total: 12.8 GB (1.3% of RAM)
      Impact: Could run 3 more VMs without this overhead

> 📊 **REAL NUMBERS - PAGE TABLE OVERHEAD AT SCALE**
>
> **Measured on production database server:** - Total RAM: 512 GB -
> Running processes: 150 (mostly database workers) - Total RSS: 380 GB -
> Page table overhead: 6.8 GB - Percentage: 1.8% of RSS, 1.3% of total
> RAM
>
> **Impact:** That 6.8 GB could be used for database buffers instead. At
> \$50/GB/month for cloud RAM, that\'s \$340/month wasted on page table
> metadata.

### 8.7.2 Lazy Allocation: Saving Memory

Operating systems don\'t allocate all page table levels upfront. They
use lazy allocation---create page tables only when pages are actually
accessed:

``` {.sourceCode .c}
// Page fault handler allocates page tables on-demand
int handle_pte_fault(struct vm_area_struct *vma, unsigned long address,
                     pte_t *pte, pmd_t *pmd, unsigned int flags) {
    // If we get here, upper levels (PML4, PDPT, PD) already exist
    // They were allocated by the fault path walk
    
    if (pte_none(*pte)) {
        // PTE doesn't exist yet—this is a true page fault
        return do_fault(vma, address, pte, pmd, flags);
    }
    
    // PTE exists, handle other fault types
    // ...
}

// Walking page tables allocates missing levels
pte_t *get_pte_with_allocation(struct mm_struct *mm, unsigned long address) {
    pgd_t *pgd;
    p4d_t *p4d;
    pud_t *pud;
    pmd_t *pmd;
    pte_t *pte;
    
    // PML4 always exists (allocated at mm_struct creation)
    pgd = pgd_offset(mm, address);
    
    // Allocate P4D if needed (on some architectures, same as PGD)
    p4d = p4d_alloc(mm, pgd, address);
    if (!p4d)
        return NULL;
    
    // Allocate PDPT if needed
    pud = pud_alloc(mm, p4d, address);
    if (!pud)
        return NULL;
    
    // Allocate PD if needed
    pmd = pmd_alloc(mm, pud, address);
    if (!pmd)
        return NULL;
    
    // Allocate PT if needed
    pte = pte_alloc(mm, pmd, address);
    if (!pte)
        return NULL;
    
    return pte;
}

/* Based on Linux kernel mm/memory.c */
```

Savings from lazy allocation are dramatic for sparse address spaces:

    Example: Typical user process address space

    Code segment:     0x00400000 - 0x00500000 (1 MB)
    Libraries:        0x7F000000 - 0x7F800000 (8 MB)
    Heap:             0x10000000 - 0x20000000 (256 MB)
    Stack:            0x7FFFFFFFE000 - 0x7FFFFFFFF000 (4 MB)

    Total mapped: ~270 MB spread across 256 TB address space!

    Eager allocation (allocate everything):
      Would need page tables for entire 256 TB space
      Cost: Gigabytes of page tables for empty space
      Completely impractical
      
    Lazy allocation (allocate on-demand):
      PML4: 1 page (4 KB) - always exists
      PDPTs: 3 pages (12 KB) - one for code, one for heap, one for stack
      PDs: 5 pages (20 KB) - code/libs share, heap has several, stack has one
      PTs: 70 pages (280 KB) - only for actually-used pages
      Total: ~316 KB
      
    Savings: Gigabytes → 316 KB = Millions-fold reduction!

> 💡 **KEY INSIGHT**
>
> Lazy page table allocation is why sparse address spaces work at all. A
> process can have a massive 256 TB virtual address space but only pays
> for the page tables it actually uses. Without lazy allocation, every
> process would need gigabytes just for empty page table structures.

### 8.7.3 Page Table Reclamation Under Pressure

When memory is tight, the kernel can reclaim empty page tables:

``` {.sourceCode .c}
// Check if page table is completely empty
bool page_table_empty(pte_t *pte_base) {
    for (int i = 0; i < PTRS_PER_PTE; i++) {
        if (!pte_none(pte_base[i]))
            return false;  // Found a valid entry
    }
    return true;  // All entries are empty
}

// Free empty page tables
void free_empty_page_tables(struct mm_struct *mm, unsigned long start,
                           unsigned long end) {
    unsigned long addr;
    
    for (addr = start; addr < end; addr += PMD_SIZE) {
        pmd_t *pmd = pmd_offset(..., addr);
        
        if (!pmd_present(*pmd))
            continue;  // Already freed
        
        pte_t *pte_base = pte_offset_map(pmd, addr);
        
        if (page_table_empty(pte_base)) {
            // This PT is empty—free it
            pte_free(mm, pte_base);
            pmd_clear(pmd);
            
            // Also check if PD is now empty and can be freed
            check_and_free_pd_if_empty(mm, pmd);
        }
    }
}

/* Conceptual based on Linux mm/memory.c */
```

When does page table reclamation happen?

    Trigger 1: Large munmap()
      Process unmaps 1 GB region
      → Many page tables now empty
      → Free them immediately

    Trigger 2: Process exit
      Process terminates
      → All its page tables freed
      → Memory returned to system

    Trigger 3: Memory pressure (less common)
      System running low on memory
      → Scan for empty page tables
      → Free them to reclaim memory
      → This is rare—usually other memory reclaimed first

### 8.7.4 Huge Pages: Dramatic Overhead Reduction

Chapter 4 showed huge pages improve TLB reach. They also dramatically
reduce page table overhead:

    Mapping 100 GB with 4KB pages:
      Pages: 100 GB / 4 KB = 26,214,400 pages
      PTs needed: 26,214,400 / 512 = 51,200 (200 MB)
      PDs needed: 51,200 / 512 = 100 (400 KB)
      PDPTs: 100 / 512 = 1 (4 KB)
      PML4: 1 (4 KB)
      Total: ~200 MB page table overhead
      
    Mapping 100 GB with 2MB huge pages:
      Pages: 100 GB / 2 MB = 51,200 huge pages
      PTs needed: NONE (huge pages skip PT level!)
      PDs needed: 51,200 / 512 = 100 (400 KB)
      PDPTs: 100 / 512 = 1 (4 KB)
      PML4: 1 (4 KB)
      Total: ~400 KB page table overhead
      
    Reduction: 200 MB → 400 KB = 500× less!

Linux Transparent Huge Pages automatically promotes eligible pages:

``` {.sourceCode .c}
// khugepaged scans for promotion opportunities
int khugepaged_scan_pmd(struct mm_struct *mm, struct vm_area_struct *vma,
                       unsigned long address) {
    pmd_t *pmd;
    pte_t *pte;
    int i;
    
    pmd = mm_find_pmd(mm, address);
    if (!pmd)
        return 0;
    
    // Check if all 512 pages are present and suitable
    pte = pte_offset_map_lock(mm, pmd, address);
    
    for (i = 0; i < HPAGE_PMD_NR; i++) {
        if (pte_none(pte[i]) || !pte_present(pte[i]))
            goto out;  // Not all pages present
        
        if (pte_write(pte[i]) != pte_write(pte[0]))
            goto out;  // Mixed permissions
    }
    
    // All 512 pages present with uniform permissions
    // This is a candidate for collapse
    return 1;
    
out:
    pte_unmap_unlock(pte, ptl);
    return 0;
}

int collapse_huge_page(struct mm_struct *mm, unsigned long address) {
    struct page *hpage;
    pmd_t *pmd;
    pte_t *pte_base;
    int i;
    
    // Allocate one 2MB huge page
    hpage = alloc_hugepage_vma(NULL, address, HPAGE_PMD_ORDER);
    if (!hpage)
        return -ENOMEM;
    
    // Copy all 512 small pages into the huge page
    pte_base = pte_offset_map(pmd, address);
    for (i = 0; i < HPAGE_PMD_NR; i++) {
        struct page *src = pte_page(pte_base[i]);
        copy_page(page_address(hpage) + i * PAGE_SIZE,
                 page_address(src));
    }
    
    // Free the old page table (512 PTEs, 4KB)
    pte_free(mm, pte_base);
    
    // Install huge page PMD entry (skips PT level!)
    pmd = pmd_offset(..., address);
    set_pmd_at(mm, address, pmd, mk_huge_pmd(hpage, vma->vm_page_prot));
    
    return 0;
}

/* Based on Linux kernel mm/huge_memory.c
   Reference: collapse_huge_page() */
```

------------------------------------------------------------------------

## 8.8 Performance Analysis: Putting It All Together

With full understanding of mechanisms and policies, let\'s explore how
to diagnose and fix memory management issues.

### 8.8.1 The Complete PostgreSQL OOM Case Study

Let\'s return to our opening mystery and solve it with everything we\'ve
learned:

**The Mystery:**

``` {.sourceCode .bash}
$ free -h
              total    used    free  shared  buff/cache  available
Mem:           64G     45G    2.1G    156M         16G        17G

kernel: Out of memory: Killed process 2847 (postgres)
kernel: total-vm:17825244kB, anon-rss:15728640kB

17 GB shows as "available" but PostgreSQL was killed. Why?
```

**Investigation Step 1: Check page table overhead**

``` {.sourceCode .bash}
$ cat /proc/meminfo | grep PageTables
PageTables:      8388608 kB  # 8 GB in page tables!

# This is the smoking gun.
# For 48 GB total PostgreSQL (3 instances × 16 GB each):
# Expected PT overhead: 48 GB × 0.002 = 96 MB
# Actual: 8 GB = 83× higher than expected!
```

**Investigation Step 2: Examine process details**

``` {.sourceCode .bash}
$ for pid in $(pgrep postgres); do
    echo "PID $pid:"
    grep -E 'VmRSS|VmPTE' /proc/$pid/status
done

PID 2847:
VmRSS:  15728640 kB  # 15 GB resident
VmPTE:   2621440 kB  # 2.5 GB page tables!

PID 3456:
VmRSS:  16777216 kB  # 16 GB resident
VmPTE:   2883584 kB  # 2.8 GB page tables!

PID 4123:
VmRSS:  15204352 kB  # 14.5 GB resident
VmPTE:   2490368 kB  # 2.4 GB page tables!

Total page tables: ~7.7 GB
Total RSS: ~46 GB

Expected PT for 46 GB: ~92 MB
Actual: 7.7 GB = 84× too high!
```

**Investigation Step 3: Check memory fragmentation**

``` {.sourceCode .bash}
$ cat /proc/2847/maps | wc -l
45,678  # Process has 45,000 VMAs!

$ cat /proc/2847/maps | head -30
# Thousands of tiny separate allocations:
7f1234000000-7f1234001000 rw-p ... # 4 KB
7f1234001000-7f1234002000 rw-p ... # 4 KB
7f1234002000-7f1234003000 rw-p ... # 4 KB
...
(repeated thousands of times)
```

**Root Cause Analysis:**

    Configuration:
      huge_pages = off (default)
      shared_buffers = 16 GB
      max_connections = 1000
      work_mem = 4 MB

    What happened:
      1. 16 GB shared_buffers → should be one large mapping
         But without huge pages, uses 4 KB pages
         16 GB / 4 KB = 4,194,304 pages
         Needs 4,194,304 / 512 = 8,192 page tables = 32 MB
         
      2. 1000 connections × 4 MB work_mem = 4 GB potential
         But allocated as many small buffers, not one large one
         Creates thousands of separate VMAs
         Each VMA needs its own page table hierarchy
         
      3. Fragmented allocation pattern:
         Instead of dense: [         16 GB          ]
         Got sparse:       [4K][4K]...[4K]...[4K]
         
         Sparse needs 100× more page tables!
         
      4. Total page tables: 8 GB
         Un-reclaimable overhead consuming 12.5% of RAM!

    Memory breakdown:
      Total RAM: 64 GB
      Active anon (PostgreSQL + others): 41 GB
      Page tables (un-reclaimable): 8 GB
      Kernel/buffers: 4 GB
      Page cache: 11 GB (reclaimable)
      Free: 0 GB
      
      "Available" calculation by 'free':
        Free + reclaimable cache = 0 + 11 GB = 11 GB
        
      But actual calculation:
        64 GB - 41 GB (apps) - 8 GB (PT) - 4 GB (kernel) = 11 GB
        
      When PostgreSQL tried to allocate more → OOM!

**The Fix:**

``` {.sourceCode .bash}
# Step 1: Enable huge pages at system level
# Calculate how many 2MB pages needed for 48 GB
# 48 GB / 2 MB = 24,576 huge pages

echo 24576 > /proc/sys/vm/nr_hugepages

$ cat /proc/meminfo | grep Huge
HugePages_Total:   24576
HugePages_Free:    24576
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB

# Step 2: Configure PostgreSQL to use huge pages
# Edit postgresql.conf:
huge_pages = try  # or 'on' to require them
shared_buffers = 16GB

# Step 3: Restart all PostgreSQL instances
systemctl restart postgresql@{1,2,3}

# Step 4: Verify huge pages are being used
$ cat /proc/meminfo | grep Huge
HugePages_Total:   24576
HugePages_Free:        0  # All allocated!
HugePages_Rsvd:        0
HugePages_Surp:        0

# Step 5: Check page table overhead now
$ cat /proc/meminfo | grep PageTables
PageTables:      524288 kB  # 512 MB

# Reduction: 8 GB → 512 MB = 16× improvement!

# Step 6: Verify per-process
$ grep VmPTE /proc/$(pgrep postgres | head -1)/status
VmPTE:    163840 kB  # 160 MB per process

# Down from 2.5 GB to 160 MB per process!
```

**Results:**

    BEFORE huge pages:
      Total RAM: 64 GB
      Page tables: 8 GB (12.5% of RAM)
      Available for apps: ~54 GB
      OOM kills: Frequent (2-3 per week)
      Query performance: Variable
      p99 latency: 120 ms
      
    AFTER huge pages:
      Total RAM: 64 GB
      Page tables: 512 MB (0.8% of RAM)
      Available for apps: ~61.5 GB  
      OOM kills: None (3 months)
      Query performance: Consistent, 12% faster
      p99 latency: 95 ms
      
    Benefits:
      1. Freed 7.5 GB memory (16× PT reduction)
      2. No more OOM kills
      3. 12% faster queries (TLB efficiency)
      4. 21% better p99 latency
      5. More stable, predictable performance

> 💡 **KEY INSIGHT**
>
> The \"17 GB available\" shown by `free` was misleading because it
> counted reclaimable page cache but didn\'t account for 8 GB of
> un-reclaimable page tables. Huge pages solved two problems
> simultaneously: reduced page table overhead from 8 GB to 512 MB
> (freeing 7.5 GB), and improved query performance through better TLB
> efficiency. One configuration change, massive impact.

------------------------------------------------------------------------

## 8.9 Summary: The Complete Picture

We\'ve completed our exploration of advanced MMU topics and system
integration. This chapter tied together all concepts from Chapters 1-7,
showing how hardware mechanisms enable software policies.

### The Hardware-Software Contract

**Hardware provides mechanisms:** - Multi-level page tables (Chapter 3)
for scalable address translation - TLB caching (Chapter 4) to avoid
expensive page walks - Accessed/Dirty bits (this chapter) to track page
usage - Page faults (Chapter 7) when translations fail - Nested
translation (this chapter) for efficient virtualization

**Software implements policies:** - **When** to allocate page tables:
Lazy allocation saves 10,000× - **Which** pages to evict: Clock/MGLRU
using A bits for LRU approximation - **How aggressively** to reclaim:
Watermarks guide kswapd and direct reclaim - **When** to use huge pages:
THP collapses pages, reducing overhead 500× - **How** to balance swap vs
cache: vm.swappiness tunes eviction preferences

**Together they enable:** - Process isolation (each process has own
virtual address space) - Memory overcommit (allocate more virtual than
physical RAM) - Efficient memory use (lazy allocation, intelligent
eviction, huge pages) - Predictable performance (background reclaim,
working set protection) - Virtualization (nested page tables with
optimizations)

### Key Insights Revisited

From the introduction, we asked: *Why was PostgreSQL killed despite \"17
GB available\"?*

**The answer:** Page table metadata consumed 8 GB of un-reclaimable
memory, but `free` only counted reclaimable page cache in \"available.\"
Huge pages fixed it by reducing page table overhead 16×.

From Section 8.2, we learned: *Nested page faults can cause 50 µs delays
for a single memory access*

**The mitigation:** Pre-populate EPT, use 2MB pages in EPT, batch fault
handling---reducing boot time by 50%.

From Section 8.4, we discovered: *Evicting dirty pages is 50-5000× more
expensive than clean pages*

**The implication:** Page replacement algorithms must use D bits to
prefer clean page eviction.

From Section 8.5, we saw: *Perfect LRU is impossible (would consume 100%
CPU)*

**The approximation:** Clock/MGLRU use A bits for coarse-grained
temporal tracking at \<0.1% CPU overhead.

### Bridging All Chapters

**Chapter 1** (Basics): Virtual memory provides isolation → **Chapter
8**: Page replacement makes overcommit practical

**Chapter 2** (Concepts): Demand paging delays allocation → **Chapter
8**: Eviction policies decide what to swap

**Chapter 3** (Page Tables): Multi-level structures scale → **Chapter
8**: Lazy alloc/free manages PT memory

**Chapter 4** (TLB): Caching avoids walks → **Chapter 8**: Huge pages
improve both TLB and PT overhead

**Chapter 7** (Faults): Faults trigger on access → **Chapter 8**:
Replacement algorithms minimize future faults

### Practical Takeaways by Role

**System Administrators:**

``` {.sourceCode .bash}
# Monitor comprehensively
watch 'cat /proc/meminfo | grep -E "MemAvailable|PageTables|Active|Inactive"'
vmstat 1

# Tune for databases
sysctl vm.swappiness=1
sysctl vm.min_free_kbytes=262144
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# Protect critical services
echo -500 > /proc/$(pidof critical_app)/oom_score_adj
```

**Application Developers:**

``` {.sourceCode .c}
// Use huge pages for large allocations
void *ptr = mmap(NULL, GB(1), PROT_READ|PROT_WRITE,
                 MAP_PRIVATE|MAP_ANONYMOUS|MAP_HUGETLB, -1, 0);

// Avoid fragmentation
void *big = malloc(GB(1));  // Not malloc() 1M times

// Provide hints
madvise(ptr, size, MADV_SEQUENTIAL);
madvise(old_ptr, old_size, MADV_DONTNEED);
```

**Hypervisor Operators:**

``` {.sourceCode .c}
// Pre-populate EPT
prepopulate_vm_ept(vm, LOW_MEMORY, MB(16));
prepopulate_vm_ept(vm, KERNEL_REGION, GB(1));

// Use huge pages at both levels
# Host THP + Guest THP = multiplicative benefit
```

### The Bigger Picture

Virtual memory systems represent decades of hardware-software co-design
evolution. What started as simple segmentation in the 1960s has evolved
into sophisticated multi-level, multi-generation systems that:

- Transparently manage terabytes of virtual address space with gigabytes
  of physical RAM
- Make intelligent eviction decisions based on access patterns
- Support efficient virtualization with nested translation
- Provide security through isolation
- Enable memory overcommit for better utilization

The key insight: **there is no one-size-fits-all policy**. Different
workloads require different tuning:

- **Databases:** Huge pages, swappiness=1, adequate min_free_kbytes
- **Desktops:** Balanced swappiness, moderate watermarks, THP=madvise
- **VMs:** Pre-populated EPT, huge pages at both levels
- **Real-time:** Locked pages (mlockall), no swapping
- **Containers:** Careful cgroup limits, memory.high for soft limits

Understanding both mechanisms (hardware capabilities) and policies
(software decisions) empowers you to make informed choices for your
specific use case. When you next encounter \"Out of Memory\" or observe
swapping, you\'ll understand the complete story from hardware A/D bits
through page table walks to kernel reclaim decisions and OOM killer
selection.

------------------------------------------------------------------------

## References

1.  Denning, P. J. (1970). \"Virtual Memory.\" *ACM Computing Surveys*,
    2(3), 153-189.
2.  Corbató, F. J. (1968). \"A paging experiment with the Multics
    system.\" *MIT Project MAC Report MAC-M-384*.
3.  Bélády, L. A. (1966). \"A Study of Replacement Algorithms for a
    Virtual-Storage Computer.\" *IBM Systems Journal*, 5(2), 78-101.
4.  Adams, K., & Agesen, O. (2006). \"A comparison of software and
    hardware techniques for x86 virtualization.\" *ACM SIGPLAN Notices*,
    41(11), 2-13.
5.  Zhao, Y. (2022). \"Multi-Gen LRU.\" Linux kernel mailing list.
    Merged in Linux 5.18.
6.  Intel Corporation (2024). *Intel 64 and IA-32 Architectures Software
    Developer\'s Manual, Volume 3: System Programming Guide*.
7.  AMD (2023). *AMD64 Architecture Programmer\'s Manual, Volume 2:
    System Programming*.
8.  ARM Ltd (2024). *ARM Architecture Reference Manual, ARMv8-A*.
9.  RISC-V International (2021). *The RISC-V Instruction Set Manual,
    Volume II: Privileged Architecture, Version 1.12*.
10. Linux Kernel (v6.5). *mm/vmscan.c, mm/oom_kill.c, mm/huge_memory.c,
    mm/memory.c*.

------------------------------------------------------------------------

**End of Chapter 8: Advanced MMU Topics - System Integration and
Optimization**

## 8.5 Page Replacement Algorithms: From Theory to Practice

Now that we understand how the hardware provides A and D bits, we can
explore how software uses them to make intelligent eviction decisions.
The goal is simple: when we must evict pages, choose the ones least
likely to be needed soon. The challenge is doing this efficiently
without perfect knowledge of future access patterns.

### 8.5.1 The Ideal: Perfect LRU

The theoretically optimal algorithm is Least Recently Used (LRU): evict
the page that was accessed longest ago. If page A was last accessed 10
seconds ago and page B was last accessed 5 seconds ago, evict page A.
This works because of temporal locality---pages accessed recently are
more likely to be accessed again soon.

The problem? Perfect LRU is impossible to implement efficiently:

``` {.sourceCode .c}
// Perfect LRU (theoretical, impossibly expensive)
struct page {
    unsigned long last_access_time;  // Timestamp of last access
    // ... other fields ...
};

// Would need to update on EVERY memory access
void perfect_lru_track_access(struct page *page) {
    page->last_access_time = get_nanoseconds();
    
    // This would run on EVERY memory access!
    // CPU does billions of memory accesses per second
    // Cost would be catastrophic
}

// Eviction would be simple
struct page *perfect_lru_evict(void) {
    struct page *oldest = NULL;
    unsigned long oldest_time = ULONG_MAX;
    
    // Find page with smallest timestamp
    for_each_page(page) {
        if (page->last_access_time < oldest_time) {
            oldest_time = page->last_access_time;
            oldest = page;
        }
    }
    
    return oldest;  // Evict this one
}
```

Why is this impossible?

    Cost analysis of perfect LRU:

    System with 8 GB RAM = 2 million pages (at 4KB each)

    Tracking overhead:
      - Update timestamp on every access
      - Modern CPU: 3 billion memory accesses/second
      - Each update: read timestamp, write new timestamp = 2 memory accesses
      - Additional memory traffic: 6 billion accesses/second just for tracking
      - Memory bandwidth: Doubles!
      - Cannot use TLB (TLB caches translations, not tracking state)
      
    Eviction overhead:
      - Scan 2 million pages to find minimum timestamp
      - 2M × 10 ns = 20 milliseconds per eviction
      - Under heavy pressure: 1000 evictions/second
      - 20 ms × 1000 = 20,000 ms = 20 seconds/second
      - More than 100% of CPU time just finding pages to evict!

> ⚠️ **PERFORMANCE TRAP**
>
> You cannot track every memory access in software. The CPU does
> billions of accesses per second. Even a single instruction per access
> would consume all CPU cycles. This is why hardware provides the A
> bit---it tracks accesses transparently during address translation with
> minimal overhead (only on first access to set the bit).

Perfect LRU is a beautiful theoretical concept but completely
impractical. Real systems must approximate LRU using the limited
information available from hardware---primarily the A bit.

### 8.5.2 Clock Algorithm: Practical LRU Approximation

The Clock algorithm, invented by Fernando Corbató in 1968, provides a
brilliant approximation of LRU using only the A bit. Pages are arranged
in a circular list. A \"clock hand\" sweeps around, giving each page
with A=1 a \"second chance\" by clearing its A bit. Pages with A=0 (not
accessed since last sweep) are evicted.

The key insight: A bit provides binary information (accessed/not
accessed) rather than precise timestamps. This is enough for good
approximation:

``` {.sourceCode .c}
// Clock algorithm (also called "Second Chance")
struct clock_state {
    struct page *hand;           // Current position in circular list
    struct list_head page_list;  // Circular list of all pages
};

struct page *clock_evict(struct clock_state *clock) {
    struct page *page = clock->hand;
    
    // Scan forward until we find a page to evict
    // This is the "clock hand" sweeping
    while (1) {
        pte_t *pte = get_pte_for_page(page);
        
        // Check accessed bit
        if (pte_young(*pte)) {
            // Page was accessed recently (A=1)
            // Give it a second chance: clear A bit and move on
            *pte = pte_mkold(*pte);  // Clear A bit
            
            // Move to next page in circular list
            page = list_next_entry(page, lru);
            if (&page->lru == &clock->page_list)
                page = list_first_entry(&clock->page_list, struct page, lru);
            
        } else {
            // Page not accessed since last sweep (A=0)
            // This page hasn't been used for at least one full rotation
            // Evict it!
            
            // Remove from list
            list_del(&page->lru);
            
            // Advance hand to next page
            clock->hand = list_next_entry(page, lru);
            if (&clock->hand->lru == &clock->page_list)
                clock->hand = list_first_entry(&clock->page_list, struct page, lru);
            
            return page;
        }
    }
}

/* Based on classical Clock algorithm
   Reference: Corbató et al., "A Paging Experiment with the Multics System", 1968 */
```

Why this works---the \"second chance\" gives pages with A=1 another
opportunity to be accessed:

    Example: 8 pages in circular list

    Initial state (all pages recently accessed):
      [A=1][A=1][A=1][A=1][A=1][A=1][A=1][A=1]
       ^hand

    Eviction request #1:
      Scan page 0: A=1 → clear to A=0, advance
      Scan page 1: A=1 → clear to A=0, advance
      Scan page 2: A=1 → clear to A=0, advance
      ...all have A=1...
      Scan page 7: A=1 → clear to A=0, advance
      Back to page 0: A=0 → EVICT!
      
      Result: All pages got their A bit cleared
      First revisited page (longest since accessed) was evicted
      
    Eviction request #2 (pages 2,4,6 accessed between evictions):
      [removed][A=0][A=1][A=0][A=1][A=0][A=1][A=0]
                ^hand
      
      Scan page 1: A=0 → EVICT!
      
      Page 1 wasn't accessed since last eviction, so evicted immediately
      Pages 2,4,6 were accessed, so they survived

    This approximates LRU: Pages that haven't been accessed for
    a full rotation are evicted. Recently accessed pages survive.

Performance characteristics:

    Clock algorithm analysis:

    Best case (page found immediately):
      - Check 1 page
      - Cost: ~100 ns
      - O(1) if victims readily available

    Worst case (all pages accessed):
      - Clear A bit on all N pages
      - Cost: N × 100 ns
      - Then evict first page
      - O(N) where N = number of pages

    Average case:
      - Scan ~10-50 pages before finding victim
      - Cost: ~1-5 µs
      - Amortized O(1) because subsequent evictions are fast

The Clock algorithm has a crucial property: it doesn\'t suffer from
Bélády\'s anomaly (where adding more memory makes performance worse).
It\'s also simple to implement and has good average-case performance.

### 8.5.3 Two-Handed Clock: Considering Cleanliness

Basic Clock doesn\'t distinguish between clean and dirty pages. But we
know dirty pages are 50-1000× more expensive to evict (must write to
disk). We can do better with a two-handed variant:

``` {.sourceCode .c}
// Two-handed clock: front hand clears A bits, back hand evicts
struct two_handed_clock {
    struct page *front_hand;  // Clears A bits (runs ahead)
    struct page *back_hand;   // Evicts pages (follows)
    unsigned int hand_distance;  // Distance between hands (tunable)
};

void advance_front_hand(struct two_handed_clock *clock) {
    struct page *page = clock->front_hand;
    pte_t *pte = get_pte_for_page(page);
    
    // Front hand simply clears A bits
    // Doesn't evict anything
    if (pte_young(*pte)) {
        *pte = pte_mkold(*pte);
    }
    
    // Advance to next page
    clock->front_hand = list_next_entry(page, lru);
}

struct page *evict_with_back_hand(struct two_handed_clock *clock) {
    struct page *page = clock->back_hand;
    
    while (1) {
        pte_t *pte = get_pte_for_page(page);
        
        // Back hand prefers clean pages over dirty
        if (!pte_young(*pte)) {  // A=0: not accessed recently
            if (!pte_dirty(*pte)) {
                // Clean AND cold: perfect victim!
                // Evict immediately
                list_del(&page->lru);
                clock->back_hand = list_next_entry(page, lru);
                return page;
            }
            
            // Dirty but cold: acceptable victim if pressured
            // Mark as candidate, but keep searching for clean page
            if (mem_pressure_high()) {
                // High pressure: take dirty page
                list_del(&page->lru);
                clock->back_hand = list_next_entry(page, lru);
                return page;
            }
        }
        
        // Not a good victim: advance
        page = list_next_entry(page, lru);
        clock->back_hand = page;
        
        // If back hand catches up to front hand, advance front
        if (distance(clock->back_hand, clock->front_hand) < clock->hand_distance) {
            advance_front_hand(clock);
        }
    }
}

/* Conceptual implementation based on BSD VM system
   Reference: McKusick et al., "The Design and Implementation of the 4.4BSD OS", 1996 */
```

The hand distance is a tunable parameter that controls how aggressive
the system is:

    Small hand distance (e.g., 64 pages):
      - Front hand barely ahead of back hand
      - Pages have little time to be re-accessed after A cleared
      - More aggressive eviction
      - Good under heavy memory pressure
      
    Large hand distance (e.g., 512 pages):
      - Front hand far ahead of back hand  
      - Pages have more time to be re-accessed after A cleared
      - Less aggressive eviction
      - Good under light memory pressure
      - Better approximation of LRU
      
    Example with hand_distance = 128:
      - Front hand clears A bits on pages
      - Back hand follows 128 pages behind
      - If page accessed in those 128 page-scans, A gets set again
      - Back hand sees A=1 and skips it
      - Only pages not accessed for 128+ page intervals get evicted

Performance improvement over single-handed Clock:

    Evicting 1000 pages under memory pressure:

    Single-handed Clock (no clean/dirty preference):
      - Evicts first page with A=0 (might be dirty)
      - 500 dirty pages, 500 clean pages (50/50 mix)
      - Average: 500 × 5ms (dirty) + 500 × 0.1ms (clean) = 2,550 ms

    Two-handed Clock (prefers clean):
      - Scans ahead for clean pages with A=0
      - Evicts clean pages when available
      - Falls back to dirty only under high pressure
      - 900 clean, 100 dirty (90/10 mix due to preference)
      - Average: 100 × 5ms (dirty) + 900 × 0.1ms (clean) = 590 ms
      
    Speed-up: 2,550 ms → 590 ms = 4.3× faster eviction!

> 💡 **KEY INSIGHT**
>
> The two-handed approach separates A bit clearing (front hand) from
> eviction decisions (back hand). This gives pages time to be
> re-accessed after their A bit is cleared, providing better LRU
> approximation. The hand distance controls the tradeoff between
> accuracy (large distance) and responsiveness to memory pressure (small
> distance).

### 8.5.4 Multi-Generational LRU (MGLRU): Modern Sophistication

Linux kernel 5.18 (released May 2022) introduced a new approach called
Multi-Generational LRU. Instead of binary A bit state
(accessed/not-accessed), MGLRU tracks multiple generations, allowing
pages to age gradually:

``` {.sourceCode .c}
// MGLRU: Pages age through 4 generations
#define MAX_NR_GENS 4  // Gen 3 (newest) → Gen 2 → Gen 1 → Gen 0 (oldest)

struct lruvec {
    struct lru_gen_struct {
        unsigned long timestamps[MAX_NR_GENS];  // When each gen started
        struct list_head lists[MAX_NR_GENS];    // Pages in each gen
    } lrugen;
};

void mglru_age_pages(struct lruvec *lruvec) {
    int gen;
    
    // Rotate generations: 3→2→1→0
    // Gen 0 pages become eviction candidates
    // New pages enter at gen 3
    
    // Move gen 0 to eviction list
    list_splice_init(&lruvec->lrugen.lists[0], &eviction_list);
    
    // Shift everyone down a generation
    for (gen = 0; gen < MAX_NR_GENS - 1; gen++) {
        list_splice_init(&lruvec->lrugen.lists[gen + 1],
                         &lruvec->lrugen.lists[gen]);
        lruvec->lrugen.timestamps[gen] = lruvec->lrugen.timestamps[gen + 1];
    }
    
    // Start new generation at gen 3
    INIT_LIST_HEAD(&lruvec->lrugen.lists[MAX_NR_GENS - 1]);
    lruvec->lrugen.timestamps[MAX_NR_GENS - 1] = jiffies;
    
    // Now scan all pages and promote those with A=1
    struct page *page;
    list_for_each_entry(page, &all_pages, lru) {
        pte_t *pte = get_pte_for_page(page);
        
        if (pte_young(*pte)) {
            // Page was accessed: promote to newest generation
            list_move(&page->lru, &lruvec->lrugen.lists[MAX_NR_GENS - 1]);
            
            // Clear A bit for next scan
            *pte = pte_mkold(*pte);
        }
        // Pages with A=0 stay in their current generation
        // They're aging toward gen 0
    }
}

struct page *mglru_evict(struct lruvec *lruvec) {
    // Evict from gen 0 (oldest generation)
    // These pages have survived multiple aging cycles without being accessed
    struct page *page = list_first_entry(&lruvec->lrugen.lists[0],
                                        struct page, lru);
    if (page) {
        list_del(&page->lru);
        return page;
    }
    
    // If gen 0 empty, age all pages and try again
    mglru_age_pages(lruvec);
    
    page = list_first_entry(&lruvec->lrugen.lists[0], struct page, lru);
    list_del(&page->lru);
    return page;
}

/* Conceptual implementation based on Linux MGLRU
   Reference: Yu Zhao, "Multi-Gen LRU", Linux kernel 5.18+, 2022
   Documentation: Documentation/admin-guide/mm/multigen_lru.rst */
```

How pages age through generations:

    Example: Page lifecycle in MGLRU

    T=0s: Page allocated, enters Gen 3 (newest)
      Gens: [0:empty][1:empty][2:empty][3:THIS PAGE]

    T=5s: First aging cycle, page has A=1 (was accessed)
      → Stays in Gen 3 (promoted because A=1)
      Gens: [0:empty][1:empty][2:old pages][3:THIS PAGE + new]

    T=10s: Second aging cycle, page has A=0 (not accessed)
      → Ages to Gen 2
      Gens: [0:old][1:older][2:THIS PAGE][3:new]

    T=15s: Third aging cycle, page has A=0 again
      → Ages to Gen 1
      Gens: [0:older][1:THIS PAGE][2:newer][3:newest]

    T=20s: Fourth aging cycle, page accessed (A=1)
      → Promoted back to Gen 3!
      Gens: [0:cold pages][1:cool][2:warm][3:THIS PAGE]
      Page got "second wind"—accessed again, so promoted

    T=25s-40s: Page not accessed for 3 cycles
      → Ages through Gen 2 → Gen 1 → Gen 0
      Gens: [0:THIS PAGE][1:...][2:...][3:...]

    T=45s: Eviction needed
      → Page evicted from Gen 0
      It survived 45 seconds but wasn't accessed for last 20s

Why MGLRU is better than two-list LRU (Linux\'s previous approach):

    Comparison: Two-list LRU vs MGLRU

    Two-list LRU (Linux 5.17 and earlier):
      - Active list: Recently accessed pages
      - Inactive list: Not recently accessed
      - Single promotion/demotion step
      - Problem: One-time accesses pollute active list
      
      Example: grep through large file
        - Touches each page once
        - All pages promoted to active list
        - Displaces useful hot pages
        - "Cache pollution" problem

    MGLRU (Linux 5.18+):
      - Four generations: 3 (hot) → 2 → 1 → 0 (cold)
      - Must survive multiple aging cycles to stay
      - Filters out one-time accesses naturally
      
      Example: same grep through large file
        - Pages enter Gen 3 on first access
        - Not accessed again: age to Gen 2 → 1 → 0
        - Evicted before polluting "hot" generations
        - Truly hot pages stay in Gen 3 through multiple promotions

Real-world benchmark results:

> 📊 **REAL NUMBERS - MGLRU PERFORMANCE**
>
> **Benchmark: PostgreSQL with 8 GB database, 4 GB RAM**\
> Workload: Mixed read/write with occasional large scans
>
> **Two-list LRU (Linux 5.17):** - Query latency p50: 15 ms - Query
> latency p99: 180 ms - Page faults: 2,200/sec - Throughput: 4,100
> queries/sec
>
> **MGLRU (Linux 5.18):** - Query latency p50: 12 ms (20% better) -
> Query latency p99: 140 ms (22% better) - Page faults: 1,850/sec (16%
> fewer) - Throughput: 4,900 queries/sec (19% better)
>
> **Why:** MGLRU better identifies truly hot pages (accessed frequently
> across multiple generations) vs. one-time scan pages (accessed once,
> then aged out quickly).

MGLRU represents the state-of-the-art in page replacement. It provides
better LRU approximation than Clock or two-list approaches while
maintaining similar O(1) amortized cost.

## 8.6 Memory Reclaim: When and How to Free Pages

Page replacement algorithms tell us **which** pages to evict. Now we
need to understand **when** eviction happens and **how** the kernel
manages the process of freeing memory under pressure.

### 8.6.1 Watermarks: Detecting Memory Pressure

The kernel doesn\'t wait until memory is completely exhausted to start
reclaiming pages. Instead, it maintains three watermark levels that
trigger increasingly aggressive reclaim:

``` {.sourceCode .c}
// Per-zone watermarks (simplified)
struct zone {
    unsigned long watermark[NR_WMARK];
};

enum zone_watermarks {
    WMARK_MIN,     // Emergency threshold: direct reclaim
    WMARK_LOW,     // Wake kswapd background thread
    WMARK_HIGH,    // kswapd can sleep
};

// Check if zone needs reclaim
bool zone_watermark_ok(struct zone *zone, unsigned int order) {
    unsigned long free_pages = zone_page_state(zone, NR_FREE_PAGES);
    unsigned long min = zone->watermark[WMARK_MIN];
    unsigned long low = zone->watermark[WMARK_LOW];
    unsigned long high = zone->watermark[WMARK_HIGH];
    
    if (free_pages < min) {
        // Below min: emergency! Direct reclaim required
        return false;
    } else if (free_pages < low) {
        // Below low: wake background reclaim daemon
        wake_up_kswapd();
        return free_pages >= min;  // Still above min
    } else if (free_pages >= high) {
        // Above high: all good, no reclaim needed
        return true;
    }
    
    // Between low and high: background reclaim running
    return true;
}

/* Based on Linux kernel mm/page_alloc.c */
```

Typical watermark values for an 8 GB system:

    8 GB RAM = 2,097,152 pages (at 4KB each)

    WMARK_HIGH:  96 MB  (24,576 pages)  3.8% of RAM
                 ↑ kswapd stops when this is reached

    WMARK_LOW:   64 MB  (16,384 pages)  2.5% of RAM
                 ↑ kswapd wakes when we drop below this

    WMARK_MIN:   32 MB  (8,192 pages)   1.3% of RAM
                 ↑ direct reclaim if we drop below this

    These are calculated from vm.min_free_kbytes sysctl
    Default min_free_kbytes = sqrt(RAM_in_MB) × 4
    For 8GB: sqrt(8192) × 4 ≈ 360 → ~32 MB minimum

The watermarks create three operational regimes:

> 📊 **REAL NUMBERS - WATERMARK BEHAVIOR**
>
> **Scenario: Gradual memory filling**
>
> T=0s: Free = 512 MB (above HIGH) → System idle, no reclaim
>
> T=30s: Application malloc(200 MB), Free = 312 MB (above HIGH) → Still
> above HIGH, no reclaim triggered
>
> T=45s: malloc(250 MB), Free = 62 MB (below LOW) → kswapd wakes, starts
> background reclaim → malloc() returns immediately (non-blocking) →
> kswapd reclaims in background
>
> T=47s: kswapd freed 50 MB, Free = 112 MB (above HIGH) → kswapd goes
> back to sleep
>
> T=60s: malloc(90 MB), Free = 22 MB (below MIN!) → Direct reclaim!
> Application blocks! → malloc() won\'t return until memory freed → User
> sees application freeze

### 8.6.2 kswapd: Background Reclaim Daemon

The `kswapd` kernel thread is responsible for background memory reclaim.
There\'s one kswapd per NUMA node, and it spends most of its time
asleep, waking only when memory drops below WMARK_LOW:

``` {.sourceCode .c}
// kswapd main loop (simplified)
static int kswapd(void *p) {
    struct pglist_data *pgdat = (struct pglist_data *)p;
    
    while (!kthread_should_stop()) {
        bool work_done = false;
        
        // Check all zones in this NUMA node
        for_each_zone(zone) {
            if (zone_free_pages(zone) < zone->watermark[WMARK_LOW]) {
                // Below low watermark: need to reclaim
                unsigned long target = zone->watermark[WMARK_HIGH];
                unsigned long current = zone_free_pages(zone);
                unsigned long to_reclaim = target - current;
                
                // Reclaim pages until we hit HIGH watermark
                unsigned long reclaimed = shrink_zone(zone, to_reclaim);
                
                if (reclaimed > 0)
                    work_done = true;
            }
        }
        
        if (!work_done) {
            // All zones above LOW watermark: go to sleep
            // Will be woken when zone drops below LOW
            set_current_state(TASK_INTERRUPTIBLE);
            schedule();  // Sleep until woken
        }
    }
    
    return 0;
}

// How pages are reclaimed from a zone
static unsigned long shrink_zone(struct zone *zone, unsigned long nr_to_reclaim) {
    unsigned long nr_reclaimed = 0;
    
    while (nr_reclaimed < nr_to_reclaim) {
        // Use page replacement algorithm (MGLRU/Clock) to pick victim
        struct page *page = select_page_to_evict();
        if (!page)
            break;  // No more evictable pages
        
        // Evict the page (may need to write to disk if dirty)
        if (try_to_free_page(page)) {
            nr_reclaimed++;
        }
        
        // Don't hog CPU: yield occasionally
        if (need_resched())
            cond_resched();
    }
    
    return nr_reclaimed;
}

/* Conceptual implementation based on Linux kernel mm/vmscan.c */
```

kswapd operates on the principle of \"work ahead of demand\":

    Timeline: kswapd behavior

    T=0s: Free=128 MB (above HIGH=96 MB)
      → kswapd sleeping

    T=10s: malloc(64 MB), Free=64 MB (equals LOW)
      → Allocation wakes kswapd
      → malloc() returns immediately (success)
      → kswapd starts reclaiming in background

    T=10.1s: kswapd examines pages
      → Find 100 clean file-backed pages
      → Drop them (no disk I/O needed)
      → Free=64 MB → 104 MB (above HIGH)
      → kswapd goes back to sleep
      
    Total user impact: 0 ms (malloc didn't block)
    Background reclaim handled everything

> 💡 **KEY INSIGHT**
>
> kswapd runs in the background to prevent applications from having to
> do direct reclaim. By freeing pages before memory is critically low,
> kswapd allows allocations to succeed without blocking. This is the
> difference between a responsive system and one that stutters under
> memory pressure.

### 8.6.3 Direct Reclaim: The Emergency Path

When memory drops below WMARK_MIN, kswapd can\'t keep up. The kernel
takes drastic action: the allocating process must free memory itself
before proceeding. This is called direct reclaim, and it\'s catastrophic
for latency:

``` {.sourceCode .c}
// Allocation path with direct reclaim
void *do_malloc(size_t size) {
    // Try to allocate normally
    struct page *page = alloc_pages(GFP_KERNEL, get_order(size));
    if (page)
        return page_to_virt(page);  // Success!
    
    // Failed: check if we're below MIN watermark
    if (zone_free_pages(zone) < zone->watermark[WMARK_MIN]) {
        // Emergency: must reclaim before allocating
        // This process BLOCKS here!
        
        unsigned long start = jiffies;
        printk(KERN_WARNING "Process %d entering direct reclaim\n", current->pid);
        
        // Try to reclaim enough pages to satisfy allocation
        unsigned long nr_reclaimed = try_to_free_pages(size / PAGE_SIZE + 32);
        
        unsigned long elapsed = jiffies_to_msecs(jiffies - start);
        printk(KERN_WARNING "Direct reclaim took %lu ms\n", elapsed);
        
        // Try allocation again
        page = alloc_pages(GFP_KERNEL, get_order(size));
        if (page)
            return page_to_virt(page);
        
        // Still failed: OOM path
        return NULL;
    }
    
    return NULL;
}

// Direct reclaim implementation
static unsigned long try_to_free_pages(unsigned long nr_to_reclaim) {
    unsigned long nr_reclaimed = 0;
    
    while (nr_reclaimed < nr_to_reclaim) {
        // Desperately search for evictable pages
        struct page *page = find_evictable_page();
        if (!page)
            break;
        
        pte_t *pte = get_pte_for_page(page);
        
        if (pte_dirty(*pte)) {
            // Page is dirty: MUST write to disk
            // This is the killer—disk I/O in the allocation path!
            
            if (page_is_file_backed(page)) {
                // Write back to file: 1-10 ms
                writeback_page(page);
            } else {
                // Write to swap: 1-10 ms
                swap_writepage(page);
            }
            
            // Each dirty page costs milliseconds!
        }
        
        // Free the page
        free_page(page);
        nr_reclaimed++;
    }
    
    return nr_reclaimed;
}

/* Based on Linux kernel mm/vmscan.c, __alloc_pages_direct_reclaim() */
```

The disaster scenario in detail:

    User calls malloc(1 MB):

    T=0: Enter allocation path
      - Check free pages: 28 MB (below MIN=32 MB)
      - kswapd is trying but can't keep up
      - Must do direct reclaim!

    T=1: Start searching for pages to evict
      - Check first page: dirty, must write
      - Write to swap: 5 ms
      
    T=6: Still need more pages
      - Check second page: dirty, must write
      - Write to swap: 5 ms
      
    ... (repeat 50 times for 1 MB allocation) ...

    T=250: Finally reclaimed enough
      - 50 pages × 5 ms = 250 ms writing dirty pages
      - Plus scanning overhead: 2 ms
      - Total time in direct reclaim: 252 ms

    T=252: Retry allocation
      - Success! Finally have free pages
      - Return from malloc()

    From user's perspective:
      - malloc(1 MB) took 252 milliseconds!
      - On a fast CPU this should be microseconds
      - Application appears frozen for 1/4 second

> ⚠️ **PERFORMANCE TRAP**
>
> Direct reclaim is the reason applications \"freeze\" under memory
> pressure. A simple malloc() call can block for hundreds of
> milliseconds while the kernel desperately writes dirty pages to disk.
> This happens in the application\'s context, so the application can\'t
> make progress. From the user\'s perspective, the application has hung.
>
> Real example: Video player doing malloc() for frame buffer hits direct
> reclaim. 250 ms delay = 15 dropped frames at 60 FPS. Video stutters
> noticeably.

The only way to avoid direct reclaim is ensuring kswapd keeps free
memory above WMARK_MIN. This requires proper tuning and avoiding
memory-intensive workloads on undersized systems.

### 8.6.4 Swappiness: Tuning Reclaim Behavior

When under memory pressure, the kernel must decide: evict file-backed
pages (easy to re-read) or anonymous pages (must write to swap)? The
`vm.swappiness` sysctl controls this tradeoff:

``` {.sourceCode .c}
// Simplified swappiness calculation
unsigned long get_scan_count(struct lruvec *lruvec, unsigned long *nr_to_scan) {
    unsigned long anon_prio, file_prio;
    unsigned long ap, fp;
    unsigned long anon_size = lruvec_lru_size(lruvec, LRU_ANON);
    unsigned long file_size = lruvec_lru_size(lruvec, LRU_FILE);
    
    // swappiness ranges from 0 to 200
    // Default is 60
    unsigned long swappiness = vm_swappiness;
    
    // Calculate scan priorities
    // Higher swappiness = more willing to swap anonymous pages
    anon_prio = swappiness;
    file_prio = 200 - swappiness;
    
    // Adjust by LRU list sizes
    ap = anon_prio * anon_size;
    fp = file_prio * file_size;
    
    // Calculate how many pages to scan from each list
    nr_to_scan[LRU_ANON] = ap / (ap + fp) * total_scan;
    nr_to_scan[LRU_FILE] = fp / (ap + fp) * total_scan;
    
    /* 
     * swappiness=0:   Strongly prefer evicting file pages
     * swappiness=60:  Default balanced behavior
     * swappiness=100: Equal treatment of anon and file
     * swappiness=200: Strongly prefer evicting anon pages (swapping)
     */
}

/* Based on Linux kernel mm/vmscan.c, get_scan_count() */
```

How different swappiness values behave:

    Scenario: System has 4 GB anonymous (malloc'd) memory
              and 4 GB file cache (mmap'd files, executables)
              Need to reclaim 1 GB

    swappiness=0 (Avoid swap, prefer file eviction):
      Priority: anon=0, file=200
      Result: Evict mostly file pages
      - Reclaim 950 MB from file cache
      - Reclaim 50 MB from anonymous memory
      Good for: Database servers (keep data in RAM, OK to re-read files)

    swappiness=60 (Default balanced):
      Priority: anon=60, file=140
      Result: Slightly prefer file eviction
      - Reclaim 600 MB from file cache
      - Reclaim 400 MB from anonymous memory
      Good for: General purpose systems

    swappiness=100 (Equal treatment):
      Priority: anon=100, file=100
      Result: Evict proportionally
      - Reclaim 500 MB from file cache
      - Reclaim 500 MB from anonymous memory
      Good for: Workloads with equal importance

    swappiness=200 (Prefer swapping):
      Priority: anon=200, file=0
      Result: Evict mostly anonymous pages
      - Reclaim 50 MB from file cache
      - Reclaim 950 MB from anonymous memory
      Good for: File servers (keep file cache hot, OK to swap processes)

Real-world tuning example:

    Database server (PostgreSQL):
      - Database uses shared_buffers (anonymous memory)
      - Keep this hot in RAM at all costs!
      - OK to drop file cache (can re-read from disk)
      
      Tuning: vm.swappiness=10
      Result: Kernel strongly prefers evicting file cache
              Database working set stays in RAM
              Query latency: Stable
              
    Desktop system:
      - Applications use anonymous memory
      - Frequently access same files (documents, code)
      - File cache is valuable
      
      Tuning: vm.swappiness=60 (default)
      Result: Balanced eviction
              Applications can swap if needed
              File cache provides fast re-access

    File server (NFS/Samba):
      - Most requests are for file data
      - File cache is critical for performance
      - Server processes can swap if needed
      
      Tuning: vm.swappiness=150
      Result: Kernel prefers swapping server processes
              File cache stays hot
              File serving latency: Low and stable

> 💡 **KEY INSIGHT - WORKLOAD SPECIFIC TUNING**
>
> There is no \"best\" swappiness value. It depends entirely on your
> workload: - Database: Low swappiness (prefer file eviction) - Desktop:
> Medium swappiness (balanced) - File server: High swappiness (prefer
> swapping processes)
>
> The default of 60 works reasonably for general-purpose systems but can
> be far from optimal for specialized workloads.

### 8.6.5 OOM Killer: The Last Resort

When reclaim fails---the kernel can\'t free enough memory even with
direct reclaim---the Out-Of-Memory (OOM) killer is invoked. Its job:
kill a process to free memory:

``` {.sourceCode .c}
// OOM killer victim selection (simplified)
struct task_struct *select_bad_process(void) {
    struct task_struct *p;
    struct task_struct *chosen = NULL;
    unsigned long chosen_points = 0;
    
    // Scan all processes
    for_each_process(p) {
        unsigned long points = 0;
        
        // Calculate "badness" score
        // Higher score = more likely to be killed
        
        // 1. Memory usage (primary factor)
        // RSS (resident set size) in pages
        points = get_mm_rss(p->mm);
        
        // 2. Add swap usage
        points += get_mm_counter(p->mm, MM_SWAPENTS);
        
        // 3. Add half of virtual memory
        // (might be mostly unmapped but still indicates big process)
        points += p->mm->total_vm / 2;
        
        // 4. Adjustments
        
        // Root processes: -25% (less likely to kill)
        if (has_capability(p, CAP_SYS_ADMIN))
            points -= points / 4;
        
        // oom_score_adj: user tunable (-1000 to +1000)
        // -1000 = never kill
        // +1000 = always prefer to kill
        points += p->signal->oom_score_adj;
        
        // 5. Never kill kernel threads or init
        if (p->flags & PF_KTHREAD || p->pid == 1)
            continue;
        
        // Track highest score
        if (points > chosen_points) {
            chosen_points = points;
            chosen = p;
        }
    }
    
    return chosen;
}

void oom_kill_process(struct task_struct *p) {
    pr_err("Out of memory: Kill process %d (%s) score %lu or sacrifice child\n",
           p->pid, p->comm, p->signal->oom_score);
    
    // Dump memory info for debugging
    dump_memory_state();
    
    // Send SIGKILL to the process
    // This is immediate and cannot be caught
    force_sig(SIGKILL, p);
    
    // Mark for memory reclaim
    mark_oom_victim(p);
}

/* Based on Linux kernel mm/oom_kill.c */
```

Example OOM decision:

    System State:
      Total RAM: 8 GB
      Free: 10 MB (below MIN)
      Direct reclaim: Failed to free enough

    Process Table:
      PID  Name          RSS    Swap   VM    Score  Adj  Final
      1    init          4 MB   0      4 MB  4      0    4 (never kill)
      234  sshd          8 MB   0      12 MB 14     0    14
      567  postgres      2 GB   100 MB 4 GB  2348   0    2348 ← Selected!
      890  chrome        1 GB   200 MB 3 GB  1400   0    1400
      1024 vim           50 MB  0      80 MB 90     0    90

    Victim: postgres (PID 567)
      Reason: Highest score (2348 points)
      Breakdown:
        - RSS: 2 GB = 524,288 pages
        - Swap: 100 MB = 25,600 pages
        - VM/2: 4 GB / 2 = 1 GB = 262,144 pages
        - Total: 811,936 pages ≈ 3.2 GB score
        - Adjustments: None (oom_score_adj=0)

    Result:
      kernel: Out of memory: Kill process 567 (postgres) score 3276800
      kernel: Killed process 567, total-vm:4194304kB, anon-rss:2097152kB
      
    Impact:
      - Process killed instantly
      - 2 GB RAM freed
      - System recovers
      - Database users see connection errors

> 🔍 **WHAT\'S REALLY HAPPENING - OOM KILLER SELECTION**
>
> The OOM killer tries to: 1. Kill the process using the most memory
> (biggest impact) 2. Avoid killing critical system processes (init,
> systemd) 3. Respect user hints (oom_score_adj) 4. Minimize collateral
> damage (prefer single process over multiple)
>
> It\'s not random---it\'s making a calculated choice about which
> process death will best help the system recover.

Tuning OOM behavior:

``` {.sourceCode .bash}
# Protect critical process from OOM killer
echo -1000 > /proc/$(pidof mysqld)/oom_score_adj
# Now mysqld will never be killed (unless all other options exhausted)

# Make process more likely to be killed
echo +500 > /proc/$(pidof big-batch-job)/oom_score_adj
# big-batch-job will be preferred victim

# Check current scores
ps aux | while read line; do
    pid=$(echo $line | awk '{print $2}')
    if [ -f /proc/$pid/oom_score ]; then
        score=$(cat /proc/$pid/oom_score)
        echo "$score $line"
    fi
done | sort -rn | head -20
# Shows 20 processes most likely to be OOM killed
```

The OOM killer is a last resort, but it\'s better than system deadlock.
Proper memory management (sizing, tuning swappiness, monitoring) should
prevent OOM from ever happening in production.

------------------------------------------------------------------------

## 8.7 Page Table Management: The Meta-Problem

We\'ve discussed evicting data pages to free memory. But page tables
themselves consume memory---often a surprising amount. On a system with
hundreds of processes or VMs, page table overhead can reach gigabytes.
This creates a meta-problem: we need memory to manage memory.

### 8.7.1 Page Table Overhead Calculations

Let\'s calculate how much memory page tables consume for a typical
process:

``` {.sourceCode .c}
// Page table overhead for multi-level paging
unsigned long calculate_pt_overhead(unsigned long virtual_size) {
    unsigned long nr_pages = virtual_size / PAGE_SIZE;
    unsigned long overhead = 0;
    
    // Level 1: PML4 (always allocated)
    // One PML4 per process, regardless of size
    overhead += PAGE_SIZE;  // 4 KB
    
    // Level 2: PDPTs
    // One PDPT per 512 GB of virtual address space
    unsigned long nr_pdpts = (virtual_size + GB(512) - 1) / GB(512);
    overhead += nr_pdpts * PAGE_SIZE;
    
    // Level 3: PDs
    // One PD per 1 GB of virtual address space
    unsigned long nr_pds = (virtual_size + GB(1) - 1) / GB(1);
    overhead += nr_pds * PAGE_SIZE;
    
    // Level 4: PTs
    // One PT per 2 MB of virtual address space
    unsigned long nr_pts = (virtual_size + MB(2) - 1) / MB(2);
    overhead += nr_pts * PAGE_SIZE;
    
    return overhead;
}

// Example calculations:
// 10 GB process:
//   PML4: 4 KB (1 table)
//   PDPTs: 4 KB (1 table for 0-512 GB)
//   PDs: 40 KB (10 tables, one per GB)
//   PTs: 20,480 KB = 20 MB (5,120 tables, one per 2 MB)
//   Total: ~20 MB overhead (0.2% of 10 GB)

// 100 processes × 1 GB each:
//   Per process: 2 MB overhead
//   Total: 200 MB overhead

// 8 VMs × 8 GB each (with EPT):
//   Guest page tables: 8 × 16 MB = 128 MB
//   Host EPT: 8 × 16 MB = 128 MB
//   Total: 256 MB overhead
```

The overhead scales with virtual address space size, not physical memory
usage. A process with a 100 GB sparse mapping (mostly unmapped) consumes
as much page table memory as one with 100 GB fully populated.

Real-world example:

> 📊 **REAL NUMBERS - PAGE TABLE OVERHEAD SCALING**
>
> **PostgreSQL database server (64 GB RAM):** - 3 postgres processes, 16
> GB shared_buffers each - Many memory-mapped files (10,000 files × 10
> MB avg) - Address space per process: 48 GB virtual
>
> Page table breakdown per process: - Dense regions (shared buffers): 16
> GB → 32 MB PTs - Sparse regions (mmap\'d files): 32 GB → 64 MB PTs -
> Total per process: \~96 MB - **Total for 3 processes: 288 MB**
>
> That\'s 288 MB of RAM (0.45% of total) just for page tables! With huge
> pages: 288 MB → 576 KB (500× reduction)

### 8.7.2 Lazy Allocation: Avoiding Waste

Allocating all page tables upfront would be wasteful. Most processes
don\'t use their entire address space. The kernel uses lazy allocation:
page tables are created only when first accessed:

``` {.sourceCode .c}
// Lazy page table allocation on page fault
int handle_page_fault(unsigned long address) {
    pgd_t *pgd;
    p4d_t *p4d;
    pud_t *pud;
    pmd_t *pmd;
    pte_t *pte;
    
    // Walk page tables, allocating levels as needed
    
    // Level 1: PGD (PML4) always exists
    // Allocated during process creation
    pgd = pgd_offset(current->mm, address);
    if (pgd_none(*pgd)) {
        // Shouldn't happen—PML4 always allocated
        return VM_FAULT_OOM;
    }
    
    // Level 2: P4D (5-level paging) or PUD
    // Allocate if missing
    p4d = p4d_alloc(current->mm, pgd, address);
    if (!p4d)
        return VM_FAULT_OOM;
    
    // Level 3: PUD (PDPT)
    // Allocate if missing
    pud = pud_alloc(current->mm, p4d, address);
    if (!pud)
        return VM_FAULT_OOM;
    
    // Level 4: PMD (PD)
    // Allocate if missing
    pmd = pmd_alloc(current->mm, pud, address);
    if (!pmd)
        return VM_FAULT_OOM;
    
    // Level 5: PTE (PT)
    // Allocate if missing
    pte = pte_alloc(current->mm, pmd, address);
    if (!pte)
        return VM_FAULT_OOM;
    
    // Now handle the actual fault (demand paging, COW, etc.)
    return do_anonymous_page(current->mm, pte, address);
}

/* Based on Linux kernel mm/memory.c, __handle_mm_fault() */
```

The savings can be enormous:

    Example: Process with sparse 64 GB address space
      - Actually using only 1 GB scattered across the space
      - 10,000 separate small allocations

    Eager allocation (allocate all page tables upfront):
      - PML4: 4 KB
      - PDPTs: 4 KB
      - PDs: 256 KB (64 tables for 64 GB)
      - PTs: 131,072 KB = 128 MB (32,768 tables for 64 GB)
      - Total: ~128 MB

    Lazy allocation (only what's used):
      - PML4: 4 KB
      - PDPTs: 4 KB (only 1 needed for first 512 GB)
      - PDs: 40 KB (only 10 needed for 10 regions of 1 GB each)
      - PTs: 20 MB (only 5,120 needed for 1 GB actual usage)
      - Total: ~20 MB

    Savings: 128 MB → 20 MB = 6.4× reduction!

Lazy allocation is why you can run hundreds of processes on limited
RAM---most of their address space exists only virtually, without
consuming physical memory for page tables.

### 8.7.3 Page Table Reclamation

Just as data pages can be reclaimed under pressure, empty page tables
can be freed. When a region of memory is unmapped, the kernel checks if
entire page tables are now empty:

``` {.sourceCode .c}
// Reclaim page tables when memory is unmapped
void unmap_page_range(struct vm_area_struct *vma,
                     unsigned long addr, unsigned long end) {
    pgd_t *pgd;
    pud_t *pud;
    pmd_t *pmd;
    pte_t *pte;
    
    // Walk the page tables, clearing entries
    for (; addr < end; addr += PAGE_SIZE) {
        pgd = pgd_offset(vma->vm_mm, addr);
        pud = pud_offset(pgd, addr);
        pmd = pmd_offset(pud, addr);
        pte = pte_offset_map(pmd, addr);
        
        // Clear the PTE
        pte_clear(vma->vm_mm, addr, pte);
        
        pte_unmap(pte);
    }
    
    // Now check if any page table pages are completely empty
    // and can be freed
    
    // Check if entire PT is empty
    pmd = pmd_offset(pud, addr);
    if (pmd_none_or_clear_bad(pmd)) {
        // All 512 PTEs in this PT are invalid
        // Free the PT page itself
        pte_free(vma->vm_mm, pmd_page(*pmd));
        pmd_clear(pmd);
    }
    
    // Check if entire PD is empty
    pud = pud_offset(pgd, addr);
    if (pud_none_or_clear_bad(pud)) {
        // All 512 PMDs in this PD are invalid
        // Free the PD page
        pmd_free(vma->vm_mm, pud_page(*pud));
        pud_clear(pud);
    }
    
    // Check if entire PDPT is empty
    pgd = pgd_offset(vma->vm_mm, addr);
    if (pgd_none_or_clear_bad(pgd)) {
        // All 512 PUDs in this PDPT are invalid
        // Free the PDPT page
        pud_free(vma->vm_mm, pgd_page(*pgd));
        pgd_clear(pgd);
    }
    
    // Note: Never free PML4 (top level)
    // It's freed only when process exits
}

/* Based on Linux kernel mm/memory.c, unmap_page_range() */
```

When reclamation happens:

    Scenario 1: munmap() large region
      - Application calls munmap(addr, 1 GB)
      - Kernel clears all PTEs in that 1 GB range
      - Checks each PT: all 512 PTEs invalid? Free PT
      - Result: Immediately reclaim 512 PTs = 2 MB

    Scenario 2: Process exit
      - All memory unmapped at once
      - All page tables freed
      - Result: Multi-megabyte instant reclaim

    Scenario 3: Memory pressure
      - Kernel scans for empty page tables
      - Frees them even if process still running
      - Result: Slow gradual reclaim (background)

But there\'s a subtlety---lazy reclamation:

``` {.sourceCode .c}
// Linux doesn't always immediately free empty page tables
// It may defer freeing until memory pressure

void free_pgtables(struct mmu_gather *tlb, struct vm_area_struct *vma) {
    // Check if we should actually free page tables now
    // or defer until later
    
    if (system_under_memory_pressure()) {
        // Memory pressure: aggressively free empty tables
        free_empty_page_tables(vma);
    } else {
        // No pressure: defer freeing
        // Empty tables might be re-used soon
        // Keep them around to avoid re-allocation cost
    }
}
```

This lazy approach trades memory for performance: empty page tables
consume memory but avoiding re-allocation reduces fault latency if the
region is accessed again.

### 8.7.4 Compact vs Sparse Layouts

Page tables don\'t have to be physically contiguous, but placing them
close together in physical memory improves cache performance. The Page
Walk Cache (PWC) benefits from spatial locality:

``` {.sourceCode .c}
// Two allocation strategies for page tables

// Strategy 1: Sparse allocation (simple but slow)
pte_t *allocate_pt_sparse(void) {
    // Allocate from general page pool
    // Pages come from anywhere in physical memory
    struct page *page = alloc_page(GFP_KERNEL);
    return page_to_virt(page);
    
    // Result: PTs scattered across physical memory
    // PWC hit rate: ~60-70%
    // Page walk latency: Higher variance
}

// Strategy 2: Compact allocation (complex but fast)
pte_t *allocate_pt_compact(struct mm_struct *mm) {
    // Try to allocate from contiguous region
    // Keep all of this process's page tables close together
    
    if (!mm->pt_pool) {
        // First PT allocation: reserve contiguous region
        // Reserve 16 MB for all future page tables
        mm->pt_pool = alloc_contiguous(PAGE_SIZE * 4096);
        mm->pt_pool_index = 0;
    }
    
    if (mm->pt_pool_index < 4096) {
        // Allocate from reserved pool
        pte_t *pt = mm->pt_pool + mm->pt_pool_index * PAGE_SIZE;
        mm->pt_pool_index++;
        return pt;
    }
    
    // Pool exhausted: fall back to sparse
    return allocate_pt_sparse();
    
    // Result: First 4096 PTs in contiguous 16 MB region
    // PWC hit rate: ~85-90%
    // Page walk latency: Lower and more predictable
}

/* Conceptual implementation based on page table clustering techniques */
```

Performance impact:

    Benchmark: Random access to 100 GB sparse mapping

    Sparse page table layout:
      - PTs scattered across physical memory
      - Random physical addresses
      - PWC miss on 40% of page walks
      - Average page walk: 120 ns
      - Total time: 12 ms per million accesses

    Compact page table layout:
      - PTs in contiguous 200 MB region
      - Spatial locality in physical memory
      - PWC miss on 15% of page walks
      - Average page walk: 85 ns
      - Total time: 8.5 ms per million accesses

    Speed-up: 29% faster page walks!

> 📊 **REAL NUMBERS - COMPACT ALLOCATION IMPACT**
>
> **Database workload (100 GB working set, random access):**
>
> **Sparse PT allocation:** - Page walk latency p50: 115 ns - Page walk
> latency p99: 220 ns - PWC hit rate: 62% - TLB miss penalty: High
> variance
>
> **Compact PT allocation:** - Page walk latency p50: 82 ns (28%
> better) - Page walk latency p99: 140 ns (36% better) - PWC hit rate:
> 88% - TLB miss penalty: Lower and predictable

The tradeoff: compact allocation requires reserving contiguous memory
upfront, which may not be available under fragmentation. Most systems
use hybrid approaches: try compact allocation, fall back to sparse if
needed.

### 8.7.5 Huge Pages: The Ultimate Optimization

We\'ve mentioned huge pages throughout this book. Their impact on page
table overhead deserves special attention:

``` {.sourceCode .c}
// Overhead comparison: 4KB vs 2MB pages
void compare_page_table_overhead(void) {
    unsigned long data_size = GB(100);  // 100 GB of data
    
    // With 4KB pages:
    unsigned long pages_4kb = data_size / KB(4);  // 25,600,000 pages
    unsigned long pts_needed = pages_4kb / 512;    // 50,000 PTs
    unsigned long overhead_4kb = pts_needed * PAGE_SIZE;
    
    printf("4KB pages:\n");
    printf("  Data pages: %lu (25.6 million)\n", pages_4kb);
    printf("  PTs needed: %lu (50,000)\n", pts_needed);
    printf("  PT overhead: %lu MB (%.2f%%)\n", 
           overhead_4kb / MB(1), 
           100.0 * overhead_4kb / data_size);
    
    // With 2MB pages:
    unsigned long pages_2mb = data_size / MB(2);  // 51,200 pages
    unsigned long pmds_needed = pages_2mb / 512;  // 100 PMDs
    unsigned long overhead_2mb = pmds_needed * PAGE_SIZE;
    
    printf("\n2MB pages:\n");
    printf("  Data pages: %lu (51,200)\n", pages_2mb);
    printf("  PMDs needed: %lu (100)\n", pmds_needed);
    printf("  PT overhead: %lu KB (%.4f%%)\n",
           overhead_2mb / KB(1),
           100.0 * overhead_2mb / data_size);
    
    printf("\nReduction: %lux smaller!\n", overhead_4kb / overhead_2mb);
}

// Output:
// 4KB pages:
//   Data pages: 25600000 (25.6 million)
//   PTs needed: 50000 (50,000)
//   PT overhead: 200 MB (0.20%)
//
// 2MB pages:
//   Data pages: 51200 (51,200)
//   PMDs needed: 100 (100)
//   PT overhead: 400 KB (0.0004%)
//
// Reduction: 512x smaller!
```

Real PostgreSQL example revisited:

    Earlier we saw PostgreSQL with:
      - 3 processes × 48 GB virtual each
      - 288 MB in page tables

    With transparent huge pages (THP) enabled:
      - Same 3 processes × 48 GB virtual
      - Dense regions use 2MB pages
      - Sparse regions still use 4KB (can't use huge pages)
      
    New breakdown:
      - Dense (48 GB): 96 MB → 192 KB (500× reduction)
      - Sparse (36 GB): 72 MB → 72 MB (unchanged)
      - Total per process: 72.2 MB
      - Total for 3 processes: 216 MB (was 288 MB)
      
    Savings: 72 MB freed

    If fully converted to huge pages:
      - Total: 288 MB → 576 KB (500× reduction!)
      - Savings: 287.4 MB freed

Huge pages provide: 1. **500× less page table overhead** (fewer levels
to allocate) 2. **512× better TLB coverage** (each TLB entry covers 2 MB
not 4 KB) 3. **Faster page walks** (one fewer level to traverse)

The challenge is allocation: 2MB huge pages require 2MB contiguous
physical memory, which may not be available due to fragmentation.

------------------------------------------------------------------------

## 8.8 Performance Analysis and Tuning

We\'ve explored the mechanisms---now let\'s see how to diagnose problems
and optimize real systems. This section covers the tools for identifying
memory management issues and the parameters for tuning them.

### 8.8.1 Essential Profiling Tools

**Tool 1: /proc/meminfo - System-Wide Memory Status**

``` {.sourceCode .bash}
$ cat /proc/meminfo
MemTotal:       65536000 kB   # Total RAM
MemFree:         2048000 kB   # Truly free (not in use)
MemAvailable:   17920000 kB   # Free + reclaimable (misleading!)
PageTables:      8192000 kB   # Memory used by page tables ← RED FLAG!
Active:         28672000 kB   # Recently accessed pages
Inactive:       16384000 kB   # Not recently accessed
Dirty:           1024000 kB   # Modified, needs writeback
Shmem:          16384000 kB   # Shared memory (tmpfs, mmap)
SwapTotal:      8388608 kB    # Total swap space
SwapFree:       8388608 kB    # Unused swap
```

Key metrics to watch:

    Red flags:
      - PageTables > 1% of MemTotal → Page table overhead problem
      - MemAvailable misleading when PageTables is high
      - Dirty > 10% of MemTotal → Write pressure
      - SwapFree much less than SwapTotal → System swapping heavily

    Example problematic output:
      MemTotal:    64 GB
      MemAvailable: 17 GB ← Looks OK!
      PageTables:    8 GB ← PROBLEM! Not reclaimable
      Actual available: 17 GB - 8 GB = 9 GB only

**Tool 2: vmstat - Real-Time Monitoring**

``` {.sourceCode .bash}
$ vmstat 1
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2  0      0 2048000 256000 8192000  0    0   100  200 1000 2000 25 10 60  5  0
 2  1      0 1024000 256000 8192000  0  5120  50  5000 1200 2200 20 15 50 15  0
                                      ↑   ↑   ↑    ↑
                                      |   |   |    |
                                      |   |   |    +--- Blocks out (write)
                                      |   |   +-------- Blocks in (read)
                                      |   +------------ Swap out (pages/s)
                                      +---------------- Swap in (pages/s)
```

Interpreting swap columns:

    Good: si=0, so=0
      → No swapping
      → System healthy

    Warning: si=100, so=200
      → Light swapping (100-200 pages/sec)
      → Monitor, may worsen

    Critical: si=5120, so=10240
      → Heavy swapping (5-10 MB/sec)
      → System thrashing
      → Applications unresponsive
      → Action required immediately!

    Real example during PostgreSQL OOM:
      si=8192, so=16384 (8-16 MB/sec swapping)
      bo=25000 (25 MB/sec disk writes)
      wa=45 (45% CPU time waiting for I/O)
      → Database completely frozen

> ⚠️ **PERFORMANCE TRAP - MISLEADING METRICS**
>
> High `MemAvailable` doesn\'t guarantee allocation success! If
> `PageTables` is high, that \"available\" memory is actually consumed
> by un-reclaimable page table overhead. Always check `PageTables` when
> diagnosing OOM issues.

**Tool 3: perf - Hardware Counter Analysis**

``` {.sourceCode .bash}
# Measure TLB miss rate
$ perf stat -e dTLB-load-misses,dTLB-loads ./application

 Performance counter stats for './application':

     12,234,567  dTLB-load-misses   # 2.5% of all dTLB accesses
    487,654,321  dTLB-loads
    
      5.123 seconds time elapsed
```

Analyzing results:

    TLB miss rate calculation:
      Misses: 12,234,567
      Total accesses: 487,654,321
      Miss rate: 2.5%
      
    Cost analysis:
      Each miss: ~100 cycles (page table walk)
      Total cost: 12,234,567 × 100 = 1,223,456,700 cycles
      At 3 GHz: 1.2 billion cycles / 3 billion per second = 0.4 seconds
      
      Application ran for 5.1 seconds
      TLB miss overhead: 0.4 / 5.1 = 7.8% of runtime!

    Action: Enable huge pages to reduce TLB misses

**Tool 4: /proc/\[pid\]/smaps - Per-Process Memory Maps**

``` {.sourceCode .bash}
$ cat /proc/1234/smaps
7f8a2c000000-7f8a30000000 rw-p 00000000 00:00 0 
Size:              65536 kB   # VMA size
KernelPageSize:        4 kB   # Underlying page size
MMUPageSize:           4 kB   # Page size used by MMU
Rss:               32768 kB   # Actually in RAM
Pss:               16384 kB   # Proportional share (RSS/sharers)
Shared_Clean:       8192 kB   # Shared, not modified
Shared_Dirty:          0 kB   # Shared, modified
Private_Clean:     16384 kB   # Private, not modified
Private_Dirty:      8192 kB   # Private, modified ← Will need swap
Referenced:        24576 kB   # Recently accessed
Anonymous:         32768 kB   # Not file-backed
AnonHugePages:     20480 kB   # Using transparent huge pages
Swap:               4096 kB   # Currently in swap
SwapPss:            2048 kB   # Proportional swap
```

Detecting issues:

    Issue 1: Fragmentation
      Size: 65536 kB (whole VMA)
      AnonHugePages: 4096 kB (only small portion)
      → Fragmentation preventing THP
      
    Issue 2: Swap pressure
      Swap: 16384 kB
      Private_Dirty: 32768 kB
      → Half the private pages swapped out
      → Performance degradation likely

    Issue 3: Memory leaks
      $ watch -n 1 'cat /proc/1234/smaps | grep -A 15 heap'
      [Watch Rss growing continuously]
      → Memory leak in heap

### 8.8.2 Common Performance Issues

**Issue 1: TLB Thrashing**

    Symptoms:
      - High CPU usage
      - perf shows high dTLB-load-misses
      - Application slower than expected
      - No disk I/O (rules out paging)

    Diagnosis:
      $ perf stat -e dTLB-load-misses,dTLB-loads,iTLB-load-misses ./app
      
      dTLB-load-misses: 45,000,000  # Data TLB misses
      dTLB-loads: 500,000,000       # Total data accesses
      iTLB-load-misses: 5,000,000   # Instruction TLB misses
      
      dTLB miss rate: 9% ← VERY HIGH (should be <1%)

    Root cause:
      - Working set larger than TLB coverage
      - Random access pattern (poor locality)
      - 4KB pages: TLB covers only 1-2 MB
      
    Solutions:
      1. Enable huge pages:
         echo always > /sys/kernel/mm/transparent_hugepage/enabled
         → 2MB pages: TLB covers 256-512 MB (256× improvement)
         
      2. Restructure data for better locality:
         - Sort by access pattern
         - Use SOA (struct of arrays) instead of AOS (array of structs)
         
      3. Increase working set if possible:
         - Process fewer items per batch
         - Partition data to fit in TLB

**Issue 2: Swap Thrashing**

    Symptoms:
      - System extremely slow
      - Applications freeze frequently
      - vmstat shows high si/so values
      - Disk I/O pegged at 100%

    Diagnosis:
      $ vmstat 1
      si    so
      8192  16384   ← 8-16 MB/sec swap I/O
      7680  15360
      8704  17408   ← Consistently high
      
      $ iostat -x 1
      Device: rrqm/s wrqm/s  await %util
      sda     0.00   0.00   45.2   99.8  ← Disk saturated

    Root cause:
      - Working set > Physical RAM
      - Kernel constantly swapping pages in/out
      - Page faults on every access
      
    Solutions:
      1. Emergency: Kill memory hog
         $ ps aux --sort=-%mem | head
         $ kill -9 [PID]
         
      2. Temporary: Disable swap
         $ swapoff -a
         → Forces OOM instead of thrashing
         → Better than 30-minute freeze
         
      3. Permanent: Add RAM or reduce working set
         - Scale horizontally (more machines)
         - Reduce cached data
         - Use mmap with MAP_POPULATE cautiously

**Issue 3: High Page Table Overhead**

    Symptoms:
      - PageTables field in /proc/meminfo unusually high
      - OOM kills despite "available" memory
      - Many small memory mappings

    Diagnosis:
      $ cat /proc/meminfo | grep PageTables
      PageTables:     8388608 kB    ← 8 GB in page tables!
      
      $ cat /proc/1234/status | grep VmData
      VmData:    16777216 kB         ← 16 GB virtual
      
      $ cat /proc/1234/maps | wc -l
      45123                          ← 45,000 VMAs!
      
      Overhead: 8 GB PTs for 16 GB data = 50% overhead!

    Root cause:
      - Fragmented memory mappings
      - Many small mmap() calls
      - Database with thousands of memory-mapped files
      
    Solutions:
      1. Enable huge pages (500× reduction):
         $ echo 24576 > /proc/sys/vm/nr_hugepages
         → Pre-allocate 48 GB of huge pages
         
      2. Consolidate mappings:
         - Use fewer, larger mmap() calls
         - Batch allocations
         - Reduce number of mapped files
         
      3. PostgreSQL specific:
         huge_pages = on
         → Shared buffers use huge pages
         → 8 GB overhead → 16 MB

### 8.8.3 Tuning Parameters

``` {.sourceCode .bash}
# Key sysctl parameters for memory management

# Minimum free memory (triggers kswapd)
vm.min_free_kbytes = 32768        # 32 MB minimum
# Too low: Direct reclaim more likely
# Too high: Wastes memory

# Swappiness (0-200, default 60)
vm.swappiness = 10                # Database server
vm.swappiness = 60                # Desktop/general
vm.swappiness = 150               # File server
# Higher = more willing to swap

# Dirty page writeback
vm.dirty_ratio = 20               # 20% max dirty before blocking
vm.dirty_background_ratio = 10   # 10% starts background writeback
# Lower = More frequent writes, less burst latency

# Zone reclaim (NUMA)
vm.zone_reclaim_mode = 0          # Prefer remote memory over reclaim
vm.zone_reclaim_mode = 1          # Prefer local reclaim
# 0 = Better for most workloads
# 1 = NUMA-aware databases

# Overcommit behavior
vm.overcommit_memory = 0          # Heuristic (default)
vm.overcommit_memory = 1          # Always allow
vm.overcommit_memory = 2          # Never overcommit
# 1 = Cloud/container environments
# 2 = Critical systems (database)

# Transparent huge pages
$ cat /sys/kernel/mm/transparent_hugepage/enabled
[always] madvise never
# always = Automatic THP
# madvise = Application controlled
# never = Disabled
```

Real tuning example - PostgreSQL optimization:

``` {.sourceCode .bash}
# Before tuning:
PageTables: 8 GB
Swapping: Heavy (si=5120/s)
Query p99: 2.5 seconds

# Apply tuning:
echo 10 > /proc/sys/vm/swappiness                      # Avoid swap
echo 24576 > /proc/sys/vm/nr_hugepages                 # 48 GB huge pages
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# PostgreSQL config:
huge_pages = on
shared_buffers = 16GB

# After tuning:
PageTables: 512 MB (16× reduction!)
Swapping: None (si=0/s)
Query p99: 180 ms (14× faster!)
TLB miss rate: 8% → 0.3% (27× improvement)
```

------------------------------------------------------------------------

## 8.9 Conclusion: The Complete Picture

We began this chapter with a mystery: a PostgreSQL instance killed by
the OOM killer despite 17 GB of \"available\" memory. Now we can explain
exactly what happened:

    The PostgreSQL OOM Mystery - Solved:

    System: 64 GB RAM, 3 postgres processes

    Problem:
      - Each process: 16 GB shared_buffers + memory-mapped files
      - Virtual address space per process: 48 GB
      - Fragmented mappings: 45,000 VMAs each
      
    Page table overhead calculation:
      - Dense regions: 16 GB → 32 MB PTs each
      - Sparse regions: 32 GB → 64 MB PTs each
      - Total per process: 96 MB
      - Total for 3 processes: 288 MB
      - But with 45,000 VMAs: 2.7 GB per process
      - Grand total: 8.1 GB in page tables!

    The math:
      MemTotal: 64 GB
      Used for data: 48 GB (3 × 16 GB)
      Used for PTs: 8 GB (un-reclaimable!)
      File cache: 6 GB
      Kernel/other: 2 GB
      Total: 64 GB (exactly full!)
      
      MemAvailable reported: 17 GB (file cache + free)
      But PageTables: 8 GB (cannot evict!)
      Actually available: 17 - 8 = 9 GB
      
      New allocation: 10 GB request
      9 GB < 10 GB → OOM!

    Solution applied:
      Enable huge pages:
        - PageTables: 8 GB → 512 MB (16× reduction)
        - Now actually available: 17 GB - 0.5 GB = 16.5 GB
        - 10 GB allocation succeeds
        - Plus: 15% performance improvement from TLB efficiency

### Integration with Previous Chapters

This capstone chapter brings together concepts from throughout the book:

**Chapter 1 (Virtual Memory Abstraction)** introduced process address
spaces. We now understand the **overhead** of that abstraction---page
tables consume memory to enable the mapping.

**Chapter 2 (Demand Paging)** showed how processes don\'t need all pages
in RAM. We now know **which** pages to evict (A/D bits) and **how** to
free them (kswapd, direct reclaim).

**Chapter 3 (Page Tables)** explained multi-level hierarchies. We now
understand **when** to allocate those levels (lazy allocation) and
**when** to free them (reclamation under pressure).

**Chapter 4 (TLB)** showed translation caching. We now know the cost
when TLB fails (page table walks) and why huge pages matter (512× better
coverage).

**Chapter 7 (Page Faults)** covered fault handling. We now understand
**nested** faults in VMs (cascading EPT violations) and **A/D bit**
faults on RISC-V.

Together, these chapters form a complete understanding of the
hardware-software contract for memory management.

### Practical Takeaways

**For System Administrators:**

    Monitoring checklist:
      ✓ Check PageTables in /proc/meminfo weekly
      ✓ Set up alerts for si/so in vmstat
      ✓ Configure OOM killer to protect critical services
      ✓ Tune swappiness for your workload type
      ✓ Consider huge pages for large-memory services

    Configuration:
      - Database servers: swappiness=10, huge pages on
      - File servers: swappiness=150, keep file cache hot
      - Desktops: swappiness=60 (default)
      - VMs: Pre-populate EPT, use huge pages in both guest and host

**For Application Developers:**

    Best practices:
      ✓ Use madvise(MADV_HUGEPAGE) for large allocations
      ✓ Avoid fragmented allocations (many small mmaps)
      ✓ Consider memory-mapped files vs read/write tradeoffs
      ✓ Profile with perf to find TLB thrashing
      ✓ Structure data for spatial locality

    Red flags:
      ✗ Allocating millions of small objects (page table overhead)
      ✗ Random access patterns (TLB thrashing)
      ✗ Frequent mmap/munmap (page table churn)
      ✗ Large sparse mappings (wasted page tables)

**For Hypervisor Operators:**

    Optimization checklist:
      ✓ Pre-populate EPT during VM creation
      ✓ Use 2MB EPT pages when possible
      ✓ Reserve huge page pool at host boot
      ✓ Enable huge pages in both guest and host
      ✓ Monitor EPT fault rate with perf

    VM density calculation:
      Account for:
        - Guest RAM
        - Guest page tables (~0.2% of RAM)
        - Host EPT (~0.2% of RAM)
        - Total: ~1.004 × guest RAM
      
      Example: 16 VMs × 8 GB
        - Guest usage: 128 GB
        - Metadata: 512 MB
        - Total needed: 128.5 GB

### The Big Picture

Memory management in modern systems involves a complex dance between:

- **Hardware** providing mechanisms (A/D bits, TLB, page faults)
- **Hypervisors** multiplexing physical memory (EPT, nested translation)
- **Operating systems** implementing policies (MGLRU, kswapd, OOM)
- **Applications** consuming resources (carefully or carelessly)

Understanding all four layers is essential for: - Debugging production
mysteries - Optimizing performance - Scaling systems efficiently -
Avoiding catastrophic failures

The PostgreSQL mystery we solved demonstrates this. The problem wasn\'t
in any single layer---it was the **interaction** between application
behavior (fragmented mappings), OS bookkeeping (page table overhead),
and hardware constraints (physical RAM limits).

### References

1.  Denning, P. J. \"Virtual Memory.\" *ACM Computing Surveys*, 1970.
2.  Corbató, F. J., et al. \"A Paging Experiment with the Multics
    System.\" *MIT Project MAC*, 1968.
3.  Zhao, Y. \"Multi-Gen LRU.\" *Linux Kernel Documentation*, 2022.
4.  Intel Corporation. \"Intel® 64 and IA-32 Architectures Software
    Developer\'s Manual, Volume 3.\" 2024.
5.  AMD. \"AMD64 Architecture Programmer\'s Manual, Volume 2: System
    Programming.\" 2024.
6.  ARM Ltd. \"ARM Architecture Reference Manual ARMv8.\" 2024.
7.  RISC-V Foundation. \"The RISC-V Instruction Set Manual, Volume II:
    Privileged Architecture.\" 2024.
8.  Gorman, M. \"Understanding the Linux Virtual Memory Manager.\"
    Prentice Hall, 2004.
9.  Love, R. \"Linux Kernel Development,\" 3rd Edition. Addison-Wesley,
    2010.
10. McKusick, M. K., et al. \"The Design and Implementation of the
    4.4BSD Operating System.\" Addison-Wesley, 1996.

**Linux Kernel Source References:** 11. `arch/x86/kvm/mmu/tdp_mmu.c` -
EPT/NPT implementation 12. `arch/x86/kvm/vmx/vmx.c` - EPT violation
handling 13. `arch/arm64/kvm/hyp/exception.c` - ARM64 Stage 2 faults 14.
`mm/vmscan.c` - Page reclaim and kswapd 15. `mm/oom_kill.c` - OOM killer
implementation 16. `mm/memory.c` - Page fault handling and page table
management 17. `mm/huge_memory.c` - Transparent huge pages 18.
`Documentation/admin-guide/mm/multigen_lru.rst` - MGLRU documentation

**Performance Analysis Tools:** 19. Gregg, B. \"Systems Performance:
Enterprise and the Cloud,\" 2nd Edition. Addison-Wesley, 2020. 20.
Gregg, B. \"BPF Performance Tools.\" Addison-Wesley, 2019.

**Additional Reading:** 21. Tanenbaum, A. S., Bos, H. \"Modern Operating
Systems,\" 4th Edition. Pearson, 2014.

------------------------------------------------------------------------

**End of Chapter 8**
