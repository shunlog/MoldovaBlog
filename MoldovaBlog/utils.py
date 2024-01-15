from django.urls import reverse


def send_verification_email(username, email):
    '''Send an email verification link to email.'''

    def create_verification_token():
        '''Returns a string - the verification token (JWT).
        The token should contain username and email.'''
        pass

    token = create_verification_token()
    url = reverse("email_verify", args=(token,))

    pass


def validate_verification_token(token):
    '''Validates the email verification token.
    Returns a tuple (username, email) if it's valid, or raises an exception otherwise.'''

    raise ValueError
    pass
