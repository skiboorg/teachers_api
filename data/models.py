from django.db import models

from user.models import User, Pupil

# Цвета по стандарту PrimeVue
TAG_COLOR_CHOICES = [
    ('primary', 'Primary'),
    ('secondary', 'Secondary'),
    ('success', 'Success'),
    ('info', 'Info'),
    ('warning', 'Warning'),
    ('help', 'Help'),
    ('danger', 'Danger'),
]
class NoteStatus(models.Model):
    name = models.CharField(max_length=100)
    tag_color = models.CharField(max_length=20, choices=TAG_COLOR_CHOICES)

    def __str__(self):
        return self.name


class Note(models.Model):
    text = models.TextField(blank=True, null=True)
    text1 = models.TextField(blank=True, null=True)
    text2 = models.TextField(blank=True, null=True)
    text3 = models.TextField(blank=True, null=True)
    status = models.ForeignKey(NoteStatus, on_delete=models.PROTECT)
    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.id}'



class LessonType(models.Model):
    name = models.CharField(max_length=100)
    tag_color = models.CharField(max_length=20, choices=TAG_COLOR_CHOICES)

    def __str__(self):
        return self.name


class LessonStatus(models.Model):
    name = models.CharField(max_length=100)
    tag_color = models.CharField(max_length=20, choices=TAG_COLOR_CHOICES)

    def __str__(self):
        return self.name


class PaymentStatus(models.Model):
    name = models.CharField(max_length=100)
    tag_color = models.CharField(max_length=20, choices=TAG_COLOR_CHOICES)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    pupils = models.ManyToManyField(Pupil, related_name='lessons', verbose_name='Ученики')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    lesson_type = models.ForeignKey(LessonType, on_delete=models.PROTECT)
    status = models.ForeignKey(LessonStatus, on_delete=models.PROTECT)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT, blank=True, null=True)
    pupils_text = models.TextField(blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.lesson_type.name} ({self.date}) - {self.teacher}"
