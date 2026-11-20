### De Morgan's Laws in Python for Offensive Security

De Morgan's laws help you understand how negation (`not`) changes combinations of AND (`and`) and OR (`or`) conditions.

They are particularly useful when auditing authentication, authorization, access-control checks, firewall rules and security validation logic.

There are two main laws.

### 1\. First De Morgan's law

\\neg(A\\land B)=\\neg A\\lor\\neg B

Python:

```python
not (A and B)
```

is logically equivalent to:

```python
(not A) or (not B)
```

Meaning: It is false that both A and B are true if at least one of them is false.

### 2\. Second De Morgan's law

\\neg(A\\lor B)=\\neg A\\land\\neg B

Python:

```python
not (A or B)
```

is logically equivalent to:

```python
(not A) and (not B)
```

Meaning: Neither A nor B is true.

### 3\. Script 1 — Verify both De Morgan's laws

Create your file:

```bash
nano de_morgan_test.py
```

Paste:

```python
from itertools import product

print("FIRST DE MORGAN'S LAW")
print("A       B       Original       Equivalent")

for A, B in product([False, True], repeat=2):

    original = not (A and B)
    equivalent = (not A) or (not B)

    print(A, B, original, equivalent)

    assert original == equivalent

print("\nSECOND DE MORGAN'S LAW")
print("A       B       Original       Equivalent")

for A, B in product([False, True], repeat=2):

    original = not (A or B)
    equivalent = (not A) and (not B)

    print(A, B, original, equivalent)

    assert original == equivalent

print("\nBoth De Morgan's laws verified!")
```

Run:

```bash
python3 de_morgan_test.py
```

This tests every possible combination of two Boolean variables.

### 4\. Script 2 — Audit authentication logic

Imagine an application requires both a valid username and password.

```python
def original_auth(username_valid, password_valid):
    return not (username_valid and password_valid)

def equivalent_auth(username_valid, password_valid):
    return (not username_valid) or (not password_valid)

tests = [
    (True, True),
    (True, False),
    (False, True),
    (False, False)
]

for username, password in tests:

    original = original_auth(username, password)
    equivalent = equivalent_auth(username, password)

    print("Username valid:", username)
    print("Password valid:", password)
    print("Original:", original)
    print("Equivalent:", equivalent)
    print("Same result:", original == equivalent)
    print("-" * 40)
```

Security interpretation:

* Valid username and valid password: rejection condition is false.

* Invalid username or invalid password: rejection condition is true.

* Both invalid: rejection condition is true.

Here, the function returns whether authentication should be rejected, not whether access should be granted.

### 5\. Script 3 — Audit access-control logic

Consider an application that requires authentication and ownership before allowing access.

```python
def original_access(authenticated, is_owner):
    return not (authenticated and is_owner)

def equivalent_access(authenticated, is_owner):
    return (not authenticated) or (not is_owner)

for auth in [False, True]:
    for owner in [False, True]:

        denied_original = original_access(auth, owner)
        denied_equivalent = equivalent_access(auth, owner)

        access_granted = not denied_original

        print("Authenticated:", auth)
        print("Owner:", owner)
        print("Access granted:", access_granted)
        print(
            "Equivalent:",
            denied_original == denied_equivalent
        )
        print("-" * 40)
```

What to investigate during an authorized bug bounty:

* Can an unauthenticated user access a protected resource?

* Can an authenticated user access another user's resource?

* Does the backend verify ownership?

* Does the application mistakenly allow access when one required condition is missing?

This is useful when investigating IDOR/BOLA vulnerabilities.

### 6\. Script 4 — Analyze multiple security conditions

Imagine an application requires:

* A valid session.

* An active account.

* A valid permission.

The access-denial condition is:

```python
not (session_valid and account_active and permission_valid)
```

Using De Morgan's law:

```python
(not session_valid) or \
(not account_active) or \
(not permission_valid)
```

Complete script:

```python
from itertools import product

def original(session, active, permission):
    return not (session and active and permission)

def transformed(session, active, permission):
    return (
        not session
        or not active
        or not permission
    )

for session, active, permission in product(
    [False, True], repeat=3
):

    result1 = original(session, active, permission)
    result2 = transformed(session, active, permission)

    print(
        f"Session={session}, "
        f"Active={active}, "
        f"Permission={permission}"
    )

    print("Original denial:", result1)
    print("Transformed denial:", result2)
    print("Equivalent:", result1 == result2)
    print("-" * 45)

    assert result1 == result2
```

There are eight possible combinations. The script verifies all of them.

### 7\. Script 5 — Build a security-condition analyzer

This script lets you enter three Boolean security conditions and compare the original and transformed expressions.

```python
def security_analyzer(session, account, permission):

    original = not (
        session and account and permission
    )

    transformed = (
        not session
        or not account
        or not permission
    )

    print("\nSECURITY CONDITION ANALYSIS")

    print("Session valid:", session)
    print("Account active:", account)
    print("Permission valid:", permission)

    print("\nOriginal denial:", original)
    print("Transformed denial:", transformed)

    if original == transformed:
        print("\nRESULT: Expressions are equivalent.")
    else:
        print("\nWARNING: Results differ!")

    if original:
        print("Access decision: DENY")
    else:
        print("Access decision: ALLOW")

security_analyzer(
    session=True,
    account=True,
    permission=False
)
```

Try changing the values to test different conditions.

### 8\. How De Morgan's laws help in offensive security

| Security area       | Application                                              |
| ------------------- | -------------------------------------------------------- |
| Authentication      | Understand failed login conditions                       |
| Authorization       | Analyze denied access conditions                         |
| IDOR/BOLA           | Examine ownership restrictions                           |
| Session management  | Identify invalid-session conditions                      |
| Input validation    | Understand rejected input conditions                     |
| Firewall rules      | Analyze combinations of permitted and blocked conditions |
| Source-code review  | Simplify complicated Boolean expressions                 |
| Reverse engineering | Understand negated conditions in application logic       |

### 9\. Important Python distinction

De Morgan's laws describe logical equivalence for Boolean values. However, Python uses short-circuit evaluation.

For example:

```python
not (check_a() and check_b())
```

and:

```python
(not check_a()) or (not check_b())
```

may not behave identically if functions have side effects or raise exceptions. Therefore, do not automatically rewrite production security code based only on Boolean equivalence.

### 10\. Test your knowledge

1. What is equivalent to not (A and B)?

(not A) or (not B)

(not A) and (not B)

2. What is equivalent to not (A or B)?

(not A) or (not B)

(not A) and (not B)

3. If session_valid is False, should a protected application grant access under the three-condition rule?

Yes

No

Check answers

Next topic: Consensus theorem — another useful Boolean simplification law for analyzing complex authorization conditions.
