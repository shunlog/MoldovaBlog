from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User


class TestProfileModel(TestCase):
    def test_profile_created(self):
        '''A Profile instance should be automatically created for each new User'''
        u = User.objects.create_user("test")
        self.assertIsInstance(u.profile, Profile)

        # the profile should be created only on the first save(),
        # using the `created` argument of the `post_save` signal
        u.save()  # this shouldn't raise an exception
