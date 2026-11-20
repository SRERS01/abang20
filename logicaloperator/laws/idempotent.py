### Python scripts for testing the Boolean idempotent laws in bug bounty

The idempotent laws help you identify duplicated conditions in application logic.

They are useful when auditing authentication, authorization, API permissions and business logic.

### 1\. Understand the idempotent laws

There are two main idempotent laws:

AND idempotent law

A\\land A=A

OR idempotent law

A\\lor A=A

In Python:

```python
A = True

print(A and A)  # True
print(A or A)   # True
```

The important idea: repeating the same Boolean condition does not change its logical result.

### 2\. Script 1: Test both idempotent laws

Create a file:

```bash
nano idempotent_test.py
```

Insert:

```python
print("AND IDEMPOTENT LAW")
print("==================")

for A in [False, True]:

    original = A and A
    simplified = A

    print(
        f"A={A} | A AND A={original} | "
        f"Simplified={simplified} | "
        f"Valid={original == simplified}"
    )

print("\nOR IDEMPOTENT LAW")
print("=================")

for A in [False, True]:

    original = A or A
    simplified = A

    print(
        f"A={A} | A OR A={original} | "
        f"Simplified={simplified} | "
        f"Valid={original == simplified}"
    )
```

Run:

```bash
python3 idempotent_test.py
```

Both laws should return `Valid=True` for every input.

### 3\. Script 2: Find duplicated conditions in authorization logic

Imagine an application has this function:

```python
def authorize(is_authenticated, is_admin):
    return is_authenticated and is_admin and is_admin
```

The condition `is_admin` appears twice.

According to the idempotent law:

A\\land B\\land B=A\\land B

Simplified code:

```python
def authorize(is_authenticated, is_admin):
    return is_authenticated and is_admin
```

Let's test both versions:

```python
from itertools import product

def original(auth, admin):
    return auth and admin and admin

def simplified(auth, admin):
    return auth and admin

print("AUTHORIZATION COMPARISON")

for auth, admin in product([False, True], repeat=2):

    result1 = original(auth, admin)
    result2 = simplified(auth, admin)

    print(
        f"Auth={auth}, Admin={admin} | "
        f"Original={result1} | "
        f"Simplified={result2} | "
        f"Equivalent={result1 == result2}"
    )
```

### 4\. Script 3: Detect duplicate Boolean conditions

This is a small static-analysis demonstration.

```python
import ast

source = """
def authorize(authenticated, admin):
    return authenticated and admin and admin

def check_session(valid, valid):
    return valid
"""

tree = ast.parse(source)

class DuplicateChecker(ast.NodeVisitor):

    def visit_BoolOp(self, node):
        seen = set()

        for value in node.values:
            expression = ast.dump(value)

            if expression in seen:
                print(
                    "Duplicate Boolean condition:",
                    ast.unparse(value),
                    "at line",
                    value.lineno
                )

            seen.add(expression)

        self.generic_visit(node)

DuplicateChecker().visit(tree)
```

Run it:

```bash
python3 duplicate_checker.py
```

Expected detection:

```text
Duplicate Boolean condition: admin
```

This is a demonstration, not a complete Python security scanner. A production analyzer would need to account for variable reassignment, function calls, scope and control flow.

### 5\. How to use idempotent laws in bug bounty

| Code pattern                    | What to investigate               |
| ------------------------------- | --------------------------------- |
| admin and admin                 | Duplicate administrator check     |
| authenticated and authenticated | Repeated authentication condition |
| owner or owner                  | Duplicate ownership condition     |
| valid_session and valid_session | Repeated session condition        |
| permission or permission        | Duplicate permission condition    |

Important: A duplicated condition is not automatically a vulnerability. Two identical checks do not provide independent protection, but you must investigate the surrounding code and verify the actual security impact.

### 6\. Advanced security testing: check authorization properties

Consider this simulated application:

```python
from itertools import product

def authorize(authenticated, active, owner, permission):
    return (
        authenticated
        and active
        and owner
        and permission
        and permission
    )

for values in product([False, True], repeat=4):

    auth, active, owner, permission = values

    access = authorize(*values)

    expected = auth and active and owner and permission

    if access != expected:
        print("Potential logic inconsistency:", values)
    else:
        print("PASS:", values, access)
```

This verifies that removing the duplicated permission condition does not change the authorization result.

### 7\. Test your understanding

1. What is A AND A equal to?

True

A

False

2. What is A OR A equal to?

A

False

True

3. What is the security significance of duplicated permission checks?

They automatically make an app secure

They may be redundant and provide no independent protection

They always create an exploit

Score: 0/3

Your next law to study: The complement law. It is particularly useful for investigating contradictory authorization conditions and incorrect denial logic.
