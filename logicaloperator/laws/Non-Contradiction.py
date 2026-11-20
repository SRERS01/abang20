### Law of Non-Contradiction in Python for Offensive Security

The Law of Non-Contradiction states that a proposition cannot be both true and false at the same time in classical Boolean logic.

It is particularly useful when auditing authentication, authorization, access-control rules, input validation and security conditions.

### 1\. Mathematical representation

A \\land \\neg A = False

Python:

```python
A and (not A)
```

This expression always evaluates to `False` when A is a Boolean value.

Examples:

```python
A = True
print(A and not A)  # False

A = False
print(A and not A)  # False
```

Why?

| A     | NOT A | A AND NOT A |
| ----- | ----- | ----------- |
| True  | False | False       |
| False | True  | False       |

A cannot be true and false simultaneously.

### 2\. Script 1 — Verify the non-contradiction law

Create:

```bash
nano non_contradiction.py
```

Paste:

```python
values = [True, False]

print("LAW OF NON-CONTRADICTION")
print("------------------------")

for A in values:

    result = A and (not A)

    print("A:", A)
    print("NOT A:", not A)
    print("A AND NOT A:", result)

    assert result is False

print("\nNon-contradiction law verified!")
```

Run:

```bash
python3 non_contradiction.py
```

This tests both Boolean possibilities and confirms that the expression always returns `False`.

### 3\. Script 2 — Audit contradictory authentication conditions

Imagine a developer writes:

```python
if authenticated and not authenticated:
    print("Access granted")
```

This condition can never be true.

Create:

```bash
nano auth_contradiction.py
```

Paste:

```python
def check_authentication(authenticated):

    condition = authenticated and not authenticated

    if condition:
        print("Access granted")
    else:
        print("Access blocked")

    return condition

for auth in [True, False]:

    print("\nAuthenticated:", auth)

    result = check_authentication(auth)

    print("Condition result:", result)
```

Run:

```bash
python3 auth_contradiction.py
```

Security impact:

A contradictory authentication condition can make legitimate users unable to access an application.

This can cause:

* Authentication failures.

* Broken application functionality.

* Unreachable protected operations.

* Denial of service at the application-logic level.

### 4\. Script 3 — Audit contradictory authorization conditions

Suppose an application requires a user to be an administrator and simultaneously not be an administrator.

```python
is_admin and not is_admin
```

This condition is impossible.

Create:

```bash
nano authorization_contradiction.py
```

Paste:

```python
def authorization_check(is_admin):

    access = is_admin and not is_admin

    if access:
        print("Administrator access granted")
    else:
        print("Administrator access denied")

    return access

for admin in [True, False]:

    print("\nAdministrator:", admin)

    authorization_check(admin)
```

Run:

```bash
python3 authorization_contradiction.py
```

Security interpretation: A contradictory authorization rule can prevent all users from satisfying the condition, including legitimate administrators.

### 5\. Script 4 — Detect contradictory conditions in Python source code

During source-code review, you may encounter contradictory expressions.

You can use Python's AST module to identify simple patterns.

Create:

```bash
nano contradiction_scanner.py
```

Paste:

```python
import ast

source = """
if authenticated and not authenticated:
    print("Access granted")

if is_admin and not is_admin:
    print("Administrator access")

if is_owner and is_admin:
    print("Access permitted")
"""

class ContradictionScanner(ast.NodeVisitor):

    def visit_BoolOp(self, node):

        if isinstance(node.op, ast.And):

            for left in node.values:
                for right in node.values:

                    if left is right:
                        continue

                    if (
                        isinstance(right, ast.UnaryOp)
                        and isinstance(right.op, ast.Not)
                        and ast.dump(left) == ast.dump(right.operand)
                    ):
                        print(
                            "Potential contradiction found:",
                            f"line {node.lineno}"
                        )

        self.generic_visit(node)

tree = ast.parse(source)

ContradictionScanner().visit(tree)
```

Run:

```bash
python3 contradiction_scanner.py
```

It detects simple expressions such as:

```python
authenticated and not authenticated
is_admin and not is_admin
```

Limitation: This is a basic pattern detector, not a complete vulnerability scanner. Contradictions can also occur across multiple conditions, variables and functions.

### 6\. Script 5 — Test authorization conditions automatically

This script checks whether an authorization condition is contradictory.

```python
from itertools import product

def authorization_check(auth, owner, admin):

    return auth and owner and admin and not admin

print("AUTHORIZATION LOGIC TEST")
print("-------------------------")

for auth, owner, admin in product(
    [False, True], repeat=3
):

    result = authorization_check(auth, owner, admin)

    print(
        f"Auth={auth}, Owner={owner}, Admin={admin}"
    )

    print("Access:", "GRANTED" if result else "DENIED")

    assert result is False

print("\nAll eight combinations tested.")
```

Run:

```bash
python3 authorization_test.py
```

The condition requires `admin` and `not admin` simultaneously, so every combination is denied.

### 7\. Security impact during bug bounty

| Security area        | What to investigate                                               |
| -------------------- | ----------------------------------------------------------------- |
| Authentication       | Contradictory login conditions                                    |
| Authorization        | Impossible permission requirements                                |
| IDOR/BOLA            | Contradictory ownership checks                                    |
| Session management   | Conditions that simultaneously require valid and invalid sessions |
| Input validation     | Mutually exclusive validation requirements                        |
| Business logic       | Operations that can never execute                                 |
| Source-code auditing | Unreachable conditional branches                                  |
| Reverse engineering  | Contradictory Boolean expressions in decompiled code              |

### Practical bug-bounty example

Suppose you find:

```python
if authenticated and not authenticated:
    return sensitive_data
```

The condition is always false.

You should investigate:

* Whether this is production code or unused code.

* Whether the branch is reachable through another condition.

* Whether legitimate users are affected.

* Whether the application has another route to the same functionality.

* Whether the issue has a demonstrable security impact.

A contradictory condition alone does not prove an exploitable vulnerability.

### 8\. Compare the three important laws

| Boolean law       | Expression  | Result       |
| ----------------- | ----------- | ------------ |
| Excluded middle   | A or not A  | Always True  |
| Non-contradiction | A and not A | Always False |
| Involution        | not (not A) | A            |

These three laws are important foundations for understanding security-related Boolean expressions.

### 9\. Test your understanding

1. What is the mathematical representation of non-contradiction?

A OR NOT A = True

A AND NOT A = False

NOT NOT A = A

2. What happens if an authorization condition requires is_admin and not is_admin?

Everyone gets access

Only administrators get access

Nobody satisfies the condition

3. What is one possible security impact of contradictory authentication logic?

Legitimate users may be blocked

Passwords become encrypted

The server automatically becomes secure

Check answers

Next topic: Consensus Theorem — a powerful Boolean simplification law that helps eliminate redundant terms in complicated security conditions.
