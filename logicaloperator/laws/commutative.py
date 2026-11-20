### Python scripts for testing the Boolean commutative laws in bug bounty

The commutative law explains that changing the order of two Boolean operands does not change the final logical result.

It is useful when auditing authentication, authorization, API security and complex conditional statements.

### 1\. Understand the commutative laws

There are three important commutative laws.

AND commutative law

A\\land B=B\\land A

OR commutative law

A\\lor B=B\\lor A

XOR commutative law

A\\oplus B=B\\oplus A

Python:

```python
A = True
B = False

print(A and B)  # False
print(B and A)  # False

print(A or B)   # True
print(B or A)   # True

print(A ^ B)    # True
print(B ^ A)    # True
```

### 2\. Script 1: Test all commutative laws

Create:

```bash
nano commutative_test.py
```

Insert:

```python
from itertools import product

print("COMMUTATIVE LAW TEST")
print("====================")

for A, B in product([False, True], repeat=2):

    # AND
    and1 = A and B
    and2 = B and A

    # OR
    or1 = A or B
    or2 = B or A

    # XOR
    xor1 = A ^ B
    xor2 = B ^ A

    print(f"\nA={A}, B={B}")

    print("AND:", and1 == and2)
    print("OR:", or1 == or2)
    print("XOR:", xor1 == xor2)
```

Run:

```bash
python3 commutative_test.py
```

All comparisons should return `True`.

### 3\. Script 2: Apply commutative law to authorization

Imagine an application has this function:

```python
def authorize(authenticated, authorized):
    return authenticated and authorized
```

You can reverse the order:

```python
def authorize_reversed(authenticated, authorized):
    return authorized and authenticated
```

Compare them:

```python
from itertools import product

def original(auth, permission):
    return auth and permission

def reversed_order(auth, permission):
    return permission and auth

for auth, permission in product([False, True], repeat=2):

    first = original(auth, permission)
    second = reversed_order(auth, permission)

    print(
        f"Auth={auth}, Permission={permission} | "
        f"Original={first} | "
        f"Reversed={second} | "
        f"Equivalent={first == second}"
    )
```

Security application: When reviewing source code, you can rearrange independent Boolean requirements to understand the policy more clearly.

For example:

Authenticated\\land Authorized

is logically equivalent to:

Authorized\\land Authenticated

Neither arrangement should grant access when either requirement is false.

### 4\. Script 3: Build a commutative-law source-code scanner

This script detects simple repeated pairs in Python expressions where the operands are reversed.

Create:

```bash
nano commutative_scanner.py
```

Insert:

```python
import ast

source = """
def check_one(auth, admin):
    return auth and admin

def check_two(auth, admin):
    return admin and auth
"""

tree = ast.parse(source)

class CommutativeScanner(ast.NodeVisitor):

    def visit_BoolOp(self, node):

        if len(node.values) == 2:

            left = ast.dump(node.values[0])
            right = ast.dump(node.values[1])

            print(
                "Boolean expression:",
                ast.unparse(node)
            )

            print(
                "Operands:",
                left,
                right
            )

        self.generic_visit(node)

CommutativeScanner().visit(tree)
```

Run:

```bash
python3 commutative_scanner.py
```

This demonstrates how to inspect Boolean expressions. It does not automatically establish that two different functions have equivalent behavior.

### 5\. Important offensive security distinction: Python evaluation order

Here is something advanced researchers must understand.

Although the commutative law is mathematically valid, Python uses short-circuit evaluation.

Consider:

```python
def first():
    print("First executed")
    return False

def second():
    print("Second executed")
    return True
```

Test:

```python
print(first() and second())
```

Only `first()` executes.

Now reverse the order:

```python
print(second() and first())
```

Both functions execute.

The final Boolean result is the same, but the execution behavior differs.

Why this matters in bug bounty:

* Authentication functions may have side effects.

* Validation functions may update application state.

* Database queries may execute in one order but not another.

* Exceptions may occur in one expression but not another.

* Logging and rate-limiting behavior may depend on evaluation order.

Therefore, never reorder real application conditions without examining their side effects.

### 6\. Security testing example

Suppose an application requires both authentication and resource ownership.

```python
def authorize(authenticated, owner):
    return authenticated and owner
```

Test all possible combinations:

```python
from itertools import product

for auth, owner in product([False, True], repeat=2):

    access = authorize(auth, owner)

    if access and not (auth and owner):
        print("SECURITY FAILURE:", auth, owner)
    else:
        print("PASS:", auth, owner, access)
```

Expected security property:

Access\\Rightarrow Authenticated\\land Owner

This is a basic authorization invariant.

### 7\. Test your understanding

1. What does the AND commutative law state?

A AND B = B AND A

A AND B = NOT A

A AND B = False

2. Does reversing Python expressions always preserve execution behavior?

Yes, always

No, because of short-circuiting and side effects

3. Which condition is logically equivalent to authenticated AND authorized?

authorized AND authenticated

authenticated OR authorized

NOT authenticated

Score: 0/3

### 8\. Next law: Associative law

Once you understand commutativity, study associativity:

(A\\land B)\\land C=A\\land(B\\land C)(A\\lor B)\\lor C=A\\lor(B\\lor C)

This is useful for analyzing applications with three or more security requirements.
