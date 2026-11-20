### Python scripts for testing the Boolean double-negation law in bug bounty

The double-negation law, also called the involution law, is useful when auditing complicated conditions involving `not`, especially authentication, authorization, input validation and session management.

### 1\. Understand the double-negation law

The mathematical formula is:

\\neg(\\neg A)=A

Meaning: negating a Boolean value twice returns its original value.

Python:

```python
A = True

print(not not A)  # True

A = False

print(not not A)  # False
```

For example:

```python
authenticated = True

print(not not authenticated)
```

Output:

```text
True
```

### 2\. Script 1: Test the double-negation law

Create a file:

```bash
nano double_negation_test.py
```

Insert:

```python
print("DOUBLE NEGATION LAW")
print("===================")

for A in [False, True]:

    original = not not A
    simplified = A

    print(
        f"A={A} | NOT NOT A={original} | "
        f"Original A={simplified} | "
        f"Valid={original == simplified}"
    )
```

Run:

```bash
python3 double_negation_test.py
```

Both Boolean values should pass.

### 3\. Script 2: Test double negation in authorization logic

Imagine an application contains:

```python
def authorize(authenticated, is_admin):
    return not not authenticated and not not is_admin
```

According to the double-negation law, this is equivalent to:

```python
def authorize(authenticated, is_admin):
    return authenticated and is_admin
```

Let's compare both versions:

```python
from itertools import product

def original(authenticated, admin):
    return not not authenticated and not not admin

def simplified(authenticated, admin):
    return authenticated and admin

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

This confirms that the two expressions give the same results for Boolean inputs.

### 4\. Script 3: Find double negation in Python source code

You can also inspect Python source code for nested `not` expressions.

Create:

```bash
nano double_negation_scanner.py
```

Insert:

```python
import ast

source = """
def check_access(authenticated):
    return not not authenticated

def check_admin(admin):
    return not not admin

def check_session(valid):
    return not valid
"""

tree = ast.parse(source)

class DoubleNegationScanner(ast.NodeVisitor):

    def visit_UnaryOp(self, node):

        if (
            isinstance(node.op, ast.Not)
            and isinstance(node.operand, ast.UnaryOp)
            and isinstance(node.operand.op, ast.Not)
        ):
            print(
                "Double negation found:",
                ast.unparse(node),
                "Line:",
                node.lineno
            )

        self.generic_visit(node)

DoubleNegationScanner().visit(tree)
```

Run:

```bash
python3 double_negation_scanner.py
```

Expected findings:

```text
Double negation found: not not authenticated Line: 3
Double negation found: not not admin Line: 6
```

This is a simple source-code pattern detector, not a vulnerability scanner.

### 5\. Script 4: Test security properties

Suppose your security requirement is:

> Access must only be granted to authenticated administrators.

Use:

```python
from itertools import product

def authorize(authenticated, admin):
    return not not authenticated and not not admin

print("SECURITY PROPERTY TEST")

for auth, admin in product([False, True], repeat=2):

    access = authorize(auth, admin)

    expected = auth and admin

    if access != expected:
        print("FAIL:", auth, admin)
    else:
        print("PASS:", auth, admin, access)
```

The script verifies that double negation does not change the intended access-control decision.

### 6\. Where to investigate double negation in bug bounty

| Code pattern          | What to investigate             |
| --------------------- | ------------------------------- |
| not not authenticated | Authentication-state conversion |
| not not is_admin      | Administrator-state conversion  |
| not not valid_session | Session validation              |
| not not is_owner      | Resource ownership checks       |
| not not permitted     | Permission-state conversion     |

Important: Double negation is not automatically a vulnerability. In Python, `not not value` converts a value to a Boolean. For non-Boolean objects, it can change the type and discard information.

For example:

```python
value = "admin"

print(value)       # admin
print(not not value)  # True
```

The original string and its Boolean representation are not equivalent as data, even though double negation preserves truthiness.

### 7\. Your practical test

1. What is NOT NOT True?

False

True

2. What is NOT NOT False?

True

False

3. What does \`not not value\` do in Python?

Converts truthiness into a Boolean

Encrypts the value

Deletes the value

Score: 0/3

### 8\. Your next Boolean law

The next one is the commutative law:

A\\land B=B\\land AA\\lor B=B\\lor A

It helps you understand how changing the order of Boolean conditions affects program logic—and why Python's short-circuit evaluation still matters when auditing real applications.
