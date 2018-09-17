from django.db import models

from common.models import AbstractBase

from users.models import User


class Class(AbstractBase):
	name = models.CharField(max_length=25, unique=True)
	description = models.TextField(null=True, blank=True)
	class_teacher = models.ForeignKey(
		User, 
		on_delete=models.SET_NULL, 
		related_name='class_teacher_of',
		null=True,
    	blank=True
	)

	def __str__(self):
		return self.name
