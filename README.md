# PBL: Secure Application Development

- Team 6
- Web app in Django

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

Clone this repository and run this in the project directory:
``` sh
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser  # create account for admin interface 
```

Copy the example configuration to `MoldovaBlog/secret_config.py` and adapt it to your environment:

``` sh
cp ./MoldovaBlog/example_secret_settings.py ./MoldovaBlog/secret_settings.py 
```

Create the media folder at your chosen `MEDIA_ROOT`:`

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

# Testing

Install requirements for tests:
``` sh
python3 -m pip install -r requirements-test.txt
```

Run all the tests:
``` sh
python3 manage.py test --parallel
```
