from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('teacher', 'Учитель'),
        ('parent', 'Родитель'),
        ('student', 'Ученик'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class SchoolClass(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TeacherProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} - {self.school_class.name}'

class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} ({self.school_class.name})'

class Parent(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    children = models.ManyToManyField(Student)

    def __str__(self):
        return self.user.name

class Message(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    school_class = models.ForeignKey(SchoolClass, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.author.name})'

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question
