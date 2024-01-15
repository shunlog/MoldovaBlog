import jwt
import datetime

from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User


def create_verification_token(username, email):
    '''Returns a string - the verification token (JWT).
    The token should contain username and email.'''
    payload = {
        'username': str(username),
        'email': str(email),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2)
        }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def send_verification_email(username, email):
    '''Send verification link to email.'''
    token = create_verification_token(username, email)
    url = reverse("email_verify", args=(token,))
    send_mail(
        'MoldovaBlog email verification',
        f'Visit the link to verify your email: {url}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def validate_verification_token(token):
    '''Validates the email verification token.
    Returns a tuple (username, email) if it's valid,
    or raises an exception otherwise.'''
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload['username'], payload['email']
    except jwt.exceptions.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
        raise ValueError('Invalid token')


def assign_email(token):
    '''Given a verification token, try to assign the email to username.
    Return username and email if successful, else raise exception.'''
    username, email = validate_verification_token(token)

    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError("No such username")

    try:
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        pass
    else:
        raise ValueError("Email already assigned")

    u.email = email
    u.save()

    return username, email
