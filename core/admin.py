from django.contrib import admin
from .models import (
    User,
    SchoolClass,
    TeacherProfile,
    Student,
    Parent,
    Message,
    FAQ
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')


admin.site.register(SchoolClass)
admin.site.register(TeacherProfile)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Message)
admin.site.register(FAQ)
