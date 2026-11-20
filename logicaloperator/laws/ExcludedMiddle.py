### Law of Excluded Middle in Python for Offensive Security

The Law of Excluded Middle is a fundamental law of classical Boolean logic. It states that a proposition must be either true or false. There is no third possibility in classical two-valued logic.

It is useful when examining authentication, authorization, input validation, access-control conditions and security decision-making.

### 1\. Mathematical representation

A \\lor \\neg A = True

Python:

```python
A or (not A)
```

This expression always evaluates to `True` for a Boolean value.

Example:

```python
authenticated = True

print(authenticated or not authenticated)
# True
```

Another example:

```python
authenticated = False

print(authenticated or not authenticated)
# True
```

Regardless of whether `authenticated` is true or false, the expression is true.

### 2\. Script 1 — Verify the excluded middle law

Create:

```bash
nano excluded_middle.py
```

Paste:

```python
values = [True, False]

print("LAW OF EXCLUDED MIDDLE")
print("----------------------")

for A in values:

    result = A or (not A)

    print("A:", A)
    print("NOT A:", not A)
    print("A OR NOT A:", result)

    assert result is True

print("\nExcluded middle law verified!")
```

Run:

```bash
python3 excluded_middle.py
```

What this script demonstrates:

* Tests both possible Boolean values.

* Applies the excluded middle law.

* Confirms that the result is always true.

### 3\. Script 2 — Analyze authentication conditions

Consider:

```python
authenticated or not authenticated
```

This is always true, meaning it cannot serve as an authentication restriction.

Create:

```bash
nano auth_logic_audit.py
```

Paste:

```python
def insecure_condition(authenticated):

    return authenticated or not authenticated

for auth in [True, False]:

    result = insecure_condition(auth)

    print("Authenticated:", auth)
    print("Condition result:", result)

    if result:
        print("Condition allows execution")
    else:
        print("Condition blocks execution")

    print("-" * 35)
```

Run:

```bash
python3 auth_logic_audit.py
```

Security impact: If a developer mistakenly uses this expression as an access-control condition, it will always pass.

For example:

```python
if authenticated or not authenticated:
    return sensitive_data
```

The condition does not actually verify authentication.

The correct example is:

```python
if authenticated:
    return sensitive_data
```

The application must also validate authorization where required.

### 4\. Script 3 — Audit permission conditions

Suppose an application has an administrator permission variable.

Incorrect condition:

```python
is_admin or not is_admin
```

This always evaluates to `True`.

Create:

```bash
nano permission_audit.py
```

Paste:

```python
def check_permission(is_admin):

    return is_admin or not is_admin

for admin in [True, False]:

    access = check_permission(admin)

    print("Administrator:", admin)
    print("Access result:", access)

    if access:
        print("Access granted")
    else:
        print("Access denied")

    print("-" * 35)
```

Run:

```bash
python3 permission_audit.py
```

Security interpretation: Even a non-administrator passes this condition. This demonstrates how a logically meaningless permission check can create an authorization vulnerability.

### 5\. Script 4 — Compare correct and incorrect access control

This script compares an insecure condition with a proper administrator check.

```python
def insecure_access(is_admin):

    return is_admin or not is_admin

def secure_access(is_admin):

    return is_admin

for admin in [True, False]:

    insecure = insecure_access(admin)
    secure = secure_access(admin)

    print("Administrator:", admin)
    print("Insecure access:", insecure)
    print("Correct access:", secure)

    if insecure and not secure:
        print("WARNING: Unauthorized access would be allowed")

    print("-" * 40)
```

Run:

```bash
python3 access_comparison.py
```

Expected security observation:

| Administrator | Insecure condition | Correct condition |
| ------------- | ------------------ | ----------------- |
| True          | Granted            | Granted           |
| False         | Granted            | Denied            |

Security lesson

A condition containing `A or not A` cannot enforce a restriction in classical Boolean logic.

### 6\. Script 5 — Automatically detect excluded-middle patterns

You can use Python's Abstract Syntax Tree (AST) module to inspect source code for expressions containing a variable OR its negation.

Create:

```bash
nano excluded_middle_scanner.py
```

Paste:

```python
import ast

source = """
if is_admin or not is_admin:
    print("Access granted")

if authenticated or not authenticated:
    print("Continue")

if is_owner or is_admin:
    print("Allowed")
"""

class ExcludedMiddleScanner(ast.NodeVisitor):

    def visit_BoolOp(self, node):

        if isinstance(node.op, ast.Or):

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
                            "Potential excluded-middle pattern:",
                            f"line {node.lineno}"
                        )

        self.generic_visit(node)

tree = ast.parse(source)

ExcludedMiddleScanner().visit(tree)
```

Run:

```bash
python3 excluded_middle_scanner.py
```

This detects simple patterns such as:

```python
is_admin or not is_admin
```

It is a basic pattern detector, not a complete security scanner. More complex expressions, aliases and dynamically constructed conditions require deeper analysis.

### 7\. Security applications

| Area                 | Security impact                                                |
| -------------------- | -------------------------------------------------------------- |
| Authentication       | Detect conditions that always pass                             |
| Authorization        | Identify ineffective permission checks                         |
| IDOR/BOLA            | Review whether ownership checks actually restrict access       |
| Session management   | Find meaningless session-validity conditions                   |
| Input validation     | Identify validation expressions that accept every Boolean case |
| Source-code auditing | Recognize tautologies                                          |
| Reverse engineering  | Simplify conditions in decompiled code                         |
| Static analysis      | Detect suspicious logical expressions                          |

### 8\. Important distinction: Excluded middle vs contradiction

These two expressions have opposite results:

| Law             | Expression  | Result       |
| --------------- | ----------- | ------------ |
| Excluded middle | A or not A  | Always True  |
| Contradiction   | A and not A | Always False |

The contradiction law is also called the law of non-contradiction in classical logic.

### 9\. Test your understanding

1. What is the excluded middle expression?

A and not A

A or not A

A and A

2. What does A or not A always return for a Boolean A?

True

False

None

3. What is the security problem with using is_admin or not is_admin as an access check?

It blocks everyone

It allows everyone through the condition

It checks the user's password

Check answers

Next topic: Law of Non-Contradiction — understanding why `A and not A` is always false and how contradictory security conditions can cause unreachable code or broken access-control logic.
