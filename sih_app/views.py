from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.conf import settings
from .models import Student, Teacher, MoodEntry, Institution, SiteSetting, JournalEntry
from .models import CounsellorSlot, Appointment, WaitingList
from .models import ChatRoom, ChatRoomMembership
from .forms import ChatRoomCreateForm
from .streamchat_api import create_stream_channel, end_stream_channel, generate_user_token, add_user_to_channel

def peer(request):
	if not request.session.get('user_type'):
		return redirect('login')
	student = Student.objects.get(email=request.session['user_email'])
	institution = student.institution
	form = ChatRoomCreateForm()
	form_errors = None
	if request.method == 'POST':
		form = ChatRoomCreateForm(request.POST)
		if form.is_valid():
			room = form.save(commit=False)
			room.creator = student
			room.institution = institution
			room.save()
			ChatRoomMembership.objects.create(room=room, student=student)
			create_stream_channel(
				str(room.id),
				room.name,
				str(student.student_id),
				[str(student.student_id)],
				room.category,
			)
			return redirect('peer_chat', room_id=room.id)
		else:
			form_errors = form.errors
	active_rooms = ChatRoom.objects.filter(institution=institution, is_active=True)
	completed_rooms = ChatRoom.objects.filter(institution=institution, is_active=False)
	return render(request, 'peer.html', {
		'active_rooms': active_rooms,
		'completed_rooms': completed_rooms,
		'form': form,
		'form_errors': form_errors,
		'student': student,
	})

def peer_chat(request, room_id):
	if not request.session.get('user_type'):
		return redirect('login')
	student = Student.objects.get(email=request.session['user_email'])
	room = get_object_or_404(ChatRoom, id=room_id)
	ChatRoomMembership.objects.get_or_create(room=room, student=student)
	
	# Add user to Stream Chat channel if they're not the creator
	is_creator = (room.creator == student)
	if not is_creator:
		try:
			add_user_to_channel(str(room.id), str(student.student_id))
		except Exception as e:
			print(f"Failed to add user to Stream channel: {e}")
	
	stream_token = generate_user_token(str(student.student_id))
	return render(request, 'peer_chat.html', {
		'room': room,
		'student': student,
		'is_creator': is_creator,
		'stream_api_key': settings.STREAM_API_KEY,
		'stream_token': stream_token,
	})

def end_chat_room(request, room_id):
	if not request.session.get('user_type'):
		return redirect('login')
	student = Student.objects.get(email=request.session['user_email'])
	room = get_object_or_404(ChatRoom, id=room_id, creator=student)
	room.is_active = False
	room.ended_at = timezone.now()
	room.save()
	end_stream_channel(str(room.id))
	return redirect('peer')

# Dashboard view
def dashboard(request):
	# Only supervisors can view dashboard
	if request.session.get('user_type') != 'supervisor':
		return redirect('login')
	teacher = Teacher.objects.get(email=request.session['user_email'])
	institution = teacher.institution

	# Get filter from GET params
	time_filter = request.GET.get('range', 'today')
	from datetime import datetime, timedelta
	now = datetime.now()
	if time_filter == 'today':
		start = now.replace(hour=0, minute=0, second=0, microsecond=0)
	elif time_filter == 'weekly':
		start = now - timedelta(days=now.weekday())
		start = start.replace(hour=0, minute=0, second=0, microsecond=0)
	elif time_filter == 'monthly':
		start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
	else:
		start = now.replace(hour=0, minute=0, second=0, microsecond=0)

	# Get all students in institution
	students = Student.objects.filter(institution=institution)
	moods = []
	from collections import Counter
	if students.exists():
		moods = list(
			MoodEntry.objects.filter(student__in=students, timestamp__gte=start)
			.values_list('mood', flat=True)
		)
	mood_counts = Counter(moods)
	# Map mood int to label/color
	mood_map = [
		{'label': 'Mood 1', 'color': '#6c7bff', 'emoji': '😃'},
		{'label': 'Mood 2', 'color': '#22c55e', 'emoji': '🙂'},
		{'label': 'Mood 3', 'color': '#f59e0b', 'emoji': '😐'},
		{'label': 'Mood 4', 'color': '#ef4444', 'emoji': '😕'},
		{'label': 'Mood 5', 'color': '#6366f1', 'emoji': '😢'},
	]
	mood_stats = []
	total = sum(mood_counts.values())
	for i, m in enumerate(mood_map):
		count = mood_counts.get(i+1, 0)
		percent = (count/total*100) if total else 0
		mood_stats.append({'label': m['label'], 'color': m['color'], 'count': count, 'percent': round(percent,1), 'emoji': m['emoji']})

	return render(request, 'dashboard.html', {
		'mood_stats': mood_stats,
		'time_filter': time_filter,
	})

