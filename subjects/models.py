from django.db import models

from common.models import AbstractBase


class Subject(AbstractBase):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=10, null=True, blank=True)

	def __str__(self):
		return self.name