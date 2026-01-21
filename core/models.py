from django.db import models
from django.contrib.auth.models import AbstractUser

# --------------------------
# Кастомный User
# --------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('teacher', 'Учитель'),
        ('parent', 'Родитель'),
        ('student', 'Ученик'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username  # Можно использовать username или first_name + last_name

# --------------------------
# Классы школы
# --------------------------
class SchoolClass(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# --------------------------
# Профиль учителя
# --------------------------
class TeacherProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.school_class.name}'

# --------------------------
# Ученики
# --------------------------
class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} ({self.school_class.name})'

# --------------------------
# Родители
# --------------------------
class Parent(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    children = models.ManyToManyField(Student)

    def __str__(self):
        return self.user.username

# --------------------------
# Сообщения / рассылки
# --------------------------
class Message(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    school_class = models.ForeignKey(SchoolClass, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.author.username})'

# --------------------------
# FAQ
# --------------------------
class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question
