from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, MoodEntry, Teacher

def supervisor_student_list(request):
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
    return render(request, 'supervisor_student_list.html', {
        'students': students,
        'query': query,
    })

def supervisor_student_detail(request, student_id):
    if request.session.get('user_type') != 'supervisor':
        return redirect('login')
    supervisor_email = request.session.get('user_email')
    try:
        supervisor = Teacher.objects.get(email=supervisor_email)
    except Teacher.DoesNotExist:
        return redirect('login')
    institution = supervisor.institution
    student = get_object_or_404(Student, student_id=student_id, institution=institution)
    moods = MoodEntry.objects.filter(student=student).order_by('-timestamp')[:10]
    return render(request, 'supervisor_student_detail.html', {
        'student': student,
        'moods': moods,
    })
