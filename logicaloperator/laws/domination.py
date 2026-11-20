### Python scripts for testing the Boolean domination law in bug bounty

The domination law states that one Boolean value can completely determine the result of an expression, regardless of the other value.

There are two domination laws.

### 1\. Understand the domination laws

AND domination

A\\land False=False

OR domination

A\\lor True=True

Python:

```python
A = True

print(A and False)  # False
print(A or True)    # True
```

### 2\. Script 1: Automatically test domination laws

Create a file:

```bash
nano domination_test.py
```

Insert:

```python
from itertools import product

print("AND DOMINATION LAW")
print("===================")

for A in [False, True]:

    result = A and False

    print(
        f"A={A} | A AND False={result} | "
        f"Expected=False | Valid={result is False}"
    )

print("\nOR DOMINATION LAW")
print("=================")

for A in [False, True]:

    result = A or True

    print(
        f"A={A} | A OR True={result} | "
        f"Expected=True | Valid={result is True}"
    )
```

Run:

```bash
python3 domination_test.py
```

You should see that both laws hold for `True` and `False`.

### 3\. Script 2: Test domination in authorization logic

Imagine a simulated application:

```python
def authorize(authenticated, authorized):
    return authenticated and authorized and False
```

Test every combination:

```python
from itertools import product

def authorize(authenticated, authorized):
    return authenticated and authorized and False

for auth, permission in product([False, True], repeat=2):

    result = authorize(auth, permission)

    print(
        f"Authenticated={auth}, "
        f"Authorized={permission}, "
        f"Access={result}"
    )
```

Because of domination:

A\\land B\\land False=False

Access is always denied.

Bug bounty interpretation: If a security decision is permanently false, investigate whether the application has a broken feature, inaccessible functionality or an incorrectly implemented authorization condition. This is not automatically an exploitable vulnerability.

### 4\. Script 3: Detect domination patterns

This script checks expressions against their simplified forms.

```python
from itertools import product

def original_and(A, B):
    return A and B and False

def simplified_and(A, B):
    return False

def original_or(A, B):
    return A or B or True

def simplified_or(A, B):
    return True

print("DOMINATION ANALYSIS")

for A, B in product([False, True], repeat=2):

    and_match = original_and(A, B) == simplified_and(A, B)
    or_match = original_or(A, B) == simplified_or(A, B)

    print(
        f"A={A}, B={B} | "
        f"AND equivalent={and_match} | "
        f"OR equivalent={or_match}"
    )
```

### 5\. Security applications

| Domination pattern      | What to investigate                         |
| ----------------------- | ------------------------------------------- |
| permission and False    | Permanently denied access                   |
| authenticated and False | Login-dependent operation always fails      |
| role or True            | Role condition has no effect                |
| is_admin or True        | Administrator requirement is ineffective    |
| valid_session or True   | Session-validity requirement is ineffective |

For example:

```python
def check_access(is_admin):
    return is_admin or True
```

This always returns `True`, even when `is_admin` is `False`.

That could represent a serious authorization flaw if this function controls access to a protected resource.

### 6\. Your domination-law practice test

1. What does A AND False always return?

A

True

False

2. What does A OR True always return?

True

False

A

3. Which pattern could indicate an ineffective administrator check?

is_admin and True

is_admin or True

is_admin and False

Score: 0/3

Next recommended law: The idempotent law. It helps you identify duplicated Boolean conditions in authentication and authorization code.
