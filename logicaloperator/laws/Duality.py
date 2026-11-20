### Principle of Duality in Python for Offensive Security

The Principle of Duality is a Boolean algebra principle that allows you to create a logically valid dual expression by exchanging:

* AND (`and`) with OR (`or`).

* True (`True`) with False (`False`).

Variables and their complements remain unchanged.

It is useful in offensive security when analyzing access-control conditions, authentication logic, firewall rules, source code and security policies.

### 1\. Mathematical explanation

Consider this Boolean identity:

A \\land True = A

Its dual is:

A \\lor False = A

Notice the changes:

| Original | Dual    |
| -------- | ------- |
| AND (∧)  | OR (∨)  |
| OR (∨)   | AND (∧) |
| True     | False   |
| False    | True    |

The variables remain unchanged.

### More examples

| Original law | Dual law |
| ------------ | -------- |
|              |          |
|              |          |
|              |          |
|              |          |
|              |          |

Important: Duality does not mean the original expression and its dual always have the same result. It means that a valid Boolean identity produces another valid identity when the duality substitutions are applied.

### 2\. Script 1 — Demonstrate the principle of duality

Create:

```bash
nano duality_test.py
```

Paste:

```python
values = [True, False]

print("PRINCIPLE OF DUALITY")
print("--------------------")

for A in values:

    # Original identity
    original_left = A and True
    original_right = A

    # Dual identity
    dual_left = A or False
    dual_right = A

    print("\nA:", A)

    print("Original left:", original_left)
    print("Original right:", original_right)

    print("Dual left:", dual_left)
    print("Dual right:", dual_right)

    assert original_left == original_right
    assert dual_left == dual_right

print("\nDuality identities verified!")
```

Run:

```bash
python3 duality_test.py
```

This verifies the identity law and its dual for both Boolean values.

### 3\. Script 2 — Test duality across multiple Boolean laws

This script verifies several Boolean identities alongside their duals.

Create:

```bash
nano duality_laws.py
```

Paste:

```python
from itertools import product

print("TESTING BOOLEAN DUALITY")

for A, B, C in product([False, True], repeat=3):

    # Original distributive identity
    original_left = A and (B or C)
    original_right = (A and B) or (A and C)

    # Dual distributive identity
    dual_left = A or (B and C)
    dual_right = (A or B) and (A or C)

    assert original_left == original_right
    assert dual_left == dual_right

    # Original absorption identity
    original_absorption = A or (A and B)

    # Dual absorption identity
    dual_absorption = A and (A or B)

    assert original_absorption == A
    assert dual_absorption == A

print("Distributive identities: PASSED")
print("Absorption identities: PASSED")
print("Duality verification: PASSED")
```

Run:

```bash
python3 duality_laws.py
```

There are eight combinations of A, B and C. The script checks both distributive identities and both absorption identities.

### 4\. Script 3 — Apply duality to authorization logic

Imagine a web application has this authorization rule:

```python
authenticated and (is_owner or is_admin)
```

Meaning:

* The user must be authenticated.

* The user must own the resource or be an administrator.

The dual expression is:

```python
authenticated or (is_owner and is_admin)
```

These are not equivalent authorization policies. The dual is a different condition.

Create:

```bash
nano authorization_duality.py
```

Paste:

```python
def original_policy(auth, owner, admin):

    return auth and (owner or admin)

def dual_policy(auth, owner, admin):

    return auth or (owner and admin)

tests = [
    (True, True, False),
    (True, False, True),
    (False, True, True),
    (False, False, False)
]

for auth, owner, admin in tests:

    original = original_policy(auth, owner, admin)
    dual = dual_policy(auth, owner, admin)

    print("\nAuthentication:", auth)
    print("Ownership:", owner)
    print("Administrator:", admin)

    print("Original policy:", original)
    print("Dual policy:", dual)

    if original != dual:
        print("WARNING: The policies produce different results.")
```

Run:

```bash
python3 authorization_duality.py
```

Security impact: This demonstrates why you should not casually replace AND with OR in security conditions.

For example, the original policy requires authentication. The dual policy can grant access to someone who is not authenticated if they satisfy the other conditions.

The dual expression is useful for studying the logical structure, but it should not automatically replace the original authorization policy.

