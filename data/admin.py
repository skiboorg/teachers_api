from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Lesson)
admin.site.register(LessonType)
admin.site.register(LessonStatus)
admin.site.register(PaymentStatus)
admin.site.register(Note)
admin.site.register(NoteStatus)
