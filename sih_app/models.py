
from django.db import models
# MoodEntry model for storing mood history in DB
class MoodEntry(models.Model):
	student = models.ForeignKey('Student', on_delete=models.CASCADE)
	mood = models.PositiveSmallIntegerField()
	timestamp = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.student} - Mood: {self.mood} at {self.timestamp}"

class Institution(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __str__(self):
		return self.name
# Site-wide settings for quote update interval
class SiteSetting(models.Model):
	quote_update_interval = models.PositiveIntegerField(default=3600, help_text="Quote update interval in seconds")
	def __str__(self):
		return f"Site Settings (Quote interval: {self.quote_update_interval}s)"

class Student(models.Model):
	email = models.EmailField(unique=True)
	student_id = models.CharField(max_length=20, unique=True)
	password = models.CharField(max_length=128)
	institution = models.ForeignKey('Institution', on_delete=models.CASCADE, null=True, blank=True)
	# Add more fields as needed

	def __str__(self):
		return f"{self.email} ({self.student_id})"

class Teacher(models.Model):
	email = models.EmailField(unique=True)
	access_code = models.CharField(max_length=20)
	password = models.CharField(max_length=128)
	institution = models.ForeignKey('Institution', on_delete=models.CASCADE, null=True, blank=True)
	# Add more fields as needed

	def __str__(self):
		return f"{self.email} (Supervisor)"
class JournalEntry(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	entry_text = models.TextField()
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.student.student_id} - {self.date} {self.time}"


# New model for counsellor slots
class CounsellorSlot(models.Model):
	counsellor_name = models.CharField(max_length=100)
	specialization = models.CharField(max_length=100)
	day = models.CharField(max_length=20)  # e.g., Monday, Tuesday
	start_time = models.TimeField()
	end_time = models.TimeField()
	created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return f"{self.counsellor_name} ({self.specialization}) {self.day} {self.start_time}-{self.end_time}"

# Appointment with status and slot reference
class Appointment(models.Model):
	STATUS_CHOICES = [
		("confirmed", "Confirmed"),
		("completed", "Completed"),
		("cancelled", "Cancelled"),
		("waiting", "Waiting List"),
	]
	slot = models.ForeignKey(CounsellorSlot, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmed")
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.student} - {self.slot} ({self.status})"

# Waiting list for slots
class WaitingList(models.Model):
	slot = models.ForeignKey(CounsellorSlot, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"Waiting: {self.student} for {self.slot}"
