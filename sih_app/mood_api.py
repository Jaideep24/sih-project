from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import MoodEntry, Student

@csrf_exempt
def save_mood(request):
    if request.method == 'POST' and request.session.get('user_type') == 'student':
        student_email = request.session.get('user_email')
        mood = int(request.POST.get('mood', 0))
        if not (1 <= mood <= 5):
            return JsonResponse({'success': False, 'error': 'Invalid mood value'})
        try:
            student = Student.objects.get(email=student_email)
            MoodEntry.objects.create(student=student, mood=mood, timestamp=timezone.now())
            return JsonResponse({'success': True})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def get_mood_history(request):
    if request.session.get('user_type') == 'student':
        student_email = request.session.get('user_email')
        try:
            student = Student.objects.get(email=student_email)
            moods = MoodEntry.objects.filter(student=student).order_by('-timestamp')[:30]
            data = [
                {'mood': m.mood, 'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M')} for m in moods
            ]
            return JsonResponse({'success': True, 'history': data})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
