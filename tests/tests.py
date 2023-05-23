import unittest

from enum_extensions.enum import StringEnum
from enum_extensions.exceptions import InvalidTypeException, DuplicateValueException
from tests.factories import (
    PaymentMethod,
    CardProvider,
    CARDS,
    WALLETS,
    ALL_METHODS,
    CARD_PROVIDERS,
    WalletProvider,
    WALLET_PROVIDERS,
)


class TestStringEnum(unittest.TestCase):
    def test_repr(self):
        foo = StringEnum("foo")
        self.assertEqual(repr(foo), "<StringEnum.foo>")

    def test_eq(self):
        foo1 = StringEnum("foo")
        foo2 = StringEnum("foo")
        self.assertEqual(foo1, foo2)
        bar = StringEnum("bar")
        self.assertNotEqual(foo1, bar)

    def test_hash(self):
        foo = StringEnum("foo")
        self.assertEqual(hash(foo), hash("foo"))

    def test_or(self):
        foo = StringEnum("foo")
        bar = StringEnum("bar")
        self.assertEqual(foo | bar, StringEnum("bar|foo"))

    def test_and(self):
        foo = StringEnum("foo")
        bar = StringEnum("bar")
        self.assertFalse(foo & bar)
        foo2 = StringEnum("foo")
        self.assertTrue(foo & foo2)

    def test_invert(self):
        my_enum = StringEnum("foo")
        self.assertNotEqual(my_enum, ~my_enum)

    def test_missing(self):
        self.assertEqual(StringEnum._missing_("foo"), StringEnum("foo"))
        self.assertEqual(StringEnum._missing_("bar"), StringEnum("bar"))
        self.assertEqual(StringEnum._missing_("baz"), StringEnum("baz"))


class TestPaymentMethods(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(TypeError):
            PaymentMethod()

    def test_and(self):
        self.assertTrue(PaymentMethod.MASTERCARD & CARDS)
        self.assertTrue(PaymentMethod.VISA & CARDS)

        self.assertFalse(PaymentMethod.VENMO & CARDS)
        self.assertFalse(PaymentMethod.PAYPAL & CARDS)

        self.assertTrue(PaymentMethod.APPLE_PAY & WALLETS)
        self.assertTrue(PaymentMethod.GOOGLE_PAY & WALLETS)
        self.assertTrue(PaymentMethod.VENMO & WALLETS)
        self.assertTrue(PaymentMethod.PAYPAL & WALLETS)

        self.assertFalse(PaymentMethod.VISA & WALLETS)
        self.assertFalse(PaymentMethod.MASTERCARD & WALLETS)

    def test_or_none(self):
        with self.assertRaises(InvalidTypeException):
            self.assertFalse(PaymentMethod.VISA | None)

    def test_and_none(self):
        with self.assertRaises(InvalidTypeException):
            self.assertFalse(PaymentMethod.MASTERCARD & None)

    def test_duplicate_or(self):
        with self.assertRaises(DuplicateValueException):
            PaymentMethod.VISA | PaymentMethod.VISA

    def test_and_self(self):
        self.assertTrue(PaymentMethod.VISA & PaymentMethod.VISA)

    def test_and_conflict(self):
        self.assertFalse(PaymentMethod.VISA & PaymentMethod.PAYPAL)

    def test_and_string(self):
        # case insensitive
        self.assertTrue(PaymentMethod.VISA & "visa")
        self.assertTrue(PaymentMethod.VISA & "VISA")
        self.assertFalse(PaymentMethod.PAYPAL & "VISA")

    def test_merged_enums(self):
        self.assertTrue(CardProvider.VISA & CARD_PROVIDERS)
        self.assertTrue(CardProvider.MASTERCARD & CARD_PROVIDERS)

        self.assertTrue(WalletProvider.VENMO & WALLET_PROVIDERS)
        self.assertTrue(WalletProvider.PAYPAL & WALLET_PROVIDERS)

        self.assertTrue(CardProvider.VISA & ALL_METHODS)
        self.assertTrue(CardProvider.MASTERCARD & ALL_METHODS)
        self.assertTrue(WalletProvider.VENMO & ALL_METHODS)
        self.assertTrue(WalletProvider.PAYPAL & ALL_METHODS)
