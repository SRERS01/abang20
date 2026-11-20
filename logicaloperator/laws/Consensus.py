### Consensus Theorem in Python for Offensive Security

The Consensus Theorem is a Boolean algebra law used to eliminate redundant terms from complicated logical expressions without changing their Boolean result.

It is useful when auditing authentication, authorization, access-control rules, firewall conditions and application business logic.

### 1\. Mathematical representation

The main Consensus Theorem is:

AB+\\neg AC+BC=AB+\\neg AC

Where:

* represents a Boolean condition.

* represents another condition.

* represents a third condition.

* means OR.

* Multiplication means AND.

* means NOT.

In Python:

```python
(A and B) or (not A and C) or (B and C)
```

is equivalent to:

```python
(A and B) or (not A and C)
```

The term `B and C` is redundant. It is called the consensus term.

### Why is it redundant?

There are two possibilities:

* If A is true, then `A and B` already determines the result when B and C are true.

* If A is false, then `not A and C` already determines the result when B and C are true.

Therefore, `B and C` adds no new true cases.

### 2\. Script 1 — Verify the Consensus Theorem

Create:

```bash
nano consensus_test.py
```

Paste:

```python
from itertools import product

def original(A, B, C):
    return (
        (A and B)
        or (not A and C)
        or (B and C)
    )

def simplified(A, B, C):
    return (
        (A and B)
        or (not A and C)
    )

print("CONSENSUS THEOREM TEST")
print("----------------------")

for A, B, C in product([False, True], repeat=3):

    result1 = original(A, B, C)
    result2 = simplified(A, B, C)

    print(
        f"A={A}, B={B}, C={C} | "
        f"Original={result1}, Simplified={result2}"
    )

    assert result1 == result2

print("\nConsensus theorem verified!")
```

Run:

```bash
python3 consensus_test.py
```

What the script does:

* Tests all eight combinations of A, B and C.

* Compares the original expression with the simplified expression.

* Uses `assert` to verify that both produce identical results.

### 3\. Script 2 — Apply Consensus to authorization logic

Imagine an application has three access conditions:

* A: User has administrator status.

* B: User has a valid permission.

* C: User has a special access condition.

The original authorization expression is:

```python
(admin and permission) or \
(not admin and special_access) or \
(permission and special_access)
```

The simplified expression is:

```python
(admin and permission) or \
(not admin and special_access)
```

Create:

```bash
nano authorization_consensus.py
```

Paste:

```python
def original_access(admin, permission, special_access):

    return (
        (admin and permission)
        or
        (not admin and special_access)
        or
        (permission and special_access)
    )

def simplified_access(admin, permission, special_access):

    return (
        (admin and permission)
        or
        (not admin and special_access)
    )

tests = [
    (True, True, True),
    (True, True, False),
    (True, False, True),
    (False, True, True),
    (False, False, True),
    (False, False, False)
]

for admin, permission, special in tests:

    original = original_access(admin, permission, special)

    simplified = simplified_access(
        admin, permission, special
    )

    print("\nAdmin:", admin)
    print("Permission:", permission)
    print("Special access:", special)

    print("Original:", original)
    print("Simplified:", simplified)
    print("Equivalent:", original == simplified)

    assert original == simplified
```

Run:

```bash
python3 authorization_consensus.py
```

Security impact: You can use this technique to understand whether an authorization expression contains redundant access paths.

Important: The example demonstrates Boolean equivalence, not a recommended authorization design. You must verify that the simplified policy still matches the application's intended security requirements.

### 4\. Script 3 — Test all possible authorization combinations

During bug-bounty testing, you should not test only a few combinations.

Create:

```bash
nano access_matrix_consensus.py
```

Paste:

```python
from itertools import product

def check_access(admin, permission, special):

    return (
        (admin and permission)
        or
        (not admin and special)
    )

print("AUTHORIZATION TEST MATRIX")
print("--------------------------")

for admin, permission, special in product(
    [False, True], repeat=3
):

    access = check_access(
        admin, permission, special
    )

    print(
        f"Admin={admin}, "
        f"Permission={permission}, "
        f"Special={special}, "
        f"Access={access}"
    )

print("\nAll eight combinations tested.")
```

Run:

```bash
python3 access_matrix_consensus.py
```

This is a simple example of exhaustive Boolean testing.

### 5\. Script 4 — Automatically detect a consensus pattern

