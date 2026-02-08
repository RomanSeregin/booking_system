from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Room, Booking
from .forms import BookingForm, RegisterForm
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib import messages



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'booking/register.html', {'form': form})

@login_required
def create_booking(request):
    rooms = Room.objects.all()  # получаем все комнаты

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('my_bookings')
    else:
        form = BookingForm(initial={'name': request.user.username})

    return render(request, 'booking/booking_form.html', {'form': form, 'rooms': rooms})

def bookings_api(request):
    bookings = Booking.objects.filter(status='confirmed')
    events = []
    for b in bookings:
        events.append({
            'title': b.room.name,
            'start': datetime.combine(b.start_date, datetime.min.time()).strftime('%Y-%m-%dT%H:%M:%S'),
            'end': (datetime.combine(b.end_date, datetime.min.time()) + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S'),
        })
    return JsonResponse(events, safe=False)

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронювання оновлено!')
            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/booking_form.html', {'form': form, 'edit': True})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Бронювання видалено!')
        return redirect('my_bookings')

    return render(request, 'booking/confirm_delete.html', {'booking': booking})

def room_list(request):
    rooms = Room.objects.all()

    room_type = request.GET.get('type')
    if room_type:
        rooms = rooms.filter(type=room_type)

    return render(request, 'booking/room_list.html', {
        'rooms': rooms
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


def home(request):
    return render(request, 'booking/home.html')