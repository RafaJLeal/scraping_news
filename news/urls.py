from django.urls import path

from news.views import *


urlpatterns = [
	path('', home, name='home'),
	path('scrape/', scrape, name='scrape'),
]