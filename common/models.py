import uuid

from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings

from common.utilities import (
	GENDER_CHOICES,
	CURRICULUM_CHOICES,
	CATEGORY_CHOICES,
)

from phonenumber_field.modelfields import PhoneNumberField

class SoftDeletionQuerySet(QuerySet):
	def delete(self):
		return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now(), 
			is_deleted=True, is_active=False)

	def hard_delete(self):
		return super(SoftDeletionQuerySet, self).delete()

	def alive(self):
		return self.filter(deleted_at=None)

	def dead(self):
		return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
	def __init__(self, *args, **kwargs):
		self.alive_only = kwargs.pop('alive_only', True)
		super(SoftDeletionManager, self).__init__(*args, **kwargs)

	def get_queryset(self):
		if self.alive_only:
			return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
		return SoftDeletionQuerySet(self.model)

	def hard_delete(self):
		return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
	deleted_at = models.DateTimeField(blank=True, null=True)
	is_deleted = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	objects = SoftDeletionManager()
	all_objects = SoftDeletionManager(alive_only=False)

	class Meta:
		abstract = True

	def delete(self):
		self.deleted_at = timezone.now()
		self.is_deleted = True
		self.is_active = False
		self.save()

	def hard_delete(self):
		super(SoftDeletionModel, self).delete()

class AbstractBase(SoftDeletionModel):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, blank=True,
		on_delete=models.PROTECT,
		related_name="%(app_label)s_%(class)s_related",
		related_query_name="%(app_label)s_%(class)ss",
	)
	
	class Meta:
		abstract = True
		ordering = ('-updated_at', '-created_at')