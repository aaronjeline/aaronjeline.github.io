# Readings
This page contains a collections of interesting resources, across a
variety of topics. My main criterion for posting here is that I found it
interesting or useful. My only rule is that I have to have actually read
it to post it here. Suggestions always welcome. Page inspired by the
great one at [mcyoung.xyz](https://mcyoung.xyz/syllabus).

## Programming Language Theory/Type Theory
Resources on the formal definitions of programming languages and type
systems. While real languages are always more than theoretical models,
it's essential to ground in these models. You can prevent making
mistakes that have been made before, have consistency in your design, 
and make sure that your type system actually guarantees something.

* By the god Benjamin Pierce
    * [Software Foundations](https://softwarefoundations.cis.upenn.edu) The first two volumes have you learning the Coq
      proof assistant and build up to your formalizing and proving
      things about simple imperative and functional languages, as well as
      a simple type system and all of the basic extensions. It's a great
      foundational text. (Many more people than just Benjamin Pierce
      contributed to this)
    * [Types and Programming Languages](https://www.cis.upenn.edu/~bcpierce/tapl/) 
        TAPL is a masterpiece. It goes into greater depth on topics than
        SF, at the cost of not all being formalized in Coq.
    * [Advanced Topics in Types and Programming Languages](https://www.cis.upenn.edu/~bcpierce/attapl/) 
        ATAPL Covers a bunch of the wacky things not covered in TAPL,
        such as: types systems for assembly languages, dependent types, substructural
        types.
* [Programming Languages: Applications and
  Interpretations](https://www.plai.org/3/2/PLAI%20Version%203.2.2%20electronic.pdf)
  Introduces a wide variety of languages features and ideas via simple interpreters.
* [The Little Typer](https://thelittletyper.com/) A very cool Socratic
  style introduction to dependent type theory
* [Interpreters Chapter from
  SICP](https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/full-text/book/book-Z-H-25.html#%_chap_4)
  Fun chapter on implementing a core interpreter for a simple functional
  language and expanding it with wacky features

## Programming Language Design
Moving away from considering languages as abstract mathematical objects,
this is a series of posts that talk about language _design_. 

* [Let Futures Be
  Futures](https://without.boats/blog/let-futures-be-futures/) Notes on
  the design of async Rust.
* [Ownership](https://without.boats/blog/ownership/) How to take
  advantage of substructural type systems in a language
* [References are like
  jumps](https://without.boats/blog/references-are-like-jumps/) on
  how languages can enable or interface with "local reasoning" about
  whether your program is correct
* [The Rust I wanted had no
  future](https://graydon2.dreamwidth.org/307291.html) Essay from
  Graydon Hoare, the original creator of Rust, about how the project has
  diverged from where he thought it would go. Talks about why it
  diverged and how.
* [I want off Mr. Golang's Wild
  Ride](https://fasterthanli.me/articles/i-want-off-mr-golangs-wild-ride) on how languages 
    (and specifically their standard libraries and type systems) can
    help make software either robust or fragile.

## Compilers
Notes on (usually optimizing) compilers. Fast languages use compilers.
Compilers are cool. I like compilers.

* [MinCaml](https://esumii.github.io/min-caml/paper.pdf) Paper on a nice
  simple compiler for functional languages.
* [CS
  6120](https://www.cs.cornell.edu/courses/cs6120/2020fa/self-guided/)
  Not a reading, but a set of lectures. 
* [A Guide to Undefined Behaviour in C and
  C++](https://blog.regehr.org/archives/213),[Part
  2](https://blog.regehr.org/archives/226),[Part 3](https://blog.regehr.org/archives/232) A guide to thinking about what undefined behaviour means.
  An important quote form the article:

> It is very common for people to say — or at least think — something like this:
> The x86 ADD instruction is used to implement C’s signed add operation, and it has two’s complement behavior when the result overflows. I’m developing for an x86 platform, so I should be able to expect two’s complement semantics when 32-bit signed integers overflow.
> THIS IS WRONG. You are saying something like this:
> Somebody once told me that in basketball you can’t hold the ball and run. I got a basketball and tried it and it worked just fine. He obviously didn’t understand basketball.

* [What Every C Programmer Should Know About Undefined
  Behaviour](https://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html) [Part 2](https://blog.llvm.org/2011/05/what-every-c-programmer-should-know_14.html) [Part 3](https://blog.llvm.org/2011/05/what-every-c-programmer-should-know_21.html)
    Explains a lot of the optimizations that undefined behaviour
    enables. If you're a language safety advocate (like me), it's important to understand this.
* [Notes on Type Layout and ABIs in
  Rust](https://faultlore.com/blah/rust-layouts-and-abis/) and [How
  Swift Achieved Dynamic Linking Where Rust
  Couldn't](https://faultlore.com/blah/swift-abi/) and [C isn't a
  Programming Language
  Anymore](https://faultlore.com/blah/c-isnt-a-language/) The best
  collections of articles on dynamic linking/ABIs.
* [Formal verification of a realistic
  compiler](https://xavierleroy.org/publi/compcert-CACM.pdf) The
  CompCERT project: a formally verified compiler for C
* [Proving the correctness of a
  compiler](https://xavierleroy.org/courses/EUTypes-2019/) By the same
  author as the above, but about a much simpler language
* [The implementation of functional programming
  languages](https://www.microsoft.com/en-us/research/wp-content/uploads/1987/01/slpj-book-1987-small.pdf)
  Implementing a compiler/runtime for a lazy,functional programming
  language (think Haskell)

## Security 
* [Building a HashMap in
  Rust](https://cglab.ca/~abeinges/blah/robinhood-part-1/) I promise
  this is actually a security article
* [What is memory
  safety](http://www.pl-enthusiast.net/2014/07/21/memory-safety/)
  Getting a good rigorous definition of memory safety
* [Software Security is a Programming Languages
  Issue](http://www.pl-enthusiast.net/2018/08/13/security-programming-languages-issue/)
  Makes the argument that PL theory/design is essential for improving
  the security of the ecosystem.
* [Cedar: a new language for
  Authorization](https://arxiv.org/pdf/2403.04651) Paper on the Cedar
  language I was (and am) involved with designing

## Automated Reasoning/Formal Methods
This topic is really cool. It's also frustratingly opaque. There is no
equivalent of "software foundations" for other AR techniques, and that's a
shame.

* [CSE 507 - Computer Aided Reasoning for
  Software](https://courses.cs.washington.edu/courses/cse507/21au/calendar.html)
  Great course
* [The Rosette
  Guide](https://docs.racket-lang.org/rosette-guide/index.html) A cool
  tool for solver assisted programming
* [Formal Methods: Just Good Engineering
  Practice?](https://brooker.co.za/blog/2024/04/17/formal.html) 
* [Formal Methods only solve half my
  problems](https://brooker.co.za/blog/2022/06/02/formal.html)
* Decision Procedures by Daniel Kroenig
* Handbook of Satisfiability, second edition

## Things That Will Bite You
* [The Absolute Minimum Every Software Developer Must Know About
  Unicode](https://tonsky.me/blog/unicode/) ASCII is dead. This isn't
  that complicated if your read it.
* [Text Rendering Hates You](https://faultlore.com/blah/text-hates-you/)
* [Falsehoods programmers believe about
  timezones](https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time)

## Systems - distributed or otherwise
* [Atomic Commitment: The Unscalability
  Protocol](https://brooker.co.za/blog/2022/10/04/commitment.html)
* [Not Just Scale](https://brooker.co.za/blog/2024/06/04/scale.html)
  What's the point of this cloud thing anyway?
* [Metastable Failures in Distributed
  Systems](https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s11-bronson.pdf)
* [IronFleet: Proving Practical Distributed Systems
  Correct](https://www.cs.columbia.edu/~junfeng/17sp-e6121/papers/ironfleet.pdf)


## Software Engineering
* [Parse, don't
  validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)
* [Choosing Properties for Property Based
  Testing](https://fsharpforfunandprofit.com/posts/property-based-testing-2/)
* [How we build Cedar: A Verification Guided
  Approach](https://arxiv.org/pdf/2407.01688) Paper on our development
  methodology for Cedar
