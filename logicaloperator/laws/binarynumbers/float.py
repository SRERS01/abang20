In Python, you can convert floating-point numbers (numbers with decimal points) into binary using several methods.

Unlike integers, floats have two parts:

* Integer part – digits before the decimal point.

* Fractional part – digits after the decimal point.

### 1\. Convert a float using Python

Python's `bin()` function does not accept floats directly. You can use `float.hex()` to get a hexadecimal representation, or use a custom conversion algorithm for binary.

Example:

```python
number = 12.625

integer_part = int(number)
fractional_part = number - integer_part

print("Integer:", bin(integer_part))
print("Fraction:", fractional_part)
```

### 2\. Convert the complete float to binary

Here is a Python script that converts both parts:

```python
def float_to_binary(number, precision=10):
    integer_part = int(number)
    fractional_part = number - integer_part

    # Convert integer part
    integer_binary = bin(integer_part)[2:]

    # Convert fractional part
    fractional_binary = ""

    for _ in range(precision):
        fractional_part *= 2

        if fractional_part >= 1:
            fractional_binary += "1"
            fractional_part -= 1
        else:
            fractional_binary += "0"

    return integer_binary + "." + fractional_binary

print(float_to_binary(12.625))
```

Output:

```text
1100.1010000000
```

Therefore:

12.625_{10}=1100.101_2

### 3\. Convert using IEEE 754 representation

Computers commonly store Python floats using the IEEE 754 double-precision (64-bit) format.

```python
import struct

number = 12.625

binary = format(
    int.from_bytes(struct.pack(">d", number), "big"),
    "064b"
)

print(binary)
```

Output:

```text
0100000000101001010000000000000000000000000000000000000000000000
```

This representation contains:

| Component           | Bits | Purpose              |
| ------------------- | ---- | -------------------- |
| Sign                | 1    | Positive or negative |
| Exponent            | 11   | Represents the scale |
| Fraction (mantissa) | 52   | Represents precision |

### 4\. Important security applications

Understanding floating-point binary representation helps when investigating:

* Numeric input validation.

* Floating-point precision errors.

* Authentication and comparison logic.

* Buffer and data-format analysis.

* Serialization and deserialization vulnerabilities.

* Numeric edge cases in APIs.

Important: My first conversion algorithm assumes a non-negative number. Negative numbers need a sign-handling adjustment, and some decimal fractions cannot be represented exactly in binary.

Would you like to learn how IEEE 754 converts a float into its exact 64-bit binary representation, step by step?
