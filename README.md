# PBL: Secure Application Development

- Team 6
- Web app in Django

# Requirements

    Django==5.0
    Python==3.11

# Installation

``` sh
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -r requirements.txt
```

# Running

``` sh
source .venv/bin/activate

# only required on the first run,
# or if the models have been changed
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver
```

# Testing

``` sh
source .venv/bin/activate

python3 manage.py test
```
