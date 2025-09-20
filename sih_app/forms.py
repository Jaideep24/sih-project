from django import forms
from .models import ChatRoom

# Form for creating a chat room
class ChatRoomCreateForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'category']

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class JournalForm(forms.Form):
    entry = forms.CharField(widget=forms.Textarea, label='Journal Entry')

class BookingForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    counsellor = forms.ChoiceField(choices=[('Dr. Patel', 'Dr. Patel'), ('Ms. Rivera', 'Ms. Rivera'), ('Mr. Chen', 'Mr. Chen')])
