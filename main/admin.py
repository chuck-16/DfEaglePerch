from django.contrib import admin
from .models import Story, ReadingList, ClickCounter

# Register your models here.
admin.site.register(Story)
admin.site.register(ReadingList)
admin.site.register(ClickCounter)