# Implementing convergent and commutative replicated data types in DistAlgo
<https://sites.google.com/a/stonybrook.edu/sbcs535/projects/crdt-distalgo>

#### Specification for Op-Based Counter - Spec 5: 
An op-based counter as presented in Specification 5. Its payload is an integer. Its empty
atSource clause is omitted; the downstream phase just adds or subtracts locally. It is wellknown
that addition and subtraction commute, assuming no overflow. 
<https://hal.inria.fr/inria-00555588/document>

```
payload integer i
initial 0 
query value () : integer j
  let j = i
update increment ()
  downstream () ⊲ No precond: delivery order is empty
  i := i + 1
update decrement ()
  downstream () ⊲ No precond: delivery order is empty
  i := i − 1
  ```
 
#### Specification for State-based Increment-Only Counter - Spec 6: 
A Counter that only increments. The payload is vector of integers; each source replica is assigned an entry. To increment, add 1 to the entry of the source replica. The value is the sum of all entries. Merge takes the maximum of each entry. 
<https://hal.inria.fr/inria-00555588/document>

```
payload integer[n] P 
  initial [0, 0, . . . , 0]
update increment ()
  let g = myID() 
  P[g] := P[g] + 1
query value () : integer v
  let v = sum(P[i])∀i
compare (X, Y) : boolean b
  let b = (∀i ∈ [0, n − 1] : X.P[i] ≤ Y.P[i])
merge (X, Y ) : payload Z
  let ∀i ∈ [0, n − 1] : Z.P[i] = max(X.P[i], Y.P[i])
```

#### Specification for State-based PN-Counter - Spec 7:
A positive-negative counter (PN-Counter) is a CRDT that can both increase or decrease and converge correctly in the light of commutative operations. Both increment() and decrement() operations are allowed and thus negative values are possible as a result.
<https://hal.inria.fr/inria-00555588/document>

```
payload integer[n] P, integer[n] N ⊲ One entry per replica
initial [0, 0, . . . , 0], [0, 0, . . . , 0]
update increment ()
  let g = myID() 
  P[g] := P[g] + 1
update decrement ()
  let g = myID()
  N[g] := N[g] + 1
query value () : integer v
  let v = sum(P[i])∀i − sum(N[i])∀i
compare (X, Y) : boolean b
  let b = (∀i ∈ [0, n − 1] : X.P[i] ≤ Y.P[i] ∧ ∀i ∈ [0, n − 1] : X.N[i] ≤ Y.N[i])
merge (X, Y ) : payload Z
  let ∀i ∈ [0, n − 1] : Z.P[i] = max(X.P[i], Y.P[i])
  let ∀i ∈ [0, n − 1] : Z.N[i] = max(X.N[i], Y.N[i])
 ```
#### Specification for State-based Last-Writer-Wins Register (LWW-Register) - Spec 8:
Last-write-wins element set (LWW-e-Set) keeps track of element additions and removals but with respect to the timestamp that is attached to each element. Timestamps should be unique and have ordering properties.
<https://hal.inria.fr/inria-00555588/document>

```
payload X x, timestamp t 
  initial ⊥, 0
update assign (X w)
  x, t := w, now() 
query value () : X w
  let w = x
compare (R, R') : boolean b
  let b = (R.t ≤ R'.t)
merge (R, R') : payload R''
  if R.t ≤ R'.t then R''.x, R''.t = R'.x, R'.t
  else R''.x, R''.t = R.x, R.t
```
#### Specification for State-based G-Set - Spec 11: 
A Grow-Only Set (G-Set) supports operations add and lookup only. The G-Set is useful as a building
block for more complex constructions.
<https://hal.inria.fr/inria-00555588/document>

```
payload set A
  initial ∅
update add (element e)
  A := A ∪ {e}
query lookup (element e) : boolean b
  let b = (e ∈ A)
compare (S, T) : boolean b
  let b = (S.A ⊆ T.A)
merge (S, T) : payload U
  let U.A = S.A ∪ T.A
  ```
  
