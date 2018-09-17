from rest_framework.routers import SimpleRouter

from subjects import views

router = SimpleRouter()
router.register(r'', views.SubjectViewSet)

urlpatterns = router.urls