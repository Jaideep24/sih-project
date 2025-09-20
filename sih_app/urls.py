from django.urls import path
from . import views
from .quote_api import get_quote
from . import mood_api
from .supervisor_student_views import supervisor_student_list, supervisor_student_detail

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('myspace/', views.myspace, name='myspace'),
    path('peer/', views.peer, name='peer'),
    path('support/', views.support, name='support'),
    path('wellness/', views.wellness, name='wellness'),
    path('logout/', views.logout_view, name='logout'),
    path('supervisor/home/', views.supervisor_home, name='supervisor_home'),
    path('supervisor/counsellor/', views.counsellor_slot_management, name='counsellor_slot_management'),
    path('book-slot/', views.book_slot, name='book_slot'),
    path('supervisor/appointments/', views.supervisor_appointments, name='supervisor_appointments'),
    path('my-appointments/', views.student_appointments, name='student_appointments'),
    path('api/quote/', get_quote, name='get_quote'),
    path('api/save_mood/', mood_api.save_mood, name='save_mood'),
    path('api/mood_history/', mood_api.get_mood_history, name='mood_history'),
        path('supervisor/students/', supervisor_student_list, name='supervisor_student_list'),
        path('supervisor/students/<str:student_id>/', supervisor_student_detail, name='supervisor_student_detail'),
]
