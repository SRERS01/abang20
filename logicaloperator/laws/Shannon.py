### Shannon Expansion Theorem in Boolean Algebra

The Shannon Expansion Theorem is a Boolean algebra technique used to break a complex logical expression into two simpler expressions.

It divides a Boolean function into two possible cases:

* When a variable is `True`.

* When that variable is `False`.

In offensive security, this is useful for analysing authentication conditions, authorization logic, session checks, API permissions, and complex security decisions.

### 1\. Mathematical formula

For a Boolean function and variable :

\\boxed{F=A\\cdot F_{A=1}+\\neg A\\cdot F_{A=0}}

Where:

* = original Boolean expression.

* = variable being examined.

* = expression when A is True.

* = expression when A is False.

* = AND.

* = OR.

* = NOT.

This is also called Shannon decomposition.

### 2\. Simple example

Consider:

F=(A\\land B)\\lor C

We want to expand the expression around variable A.

Case 1: A = True

Substitute True for A:

F_{A=1}=(1\\land B)\\lor C

Therefore:

F_{A=1}=B\\lor C

Case 2: A = False

Substitute False for A:

F_{A=0}=(0\\land B)\\lor C

Therefore:

F_{A=0}=C

Now apply Shannon expansion:

F=(A\\land(B\\lor C))\\lor(\\neg A\\land C)

The expanded expression is logically equivalent to the original.

### 3\. Python implementation

Create a file:

```bash
nano shannon_expansion.py
```

Insert:

```python
from itertools import product

# Original Boolean function
def original(A, B, C):
    return (A and B) or C

# Shannon expansion around A
def shannon(A, B, C):

    # Function when A = True
    f_true = B or C

    # Function when A = False
    f_false = C

    return (A and f_true) or ((not A) and f_false)

print("A | B | C | Original | Shannon")

for A, B, C in product([False, True], repeat=3):

    result1 = original(A, B, C)
    result2 = shannon(A, B, C)

    print(A, B, C, result1, result2)

    assert result1 == result2

print("\nBoth expressions are equivalent.")
```

Run:

```bash
python3 shannon_expansion.py
```

Expected result

```text
Both expressions are equivalent.
```

The script checks all eight possible combinations of A, B and C.

### 4\. Application in offensive security

Imagine an application uses this authorization condition:

```python
access = authenticated and (is_admin or is_owner)
```

Let:

* A = authenticated

* B = is_admin

* C = is_owner

The original expression is:

F=A\\land(B\\lor C)

Expand around authentication (A).

Case 1: Authenticated = True

F_{A=1}=B\\lor C

The user gets access if they are an administrator or the resource owner.

Case 2: Authenticated = False

F_{A=0}=0

The user receives no access, regardless of administrator or ownership values.

The Shannon expansion becomes:

F=(A\\land(B\\lor C))\\lor(\\neg A\\land0)

Simplifying:

F=A\\land(B\\lor C)

This demonstrates how authentication controls the entire authorization decision.

### 5\. Practical security audit script

Create:

```bash
nano security_shannon_audit.py
```

Insert:

```python
from itertools import product

def original_access(auth, admin, owner):
    return auth and (admin or owner)

def shannon_access(auth, admin, owner):

    # Case 1: auth = True
    f_true = admin or owner

    # Case 2: auth = False
    f_false = False

    return (
        (auth and f_true)
        or
        ((not auth) and f_false)
    )

print("AUTH | ADMIN | OWNER | ACCESS")

for auth, admin, owner in product(
    [False, True], repeat=3
):

    result = original_access(auth, admin, owner)
    expanded = shannon_access(auth, admin, owner)

    print(auth, admin, owner, result)

    assert result == expanded

print("\n[+] Shannon equivalence verified")
```

Run:

```bash
python3 security_shannon_audit.py
```

This tests the authorization expression across all eight possible states.

### 6\. Where Shannon expansion helps in bug bounty

| Security area      | Practical application                              |
| ------------------ | -------------------------------------------------- |
| Authentication     | Separate authenticated and unauthenticated paths   |
| Authorization      | Analyse admin and ordinary-user permissions        |
| IDOR/BOLA          | Examine ownership and access conditions            |
| API security       | Split request-permission decisions into cases      |
| Session security   | Analyse valid and invalid session branches         |
| Firewall logic     | Examine allowed and denied traffic conditions      |
| Business logic     | Break complex conditional rules into smaller cases |
| Static analysis    | Simplify and inspect Boolean expressions           |
| Symbolic execution | Explore alternative execution paths                |
| SAT solving        | Convert expressions into manageable logical cases  |

### 7\. Important advanced concept: Multiple Shannon expansions

You can expand a Boolean function around different variables.

For example:

F=A\\land(B\\lor C)

You can expand around A, B or C.

This is useful because the variable you choose determines how you divide the security logic.

A good security reviewer might first examine:

* Authentication.

* Then administrator privileges.

* Then resource ownership.

* Then any additional permission checks.

Important: Shannon expansion is a reasoning and decomposition technique, not an automatic vulnerability detector. It helps reveal how each condition affects a decision. You must still compare the implemented behaviour against the application's intended security policy.

### 8\. Test your understanding

Shannon Expansion Quiz

1. What does Shannon expansion do?

Breaks a Boolean expression into two cases

Deletes all variables

Encrypts Boolean values

2. If A = False, what is the value of A AND B?

True

False

Depends on B

3. In bug bounty, why expand an authorization expression around authentication?

To analyse authenticated and unauthenticated paths

To increase network speed

To bypass every login

0/3 answered

Reset

Next topic: Boolean Consensus Theorem, Shannon expansion with decision trees, or Binary Decision Diagrams (BDDs).
