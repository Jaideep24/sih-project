from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, MoodEntry, Teacher
from django.db.models import Q

def supervisor_student_details(request):
    if request.session.get('user_type') != 'supervisor':
        return redirect('login')
    supervisor_email = request.session.get('user_email')
    try:
        supervisor = Teacher.objects.get(email=supervisor_email)
    except Teacher.DoesNotExist:
        return redirect('login')
    institution = supervisor.institution
    query = request.GET.get('q', '').strip()
    students = Student.objects.filter(institution=institution)
    if query:
        students = students.filter(student_id__icontains=query)
    # Prefetch mood history for each student (last 10 entries)
    student_data = []
    for student in students:
        moods = MoodEntry.objects.filter(student=student).order_by('-timestamp')[:10]
        student_data.append({
            'student': student,
            'moods': moods,
        })
    return render(request, 'supervisor_student_details.html', {
        'student_data': student_data,
        'query': query,
    })
