# Secure Blog in Django

This is a web app I developed for an university course in which we studied best security practices.
The application is a simple blog/news website on which admins can post articles, and the users can register and leave comments.
Although minimal, it has most of the basic features all modern web apps:
- Authentication (sign up, login, session management)
- Authorization (permissions)
- File upload

The goal of this project was to learn the best practices of developing secure web apps.
The book "The Web Application Hacker’s Handbook" gives a good introduction to the topic.
For a more structured approach in keeping track of all the various security features,
we used the "[OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)" document as a guide,
We implemented most of the Level 1 requirements as well as some of Level 2,
which is a pretty good assurance that our application is safe at least against the most common web app vulnerabilities.

The [Django documentation on security](https://docs.djangoproject.com/en/5.0/topics/security/) was also a valuable resource for configuring our app correctly.
In general, for the sake of security, we adopted a development methodology in which we would prefer ready solutions to writing our own,
or at least doing a lot of research on the best solutions for every problem we encountered
to make sure that most of our code is tested and highly reliable.

# Screenshots

<p float="left">
  <img src="img/home.png" width="49%" />
  <img src="img/home2.png" width="49%" />
  <img src="img/post.png" width="49%" />
  <img src="img/comments.png" width="49%" />
  <img src="img/user.png" width="49%" />
  <img src="img/admin.png" width="49%" />
  <img src="img/login.png" width="49%" />
  <img src="img/signup.png" width="49%" />
</p>


# Requirements

    Django==5.0
    Python==3.11

It's recommended to use a virtual environment for this project. For example:
``` sh
python3 -m venv .venv
source .venv/bin/activate
# on windows type this instead:
# .\.venv\Scripts\activate
```

# Installation

Clone this repository and install the dependencies:
``` sh
python3 -m pip install -r requirements.txt
```

Copy the example configuration to `MoldovaBlog/secret_config.py` and adapt it to your environment:

``` sh
cp ./MoldovaBlog/example_secret_settings.py ./MoldovaBlog/secret_settings.py 
```

Run these:
``` sh
python3 manage.py migrate
python3 manage.py createsuperuser  # create account for admin interface 
```

Create the media folder at your chosen `MEDIA_ROOT` (from the `secret-settings.py` file):

``` sh
sudo mkdir -p /var/www
sudo mkdir /var/www/MoldovaBlog
sudo chown <your_username> /var/www/MoldovaBlog
chgrp <your_username> /var/www/MoldovaBlog
```

# Running

``` sh
python3 manage.py migrate  # required if the models have been changed

python3 manage.py runserver
```

- homepage: http://127.0.0.1:8000/
- admin page: http://127.0.0.1:8000/admin

Things to try out:
1. Create some posts on the admin page
2. Go to the homepage and register a new user
3. Find the posts you have created
4. Leave some comments
5. Log out, log in, reset password, etc.

# Testing

Install requirements for tests:
``` sh
python3 -m pip install -r requirements-test.txt
```

Run all the tests:
``` sh
python3 manage.py test --parallel
```