### 5\. Script 4 — Analyze security policy duals

Here is a more practical example.

Suppose an application requires all three conditions:

* Valid session.

* Active account.

* Valid permission.

Original security policy:

```python
session and account and permission
```

Its dual is:

```python
session or account or permission
```

Create:

```bash
nano security_duality.py
```

Paste:

```python
from itertools import product

def original_policy(session, account, permission):
    return session and account and permission

def dual_policy(session, account, permission):
    return session or account or permission

print("SECURITY POLICY DUALITY")
print("-----------------------")

for session, account, permission in product(
    [False, True], repeat=3
):

    original = original_policy(
        session, account, permission
    )

    dual = dual_policy(
        session, account, permission
    )

    print(
        f"Session={session}, "
        f"Account={account}, "
        f"Permission={permission}"
    )

    print("Original:", original)
    print("Dual:", dual)

    if original != dual:
        print("Different security decision")

    print("-" * 40)
```

Run:

```bash
python3 security_duality.py
```

What you learn: A policy requiring every condition is very different from one requiring only one condition.

### 6\. Script 5 — Build a simple dual-expression converter

This script demonstrates how to convert a restricted Boolean expression into its dual using Python's AST module.

It supports simple expressions involving `and`, `or`, `True`, `False` and variables.

Create:

```bash
nano dual_converter.py
```

Paste:

```python
import ast

def make_dual(node):

    if isinstance(node, ast.BoolOp):

        if isinstance(node.op, ast.And):
            new_op = ast.Or()

        elif isinstance(node.op, ast.Or):
            new_op = ast.And()

        else:
            raise ValueError("Unsupported Boolean operator")

        return ast.BoolOp(
            op=new_op,
            values=[make_dual(x) for x in node.values]
        )

    elif isinstance(node, ast.Constant):

        if node.value is True:
            return ast.Constant(value=False)

        if node.value is False:
            return ast.Constant(value=True)

        return node

    elif isinstance(node, ast.Name):
        return node

    elif isinstance(node, ast.UnaryOp):
        return ast.UnaryOp(
            op=node.op,
            operand=make_dual(node.operand)
        )

    else:
        raise ValueError("Unsupported expression")

expression = "A and (B or True)"

tree = ast.parse(expression, mode="eval")

dual_tree = make_dual(tree.body)

result = ast.unparse(dual_tree)

print("Original:", expression)
print("Dual:", result)
```

Run:

```bash
python3 dual_converter.py
```

Expected output:

```text
Original: A and (B or True)
Dual: A or (B and False)
```

This is an educational converter for a limited expression grammar, not a general-purpose Boolean parser.

### 7\. Security impact in offensive security

| Security area        | How duality helps                                           |
| -------------------- | ----------------------------------------------------------- |
| Authentication       | Understand AND-based versus OR-based login requirements     |
| Authorization        | Examine alternative permission policies                     |
| IDOR/BOLA            | Analyze ownership and administrator conditions              |
| Firewall rules       | Understand allow/deny logic                                 |
| Input validation     | Compare conditions requiring all checks versus any check    |
| Reverse engineering  | Interpret Boolean expressions in decompiled code            |
| Source-code auditing | Recognize how changing operators changes security decisions |
| Static analysis      | Generate related expressions for testing                    |

### Important bug-bounty lesson

When reviewing an application, pay special attention to this difference:

```python
authenticated and is_admin
```

versus:

```python
authenticated or is_admin
```

The first requires both conditions. The second requires only one.

A misplaced `or` instead of `and` can create a serious authorization weakness. Verify the actual server-side behaviour using accounts and resources you are authorized to test.

### 8\. Quick revision

Remember the two substitutions:

AND OR

TRUE FALSE

Variables and their negations remain unchanged.

### 9\. Test your understanding

1. What is the dual of A AND True = A?

A OR False = A

A AND False = A

A OR True = A

2. What happens to AND when constructing a dual expression?

It becomes NOT

It becomes OR

It remains AND

3. Are an authorization expression and its dual necessarily equivalent?

Yes, always

No, they can produce different results

Check answers

Next topic: Consensus Theorem — useful for simplifying complex Boolean expressions and identifying redundant logical conditions during security code audits.
