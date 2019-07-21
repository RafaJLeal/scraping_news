# Web scraping news
Application with basic user management and web scraping news of this <a href="https://elpais.com/">page<a>.

Python and Django versions:
  - Python 3.7.3
  - Django 2.2.2

Components needed to install:
  - requests -> pip install requests
  - beautifulsoup4 -> pip install beautifulsoup4
  - lxml -> pip install lxml
  - Pillow -> pip install Pillow
  - Bootstrap 4 -> pip install django-bootstrap4

Deployment of the application:
  - Be placed in the root folder of the project ../scraping_news
  - Execute the following commands:
    - python manage.py migrate
    - python manage.py collectstatic
    - python manage.py runserver
  - Access via web to http://localhost:8000
