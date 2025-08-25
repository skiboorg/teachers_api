from django.urls import path,include
from . import views

urlpatterns = [
    path('me', views.GetUser.as_view()),
    path('update', views.UpdateUser.as_view()),
    path('activate', views.ActivateUser.as_view()),
    path('reset', views.ResetPassword.as_view()),
    path('pupils', views.GetPupils.as_view()),

]
