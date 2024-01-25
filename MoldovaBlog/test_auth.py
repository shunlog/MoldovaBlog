import unittest
import datetime
import re

from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from freezegun import freeze_time

from .utils import create_verification_token, validate_verification_token
from .forms import UserEmailCreationForm


class TokenTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.u1 = User.objects.create_user("john", "", "johnpassword")
        self.u1_email = "johnny@gmail.com"

    def test_correct_token(self):
        '''Test that the JWT token can be created and validated.'''
        tok = create_verification_token(self.u1.username, self.u1_email)
        uname, email = validate_verification_token(tok)
        self.assertEqual(self.u1.username, uname)
        self.assertEqual(self.u1_email, email)

    def test_wrong_token(self):
        '''Test that a wrong token raises an error.'''
        tok = create_verification_token(self.u1.username, self.u1_email)
        tok = tok[-1] + chr(ord(tok[-1]) + 1)  # garble the token a bit
        with self.assertRaises(ValueError):
            validate_verification_token(tok)

    def test_token_expired(self):
        '''Tokens should expire in 2 hours.'''
        tok = create_verification_token(self.u1.username, self.u1_email)
        with freeze_time(datetime.datetime.now() + datetime.timedelta(hours=2.1)):
            with self.assertRaises(ValueError):
                validate_verification_token(tok)


class AuthTestCase(TestCase):
    def setUp(self):
        self.uname = "johnny123"
        self.pwd = "arstarstarst"
        self.email = "johnny@test.com"

        self.uname2 = "john"
        self.pwd2 = "doe123123123"

        self.c = Client()

    def test_email_field_empty(self):
        '''The email field is not set immediately after registration.'''
        response = self.c.post(reverse("signup"),
                          {"username": self.uname,
                           "password1": self.pwd,
                           "password2": self.pwd,
                           "email": self.email})
        self.assertEqual(response.status_code, 302)
        u = User.objects.get(username=self.uname)
        self.assertEqual(u.email, "")

    def test_required_fields(self):
        '''Return an error if not all required fields were provided.'''
        f = UserEmailCreationForm({})
        self.assertEqual(len(f.errors), 3)

        f = UserEmailCreationForm({"username": self.uname,
                                   "password1": self.pwd})
        self.assertEqual(len(f.errors), 1)

    def test_email_is_optional(self):
        '''Email field is optional.'''
        response = self.c.post(reverse("signup"),
                          {"username": self.uname,
                           "password1": self.pwd,
                           "password2": self.pwd})
        self.assertEqual(response.status_code, 302)

    def test_verification_email_sent(self):
        '''An email with a verification link is sent.'''
        response = self.c.post(reverse("signup"),
                          {"username": self.uname,
                           "password1": self.pwd,
                           "password2": self.pwd,
                           "email": self.email})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

        # we can't compare the token as well because it's different every time
        # so instead we just compare the URL up to the token
        p = reverse("email_verify", args=('some_token',))
        path = p[:p.rfind('/')]
        ret = mail.outbox[0].body.find(path)
        self.assertNotEqual(ret, -1)

    def test_verify_email(self):
        '''Verifying the email sets the email field.'''
        u = User.objects.create_user(username=self.uname, password=self.pwd)
        tok = create_verification_token(self.uname, self.email)
        response = self.c.post(reverse("email_verify", args=(tok,)))

        self.assertEqual(response.status_code, 200)

        u.refresh_from_db()
        self.assertEqual(u.email, self.email)

    def test_verify_email_fails(self):
        '''Verifying the email fails if it's already assigned to someone else.'''
        u1 = User.objects.create_user(username=self.uname, password=self.pwd)
        u2 = User.objects.create_user(username=self.uname2, password=self.pwd2)

        # both users want to verify the same email
        tok1 = create_verification_token(self.uname, self.email)
        tok2 = create_verification_token(self.uname2, self.email)

        # only the first succeeds
        response = self.c.post(reverse("email_verify", args=(tok2,)))
        self.assertEqual(response.status_code, 200)

        response = self.c.post(reverse("email_verify", args=(tok1,)))
        self.assertEqual(response.status_code, 400)

    def test_signup_and_verify_email(self):
        '''Simulate the entire process of signinp up and clicking the verification link.'''
        response = self.c.post(reverse("signup"),
                          {"username": self.uname,
                           "password1": self.pwd,
                           "password2": self.pwd,
                           "email": self.email})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0].body
        # hostname is "testserver", the rest is the path
        path = re.search(r'testserver(/\S+)', email).group(1)
        self.assertIsNotNone(path)

        response = self.c.get(path)
        self.assertEqual(response.status_code, 200)
        u = User.objects.get(username=self.uname)
        self.assertEqual(u.email, self.email)

    def test_signup_without_email_then_add_one(self):
        '''Simulate the entire process of signinp up and then adding and verifying an email.'''
        # 1. register
        response = self.c.post(reverse("signup"),
                          {"username": self.uname,
                           "password1": self.pwd,
                           "password2": self.pwd})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

        # 2. log in
        response = self.c.post(reverse("login"), {"username": self.uname,
                                                  "password": self.pwd})

        # 3. change (add) email
        response = self.c.post(reverse("add_email"),
                               {'email': self.email,
                                'password': self.pwd})
        self.assertEqual(response.url, reverse("email_sent"))
        self.assertEqual(len(mail.outbox), 1)

        # 4. verify email
        email = mail.outbox[0].body
        path = re.search(r'testserver(/\S+)', email).group(1)  # hostname is "testserver", the rest is the path
        self.assertIsNotNone(path)

        response = self.c.get(path)
        self.assertEqual(response.status_code, 200)
        u = User.objects.get(username=self.uname)
        self.assertEqual(u.email, self.email)

    def test_change_email_wrong_password(self):
        '''Verify that the user has to supply the right password to change his email.'''
        User.objects.create_user(username=self.uname, password=self.pwd)
        self.c.login(username=self.uname, password=self.pwd)

        response = self.c.post(reverse("add_email"),
                               {'email': self.email,
                                'password': self.uname})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errorlist')
        self.assertEqual(len(mail.outbox), 0)

    def test_change_email_without_being_logged_in(self):
        '''If you're not logged in, you can't change your email (duh).'''
        response = self.c.post(reverse("add_email"),
                               {'email': self.email,
                                'password': self.pwd})
        self.assertNotEqual(response.url, reverse("email_sent"))
        self.assertEqual(len(mail.outbox), 0)
