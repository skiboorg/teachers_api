from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ReelsIdeaViewSet, MasterClassIdeaViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"reels-ideas", ReelsIdeaViewSet)
router.register(r"masterclass-ideas", MasterClassIdeaViewSet)

urlpatterns = router.urls
