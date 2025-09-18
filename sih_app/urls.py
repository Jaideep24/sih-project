from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin/', views.admin_view, name='admin'),
    path('myspace/', views.myspace, name='myspace'),
    path('peer/', views.peer, name='peer'),
    path('support/', views.support, name='support'),
    path('wellness/', views.wellness, name='wellness'),
]
