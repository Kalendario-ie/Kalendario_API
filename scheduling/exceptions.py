from django.core.exceptions import ValidationError


class DifferentOwnerError(ValidationError):
    """
    This error is to be used when elements in a one to many relationship does not belong to the same owner
    """
    def __init__(self, message, code=None, params=None):
        super().__init__(message, code, params)


class InvalidCustomer(ValidationError):
    """
    This error is to be used when the customer for an appointment is invalid
    """
    def __init__(self, message, code=None, params=None):
        super().__init__(message, code, params)