# Supervisor: manage appointments and waiting list
def supervisor_appointments(request):
	if request.session.get('user_type') != 'supervisor':
		return redirect('login')
	teacher = Teacher.objects.get(email=request.session['user_email'])
	slots = CounsellorSlot.objects.filter(created_by=teacher)
	# Only show appointments and waiting list for slots created by this supervisor (their own institution)
	appointments = Appointment.objects.filter(slot__in=slots)
	waiting_list = WaitingList.objects.filter(slot__in=slots)
	if request.method == 'POST':
		if 'appt_id' in request.POST:
			appt = Appointment.objects.get(id=request.POST['appt_id'])
			appt.status = request.POST['status']
			appt.save()
		elif 'waiting_id' in request.POST:
			waiting = WaitingList.objects.get(id=request.POST['waiting_id'])
			if request.POST.get('action') == 'confirm':
				# Only create appointment if not already present for this slot/student
				if not Appointment.objects.filter(slot=waiting.slot, student=waiting.student).exists():
					Appointment.objects.create(slot=waiting.slot, student=waiting.student, status='confirmed')
				waiting.delete()
			elif request.POST.get('action') == 'remove':
				waiting.delete()
		# Refresh data after changes
		appointments = Appointment.objects.filter(slot__in=slots)
		waiting_list = WaitingList.objects.filter(slot__in=slots)
	return render(request, 'supervisor_appointments.html', {
		'appointments': appointments,
		'waiting_list': waiting_list,
	})

# Student slot booking and waiting list view
def book_slot(request):
	if request.session.get('user_type') != 'student':
		return redirect('login')
	student = Student.objects.get(email=request.session['user_email'])
	# Only show slots created by supervisors from the student's institution
	slots = CounsellorSlot.objects.filter(is_active=True, created_by__institution=student.institution)
	booked_appointments = Appointment.objects.filter(student=student, slot__created_by__institution=student.institution)
	booked_slot_ids = [a.slot.id for a in booked_appointments]
	slot_statuses = {a.slot.id: a.status for a in booked_appointments}
	waiting_list = WaitingList.objects.filter(student=student, slot__created_by__institution=student.institution)
	waiting_slot_ids = [w.slot.id for w in waiting_list]
	if request.method == 'POST':
		slot_id = request.POST.get('slot_id')
		slot = CounsellorSlot.objects.get(id=slot_id, created_by__institution=student.institution)
		# Check if slot is already booked by another student
		if Appointment.objects.filter(slot=slot, status='confirmed').exists():
			# Add to waiting list if not already
			if not WaitingList.objects.filter(slot=slot, student=student).exists():
				WaitingList.objects.create(slot=slot, student=student)
		else:
			Appointment.objects.create(slot=slot, student=student, status='confirmed')
		# Refresh data after booking
		booked_appointments = Appointment.objects.filter(student=student, slot__created_by__institution=student.institution)
		booked_slot_ids = [a.slot.id for a in booked_appointments]
		slot_statuses = {a.slot.id: a.status for a in booked_appointments}
		waiting_list = WaitingList.objects.filter(student=student, slot__created_by__institution=student.institution)
		waiting_slot_ids = [w.slot.id for w in waiting_list]
	return render(request, 'book_slot.html', {
		'slots': slots,
		'booked_slot_ids': booked_slot_ids,
		'slot_statuses': slot_statuses,
		'waiting_list': waiting_list,
		'waiting_slot_ids': waiting_slot_ids,
	})

def signup(request):
	institutions = Institution.objects.all()
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		student_id = request.POST.get('student_id')
		institution_id = request.POST.get('institution')
		if Student.objects.filter(email=email).exists():
			return render(request, 'signup.html', {'error': 'Email already exists', 'institutions': institutions})
		institution = Institution.objects.get(id=institution_id) if institution_id else None
		Student.objects.create(email=email, password=password, student_id=student_id, institution=institution)
		return redirect('login')
	return render(request, 'signup.html', {'institutions': institutions})

