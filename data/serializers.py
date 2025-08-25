from rest_framework import serializers

from user.models import User
from user.serializers import UserSerializer
from .models import *

class NoteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteStatus
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    status = NoteStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=NoteStatus.objects.all(), source='status', write_only=True
    )
    class Meta:
        model = Note
        fields = '__all__'


class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = '__all__'


class LessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonStatus
        fields = '__all__'


class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='teacher', write_only=True
    )
    lesson_type_id = serializers.PrimaryKeyRelatedField(
        queryset=LessonType.objects.all(), source='lesson_type', write_only=True
    )
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=LessonStatus.objects.all(), source='status', write_only=True
    )
    payment_status_id = serializers.PrimaryKeyRelatedField(
        queryset=PaymentStatus.objects.all(),
        source='payment_status',
        write_only=True,
        required=False,
        allow_null=True
    )

    # Read-only nested serializers for output
    lesson_type = LessonTypeSerializer(read_only=True)
    status = LessonStatusSerializer(read_only=True)
    payment_status = PaymentStatusSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'teacher_id', 'lesson_type_id', 'status_id', 'payment_status_id',
            'created_at','pupils', 'comment','comment_hidden','pupils_text', 'lesson_type', 'status', 'payment_status',
            'date', 'start_time', 'end_time'
        ]
