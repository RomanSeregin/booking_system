from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Booking, Room



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class BookingForm(forms.ModelForm):
    # добавляем поле имени
    name = forms.CharField(label='Ваше ім’я', max_length=100)

    class Meta:
        model = Booking
        fields = ['name', 'room', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.order_by('type', 'name')

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if room and start_date and end_date:
            conflicts = Booking.objects.filter(
                room=room,
                status='confirmed',
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            if conflicts.exists():
                raise ValidationError("Цей період зайнятий, виберіть інший.")

        return cleaned_data