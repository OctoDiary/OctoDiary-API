class CredentialsException(Exception):
    def __init__(self, error):
        super().__init__(error + ' credentials given!')


class TooManyCredentialsGivenException(CredentialsException):
    """Raised when too many credentials given."""
    def __init__(self):
        super().__init__('Too many')


class NoCredentialsGivenException(CredentialsException):
    """Raised when no credentials given."""
    def __init__(self):
        super().__init__('No')


class NotEnoughCredentialsException(CredentialsException):
    """Raised when no credentials given."""
    def __init__(self):
        super().__init__('Not enough')


class LoginFailedException(Exception):
    """Raised when the login fails."""
    def __init__(self):
        super().__init__('Username and password did not match!')


class ServerException(Exception):
    """Raised when the server gives an error."""
    def __init__(self):
        super().__init__('Server error. Please try again later.')


class InvalidRequestException(Exception):
    """Raised when user requests information incorrectly."""
    def __init__(self):
        super().__init__('Invalid request. Please check call parameters.')
