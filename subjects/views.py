from rest_framework.viewsets import ModelViewSet

from subjects.models import Subject

from subjects.serializers import (
	SubjectSerializer,
)


class BaseViewSet(ModelViewSet):
	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)


class SubjectViewSet(BaseViewSet):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer