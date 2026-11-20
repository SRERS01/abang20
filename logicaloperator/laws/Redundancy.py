### Redundancy Law in Boolean Algebra

The Redundancy Law states that a Boolean expression may contain a term that does not change the final result. That unnecessary term is called a redundant term.

In offensive security, redundancy analysis helps you identify unnecessary conditions in authentication, authorization, access-control rules, firewall policies, and application logic.

### 1\. Main redundancy laws

Law 1:

A \\lor (A \\land B)=A

Python:

```python
A or (A and B) == A
```

Meaning: Once `A` is True, adding `A and B` does not change the result.

Law 2:

A \\land (A \\lor B)=A

Python:

```python
A and (A or B) == A
```

Meaning: If `A` is False, the whole expression is False. If `A` is True, the expression is True regardless of `B`.

Law 3:

(A \\land B)\\lor(A\\land \\neg B)=A

Python:

```python
(A and B) or (A and not B)
```

Simplifies to:

```python
A
```

Meaning: Whether `B` is True or False, the result depends only on `A`.

### 2\. How redundancy appears in offensive security

Imagine an application has this access-control condition:

```python
is_admin = True
is_owner = False

access = is_admin or (is_admin and is_owner)

print(access)
```

The expression simplifies to:

```python
access = is_admin
```

The ownership condition does not affect the result whenever the user is an administrator.

Security implication: When reviewing authorization code, identify conditions that appear important but do not actually restrict access. Confirm whether that is the intended policy before calling it a vulnerability.

### 3\. Test redundancy using Python

Create a file:

```bash
nano redundancy_test.py
```

Insert:

```python
from itertools import product

def original(A, B):
    return A or (A and B)

def simplified(A, B):
    return A

print("A | B | Original | Simplified")

for A, B in product([False, True], repeat=2):
    result1 = original(A, B)
    result2 = simplified(A, B)

    print(A, B, result1, result2)

    assert result1 == result2

print("\nBoth expressions are equivalent.")
```

Run:

```bash
python3 redundancy_test.py
```

Expected output:

```text
A | B | Original | Simplified
False False False False
False True  False False
True  False True  True
True  True  True  True

Both expressions are equivalent.
```

### 4\. Apply redundancy analysis to authorization

Create:

```bash
nano authorization_audit.py
```

Insert:

```python
def original_access(authenticated, is_admin, is_owner):
    return (
        authenticated and
        (is_admin or (is_admin and is_owner))
    )

def simplified_access(authenticated, is_admin):
    return authenticated and is_admin

test_cases = [
    (True, True, True),
    (True, True, False),
    (True, False, True),
    (False, True, True),
]

for auth, admin, owner in test_cases:

    old = original_access(auth, admin, owner)
    new = simplified_access(auth, admin)

    print(
        f"Authenticated={auth}, "
        f"Admin={admin}, "
        f"Owner={owner}, "
        f"Original={old}, "
        f"Simplified={new}"
    )

    assert old == new
```

Run:

```bash
python3 authorization_audit.py
```

This tests whether the ownership condition is redundant in this particular authorization expression.

### 5\. Where to investigate redundancy during bug bounty

| Security area       | What to investigate                                 |
| ------------------- | --------------------------------------------------- |
| Authentication      | Unnecessary login conditions                        |
| Authorization       | Redundant role and ownership checks                 |
| IDOR/BOLA           | Whether ownership checks actually affect access     |
| API security        | Conditions that do not restrict sensitive endpoints |
| Session management  | Unnecessary or ineffective session conditions       |
| Firewall rules      | Duplicate or ineffective access rules               |
| Feature permissions | Permission checks that do not change the outcome    |

### 6\. Important distinction

Redundancy is not automatically a vulnerability.

For example:

```python
access = is_admin or (is_admin and is_owner)
```

is logically equivalent to:

```python
access = is_admin
```

But if the intended policy requires both administrator privileges and ownership, the original expression is already incorrectly designed. The real issue is the mismatch between the intended security policy and the implemented condition.

Also, Boolean simplification assumes pure Boolean values. Python functions with side effects or exceptions may behave differently when redundant terms are removed.

### 7\. Your practical challenge

Test your understanding

1. Simplify: A or (A and B)

A

B

A and B

2. Simplify: A and (A or B)

A or B

A

B

3. If an ownership condition is redundant in an access-control expression, what should you do?

Immediately exploit it

Check the intended authorization policy

Delete the condition

0 of 3 answered

Reset quiz

Next topic: Boolean Complementation and Redundancy in complex access-control expressions.
