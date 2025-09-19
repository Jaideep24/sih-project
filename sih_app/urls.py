from django.urls import path
from . import views
from .quote_api import get_quote

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
]
