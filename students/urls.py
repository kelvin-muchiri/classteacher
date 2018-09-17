from rest_framework.routers import SimpleRouter

from students import views

router = SimpleRouter()
router.register(r'', views.StudentViewSet)

urlpatterns = router.urls