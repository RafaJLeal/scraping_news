from django.contrib import admin

from news.models import Headline, UserProfile

admin.site.register(Headline)
admin.site.register(UserProfile)
