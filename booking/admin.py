from django.contrib import admin
from .models import Room, Booking

from django.contrib import admin
from .models import Room, Booking

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity', 'price_per_day')  # <-- исправлено
    list_filter = ('type',)
    search_fields = ('name', 'features')

admin.site.register(Room, RoomAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'room')
    search_fields = ('user__username', 'room__name')

admin.site.register(Booking, BookingAdmin)