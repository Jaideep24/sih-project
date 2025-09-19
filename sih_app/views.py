def dashboard(request):
	return render(request, 'dashboard.html')
# Student: view appointments and waiting list status
def student_appointments(request):
	if request.session.get('user_type') != 'student':
		return redirect('login')
	student = Student.objects.get(email=request.session['user_email'])
	appointments = Appointment.objects.filter(student=student)
	waiting_list = WaitingList.objects.filter(student=student)
	return render(request, 'student_appointments.html', {
		'appointments': appointments,
		'waiting_list': waiting_list,
	})
# Supervisor: manage appointments and waiting list
def supervisor_appointments(request):
	if request.session.get('user_type') != 'supervisor':
		return redirect('login')
	teacher = Teacher.objects.get(email=request.session['user_email'])
	slots = CounsellorSlot.objects.filter(created_by=teacher)
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
				# Confirm this student, create appointment, remove from waiting list
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
from .models import CounsellorSlot, Appointment, WaitingList

# Student slot booking and waiting list view
def book_slot(request):
	if request.session.get('user_type') != 'student':
		return redirect('login')
	student = Student.objects.get(email=request.session['user_email'])
	slots = CounsellorSlot.objects.filter(is_active=True)
	booked_appointments = Appointment.objects.filter(student=student)
	booked_slot_ids = [a.slot.id for a in booked_appointments]
	slot_statuses = {a.slot.id: a.status for a in booked_appointments}
	waiting_list = WaitingList.objects.filter(student=student)
	waiting_slot_ids = [w.slot.id for w in waiting_list]
	if request.method == 'POST':
		slot_id = request.POST.get('slot_id')
		slot = CounsellorSlot.objects.get(id=slot_id)
		# Check if slot is already booked by another student
		if Appointment.objects.filter(slot=slot, status='confirmed').exists():
			# Add to waiting list if not already
			if not WaitingList.objects.filter(slot=slot, student=student).exists():
				WaitingList.objects.create(slot=slot, student=student)
		else:
			Appointment.objects.create(slot=slot, student=student, status='confirmed')
		# Refresh data after booking
		booked_appointments = Appointment.objects.filter(student=student)
		booked_slot_ids = [a.slot.id for a in booked_appointments]
		slot_statuses = {a.slot.id: a.status for a in booked_appointments}
		waiting_list = WaitingList.objects.filter(student=student)
		waiting_slot_ids = [w.slot.id for w in waiting_list]
	return render(request, 'book_slot.html', {
		'slots': slots,
		'booked_slot_ids': booked_slot_ids,
		'slot_statuses': slot_statuses,
		'waiting_list': waiting_list,
		'waiting_slot_ids': waiting_slot_ids,
	})
def signup(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		student_id = request.POST.get('student_id')
		if Student.objects.filter(email=email).exists():
			return render(request, 'signup.html', {'error': 'Email already exists'})
		Student.objects.create(email=email, password=password, student_id=student_id)
		return redirect('login')
	return render(request, 'signup.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from .models import Student, Teacher

from django.shortcuts import render

from .models import SiteSetting
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
		# Determine which form was submitted by checking for unique fields
		if request.POST.get('student_id'):
			# Student login form
			email = request.POST.get('email')
			student_id = request.POST.get('student_id')
			password = request.POST.get('password')
			try:
				student = Student.objects.get(email=email, student_id=student_id)
				if student.password == password:
					request.session['user_type'] = 'student'
					request.session['user_email'] = email
					return redirect('index')
			except Student.DoesNotExist:
				pass
			return render(request, 'login.html', {'error': 'Invalid student credentials'})
		elif request.POST.get('access_code'):
			# Supervisor login form
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
	return render(request, 'supervisor_home.html')

# Counsellor slot management view
from .models import CounsellorSlot
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

from .models import JournalEntry

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
	return render(request, 'myspace.html', {'entries': entries})

def peer(request):
	if not request.session.get('user_type'):
		return redirect('login')
	return render(request, 'peer.html')

def support(request):
	if not request.session.get('user_type'):
		return redirect('login')
	if request.method == 'POST':
		date = request.POST.get('date')
		time = request.POST.get('time')
		counsellor = request.POST.get('counsellor')
		user = request.session.get('user_email', 'Anonymous')
		if date and time and counsellor:
			from .models import Appointment
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
