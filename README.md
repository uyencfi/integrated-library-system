# integrated-library-system
Assignment 1 for BT2102: Data Management and Visualisation

Django web app for the ILS

1. Virtual environment
2. pip install -r requirements.txt
3. mysql workbench: create schema `ils`;
4. create + import mongodb: Database `Assignment1`, collections `Books`. Import `books.json` (the old version)
5. libsys/settings.py: fill in DATABASE settings to your mysql username and password
6. python manage.py migrate
7. python database_setup.py (FILL IN YOUR MYSQL USERNAME + PASSWORD)
8. python manage.py createsuperuser
9. python manage.py runserver
10. Control-C to stop the server.
