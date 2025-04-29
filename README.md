# UniHaven

### This repository is to develop a web-service API in Agile development to provide quick accommodation search service for undergraduates and post-graduates in the University of Hong Kong

## Latest Update Note - 2025/Apr/28th

- Authentication Implemented
- Email Notification Implemented (printed on the console for both user and cedars-specialist, only the university defined in the accommodation item will get notification for the change in reservation)
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

## To Add University instance and Connect University to an Existing Accommodation item

1.  Run the shell `python3 manage.py shell`
2.  Make University instances - HKU, HKUST, CUHK in this project scope

        from authentication.models import University, ServiceAccount
        from rest_framework.authtoken.models import Token
        from Accommodations.models import Accommodation

        hku   = University.objects.create(code='HKU',   name='The University of Hong Kong', specialist_email='')
        hkust = University.objects.create(code='HKUST', name='Hong Kong University of Science and Technology', specialist_email='')
        cuhk  = University.objects.create(code='CUHK',  name='The Chinese University of Hong Kong', specialist_email='')

3.  Add specialist email address

        hku.specialist_email = 'support@cedars.hku.edu.hk'
        hku.save()

4.  Link an existing Accommodation to one or more universities (replace 11124 with your accommodation’s PK)

        from Accommodations.models import Accommodation
        acc = Accommodation.objects.get(pk=11124)
        print(acc.universities.all())  # --> if this prints [], empty queryset
        from authentication.models import University
        hku = University.objects.get(code='HKU') # HKU in this example

        acc.universities.add(hku) --> Add university to the accommodation item
        acc.save()

    `print(acc.universities.all()) ` to check which university is offering this accommodation

## To Make a dummy Account, please follow the sequence

1.  Create Dummy User for the service

        from django.contrib.auth import get_user_model
        from rest_framework.authtoken.models import Token
        from authentication.models import University, ServiceAccount

        User = get_user_model()

2.  make the service user

        svc_user = User.objects.create_user(username='cedars-hku', email='<email address>', password='<password>')

3.  create the token for that user

        token = Token.objects.create(user=svc_user)
        print("Token key is:", token.key)

4.  link to your ServiceAccount

        uni = University.objects.get(code='HKU')
        ServiceAccount.objects.create(name='cedars-hku', university=uni, token=token)
