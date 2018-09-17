from rest_framework.viewsets import ModelViewSet

from students.models import Student

from students.serializers import (
	StudentSerializer,
	StudentInlineSerializer
)


class BaseViewSet(ModelViewSet):
	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)


class StudentViewSet(BaseViewSet):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer

	def get_serializer_class(self):
		serializer_class = StudentSerializer
		if self.action in ['retrieve', 'list']:            
			serializer_class = StudentInlineSerializer
		return serializer_class