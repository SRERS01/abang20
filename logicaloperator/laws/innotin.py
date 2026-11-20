### All Python Membership Operators

Python has exactly 2 built-in membership operators:

| No. | Operator | Meaning                                                  | Example              |
| --- | -------- | -------------------------------------------------------- | -------------------- |
| 1   | in       | Checks whether an element exists in a collection         | "admin" in users     |
| 2   | not in   | Checks whether an element does not exist in a collection | "guest" not in users |

### 1\. `in` operator

Purpose: Determines whether a value exists in a collection.

```python
users = ["admin", "guest", "researcher"]

print("admin" in users)
```

Output: `True`

Offensive security applications:

* Username allowlist testing.

* Input validation analysis.

* API parameter testing.

* Searching for sensitive strings.

* Checking permitted file extensions.

Security impact: Weak membership validation can allow unauthorized input or unintended access.

### 2\. `not in` operator

Purpose: Determines whether a value does not exist in a collection.

```python
blocked_users = ["attacker", "unauthorized", "guest"]

print("admin" not in blocked_users)
```

Output: `True`

Offensive security applications:

* Blocklist testing.

* File-upload restriction analysis.

* Input-filter testing.

* Restricted username analysis.

* API filtering analysis.

Security impact: Incomplete blocklists can allow prohibited inputs or unexpected file types.

### 3\. Complete membership verification script

```python

# PYTHON MEMBERSHIP OPERATOR TESTER

users = ["admin", "guest", "researcher"]

test_values = [
    "admin",
    "guest",
    "attacker",
    "researcher"
]

print("MEMBERSHIP SECURITY TEST")
print("=" * 40)

for value in test_values:

    if value in users:
        print(value, "=> FOUND")

    if value not in users:
        print(value, "=> NOT FOUND")
```

### 4\. Collections that support membership testing

| Collection | Example                             |
| ---------- | ----------------------------------- |
| List       | "admin" in ["admin", "user"]        |
| Tuple      | "admin" in ("admin", "user")        |
| Set        | "admin" in {"admin", "user"}        |
| String     | "pass" in "password"                |
| Dictionary | "username" in {"username": "admin"} |
| Range      | 5 in range(1, 10)                   |

Important: For dictionaries, membership checks keys, not values.

### 5\. Security research applications

| Research area       | Membership usage                        |
| ------------------- | --------------------------------------- |
| Web security        | Inspect input filters                   |
| API security        | Check permitted parameters              |
| Android security    | Search configuration values             |
| File security       | Examine extensions                      |
| Authentication      | Analyze username restrictions           |
| Reverse engineering | Search strings in extracted data        |
| Network security    | Check known indicators in captured data |

Final point: There are only two Python membership operators: `in` and `not in`. Different collections change what is being checked, but they do not create additional membership operators.