def index(request):
	user_type = request.session.get('user_type')
	if user_type == 'student':
		interval = 3600
		if SiteSetting.objects.exists():
			interval = SiteSetting.objects.first().quote_update_interval
		return render(request, 'index.html', {'quote_update_interval': interval})
	elif user_type == 'supervisor':
		return redirect('supervisor_home')
	else:
		return redirect('login')

def login(request):
	if request.method == 'POST':
		# Student login form (default)
		if not request.POST.get('access_code'):
			email = request.POST.get('email')
			password = request.POST.get('password')
			try:
				student = Student.objects.get(email=email)
				if student.password == password:
					request.session['user_type'] = 'student'
					request.session['user_email'] = email
					return redirect('index')
			except Student.DoesNotExist:
				pass
			return render(request, 'login.html', {'error': 'Invalid student credentials'})
		# Supervisor login form
		elif request.POST.get('access_code'):
			email = request.POST.get('email')
			access_code = request.POST.get('access_code')
			password = request.POST.get('password')
			try:
				teacher = Teacher.objects.get(email=email, access_code=access_code)
				if teacher.password == password:
					request.session['user_type'] = 'supervisor'
					request.session['user_email'] = email
					return redirect('supervisor_home')
			except Teacher.DoesNotExist:
				pass
			return render(request, 'login.html', {'error': 'Invalid supervisor credentials'})
	return render(request, 'login.html')


# Supervisor home view
def supervisor_home(request):
	if request.session.get('user_type') != 'supervisor':
		return redirect('login')
	teacher = Teacher.objects.get(email=request.session['user_email'])
	return render(request, 'supervisor_home.html', {'teacher': teacher})

# Counsellor slot management view
def counsellor_slot_management(request):
	if request.session.get('user_type') != 'supervisor':
		return redirect('login')
	teacher = Teacher.objects.get(email=request.session['user_email'])
	if request.method == 'POST':
		CounsellorSlot.objects.create(
			counsellor_name=request.POST['counsellor_name'],
			specialization=request.POST['specialization'],
			day=request.POST['day'],
			start_time=request.POST['start_time'],
			end_time=request.POST['end_time'],
			created_by=teacher
		)
	slots = CounsellorSlot.objects.filter(created_by=teacher)
	return render(request, 'counsellor_slot_management.html', {'slots': slots})

def myspace(request):
	if not request.session.get('user_type'):
		return redirect('login')
	student_email = request.session.get('user_email')
	student = None
	entries = []
	if student_email:
		try:
			student = Student.objects.get(email=student_email)
			entries = JournalEntry.objects.filter(student=student).order_by('-date', '-time')
		except Student.DoesNotExist:
			pass
	if request.method == 'POST':
		entry_text = request.POST.get('entry_text')
		if entry_text and student:
			JournalEntry.objects.create(student=student, entry_text=entry_text)
			# Refresh entries after new entry
			entries = JournalEntry.objects.filter(student=student).order_by('-date', '-time')
	return render(request, 'myspace.html', {'entries': entries, 'student': student})

def support(request):
	if not request.session.get('user_type'):
		return redirect('login')
	if request.method == 'POST':
		date = request.POST.get('date')
		time = request.POST.get('time')
		counsellor = request.POST.get('counsellor')
		user = request.session.get('user_email', 'Anonymous')
		if date and time and counsellor:
			Appointment.objects.create(user=user, date=date, time=time, counsellor=counsellor)
			return render(request, 'support.html', {'success': 'Booking confirmed!'})
	return render(request, 'support.html')

def wellness(request):
	if not request.session.get('user_type'):
		return redirect('login')
	return render(request, 'wellness.html')

def logout_view(request):
		request.session.flush()
		return redirect('login')

# Student appointments view
def student_appointments(request):
	if request.session.get('user_type') != 'student':
		return redirect('login')
	student = Student.objects.get(email=request.session['user_email'])
	# Only show appointments and waiting list for slots created by supervisors from the student's institution
	appointments = Appointment.objects.filter(student=student, slot__created_by__institution=student.institution)
	waiting_list = WaitingList.objects.filter(student=student, slot__created_by__institution=student.institution)
	return render(request, 'student_appointments.html', {
		'appointments': appointments,
		'waiting_list': waiting_list,
	})
