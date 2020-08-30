from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Allpost)
admin.site.register(Post_liked)
admin.site.register(Following)
admin.site.register(Follower)