from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, room_list, create_booking, register, my_bookings, bookings_api, edit_booking, delete_booking

urlpatterns = [
    path('', home, name='home'),
    path('rooms/', room_list, name='rooms'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('booking/', create_booking, name='booking'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('api/bookings/', bookings_api, name='bookings_api'),
    path('booking/edit/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('booking/delete/<int:booking_id>/', delete_booking, name='delete_booking'),
]