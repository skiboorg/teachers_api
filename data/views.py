from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


class TeacherListView(APIView):
    def get(self, request):
        teachers = User.objects.all()
        serializer = UserSerializer(teachers, many=True)
        return Response(serializer.data)


class StatusesView(APIView):
    def get(self, request):
        note_statuses = NoteStatus.objects.all()
        lesson_types = LessonType.objects.all()
        lesson_statuses = LessonStatus.objects.all()
        payment_statuses = PaymentStatus.objects.all()

        return Response({
            'note_statuses': NoteStatusSerializer(note_statuses, many=True).data,
            'lesson_types': LessonTypeSerializer(lesson_types, many=True).data,
            'payment_statuses': PaymentStatusSerializer(payment_statuses, many=True).data,
            'lesson_statuses': LessonStatusSerializer(lesson_statuses, many=True).data,
        },status=200)


class TeacherLessonsView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        teacher = get_object_or_404(User, id=user_id)
        lessons = Lesson.objects.filter(teacher=teacher).order_by('-date', '-start_time')
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonAPIView(APIView):
    def post(self, request):
        """Создание урока"""
        print(request.data)
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Полное обновление урока"""
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Частичное обновление урока"""
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Удаление урока"""
        lesson = get_object_or_404(Lesson, pk=pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class NoteAPIView(APIView):
    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Создание заметки"""
        print(request.data)
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Полное обновление заметки"""
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Частичное обновление заметки"""
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Удаление заметки"""
        note = get_object_or_404(Note, pk=pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
