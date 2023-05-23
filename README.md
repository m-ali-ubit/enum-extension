# Enum Extension


![Python Version](https://img.shields.io/badge/PythonVersion-%3E%3D3.6-blue)
![Licence](https://img.shields.io/github/license/m-ali-ubit/enum-extension?style=plastic)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/m-ali-ubit/enum-extension/ci.yml?style=plastic)
![Code Formatting](https://img.shields.io/badge/CodeFormatting-Black-blue)
![Code Styling](https://img.shields.io/badge/CodeStyling-Pylint-blue)
![Code Styling](https://img.shields.io/badge/CodeStyling-PEP8-blue)
![Code Styling](https://img.shields.io/badge/CodeStyling-Flake8-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/m-ali-ubit/enum-extension?style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/m-ali-ubit/enum-extension?style=plastic)

enum-extension is a Python library that extends the functionality of the built-in enum module,
offering an array of additional features and utilities to simplify enumeration handling and expand its capabilities.

## Installation
You can install enum-extension using pip:

`pip install enum-extension`

## Description

The enum-extension library enhances the native enum module in Python, providing additional functionality for enumerations.
It introduces the StringEnum class, which inherits from the standard enum.Enum and extends its capabilities.
With enum-extension, you can perform bitwise operations such as OR, AND, and NOT on string type enum values,
combine multiple enums into a single variable, and easily check for membership within combined enums.

## Usage

Here are some examples of how to use StringEnum:

```python
from enum_extensions import StringEnum

# Create an enum by inheriting from StringEnum
class PaymentMethod(StringEnum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    APPLE_PAY = "APPLE_PAY"
    GOOGLE_PAY = "GOOGLE_PAY"
    VENMO = "VENMO"
    PAYPAL = "PAYPAL"

# Use | to combine two enums into one
CARDS = PaymentMethod.MASTERCARD | PaymentMethod.VISA   # PaymentMethod.MASTERCARD|VISA

# Use ~ to get the opposite values of an enum
WALLETS = ~CARDS   # PaymentMethod.APPLE_PAY|GOOGLE_PAY|PAYPAL|VENMO

# Use & operator to check for membership of an enum in the combined enum
PaymentMethod.MASTERCARD & CARDS  # True
PaymentMethod.VISA & CARDS        # True
PaymentMethod.VENMO & CARDS       # False

# Check membership using a string value with & operator (case-insensitive)
CARDS & "Visa"   # True
CARDS & "visa"   # True

# Check string with enum value as a comparison
PaymentMethod.VISA & "visa"    # True
PaymentMethod.PAYPAL & "VISA"  # False

# Use comparison operator to check for equality
PaymentMethod.VISA == "visa"   # True
PaymentMethod.PAYPAL == "VISA"  # False

paypal1 = PaymentMethod.PAYPAL
paypal2 = PaymentMethod.PAYPAL
paypal1 == paypal2    # True

# Create multiple enum classes and merge their values
class CardProvider(StringEnum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"

class WalletProvider(StringEnum):
    VENMO = "VENMO"
    PAYPAL = "PAYPAL"

CARD_PROVIDERS = CardProvider.MASTERCARD | CardProvider.VISA      # CardProvider.MASTERCARD|VISA
WALLET_PROVIDERS = WalletProvider.VENMO | WalletProvider.PAYPAL   # WalletProvider.PAYPAL|VENMO

# Merge two separate StringEnum class values
ALL_METHODS = CARD_PROVIDERS | WALLET_PROVIDERS    # CardProvider_WalletProvider.MASTERCARD|PAYPAL|VENMO|VISA

# Check for membership with the merged enum
WalletProvider.VENMO & WALLET_PROVIDERS    # True
CardProvider.MASTERCARD & ALL_METHODS      # True

# Please note that the merge and combine operations do not modify the original enum definitions but create new enum values.
```

If you have any suggestions or feature requests, please feel free to contribute or reach out.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

Hope you find enum-extension helpful and convenient for working with enumerations in Python.

If you encounter any issues or have any questions, please don't hesitate to open an issue on [GitHub](https://github.com/m-ali-ubit/enum-extension/issues).

This package is owned and maintained by [m-ali-ubit](https://github.com/m-ali-ubit).
