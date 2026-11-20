### Boolean Absorption Laws in Offensive Security

The absorption laws are Boolean algebra rules used to simplify logical expressions by removing redundant conditions without changing their logical result.

There are two main absorption laws.

### 1\. First absorption law

A \\lor (A \\land B)=A

In Python:

```python
A or (A and B)
```

is logically equivalent to:

```python
A
```

Meaning: If A is already true, adding `A and B` does not change the result.

Example:

```python
is_admin or (is_admin and is_owner)
```

Simplifies to:

```python
is_admin
```

The ownership condition is redundant in this particular expression.

### 2\. Second absorption law

A \\land (A \\lor B)=A

In Python:

```python
A and (A or B)
```

is logically equivalent to:

```python
A
```

Meaning: If A is false, the entire expression is false. If A is true, `A or B` is already true.

Example:

```python
authenticated and (authenticated or is_admin)
```

Simplifies to:

```python
authenticated
```

The administrator condition does not affect the result.

### 3\. Why absorption matters in offensive security

Absorption can help you identify:

* Redundant authentication checks.

* Unnecessary authorization conditions.

* Confusing role-based access logic.

* Conditions that look protective but do not actually restrict access.

* Dead or ineffective Boolean checks.

Remember: a redundant condition is not automatically a vulnerability. You must understand what the application is supposed to enforce.

### 4\. Script 1 — Test both absorption laws

Create:

```bash
nano absorption_test.py
```

Paste:

```python
from itertools import product

print("FIRST ABSORPTION LAW")
print("A B | Original | Simplified")

for A, B in product([False, True], repeat=2):
    original = A or (A and B)
    simplified = A

    print(A, B, "|", original, "|", simplified)

    assert original == simplified

print("\nSECOND ABSORPTION LAW")
print("A B | Original | Simplified")

for A, B in product([False, True], repeat=2):
    original = A and (A or B)
    simplified = A

    print(A, B, "|", original, "|", simplified)

    assert original == simplified

print("\nBoth absorption laws passed.")
```

Run:

```bash
python3 absorption_test.py
```

What it does:

* Tests all four possible combinations of A and B.

* Compares the original and simplified expressions.

* Uses `assert` to verify equivalence.

### 5\. Script 2 — Find redundant authorization conditions

Imagine an application uses:

```python
is_admin or (is_admin and is_owner)
```

Create:

```bash
nano redundant_check.py
```

Paste:

```python
def original_check(is_admin, is_owner):
    return is_admin or (is_admin and is_owner)

def simplified_check(is_admin, is_owner):
    return is_admin

tests = [
    (False, False),
    (False, True),
    (True, False),
    (True, True),
]

for admin, owner in tests:

    original = original_check(admin, owner)
    simplified = simplified_check(admin, owner)

    print("Admin:", admin, "Owner:", owner)
    print("Original result:", original)
    print("Simplified result:", simplified)
    print("Equivalent:", original == simplified)
    print("-" * 35)
```

Run:

```bash
python3 redundant_check.py
```

Security interpretation: The ownership check adds no restriction because the administrator condition alone determines the result.

### 6\. Script 3 — Analyze authentication logic

Consider:

```python
authenticated and (authenticated or is_admin)
```

Create:

```bash
nano auth_absorption.py
```

Paste:

```python
def original_access(authenticated, is_admin):
    return authenticated and (
        authenticated or is_admin
    )

def simplified_access(authenticated, is_admin):
    return authenticated

for auth in [False, True]:
    for admin in [False, True]:

        original = original_access(auth, admin)
        simplified = simplified_access(auth, admin)

        print(
            f"Authenticated={auth}, Admin={admin}"
        )

        print("Original:", original)
        print("Simplified:", simplified)
        print("Equivalent:", original == simplified)
        print("-" * 35)
```

Run:

```bash
python3 auth_absorption.py
```

This demonstrates that the administrator condition does not change the access decision in this particular expression.

### 7\. Script 4 — Automatically test absorption across many inputs

This example tests both laws using generated Boolean inputs.

```bash
nano absorption_audit.py
```

```python
from itertools import product

def audit_absorption():
    passed = 0
    failed = 0

    for A, B in product([False, True], repeat=2):

        law_one = A or (A and B)
        law_two = A and (A or B)

        if law_one == A:
            passed += 1
        else:
            failed += 1

        if law_two == A:
            passed += 1
        else:
            failed += 1

    print("Tests passed:", passed)
    print("Tests failed:", failed)

    if failed == 0:
        print("Both absorption laws verified.")

audit_absorption()
```

Run:

```bash
python3 absorption_audit.py
```

Expected result

```text
Tests passed: 8
Tests failed: 0
Both absorption laws verified.
```

### 8\. How to use absorption during a bug bounty

When examining an authorization condition, look for patterns such as:

```python
if is_admin or (is_admin and has_permission):
    allow_access()
```

Simplification:

```python
if is_admin:
    allow_access()
```

Questions to investigate:

* Was `has_permission` intended to restrict administrator access?

* Does the actual implementation match the documented access policy?

* Are ordinary users prevented from accessing administrator functions?

* Does the backend enforce the correct permissions?

* Are there other checks outside this particular expression?

Important: Boolean equivalence assumes pure Boolean values. Python short-circuit evaluation means replacing an expression can change whether a function is called, whether an exception occurs, or whether a side effect happens.

### 9\. Quick revision table

| Law               | Original       | Simplified |
| ----------------- | -------------- | ---------- |
| First absorption  | A or (A and B) | A          |
| Second absorption | A and (A or B) | A          |

### 10\. Test your understanding

1. Simplify A or (A and B).

A

B

A and B

2. Simplify A and (A or B).

A or B

A

B

3. If is_admin or (is_admin and is_owner) is true, which condition determines the result?

is_owner

is_admin

Both equally

Check answers

Next topic: De Morgan's Laws — particularly useful for understanding negated authentication and authorization conditions.
