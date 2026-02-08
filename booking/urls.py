from django.urls import path
from django.contrib.auth import views as auth_views
from .views import room_list, create_booking, register, my_bookings

urlpatterns = [
    path('', room_list, name='rooms'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('booking/', create_booking, name='booking'),
    path('my-bookings/', my_bookings, name='my_bookings'),
]