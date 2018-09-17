from django.db import models

from common.models import AbstractBase

from users.models import User

from classes.models import Class


class Student(AbstractBase):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	date_of_birth = models.DateField()
	admission_number =  models.CharField(
		max_length=255, 
		null=True, 
		blank=True
	)
	student_class = models.ForeignKey(
		Class, 
		on_delete=models.PROTECT, 
		related_name='students',
	)

	def __str__(self):
		full_name = self.full_name

		return " ".join([
			full_name, self.admission_number or ""
		]).strip()

	@property
	def full_name(self):
		return " ".join([
			self.first_name, self.last_name
		]).strip()