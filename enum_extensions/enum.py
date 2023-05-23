from enum import Enum
from typing import Type, Union, Optional

from enum_extensions.exceptions import InvalidTypeException, DuplicateValueException


class StringEnum(Enum):
    """
    Custom enumeration class for representing string values.

    Description:
    The StringEnum class is a custom implementation of the Enum class that specializes in representing string values.
    It provides the support for the bitwise operation on string type enums.

    Usage:
    - Creating a new string-based enumeration class:
        class MyEnum(StringEnum):
            VALUE_1 = "First Value"
            VALUE_2 = "Second Value"
            ...

    - Accessing enumeration members:
        value = MyEnum.VALUE_1
        print(value)  # Output: MyEnum.VALUE_1

    - Comparing enumeration members:
        value1 = MyEnum.VALUE_1
        value2 = MyEnum.VALUE_2
        print(value1 == value2)  # Output: False

    - Iterating over enumeration members:
        for member in MyEnum:
            print(member)  # Output: MyEnum.VALUE_1, MyEnum.VALUE_2, ...

    - Getting the string value of an enumeration member:
        print(MyEnum.VALUE_1.value)  # Output: "First Value"

    class PaymentMethod(StringEnum):
        VISA = "VISA"
        MASTERCARD = "MASTERCARD"
        APPLE_PAY = "APPLE_PAY"
        GOOGLE_PAY = "GOOGLE_PAY"
        VENMO = "VENMO"
        PAYPAL = "PAYPAL"

    - Aggregating multiple enums to single variable using OR '|'operator
        CARDS = PaymentMethod.MASTERCARD | PaymentMethod.VISA
        print(CARDS)    # PaymentMethod.MASTERCARD|VISA

    - Using negation NOT '~' to get the invert values of CARDS
        WALLETS = ~CARDS
        print(WALLETS)    # PaymentMethod.APPLE_PAY|GOOGLE_PAY|VENMO|PAYPAL
    """

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self.value}>"

    def __eq__(self, other: Union[str, Type["StringEnum"]]) -> bool:
        """
        Checks if the enumeration member is equal to another value.

        Parameters:
        - other (str, Type['StringEnum']): The value to compare with the enumeration member.

        Returns:
        - result (bool): True if the enumeration member is equal to 'other', False otherwise.

        Description:
        This method is used to check if the enumeration member is equal to another value.
        If 'other' is a string, it compares the value of the enumeration member with 'other' using the '==' operator.
        If 'other' is an instance of the same enumeration class, it compares the values of both members.
        If 'other' does not match any of the above types, it returns False.

        The method returns a boolean value indicating the result of the equality comparison.
        """
        if isinstance(other, str):  # pylint: disable=R1705
            return self.value == other
        elif isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __or__(self, other: Optional["StringEnum"]) -> Union["StringEnum", Enum]:
        """
        Performs a bitwise 'or' operation between the enumeration member and another value.

        Parameters:
        - other (Optional['StringEnum']): The value to perform the 'or' operation with.

        Returns:
        - result ('StringEnum', Enum): The result of the 'or' operation.

        Raises:
        - DuplicateValueException: If 'other' is not None and has the same value as the enumeration member.
        - InvalidTypeException: If 'other' is not an instance of the same enumeration class,
          an object that subclasses StringEnum, or None.

        Description:
        This method is used to perform a bitwise 'or' operation between the enumeration member and another value.
        If 'other' is not None and has the same value as the enumeration member, a DuplicateValueException is raised.
        If 'other' is an instance of the same enumeration class, it joins the values of both members,
        removing any duplicates, and returns a new instance of the enumeration class with the joined value.
        If 'other' is an object that subclasses StringEnum, it performs a similar joining operation but
        creates a new class with the merged values and returns an instance of that merged class.
        If 'other' is None, it returns new instance of the enumeration class with the same value as the current member.

        The method returns an instance of the enumeration class.
        """

        def remove_duplicate(value: str) -> str:
            # OR between 2 aggregated enum value can lead to duplicate values
            # it removes the duplicate values
            return "|".join(sorted(set(value.split("|"))))

        if other is not None and self.value == other.value:
            raise DuplicateValueException(self.value, other.value)
        if isinstance(other, self.__class__):
            joined_value = remove_duplicate(f"{self.value}|{other.value}")
            return self.__class__(joined_value)
        if issubclass(other.__class__, StringEnum):
            merged_value = remove_duplicate(f"{self.value}|{other.value}")
            merged_class_name = f"{self.__class__.__name__}_{other.__class__.__name__}"
            merged_class = StringEnum(  # pylint: disable=E1121
                merged_class_name, [(merged_value, merged_value)]
            )
            setattr(merged_class, "merged", True)
            return merged_class(merged_value)
        raise InvalidTypeException("StringEnum", type(other))

    def __and__(self, other: Optional[Union[str, "StringEnum"]]) -> bool:
        """
        Performs a bitwise 'and' operation between the enumeration member and another value.

        Parameters:
        - other (Optional[Union[str, "StringEnum"]]): The value to perform the 'and' operation with.

        Returns:
        - result (bool): The result of the 'and' operation.

        Raises:
        - InvalidTypeException: If the type of 'other' is not a string, an instance of the same enumeration class,
          or an object with a 'merged' attribute, its a flag to mark a merged enum of two string enums.

        Description:
        This method is used to perform a bitwise 'and' operation between the enumeration member and another value.
        If 'other' is a string, it performs a case-insensitive check to determine if the value of the enumeration member
        is present within the other string. If 'other' is an instance of the StringEnum class or an object with a
        'merged' attribute, it checks if the value of the enumeration member is equal to the value of 'other'.
        If 'other' does not match any of the above types, an InvalidTypeException is raised.

        The method returns a boolean value indicating the result of the 'and' operation.
        """
        if isinstance(other, str):  # pylint: disable=R1705
            return self.value.lower() in other.lower()
        elif isinstance(other, self.__class__) or hasattr(other, "merged"):
            return self.value in other.value
        else:
            raise InvalidTypeException(type(self.__class__), type(other))

    def __invert__(self) -> "StringEnum":
        """
        Inverts the enumeration member by creating a new instance with missing values.

        Returns:
        - inverted ('Enum'): A new instance of the enumeration class with missing values inverted.

        Description:
        This method is used to invert the enumeration member by creating a new instance of the enumeration class.
        It iterates over all the members of the enumeration class and checks for missing values not present
        in the current member's value.
        It creates a new instance with missing values inverted and returns it.
        If no missing values are found, it returns the current instance itself.
        """
        members = self.__class__._value2member_map_
        inverted = None
        for member_key, member_object in members.items():
            if member_key not in self._value_:
                if inverted is None:
                    inverted = self.__class__(member_key)
                else:
                    inverted = inverted | member_object
        return inverted or self.__class__("")

    @classmethod
    def _missing_(cls: Type["StringEnum"], value: str) -> "StringEnum":
        """
        Creates a new instance of the StringEnum class with the specified value.

        Parameters:
        - cls (Type['StringEnum']): The class object of the enumeration.
        - value (str): The value assigned to the enumeration member.

        Returns:
        - member ('StringEnum'): An instance of the StringEnum class with the specified value.

        Description:
        This method is called when a value is assigned to a non-existent enumeration member.
        It creates a new instance of the StringEnum class with the specified value and returns it.
        The created instance will have its '_name_' and '_value_' attribute set to the given value.
        """
        member = object.__new__(cls)
        member._name_ = value
        member._value_ = value
        return member
