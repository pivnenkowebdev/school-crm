from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TeacherProfile, Parent, Student, Message, SchoolClass
from django.db.models import Q

@login_required
def dashboard(request):
    user = request.user

    # Админ
    if user.role == 'admin':

        if request.method == "POST":
            title = request.POST.get("title")
            text = request.POST.get("text")
            class_id = request.POST.get("school_class")

            school_class = None
            if class_id:
                school_class = SchoolClass.objects.get(id=class_id)

            if title and text:
                Message.objects.create(
                    author=user,
                    title=title,
                    text=text,
                    school_class=school_class
                )
                return redirect('dashboard')

        messages = Message.objects.all().order_by('-created_at')
        classes = SchoolClass.objects.all()

        return render(request, 'core/dashboard-admin.html', {
            'messages': messages,
            'classes': classes
        })

    # Учитель
    elif user.role == 'teacher':
        teacher = TeacherProfile.objects.get(user=user)

        if request.method == "POST":
            title = request.POST.get("title")
            text = request.POST.get("text")

            if title and text:
                Message.objects.create(
                    author=user,
                    title=title,
                    text=text,
                    school_class=teacher.school_class
                )
                return redirect('dashboard')

        messages = Message.objects.filter(
            Q(school_class=teacher.school_class) |
            Q(school_class__isnull=True)
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
            Q(school_class__student__in=children) |
            Q(school_class__isnull=True)
        ).distinct().order_by('-created_at')

        return render(request, 'core/dashboard-parent.html', {
            'messages': messages,
            'children': children
        })

    # Ученик
    elif user.role == 'student':
        student = Student.objects.get(user=user)

        messages = Message.objects.filter(
            Q(school_class=student.school_class) |
            Q(school_class__isnull=True)
        ).order_by('-created_at')

        return render(request, 'core/dashboard-student.html', {
            'messages': messages,
            'school_class': student.school_class
        })

    # Если роль странная
    return redirect('/')
