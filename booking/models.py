from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    ROOM_TYPES = [
        ('auditorium', 'Аудиторія'),
        ('conference', 'Конференц-зал'),
        ('lab', 'Лабораторія'),
        ('other', 'Інше'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ROOM_TYPES, default='other')
    capacity = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=1000)  # дефолтная цена
    features = models.TextField(
        verbose_name="Особливості (проєктор, Wi-Fi, дошка тощо)"
    )

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.room.name}"