from django.contrib import admin
from .models import Feed, User, News

admin.site.register(Feed)
admin.site.register(User)
admin.site.register(News)