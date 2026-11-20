### Python scripts for testing the Boolean associative laws in bug bounty

The associative laws explain how you can group three or more Boolean conditions without changing their final logical result.

They are useful when auditing complex authentication, authorization, session validation and business-logic conditions.

### 1\. Understand the associative laws

There are two main associative laws.

AND associative law

(A\\land B)\\land C=A\\land(B\\land C)

OR associative law

(A\\lor B)\\lor C=A\\lor(B\\lor C)

Python:

```python
A = True
B = False
C = True

print((A and B) and C)
print(A and (B and C))

print((A or B) or C)
print(A or (B or C))
```

The results are identical for each pair of expressions.

### 2\. Script 1: Test both associative laws

Create:

```bash
nano associative_test.py
```

Insert:

```python
from itertools import product

print("ASSOCIATIVE LAW TEST")
print("====================")

for A, B, C in product([False, True], repeat=3):

    # AND associative law
    and_left = (A and B) and C
    and_right = A and (B and C)

    # OR associative law
    or_left = (A or B) or C
    or_right = A or (B or C)

    print(f"\nA={A}, B={B}, C={C}")

    print("AND equivalent:", and_left == and_right)
    print("OR equivalent:", or_left == or_right)
```

Run:

```bash
python3 associative_test.py
```

There are possible combinations. Both laws should pass all eight.

### 3\. Script 2: Apply associative law to authorization

Imagine an application requires:

* Authentication.

* An active account.

* Permission to access a resource.

Original function:

```python
def authorize(authenticated, active, permitted):
    return (authenticated and active) and permitted
```

Rearranged grouping:

```python
def authorize_rearranged(authenticated, active, permitted):
    return authenticated and (active and permitted)
```

Compare both:

```python
from itertools import product

def original(auth, active, permitted):
    return (auth and active) and permitted

def rearranged(auth, active, permitted):
    return auth and (active and permitted)

for values in product([False, True], repeat=3):

    result1 = original(*values)
    result2 = rearranged(*values)

    print(
        f"Inputs={values} | "
        f"Original={result1} | "
        f"Rearranged={result2} | "
        f"Equivalent={result1 == result2}"
    )
```

Bug bounty application: You can simplify the grouping of complicated security conditions to understand exactly which requirements must be satisfied.

### 4\. Script 3: Test a complex security decision

Let's create a simulated access-control system.

```python
from itertools import product

def authorize(authenticated, active, owner, permitted):

    return (
        (authenticated and active)
        and (owner and permitted)
    )

def authorize_rearranged(authenticated, active, owner, permitted):

    return (
        authenticated
        and (active and (owner and permitted))
    )

print("SECURITY LOGIC ANALYSIS")

for values in product([False, True], repeat=4):

    original = authorize(*values)
    rearranged = authorize_rearranged(*values)

    print(
        f"{values} | "
        f"Original={original} | "
        f"Rearranged={rearranged} | "
        f"Equivalent={original == rearranged}"
    )
```

This tests all 16 combinations.

### 5\. Script 4: Analyze grouped conditions in source code

You can use Python's AST module to inspect Boolean grouping.

Create:

```bash
nano associative_scanner.py
```

Insert:

```python
import ast

source = """
def check_access(auth, active, owner):
    return (auth and active) and owner

def check_admin(auth, admin, active):
    return auth and (admin and active)
"""

tree = ast.parse(source)

class AssociativeScanner(ast.NodeVisitor):

    def visit_BoolOp(self, node):

        if isinstance(node.op, (ast.And, ast.Or)):

            print(
                "Boolean expression:",
                ast.unparse(node)
            )

            print(
                "Operator:",
                type(node.op).__name__
            )

        self.generic_visit(node)

AssociativeScanner().visit(tree)
```

Run:

```bash
python3 associative_scanner.py
```

This identifies Boolean expression structures for manual review. It does not determine whether an application has a vulnerability.

### 6\. Where associative laws help in bug bounty

| Code pattern                            | What to investigate                   |
| --------------------------------------- | ------------------------------------- |
| (auth and active) and owner             | Authentication and resource ownership |
| auth and (active and permission)        | Grouped authorization requirements    |
| (valid and not_expired) and not_revoked | Session validation                    |
| (admin or moderator) or owner           | Alternative access roles              |
| ((verified and active) and permitted)   | Account eligibility                   |

For example:

```python
def access_control(auth, active, owner, permission):
    return ((auth and active) and owner) and permission
```

You can rewrite it as:

```python
def access_control(auth, active, owner, permission):
    return auth and (active and (owner and permission))
```

Both have the same Boolean result for Boolean inputs.

### Important Python security distinction

Associativity preserves the mathematical Boolean result, but changing grouping can change execution behavior when expressions contain function calls, exceptions or side effects.

For example:

```python
def check_a():
    print("A executed")
    return False

def check_b():
    print("B executed")
    return True

def check_c():
    print("C executed")
    return True
```

With short-circuit evaluation:

```python
result = (check_a() and check_b()) and check_c()
```

Only `check_a()` executes.

Do not assume that algebraic equivalence means identical program execution.

### 7\. Test your understanding

1. What does the AND associative law state?

(A AND B) AND C = A AND (B AND C)

A AND B = NOT C

A AND A = A

2. How many Boolean combinations exist for three independent Boolean variables?

4

8

16

3. What is an important limitation when changing grouping in Python?

It always changes the result

It can affect execution behavior when there are side effects or exceptions

It encrypts the conditions

Score: 0/3

### 8\. Next law: Distributive laws

The next laws are particularly useful when breaking down complex authorization conditions:

A\\land(B\\lor C)=(A\\land B)\\lor(A\\land C)A\\lor(B\\land C)=(A\\lor B)\\land(A\\lor C)

They help you identify alternative access paths and understand how multiple security requirements interact.
