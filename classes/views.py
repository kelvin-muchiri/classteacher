from rest_framework.viewsets import ModelViewSet

from classes.models import Class

from classes.serializers import (
	ClassSerializer,
	ClassInlineSerializer,
)


class BaseViewSet(ModelViewSet):
	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)


class ClassViewSet(BaseViewSet):
	queryset = Class.objects.all()
	serializer_class = ClassSerializer

	def get_serializer_class(self):
		serializer_class = ClassSerializer
		if self.action in ['retrieve', 'list']:            
			serializer_class = ClassInlineSerializer
		return serializer_class
