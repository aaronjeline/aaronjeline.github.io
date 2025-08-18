% USENIX 2025 Travel Blog
% Aaron Eline
% August 17, 2025
# USENIX 2025 Travel Blog  
  
This past week I attended the 34th USENIX Security conference. I had a great a time and met a bunch of wonderful people. Wanted to take a bit and gather my thoughts on the work I saw presented.   
  
## Conference Format   
  
This year, USENIX adopted a new format. Most talks were only three minutes long, with a couple of selected talks extended to twelve minutes. Poster sessions for all talks immediately followed the talks. This was … okay? Three minutes is really not enough time to do much more than present a verbal abstract. I don’t think I got anything from any of the three-minute talks beyond “hey, maybe I should read that paper”. On the other hand, I really enjoyed having the poster sessions so close to the talks. Having questions fresh in mind made for some great discussions with authors.   
  
## Fuzzing  
  
My reason for attendance was to keep up to date with fuzzing research, and boy was there a lot of it. Before I dive into specific papers, two general observations. Firstly, it’s really a shame that the fuzzing and PBT worlds don’t talk to each other more. Coverage-guided fuzzing is clearly an empirically very good search strategy for finding test cases, but the fuzzing literature seems stuck on only searching for violations of a few blessed properties (usually memory safety via ASan). Additionally, the amount of work that started with the sentence “generating non-textual input with fuzzers is hard” surprised me, given that the PBT and parametric fuzzing communities have worked hard on this problem for years. (Shoutout to the excellent work by Rohan Padye and my colleague Vasu Vikram on bridging this gap). Secondly, boy is differential testing big! Now I’ll go through a selection of the work I found interesting:  
  
* [My ZIP isn't your ZIP: Identifying and Exploiting Semantic Gaps Between ZIP Parsers](https://www.usenix.org/conference/usenixsecurity25/presentation/you) - Diff tested ZIP parsers, revealing a smattering of bugs in popular ZIP implementations and finding that no two ZIP parsers actually parse the same format. I appreciated the speaker directly calling out the need to abandon Postal’s law if we’d like to have secure systems. The also found that the differences in parsing can be used to defeat content scanning systems.   
* [Fuzzing the PHP Interpreter via Dataflow Fusion](Fuzzing%20the%20PHP%20Interpreter%20via%20Dataflow%20Fusion)*. Neat work that uses dataflow graphs as the genetic representation of programs for fuzzing. They define mutation operators on these dataflow graphs. They’ve also put in some great legwork integrating this into the CI for the PHP project, and show continual ability to find bugs. It does make me wonder what the thread model for bugs in a language interpreter (beyond certain notable JS-shaped exceptions) is? I’m already asking it to run arbitrary, un-sandboxed code?  
* [ELFuzz: Efficient Input Generation via LLM-driven Synthesis Over Fuzzer Space](https://www.usenix.org/conference/usenixsecurity25/presentation/chen-chuyang) - Neat paper along the line of work of using language models to improve fuzzing. The conventional wisdom seems to be that using the LLM to generate test cases won’t work for speed reasons (although some counterexamples here!). This work explores using the LLM to generate the generator. In particular, it evolves the generator with several prompt-based mutation strategies, evaluates the new generators on a coverage metric, and selects for N generators that optimize the metric. Seems like this could be especially useful integrated with PBT.  
* [RangeSanitizer: Detecting Memory Errors with Efficient Range Checks](https://www.usenix.org/conference/usenixsecurity25/presentation/gorter) - Not really a fuzzing paper but fuzzers are gonna like it. Improvement on ASan performance that doesn’t lose any bug-finding precision. Clever encoding of red-zones that makes checking really fast. About a 2x speed up on ASan, which means faster fuzzing which means more bugs found. Still likely too slow for production use, sadly.   
*  [Robust, Efficient, and Widely Available Greybox Fuzzing for COTS Binaries with System Call Pattern Feedback](https://www.usenix.org/conference/usenixsecurity25/presentation/xiao-jifan) - Clever idea, using system calls as the feedback mechanism instead of coverage. Doesn’t require instrumentation, and authors claim the metrics correlate well.   
  
## Defensive Papers  
* [Vest: Verified, Secure, High-Performance Parsing and Serialization for Rust](https://www.usenix.org/conference/usenixsecurity25/presentation/cai-yi) - Very nice piece of practical formals methods work! Bringing an Everparse like system to Rust via Kani. Parsers generated here are a little bit more flexible than Everparse’s, and they verify much faster.  
* [SoK: Automated Vulnerability Repair: Methods, Tools, and Assessments](https://www.usenix.org/conference/usenixsecurity25/presentation/hu-yiwei) - A nice SoK on language model based automated patching. Includes a nice dataset.  
  
## Offensive Papers  
  
* [The DOMino Effect: Detecting and Exploiting DOM Clobbering Gadgets via Concolic Execution with Symbolic DOM](https://www.usenix.org/conference/usenixsecurity25/presentation/liu-zhengyu) - Learned about a new exploit here, hadn’t seen DOM Clobbering before. The basic gist is:  
    * The DOM is a global namespace  
    * Scripts may read from that namespace in order to construct security sensitive values, like URLs that will subsequently be queried   
    * Attacker controlled scripts can race to shadow those values, leading to attacker control of the URLs   
    * Paper contains a Concolic execution engine for finding DOM clobbering opportunities.   
* I'll update this as read more! The three minute format makes it hard
  to catch cool insights from topics where you aren't familiar with the
  research area.
  
## Reverse Engineering  
  
Bunch of neat papers here I’m not qualified to comment on! [TRex: Practical Type Reconstruction for Binary Code](https://www.usenix.org/conference/usenixsecurity25/presentation/bosamiya) uses structural type inference to construct types from decompiled programs. I really liked the insight that true type reconstruction isn’t actually possible, you might as well give up and try for something else!
It reminded me of an insight we had working on 3C, and this can really
unlock cool work.
  
## Wrapping Up  
  
All in all, this was a super fun event! Met a bunch of great people. Thanks to all the organizers and presenters and I hope to attend next year!   
  
  
