% Verifying A Wacky Sparse Set Implementation (Part 1)
% Aaron Eline
% May 19, 2024

# Verifying A Wacky Sparse Set Implementation (Part 1)

One of my favorite blog posts is Russ Cox’s [Using Uninitialized Memory for Fun and Profit](https://research.swtch.com/sparse), which describes a very clever sparse set implementation that that involves reading from uninitialized memory. I thought it would be fun to try and build a formally verified implementation of this data-structure in Dafny. If you’re already familiar with Dafny and formal verification, skip to [Part 2](lol)

## What is Dafny?

[Dafny](https://dafny.org) is a “verification-aware programming language” that uses automated reasoning to prove program invariants at compile time. This lets you ensure things about all possible executions of your programs, instead of just testing various cases. As a simple example, let’s write an absolute value function:

```dafny
method abs(x : int) returns (r : int) {
   r := x;
}
```

This denotes a `method` named `abs` that takes single an integer as a parameter, and returns an integer named `r`. Most language don’t’ have you named your return values, but we’ll see why dafny does in a minute. It’s hard to write code without bugs (keen eyed readers may have spotted one!): so let’s try to verify that the method is correct:

```dafny
method abs(x : int) returns (r : int)
ensures r >= 0
{
		r := x;
}
```

We’ve added an `ensures` clause to the method signature, saying that after this method returns, `r` must be greater than or equal to `0`. (This is why we need to name the return value, if we don’t name it we can’t talk about it) `ensures` clauses form a methods “Contract”, the set of rules it guarantees to uphold for all possible inputs. This method will now fail to compile, because we clearly don’t uphold the contract. If we adjust the body to say:

```
{
  if x < 0 {
    r := -x;
  } else {
    r := x;
  }
}
```

Now it’ll compile. Dafny knows that in the true-branch, `x` will be less than zero, so `-x` will be greater than zero, so indeed `r` will be greater than or equal to zero. Likewise, in the false-branch: `x` must be greater than or equal to zero, so assigning to `r` will make `r` greater than or equal to zero. Dafny figures this using an automated reasoning technique called a [SMT Solver](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories). There’s an important lesson to point out here: _verification is only as good as your specification_.

```dafny
method abs(x : int) returns (r : int)
ensures r >= 0
{
  r := 5;
}
```

This will also compile, and clearly does meet the specification, but also clearly does not implement an absolute value function!

There’s another way we could have gotten the method to compile, which is to add a `requires` clause:

```
method abs(x : int) returns (r : int)
requires x >= 0
ensures r >= 0
{
  r := x;
}
```

This compiles, and will result in dafny ensuring that at every call to `abs`, it’s impossible for `x` to be less than `0`. Since `x` must be greater than or equal to zero, and all we do is assign `r` to `x`, then clearly the `ensures`1 clause also holds. Obviously this makes `abs` pretty useless, but demonstrates both sides of the Contract mechanism. Dafny attempts to have most of the features you’d expect from a modern language, including objects, first-class functions, and algebraic types. We’ll try to use to ensure we implement the data structure Cox describes correctly.

## Round One: a simple set data structure

Before trying to prove anything the cool safety-violating structure, let’s write probably the simplest possible set data structure: one backed by a flat array containing all of the members.

```dafny
class ArraySet {
}
```

Our set will be represented as an object, with two fields:

```dafny
var arr : array<boo>
```

`arr` will track which integers are part of the set: `arr[i]` being `true` will means `i` is a member of these set.

```dafny
ghost var spec : set<nat>
```

`ghost` vars are a neat feature of dafny. They instruct the compiler that a variable/function should _not_ be including the compiled program, but instead should only be used for compile-team reasoning. In this case, we’re using the a ghost var that corresponds to Dafny’s built-in mathematical notion of Sets.

### Validity Predicate

Now we’ll define our first method. This method will be in charge of ensuring that the actual data structure (`arr`) corresponds with the mathematical set (the `ghost` set):

```dafny
ghost function valid() : bool
{
   ...
}
```

This is a `ghost function`: `ghost` again meaning “don’t actually compile this, just use it for compile-time proving” and `function` meaning that the block of code has no side effects and always terminates. In order to use code in a proof, it must be a `function`.

So how do we actually check that the two structures correspond:

```
{
  (set x : int | 0 <= x < this.arr.Length && this.arr[x] == true) == this.spec
}
```

This is a “set comprehension” (similar to list comprehensions, but you know, for sets). It instructs Dafny to create a set containing every integer for which the expression after `|` evaluates to `true`. In this case that’s every integer that’s in bound of the array, and for which that position of the array is set to `true`, exactly the interpretation we specified above. Then we check that our constructed set is equal to our `spec` variable. If it is: we’re valid!

### Constructor

Here’s the specification for the constructor:

```dafny
constructor(size : nat)
ensures valid()
ensures spec == {}
```

This means that when the constructor is finished, two things must be true: 1. `valid()` must evaluate to `true` 2. `spec` must be equal to the empty set

Taken together: that means that the data structure must represent the empty set. This should be trivial, we just need to construct a big array of `false`.

```dafny
{
  spec := {}; // Make spec the empty set: ez pz
  // Allocate a new array, contains unintialized memory
  var arr := new bool[size];
  var i := 0;
  while (i < arr.length)
  {
	  arr[i] := false;
	  i := i + 1;
  }
  this.arr := arr;
}
```

This looks right, but won’t actually compile. Not because it’s wrong: but because Dafny isn’t able to prove that it’s right. Modern SMT solvers are very cool but aren’t magical: sometimes we’re going to need to give Dafny a helping hand.

Firstly: Dafny ins’t able to prove that our `while` loop will always terminate. We can help Dafny out by writing “loop invariants”: an expression that will be true every pass through the loop. Here’s one that will help Dafny prove the loop terminates:

```dafny
invariant 0 <= i <= arr.Length
```

Dafny now complains it’s not able to prove that `valid()` will be true. We know that `spec == {}`, and in order for `valid()` to be true, we need to make sure that `arr` only contains `false`. We can convince Dafny we’ve done this by adding an invariant showing that every time through the loop, we make progress towards every element being `false`:

```dafny
invariant forall j : nat :: j < i ==> arr[i] == false
```

Breaking this down:

- `forall j : nat` This invariant will be true for every possible Natural number (numbers >= `0`). Assign `j` to be an arbitrary natural number.
- `j < i ==> arr[i] == false`: The `==>` operator is logical implication. So if `j < i` then `arr[i]` must be `false`.
- In total: this says that every array entry less than `i` will be `false`, and since `i` is always increasing: this loop will eventually fill the whole array.
  With these two invariants Dafny gives us the sign off.

### Membership Check

First we’ll write the method for checking if a given number is in the set. Let’s again start with our specification:

```dafny
method is_number(x : nat) returns (r : bool)
requires valid()
ensures valid()
ensures r == (x in spec)
{
  ...
}
```

We’ve got one precondition and two post-conditions in the contract. First: we require that this method can only be called on a valid set. There’s no way we can guarantee anything about the method if you hand us a set that’s already in an inconsistent state. Secondly: we promise we’ll leave the set in valid state when we’re done. Finally, we promise that our return value `r` will be true if and only if `x` is indeed in the `spec` set. (Remember: `spec` is only around at compile-time, it doesn’t exist at all at runtime.

Here’s a first pass at implementing the body:

```dafny
{
  r := arr[x];
}
```

And again, Dafny complains. This time for actual mistake we’ve made. We didn’t check that `x` was in bounds of the array.

Pass #2:

```dafny
{
  if (x < this.arr.Length) {
    r := arr[x];
  } else { // If `x` is out of bounds it can't be in the set
    r := false;
  }
}
```

And no complaints! Dafny was able to prove we met all the specifications by itself. Neat. You’ll note we only had to check the upper bound of the array, and didn’t check that `x` was greater than or equal to `0`, because we declared that `x` had type `nat` instead of `int`.

### Insertion

Finally, let’s write the method for inserting elements into the set. As usual, we’ll start with the spec:

```dafny
// Attempt to insert `x` into the set.
// Returns `false` if insertion fails
method insert(x : nat) returns (r : bool)
requires valid()
ensures valid()
...
```

Again we require a valid set and promise to return a valid set.

```dafny
...
ensures !r ==> spec == old(spec)
...
```

If `r` is false (meaning that insertion failed), we want to ensure that the set is unchanged. The `old()` syntax allows us to refer to the value of `spec` when we entered the method. So we assert that if `r` is false, the value of `spec` must be equal to what it was when the method was called.

```dafny
...
ensures r ==> spec == old(spec) + {x}
...
```

On the other hand, if `r` is true, we want `spec` to be equal to the union of its original value and the set containing just `x`.

```
...
modifies this
modifies this.arr
```

Finally: Dafny requires us to annotate what fields we’re going to mutate. To repeat: here’s the full spec:

```
method insert(x : nat) returns (r : bool)
requires valid()
ensures valid()
ensures !r ==> spec == old(spec)
ensures r ==> spec == old(spec) + {x}
modifies this
modifies this.arr
{
  ...
}
```

And now for the body:

```
{
  if (x < this.arr.Length) {
    // Update the spec.
    spec := spec + {x};
    // Update the real array
    arr[x] := true;
    // Insertion succeeds
    r := true;
  } else {
    r := false;
  }
}
```

And again: Dafny is able to prove it all automatically. It might seem weird that we can update the value of `spec`, since we said it doesn’t exist at runtime. That update is only used for the purposes of proving things, and dafny is able to verify that the value of `spec` doesn’t actually influence the return value of this method in any way. If it did, it would be an error.

## Recap

We’ve proven that a simple set implementation corresponds to Dafny’s mathematical Set object. This isn’t a very good set implementation though (it allocates enough space to store every member of the set even when the set is empty), so next time we’ll follow the same methodology, but for a much cooler data structure.
