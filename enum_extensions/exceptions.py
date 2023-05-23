class InvalidTypeException(Exception):
    def __init__(self, expected, received):
        self.message = f"Expected {expected} type object, got {received}"
        super().__init__(self.message)


class DuplicateValueException(Exception):
    def __init__(self, current, next_):
        self.message = f"{current} is same as {next_}."
        super().__init__(self.message)
