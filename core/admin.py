from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
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
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'role')
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Роль', {'fields': ('role',)}),
    )

admin.site.register(SchoolClass)
admin.site.register(TeacherProfile)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Message)
admin.site.register(FAQ)
