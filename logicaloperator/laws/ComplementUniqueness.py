### Complement Uniqueness Law in Boolean Algebra

The Complement Uniqueness Law states that every Boolean variable has exactly one complement.

In simple terms, for a Boolean variable , there is only one value that can serve as its complement and satisfy both complement laws.

### 1\. The mathematical law

If is the complement of , then:

A \\land B = 0A \\lor B = 1

Therefore:

\\boxed{B=\\neg A}

The complement is unique because no other Boolean value can satisfy both equations.

### Truth table

| A     | Complement B | A AND B | A OR B |
| ----- | ------------ | ------- | ------ |
| False | True         | False   | True   |
| True  | False        | False   | True   |

### 2\. Python implementation

Create a file:

```bash
nano complement_uniqueness.py
```

Insert:

```python
from itertools import product

def check_complement(A, B):
    return (A and B) == False and (A or B) == True

for A, B in product([False, True], repeat=2):
    if check_complement(A, B):
        print(f"A={A}, B={B}: Valid complement")
    else:
        print(f"A={A}, B={B}: Not a complement")
```

Run:

```bash
python3 complement_uniqueness.py
```

Expected output:

```text
A=False, B=False: Not a complement
A=False, B=True: Valid complement
A=True, B=False: Valid complement
A=True, B=True: Not a complement
```

Notice that each value of `A` has exactly one valid complement.

### 3\. Application in offensive security

Complement uniqueness is useful when auditing security conditions that depend on opposite states.

For example:

```python
is_authenticated = True
is_unauthenticated = not is_authenticated

print(is_authenticated)
print(is_unauthenticated)
```

Output:

```text
True
False
```

The two states are logical opposites.

### Security areas to investigate

| Security area      | What to examine                             |
| ------------------ | ------------------------------------------- |
| Authentication     | Authenticated versus unauthenticated states |
| Authorization      | Authorized versus unauthorized decisions    |
| Session management | Valid versus invalid session states         |
| Firewall logic     | Allowed versus denied traffic               |
| Input validation   | Valid versus invalid input conditions       |
| API security       | Permitted versus rejected requests          |

### 4\. Practical security audit script

Suppose you are reviewing an application's access decision.

```python
def audit_access(authenticated, denied):
    expected_denied = not authenticated

    if denied != expected_denied:
        print("[!] Inconsistent authentication states")
    else:
        print("[+] Complement relationship is correct")

audit_access(True, False)
audit_access(False, True)
audit_access(True, True)
```

The third test reports an inconsistency because a user cannot simultaneously be authenticated and denied under this particular assumed two-state model.

Important: Real applications may have more than two states, such as expired, locked, pending verification, or disabled. Do not assume every denied user is simply unauthenticated.

### 5\. Why this matters in bug bounty

When reviewing source code, ask:

* Does the application correctly distinguish authenticated and unauthenticated users?

* Can contradictory security states occur?

* Are authorization decisions based on reliable server-side state?

* Can an expired session still be treated as valid?

* Are denial conditions correctly implemented?

Complement uniqueness helps reason about logical consistency. It does not independently detect vulnerabilities.

### 6\. Test your understanding

1. If A = True, what is its unique complement?

True

False

2. Can False and True both be complements of the same Boolean value A?

Yes

No

3. What does complement uniqueness help you examine in security code?

Contradictory logical states

Network speed

File compression

Reset quiz

Next Boolean law: De Morgan's Laws — particularly useful for understanding how negation changes complex authentication and authorization conditions.