You can use Python's SymPy library to simplify Boolean expressions.

Install it:

```bash
python3 -m pip install sympy
```

Create:

```bash
nano consensus_sympy.py
```

Paste:

```python
from sympy import symbols, Or, And, Not
from sympy.logic.boolalg import simplify_logic

A, B, C = symbols("A B C")

original = Or(
    And(A, B),
    And(Not(A), C),
    And(B, C)
)

simplified = simplify_logic(
    original,
    form="dnf"
)

print("Original expression:")
print(original)

print("\nSimplified expression:")
print(simplified)

print("\nEquivalent:", simplify_logic(
    Or(
        And(A, B),
        And(Not(A), C),
        And(B, C),
        Not(simplified)
    )
) is False)
```

A simpler and more reliable equivalence check is:

```python
from sympy.logic.boolalg import Equivalent
from sympy import satisfiable

difference = And(
    original,
    Not(simplified)
)

reverse_difference = And(
    simplified,
    Not(original)
)

print("Original differs from simplified:",
      satisfiable(difference) is not False)

print("Simplified differs from original:",
      satisfiable(reverse_difference) is not False)
```

If both differences are unsatisfiable, the expressions are equivalent.

### 6\. Script 5 — Use a SAT-style security condition checker

SAT solving helps determine whether a Boolean expression can ever produce a particular result.

Create:

```bash
nano consensus_sat.py
```

Paste:

```python
from sympy import symbols, And, Or, Not
from sympy.logic.inference import satisfiable

admin, permission, special = symbols(
    "admin permission special"
)

original = Or(
    And(admin, permission),
    And(Not(admin), special),
    And(permission, special)
)

simplified = Or(
    And(admin, permission),
    And(Not(admin), special)
)

difference = Or(
    And(original, Not(simplified)),
    And(simplified, Not(original))
)

result = satisfiable(difference)

if result is False:
    print("Expressions are logically equivalent.")
else:
    print("Expressions differ.")
    print("Counterexample:", result)
```

Run:

```bash
python3 consensus_sat.py
```

This approach is useful when Boolean conditions become too complicated to inspect manually.

### 7\. Security impact in offensive security

| Security area       | Application                                               |
| ------------------- | --------------------------------------------------------- |
| Authentication      | Simplify complicated authentication conditions            |
| Authorization       | Identify redundant permission paths                       |
| IDOR/BOLA           | Examine ownership and alternative access conditions       |
| Firewall auditing   | Simplify combinations of allow/deny rules                 |
| Input validation    | Identify redundant validation terms                       |
| Source-code review  | Find unnecessary Boolean conditions                       |
| Reverse engineering | Simplify conditions found in decompiled code              |
| SAT/SMT analysis    | Check whether certain security conditions are satisfiable |

### Practical bug-bounty example

Suppose you discover:

```python
if (
    (is_admin and has_permission)
    or
    (not is_admin and special_access)
    or
    (has_permission and special_access)
):
    return sensitive_data
```

You can apply the Consensus Theorem to simplify it:

```python
if (
    (is_admin and has_permission)
    or
    (not is_admin and special_access)
):
    return sensitive_data
```

Now you can investigate the two remaining access paths separately.

Questions to ask:

* Is administrator status verified by the server?

* Is permission checked against the requested resource?

* Is special access granted only to authorized users?

* Can an ordinary account reach a protected resource?

* Does the actual backend behaviour match the documented policy?

Important: A mathematically redundant condition is not automatically a vulnerability. Also, Boolean simplification assumes pure Boolean operands; Python functions with side effects or exceptions can make execution behaviour different.

### 8\. Quick revision

Consensus Theorem

AB+\\neg AC+BC=AB+\\neg AC

Python equivalent

```python
(A and B) or (not A and C) or (B and C)
```

simplifies to:

```python
(A and B) or (not A and C)
```

Main lesson: The term `B and C` is redundant.

### 9\. Test your understanding

1. What is the redundant consensus term in AB + ¬AC + BC?

AB

¬AC

BC

2. How many Boolean combinations exist for A, B and C?

4

8

16

3. Does removing a redundant Boolean term automatically create a vulnerability?

Yes

No

Check answers

Next topic: Shannon Expansion Theorem — particularly useful for breaking complex Boolean security conditions into smaller cases and systematically testing every possible access path.
