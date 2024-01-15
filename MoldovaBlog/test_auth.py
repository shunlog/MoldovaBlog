#!/usr/bin/env python3
import unittest
from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .utils import create_verification_token, validate_verification_token


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
        self.assertRaises(ValueError, validate_verification_token, (tok,))


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

    # TODO test for field errors instead of status_code 400
    # def test_required_fields(self):
    #     '''Return an error if not required fields were provided.'''
    #     response = self.c.post(reverse("signup"), {})
    #     self.assertEqual(response.status_code, 400)

    #     response = self.c.post(reverse("signup"),
    #                       {"username": self.uname,
    #                        "password1": self.pwd})
    #     response = self.c.post(reverse("signup"), {})
    #     self.assertEqual(response.status_code, 400)

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

        p = reverse("email_verify", args=('some_token',))
        # we can't compare the token as well because it's different every time
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

        tok1 = create_verification_token(self.uname, self.email)
        tok2 = create_verification_token(self.uname2, self.email)

        response = self.c.post(reverse("email_verify", args=(tok2,)))
        self.assertEqual(response.status_code, 200)

        response = self.c.post(reverse("email_verify", args=(tok1,)))
        self.assertEqual(response.status_code, 400)
