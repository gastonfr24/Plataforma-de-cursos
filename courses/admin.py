from ast import Sub
from django.contrib import admin
from .models import Course, Chapter, Lesson, Author, Pricing, Subscription

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Author)
admin.site.register(Pricing)
admin.site.register(Subscription)