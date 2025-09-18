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

def index(request):
	if not request.session.get('user_type'):
		return redirect('login')
	return render(request, 'index.html')

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
					return redirect('admin')
			except Teacher.DoesNotExist:
				pass
			return render(request, 'login.html', {'error': 'Invalid supervisor credentials'})
	return render(request, 'login.html')

def admin_view(request):
	if request.session.get('user_type') != 'supervisor':
		return redirect('login')
	return render(request, 'admin.html')

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