#### Specification for State-based 2P-Set - Spec 12: 
Two-phase set (2P-Set) allows both additions and removals to the set. Internally it comprises of two G-Sets, one to keep track of additions and the other for removals.
<https://hal.inria.fr/inria-00555588/document>

```
payload set A, set R 
  initial ∅, ∅
query lookup (element e) : boolean b
  let b = (e ∈ A ∧ e /∈ R)
update add (element e)
  A := A ∪ {e}
update remove (element e)
  pre lookup(e)
  R := R ∪ {e}
compare (S, T) : boolean b
  let b = (S.A ⊆ T.A ∨ S.R ⊆ T.R)
merge (S, T) : payload U
  let U.A = S.A ∪ T.A
  let U.R = S.R ∪ T.R
```
 #### Specification for Op-based U-Set - Spec 13:
If elements are unique, a removed element will never be added again. If, furthermore, a
downstream precondition ensures that add(e) is delivered before remove(e), there is no need
to record removed elements, and the remove-set is redundant. (Causal delivery is sufficient
to ensure this precondition.) 
<https://hal.inria.fr/inria-00555588/document>

```
payload set S
  initial ∅
query lookup (element e) : boolean b
  let b = (e ∈ S)
update add (element e)
  atSource (e)
    pre e is unique
  downstream (e)
    S := S ∪ {e}
update remove (element e)
  atSource (e)
    pre lookup(e) 
  downstream (e)
    pre add(e) has been delivered ⊲ Causal order suffices
    S := S \ {e}
 ```

 #### Specification for Op-based Observed-Remove Set (OR-Set) - Spec 15:
An OR-Set (Observed-Removed-Set) allows deletion and addition of elements similar to LWW-e-Set, but does not surface only the most recent one. Additions are uniquely tracked via tags and an element is considered member of the set if the deleted set consists of all the tags present within additions.
<https://hal.inria.fr/inria-00555588/document>

```
payload set S ⊲ set of pairs { (element e, unique-tag u), . . . }
  initial ∅
query lookup (element e) : boolean b
  let b = (∃u : (e, u) ∈ S)
update add (element e)
  atSource (e)
    let α = unique()
  downstream (e, α)
     S := S ∪ {(e, α)}
update remove (element e)
  atSource (e)
    pre lookup(e)
    let R = {(e, u)|∃u : (e, u) ∈ S}
  downstream (R)
    pre ∀(e, u) ∈ R : add(e, u) has been delivered 
    S := S \ R 
    
```

#### Specification for 2P2P Graph - Spec 16:
A 2P2P-Graph is the combination of two 2P-Sets, the dependencies between
them are resolved by causal delivery. Dependencies between addEdge and removeEdge,
and between addVertex and removeVertex are resolved as in 2P-Set.
<https://hal.inria.fr/inria-00555588/document>
```
payload set VA, VR, EA, ER
initial ∅, ∅, ∅, ∅
query lookup (vertex v) : boolean b
  let b = (v ∈ (VA \ VR))
query lookup (edge (u, v)) : boolean b
  let b = (lookup(u) ∧ lookup(v) ∧ (u, v) ∈ (EA \ ER))
update addVertex (vertex w)
   atSource (w)
downstream (w)
   VA := VA ∪ {w}
update addEdge (vertex u, vertex v)
   atSource (u, v)
     pre lookup(u) ∧ lookup(v) ⊲ Graph precondition: E ⊆ V × V
   downstream (u, v)
     EA := EA ∪ {(u, v)}
update removeVertex (vertex w)
   atSource (w)
    pre lookup(w) ⊲ 2P-Set precondition
    pre ∀(u, v) ∈ (EA \ ER) : u 6= w ∧ v 6= w ⊲ Graph precondition: E ⊆ V × V
   downstream (w)
    pre addVertex(w) delivered ⊲ 2P-Set precondition
    VR := VR ∪ {w}
update removeEdge (edge (u, v))
   atSource ((u, v))
    pre lookup((u, v)) ⊲ 2P-Set precondition
   downstream (u, v)
    pre addEdge(u, v) delivered ⊲ 2P-Set precondition
    ER := ER ∪ {(u, v)}
