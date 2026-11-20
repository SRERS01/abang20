### Python scripts for testing Boolean complement laws in bug bounty

The complement laws are important in security code auditing because they help you identify contradictory conditions, incorrect access decisions and logic that is always true.

### 1\. Understand the complement laws

There are two fundamental complement laws.

AND complement law

A\\land\\neg A=False

OR complement law

A\\lor\\neg A=True

In Python:

```python
A = True

print(A and not A)  # False
print(A or not A)   # True
```

The meaning:

* A condition and its opposite can never both be true.

* A condition or its opposite must always have at least one true value.

### 2\. Script 1: Test both complement laws

Create a file:

```bash
nano complement_test.py
```

Insert:

```python
print("AND COMPLEMENT LAW")
print("==================")

for A in [False, True]:

    result = A and not A

    print(
        f"A={A} | A AND NOT A={result} | "
        f"Expected=False | Valid={result is False}"
    )

print("\nOR COMPLEMENT LAW")
print("=================")

for A in [False, True]:

    result = A or not A

    print(
        f"A={A} | A OR NOT A={result} | "
        f"Expected=True | Valid={result is True}"
    )
```

Run:

```bash
python3 complement_test.py
```

You should get `Valid=True` for all four tests.

### 3\. Script 2: Find contradictory authorization conditions

Imagine you are auditing an application:

```python
def authorize(authenticated):
    return authenticated and not authenticated
```

This condition can never grant access.

Mathematically:

A\\land\\neg A=False

Test it:

```python
from itertools import product

def authorize(authenticated):
    return authenticated and not authenticated

for (auth,) in product([False, True], repeat=1):

    access = authorize(auth)

    print(
        f"Authenticated={auth} | "
        f"Access={'GRANTED' if access else 'DENIED'}"
    )
```

Bug bounty interpretation: If a protected function always denies access because of contradictory logic, investigate whether a legitimate security-sensitive operation is broken. This may be an availability or functionality issue, not an access-control bypass.

### 4\. Script 3: Detect complementary expressions

This script compares a condition with its opposite.

Create:

```bash
nano complement_analyzer.py
```

Insert:

```python
from itertools import product

def original(A, B):
    return A and not A

def simplified(A, B):
    return False

def original_or(A, B):
    return A or not A

def simplified_or(A, B):
    return True

for A, B in product([False, True], repeat=2):

    and_result = original(A, B)
    and_simple = simplified(A, B)

    or_result = original_or(A, B)
    or_simple = simplified_or(A, B)

    print(
        f"A={A}, B={B} | "
        f"AND equivalent={and_result == and_simple} | "
        f"OR equivalent={or_result == or_simple}"
    )
```

Run:

```bash
python3 complement_analyzer.py
```

This verifies that the expressions are logically equivalent for every input combination.

### 5\. Script 4: Find complementary conditions in Python source code

You can also inspect source code for simple contradictory conditions.

```python
import ast

source = """
def check_access(authenticated):
    return authenticated and not authenticated

def check_role(admin):
    return admin or not admin
"""

tree = ast.parse(source)

class ComplementChecker(ast.NodeVisitor):

    def visit_BoolOp(self, node):
        expressions = [ast.dump(x) for x in node.values]

        for value in node.values:
            if isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.Not):
                opposite = ast.dump(value.operand)

                if opposite in expressions:
                    print(
                        "Complementary condition found:",
                        ast.unparse(node),
                        "at line",
                        node.lineno
                    )

        self.generic_visit(node)

ComplementChecker().visit(tree)
```

This detects simple complementary expressions within the same Boolean operation. It is not a complete static-analysis engine.

### 6\. How complement laws help in bug bounty

| Code pattern                        | What to investigate                    |
| ----------------------------------- | -------------------------------------- |
| authenticated and not authenticated | Contradictory authentication condition |
| admin and not admin                 | Impossible administrator condition     |
| valid_session or not valid_session  | Session condition has no effect        |
| owner or not owner                  | Ownership condition has no effect      |
| permission and not permission       | Contradictory permission condition     |

Consider this example:

```python
def check_admin(is_admin):
    return is_admin or not is_admin
```

This always returns `True`.

If this function is used as an authorization decision, it could be a serious security issue because the administrator condition has no effect.

However, always inspect the surrounding authorization checks and verify the actual impact.

### 7\. A more advanced security property test

Let's build a function that checks whether unauthorized users can receive access.

```python
from itertools import product

def authorize(authenticated, is_admin):
    return is_admin or not is_admin

print("COMPLEMENT SECURITY TEST")

for auth, admin in product([False, True], repeat=2):

    access = authorize(auth, admin)

    if access and not (auth and admin):
        print(
            "WARNING: Access granted without "
            "authentication and administrator status",
            auth, admin
        )
    else:
        print("PASS:", auth, admin, access)
```

The test should identify cases where access is granted without the required conditions.

### 8\. Test your knowledge

1. What is A AND NOT A?

True

False

A

2. What is A OR NOT A?

False

True

NOT A

3. What is wrong with \`admin or not admin\` when used as an admin authorization check?

It always returns True

It always returns False

It encrypts the admin value

Score: 0/3

Next law: Double-negation law (involution).

\\neg(\\neg A)=A

This will help you understand nested negations in authentication, access-control and validation code.
