# UniHaven

### This repository is to develop a web-service API with Agail approach to provide quick accommodation search service for undergraduates and post-graduates in the University of Hong Kong

## Requirements

pipenv
Python
Django ~=5.1
djangorestframework

## File Structure

    SourceCode #Project Root
    ├── UniHaven # Config Root
    ├── Accommodation #App Folder
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

1. `python3 -m pipenv install Django~=5.1` to install Django
2. `pip install djangorestframework` to install Django REST framework
3. `python3 -m pipenv shell` to run virtual environment
4. `python3 manage.py runserver` to run server

When there is update in database

1. `python3 manage.py makemigrates`
2. `python3 manage.py migrates`
