from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import TeacherProfile, Parent, Student, Message


@login_required
def dashboard(request):
    user = request.user

    # Админ
    if user.role == 'admin':
        messages = Message.objects.all().order_by('-created_at')
        return render(request, 'core/dashboard-admin.html', {
            'messages': messages
        })

    # Учитель
    elif user.role == 'teacher':
        teacher = TeacherProfile.objects.get(user=user)
        messages = Message.objects.filter(
            school_class=teacher.school_class
        ).order_by('-created_at')

        return render(request, 'core/dashboard-teacher.html', {
            'messages': messages,
            'school_class': teacher.school_class
        })

    # Родитель
    elif user.role == 'parent':
        parent = Parent.objects.get(user=user)
        children = parent.children.all()

        messages = Message.objects.filter(
            school_class__student__in=children
        ).distinct().order_by('-created_at')

        return render(request, 'core/dashboard-parent.html', {
            'messages': messages,
            'children': children
        })

    # Ученик
    elif user.role == 'student':
        student = Student.objects.get(user=user)

        messages = Message.objects.filter(
            school_class=student.school_class
        ).order_by('-created_at')

        return render(request, 'core/dashboard-student.html', {
            'messages': messages,
            'school_class': student.school_class
        })

    # Если роль странная
    return redirect('/')
