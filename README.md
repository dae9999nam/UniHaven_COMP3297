# UniHaven

### This repository is to develop a web-service API in Agile development to provide quick accommodation search service for undergraduates and post-graduates in the University of Hong Kong

## Latest Update Note - 2025/Apr/28th

- Authentication Implemented
- Email Notification Implemented (printed on the console for both user and cedars-specialist)
- Reservation Function Updated

System usage has been updated - Baek Seunghyeon

## Requirements

pipenv
Python3
Django ~=5.1
Django RESTframework

## File Structure

    SourceCode #Project Root
    ├── UniHaven # Config Root
    ├── Accommodation #App Folder
    ├── Reservation #App Folder
    ├── Rating #App Folder
    └── README.md       ├── models.py
                        ├── views.py
                        ├── serializers.py
                        └── urls.py

- Project Root = SourceCode
- Config Root = UniHaven
- Project Settings = files under UniHaven
- App root: Accommodation
- Key files: models.py, views.py, serializers.py, urls.py
- Manage Tool = manage.py

## Usage

- Setting up Requirements

1. `python3 -m pipenv install Django~=5.1` to install Django
2. `pip install djangorestframework` to install Django REST framework

- Setting up Virtual Environment and Run Server

1. `python3 -m pipenv shell` to run virtual environment
   - `exit` to exit the shell
2. `python3 manage.py runserver` to run server
   - Control-C to stop the server

When there is update in database

1. `python3 manage.py makemigrates`
2. `python3 manage.py migrates`

To create a Django project named "<projectname>" with an app called "<appname>"

1. `django-admin startproject <projectname> . `
2. `python3 manage.py startapp <appname>`

To get authenticated

1.  Run the shell `python3 manage.py shell`
2.  Make University instances - HKU, HKUST, CUHK in this project scope

        `hku   = University.objects.create(code='HKU',   name='The University of Hong Kong', specialist_email='')`
        `hkust = University.objects.create(code='HKUST', name='Hong Kong University of Science and Technology', specialist_email='')`
        `cuhk  = University.objects.create(code='CUHK',  name='The Chinese University of Hong Kong', specialist_email='')`

- Add specialist email address
