from enum_extensions.enum import StringEnum


class PaymentMethod(StringEnum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    APPLE_PAY = "APPLE_PAY"
    GOOGLE_PAY = "GOOGLE_PAY"
    VENMO = "VENMO"
    PAYPAL = "PAYPAL"


CARDS = PaymentMethod.MASTERCARD | PaymentMethod.VISA
WALLETS = ~CARDS


class CardProvider(StringEnum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"


class WalletProvider(StringEnum):
    VENMO = "VENMO"
    PAYPAL = "PAYPAL"


CARD_PROVIDERS = CardProvider.MASTERCARD | CardProvider.VISA
WALLET_PROVIDERS = WalletProvider.VENMO | WalletProvider.PAYPAL
ALL_METHODS = CARD_PROVIDERS | WALLET_PROVIDERS
