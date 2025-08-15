from django.urls import path
from . import views

urlpatterns = [
    path('teachers', views.TeacherListView.as_view(), name='teacher-list'),
    path('lessons', views.TeacherLessonsView.as_view(), name='teacher-lessons'),
    path('statuses', views.StatusesView.as_view()),
    path('lesson/', views.LessonAPIView.as_view()),                  # POST
    path('lesson/<int:pk>/', views.LessonAPIView.as_view()),         # PUT, PATCH, DELETE

                       # POST
    path('note/', views.NoteAPIView.as_view()),                      # POST
    path('note/<int:pk>/', views.NoteAPIView.as_view()),             # PUT, PATCH, DELETE
]
