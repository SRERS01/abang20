### All Python comparison (relational) operators

There are 6 fundamental comparison operators in Python.

| No. | Operator | Meaning                  | Example | Result |
| --- | -------- | ------------------------ | ------- | ------ |
| 1   | ==       | Equal to                 | 5 == 5  | True   |
| 2   | !=       | Not equal to             | 5 != 3  | True   |
| 3   | >        | Greater than             | 5 > 3   | True   |
| 4   | <        | Less than                | 3 < 5   | True   |
| 5   | >=       | Greater than or equal to | 5 >= 5  | True   |
| 6   | <=       | Less than or equal to    | 3 <= 5  | True   |

### Python script

```python
a = 10
b = 5

print(a == b)
print(a != b)
print(a > b)
print(a < b)
print(a >= b)
print(a <= b)
```

### Security applications

| Operator | Offensive security application                       |
| -------- | ---------------------------------------------------- |
| ==       | Test authentication and password-comparison logic    |
| !=       | Examine validation and exclusion conditions          |
| >        | Test numerical boundaries and rate limits            |
| <        | Test minimum-value restrictions                      |
| >=       | Examine minimum permission or threshold requirements |
| <=       | Examine maximum-value restrictions                   |

Important: In bug bounty testing, comparison operators help investigate authentication, authorization, input validation, rate limiting, API parameters and business-logic vulnerabilities. Use them only on systems you are authorized to test.
