from django.db import models

class Student(models.Model):
	email = models.EmailField(unique=True)
	student_id = models.CharField(max_length=20, unique=True)
	password = models.CharField(max_length=128)
	# Add more fields as needed

	def __str__(self):
		return f"{self.email} ({self.student_id})"

class Teacher(models.Model):
	email = models.EmailField(unique=True)
	access_code = models.CharField(max_length=20)
	password = models.CharField(max_length=128)
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

class Appointment(models.Model):
	user = models.CharField(max_length=100)
	date = models.DateField()
	time = models.TimeField()
	counsellor = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
