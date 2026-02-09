from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"reels-ideas", ReelsIdeaViewSet)
router.register(r"masterclass-ideas", MasterClassIdeaViewSet)



urlpatterns = [
    path('r_tags', ReelsTagListView.as_view()),
    path('r_filters', ReelsFilterListView.as_view()),
    path('mk_tags', MKTagListView.as_view()),
] + router.urls