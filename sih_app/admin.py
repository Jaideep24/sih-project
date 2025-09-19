from django.contrib import admin

from django.contrib import admin
from .models import Student, Teacher, JournalEntry, Appointment, SiteSetting

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(JournalEntry)
admin.site.register(Appointment)
admin.site.register(SiteSetting)
