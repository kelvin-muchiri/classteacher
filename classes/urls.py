from rest_framework.routers import SimpleRouter

from classes import views

router = SimpleRouter()
router.register(r'', views.ClassViewSet)

urlpatterns = router.urls