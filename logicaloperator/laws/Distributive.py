### Boolean Distributive Laws in Offensive Security

The distributive laws explain how to expand or rearrange Boolean expressions without changing their logical result.

There are two main distributive laws:

### 1\. AND distributes over OR

A \\land (B \\lor C)=(A\\land B)\\lor(A\\land C)

In Python:

```python
A and (B or C)
```

is logically equivalent to:

```python
(A and B) or (A and C)
```

Meaning: A must be true, and at least one of B or C must also be true.

### 2\. OR distributes over AND

A \\lor (B\\land C)=(A\\lor B)\\land(A\\lor C)

In Python:

```python
A or (B and C)
```

is logically equivalent to:

```python
(A or B) and (A or C)
```

Meaning: Either A is true, or both B and C are true.

### Why this matters in offensive security

Distributive laws help you break complicated access-control conditions into smaller paths. This can help you identify missing authentication checks, weak role restrictions, and inconsistent authorization logic.

For example:

```python
authenticated and (is_owner or is_admin)
```

means that a user must be authenticated and must either own the resource or be an administrator.

Expanded:

```python
(authenticated and is_owner) or (authenticated and is_admin)
```

You can now inspect the owner path and administrator path separately.

### 3\. Script 1 — Test both distributive laws

Create the file:

```bash
nano distributive_test.py
```

Paste:

```python
from itertools import product

print("AND distributes over OR")
print("A B C | Original | Expanded")
print("-" * 35)

for A, B, C in product([False, True], repeat=3):
    original = A and (B or C)
    expanded = (A and B) or (A and C)

    print(A, B, C, "|", original, "|", expanded)

    assert original == expanded

print("\nOR distributes over AND")
print("A B C | Original | Expanded")
print("-" * 35)

for A, B, C in product([False, True], repeat=3):
    original = A or (B and C)
    expanded = (A or B) and (A or C)

    print(A, B, C, "|", original, "|", expanded)

    assert original == expanded

print("\nBoth distributive laws passed.")
```

Run it:

```bash
python3 distributive_test.py
```

What this script does:

* Tests all 8 possible combinations of A, B and C.

* Compares the original expression with its expanded form.

* Uses `assert` to detect any difference.

* Confirms whether both laws hold for every combination.

### 4\. Script 2 — Analyze an authorization condition

Imagine an application allows access when a user is authenticated and is either the resource owner or an administrator.

Create:

```bash
nano authorization_test.py
```

Paste:

```python
def original_access(authenticated, is_owner, is_admin):
    return authenticated and (is_owner or is_admin)

def expanded_access(authenticated, is_owner, is_admin):
    return (
        (authenticated and is_owner)
        or
        (authenticated and is_admin)
    )

test_cases = [
    (True, True, False),
    (True, False, True),
    (True, False, False),
    (False, True, True),
    (False, True, False),
]

for auth, owner, admin in test_cases:
    original = original_access(auth, owner, admin)
    expanded = expanded_access(auth, owner, admin)

    print(
        f"Authenticated={auth}, Owner={owner}, Admin={admin}"
    )
    print("Original:", original)
    print("Expanded:", expanded)
    print("Equivalent:", original == expanded)
    print("-" * 40)
```

Run:

```bash
python3 authorization_test.py
```

Security interpretation:

| Authentication | Owner | Admin | Access  |
| -------------- | ----- | ----- | ------- |
| True           | True  | False | Granted |
| True           | False | True  | Granted |
| True           | False | False | Denied  |
| False          | True  | True  | Denied  |
| False          | True  | False | Denied  |

The important security check is that being an administrator or owner must not bypass authentication in this example.

### 5\. Script 3 — Find which access path grants permission

This script separates the two authorization paths.

```bash
nano access_paths.py
```

Paste:

```python
def check_access(authenticated, is_owner, is_admin):

    owner_path = authenticated and is_owner
    admin_path = authenticated and is_admin

    access_granted = owner_path or admin_path

    print("Owner path:", owner_path)
    print("Admin path:", admin_path)
    print("Final access:", access_granted)

    if owner_path:
        print("Reason: Authenticated resource owner")

    elif admin_path:
        print("Reason: Authenticated administrator")

    else:
        print("Reason: No valid authorization path")

check_access(
    authenticated=True,
    is_owner=False,
    is_admin=True
)
```

Run:

```bash
python3 access_paths.py
```

This helps you understand why an authorization decision was granted, rather than only seeing `True` or `False`.

### 6\. Script 4 — Test many combinations automatically

You can test all combinations of the authorization conditions:

```bash
nano access_matrix.py
```

Paste:

```python
from itertools import product

print("AUTH OWNER ADMIN | ACCESS")

for auth, owner, admin in product([False, True], repeat=3):

    access = auth and (owner or admin)

    print(
        int(auth),
        int(owner),
        int(admin),
        "|",
        "GRANTED" if access else "DENIED"
    )
```

Run:

```bash
python3 access_matrix.py
```

There are combinations. This is a simple form of exhaustive Boolean testing.

### 7\. How to apply this during bug bounty testing

When reviewing an application you are authorized to test:

* Find authorization conditions in the source code.

* Identify AND and OR operations.

* Apply distributive laws to separate the access paths.

* Check whether every path requires authentication.

* Test each path using accounts and resources you control.

* Check whether the server enforces the same restrictions as the client.

For example, inspect:

```python
if authenticated and (is_owner or is_admin):
    return sensitive_data
```

Ask:

* Can an unauthenticated user reach the sensitive data?

* Can an ordinary user access another user's resource?

* Is the administrator check performed securely?

* Does the backend independently verify ownership?

Important security lesson

A distributive law does not automatically reveal a vulnerability. It helps you understand the logical structure of a security condition so you can test each authorization path.

Important Python caveat: These expressions are equivalent as Boolean formulas when A, B and C are simple Boolean values. If they call functions with side effects, raise exceptions, or modify state, changing their order or grouping can change program behaviour because Python uses short-circuit evaluation.

### 8\. Test your understanding

Question 1. Which expression is equivalent to A and (B or C)?

(A and B) or (A and C)

(A or B) and (A or C)

A or (B and C)

Question 2. A user is authenticated but is neither owner nor admin. What is the result of authenticated and (owner or admin)?

Granted

Denied

Error

Question 3. How many combinations exist for three Boolean variables?

4

6

8

Check answers

Next Boolean law: Absorption law — useful for simplifying complicated authorization conditions.
